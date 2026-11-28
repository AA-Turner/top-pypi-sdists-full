"""The console's live feeds: every connected wrapper as the worker row the console draws.

A row is shaped from three things the wrapper itself gives: what the collector last kept of it (its health, its
state, its models, its storage), and its live resources report, asked of it now (/v1/telemetry/resources: its
cards, its host memory and cores, what is loaded with each process's own card and host bytes, its copies and its
queue). Core adds no number of its own: a card's processes are the wrapper's loaded engines by their own pids,
and what the wrapper does not say (a setting chosen for a model, a limit) is left empty until Core asks the
wrapper for it too.
"""
from ..imports import (
    json,
    threading,
    time,
)
from .. import sql
from ..wrappers import ask, registry

LIVE_KEPT_S = 1.5            # one live read of a wrapper serves every console that asks within this long
_LIVE = {}                   # wrapper name -> (when, its resources report or None)
_LOCK = threading.Lock()


def documents() -> dict:
    """{wrapper: {name: document}} of what the collector last kept of each wrapper."""
    out = {}
    for row in sql.rows("SELECT wrapper, name, document FROM wrapper_documents"):
        out.setdefault(row['wrapper'], {})[row['name']] = json.loads(row['document'])
    return out


def live(wrapper: dict):
    """A wrapper's live resources report, asked of it now (kept LIVE_KEPT_S for whoever asks next); None when it
    does not answer."""
    name, now = wrapper['name'], time.monotonic()
    with _LOCK:
        kept = _LIVE.get(name)
    if kept and now - kept[0] < LIVE_KEPT_S:
        return kept[1]
    try:
        status, report = ask(wrapper, '/v1/telemetry/resources', timeout=5)
        report = report if status == 200 and isinstance(report, dict) else None
    except Exception:  # noqa: BLE001  a wrapper that does not answer has no live report; its row says offline
        report = None
    with _LOCK:
        _LIVE[name] = (now, report)
    return report


def allocation(r: dict) -> dict:
    """One loaded engine of a wrapper (a row of its residents) as the console's allocation."""
    vram, card = r.get('vram_bytes'), r.get('device')
    card = card if isinstance(card, int) and not isinstance(card, bool) else None
    return dict(kind='slot', model_key=r.get('key'), pid=r.get('pid'), slot_id=r.get('port'),
                healthy=bool(r.get('healthy')), busy=bool(r.get('busy')), endpoint=r.get('endpoint'),
                rss_bytes=r.get('ram_bytes'), n_gpu_layers=r.get('n_gpu_layers'), ctx=r.get('ctx'),
                vram_bytes=vram, device=(f'cuda:{card}' if card is not None else None if vram is None else 'cuda' if vram > 0 else 'cpu'),
                device_id=card, last_used=r.get('last_used'), loading=bool(r.get('loading')),
                materialized=bool(r.get('healthy')) and not r.get('loading'), cpu_set=r.get('cpu_set'),
                threads=r.get('threads'), engine=r.get('engine'),
                # every card it is on (a model split over several), and beside what it holds now: what was planned
                # for it and how it was loaded (a pipeline run part by part rests in host memory)
                gpu_indexes=sorted(int(card) for card in (r.get('vram_by_device') or {}) if str(card).isdigit()),
                vram_measured=bool(r.get('vram_measured')), vram_planned_bytes=r.get('vram_planned_bytes'),
                vram_peak_bytes=r.get('vram_peak_bytes'), ram_planned_bytes=r.get('ram_planned_bytes'),
                load_mode=r.get('load_mode'), representation=r.get('representation'))


def program(command) -> str:
    """The program of a command line, as a person names it: its first word without its folders."""
    words = str(command or '').split()
    return words[0].rsplit('/', 1)[-1] if words else ''


