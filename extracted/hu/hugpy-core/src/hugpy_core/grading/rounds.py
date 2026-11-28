"""A round: a mass shot of grading calls. A test fire of a wrapper is one; so is a grading of chosen models.

A round has nothing of its own but what was asked for. Each of its calls is an ordinary call to a wrapper's front
door with a grading marker in its body (the query, its tier, the round); the wrapper queues, places and answers it
like any other, and what came of it is the wrapper's call log, read by that marker (grading/read.py). So a round
that Core forgot (it was restarted) is still whole in the call log, and asking for the same round again goes on
where it stopped: what is asked is each model's queries that were not performed yet.

    plan(wrapper, ...)      what a round of a wrapper would ask: its calls, and the models it leaves out, with why
    start(kind, ...)        ask it: the round is saved and its calls are sent
    stop(round_id)          send no more, and cancel what the wrappers still hold of it
    state(round_id)         the round as it stands
    rounds(kind, wrapper)   the rounds on record, newest first

How the calls are sent. A wrapper's front door holds every call until its queue has answered it, and its queue
plans among the calls it holds: so a model's queries are sent together (one load answers them all), and as many
models at once as stay within ROUND_CALLS_AT_ONCE calls, the ones already loaded or on the worker's own drive
first. A call the door turns away before it reaches the queue (the model needs an input the query does not carry
and Core has none to give; the wrapper cannot place it at all) never reaches the call log, so the round keeps
what the door said of it (refused).
"""
from ..imports import (
    CALL_OPEN,
    GRADING_MARKER,
    ROUND_CALL_WAIT_S,
    ROUND_CALLS_AT_ONCE,
    ROUND_KINDS,
    ROUND_SETTLE_S,
    ROUND_STOP_WAIT_S,
    json,
    quote,
    threading,
    time,
    uuid,
)
from .. import sql
from ..wrappers import ask, registry
from . import read
from .queries import supply

_LIVE = {}                      # round id -> _Live: the rounds this process is sending
STOP_AT_ONCE = 8                # calls of a stopped round a wrapper is told to cancel at once
_LOCK = threading.Lock()


class Busy(Exception):
    """A round was asked of a wrapper that another round is still being sent to (``round_id``)."""

    def __init__(self, round_id: str, wrapper: str):
        super().__init__(f'a round is already being sent to {wrapper} ({round_id}): stop it, or wait for it')
        self.round_id = round_id


class _Live:
    """A round while its calls are being sent: what this process alone knows of it."""

    def __init__(self, round_id: str, wrappers: list):
        self.id, self.wrappers = round_id, list(wrappers)
        self.cond = threading.Condition()
        self.stop = threading.Event()
        self.flying = {name: 0 for name in wrappers}        # calls each wrapper's door holds now
        self.sent = 0
        self.refused = []
        self.let_go = None          # once stopped: when the round is over whatever a wrapper is still answering


def plan(wrapper: str, models=None, hot: bool = True, cold: bool = True, complete: bool = False) -> tuple:
    """What a round of one wrapper would ask -> (calls, skipped). ``calls`` is [{wrapper, model, query}] in the
    order it is sent; ``skipped`` is [{wrapper, model, reason}]. Every model the wrapper can serve is asked its
    next query that was not performed (every such query with ``complete``); a model with none left is asked its
    first again, unless ``complete``. ``models`` keeps the round to those; ``hot`` and ``cold`` say whether models
    already on the worker's own drives, and models that must first be copied there, are asked."""
    wanted = set(models) if models else None
    left, first = read.unperformed(wrapper), read.first_query(wrapper)
    calls, skipped = [], []
    found = sql.rows("SELECT id, task, engine, weight_bytes, resident, accommodated, selectable, row FROM models WHERE wrapper = ?",
                     (wrapper,))
    # loaded now, then on the worker's own drive, then what must be copied there; the smaller first
    found.sort(key=lambda m: (not m['resident'], not m['accommodated'], m['weight_bytes'] or 0, m['id']))
    for model in found:
        name = model['id']
        if wanted is not None and name not in wanted:
            continue
        said = json.loads(model['row'])
        here = bool(model['resident'] or model['accommodated'] or said.get('served_immutable'))
        if not model['selectable']:
            why = said.get('offer_reason') or said.get('possible_reason') or said.get('env_reason') or 'its wrapper does not offer it'
        elif here and not hot:
            why = "on this worker's own drives (hot): this round asks only what must be copied there"
        elif not here and not cold:
            why = "not on this worker's own drives (it would be copied there first): this round asks only what is"
        elif name not in first:
            why = (f"the grading table has no query for {model['task'] or 'a model with no task'} "
                   f"served by {model['engine'] or 'no engine'}")
        elif complete and not left[name]:
            why = 'every query of its schedule is graded or being asked'
        else:
            asking = left[name] if complete else (left[name][:1] or [first[name]])
            calls += [dict(wrapper=wrapper, model=name, query=query) for query in asking]
            continue
        skipped.append(dict(wrapper=wrapper, model=name, reason=why))
    if wanted is not None:
        skipped += [dict(wrapper=wrapper, model=name, reason='its wrapper does not have it')
                    for name in sorted(wanted - {model['id'] for model in found})]
    return calls, skipped


