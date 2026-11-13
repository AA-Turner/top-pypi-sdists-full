"""Lifted verbatim from fitevict/probes/fixtures.py (sha256 78215cc129652d3f): load_fixture and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py; the definitions below are the original text."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _inside(root, relative):
    path = (root / relative).resolve(strict=True)
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise ValueError('fixture path escapes its collection') from None
    return path


def load_fixture(library, fixture_id):
    root = Path(library).resolve(strict=True)
    matches = []
    for collection in (root / 'fixtures', root / 'images'):
        if not collection.is_dir():
            continue
        for path in sorted(collection.glob('*/t*/manifest.json')):
            manifest = json.loads(path.read_text())
            if manifest.get('id') == fixture_id:
                matches.append((collection, path, manifest))
    if len(matches) != 1:
        raise ValueError('fixture must identify exactly one manifest')
    collection, path, manifest = matches[0]
    data = {}
    total = 0
    for record in manifest['files']:
        asset = _inside(collection, record['path'])
        total += asset.stat().st_size
        if total > 32 * 1024 * 1024:
            raise ValueError('fixture exceeds 32 MiB probe input limit')
        raw = asset.read_bytes()
        if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise ValueError('fixture size/hash mismatch: ' + record['path'])
        if asset.name in data:
            raise ValueError('ambiguous fixture basenames')
        data[asset.name] = raw
    return manifest, data, hashlib.sha256(path.read_bytes()).hexdigest()
