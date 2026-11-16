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


# A unit's capabilities (its Wrapper reads them from the pipeline classes its folder declares, 2026-11-15) as the
# tasks Video asks for.
CAPABILITY_TASKS = {'t2v': ('text-to-video',), 'i2v': ('image-to-video',), 'v2v': ('video-to-video',),
                    'reference': ('video-to-video',), 'extend': ('video-to-video',),
                    'upscale': ('video-upscale',), 'interpolate': ('video-interpolation',),
                    'avatar': ('audio-to-video',)}


def _fleet_video():
    """{model key: {capabilities, hosts, bytes, engine}} for every whole model a connected host holds, from the fleet
    models database (each host's Discovery, through its Wrapper). Empty when the fleet table cannot be read."""
    try:
        from hugpy_core.registry import fleet_central
        entries = fleet_central.catalog()
    except Exception:  # noqa: BLE001 - no fleet facts: the models table alone, as before
        return {}
    out = {}
    for m in entries:
        caps = set(m.get('capabilities') or [])
        if m.get('variation') != '*' and not caps:
            continue
        f = out.setdefault(m['key'], dict(capabilities=set(), hosts=set(), bytes=0, engine=m.get('engine')))
        f['capabilities'] |= caps
        f['hosts'] |= {h.get('holder') for h in m.get('holders') or [] if h.get('holder')}
        f['bytes'] = max(f['bytes'], int(m.get('bytes') or 0))
    return out


def video_models():
    """The video models Video may choose from: each with the tasks it can serve and whether it is available.

    Tasks come from what the model can render (the fleet's capabilities, read from its declared pipeline) where its
    Wrapper reports them, else from the models table as before; an operator's task_override always counts.
    ``available`` is a fact, no longer a stamp: a connected host holds the model whole (2026-11-15)."""
    from types import SimpleNamespace
    with _conn() as conn:
        rows = conn.execute('SELECT model_key,primary_task,metadata,framework FROM models').fetchall()
    base = {}
    for row in rows:
        meta = dict(row['metadata'] or {})
        tasks = set(meta.get('tasks') or [])
        if row['primary_task']:
            tasks.add(row['primary_task'])
        override = meta.get('task_override')
        overrides = override if isinstance(override, list) else [override] if isinstance(override, str) else []
        base[row['model_key'].split('::', 1)[0]] = (row['model_key'], tasks | set(overrides), set(overrides),
                                                    row['framework'], meta)
    fleet = _fleet_video()
    out = {}
    for key in sorted(set(base) | set(fleet)):
        model_key, tasks, overrides, framework, meta = base.get(key, (key, set(), set(), None, {}))
        f = fleet.get(key)
        if f and f['capabilities']:
            tasks = {t for cap in f['capabilities'] for t in CAPABILITY_TASKS.get(cap, ())} | overrides
        if not any('video' in task for task in tasks) or meta.get('adapter') or meta.get('serveable') is False:
            continue
        extra = {**meta, 'available': bool(f and f['hosts']),
                 'capabilities': sorted(f['capabilities']) if f else [],
                 'hosts': sorted(f['hosts']) if f else [], 'bytes': f['bytes'] if f else None}
        out[model_key] = SimpleNamespace(tasks=tuple(sorted(tasks)), framework=framework or (f or {}).get('engine'),
                                         hub_id=meta.get('hub_id') or '', extra=extra)
    return out


def media_models():
    """The rows Core's model endpoint serves, read in-process: the servable id of each model,
    whether an online worker has it, and where it is loaded. A hosted Media arm selects by them,
    so what it picks is what the relay can route."""
    from hugpy_core.web.routes import model_rows
    return model_rows()