def start(kind: str, wrappers: list, models=None, hot: bool = True, cold: bool = True, complete: bool = False,
          asked: dict = None, by: str = None) -> dict:
    """Ask a round of ``wrappers``: it is saved and its calls are sent. Returns the round as it stands. LookupError
    for a wrapper Core has not connected or cannot ask now; Busy when one of them is still being sent a round;
    ValueError when there is nothing to ask (what was left out, and why, is said)."""
    if kind not in ROUND_KINDS:
        raise ValueError(f"a round is one of: {', '.join(ROUND_KINDS)}")
    reachable = {row['name'] for row in registry.status() if row['reachable']}
    for name in wrappers:
        if name not in reachable:
            raise LookupError(f'{name} is not a wrapper Core can ask now (hugpy-core wrappers)')
    calls, skipped = [], []
    for name in wrappers:
        found = plan(name, models, hot, cold, complete)
        calls += found[0]
        skipped += found[1]
    if not calls:
        raise ValueError('nothing to ask: ' + ('; '.join(sorted({one['reason'] for one in skipped})) or 'no model is served there'))
    round_id = f"{'tf' if kind == 'test-fire' else 'gr'}-{uuid.uuid4().hex[:12]}"
    live = _Live(round_id, wrappers)
    with _LOCK:
        for other in _LIVE.values():
            shared = set(other.wrappers) & set(wrappers)
            if shared:
                raise Busy(other.id, sorted(shared)[0])
        _LIVE[round_id] = live
    try:
        conn = sql.writer()
        try:
            with conn:
                conn.execute("INSERT INTO grading_rounds (id, kind, wrappers, asked, plan, skipped, started_at, asked_by) "
                             "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                             (round_id, kind, json.dumps(list(wrappers)),
                              json.dumps(dict(asked or {}, models=sorted(models) if models else None, hot=bool(hot),
                                              cold=bool(cold), complete=bool(complete))),
                              json.dumps(calls), json.dumps(skipped), time.time(), by))
        finally:
            conn.close()
    except Exception:
        with _LOCK:
            _LIVE.pop(round_id, None)
        raise
    threading.Thread(target=run, args=(live, calls), daemon=True, name=f'round {round_id}').start()
    return state(round_id)


def run(live: _Live, calls: list) -> None:
    """Send a round's calls, a wrapper at a time in its own thread, and note the round ended when every call has
    come back (or it was stopped and its wrappers hold none of it any more)."""
    try:
        threads = [threading.Thread(target=send, args=(live, name, [call for call in calls if call['wrapper'] == name]),
                                    daemon=True, name=f'round {live.id} {name}') for name in live.wrappers]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        settle(live)
        note(live.id, ended_at=time.time(), ended_why='stopped' if live.stop.is_set() else 'complete')
    except Exception as exc:  # noqa: BLE001  said and noted: a round never ends silently
        print(f'round {live.id}: {type(exc).__name__}: {exc}', flush=True)
        note(live.id, ended_at=time.time(), ended_why=f'failed: {type(exc).__name__}: {exc}')
    finally:
        with _LOCK:
            _LIVE.pop(live.id, None)


def settle(live: _Live) -> None:
    """Wait until Core has read, from the wrappers' call logs, every call of a round as its wrapper finished it. A
    wrapper has answered a call a moment before Core's collector reads that call's row: a round said to be over
    before then would be read with its last answers missing."""
    deadline = time.time() + ROUND_SETTLE_S
    while time.time() < deadline:
        read = sql.rows(f"SELECT count(*) AS n FROM calls WHERE grading_round = ? AND state IS NOT NULL AND "
                        f"state NOT IN ({', '.join('?' * len(CALL_OPEN))})", (live.id, *CALL_OPEN))[0]['n']
        with live.cond:
            if read >= live.sent - len(live.refused) - sum(live.flying.values()):
                return
        time.sleep(0.5)


