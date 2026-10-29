#!/usr/bin/env python3
"""Check this companion's file identities; no mathematical claim is verified."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parent
DOI = '10.5281/zenodo.23752103'


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def check_file(path: Path, expected: dict) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError('Missing or unsafe file: ' + str(path))
    if path.stat().st_size != expected['bytes'] or sha256(path) != expected['sha256']:
        raise ValueError('File identity mismatch: ' + str(path))


def verify() -> int:
    if sys.flags.optimize:
        raise ValueError('Run without -O, -OO or PYTHONOPTIMIZE.')
    manifest = ROOT / 'GITHUB_FILES.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('Missing or unsafe companion manifest.')
    doc = json.loads(manifest.read_text(encoding='utf-8'))
    if doc['schema'] != 'BCLD_GITHUB_FILES_V2' or doc['publication_doi'] != DOI:
        raise ValueError('Unexpected companion identity.')
    for name, expected in doc['files'].items():
        rel = PurePosixPath(name)
        if rel.is_absolute() or not rel.parts or any(p in {'.', '..'} for p in rel.parts):
            raise ValueError('Unsafe manifest path: ' + name)
        if '\\' in name or str(rel) != name or name == 'GITHUB_FILES.json':
            raise ValueError('Unexpected manifest path: ' + name)
        path = ROOT.joinpath(*rel.parts)
        if any(parent.is_symlink() for parent in path.parents if parent != ROOT and ROOT in parent.parents):
            raise ValueError('Symbolic-link parent in manifest path: ' + name)
        check_file(path, expected)
    return len(doc['files'])


if __name__ == '__main__':
    try:
        count = verify()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit('GITHUB_COMPANION_FILE_INTEGRITY_FAIL: ' + str(exc))
    print('GITHUB_COMPANION_FILE_INTEGRITY_PASS', count)
    print('Scope: file identity only; no mathematical proof or numerical replay.')
