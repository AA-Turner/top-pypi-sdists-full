"""Resource display projections over existing worker reports; no collector."""
from __future__ import annotations


def storage_view(worker: dict, reports: list[dict]) -> dict:
    """One row per reported filesystem on a named box, retaining source pointers.

    Registry names are the box identity used by the wrapper telemetry mirror.
    Missing filesystem identities stay separate unless their exact model root
    already belongs to one identified filesystem. Never merge by capacity.
    """
    name = worker.get('name')
    sources = [r for r in reports if r.get('name') == name] if name else [worker]
    groups = {}
    pending = []
    for r in sources:
        s = r.get('storage') or {}
        if not s:
            continue
        root = s.get('root') or s.get('store_root')
        identity = next(((k, s[k]) for k in ('filesystem_uuid', 'fs_uuid', 'device', 'mount') if s.get(k)), None)
        entry = (r, s, root)
        if identity:
            groups.setdefault(identity, []).append(entry)
        else:
            pending.append(entry)
    for entry in pending:
        r, s, root = entry
        matches = [key for key, rows in groups.items() if root and any(e[2] == root for e in rows)]
        key = matches[0] if len(matches) == 1 else ('report', r.get('id'))
        groups.setdefault(key, []).append(entry)
    volumes = []
    for identity, entries in groups.items():
        # Choose a complete measurement as a unit: do not mix total from one
        # report with free space from another. Partial reports still add paths.
        entries.sort(key=lambda e: float(e[1].get('measured_at') or e[0].get('last_seen') or 0), reverse=True)
        measured = next((e for e in entries if e[1].get('disk_total') is not None and e[1].get('disk_free') is not None), None)
        r, s, _ = measured or entries[0]
        total, free = (s.get('disk_total'), s.get('disk_free')) if measured else (None, None)
        volumes.append({
            'id': f'{identity[0]}:{identity[1]}', 'identity_kind': identity[0],
            'device': next((e[1]['device'] for e in entries if e[1].get('device')), None),
            'mounts': sorted({e[1]['mount'] for e in entries if e[1].get('mount')}),
            'paths': sorted({e[2] for e in entries if e[2]}),
            'fstype': s.get('fstype'), 'total': total, 'free': free,
            'used': max(0, total - free) if measured else None,
            'measurement_source': {'worker_id': r.get('id'), 'field': 'storage'} if measured else None,
            'reported_at': r.get('last_seen'),
            'sources': [{'worker_id': e[0].get('id'), 'url': e[0].get('url'),
                         'version': e[0].get('pkg_version'), 'field': 'storage'} for e in entries],
        })
    return {'host': name, 'volumes': volumes}


def unique_gpus(cards: list[dict]) -> list[dict]:
    """A reindexed card is one UUID; retain its newest measured report."""
    chosen = {}
    for i, card in enumerate(cards):
        identity = ('uuid', card['uuid']) if card.get('uuid') else ('index', card.get('index', i))
        prior = chosen.get(identity)
        stamp = float((card.get('gpu_state') or {}).get('at') or card.get('measured_at') or 0)
        prior_stamp = float((prior.get('gpu_state') or {}).get('at') or prior.get('measured_at') or 0) if prior else -1
        if prior is None or stamp > prior_stamp:
            chosen[identity] = card
    return sorted(chosen.values(), key=lambda c: c.get('index') if c.get('index') is not None else -1)
