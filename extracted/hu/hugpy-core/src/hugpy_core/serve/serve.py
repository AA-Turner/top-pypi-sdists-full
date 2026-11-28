"""Core's door: one HTTP API. The wrappers connect here, and Core's command line and screens read here.

    GET    /health                             open: who answers here, and how Core stands (with a key: how many
                                               wrappers it has)
    GET    /api/auth/config                    open: how the console signs in (it does not: a key opens the door)
    GET    /api/console/bootstrap              open: which optional parts this install has (none)
    GET    /api/core/key                       open: whether this caller carries a key
    POST   /api/core/key                       {key}: the console's key form (shown when an action was refused for
                                               want of the key); a key of Core's is kept as a cookie
    DELETE /api/core/key                       forget the key in this browser
    GET    /api/llm/snapshot, /api/llm/events  the console's live feeds, and the same pushed as they change
    GET    /api/fleet/workers                  the wrappers as the console's worker rows
    GET    /api/models, /api/llm/calls/raw     the console's models, and the call log as the wrappers recorded it
    GET    /api/readiness, /readiness          how this install stands, for the landing page's "Your instance"
    GET    /api/fleet/catalog[/{model}]        the Models tab: every recorded model folder with its variations;
                                               one whole, with its files and the tables that hold rows of it
    GET    /api/console/schema, /api/fleet/workers/saved    the placements and knobs as the function library
                                               defines them; the saved connections (never a key)
    GET    /api/modelsdb/models | /builds | /dictionary      the fleet's models database: every recorded model
    GET    /api/modelsdb/models/{worker}/{model}[/tables/{table} | /tensors]   one model's page and its tables,
                                               read where they are: its wrapper, the call log
    POST   /api/fleet/workers/{name}/test-fire  {grade, hot, cold}: a test fire of that wrapper: a round of grading
                                               calls, each model's queries that were not performed yet
    GET    .../test-fire/current | /{job} | /history | /history/{job} | /analysis      the round as it stands, the
                                               rounds before it, and what they say of each model
    POST   .../test-fire/{job}/stop | /history/{job}/resume
    GET    /api/llm/benchmark/suites           the grading table as the console's suites
    GET    /api/llm/model-metrics2             one row a model and wrapper: its calls and its grade
    GET    /api/llm/models/{model}/metrics     every call of one model, the graded ones with their verdicts
    GET    /api/llm/benchmark/status | /runs | /runs/{run}       the round being sent, and the rounds on record
    POST   /api/llm/benchmark/run | /cancel    {models, workers}: grade chosen models; stop the round being sent
    GET    anything else                       the console: one of its built files, or its index for one of its
                                               own pages (/, /console, /docs). Without a console: what answers here
    POST   /api/fleet/workers/connect          {url, key}: connect the wrapper at url (what a wrapper's own
                                               installer posts: hugpy-wrapper system register --core URL)
    GET    /v1/wrappers                        the saved connections, each with how it stands (never a key)
    POST   /v1/wrappers/{name}/disconnect      switch a saved connection off: it is no longer read
    POST   /v1/wrappers/{name}/reconnect       switch it on again
    DELETE /v1/wrappers/{name}                 forget a connection (its calls and loads stay)
    GET    /v1/fleet                           every wrapper now: its cards, memory, loaded models and drives
    GET    /v1/calls                           ?wrapper=&model=&state=&graded=1&limit=&before=: the calls of
                                               every wrapper, newest first, without what was asked and answered
    GET    /v1/calls/{request_id}              one call whole, as its wrapper published it, with its stages
    GET    /v1/models                          ?wrapper=&search=&task=&engine=&endpoint=: the models of the fleet,
                                               each with the wrappers that can serve it, the paths it is called
                                               on and what a call of it must carry
    POST   /v1/chat/completions, /v1/images/generations, ...   a call of a model: every path an engine of a
                                               connected wrapper answers on (relay/). Core passes the call on to a
                                               wrapper that offers the model; that wrapper's queue decides when
                                               it runs. The answer says who gave it (X-Hugpy-Wrapper)
    GET    /v1/models/template, /v1/models/options   ?model=: what a call of a model must carry, and what is
                                               chosen for it, asked where it is offered (POST options: set them)
    GET    /v1/artifacts/{id}                  the file a call made, from the wrapper that made it
    GET    /v1/requests/{request_id}           where a call is, as the wrapper that has it says (queued, copying,
                                               loading, answering and its step, done, failed, cancelled)
    POST   /v1/requests/{request_id}/cancel    stop a call, where it is
    GET    /api/keys                           the keys Core gave out (never a key) and whether calls ask one
    POST   /api/keys                           {name, kind: api | guest, expires_days}: a new key, said this once
    DELETE /api/keys/{id}                      revoke one
    POST   /api/keys/prune                     {expired, older_than_days, unused_only}: remove old ones
    PUT    /api/keys/require                   {require}: whether a call of a model must carry a key
    GET    /api/keys/verify                    open: whether this caller carries a key that opens calls (what a
                                               web front asks before it lets a caller from outside through)
    GET    /v1/grading                         ?wrapper=&model=: every model's standing: graded, passed, asked next
    GET    /v1/grading/queries                 ?suite=: the grading table
    GET    /v1/grading/schedule                ?wrapper=&model=: every query of a model's schedule, with its verdict
    GET    /v1/grading/calls                   ?wrapper=&model=&round=&limit=: the calls made with a grading marker
    GET    /v1/rounds                          ?kind=&wrapper=: the rounds of grading calls on record
    POST   /v1/rounds                          {kind, wrappers, models, hot, cold, complete}: ask a round
    GET    /v1/rounds/{round}                  a round as it stands, with every call of it
    POST   /v1/rounds/{round}/stop             send no more of it, and cancel what its wrappers still hold
    POST   /api/fleet/workers/{name}/wildcard  {enabled}: whether Core's own choice of a host may take this
                                               wrapper (on unless switched off): the console's wildcard switch
    POST   /fleet-link/register                {name}: a link for a wrapper Core cannot reach -> its secret
    GET    /fleet-link/{name}/poll             ?wait=: (that wrapper) the requests Core has for it
    POST   /fleet-link/{name}/answer           (that wrapper) {id, status, content_type, body_b64}
    POST   /fleet-link/{name}/answer/{id}      (that wrapper) the answer streamed: its raw bytes

Who may ask (the operator, 2026-11-18: "it shouldnt need the key to view the console or anythig, just for
connecting a wrapper that isnt alreafdy connected"):

  to view     nothing. The console's files and what the console reads (/api/llm/..., /api/fleet/workers,
              /api/models) are open to whoever reaches this door, and so is what the console's own controls ask
              of the fleet (a test fire, a grading). Where the door is reachable from outside, what stands in
              front of it decides who views (a web front's sign-in on /api/).
  a key       to connect a wrapper (POST /api/fleet/workers/connect, /fleet-link/register), to make or revoke
              keys and turn the switch below, and for Core's own API under /v1/, which a web front may pass on
              from anywhere. A key is never replaced by where a call seems to come from: a web front or a
              forward of the port makes any caller look local.
  a call      of a model (the routes Core passes on, GET /v1/models): nothing, until the operator turns on
              "require an API key for /v1 calls" (PUT /api/keys/require); then a key, Core's own or one it gave
              out for calls (keys/keys.py). Open means open to whoever reaches this door: where the door is
              reachable from outside, the web front asks a key of the callers it does not know (GET
              /api/keys/verify), whatever the switch says.

A key Core gave out by a name (the console's API tab) opens what it was made for: calls (api, guest), or
connecting a wrapper (enroll: what a new wrapper's install carries). Two keys open everything that asks one: the key of this host's own programs, which every account of the host can read and
nothing outside it can (settings.local_key_file; Core's command line carries it), and Core's API key, which is
what another host is given (`sudo hugpy-core system key` prints it). A browser carries its key as a cookie, given
by the console's key form when an action was refused for want of it. A wrapper's poll and answers carry that
wrapper's own link secret.

The Flask category registry declares Core's fixed endpoints. Core's HTTP transport owns
request bodies, streaming, and disconnect handling.
"""
from ..imports import (
    API_PREFIXES,
    Blueprint,
    Flask,
    RoutingException,
    MethodNotAllowed,
    NotFound,
    register_categories,
    spec,
    DoorServer,
    KEY_COOKIE,
    SimpleCookie,
    ensure_secret,
    file_under,
    JsonRequestHandler,
    LINK_POLL_WAIT_S,
    PACKAGE,
    base64,
    bearer,
    json,
    key_matches,
    http_json,
    os,
    parse_qs,
    read_secret,
    signal,
    socket,
    threading,
    time,
    tool_version,
    unquote,
    urlencode,
    urlsplit,
)
from .. import collate, console, grading, keys, relay, settings, sql
from ..wrappers import Refused, connect, link, registry
from .arm_schema import arm_routes, installed_arms
from .discord import discord_status, discord_api
from ..console import predictions

