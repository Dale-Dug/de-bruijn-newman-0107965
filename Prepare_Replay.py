#!/usr/bin/env python3
"""Restore all 16 unchanged Zenodo files; optionally run the original integrity check."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

sys.dont_write_bytecode = True
from Verify_GitHub_Files import DOI, ROOT, check_file, verify

ARCHIVE = 'Proof_and_Replay.zip'
ARCHIVE_URL = 'https://zenodo.org/api/records/23752103/files/Proof_and_Replay.zip/content'
ARCHIVE_BYTES = 201060812
ARCHIVE_SHA256 = 'bf5c7b3dca9e17e84e146ecc5ca0c6f671b409613088212e3f0b8a0b15f6aaf6'


def download(path: Path, expected: dict) -> None:
    request = urllib.request.Request(ARCHIVE_URL, headers={
        'User-Agent': 'BCLD-0107965-publication-companion/1.0',
        'Accept': 'application/zip, application/octet-stream',
    })
    count = 0
    with urllib.request.urlopen(request, timeout=60) as response, path.open('xb') as target:
        for block in iter(lambda: response.read(1024 * 1024), b''):
            count += len(block)
            if count > expected['bytes']:
                raise ValueError('Download exceeds the pinned archive size.')
            target.write(block)
    check_file(path, expected)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--archive', type=Path, help='An existing exact Proof_and_Replay.zip.')
    source.add_argument('--download', action='store_true', help='Download the pinned archive from Zenodo.')
    parser.add_argument('--output', type=Path, required=True, help='A NEW directory outside this repository.')
    parser.add_argument('--verify-deposit', action='store_true',
                        help='Run the unchanged integrity/configuration checker; no scientific programs.')
    args = parser.parse_args()
    verify()
    provenance = json.loads((ROOT / 'REPOSITORY_PROVENANCE.json').read_text(encoding='utf-8'))
    if provenance['publication_doi'] != DOI:
        raise ValueError('Publication DOI mismatch.')
    expected = provenance['original_deposit_files']
    if len(expected) != 16 or ARCHIVE not in expected:
        raise ValueError('Original deposit inventory mismatch.')
    for name in expected:
        if Path(name).name != name or name in {'.', '..'} or '\\' in name:
            raise ValueError('Unsafe original filename: ' + name)
    archive = expected[ARCHIVE]
    if (archive['bytes'], archive['sha256'], archive['url']) != (ARCHIVE_BYTES, ARCHIVE_SHA256, ARCHIVE_URL):
        raise ValueError('Pinned scientific archive identity mismatch.')
    candidate = args.output.expanduser()
    if candidate.is_symlink():
        raise ValueError('The output must not be a symbolic link.')
    output = candidate.resolve()
    if output.exists() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside this repository; existing paths are never overwritten.')
    local = args.archive.expanduser() if args.archive is not None else None
    if local is not None:
        check_file(local, archive)
    for name, info in expected.items():
        if name != ARCHIVE:
            check_file(ROOT / 'deposit' / name, info)
    output.mkdir(parents=True, exist_ok=False)
    try:
        for name in expected:
            if name != ARCHIVE:
                shutil.copyfile(ROOT / 'deposit' / name, output / name)
        if local is None:
            download(output / ARCHIVE, archive)
        else:
            shutil.copyfile(local, output / ARCHIVE)
        for name, info in expected.items():
            check_file(output / name, info)
        if args.verify_deposit:
            subprocess.run([sys.executable, '-I', '-B', str(output / 'Verify_Deposit.py'),
                            '--directory', str(output)], cwd=output, check=True)
        verify()
    except BaseException:
        # Only remove the new directory created by this invocation, never an existing destination.
        shutil.rmtree(output)
        raise
    print('ORIGINAL_ZENODO_DEPOSIT_RESTORED_AND_HASH_CHECKED 16')
    print('Location:', output)
    print('Original integrity/configuration checker:', 'passed' if args.verify_deposit else 'not run')
    print('No scientific programs or native producers were executed. Read Verification_Guide.pdf for replay.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError, subprocess.CalledProcessError) as exc:
        raise SystemExit('PREPARATION FAILED: ' + str(exc) +
                         '\nNever bypass a checksum mismatch. For download failures, use an exact local archive with --archive.')
