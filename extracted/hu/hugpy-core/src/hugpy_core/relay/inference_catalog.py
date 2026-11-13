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
    """The text models of Core's one model list (web/routes.model_rows), in the shape a hosted
    arm's picker reads: the name to send, whether a worker has it loaded, whether one serves it."""
    from hugpy_core.web.routes import model_rows
    out = []
    for row in model_rows():
        name = row.get('id') or ''
        if row.get('object') != 'model' or name.startswith('session:'):
            continue
        if 'text-generation' not in [row.get('primary_task'), *(row.get('tasks') or [])]:
            continue
        serving, held = bool(row.get('loaded_on')), bool(row.get('available'))
        out.append({'model': name, 'serving': serving, 'held': serving or held,
                    'state': 'serving' if serving else 'hot' if held else 'unknown'})
    return out


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
    """The rows Core's model endpoint serves, read in-process: the servable id of each model,
    whether an online worker has it, and where it is loaded. A hosted Media arm selects by them,
    so what it picks is what the relay can route."""
    from hugpy_core.web.routes import model_rows
    return model_rows()