OPEN, KEY, LINK, CALL, ENROLL = 'open', 'key', 'link', 'call', 'enroll'      # who may ask a route
CALL_KEYS, ENROLL_KEYS = ('api', 'guest'), ('enroll',)   # the kinds of key Core gave out that open each
STOPPING = threading.Event()                      # set when Core is told to stop: a feed held open ends


def version() -> str:
    return tool_version(PACKAGE, __file__)


def standing() -> list:
    """The saved connections with how each stands; a wrapper's own reasons as the list it gave."""
    return [dict(row, reasons=json.loads(row['reasons']) if row.get('reasons') else []) for row in registry.status()]


# ── the answers ──────────────────────────────────────────────────────────────────────────────────────────

def about(door, args, query):
    return 200, dict(service=PACKAGE, package=PACKAGE, version=version(),
                     says='hugpy-core: the coordinator of the wrappers of many hosts. This install carries no console; '
                          'its API is here (GET /health; the rest asks a key), and on its host `hugpy-core` shows the fleet.')


def auth_config(door, args, query):
    """What the console asks first: how it signs in. This Core has no accounts: a key opens its door."""
    return 200, dict(mode='open', base=None)


def console_bootstrap(door, args, query):
    """Standalone arms advertised by the local installation."""
    arms = {name: dict(version=entry.get('version'), ui=entry.get('ui'),
                       manifest=entry.get('manifest'), categories=entry['categories'])
            for name, entry in installed_arms().items()}
    return 200, dict(arms=arms, core=dict(package=PACKAGE, version=version()))


def api_schema(door, args, query):
    """List routes according to the service that answers them."""
    methods = {}
    for rule in _flask_routes.url_map.iter_rules():
        methods.setdefault(rule.rule, set()).update(rule.methods - {'HEAD', 'OPTIONS'})
    methods.pop('/v1/<path:model_endpoint>', None)
    for path in relay.routes():
        methods.setdefault(path, set()).add('POST')
    arms = {}
    for name, entry in installed_arms().items():
        routes = arm_routes(entry)
        arms[name] = dict(status='available' if routes is not None else 'unavailable',
                          version=entry.get('version'), ui=entry.get('ui'),
                          manifest=entry.get('manifest'), routes=routes)
    return 200, dict(core=[dict(path=path, methods=sorted(verbs)) for path, verbs in sorted(methods.items())],
                     arms=arms)



def key_state(door, args, query):
    """Whether this caller carries a key."""
    held = door.keyed()
    return (200, dict(keyed=held)) if held else (401, dict(error='this Core asks a key', source='client'))


def key_take(door, args, query):
    """The console's key form: {key}. A key that is Core's is given back as a cookie the browser keeps and sends
    with every request, the live feed included (a feed cannot carry a header). The page never reads it."""
    given = str(door.read_json().get('key') or '').strip()
    if not (key_matches(given, read_secret(settings.local_key_file())) or key_matches(given, read_secret(settings.api_key_file()))):
        return 401, dict(error='that is not a key of this Core (on its host: cat /etc/hugpy/core.local.key; from '
                               'elsewhere its API key: sudo hugpy-core system key)', source='client')
    secure = '; Secure' if door.headers.get('X-Forwarded-Proto') == 'https' else ''
    return 200, dict(keyed=True), {'Set-Cookie': f'{KEY_COOKIE}={given}; Path=/; Max-Age=31536000; HttpOnly; SameSite=Strict{secure}'}


def key_drop(door, args, query):
    return 200, dict(keyed=False), {'Set-Cookie': f'{KEY_COOKIE}=; Path=/; Max-Age=0; HttpOnly; SameSite=Strict'}


def console_snapshot(door, args, query):
    return 200, console.feeds.snapshot()


def console_events(door, args, query):
    """The console's live feed (server-sent events): every feed at once, then each again as it changes."""
    door.send_response(200)
    for name, value in (('Content-Type', 'text/event-stream'), ('Cache-Control', 'no-cache'), ('X-Accel-Buffering', 'no')):
        door.send_header(name, value)
    door.end_headers()

    def send(event, document) -> bool:
        text = ': keepalive\n\n' if event is None else f'event: {event}\ndata: {json.dumps(document, default=str)}\n\n'
        try:
            door.wfile.write(text.encode())
            door.wfile.flush()
            return True
        except OSError:                      # the console went away
            return False
    console.feeds.stream(send, alive=lambda: not STOPPING.is_set())
    return None


def console_workers(door, args, query):
    return 200, console.feeds.workers()


def console_models(door, args, query):
    return 200, console.catalog.models()


def console_calls_raw(door, args, query):
    return 200, console.catalog.calls_raw(limit=int(query.get('limit') or 100),
                                          before=int(query['before']) if query.get('before') else None,
                                          load=query.get('load'), worker=query.get('worker'), model=query.get('model_name'))


