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


# Engines whose units answer chat (the Wrapper's call templates, hugpy_wrapper queue/templates.py CHAT): a unit one
# of them serves is a text model whatever its catalog tag says (2026-11-16: a FLUX text-encoder GGUF tagged
# text-to-image was offered in Video's image pickers, and the Wrapper had no image unit for it: 404).
CHAT_ENGINES = frozenset(("llama-server", "transformers", "vision", "vllm", "sglang", "ollama"))
# Engines with one fixed call whatever the unit (the Wrapper's _FIXED): what they render and the input they need.
FIXED_ENGINE_CALLS = {"videoupres": (("video-upscale",), ("video",)),
                      "videointerp": (("video-interpolation",), ("video",))}
# A diffusers pipeline's own sub-folders, by name: the parts rule when no fleet facts say which units have an engine.
PIPELINE_PARTS = frozenset(("text_encoder", "text_encoder_2", "text_encoder_3", "tokenizer", "tokenizer_2",
                            "tokenizer_3", "vae", "transformer", "transformer_2", "unet", "scheduler", "prior",
                            "image_encoder", "image_processor", "feature_extractor", "safety_checker", "processor"))


def call_facts(engine, class_names, capabilities, key, tasks):
    """(tasks, needs, pipeline) of a unit, read the way the Wrapper serving it reads a call (queue/templates.py): the
    engine decides which call the unit answers; the diffusers pipeline class (else the model's own name, for Wan's
    layout or a single-file checkpoint) decides which inputs that call must carry; the fleet's capabilities say
    what else a video unit renders. ``needs`` are input kinds (text, image, video, audio, mask); None when the
    engine is not known, and units of other engines keep their tasks with no needs."""
    pipeline = next((c for c in class_names or () if c.endswith("Pipeline")), None)
    name = (pipeline or key or "").lower()
    if engine in CHAT_ENGINES:
        vision = engine == "vision" or "image-text-to-text" in tasks
        return ["text-generation"] + (["image-text-to-text"] if vision else []), ["text"], pipeline
    if engine in FIXED_ENGINE_CALLS:
        rendered, needs = FIXED_ENGINE_CALLS[engine]
        return list(rendered), list(needs), pipeline
    if engine in ("imagegen", "comfy"):
        if "upscale" in name or "redux" in name:
            return ["image-to-image"], ["image"], pipeline
        if "img2img" in name or "inpaint" in name or "edit" in name:
            return ["image-to-image"], ["image", "text"] + (["mask"] if "inpaint" in name else []), pipeline
        return ["text-to-image"] + [t for t in ("image-to-image",) if t in tasks], ["text"], pipeline
    if engine == "videogen":
        if "avatar" in name:
            needs, primary = ["audio", "image"], "audio-to-video"
        elif "imagetovideo" in name or "i2v" in name:
            needs, primary = ["image"], "image-to-video"
        elif "videotovideo" in name:
            needs, primary = ["video"], "video-to-video"
        else:
            needs, primary = ["text"], "text-to-video"
        rendered = [t for cap in capabilities or () for t in CAPABILITY_TASKS.get(cap, ())]
        return list(dict.fromkeys(rendered or [primary])), needs, pipeline
    return list(tasks), (None if engine is None else []), pipeline


def _picker_facts():
    """What serves each model now, for the pickers: ({key: [fleet catalog entries]}, {id: Core model row}); either is
    None when its source cannot be read (the picker then lists the models table alone, as before)."""
    try:
        from hugpy_core.registry import fleet_central
        fleet = {}
        for m in fleet_central.catalog():
            fleet.setdefault(m["key"], []).append(m)
    except Exception:  # noqa: BLE001 - no fleet facts: tags and no availability, as before 2026-11-16
        fleet = None
    try:
        from hugpy_core.web.routes import model_rows
        served = {row["id"]: row for row in model_rows()}
    except Exception:  # noqa: BLE001
        served = None
    return fleet, served


def picker_models():
    """Capability catalog for browser pickers, without allocation or session probes.

    Each row also says what serves it (2026-11-16, operator: a text encoder and a model no running host could serve
    were offered in /video): ``engine``, ``pipeline``, ``needs`` (the inputs the Wrapper refuses a call without),
    ``tasks`` read from those rather than the catalog tag, ``available`` (an online worker serves it now),
    ``hosts`` (those workers) and ``held_by`` (connected hosts whose drives hold it; a call copies it from there).
    A pipeline's own sub-folders (its text_encoder, vae, ...) and ``key::*`` twins of a listed key are not
    offered: a call cannot name the one, and the other is the same model twice."""
    with _conn() as conn:
        rows = conn.execute('SELECT model_key,primary_task,metadata,framework '
                            'FROM models ORDER BY model_key').fetchall()
    fleet, served = _picker_facts()
    keys = {row['model_key'] for row in rows} | set(fleet or ())
    out = []
    for row in rows:
        key = row['model_key']
        head, _, variation = key.partition('::')
        parent, _, part = head.rpartition('/')
        if variation == '*' and head in keys:
            continue
        # Nested (at any depth) under another model and served by no engine of its own: a part of that model (a
        # pipeline's encoder or vae, a MoE expert's high/low-noise weights, a split checkpoint's diffusion_models).
        # A nested GGUF with its own engine stays.
        steps = head.split('/')
        nested = any('/'.join(steps[:i]) in keys for i in range(1, len(steps)))
        if nested and (part in PIPELINE_PARTS and parent in keys if fleet is None
                       else not any(m.get('engine') for m in fleet.get(head) or ())):
            continue
        meta = dict(row['metadata'] or {})
        tasks = list(meta.get('tasks') or [])
        if row['primary_task']:
            tasks.append(row['primary_task'])
        override = meta.get('task_override')
        overrides = override if isinstance(override, list) else [override] if isinstance(override, str) else []
        primary = row['primary_task']
        facts = {}
        if fleet is not None:
            entries = fleet.get(head) or []
            unit = next((m for m in entries if m['variation'] == (variation or '*')), None)
            engine = (unit or {}).get('engine') or (None if variation else next(
                (m['engine'] for m in entries if m.get('engine')), None))
            names = [c for m in entries for c in m.get('class_names') or ()]
            caps = [c for m in entries for c in m.get('capabilities') or ()]
            tasks, needs, pipeline = call_facts(engine, names, caps, head, list(dict.fromkeys(tasks)))
            facts = {'engine': engine, 'pipeline': pipeline,
                     'held_by': sorted({h['holder'] for m in entries for h in m.get('holders') or ()
                                        if (not variation or m['variation'] == variation) and h.get('holder')})}
            if needs is not None:
                facts['needs'] = needs
            if primary not in tasks:
                primary = tasks[0] if tasks else primary
        if served is not None:
            got = served.get(key) or {}
            facts.update(available=bool(got.get('available')), hosts=list(got.get('workers') or []))
        out.append({**{field: meta[field] for field in
                       ('hub_id', 'adapter', 'serveable', 'unserveable_reason', 'task_override') if field in meta},
                    'id': key, 'model_key': key, 'name': meta.get('name') or key,
                    'object': 'model', 'owned_by': 'hugpy', 'framework': row['framework'],
                    'primary_task': primary, 'tasks': list(dict.fromkeys([*tasks, *overrides])), **facts})
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