def cards(report: dict) -> list:
    """The wrapper's cards as the console's gpus: each with every process on it, by pid and the bytes the driver
    says it holds there now. One of the wrapper's own is named by the model it serves; any other by who it is
    (its program, the account it runs as, its command line, since when): the wrapper says so of each
    (gpu_state[].processes). A wrapper from before it did says only what its own engines held when their loads
    came up, and the console then shows the rest of what is used on the card as held by nobody it can name."""
    residents = [r for r in report.get('residents') or [] if r.get('pid')]
    state_of = {r['pid']: r.get('state') for r in residents}
    out = []
    for g in report.get('gpu_state') or []:
        device = g.get('device')
        listed = g.get('processes')
        if listed is not None:
            held = {str(p['pid']): int(p.get('bytes') or 0) for p in listed}
            ours = [p['pid'] for p in listed if p.get('hugpy')]
            named = {str(p['pid']): (dict(model_key=p.get('key'), state=state_of.get(p.get('resident_pid')), owner=p.get('user'),
                                          command=p.get('command'), started_at=p.get('started_at'), ram_bytes=p.get('ram_bytes'))
                                     if p.get('hugpy') else
                                     dict(program=program(p.get('command')) or p.get('name'), owner=p.get('user'),
                                          command=p.get('command'), started_at=p.get('started_at'),
                                          ram_bytes=p.get('ram_bytes'), model_name=p.get('model_file')))
                     for p in listed}
        else:
            mine = [r for r in residents if (r.get('vram_bytes') or 0) > 0 and r.get('device') in (device, None)]
            held = {str(r['pid']): int(r.get('vram_bytes') or 0) for r in mine}
            ours = [r['pid'] for r in mine]
            named = {str(r['pid']): dict(model_key=r.get('key'), state=r.get('state')) for r in residents}
        out.append(dict(
            index=device, name=g.get('name'), uuid=g.get('uuid'), memory_total=g.get('total'), memory_used=g.get('used'),
            memory_free=g.get('free'), utilization_pct=g.get('utilization_pct'), temperature_c=g.get('temperature_c'),
            gpu_state=dict(total=g.get('total'), used=g.get('used'), free=g.get('free'), at=g.get('at'),
                           processes=held, hugpy_pids=ours, probe_pids=[], pid_models=named,
                           # whether every process on the card is named here (the wrapper lists them all), or only
                           # this wrapper's own engines are
                           listed=listed is not None)))
    return out


def worker_row(status: dict, kept: dict, report, routes=(), blocks=(), static=()) -> dict:
    """One wrapper as the console's worker row. ``status`` is its row of wrapper_status, ``kept`` its documents,
    ``report`` its live resources report (None when it did not answer: the row then says what was last kept)."""
    state, health = kept.get('state') or {}, kept.get('health') or {}
    shown = report or state
    host = (shown.get('host_state') or [{}])[0]
    residents = shown.get('residents') or []
    gpus = cards(shown)
    catalog = (kept.get('models') or {}).get('data') or []
    reported_static = {m['id']: m.get('static') for m in catalog}
    desired_static = {row['model']: bool(row['enabled']) for row in static}
    residency = {model: 'static' for model, enabled in (reported_static | desired_static).items() if enabled}
    pending_static = [model for model, enabled in desired_static.items() if reported_static.get(model) is not enabled]
    online = bool(status['reachable']) and report is not None
    total, available = host.get('mem_total'), host.get('mem_available')
    return dict(
        id=status['name'], name=status['name'], url=status['url'], role='worker', pool='', admission='approved',
        status='online' if online else 'offline', connected=bool(status['connected']),
        last_seen=(shown.get('sampled_at') or status.get('read_at')), link=bool(status['link']),
        link_ts=status.get('read_at'), worker_state='ready' if online else 'offline', state_stale=not online,
        wrapper_version=health.get('version'), pkg_version=None,
        engine=state.get('engine') or dict(name='hugpy-wrapper', supports_gpu_offload=bool(gpus)),
        health=dict(status=health.get('status'), reasons=health.get('reasons') or [], warnings=health.get('warnings') or []),
        error=status.get('error'),
        gpus=gpus, vram_total=sum(int(g.get('memory_total') or 0) for g in gpus) or None,
        vram_used=sum(int(g.get('memory_total') or 0) - int(g.get('memory_free') or 0) for g in gpus) if gpus else None,
        ram_total=total, free_ram=available, ram_free_bytes=available,
        ram_used=(total - available) if total is not None and available is not None else None,
        swap_total=host.get('swap_total'), swap_free=host.get('swap_free'),
        cpu=(shown.get('cpu_state') or [None])[0],
        allocations=[allocation(r) for r in residents],
        loaded_models=[r.get('key') for r in residents if r.get('healthy') and not r.get('loading')],
        loading=[r.get('key') for r in residents if r.get('loading')],
        # the wrapper's models are a list of what it can serve, not a count of copies on its drives: where a
        # model is stored is its Discovery's to say (its storage report, below)
        models=[m['id'] for m in catalog if m.get('selectable') is not False], assigned_models=[row['model'] for row in routes],
        preferred_models=[row['model'] for row in routes if row['explicit']],
        catalog=catalog, models_local=[], models_central={}, models_discovered=None,
        storage=kept.get('storage'), storage_view='local',
        resources=report, resources_sampled_at=(report or {}).get('sampled_at'),
        cards=[], gpu_policy={}, data_service=state.get('data_service'), settings_report=state.get('settings_report'),
        # nothing below is the wrapper's until Core asks it: no setting, limit or block is made up here
        static_pending=pending_static,
        config=dict(residency=residency,
                    pinned={row['model']: True for row in routes if row['pinned']}), limits={}, model_pair_settings={},
        blocked_models={model: dict(blocked=True, by='operator') for model in blocks},
        model_alloc_modes={}, model_placements={}, moe_capable={}, moe_effective={}, bnb_available={},
        provisioning=[], provision_progress={}, loaded_detail={},
        # whether Core's own choice of a host may take it (wrappers/registry.py wildcard): Core's to say
        wildcard=bool(status.get('wildcard', 1)))


