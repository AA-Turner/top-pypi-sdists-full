"""Model keys identify repositories; GGUF quant files identify variants."""
from __future__ import annotations
import os
import re
from psycopg import sql
from psycopg.types.json import Jsonb


def parent_key(key, file):
    key = str(key or '')
    filename = os.path.basename(str(file or ''))
    if not filename.lower().endswith('.gguf'):
        return key
    stem = filename[:-5]
    suffix = '~' + stem
    candidate = key
    # A path-copy hash may follow the historical quant suffix.
    if re.search(r'~[0-9a-f]{8}$', candidate, re.I):
        shorter = candidate.rsplit('~', 1)[0]
        if shorter.lower().endswith(suffix.lower()):
            candidate = shorter
    if candidate.lower().endswith(suffix.lower()):
        parent = candidate[:-len(suffix)]
        if parent:
            return parent
    return key



def directory_handle(relative_dir):
    """Same explicit path encoding used by discovery and the browser."""
    if not isinstance(relative_dir, str) or not relative_dir or relative_dir.startswith('/'):
        return None
    parts = relative_dir.split('/')
    if any(part in ('', '.', '..') for part in parts):
        return None
    return '~'.join(part.replace('%', '%25').replace('~', '%7E') for part in parts)


def resolve_handle(handle, models):
    """Resolve only published handles; an ambiguous short name stays unresolved."""
    matches = set()
    for model in models:
        key = model.get('model_key') or model.get('id')
        identity = model.get('identity') or {}
        identities = [identity, *((model.get('variables') or {}).get('discovery_identity') or [])]
        handles = [key, *(model.get('aliases') or []),
                   *(h for item in identities for h in item.get('handles', []))]
        if handle in handles and key:
            matches.add(key)
    return next(iter(matches)) if len(matches) == 1 else handle

def alias_map(keys, files, census):
    """Build redirects only from exact file suffixes or matching Hub identities."""
    known = set(keys)
    aliases = {}
    hub_groups = {}
    for row in census:
        hub = str(row.get('hub_id') or '')
        if hub.count('/') == 1:
            hub_groups.setdefault(hub, []).append(row['model_key'])
    for hub, group in hub_groups.items():
        repo = hub.rsplit('/', 1)[-1]
        qualified = hub.replace('/', '~')
        canonical = min(group, key=lambda key: (key != repo, key != qualified, len(key), key))
        for key in group:
            if key != canonical:
                aliases[key] = canonical
    # Exact Hub handles are evidence even if only the short directory key was
    # ever persisted. They allow old owner-qualified quant records to converge.
    hub_targets = {hub.replace('/', '~'): min(group, key=lambda key:
                    (key != hub.rsplit('/', 1)[-1], len(key), key))
                   for hub, group in hub_groups.items()}
    by_key = {}
    for row in files:
        by_key.setdefault(row['model_key'], set()).add(row['file'])
    for key in sorted(known):
        names = by_key.get(key, ()) or {row['file'] for row in files}
        parents = {parent_key(key, name) for name in names}
        parents.discard(key)
        if len(parents) == 1:
            parent = next(iter(parents))
            # A quant-looking string alone is insufficient: its parent must be known.
            if parent in known or parent in hub_targets:
                aliases[key] = aliases.get(parent, hub_targets.get(parent, parent))
    for key in list(aliases):
        target, seen = aliases[key], {key}
        while target in aliases and target not in seen:
            seen.add(target); target = aliases[target]
        if target in seen:
            aliases.pop(key)
        else:
            aliases[key] = target
    return aliases


def merged_settings(parent, alias):
    """Existing explicit parent choices win; conflicting alias values are archived."""
    parent, alias = dict(parent or {}), dict(alias or {})
    conflicts = {k: {'parent': parent[k], 'alias': v} for k, v in alias.items()
                 if k in parent and parent[k] != v}
    return {**alias, **parent}, conflicts