def send(live: _Live, name: str, calls: list) -> None:
    """One wrapper's calls of a round: a model's queries together, the next model's once there is room among the
    calls its door holds; then wait for every one to come back."""
    wrapper = registry.get(name)
    asked = {query['id']: query for query in sql.rows("SELECT id, tier, endpoint, body FROM grading_queries")}
    batches = {}
    for call in calls:
        batches.setdefault(call['model'], []).append(call['query'])
    for model, queries in batches.items():
        with live.cond:
            live.cond.wait_for(lambda: live.stop.is_set() or live.flying[name] == 0
                               or live.flying[name] + len(queries) <= ROUND_CALLS_AT_ONCE)
            if live.stop.is_set() or wrapper is None:
                break
            live.flying[name] += len(queries)
            live.sent += len(queries)
        for query in queries:
            threading.Thread(target=fire, args=(live, wrapper, model, asked.get(query) or dict(id=query)), daemon=True,
                             name=f'round {live.id} call').start()
    with live.cond:
        # every call comes back; a round that was stopped lets go of a call its wrapper is still answering (the
        # answer is read from the call log all the same when it comes)
        while live.flying[name] and not (live.let_go and time.time() > live.let_go):
            live.cond.wait(1.0)


def deliver(live: _Live, wrapper: dict, endpoint: str, body: dict, key: str) -> tuple:
    """One call to a wrapper's door, held open until its queue has answered it -> (status, document). A door that
    drops the connection (a burst of calls can overrun the connections it has waiting) is asked again, a little
    later each time: the call goes under one key (Idempotency-Key), so a wrapper that did take it the first time
    answers with the row it has and never runs it twice."""
    for wait in (0.5, 1, 2, 4, 8, None):
        try:
            return ask(wrapper, endpoint, body, timeout=ROUND_CALL_WAIT_S, headers={'Idempotency-Key': key})
        except ConnectionError:
            if wait is None or live.stop.is_set():
                raise
            time.sleep(wait)


def fire(live: _Live, wrapper: dict, model: str, query: dict) -> None:
    """One call of a round: the query's body, for the model, with the grading marker. A call the wrapper's door
    says lacks an input is sent once more with the file of media/ that supplies it."""
    status, said = None, None
    try:
        if not query.get('body'):
            raise LookupError(f"the grading table no longer has the query {query['id']}")
        body = dict(json.loads(query['body']), model=model, metadata={GRADING_MARKER: dict(
            query=query['id'], tier=read.tier_name(query['tier']), round=live.id)})
        key = f"{live.id}:{query['id']}:{model}"[:200]
        status, said = deliver(live, wrapper, query['endpoint'], body, key)
        if status == 422 and isinstance(said, dict) and said.get('needs'):
            supplied = supply(said['needs'], body)
            if supplied is not None:
                status, said = deliver(live, wrapper, query['endpoint'], supplied, key)
    except Exception as exc:  # noqa: BLE001  the call did not reach the wrapper, or its answer did not reach Core
        said = dict(error=f'{type(exc).__name__}: {exc}')
    finally:
        with live.cond:
            # a call the wrapper queued is in its call log (it says its queue id); any other is only known here
            told = said if isinstance(said, dict) else {}
            if told.get('queue_id') is None:
                live.refused.append(dict(wrapper=wrapper['name'], model=model, query=query['id'], status=status, at=time.time(),
                                         error=told.get('error') or f'HTTP {status}',
                                         needs=[need.get('name') for need in told.get('needs') or []] or None))
                note(live.id, refused=json.dumps(live.refused))
            live.flying[wrapper['name']] -= 1
            live.cond.notify_all()


def note(round_id: str, **columns) -> None:
    """Write columns of a round's own row."""
    conn = sql.writer()
    try:
        with conn:
            conn.execute(f"UPDATE grading_rounds SET {', '.join(f'{name} = ?' for name in columns)} WHERE id = ?",
                         (*columns.values(), round_id))
    finally:
        conn.close()


def stop(round_id: str) -> dict:
    """Stop a round: no more of it is sent, and what its wrappers still hold of it is cancelled (a call already
    being answered finishes). Returns {id, was_running, cancelled: how many calls a wrapper was told to drop}.
    LookupError for a round that is not on record."""
    if not sql.rows("SELECT 1 FROM grading_rounds WHERE id = ?", (round_id,)):
        raise LookupError(f'no round {round_id} is on record')
    with _LOCK:
        live = _LIVE.get(round_id)
    if live is None:
        return dict(id=round_id, was_running=False, cancelled=0)
    live.stop.set()
    with live.cond:
        live.let_go = live.let_go or time.time() + ROUND_STOP_WAIT_S
        live.cond.notify_all()
    told, deadline, wrappers = set(), live.let_go, {row['name']: row for row in registry.saved()}

    def tell(row: dict) -> None:
        try:
            ask(wrappers[row['wrapper']], f"/v1/requests/{quote(row['request_id'], safe='')}/cancel", {}, timeout=30)
        except Exception as exc:  # noqa: BLE001  said; the next look tries what is still open
            print(f"round {round_id}: {row['wrapper']} was not told to cancel {row['request_id']} ({exc})", flush=True)
            told.discard(row['request_id'])

    def cancel() -> None:
        # the calls the wrappers hold are in their call logs, which Core reads within seconds: each is cancelled
        # by the id its wrapper gave it, the ones still waiting first and several at a time, until none is left
        # open or the wrappers have let go of every call
        while time.time() < deadline and any(live.flying.values()):
            found = [row for row in sql.rows(
                f"SELECT wrapper, request_id, state FROM calls WHERE grading_round = ? AND (state IS NULL OR "
                f"state IN ({', '.join('?' * len(CALL_OPEN))})) ORDER BY state = 'running', received_at DESC", (round_id, *CALL_OPEN))
                if row['request_id'] not in told and row['wrapper'] in wrappers]
            for at in range(0, len(found), STOP_AT_ONCE):
                threads = [threading.Thread(target=tell, args=(row,), daemon=True) for row in found[at:at + STOP_AT_ONCE]]
                told.update(row['request_id'] for row in found[at:at + STOP_AT_ONCE])
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
            time.sleep(1.0)
    threading.Thread(target=cancel, daemon=True, name=f'round {round_id} stop').start()
    return dict(id=round_id, was_running=True, cancelled=sum(live.flying.values()))