def console_readiness(door, args, query):
    return 200, console.catalog.readiness()


def console_folders(door, args, query):
    return 200, console.catalog.folders_list(whole=query.get('view') != 'index')


def console_folder(door, args, query):
    if query.get('records'):
        return 200, console.catalog.records(args['key'], query['records'], query.get('offset'))
    return 200, console.catalog.folder(args['key'])


def console_schema(door, args, query):
    return 200, console.catalog.schema()


def console_saved(door, args, query):
    return 200, console.catalog.saved()


def models_db(answer):
    """A read of the models database; what it could not answer goes out under the code the console knows."""
    def route(door, args, query):
        try:
            return 200, answer(args, query)
        except console.modelsdb.Unanswered as exc:
            return exc.status, dict(error=dict(code=exc.code, message=str(exc)), reason=exc.code, source='client')
    return route


def test_fire_start(door, args, query):
    return console.grading.fire(args['name'], door.read_json(), by=door.caller())


def test_fire_current(door, args, query):
    return 200, console.grading.current(args['name'])


def test_fire_job(door, args, query):
    return 200, console.grading.job(console.grading.find(args['name'], args['job']), int(query.get('limit') or 0))


def test_fire_stop(door, args, query):
    return 200, console.grading.stop_job(args['name'], args['job'])


def test_fire_history(door, args, query):
    return 200, console.grading.history(args['name'], int(query.get('limit') or 50))


def test_fire_history_run(door, args, query):
    return 200, console.grading.history_run(args['name'], args['job'])


def test_fire_resume(door, args, query):
    return console.grading.resume(args['name'], args['job'], by=door.caller())


def test_fire_analysis(door, args, query):
    return 200, console.grading.analysis(args['name'], int(query.get('runs') or 20))


def grading_suites(door, args, query):
    return 200, console.grading.suites()


def grading_metrics(door, args, query):
    return 200, console.grading.metrics(query.get('model'))


def grading_model_calls(door, args, query):
    return 200, console.grading.model_calls(args['model'], int(query.get('limit') or 2000))


def grading_run_status(door, args, query):
    return 200, console.grading.run_status()


def grading_runs(door, args, query):
    return 200, console.grading.runs()


def grading_run(door, args, query):
    return 200, console.grading.run(grading.rounds.state(args['run']))


def grading_run_start(door, args, query):
    return console.grading.start_run(door.read_json(), by=door.caller())


def grading_run_cancel(door, args, query):
    return console.grading.cancel_run()


def grading_judge(door, args, query):
    """The console's "Judge now": no model judges another here."""
    return 409, dict(status='idle', reason='answers are checked by rule (the checks of the grading table): no model judges another',
                     error='answers are checked by rule (the checks of the grading table): no model judges another')


def failed_loads(door, args, query):
    return 200, console.grading.failed_loads(query.get('model'), int(query.get('limit') or 1))


def no_review(door, args, query):
    """The console's review section (screening models on the hub) hides itself on this answer: Core grades the
    models its wrappers serve and screens none."""
    return 404, dict(error='404: this Core has no review pipeline; it grades the models its wrappers serve', source='client')


def grading_standing(door, args, query):
    return 200, dict(models=grading.read.standing(query.get('wrapper'), query.get('model')))


def grading_queries(door, args, query):
    return 200, dict(queries=grading.read.queries(query.get('suite')))


def grading_schedule(door, args, query):
    return 200, dict(schedule=grading.read.schedule(query.get('wrapper'), query.get('model')))


def grading_calls(door, args, query):
    return 200, dict(calls=grading.read.graded(query.get('wrapper'), query.get('model'), query.get('round'),
                                               limit=int(query.get('limit') or 100)))


def rounds_list(door, args, query):
    return 200, dict(rounds=grading.rounds.rounds(query.get('kind'), query.get('wrapper'), int(query.get('limit') or 100)))


def round_start(door, args, query):
    body = door.read_json()
    try:
        return 202, grading.rounds.start(body.get('kind') or 'grading', list(body.get('wrappers') or []), body.get('models') or None,
                                         hot=body.get('hot', True) is not False, cold=body.get('cold', True) is not False,
                                         complete=bool(body.get('complete')), by=door.caller())
    except grading.rounds.Busy as exc:
        return 409, dict(error=str(exc), round=exc.round_id, source='client')


def round_state(door, args, query):
    return 200, grading.rounds.state(args['round'], int(query['calls']) if query.get('calls') else None)


def round_stop(door, args, query):
    return 200, grading.rounds.stop(args['round'])


def console_file(path: str):
    """The file of the console a path names: one of its built files, or its index for one of its own pages (a
    path that names no file type: /, /console, /docs). None when this install carries no console, or the path
    names a file that is not there."""
    root = settings.console_dir()
    index = os.path.join(root, 'index.html')
    if not os.path.isfile(index):
        return None
    found = file_under(root, unquote(path))
    if found:
        return found
    return None if os.path.splitext(path)[1] else index


def health(door, args, query):
    collecting = any(t.name == 'collector' and t.is_alive() for t in threading.enumerate())
    reasons = [] if collecting else ['the collector is not running: nothing is read of the wrappers']
    said = dict(status='ok' if collecting else 'degraded', reasons=reasons, service=PACKAGE, package=PACKAGE, version=version())
    if door.keyed():                       # what Core has is said to who may ask it
        found = registry.status()
        said['wrappers'] = dict(saved=len(found), connected=sum(1 for row in found if row['connected']),
                                reachable=sum(1 for row in found if row['reachable']))
    return (200 if collecting else 503), said


def wrappers_list(door, args, query):
    return 200, dict(wrappers=standing())


def wrapper_connect(door, args, query):
    body = door.read_json()
    saved = connect(body.get('url'), body.get('key') or '', by=door.caller())
    link.wake(saved['name'])
    collate.wake()
    return 200, saved


def wrapper_switch(on: bool):
    def answer(door, args, query):
        row = registry.switch(args['name'], on)
        if row is None:
            return 404, dict(error=f"no saved connection is named {args['name']}")
        link.wake(args['name'])
        collate.wake()
        return 200, dict(registry.public(row), message='it is read again' if on else 'it is no longer read; its address and key stay saved')
    return answer


def wrapper_wildcard(door, args, query):
    """The console's wildcard switch of a worker: whether Core's own choice of a host may take it."""
    body = door.read_json()
    on = body.get('enabled') if 'enabled' in body else body.get('wildcard')
    if not isinstance(on, bool):
        raise ValueError('send {"enabled": true} or {"enabled": false}')
    now = registry.set_wildcard(args['name'], on, by=door.caller())
    if now is None:
        return 404, dict(error=f"no saved connection is named {args['name']}")
    return 200, dict(name=args['name'], wildcard=now, enabled=now,
                     message=('calls of any model it offers may be sent to it' if now else
                              'only allocated models can be routed to it'))


