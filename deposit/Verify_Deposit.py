#!/usr/bin/env python3
"""Verify the reconstructed 16-file deposit and its recorded replay bindings.

Requires Python's standard library only. This is an exhaustive release-byte,
source-identity and endpoint verifier, not an execution of the mathematical
consumers. Run the separate 15-stage replay for fresh mathematical execution.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
import argparse
import ast
import gzip
import hashlib
import json
import re
import stat
import sys
import zipfile

sys.set_int_max_str_digits(100000)
DOI = '10.5281/zenodo.23752103'
VERSION_NOTE = 'This edition supersedes referee edition 3 of 28 October 2026; the numerical plan, source table and comparison history are unchanged; Appendix B adds the direct source reconstruction.'
EXPECTED = {
    'Unconditional_0107965.pdf', 'Unconditional_0107965.tex',
    'Matched_Source_Supplement.pdf', 'Further_Consequences.pdf',
    'Verification_Guide.pdf', 'Prior_Analytic_Foundations.pdf',
    'Prior_Correlated_Translated_Probes.pdf', 'Manuscript_Sources.zip',
    'Proof_and_Replay.zip', 'README.md', 'CITATION.cff', 'LICENSES_AND_RIGHTS.md',
    'Release_Manifest.json', 'Verification_Receipt.json', 'Verify_Deposit.py',
    'SHA256SUMS.txt'}
CURRENT_TEX = {'Unconditional_0107965.tex', 'Matched_Source_Supplement.tex',
               'Further_Consequences.tex', 'Verification_Guide.tex'}
PREFIX = 'Proof_and_Replay/Lambda_Peer_Review/'
SUPPORT = 'Proof_and_Replay/Release_Support/'
ENDPOINT = F(427693072077942473661578098491,
             3961408125713216879677197516800)
ORIGINAL_MANIFEST_SHA = 'd817cf1d62f2c98db594f2fc580bb4492903419b914aabb3f434f31ccae3a59d'
DIRECT_CHECKER_SHA = 'a0e8cca86919957d82b714413adc4cc967a32aee94c8b521554d6d2a8a01ce19'
PRIOR_HASHES = {
    'Prior_Analytic_Foundations.pdf': 'fe06339d12cfefe00b9da826ff812e31bb1be3cdaa698b78d4d85ad8b0ae53a9',
    'Prior_Correlated_Translated_Probes.pdf': 'ad3e552b7429e685514cfa4ccfadebe9daf382c8000d95afb584932f0e226787'}
FIXED_NUMERICAL_BINDINGS = {
    'verification/source_overlays/ALL67_OPERATIONAL_SOURCE_TABLE.json':
        'ad015e0b765c20068bd690890bbbf07e48d0d2437c67ae6ff753a445ac255657',
    'inputs/workspace/lambda_round15/flow_main_v2/MAIN_CLOCK_SOURCE.json':
        'b59905d7b994d3424ba14f9347be75a2429ae4d4b0de2c2404971ffda1d4d536',
    'inputs/workspace/lambda_round14/material/m8_late/M8_LATE_PLAN.json':
        'ec346b7c1136eda38021eb6323033b3b48ed21e6f7458eeeac7cc9579db2497a',
    'inputs/workspace/lambda_round16/ordinary_7_8_flow/full_flow/FLOW.json.gz':
        'a664e829a3681d96e474bcf875d80cba7b16fe8f65e050c69f01b5ea07de4737',
    'verification/arcs/COMPACT_ALL_ARC_MARGIN_LOWER_BOUNDS.jsonl.gz':
        '77cad9fb775100704100311640f786656afecf831d795a0e2cdd57f51e27735d'}
STEPS = {
    'native': 'source_primitives/check_native_primitives.py',
    'activation': 'source_primitives/check_activation_primitives.py',
    'spectral': 'referee/check_all_spectral_envelopes.py',
    'affine': 'referee/check_original_affine_native.py',
    'heads28': 'head_and_phase/verify_head_and_phase.py',
    'heads39': 'global_analytic/check_retained_39_heads.py',
    'wall': 'global_analytic/check_wall_and_physical.py',
    'overlays': 'source_overlays/verify_source_overlays_independent.py',
    'kernel': 'kernel/verify_all67_independent.py',
    'arcs': 'arcs/verify_arcs_fresh.py',
    'compact-arcs': 'arcs/compact_arc_witnesses.py',
    'interfaces': 'referee/check_mathematical_interfaces.py',
    'physical-debit-map': 'review/physical_debit/verify_physical_debit_map.py',
    'arithmetic-credit-map': 'review/arithmetic_credit/build_credit_audit.py',
    'direct-source': 'direct_source/verify_direct_source.py'}
GROUPS = [
    ['native', 'activation', 'spectral', 'heads28', 'heads39', 'wall', 'kernel', 'arcs'],
    ['affine', 'overlays', 'compact-arcs'],
    ['interfaces', 'physical-debit-map', 'arithmetic-credit-map'],
    ['direct-source']]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def stream_hash(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(1024*1024), b''):
        h.update(block)
    return h.hexdigest()


def file_hash(path):
    with path.open('rb') as stream:
        return stream_hash(stream)


def valid_path(name, directory=False):
    if directory:
        name = name.rstrip('/')
    p = PurePosixPath(name)
    return (bool(name) and not p.is_absolute() and '\\' not in name and
            '\0' not in name and not name.split('/')[0].endswith(':') and
            all(x not in ('', '.', '..') for x in name.split('/')))


def archive_safety(archive):
    names = set()
    for info in archive.infolist():
        need(valid_path(info.filename, info.is_dir()), 'Unsafe ZIP path: '+info.filename)
        need(info.filename not in names, 'Duplicate ZIP path: '+info.filename)
        names.add(info.filename)
        mode = stat.S_IFMT(info.external_attr >> 16)
        need(mode in (0, stat.S_IFREG, stat.S_IFDIR), 'Non-regular ZIP entry: '+info.filename)
        need(not (info.flag_bits & 1), 'Encrypted ZIP entry: '+info.filename)
    need(archive.testzip() is None, 'ZIP CRC failure')
    return {n for n in names if not n.endswith('/')}


def list_manifest(document, label):
    entries = document['files']
    need(isinstance(entries, list), label+' must use a files array')
    result = {}
    for entry in entries:
        name = entry['path']
        need(valid_path(name) and name not in result, label+' has unsafe/duplicate path')
        need(type(entry['bytes']) is int and entry['bytes'] >= 0 and
             re.fullmatch('[0-9a-f]{64}', entry['sha256']) is not None,
             label+' has invalid identity: '+name)
        result[name] = entry
    if 'file_count' in document:
        need(document['file_count'] == len(result), label+' count mismatch')
    if 'total_bytes' in document:
        need(document['total_bytes'] == sum(e['bytes'] for e in result.values()),
             label+' total-byte mismatch')
    return result


def checked_steps(value, label):
    need(isinstance(value, list) and len(value) == 15, label+' must contain fifteen stages')
    names = [r['step'] for r in value]
    need(len(set(names)) == 15 and set(names) == set(STEPS), label+' stage inventory mismatch')
    need(all(type(r['exit_code']) is int and r['exit_code'] == 0 for r in value),
         label+' reports a failing/noninteger exit code')
    return {r['step']: r['exit_code'] for r in value}


def check_cff_dois(text):
    """Read this release's block-style CFF DOI fields, excluding references."""
    top_dois = []
    preferred_fields = []
    preferred_sections = 0
    section = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = re.fullmatch(r'( *)([A-Za-z][A-Za-z0-9_-]*):(?: +(.*))?', line)
        if match is None:
            continue
        indent, key, value = len(match[1]), match[2], (match[3] or '').strip()
        if indent == 0:
            section = key
            if key == 'doi':
                top_dois.append(value)
            elif key == 'preferred-citation':
                preferred_sections += 1
                need(not value, 'Expected block-style preferred-citation')
        elif section == 'preferred-citation':
            preferred_fields.append((indent, key, value))

    def scalar(value):
        value = re.sub(r'\s+#.*$', '', value).strip()
        if value[:1] in ('\"', "'"):
            need(len(value) >= 2 and value[-1] == value[0], 'Malformed quoted CFF DOI')
            value = value[1:-1]
        return value

    need(len(top_dois) == 1 and scalar(top_dois[0]) == DOI, 'CFF top-level DOI inconsistent')
    need(preferred_sections == 1 and preferred_fields, 'Missing or duplicate CFF preferred-citation')
    depth = min(item[0] for item in preferred_fields)
    preferred_dois = [value for indent, key, value in preferred_fields
                      if indent == depth and key == 'doi']
    need(len(preferred_dois) == 1 and scalar(preferred_dois[0]) == DOI,
         'CFF preferred-citation DOI inconsistent')


