"""A call of a model, passed on to a wrapper that can serve it.

A caller asks Core. Core finds the wrappers that offer the model, takes the one where the model has the most
suitable allocation by what each publishes of itself (holders), and passes the call on to that wrapper's own front
door as it was sent. When the call
runs, and where its model goes on that host, are the wrapper's to decide (its admission, its queue, its
placement): Core chooses a host, never a place on it. The answer comes back as the wrapper gives it, a stream as
it is made, with who answered in X-Hugpy-Wrapper. A caller that hangs up is seen, and the wrapper is left too, so
it cancels what it had queued for them.

    routes()                 the paths a call is made on: what the engines of the connected wrappers answer on
    holders(model)           the wrappers that offer a model, the one to ask first
    call(door, path)         pass a call on, and its answer back
    of_model(door, path)     a read or a setting of one model (its template, its options), asked where it is offered
    fetch(door, path)        a read of what one wrapper holds (the file a call made), asked of each until one has it
    where(door, path)        where a call is, as the wrapper that has it says
    cancel(door, path)       stop a call, where it is

No call is recorded here: the wrappers record their calls, and the collector reads them. What is remembered,
in this process's memory alone, is which wrapper each of the calls passed on lately went to (by the id its caller
sent with it), so a caller's next question about its call goes to that wrapper at once.
"""
from ..imports import (
    CALL_OPEN,
    LINK_ANSWER_WAIT_S,
    LINK_STREAM_STALL_S,
    json,
    queue,
    re,
    threading,
    time,
)
from .. import sql
from ..wrappers import link, registry

CONNECT_S = 15                    # reaching a wrapper's door; the wait for its answer has no limit of Core's own
ROUTES_KEPT_S = 5.0               # the paths calls are made on are read from what was collated at most this often
PASSED_ON = ('Content-Type', 'Accept', 'Idempotency-Key')        # what of a call's headers goes with it
FORM_MODEL = re.compile(rb'name="model"\r\n\r\n([^\r\n]*)\r\n')  # the model field of a form (a transcription)
_ROUTES = [0.0, frozenset()]
SENT_IDS = ('Idempotency-Key', 'X-Hugpy-Parent-Request-Id')     # where a caller says the id it knows its call by
PASSED_KEPT = 4096                # how many of the calls passed on lately are remembered (who took each)
_PASSED = {}                      # the id a caller sent with a call -> the wrapper it was passed on to
_PASSED_LOCK = threading.Lock()


def routes() -> frozenset:
    """Every path a call is made on: the route of each engine a connected wrapper has, and the others its models
    say they answer on. Read from what the collector kept, so a wrapper's new engine is a route here without a
    change to Core."""
    if time.monotonic() - _ROUTES[0] > ROUTES_KEPT_S:
        found = {row['endpoint'] for row in sql.rows('SELECT DISTINCT endpoint FROM engines WHERE endpoint IS NOT NULL')}
        found |= {row['endpoint'] for row in sql.rows(
            "SELECT DISTINCT e.value AS endpoint FROM models m, json_each(m.endpoints) e")}
        _ROUTES[:] = [time.monotonic(), frozenset(path for path in found if isinstance(path, str) and path.startswith('/v1/'))]
    return _ROUTES[1]


def asked(raw: bytes, content_type: str):
    """The model a call names: the "model" of its JSON body, or of its form; None when it names none."""
    if (content_type or '').split(';')[0].strip().lower() == 'multipart/form-data':
        found = FORM_MODEL.search(raw)
        return found.group(1).decode(errors='replace').strip() or None if found else None
    try:
        document = json.loads(raw or b'{}')
    except ValueError:
        return None
    model = document.get('model') if isinstance(document, dict) else None
    return model if isinstance(model, str) and model else None


TIERS = ('gpu', 'ram', 'swap', 'disk')          # where a model's bytes lie, fastest first, as the wrappers name them


def shares(parts) -> tuple:
    """A placement as the share of the model on each tier, fastest first: (card, host memory, swap, disk), each
    0..1. ``parts`` is {tier: an amount} in any one unit (percent, bytes); a name that begins with a tier's is
    that tier's (disk_mmap is disk). Nothing said: no share anywhere."""
    if not isinstance(parts, dict):
        return (0.0,) * len(TIERS)
    by = {tier: sum(float(v or 0) for k, v in parts.items() if str(k).startswith(tier)) for tier in TIERS}
    total = sum(by.values())
    return tuple(by[tier] / total if total else 0.0 for tier in TIERS)