def model_routing_allocation(field: str):
    def answer(door, args, query):
        name, model = args['name'], args['model']
        enabled = door.read_json().get(field)
        if not model.strip() or not isinstance(enabled, bool):
            raise ValueError(f'send a model and a boolean {field}')
        if registry.get(name) is None:
            return 404, dict(error=f'no saved connection is named {name}')
        if field == 'pinned':
            if not registry.pin_route(name, model, enabled):
                return 404, dict(error='allocate this model before pinning it')
        elif enabled:
            if not registry.record_route(name, model, explicit=True):
                return 404, dict(error=f'no saved connection is named {name}')
        elif not registry.remove_route(name, model):
            return 409, dict(error='the allocation is pinned or already removed')
        return 200, dict(ok=True, model=model, worker=name, **{field: enabled})
    return answer


def model_blocked(blocked: bool):
    def answer(door, args, query):
        name, model = args['name'], args['model']
        if registry.get(name) is None:
            return 404, dict(error=f'no saved connection is named {name}')
        registry.set_model_block(name, model, blocked)
        return 200, dict(ok=True, model=model, worker=name, blocked=blocked)
    return answer


def worker_model_static(door, args, query):
    body = door.read_json()
    model, enabled = body.get('model'), body.get('static')
    if not isinstance(model, str) or not model.strip() or not isinstance(enabled, bool):
        raise ValueError('send a model and a boolean static flag')
    name = args['name']
    if not registry.set_model_static(name, model, enabled):
        return 404, dict(error=f'no saved connection is named {name}')
    return 200, dict(model=model, static=enabled)


def worker_context_edits(door, args, query):
    name = args['name']
    if door.command == 'GET':
        return 200, dict(context=next((json.loads(row['patch']) for row in registry.context_edits(name)
                                       if row['model'] == query.get('model')), {}))
    body = door.read_json()
    model, patch = body.get('model'), body.get('context')
    if not isinstance(model, str) or not model.strip() or not isinstance(patch, dict) or not patch:
        raise ValueError('send a model and a context edit')
    if patch.keys() - {'ctx', 'ctx_min', 'ctx_on'}:
        raise ValueError('context accepts ctx, ctx_min and ctx_on')
    for field in ('ctx', 'ctx_min'):
        value = patch.get(field)
        if value is not None and (type(value) is not int or value < 1):
            raise ValueError(f'{field} must be a positive token count')
    if patch.get('ctx_on') not in (None, 'gpu', 'ram'):
        raise ValueError('ctx_on must be gpu, ram or null')
    if patch.get('ctx') and patch.get('ctx_min', 0) and patch['ctx_min'] > patch['ctx']:
        raise ValueError('minimum context must be at or below maximum context')
    if not registry.save_context_edit(name, model, patch):
        return 404, dict(error=f'no saved connection is named {name}')
    return 202, dict(model=model, pending=True)


WORKER_SETTINGS_PATHS = {
    'wrapper': '/v1/settings/wrapper',
    'discovery': '/v1/settings/discovery',
    'engine': '/v1/engines',
    'storage': '/v1/drives',
}


def worker_component_settings(door, args, query):
    path = WORKER_SETTINGS_PATHS.get(args['component'])
    if door.command == 'POST' and args['component'] != 'wrapper':
        return 405, dict(error='Only Wrapper settings can be changed here.')
    if path is None:
        return 404, dict(error='Unknown worker component')
    wrapper = registry.get(args['name'])
    if wrapper is None:
        return 404, dict(error='Unknown worker')
    if not wrapper['connected']:
        return 503, dict(error=f"{args['name']} is offline. Reconnect it to read its settings.")
    if relay.passed(door, wrapper, path, door.read_bytes() if door.command == "POST" else b"", skip=(404,)) == 404:
        return 404, dict(error='This worker version does not publish this component report.')


def station_help_ask(door, args, query):
    """Send a Console question to the configured Station's read-only B chat."""
    station = os.environ.get("HUGPY_STATION_HELP_URL", "").rstrip("/")
    credentials = os.environ.get("CREDENTIALS_DIRECTORY")
    token = read_secret(os.path.join(credentials, "station-help.token")) if credentials else None
    if not station or not token:
        return 503, dict(error="Station Help is unavailable on this Core.")
    try:
        data = json.loads(door.read_bytes())
        question = data.get("question")
        text = data.get("text") or question
        history = data.get("history") or []
        if not isinstance(question, str) or not question.strip() or not isinstance(text, str) or not isinstance(history, list):
            raise ValueError
    except (AttributeError, ValueError):
        return 400, dict(error="Send a question and optional conversation history.")
    history = [{"role": row["role"], "content": row["content"][:4000]}
               for row in history[-20:] if isinstance(row, dict)
               and row.get("role") in ("user", "assistant") and isinstance(row.get("content"), str)]
    try:
        door.pass_on(station + "/api/b/chat?vm=@self", method="POST",
                     data=json.dumps(dict(text=text[:12000], history=history, console_help=True)).encode(),
                     headers={"Content-Type": "application/json", "X-Console-Token": token}, timeout=185)
    except (OSError, TimeoutError):
        return 502, dict(error="Station did not answer the Help request.")


def worker_model_action(path: str):
    """Relay a console action to its saved wrapper through the console's API."""
    def answer(door, args, query):
        wrapper = registry.get(args['name'])
        if wrapper is None or not wrapper['connected']:
            return 404, dict(error=f"no connected wrapper is named {args['name']}")
        target = path + ('?' + urlencode({'model': query['model']}) if 'model' in query else '')
        relay.passed(door, wrapper, target, door.read_bytes() if door.command == 'POST' else b'')
    return answer


def wrapper_forget(door, args, query):
    if not registry.forget(args['name']):
        return 404, dict(error=f"no saved connection is named {args['name']}")
    link.wake(args['name'])
    collate.wake()
    return 200, dict(name=args['name'], message='forgotten; its calls and loads stay on record')


def fleet(door, args, query):
    return 200, dict(wrappers=collate.fleet())


def calls(door, args, query):
    return 200, dict(calls=collate.calls(wrapper=query.get('wrapper'), model=query.get('model'), state=query.get('state'),
                                         limit=int(query.get('limit') or 50),
                                         before=float(query['before']) if query.get('before') else None,
                                         graded=query.get('graded') in ('1', 'true')))


def call(door, args, query):
    found = collate.call(args['request_id'])
    return (200, found) if found else (404, dict(error=f"Core has no call with the request id {args['request_id']}"))


def models(door, args, query):
    found = collate.models(wrapper=query.get('wrapper'), search=query.get('search'), task=query.get('task'),
                           engine=query.get('engine'), endpoint=query.get('endpoint'))
    return 200, dict(object='list', data=[dict(row, object='model', owned_by=row['engine']) for row in found])


