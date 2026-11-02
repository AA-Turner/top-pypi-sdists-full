"""Small database projection for inference choices; no HTTP or full dossiers."""
from hugpy_core.relay.inference_requests import _conn


def model_tasks(model_key):
    """Read one model's declared capabilities without building a fleet catalog."""
    with _conn() as conn:
        row = conn.execute('SELECT primary_task,metadata FROM models WHERE model_key='
                           'COALESCE((SELECT model_key FROM model_key_aliases WHERE alias_key=%s),%s)',
                           (model_key, model_key)).fetchone()
    if row is None:
        return None
    metadata = row['metadata'] or {}
    tasks = metadata.get('tasks')
    tasks = list(tasks) if isinstance(tasks, list) else []
    if row['primary_task']:
        tasks.append(row['primary_task'])
    override = metadata.get('task_override')
    tasks.extend(override if isinstance(override, list) else [override] if isinstance(override, str) else [])
    return set(tasks) if tasks else None


def picker_models():
    """Capability catalog for browser pickers, without allocation or session probes."""
    with _conn() as conn:
        rows = conn.execute('SELECT model_key,primary_task,metadata,framework '
                            'FROM models ORDER BY model_key').fetchall()
    out = []
    for row in rows:
        meta = dict(row['metadata'] or {})
        tasks = list(meta.get('tasks') or [])
        if row['primary_task']:
            tasks.append(row['primary_task'])
        override = meta.get('task_override')
        tasks.extend(override if isinstance(override, list) else [override] if isinstance(override, str) else [])
        key = row['model_key']
        out.append({**{field: meta[field] for field in
                       ('hub_id', 'adapter', 'serveable', 'unserveable_reason', 'task_override') if field in meta},
                    'id': key, 'model_key': key, 'name': meta.get('name') or key,
                    'object': 'model', 'owned_by': 'hugpy', 'framework': row['framework'],
                    'primary_task': row['primary_task'], 'tasks': list(dict.fromkeys(tasks))})
    return out


def text_models():
    from hugpy_core.registry import registry
    from hugpy_core.models.keys import model_key_forms, serveable_match
    with _conn() as conn:
        rows = conn.execute('SELECT model_key,primary_task,metadata FROM models').fetchall()
    workers = [w for w in registry.all_workers() if registry.is_online(w)]
    out = []
    for row in rows:
        metadata = row['metadata'] or {}
        tasks = [row['primary_task'], *(metadata.get('tasks') or [])]
        if 'text-generation' not in tasks or metadata.get('adapter') or metadata.get('serveable') is False:
            continue
        key = row['model_key']
        wanted = model_key_forms(key)
        serving = any(serveable_match(key, wanted, w.get('loaded_models') or []) for w in workers)
        held = serving or any(serveable_match(key, wanted,
                       [*(w.get('models') or []), *(w.get('models_local') or [])]) for w in workers)
        out.append({'model': key, 'serving': serving, 'held': held,
                    'state': 'serving' if serving else 'hot' if held else 'unknown'})
    return sorted(out, key=lambda row: row['model'])


def video_models():
    """Canonical video task facts, without the full HTTP model dossier."""
    from types import SimpleNamespace
    with _conn() as conn:
        rows = conn.execute('SELECT model_key,primary_task,metadata,framework FROM models').fetchall()
    out = {}
    for row in rows:
        meta = dict(row['metadata'] or {})
        tasks = set(meta.get('tasks') or [])
        if row['primary_task']:
            tasks.add(row['primary_task'])
        override = meta.get('task_override')
        tasks.update(override if isinstance(override, list) else [override] if isinstance(override, str) else [])
        if not any('video' in task for task in tasks) or meta.get('adapter') or meta.get('serveable') is False:
            continue
        out[row['model_key']] = SimpleNamespace(tasks=tuple(tasks), framework=row['framework'],
            hub_id=meta.get('hub_id') or '', extra={**meta, 'available': True})
    return out


def media_models():
    """The same availability facts as Core's model endpoint, called directly."""
    from hugpy_core.web.routes import catalog_rows
    return catalog_rows()