def workers() -> list:
    """Every saved wrapper as a worker row, each asked for its live report now."""
    kept = documents()
    by_name = {row['name']: row for row in registry.saved()}
    routes = {}
    for row in registry.model_routes():
        routes.setdefault(row['wrapper'], []).append(row)
    blocks = {}
    for row in registry.model_blocks():
        blocks.setdefault(row['wrapper'], []).append(row['model'])
    static = {}
    for row in registry.model_static():
        static.setdefault(row['wrapper'], []).append(row)
    return [worker_row(status, kept.get(status['name'], {}),
                       live(by_name[status['name']]) if status['reachable'] else None, routes.get(status['name'], ()),
                       blocks.get(status['name'], ()), static.get(status['name'], ()))
            for status in registry.status()]


LIVENESS = ('id', 'name', 'status', 'last_seen', 'cpu', 'free_ram', 'ram_free_bytes', 'ram_total', 'swap_total', 'swap_free',
            'storage', 'storage_view', 'link', 'link_ts', 'worker_state', 'state_stale', 'loaded_models', 'loading',
            'resources', 'allocations', 'cards', 'gpu_policy', 'resources_sampled_at', 'moe_effective')


def liveness(rows: list) -> list:
    """The small per-beat readings of each worker row."""
    return [dict({key: row.get(key) for key in LIVENESS}, pid_registry={},
                 gpus=[dict(index=g.get('index'), memory_free=g.get('memory_free'), memory_total=g.get('memory_total'))
                       for g in row.get('gpus') or []]) for row in rows]


def gpu_state(rows: list) -> dict:
    """Every card and host of the fleet as the console's gpu_state feed."""
    return dict(
        cards=[dict(g['gpu_state'], worker=row['name'], device=g.get('index'), name=g.get('name'), usable=g.get('memory_total'),
                    reserved=0, reason='wrapper') for row in rows for g in row.get('gpus') or []],
        hosts={row['name']: dict(mem_total=row.get('ram_total'), mem_available=row.get('free_ram'),
                                 swap_total=row.get('swap_total'), swap_free=row.get('swap_free')) for row in rows},
        activity={})


def queue(rows: list) -> dict:
    """What every wrapper is working on and holding in its queue now, counted as each wrapper says."""
    waiting = sum(int(((row.get('resources') or {}).get('queue') or {}).get('waiting') or 0) for row in rows)
    active = sum(int((row.get('resources') or {}).get('active_requests') or 0) for row in rows)
    return dict(active=[], counts=dict(waiting=waiting, active=active, total=waiting + active))


def call_log_version() -> int:
    """A number that moves when a call is added to what Core holds: a console that shows calls reads again."""
    return sql.rows("SELECT coalesce(max(rowid), 0) AS n FROM wrapper_log WHERE log = 'call_log'")[0]['n']


def feeds() -> dict:
    """Every feed of the console, as it is now."""
    rows = workers()
    return dict(workers=rows, liveness=liveness(rows), gpu_state=gpu_state(rows), activity={}, queue=queue(rows),
                slots=dict(slots=[], resources=dict(used_bytes=0, total_bytes=0)), serving=[], peers=[], jobs=[],
                downloads=[], phones=[], call_log_version=call_log_version())


def snapshot() -> dict:
    return dict(ts=time.time(), feeds=feeds(), versions={}, updated={})


def stream(send, alive, every: float = 2.0, keepalive: float = 15.0) -> None:
    """Push the feeds to one console for as long as it listens: all of them at once, then each one again when it
    reads differently. ``send(event, document)`` writes one event (None: a keep-alive line) and returns False when
    the console is gone; ``alive()`` says whether Core is still running."""
    current = feeds()
    last = {name: json.dumps(payload, sort_keys=True, default=str) for name, payload in current.items()}
    if not send('snapshot', dict(ts=time.time(), feeds=current, versions={}, updated={})):
        return
    quiet = time.monotonic()
    while alive():
        time.sleep(every)
        current, sent = feeds(), False
        for name, payload in current.items():
            text = json.dumps(payload, sort_keys=True, default=str)
            if last.get(name) == text:
                continue
            last[name] = text
            if not send('feed', dict(feed=name, version=int(time.time()), updated=time.time(), payload=payload)):
                return
            sent = True
        if sent:
            quiet = time.monotonic()
        elif time.monotonic() - quiet >= keepalive:
            quiet = time.monotonic()
            if not send(None, None):
                return