# ── a call of a model, passed on to a wrapper (relay/) ───────────────────────────────────────────────────

def model_read(door, args, query):
    """What is asked of one model where it is offered (its template, its options)."""
    return relay.of_model(door, door.path, query.get('model'), query)


def artifact(door, args, query):
    return relay.fetch(door, door.path)


def call_cancel(door, args, query):
    return relay.cancel(door, door.path, args.get('request_id'))


def call_where(door, args, query):
    return relay.where(door, door.path, args.get('request_id'))


# ── the keys Core gives out (keys/) ──────────────────────────────────────────────────────────────────────

def keys_list(door, args, query):
    return 200, dict(keys=keys.listed(), require_key=keys.required())


def key_make(door, args, query):
    body = door.read_json()
    return 200, keys.make(body.get('name'), body.get('kind'), body.get('expires_days'), by=door.caller())


def key_revoke(door, args, query):
    if not keys.revoke(args['id']):
        return 404, dict(error=f"Core gave out no key with the id {args['id']}")
    return 200, dict(id=args['id'], message='revoked: it opens nothing from now on')


def keys_prune(door, args, query):
    body = door.read_json()
    return 200, dict(count=keys.prune(bool(body.get('expired', True)), body.get('older_than_days'), bool(body.get('unused_only'))))


def keys_require(door, args, query):
    required = door.read_json().get('require')
    if not isinstance(required, bool):
        raise ValueError('require must be a boolean')
    return 200, dict(require_key=keys.require(required, by=door.caller()))


def install_link_key(door, args, query):
    directory = os.environ.get('CREDENTIALS_DIRECTORY')
    secret = read_secret(os.path.join(directory, 'install-link-bridge')) if directory else None
    if not secret:
        return 503, dict(error='The install-link key bridge is unavailable')
    if not key_matches(door.headers.get('X-Hugpy-Install-Bridge', ''), secret):
        return 403, dict(error='Install-link bridge authentication required')
    body = door.read_json()
    action = body.get('action')
    if action == 'revoke':
        return 200, dict(revoked=keys.revoke(str(body.get('key_id') or ''), install_link_only=True))
    if action != 'create':
        raise ValueError('Unknown install-link action')
    label = str(body.get('label') or '').strip()
    link_id = str(body.get('link_id') or '')
    if not label or not 1 <= len(link_id) <= 128 or not link_id.isascii() or not link_id.replace('-', '').replace('_', '').isalnum():
        raise ValueError('A label and valid link ID are required')
    expiry = body.get('expires_at')
    try:
        days = (float(expiry) - time.time()) / 86400 if expiry is not None else None
    except (TypeError, ValueError, OverflowError):
        raise ValueError('Key expiry must be a date in the future') from None
    if days is not None and not 0 < days < float('inf'):
        raise ValueError('Key expiry must be a date in the future')
    key = keys.make(label, 'api', days, by=f'install-link:{link_id}')
    return 201, dict(id=key['id'], key=key['key'], expires_at=key['expires_at'])


def key_verify(door, args, query):
    """Whether this caller carries a key that opens calls: Core's own, or one it gave out for them. What a web
    front asks of a caller from outside, whatever the switch says."""
    held = door.keyed() or (keys.holder(bearer(door), CALL_KEYS) or {}).get('kind')
    return (200, dict(keyed=held)) if held else (401, dict(error='no key that opens calls', source='client'))


def link_register(door, args, query):
    return 200, link.register(door.read_json().get('name'), by=door.caller())


def link_poll(door, args, query):
    try:
        wait = float(query.get('wait') or LINK_POLL_WAIT_S)
    except ValueError:
        wait = LINK_POLL_WAIT_S
    jobs = link.take(args['name'], wait)
    if jobs is None:
        return 409, dict(error='Core has paused this worker link', source='core'), {'Retry-After': '300'}
    return 200, dict(jobs=jobs)


def link_answer(door, args, query):
    try:
        body = door.read_json()
        taken = link.answer(args['name'], body['id'], body['status'], body.get('content_type'),
                            base64.b64decode(body.get('body_b64') or ''))
    except (KeyError, TypeError) as exc:
        raise ValueError(f'an answer is {{id, status, content_type, body_b64}}: {exc}') from None
    return 200, dict(taken=taken)


def link_answer_stream(door, args, query):
    try:
        length = int(door.headers.get('Content-Length') or 0)
        status = int(door.headers.get('X-Hugpy-Status') or 200)
    except ValueError:
        raise ValueError('a streamed answer has Content-Length and X-Hugpy-Status') from None
    try:
        taken = link.answer_stream(args['name'], args['job'], status, door.headers.get('X-Hugpy-Content-Type'),
                                   length, door.rfile)
    except TimeoutError as exc:
        return 504, dict(error=str(exc))
    return 200, dict(taken=taken)


def model_post(door, args, query):
    """Forward model calls on the paths currently advertised by Wrappers."""
    path = urlsplit(door.path).path
    if path not in relay.routes():
        return 404, dict(error=f'no route POST {path}')
    if not door.may(CALL, {}):
        door.unkeyed('POST', CALL)
        return None
    relay.call(door, door.path, query)
    return None


DOWNLOAD_IDLE_TTL_S = 15
_download_jobs_lock = threading.Lock()
_download_jobs_idle_until = 0.0
_download_jobs_revision = 0


def download_api(path):
    """Forward a fixed Downloader route to the same host's loopback service."""
    def forward(door, args, query):
        global _download_jobs_idle_until, _download_jobs_revision
        idle_read = path == '/jobs' and door.command == 'GET' and not query
        with _download_jobs_lock:
            if idle_read and time.monotonic() < _download_jobs_idle_until:
                return 200, {'jobs': []}
            revision = _download_jobs_revision
        job_id = args.get('job_id')
        if job_id is not None and (not 6 <= len(job_id) <= 64 or not job_id.isascii() or not job_id.isalnum()):
            return 404, dict(error='Invalid download job ID')
        port = int(os.environ.get('HUGPY_DOWNLOADER_HTTP_PORT', '8767'))
        url = f'http://127.0.0.1:{port}{path.format(**args)}'
        if query:
            url += '?' + urlencode(query)
        body = door.read_json() if door.command == 'PUT' or (door.command == 'POST' and path == '/jobs') else None
        credential = None
        if path.startswith('/credentials/'):
            directory = os.environ.get('CREDENTIALS_DIRECTORY')
            credential = read_secret(os.path.join(directory, 'downloader-admin')) if directory else None
            if credential is None:
                return 503, dict(error='Downloader credential management is unavailable on this host')
        try:
            status, document = http_json(url, body, method=door.command, bearer=credential, timeout=12)
        except OSError:
            return 503, dict(error='Hugpy Downloader is unavailable on this host')
        if path.startswith('/jobs') and 200 <= status < 300:
            with _download_jobs_lock:
                if door.command != 'GET':
                    _download_jobs_revision += 1
                    _download_jobs_idle_until = 0.0
                elif path == '/jobs' and revision == _download_jobs_revision and isinstance(document, dict):
                    _download_jobs_idle_until = (time.monotonic() + DOWNLOAD_IDLE_TTL_S
                                                 if idle_read and document.get('jobs') == [] else 0.0)
        return status, document if document is not None else dict(error='Invalid response from Hugpy Downloader')

    return forward