def holders(model: str, named: str = None, endpoint: str = None) -> list:
    """The wrappers that can be asked now and offer ``model``, the one to ask first: the one where the model has the
    preferred routing allocation and most suitable hardware placement (operator 2026-11-24: "it should simply route to which wrapper has the most suitable
    model allocation"), in each wrapper's own words. A wrapper says of every model how a load of it would lie there
    now (its model row: options.placed), and of a model it has loaded what that holds where (its residents). The
    most of the model on the card is first, then the most in host memory; among equals one that has it loaded,
    then one that has it on the drive it is loaded from, then the one with the fewest calls it has not finished.
    Selectable wrappers rank first. Among them explicit allocations outrank allocations from
    earlier calls and wildcard candidates. If no selectable wrapper matches, ask an allocated
    wrapper that has the model so it can answer with its own admission result.

    ``model`` is a model's id (key::variation) or its key alone: which variation a bare key means is its
    wrapper's to say. A named request narrows the choice to that wrapper. Routing blocks still exclude a wrapper."""
    found = sql.rows(
        "SELECT m.wrapper, m.id, COALESCE(m.selectable, 0) AS selectable, COALESCE(m.resident, 0) AS resident, "
        "COALESCE(m.accommodated, 0) AS accommodated, json_extract(m.row, '$.options.placed.pct') AS placed, "
        "(SELECT r.vram_bytes FROM residents r WHERE r.wrapper = m.wrapper AND r.model = m.id LIMIT 1) AS vram, "
        "(SELECT r.ram_bytes FROM residents r WHERE r.wrapper = m.wrapper AND r.model = m.id LIMIT 1) AS ram, "
        "s.wildcard, COALESCE((SELECT MAX(1 + a.explicit) FROM wrapper_model_routes a "
        "WHERE a.wrapper = m.wrapper AND (a.model = m.id OR a.model = m.model_key)), 0) AS routing_priority "
        "FROM models m JOIN wrapper_status s ON s.name = m.wrapper "
        "WHERE s.reachable = 1 "
        "AND (m.id = :model OR m.model_key = :model OR m.id = :model || '::*') "
        "AND (:named IS NULL OR m.wrapper = :named) "
        "AND (:endpoint IS NULL OR EXISTS (SELECT 1 FROM json_each(m.endpoints) e WHERE e.value = :endpoint)) "
        "AND NOT EXISTS (SELECT 1 FROM wrapper_model_blocks b WHERE b.wrapper = m.wrapper "
        "AND (b.model = m.id OR b.model = m.model_key OR b.model = :model "
        "OR (:model = m.model_key AND substr(b.model, 1, length(:model) + 2) = :model || '::')))",
        dict(model=model, named=named, endpoint=endpoint))
    found = [row for row in found if row['routing_priority'] or (row['wildcard'] and row['selectable'])]
    for row in found:
        held = dict(gpu=row['vram'] or 0, ram=row['ram'] or 0) if row['resident'] and (row['vram'] or row['ram']) else None
        try:
            row['lies'] = shares(held or json.loads(row['placed'] or 'null'))
        except ValueError:
            row['lies'] = shares(None)
    best = {}                                   # a bare key may be several variations: each wrapper's best
    for row in sorted(found, key=lambda row: (-row['selectable'], -row['routing_priority'], [-share for share in row['lies']], -row['resident'],
                                              -row['accommodated'], row['id'])):
        best.setdefault(row['wrapper'], row)
    waiting = {}
    if len(best) > 1:
        states = ', '.join('?' * len(CALL_OPEN))
        waiting = {row['wrapper']: row['calls'] for row in sql.rows(
            f"SELECT wrapper, count(*) AS calls FROM calls WHERE state IS NULL OR state IN ({states}) GROUP BY wrapper", CALL_OPEN)}
    return sorted(best.values(), key=lambda row: (-row['selectable'], -row['routing_priority'], [-share for share in row['lies']], -row['resident'],
                                                  -row['accommodated'], waiting.get(row['wrapper'], 0), row['wrapper']))