def verify(directory):
    need(directory.is_dir() and not directory.is_symlink(), 'Public folder missing or linked')
    actual = {p.name for p in directory.iterdir() if not p.name.startswith('.')}
    need(actual == EXPECTED, 'Public inventory mismatch: missing='+str(sorted(EXPECTED-actual))+
         ', extra='+str(sorted(actual-EXPECTED)))
    for name in EXPECTED:
        p = directory/name
        need(p.is_file() and not p.is_symlink(), 'Missing or linked public file: '+name)
    manifest = json.loads((directory/'Release_Manifest.json').read_text())
    need(manifest['schema'] == 'BCLD_RECONSTRUCTED_DEPOSIT_V1', 'Wrong release schema')
    need(manifest['doi'] == DOI, 'Wrong release DOI')
    need(manifest['version_note'] == VERSION_NOTE, 'Release version note mismatch')
    need(manifest['public_file_count'] == 16 and F(manifest['upper_exact']) == ENDPOINT,
         'Wrong release file count or endpoint')
    payloads = EXPECTED-{'Release_Manifest.json', 'SHA256SUMS.txt'}
    need(set(manifest['files']) == payloads, 'Release manifest must bind fourteen public payloads')
    hashes = {}
    for name in EXPECTED:
        hashes[name] = file_hash(directory/name)
    for name, entry in manifest['files'].items():
        p = directory/name
        need(p.stat().st_size == entry['bytes'] and hashes[name] == entry['sha256'],
             'Public identity mismatch: '+name)
        if name.endswith('.pdf'):
            with p.open('rb') as f:
                need(f.read(5) == b'%PDF-', 'Invalid PDF header: '+name)
    sums = {}
    for line in (directory/'SHA256SUMS.txt').read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([^/\\]+)', line)
        need(match is not None, 'Malformed public checksum line')
        sha, name = match.groups()
        need(name not in sums, 'Duplicate public checksum entry')
        sums[name] = sha
    need(set(sums) == EXPECTED-{'SHA256SUMS.txt'}, 'Public checksum coverage mismatch')
    for name, sha in sums.items():
        need(hashes[name] == sha, 'Public checksum mismatch: '+name)
    for name, sha in PRIOR_HASHES.items():
        need(hashes[name] == sha, 'Historical PDF changed: '+name)
    need(DOI in (directory/'README.md').read_text(), 'README lacks reserved DOI')
    check_cff_dois((directory/'CITATION.cff').read_text())

    receipt = json.loads((directory/'Verification_Receipt.json').read_text())
    need(receipt['schema'] == 'BCLD_RECONSTRUCTED_VERIFICATION_V1', 'Wrong verification receipt schema')
    need(receipt['doi'] == DOI and receipt['version_note'] == VERSION_NOTE,
         'Receipt DOI or version note mismatch')
    finite = receipt['finite_replay']
    need(finite['status'] == 'PASS' and finite['passed_steps'] == 15,
         'No complete fifteen-stage passing receipt')
    need(finite['assertions_enabled'] is True and
         finite['historical_filesystem_fallback'] is False and
         finite['discovery_mode'] is False, 'Fresh replay mode/assertion safeguards missing')
    public_steps = checked_steps(finite['steps'], 'Public replay receipt')
    source_ids = receipt['current_manuscript_sources']
    need(set(source_ids) == CURRENT_TEX, 'Current source archive must bind four matching TeX files')
    with zipfile.ZipFile(directory/'Manuscript_Sources.zip') as sources:
        source_names = archive_safety(sources)
        need(all(n.startswith('Manuscript_Sources/') for n in source_names),
             'Unexpected manuscript-source root')
        for name, entry in source_ids.items():
            member = 'Manuscript_Sources/'+name
            data = sources.read(member)
            need(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'],
                 'Current manuscript-source binding mismatch: '+name)
            need(DOI.encode() in data, 'Current TeX lacks reserved DOI: '+name)
        need(sources.read('Manuscript_Sources/Unconditional_0107965.tex') ==
             (directory/'Unconditional_0107965.tex').read_bytes(), 'Public/source-archive main TeX mismatch')

    with zipfile.ZipFile(directory/'Proof_and_Replay.zip') as proof:
        names = archive_safety(proof)
        digest_cache = {}

        def member_hash(name):
            if name not in digest_cache:
                with proof.open(name) as f:
                    digest_cache[name] = stream_hash(f)
            return digest_cache[name]

        def read_json(name):
            return json.loads(proof.read(name))

        def identity(name, entry):
            need(name in names and proof.getinfo(name).file_size == entry['bytes'] and
                 member_hash(name) == entry['sha256'], 'Archive identity mismatch: '+name)

        inner = list_manifest(read_json(PREFIX+'BUNDLE_MANIFEST.json'), 'Scientific manifest')
        support = list_manifest(read_json(SUPPORT+'SUPPORT_MANIFEST.json'), 'Support manifest')
        actual_inner = {n[len(PREFIX):] for n in names if n.startswith(PREFIX)}
        actual_support = {n[len(SUPPORT):] for n in names if n.startswith(SUPPORT)}
        need(actual_inner == set(inner)|{'BUNDLE_MANIFEST.json'}, 'Scientific manifest coverage mismatch')
        need(actual_support == set(support)|{'SUPPORT_MANIFEST.json'}, 'Support manifest coverage mismatch')
        need(names == {PREFIX+n for n in actual_inner}|{SUPPORT+n for n in actual_support}|
             {'Proof_and_Replay/START_HERE.txt'}, 'Unmanifested proof-archive root payload')
        for name, entry in inner.items():
            identity(PREFIX+name, entry)
        for name, entry in support.items():
            identity(SUPPORT+name, entry)
        original_name = SUPPORT+'SOURCE_BUNDLE_MANIFEST.json'
        need(member_hash(original_name) == ORIGINAL_MANIFEST_SHA, 'Original scientific manifest changed')
        original = list_manifest(read_json(original_name), 'Original scientific manifest')
        original_consumers = {
            ('review/'+s[len('review/'):] if s.startswith('review/') else 'verification/'+s)
            for n, s in STEPS.items() if n != 'direct-source'}
        protected = {n for n in original if n.startswith(('inputs/', 'runtime/')) or
                     n in original_consumers or
                     re.fullmatch(r'verification/kernel/ROW_\d{3}_ACTUAL_CERTIFICATE.json.gz', n)}
        need(len(original_consumers) == 14 and original_consumers <= set(original),
             'Original fourteen scientific consumers missing from original record')
        for name in protected:
            need(name in inner and inner[name]['bytes'] == original[name]['bytes'] and
                 inner[name]['sha256'] == original[name]['sha256'],
                 'Original mathematical input/runtime/consumer changed: '+name)
        for name, sha in FIXED_NUMERICAL_BINDINGS.items():
            need(member_hash(PREFIX+name) == sha, 'Immutable source/kernel/flow binding changed: '+name)
        direct_code = 'verification/direct_source/verify_direct_source.py'
        need(member_hash(PREFIX+direct_code) == DIRECT_CHECKER_SHA, 'Direct-source consumer changed')
        for ext in ('pdf', 'tex'):
            need(proof.read(PREFIX+'manuscript/Proof_Peer_Review.'+ext) ==
                 (directory/('Unconditional_0107965.'+ext)).read_bytes(),
                 'Public/proof-archive current main mismatch: '+ext)
            alias = PREFIX+'manuscript/main.'+ext
            if alias in names:
                need(proof.read(alias) == (directory/('Unconditional_0107965.'+ext)).read_bytes(),
                     'Current manuscript alias mismatch: '+ext)

        driver_values = {}
        tree = ast.parse(proof.read(PREFIX+'replay/run.py').decode())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ('STEPS', 'GROUPS'):
                        need(target.id not in driver_values, 'Duplicate driver stage/group declaration')
                        driver_values[target.id] = ast.literal_eval(node.value)
        need(driver_values.get('STEPS') == STEPS and driver_values.get('GROUPS') == GROUPS,
             'Actual fifteen-stage driver or dependency groups mismatch')

        def evidence_path(key):
            name = finite[key+'_path']
            need(valid_path(name) and name.startswith(SUPPORT) and name in names,
                 'Invalid replay evidence path: '+key)
            need(member_hash(name) == finite[key+'_sha256'], 'Replay evidence hash mismatch: '+key)
            return name

        core_name = evidence_path('core_manifest')
        run_name = evidence_path('run_receipt')
        direct_name = evidence_path('direct_source_receipt')
        core = list_manifest(read_json(core_name), 'Fresh-run core identity manifest')
        kernel_names = {n for n in inner if
                        re.fullmatch(r'verification/kernel/ROW_\d{3}_ACTUAL_CERTIFICATE.json.gz', n)}
        need(len(kernel_names) == 67, 'Expected exactly 67 actual kernel certificates')
        required_core = {n for n in inner if n.startswith(('inputs/', 'runtime/')) or
                         (n.startswith(('verification/', 'review/')) and n.endswith('.py'))}
        required_core |= {'replay/run.py', 'replay/launch.py', 'verify_bundle.py'}|kernel_names
        need(required_core <= set(core) <= set(inner), 'Fresh-run core identity coverage incomplete')
        for name, entry in core.items():
            need(entry['bytes'] == inner[name]['bytes'] and entry['sha256'] == inner[name]['sha256'],
                 'Delivered core differs from recorded fresh-run core: '+name)
        run = read_json(run_name)
        need(run['all_requested_pass'] is True and run['all_required_steps'] is True and
             run['discovery_mode'] is False and run['historical_filesystem_fallback'] is False,
             'Actual execution receipt does not certify a strict complete run')
        need(checked_steps(run['steps'], 'Actual execution receipt') == public_steps,
             'Public and actual replay step records differ')

        dependency_doc = read_json(PREFIX+'replay/INPUT_DEPENDENCY_MANIFEST.json')
        deps = list_manifest(dependency_doc, 'Raw-input dependency manifest')
        need(len(deps) == 170, 'Immutable raw-input closure must contain 170 files')
        for name, entry in deps.items():
            identity(PREFIX+'inputs/'+name, entry)
            need('inputs/'+name in core, 'Raw dependency absent from fresh-run core: '+name)
        access_prefix = finite['access_logs_prefix']
        need(access_prefix.startswith(SUPPORT) and access_prefix.endswith('/') and
             valid_path(access_prefix, True), 'Invalid fresh access-log prefix')
        all_reads = set()
        direct_reads = None
        for stage, script in STEPS.items():
            if script.startswith('review/'):
                actual_script = script[len('review/'):]
                basename = 'review__'+actual_script.replace('/', '__')+'.json'
            else:
                actual_script = script
                basename = script.replace('/', '__')+'.json'
            access = read_json(access_prefix+basename)
            need(access['script'] == actual_script and access['discovery'] is False and
                 access['historical_access_fallback'] is False,
                 'Fresh access-mode or script mismatch: '+stage)
            reads = access['raw_inputs_read']
            need(isinstance(reads, list) and len(reads) == len(set(reads)),
                 'Duplicate raw input access inventory: '+stage)
            for name in reads:
                need(valid_path(name) and 'workspace/'+name in deps,
                     'Actual replay read outside frozen raw-input closure: '+name)
            all_reads.update(reads)
            if stage == 'direct-source':
                direct_reads = set(reads)
        direct = read_json(direct_name)
        need(direct['schema'] == 'DIRECT_67_SOURCE_RECONSTRUCTION_V1' and direct['status'] == 'PASS' and
             direct['stage'] == 'direct-source' and direct['checker_sha256'] == DIRECT_CHECKER_SHA,
             'Wrong direct-source reconstruction receipt')
        need(direct['rows_checked'] == 67 and direct['final_fields_reconstructed'] == 268 and
             direct['main_lower_bounds_proved_directly'] == 67 and
             direct['same_final_jet_bodies_checked'] == [0, 16, 44] and
             direct['all_28_shared_rows_use_fixed_amplitude'] is True and
             direct['M8_critical_value_list_complete'] is True and
             direct['saved_acceptance_flags_read'] is False and
             direct['normalizer_coordinate_budget_rows_checked'] == 67,
             'Direct-source reconstruction coverage mismatch')
        need(set(direct['raw_inputs']) == direct_reads,
             'Direct-source raw inputs differ from actual fresh access log')
        for name, entry in direct['raw_inputs'].items():
            identity(PREFIX+'inputs/workspace/'+name, entry)
        operational = read_json(PREFIX+'verification/source_overlays/ALL67_OPERATIONAL_SOURCE_TABLE.json')
        source = read_json(PREFIX+'inputs/workspace/lambda_round15/flow_main_v2/MAIN_CLOCK_SOURCE.json')['records']
        plan = read_json(PREFIX+'inputs/workspace/lambda_round14/material/m8_late/M8_LATE_PLAN.json')['rows']
        rows = direct['rows']
        need(all(len(x) == 67 for x in (rows, operational, source, plan)), 'Source/body row coverage mismatch')
        for i, (row, op, src, body) in enumerate(zip(rows, operational, source, plan)):
            need(row['row'] == op['row'] == src['row'] == body['row'] == i, 'Source row ordering mismatch')
            for key in ('main_lo', 'native_debit', 'first_hi', 'last_hi'):
                need(F(row['fields'][key]) == F(op['fields'][key]) == F(src[key]),
                     'Direct-source final-field binding failed: '+str(i)+'/'+key)
            need(list(map(F, row['time'])) == list(map(F, body['time'])) ==
                 [F(src['t_lo']), F(src['t_hi'])], 'Direct-source whole-time domain mismatch')
            need(list(map(F, row['q_interval'])) == list(map(F, body['q_interval'])) ==
                 list(map(F, src['q_interval'])), 'Direct-source contact domain mismatch')
            expected_functional = {'nodes': body['nodes'], 'joint_jet_overlay': body.get('joint_jet_overlay')}
            need(row['functional'] == op['functional'] == expected_functional,
                 'Direct-source final-functional binding failed')
        flow_name = PREFIX+'inputs/workspace/lambda_round16/ordinary_7_8_flow/full_flow/FLOW.json.gz'
        with proof.open(flow_name) as compressed, gzip.GzipFile(fileobj=compressed) as stream:
            flow = json.load(stream)
        need(F(flow['initial_sigma']) == F(7, 8) and
             F(flow['initial_q']) == F(562500000001, 10**12), 'Wrong initial strip/cushion')
        need(flow['steps'] == len(flow['records']) == 221010, 'Wrong actual comparison arc count')
        t, q = F(flow['terminal_t']), F(flow['terminal_q'])
        last = flow['records'][-1]
        need(t == F(22101, 204800) and q == F(7902377963830536747158643, 2**96),
             'Wrong terminal comparison data')
        need(F(last['t'])+F(last['dt']) == t and F(last['qout']) == q,
             'Last comparison arc does not meet terminal data')
        need(t+q/2 == F(flow['endpoint']) == ENDPOINT and ENDPOINT < F(107964910079, 10**12),
             'Full terminal contraction or strict decimal ceiling failed')
    return {'status': 'PASS', 'doi': DOI,
            'scientific_edition': 'Reconstructed proof and replay edition',
            'version_note': VERSION_NOTE, 'public_files': 16,
            'scientific_payload_files': len(inner), 'support_payload_files': len(support),
            'fresh_run_core_files': len(core), 'immutable_original_core_files': len(protected),
            'recorded_fresh_replay_stages': 15, 'actual_distinct_raw_inputs_opened': len(all_reads),
            'frozen_raw_dependency_files': 170, 'kernel_rows': 67,
            'source_rows': 67, 'source_fields_reconstructed': 268, 'comparison_arcs': 221010,
            'exact_endpoint': str(ENDPOINT), 'historical_pdfs_preserved': True,
            'mathematical_consumers_executed_by_this_verifier': False,
            'scope': 'Exhaustive public/inner/support byte integrity, preserved original numerical core, recorded fresh replay source bindings, direct source/body bindings and exact terminal arithmetic. Mathematical replay is a separate command.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--json', type=Path, help='Optional result path outside the public upload folder')
    args = ap.parse_args()
    try:
        result = verify(args.directory.resolve())
    except Exception as error:
        print('FAIL:', error, file=sys.stderr)
        return 1
    if args.json:
        need(args.json.resolve().parent != args.directory.resolve(),
             'Write the audit result outside the canonical sixteen-file folder')
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    print('Deposit integrity and replay bindings PASS. Full mathematical replay is the separate fifteen-stage command.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