def endpoint(method, access, handler):
    """Register a Core handler with its access policy and existing request transport."""
    def view(_door, _query, **args):
        return _door.dispatch(method, access, handler, args, _query)

    return spec(view, method, inputs='path', response='native')


ALL_CATEGORIES = {
    'health': {
        '': endpoint('GET', OPEN, health),
    },
    'api': {
        'auth/config': endpoint('GET', OPEN, auth_config),
        'console/bootstrap': endpoint('GET', OPEN, console_bootstrap),
        'core/key': [
            endpoint('GET', OPEN, key_state),
            endpoint('POST', OPEN, key_take),
            endpoint('DELETE', OPEN, key_drop),
        ],
        'keeper/help/ask': endpoint('POST', KEY, station_help_ask),
        'llm/snapshot': endpoint('GET', OPEN, console_snapshot),
        'llm/events': endpoint('GET', OPEN, console_events),
        'fleet/workers': endpoint('GET', OPEN, console_workers),
        'fleet/workers/<name>/settings/<component>': [
            endpoint('GET', OPEN, worker_component_settings),
            endpoint('POST', OPEN, worker_component_settings),
        ],
        'models': endpoint('GET', OPEN, console_models),
        'models/console': endpoint('GET', OPEN, console_models),
        'llm/calls/raw': endpoint('GET', OPEN, console_calls_raw),
        'readiness': endpoint('GET', OPEN, console_readiness),
        'fleet/catalog': endpoint('GET', OPEN, console_folders),
        'fleet/catalog/<path:key>': endpoint('GET', OPEN, console_folder),
        'schema': endpoint('GET', OPEN, api_schema),
        'console/schema': endpoint('GET', OPEN, console_schema),
        'fleet/workers/saved': endpoint('GET', OPEN, console_saved),
        'modelsdb/models': endpoint('GET', OPEN, models_db(lambda args, query: console.modelsdb.fleet(
                q=query.get('q'), status=query.get('status'), worker=query.get('worker'), engine=query.get('engine'), task=query.get('task'),
                sort=query.get('sort'), desc=query.get('desc') in ('1', 'true'), limit=int(query.get('limit') or 200),
                offset=int(query.get('offset') or 0)))),
        'modelsdb/builds': endpoint('GET', OPEN, models_db(lambda args, query: dict(
                protocol='hugpy-models-db', version=1, capability='models-db-v1', include_removed=False, builds=console.modelsdb.builds()))),
        'modelsdb/dictionary': endpoint('GET', OPEN, models_db(lambda args, query: console.modelsdb.dictionary())),
        'modelsdb/models/<worker>/<path:uid>/tables/<table>': endpoint('GET', OPEN, models_db(lambda args, query: console.modelsdb.table(
                args['worker'], args['uid'], args['table'], query.get('limit'), query.get('offset')))),
        'modelsdb/models/<worker>/<path:uid>/tensors': endpoint('GET', OPEN, models_db(lambda args, query: console.modelsdb.tensors(
                args['worker'], args['uid'], query.get('table') or 'model_tensors', query.get('after'), query.get('limit')))),
        'modelsdb/models/<worker>/<path:uid>': endpoint('GET', OPEN, models_db(lambda args, query: console.modelsdb.model(args['worker'], args['uid']))),
        'llm/db/sources': endpoint('GET', OPEN, models_db(lambda args, query: console.database.sources())),
        'llm/db/tables': endpoint('GET', OPEN, models_db(lambda args, query: console.database.tables(query.get('source')))),
        'llm/db/rows': endpoint('GET', OPEN, models_db(lambda args, query: console.database.rows(
                query.get('source'), query.get('schema'), query.get('table'), query.get('limit'), query.get('offset'), query.get('q') or '',
                query.get('column') or '', query.get('sort') or '', query.get('direction') or 'asc'))),
        'discord/status': endpoint('GET', OPEN, discord_status),
        'discord/bindings': [endpoint(method, KEY, discord_api('bindings')) for method in ('GET', 'POST')],
        'discord/bindings/<item_id>': endpoint('DELETE', KEY, discord_api('bindings/{item_id}')),
        'discord/channels': endpoint('GET', KEY, discord_api('channels')),
        'discord/users': endpoint('GET', KEY, discord_api('users')),
        'discord/outbox': endpoint('POST', KEY, discord_api('outbox')),
        'discord/bridges': [endpoint(method, KEY, discord_api('bridges')) for method in ('GET', 'POST')],
        'discord/bridges/<item_id>': endpoint('DELETE', KEY, discord_api('bridges/{item_id}')),
        'discord/bridges/<item_id>/messages': [
            endpoint(method, KEY, discord_api('bridges/{item_id}/messages')) for method in ('GET', 'DELETE')
        ],
        'discord/bridges/<item_id>/approve': endpoint('POST', KEY, discord_api('bridges/{item_id}/approve')),
        'discord/bridges/<item_id>/reject': endpoint('POST', KEY, discord_api('bridges/{item_id}/reject')),
        'discord/sessions': [endpoint(method, KEY, discord_api('sessions')) for method in ('GET', 'POST')],
        'discord/sessions/prune': endpoint('POST', KEY, discord_api('sessions/prune')),
        'discord/sessions/<item_id>': endpoint('DELETE', KEY, discord_api('sessions/{item_id}')),
        'downloads/catalog/hf': endpoint('GET', OPEN, download_api('/catalog/hf')),
        'downloads/catalog/hf/spec': endpoint('GET', OPEN, download_api('/catalog/hf/spec')),
        'downloads/catalog/civitai': endpoint('GET', OPEN, download_api('/catalog/civitai')),
        'downloads/credentials/hf': [
            endpoint(method, OPEN if method == 'GET' else KEY, download_api('/credentials/hf')) for method in ('GET', 'PUT', 'DELETE')
        ],
        'downloads/credentials/civitai': [
            endpoint(method, OPEN if method == 'GET' else KEY, download_api('/credentials/civitai')) for method in ('GET', 'PUT', 'DELETE')
        ],
        'downloads/jobs': [
            endpoint('GET', OPEN, download_api('/jobs')),
            endpoint('POST', KEY, download_api('/jobs')),
        ],
        'downloads/jobs/<job_id>': endpoint('GET', OPEN, download_api('/jobs/{job_id}')),
        'downloads/jobs/<job_id>/cancel': endpoint('POST', KEY, download_api('/jobs/{job_id}/cancel')),
        'downloads/jobs/<job_id>/retry': endpoint('POST', KEY, download_api('/jobs/{job_id}/retry')),
        'llm/db/search': endpoint('GET', OPEN, models_db(lambda args, query: console.database.search(
                query.get('source'), query.get('q'), query.get('cursor') or ''))),
        'fleet/workers/<name>/test-fire': endpoint('POST', OPEN, test_fire_start),
        'fleet/workers/<name>/test-fire/current': endpoint('GET', OPEN, test_fire_current),
        'fleet/workers/<name>/test-fire/history': endpoint('GET', OPEN, test_fire_history),
        'fleet/workers/<name>/test-fire/history/<job>': endpoint('GET', OPEN, test_fire_history_run),
        'fleet/workers/<name>/test-fire/history/<job>/resume': endpoint('POST', OPEN, test_fire_resume),
        'fleet/workers/<name>/test-fire/analysis': endpoint('GET', OPEN, test_fire_analysis),
        'fleet/workers/<name>/test-fire/<job>': endpoint('GET', OPEN, test_fire_job),
        'fleet/workers/<name>/test-fire/<job>/stop': endpoint('POST', OPEN, test_fire_stop),
        'llm/benchmark/suites': endpoint('GET', OPEN, grading_suites),
        'llm/benchmark/status': endpoint('GET', OPEN, grading_run_status),
        'llm/benchmark/runs': endpoint('GET', OPEN, grading_runs),
        'llm/benchmark/runs/<run>': endpoint('GET', OPEN, grading_run),
        'llm/benchmark/run': endpoint('POST', OPEN, grading_run_start),
        'llm/benchmark/cancel': endpoint('POST', OPEN, grading_run_cancel),
        'llm/benchmark/judge': endpoint('POST', OPEN, grading_judge),
        'llm/model-metrics2': endpoint('GET', OPEN, grading_metrics),
        'llm/models/<path:model>/metrics': endpoint('GET', OPEN, grading_model_calls),
        'llm/predictions': endpoint('GET', OPEN, lambda door, args, q: (200, dict(
            rows=predictions.recent(q.get('worker'), q.get('model'), q.get('limit', 300)),
            workers=[row['name'] for row in registry.saved()]))),
        'llm/predictions/accuracy': endpoint('GET', OPEN, lambda door, args, q: (200, dict(
            models=predictions.accuracy(q.get('worker'), q.get('model'), q.get('limit', 300))))),
        'llm/predictions/current': endpoint('GET', OPEN, lambda door, args, q: (
            200, predictions.current(q.get('worker'), q.get('model')))),
        'llm/predictions/<worker>/<request_id>': endpoint('GET', OPEN, lambda door, a, q: (
            200, predictions.detail(a['worker'], a['request_id']))),
        'llm/compute-actions': endpoint('GET', OPEN, failed_loads),
        'llm/review/status': endpoint('GET', OPEN, no_review),
        'llm/review/runs': endpoint('GET', OPEN, no_review),
        'keys': [
            endpoint('GET', OPEN, keys_list),
            endpoint('POST', KEY, key_make),
        ],
        'keys/install-link': endpoint('POST', OPEN, install_link_key),
        'keys/prune': endpoint('POST', KEY, keys_prune),
        'keys/require': endpoint('PUT', KEY, keys_require),
        'keys/verify': endpoint('GET', OPEN, key_verify),
        'keys/<id>': endpoint('DELETE', KEY, key_revoke),
        'fleet/workers/connect': endpoint('POST', ENROLL, wrapper_connect),
        'llm/models/<path:model>/workers/<name>/block': endpoint('POST', OPEN, model_blocked(True)),
        'llm/models/<path:model>/workers/<name>/unblock': endpoint('POST', OPEN, model_blocked(False)),
        'models/database/<path:model>/workers/<name>/assigned': endpoint('POST', OPEN, model_routing_allocation('assigned')),
        'models/database/<path:model>/workers/<name>/pinned': endpoint('POST', OPEN, model_routing_allocation('pinned')),
        'fleet/workers/<name>/wildcard': endpoint('POST', OPEN, wrapper_wildcard),
        'fleet/workers/<name>/disconnect': endpoint('POST', OPEN, wrapper_switch(False)),
        'fleet/workers/<name>/reconnect': endpoint('POST', OPEN, wrapper_switch(True)),
        'fleet/workers/<name>/model-static': endpoint('POST', OPEN, worker_model_static),
        'fleet/workers/<name>/model-context': [
            endpoint('GET', OPEN, worker_context_edits),
            endpoint('POST', OPEN, worker_context_edits),
        ],
        'fleet/workers/<name>/model-context-preview': endpoint('POST', OPEN, worker_model_action('/v1/models/context-preview')),
        'fleet/workers/<name>/model-layer-map': endpoint('GET', OPEN, worker_model_action('/v1/models/layer-map')),
        'fleet/workers/<name>/model-options': [
            endpoint('GET', OPEN, worker_model_action('/v1/models/options')),
            endpoint('POST', OPEN, worker_model_action('/v1/models/options')),
        ],
        'fleet/workers/<name>/load': endpoint('POST', OPEN, worker_model_action('/v1/load')),
        'fleet/workers/<name>/unload': endpoint('POST', OPEN, worker_model_action('/v1/unload')),
    },
    'readiness': {
        '': endpoint('GET', OPEN, console_readiness),
    },
    'v1': {
        'wrappers': endpoint('GET', KEY, wrappers_list),
        'wrappers/<name>/disconnect': endpoint('POST', KEY, wrapper_switch(False)),
        'wrappers/<name>/reconnect': endpoint('POST', KEY, wrapper_switch(True)),
        'wrappers/<name>': endpoint('DELETE', KEY, wrapper_forget),
        'fleet': endpoint('GET', KEY, fleet),
        'calls': endpoint('GET', KEY, calls),
        'calls/<request_id>': endpoint('GET', KEY, call),
        'models': endpoint('GET', CALL, models),
        'models/template': endpoint('GET', CALL, model_read),
        'models/options': [
            endpoint('GET', CALL, model_read),
            endpoint('POST', KEY, model_read),
        ],
        'load': endpoint('POST', KEY, model_read),
        'unload': endpoint('POST', KEY, model_read),
        'artifacts/<path:id>': endpoint('GET', CALL, artifact),
        'requests/<request_id>': endpoint('GET', CALL, call_where),
        'requests/<request_id>/cancel': endpoint('POST', CALL, call_cancel),
        'grading': endpoint('GET', KEY, grading_standing),
        'grading/queries': endpoint('GET', KEY, grading_queries),
        'grading/schedule': endpoint('GET', KEY, grading_schedule),
        'grading/calls': endpoint('GET', KEY, grading_calls),
        'rounds': [
            endpoint('GET', KEY, rounds_list),
            endpoint('POST', KEY, round_start),
        ],
        'rounds/<round>': endpoint('GET', KEY, round_state),
        'rounds/<round>/stop': endpoint('POST', KEY, round_stop),
        '<path:model_endpoint>': endpoint('POST', OPEN, model_post),
    },
    'fleet-link': {
        'register': endpoint('POST', ENROLL, link_register),
        '<name>/poll': endpoint('GET', LINK, link_poll),
        '<name>/answer': endpoint('POST', LINK, link_answer),
        '<name>/answer/<job>': endpoint('POST', LINK, link_answer_stream),
    },
}