def chosen(model, named: str = None, endpoint: str = None):
    """Choose a connected wrapper. Named model calls follow the same eligibility rules."""
    if model:
        for match in holders(model, named, endpoint):
            wrapper = registry.get(match['wrapper'])
            if wrapper and wrapper['connected']:
                return dict(wrapper, routing_model=match['id'], routing_priority=match['routing_priority'])
        if not named and not registry.connected():
            raise LookupError('no wrapper is connected to this Core')
        raise LookupError(f'no eligible wrapper offers {model}' + (f' on {named}' if named else ''))
    if named:
        wrapper = registry.get(named)
        if wrapper is None or not wrapper['connected']:
            raise LookupError(f'no connected wrapper is named {named}')
        return wrapper
    live = [row['name'] for row in sql.rows('SELECT name FROM wrapper_status WHERE reachable = 1 AND wildcard = 1 ORDER BY name')]
    live = live or [row['name'] for row in registry.connected() if registry.wildcard(row['name'])]   # none read lately: the call will tell
    if not live:
        raise LookupError('no wrapper is connected to this Core that its own choice may take: there is nothing to '
                          'pass a call on to (on a host with models: sudo hugpy-wrapper system register --core URL; '
                          'a connected one is taken again with its wildcard switch)')
    if len(live) > 1:
        raise LookupError('the call names no model' + f" (GET /v1/models lists what {', '.join(live)} offer)")
    return registry.get(live[0])


def named_by(door, query: dict = None):
    """The wrapper a request itself names, if it names one: its X-Hugpy-Wrapper header, or ?wrapper=."""
    return (door.headers.get('X-Hugpy-Wrapper') or (query or {}).get('wrapper') or '').strip() or None


def refused(door, status: int, words: str, wrapper: dict = None):
    door.send_json(status, dict(error=words, source='core', **({'wrapper': wrapper['name']} if wrapper else {})))


def passed(door, wrapper: dict, path: str, raw: bytes = b'', skip=()):
    """Pass the door's request on to ``wrapper`` at ``path`` and its answer back. Returns the status passed back
    (one of ``skip`` is returned without being passed back: the door answers otherwise), None when the caller
    left or the door has already said that the wrapper did not answer."""
    said = {'X-Hugpy-Wrapper': wrapper['name']}
    kind = door.headers.get('Content-Type') or 'application/json'
    try:
        if wrapper['link']:
            return over_link(door, wrapper, path, raw, kind, said, skip)
        sent = {name: door.headers[name] for name in PASSED_ON if door.headers.get(name)}
        sent.update({name: text for name, text in door.headers.items() if name.lower().startswith('x-hugpy-')})
        return door.pass_on(wrapper['url'].rstrip('/') + path, method=door.command, data=raw or None, headers=sent,
                            bearer=wrapper['key'] or None, timeout=CONNECT_S, said=said, skip=skip)
    except TimeoutError as exc:
        return refused(door, 504, str(exc), wrapper)
    except LookupError as exc:                # its link is down
        return refused(door, 503, str(exc), wrapper)
    except OSError as exc:
        return refused(door, 502, f"{wrapper['name']}'s wrapper did not answer at {wrapper['url']}: {exc}", wrapper)


def over_link(door, wrapper: dict, path: str, raw: bytes, kind: str, said: dict, skip=()):
    """The same over the link of a wrapper that connects out (wrappers/link.py)."""
    found = link.suggest(wrapper['name'], door.command, path, kind, raw, LINK_ANSWER_WAIT_S)
    if found[0] != 'stream':
        status, answered, body = found
        if status in skip:
            return status
        door.send_json(status, bytes(body), {'Content-Type': answered, **said})
        return status
    _, status, answered, length, pipe = found
    if status in skip:
        # not this wrapper's to answer (the door asks the next): what it streams is read out and dropped, never
        # sent. It was sent: a wrapper on a link that answered 404 as a stream had its 404 passed on, and the
        # answer of the wrapper asked next was written after it as if it were its body (2026-11-24: an image
        # asked of two wrappers came back as a 404 with 360 KB of another answer behind it)
        try:
            while pipe.get(timeout=LINK_STREAM_STALL_S) is not None:
                pass
        except queue.Empty:
            pass
        return status
    door.send_response(status)
    for name, text in {'Content-Type': answered, **said}.items():
        door.send_header(name, text)
    door.close_connection = True              # its end is the end of the connection
    door.end_headers()
    try:
        while True:
            block = pipe.get(timeout=LINK_STREAM_STALL_S)
            if block is None:
                return status
            door.wfile.write(block)
            door.wfile.flush()
    except (queue.Empty, BrokenPipeError, ConnectionResetError):
        return None