def close_interrupted() -> int:
    """Rounds that were being sent when Core last stopped: noted as ended then (a wrapper cancels a call whose
    caller went away). Run once, when Core starts. Returns how many."""
    conn = sql.writer()
    try:
        with conn:
            return conn.execute("UPDATE grading_rounds SET ended_at = ?, ended_why = 'interrupted: Core was restarted' "
                                "WHERE ended_at IS NULL", (time.time(),)).rowcount
    finally:
        conn.close()


def running(wrapper: str = None):
    """The id of the round being sent now (to ``wrapper``, when one is named), or None."""
    with _LOCK:
        return next((live.id for live in _LIVE.values() if wrapper is None or wrapper in live.wrappers), None)


def state(round_id: str, calls: int = None) -> dict:
    """A round as it stands: what was asked, the calls it set out to make (plan), what it left out (skipped), what
    a wrapper's door turned away (refused), how many were sent and how many its wrappers hold now (flying), and
    every call of it in the call log, newest first, with its verdict (``calls`` keeps the newest that many).
    LookupError for a round that is not on record."""
    found = sql.rows("SELECT * FROM grading_rounds WHERE id = ?", (round_id,))
    if not found:
        raise LookupError(f'no round {round_id} is on record')
    row = found[0]
    for name in ('wrappers', 'asked', 'plan', 'skipped', 'refused'):
        row[name] = json.loads(row[name])
    with _LOCK:
        live = _LIVE.get(round_id)
    logged = read.graded(round_id=round_id)
    if live is not None:
        with live.cond:
            row.update(refused=list(live.refused))
            flying, sent = sum(live.flying.values()), live.sent
    else:
        flying, sent = 0, len(logged) + len(row['refused'])
    return dict(row, running=live is not None, stopping=bool(live and live.stop.is_set()), sent=sent, flying=flying,
                logged=len(logged), calls=logged[:calls] if calls else logged)


def rounds(kind: str = None, wrapper: str = None, limit: int = 100) -> list:
    """The rounds on record, newest first: each with what was asked, how many calls it planned and left out, and
    what the call log holds of it (calls, answered, failed). Its plan and its calls are read by state()."""
    where, params = [], []
    if kind:
        where.append('r.kind = ?')
        params.append(kind)
    if wrapper:
        where.append('EXISTS (SELECT 1 FROM json_each(r.wrappers) w WHERE w.value = ?)')
        params.append(wrapper)
    found = sql.rows(
        "SELECT r.id, r.kind, r.wrappers, r.asked, r.started_at, r.ended_at, r.ended_why, r.asked_by, "
        "json_array_length(r.plan) AS planned, json_array_length(r.skipped) AS skipped, json_array_length(r.refused) AS refused, "
        "coalesce(c.calls, 0) AS calls, coalesce(c.answered, 0) AS answered, coalesce(c.failed, 0) AS failed "
        "FROM grading_rounds r LEFT JOIN (SELECT grading_round, count(*) AS calls, sum(state = 'done') AS answered, "
        "sum(state = 'failed') AS failed FROM calls WHERE grading_round IS NOT NULL GROUP BY grading_round) c "
        "ON c.grading_round = r.id"
        + (' WHERE ' + ' AND '.join(where) if where else '') + ' ORDER BY r.started_at DESC LIMIT ?',
        (*params, max(1, min(int(limit), 500))))
    with _LOCK:
        live = set(_LIVE)
    for row in found:
        row.update(wrappers=json.loads(row['wrappers']), asked=json.loads(row['asked']), running=row['id'] in live)
    return found


__all__ = ['Busy', 'close_interrupted', 'plan', 'rounds', 'running', 'start', 'state', 'stop']