def _copy_keyed(conn, table, alias, canonical):
    columns = [r[0] for r in conn.execute(
        'SELECT column_name FROM information_schema.columns WHERE table_schema=current_schema() '
        'AND table_name=%s ORDER BY ordinal_position', (table,))]
    if not columns:
        return
    fields = sql.SQL(',').join(map(sql.Identifier, columns))
    selected = sql.SQL(',').join(sql.SQL('%s') if name == 'model_key' else sql.Identifier(name) for name in columns)
    conn.execute(sql.SQL('INSERT INTO {} ({}) SELECT {} FROM {} WHERE model_key=%s ON CONFLICT DO NOTHING').format(
        sql.Identifier(table), fields, selected, sql.Identifier(table)), (canonical, alias))


def reconcile(conn):
    """Retire historical quant identities while retaining source facts and history."""
    from psycopg.rows import dict_row
    keys = [row[0] for row in conn.execute('SELECT model_key FROM model_dossier_raw_keys')]
    files = [{'model_key': k, 'file': f} for k, f in conn.execute(
        'SELECT model_key,file FROM model_quant_facts UNION SELECT model_key,file FROM model_worker_quants')]
    census = [{'model_key': k, 'hub_id': hub} for k, hub in conn.execute('SELECT model_key,hub_id FROM model_census')]
    aliases = alias_map(keys, files, census)
    changed, conflicts = 0, []
    for alias, canonical in sorted(aliases.items()):
        conn.execute('INSERT INTO model_key_aliases(alias_key,model_key,evidence) VALUES (%s,%s,%s) '
                     'ON CONFLICT(alias_key) DO UPDATE SET model_key=EXCLUDED.model_key',
                     (alias, canonical, Jsonb({'source': 'quant file suffix / Hub identity'})))
        # Canonical census and quant facts may be missing when only an old alias survived.
        _copy_keyed(conn, 'model_census', alias, canonical)
        _copy_keyed(conn, 'model_quant_facts', alias, canonical)
        with conn.cursor(row_factory=dict_row) as cur:
            old_rows = cur.execute('SELECT * FROM model_workers WHERE model_key=%s', (alias,)).fetchall()
        for old in old_rows:
            wid = old['worker_id']
            conn.execute('INSERT INTO model_workers(model_key,worker_id) VALUES (%s,%s) ON CONFLICT DO NOTHING',
                         (canonical, wid))
            with conn.cursor(row_factory=dict_row) as cur:
                parent = cur.execute('SELECT * FROM model_workers WHERE model_key=%s AND worker_id=%s',
                                     (canonical, wid)).fetchone()
            settings, collision = merged_settings(parent['user_settings'], old['user_settings'])
            if collision:
                conflicts.append({'alias': alias, 'model_key': canonical, 'worker': wid, 'conflicts': collision})
            conn.execute('INSERT INTO model_alias_pair_archive(alias_key,model_key,worker_id,payload) '
                         'VALUES (%s,%s,%s,%s) ON CONFLICT(alias_key,worker_id) DO NOTHING',
                         (alias, canonical, wid, Jsonb(dict(old), dumps=lambda v: __import__('json').dumps(v,default=str))))
            conn.execute('UPDATE model_workers SET user_settings=%s, assigned=assigned OR %s, pinned=pinned OR %s, '
                         'pinned_by=coalesce(pinned_by,%s), pinned_at=coalesce(pinned_at,%s), '
                         'env_profile=coalesce(env_profile,%s), updated_at=now() '
                         'WHERE model_key=%s AND worker_id=%s',
                         (Jsonb(settings), old.get('assigned',False), old.get('pinned',False),
                          old.get('pinned_by'),old.get('pinned_at'),old.get('env_profile'), canonical,wid))
        _copy_keyed(conn, 'model_worker_quants', alias, canonical)
        conn.execute('DELETE FROM model_workers WHERE model_key=%s', (alias,))
        changed += len(old_rows)
    # Discovery handles can predate reconciliation and point at an old copy
    # key. Keep every redirect one hop, including handles not in the raw keys.
    for alias, canonical in sorted(aliases.items()):
        conn.execute('UPDATE model_key_aliases SET model_key=%s WHERE model_key=%s',
                     (canonical, alias))
    return {'aliases':len(aliases),'pairs_moved':changed,'settings_conflicts':conflicts}