def _route_registry():
    app = Flask(__name__, static_folder=None)
    app.url_map.merge_slashes = False
    blueprint = Blueprint('core', __name__)
    register_categories(blueprint, ALL_CATEGORIES)
    app.register_blueprint(blueprint)
    return app


_flask_routes = _route_registry()


class Door(JsonRequestHandler):
    server_version = 'hugpy-core'

    def keyed(self):
        """Which key the caller carries: 'local' (the key of this host's own programs), 'api' (Core's API key),
        or None."""
        given = bearer(self)
        if not given:                      # a browser: the cookie its key form was given (/api/core/key)
            cookie = SimpleCookie(self.headers.get('Cookie') or '').get(KEY_COOKIE)
            given = cookie.value if cookie else ''
            origin = self.headers.get('Origin')
            if given and origin and self.command != 'GET' and urlsplit(origin).netloc != (self.headers.get('Host') or ''):
                return None                # a page of another site may not act with this browser's key
        if key_matches(given, read_secret(settings.local_key_file())):
            return 'local'
        return 'api' if key_matches(given, read_secret(settings.api_key_file())) else None

    def caller(self) -> str:
        """Who asks, for the record of what was saved or asked: a program of this host, the holder of the API
        key, or (where no key is asked) whoever reached the door."""
        held = self.keyed()
        return ('a program of this host' if held == 'local' else f'the API key, from {self.client_address[0]}' if held
                else f'the console, from {self.client_address[0]}')

    def may(self, access: str, args: dict) -> bool:
        if access == OPEN:
            return True
        if access == LINK:
            return key_matches(bearer(self), link.secret_of(args.get('name') or ''))
        if self.keyed() is not None:
            return True
        if access == CALL:                 # a call of a model: open until the operator turns the switch
            return not keys.required() or keys.holder(bearer(self), CALL_KEYS) is not None
        return access == ENROLL and keys.holder(bearer(self), ENROLL_KEYS) is not None

    def unkeyed(self, method: str, access: str):
        """Say that a route asks a key, and which."""
        if access == CALL:
            return self.send_json(401, dict(
                error="this Core asks a key for calls of models: send Authorization: Bearer <key> (a key is made in "
                      "the console's API tab; on Core's host its own programs carry /etc/hugpy/core.local.key)",
                source='client'))
        # The browser prompts for the key on protected actions.
        return self.send_json(401, dict(
            error="this asks Core's key: send Authorization: Bearer <key>, or give the console the key "
                  "(on Core's host: cat /etc/hugpy/core.local.key; from elsewhere its API key: sudo hugpy-core system key)",
            source='client'), {'X-Hugpy-Core-Key': 'needed'} if access in (KEY, ENROLL) else {})

    def dispatch(self, method, access, function, args, query):
        if not self.may(access, args):
            if access == LINK:
                return self.send_json(401, dict(error=f"not {args.get('name')}'s link secret: register again (sudo "
                                                      f"hugpy-wrapper system register --core CORE --link)", source='client'))
            return self.unkeyed(method, access)
        try:
            said = function(self, args, query)
            return self.send_json(*said) if said is not None else None       # None: it answered by itself (a feed)
        except Refused as exc:
            return self.send_json(exc.status, dict(error=str(exc), source='client'))
        except LookupError as exc:
            return self.send_json(404, dict(error=str(exc), source='client'))
        except ValueError as exc:
            return self.send_json(400, dict(error=str(exc), source='client'))
        except BrokenPipeError:
            return None                   # the caller left before its answer
        except Exception as exc:  # noqa: BLE001  said, to the caller and the log; the door stays open
            print(f'door: {method} {urlsplit(self.path).path} failed: {type(exc).__name__}: {exc}', flush=True)
            return self.send_json(500, dict(error=f'{type(exc).__name__}: {exc}', source='core-internal'))

    def answer(self, method: str) -> None:
        url = urlsplit(self.path)
        query = {key: values[0] for key, values in parse_qs(url.query).items()}
        try:
            route, args = _flask_routes.url_map.bind('').match('/' + url.path.strip('/'), method=method)
        except (NotFound, MethodNotAllowed, RoutingException):
            pass
        else:
            return _flask_routes.view_functions[route](
                _door=self, _query=query, **{name: unquote(value) for name, value in args.items()})
        if method == 'GET' and not url.path.startswith(API_PREFIXES):
            found = console_file(url.path)
            if found:           # a built file carries its content in its name and may be kept; a page is asked for again
                kept = 'public, max-age=31536000, immutable' if url.path.startswith('/assets/') else 'no-cache'
                return self.send_file(found, {'Cache-Control': kept})
            if url.path == '/':
                return self.send_json(*about(self, {}, query))
        return self.send_json(404, dict(error=f'no route {method} {url.path}'))

    def do_GET(self):
        self.answer('GET')

    def do_POST(self):
        self.answer('POST')

    def do_DELETE(self):
        self.answer('DELETE')

    def do_PUT(self):
        self.answer('PUT')