def call(door, path: str, query: dict = None):
    """Pass a call on: to the wrapper chosen for the model it names (or the wrapper it names), as it was sent."""
    raw = door.read_bytes()
    try:
        wrapper = chosen(asked(raw, door.headers.get('Content-Type')), named_by(door, query), path.split('?', 1)[0])
    except LookupError as exc:
        return refused(door, 503 if 'no wrapper is connected' in str(exc) else 404, str(exc))
    if wrapper.get('routing_model') and not wrapper['routing_priority']:
        registry.record_route(wrapper['name'], wrapper['routing_model'])
    sent = next((door.headers[name] for name in SENT_IDS if door.headers.get(name)), None)
    if sent:                                  # who has it, for the caller's next question about it (holder_of)
        with _PASSED_LOCK:
            if len(_PASSED) >= PASSED_KEPT:
                for old in list(_PASSED)[:PASSED_KEPT // 4]:
                    _PASSED.pop(old, None)
            _PASSED[sent[:200]] = wrapper['name']
    return passed(door, wrapper, path, raw)


def of_model(door, path: str, model: str = None, query: dict = None):
    """A read or a setting of one model (GET /v1/models/template?model=, /v1/models/options), asked of the
    wrapper a call of it would go to."""
    raw = door.read_bytes()
    try:
        named = named_by(door, query)
        wrapper = chosen(None, named) if named else chosen(model or asked(raw, door.headers.get('Content-Type')))
    except LookupError as exc:
        return refused(door, 404, str(exc))
    return passed(door, wrapper, path, raw)


def each(door, path: str, raw: bytes, first: str = None, missing: str = 'no connected wrapper has it'):
    """Ask the wrappers one after another (``first`` before the rest) until one does not answer 404."""
    names = [row['name'] for row in sql.rows('SELECT name FROM wrapper_status WHERE reachable = 1 ORDER BY name')]
    names = names or [row['name'] for row in registry.connected()]
    for name in sorted(names, key=lambda name: name != first):
        wrapper = registry.get(name)
        if wrapper and passed(door, wrapper, path, raw, skip=(404,) if len(names) > 1 else ()) != 404:
            return None
    return refused(door, 404 if names else 503, missing if names else 'no wrapper is connected to this Core')


def fetch(door, path: str):
    """A read of what one wrapper holds, by a name only it knows (the file a call made: /v1/artifacts/ID)."""
    return each(door, path, b'', (door.headers.get('X-Hugpy-Wrapper') or '').strip() or None)


def holder_of(request_id: str):
    """The wrapper that has a call, or None: the one this Core passed it on to (remembered since), else the one
    the collector read it from. Who is asked of the call first."""
    if not request_id:
        return None
    with _PASSED_LOCK:
        name = _PASSED.get(request_id[:200])
    if name:
        return name
    held = sql.rows('SELECT wrapper FROM calls WHERE request_id = ? ORDER BY received_at DESC LIMIT 1', (request_id,))
    return held[0]['wrapper'] if held else None


def cancel(door, path: str, request_id: str = None):
    """Stop a call where it is: at the wrapper Core read it from, else asked of each."""
    return each(door, path, door.read_bytes(), holder_of(request_id), 'no connected wrapper has that call')


def where(door, path: str, request_id: str = None):
    """Where a call is (GET /v1/requests/{id}): the answer of the wrapper that has it, in its own words (queued,
    copying, loading, answering and the step its engine is at, done, failed, cancelled). The caller made the call
    through Core and knows it by the id it sent with it; which wrapper took it is Core's to find."""
    return each(door, path, b'', named_by(door) or holder_of(request_id), 'no connected wrapper has that call')


__all__ = ['asked', 'call', 'cancel', 'chosen', 'fetch', 'holder_of', 'holders', 'named_by', 'of_model', 'passed',
           'routes', 'shares', 'where']