def serve(host: str = None, port: int = None) -> None:
    """Run Core: its door and the collector, until it is told to stop."""
    saved_host, saved_port = settings.address()
    host, port = host or saved_host, int(port or saved_port)
    probe = socket.socket()              # the address, before anything is started: in use is said, not raised later
    probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        probe.bind((host, port))
    except OSError as exc:
        raise SystemExit(f'hugpy-core: {host}:{port} cannot be served ({exc.strerror}): something else has it. '
                         f'Another port: hugpy-core set port N') from None
    finally:
        probe.close()
    database = sql.prepare()
    grading.prepare()
    if not settings.is_service_host():     # one account's own Core: the key its command line carries is made here
        ensure_secret(settings.local_key_file(), say=lambda *said: None)
    httpd = DoorServer((host, port), Door)
    registry.clear_unpinned_routes()
    print(f'hugpy-core {version()} on http://{host}:{port}  (db {database})', flush=True)
    stop = threading.Event()
    threading.Thread(target=collate.run, args=(stop,), daemon=True, name='collector').start()

    def ending(signum, frame):
        stop.set()
        STOPPING.set()
        threading.Thread(target=httpd.shutdown, daemon=True, name='door-shutdown').start()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, ending)
    httpd.serve_forever()
    httpd.server_close()


__all__ = ['ALL_CATEGORIES', 'Door', 'serve', 'version']
