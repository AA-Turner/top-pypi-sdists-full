"""The collector: what every connected wrapper publishes, read and kept as it was published.

One thread a connected wrapper. A pass of one wrapper:

    its /health                     who it is and how it stands (a degraded wrapper is still read)
    its state                       /v1/telemetry/state?wait=&since=: the wrapper holds the read until something
                                    changed (or POLL_WAIT_S passed), so an idle wrapper costs one request a pass
    its logs, by cursor             the tables its state names (call_log, load_runs, call_stages): the rows after
                                    the last one Core has, a page at a time, each page saved as it is read. Rows
                                    that can still change (a call that is running, a load that has not ended) are
                                    read again until they settle
    its models, units and drives    read again when its state moved or its Discovery or its engines changed, at
                                    most every DOCUMENTS_MIN_S and at least every DOCUMENTS_MAX_S; a document that
                                    reads the same as the one kept is not written again

Everything is stored whole (sql/create.py): Core adds nothing to it and drops nothing from it. A wrapper's
database has an identity (store_id); the rows of one that was replaced stay, apart.

run() follows the saved connections: a wrapper that was connected is read from then on; one that was switched
off, forgotten or moved is no longer read at its old address.
"""
from ..imports import (
    DOCUMENTS,
    LOG_PAGE,
    LOG_PATH,
    OPEN_ROWS,
    PASS_MIN_S,
    POLL_WAIT_S,
    REGISTRY_LOOK_S,
    RETRY_MAX_S,
    STATE_PATH,
    json,
    threading,
    time,
    urlencode,
)
from .. import sql
from ..wrappers import ask, read, registry

DOCUMENTS_MIN_S = 10            # the models, units and drives of a busy wrapper are read at most this often
DOCUMENTS_MAX_S = 300           # and at least this often, whatever its state says
_WAKE = threading.Event()       # set when a connection was saved or switched: run() looks at once


def wake() -> None:
    """A connection changed: the collector looks at the saved connections now, not at its next look."""
    _WAKE.set()


def keep(conn, wrapper: str, name: str, document, seen: dict) -> bool:
    """Keep one document of a wrapper. One that reads the same as the last one kept is not written again
    (``seen`` remembers the last text by name for this thread). Returns whether it was written."""
    text = json.dumps(document, sort_keys=True, separators=(',', ':'))
    if seen.get(name) == text:
        return False
    conn.execute("INSERT INTO wrapper_documents (wrapper, name, document, read_at) VALUES (?, ?, ?, ?) "
                 "ON CONFLICT(wrapper, name) DO UPDATE SET document = excluded.document, read_at = excluded.read_at",
                 (wrapper, name, text, time.time()))
    seen[name] = text
    return True


def resume(conn, wrapper: str, store_id: str, log: str) -> int:
    """Where a log is read from: before the oldest row that can still change, else after the last row kept."""
    still_open = OPEN_ROWS.get(log)
    if still_open:
        oldest = conn.execute(f"SELECT min(id) FROM wrapper_log WHERE wrapper = ? AND store_id = ? AND log = ? AND ({still_open})",
                              (wrapper, store_id, log)).fetchone()[0]
        if oldest is not None:
            return int(oldest) - 1
    last = conn.execute("SELECT max(id) FROM wrapper_log WHERE wrapper = ? AND store_id = ? AND log = ?",
                        (wrapper, store_id, log)).fetchone()[0]
    return int(last or 0)


def follow_log(conn, wrapper: dict, store_id: str, log: str) -> int:
    """Read one log of a wrapper from where Core left it to its end, page by page; each page is saved when it
    is read. Returns how many rows were new or had changed."""
    name, cursor, written = wrapper['name'], resume(conn, wrapper['name'], store_id, log), 0
    while True:
        page = read(wrapper, LOG_PATH + '?' + urlencode({'table': log, 'since': cursor, 'limit': LOG_PAGE}), 60)
        if str(page.get('store_id') or '') != store_id:
            raise ValueError(f"{name}'s database changed while its {log} was read: read again")
        with conn:
            for row in page.get('rows') or []:
                written += conn.execute(
                    "INSERT INTO wrapper_log (wrapper, store_id, log, id, row) VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(wrapper, store_id, log, id) DO UPDATE SET row = excluded.row WHERE row != excluded.row",
                    (name, store_id, log, int(row['id']), json.dumps(row, sort_keys=True, separators=(',', ':')))).rowcount
        if not page.get('more'):
            return written
        following = int(page.get('next') or 0)
        if following <= cursor:
            raise ValueError(f"{name}'s {log} cursor did not advance past {cursor}")
        cursor = following


def sync_static(wrapper: dict, catalog: dict, policy: tuple) -> bool:
    """Send changed flags to a wrapper that advertises Static support. Retry failures on a later pass."""
    rows = {row['id']: row for row in catalog.get('data', ())}
    retry = False
    for model, enabled in policy:
        row = rows.get(model)
        if row is None or 'static' not in row or row['static'] is enabled:
            continue
        try:
            status, answer = ask(wrapper, '/v1/models/options', dict(model=model, static=enabled), timeout=5)
        except (OSError, LookupError):
            retry = True
            continue
        if status == 200 and isinstance(answer, dict) and answer.get('static') is enabled:
            row['static'] = enabled
        else:
            retry = True
    return retry


def sync_context(wrapper: dict, catalog: dict, edits: list) -> bool:
    """Apply queued edits in order, leaving newer edits and unsupported wrappers alone."""
    supported = {row['id'] for row in catalog.get('data', ()) if row.get('context_editable')}
    retry = False
    for edit in edits:
        model, patch = edit['model'], edit['patch']
        if model not in supported:
            continue
        try:
            status, answer = ask(wrapper, '/v1/models/options', dict(model=model, context=json.loads(patch)), timeout=10)
        except (OSError, LookupError):
            retry = True
            continue
        if status == 200 and isinstance(answer, dict) and (answer.get('context') or {}).get('editable'):
            registry.clear_context_edit(wrapper['name'], model, patch)
        else:
            retry = True
    return retry


def collect(conn, wrapper: dict, memory: dict, stop: threading.Event = None) -> dict:
    """One pass of one wrapper. ``memory`` is this wrapper's thread's own between passes (the state number it
    waits on, what it last kept, when it last read the documents). Returns {what: how many written}; nothing is
    kept of a pass whose wrapper was disconnected while its state was waited on (``stop``)."""
    name, since = wrapper['name'], memory.get('changes', -1)
    health = read(wrapper, '/health', 10, accept=(200, 503))
    query = '?' + urlencode({'wait': POLL_WAIT_S, 'since': since}) if since >= 0 else ''
    state = read(wrapper, STATE_PATH + query, POLL_WAIT_S + 30)
    if stop is not None and stop.is_set():
        return {}
    store_id = str(state.get('store_id') or '')
    if not store_id:
        raise ValueError(f'{name} did not say which database its state is of')
    seen = memory.setdefault('seen', {})
    counts = {}
    with conn:
        counts['health'] = int(keep(conn, name, 'health', health, seen))
        counts['state'] = int(keep(conn, name, 'state', state, seen))
    for log in state.get('cursor_tables') or ():
        counts[log] = follow_log(conn, wrapper, store_id, str(log))
    # what the documents are of: the state, the Discovery record and the engines of the wrapper
    policy = tuple((row['model'], bool(row['enabled'])) for row in registry.model_static(name))
    edits = registry.context_edits(name)
    marks = (state.get('changes'), ((health.get('discovery') or {}).get('catalog') or {}).get('generation'),
             (health.get('engines') or {}).get('generation'), store_id, policy, edits)
    age = time.monotonic() - memory.get('documents_at', float('-inf'))
    if age >= DOCUMENTS_MAX_S or (marks != memory.get('marks') and age >= DOCUMENTS_MIN_S):
        documents = {what: read(wrapper, path, 60) for what, path in DOCUMENTS.items()}
        retry_static = sync_static(wrapper, documents['models'], policy)
        retry_context = sync_context(wrapper, documents['models'], edits)
        with conn:
            for what, document in documents.items():
                counts[what] = int(keep(conn, name, what, document, seen))
        memory.update(marks=None if retry_static or retry_context else marks, documents_at=time.monotonic())
    with conn:
        conn.execute("INSERT INTO collector (wrapper, store_id, changes, read_at, error, error_at) VALUES (?, ?, ?, ?, NULL, NULL) "
                     "ON CONFLICT(wrapper) DO UPDATE SET store_id = excluded.store_id, changes = excluded.changes, "
                     "read_at = excluded.read_at, error = NULL, error_at = NULL",
                     (name, store_id, int(state.get('changes') or 0), time.time()))
    memory['changes'] = int(state.get('changes') or 0)
    return counts


def note_failure(wrapper: str, error: str) -> None:
    """A pass that failed, on record: a screen says why a wrapper is not being read."""
    conn = sql.writer()
    try:
        with conn:
            conn.execute("INSERT INTO collector (wrapper, error, error_at) VALUES (?, ?, ?) "
                         "ON CONFLICT(wrapper) DO UPDATE SET error = excluded.error, error_at = excluded.error_at",
                         (wrapper, error[:2000], time.time()))
    finally:
        conn.close()


def follow(wrapper: dict, stop: threading.Event) -> None:
    """The thread of one wrapper: pass after pass until ``stop``. A pass that fails is said once, noted, and
    tried again (sooner at first, at most every RETRY_MAX_S)."""
    name, memory, failures, said = wrapper['name'], {}, 0, None
    conn = sql.writer()
    try:
        while not stop.is_set():
            began = time.monotonic()
            try:
                counts = collect(conn, wrapper, memory, stop)
                if stop.is_set():
                    break
                # what is said: rows of its logs (calls, loads), and that it is read again after a failure. Its
                # documents are read again as a matter of course
                written = {what: n for what, n in counts.items() if n and what not in ('health', 'state', *DOCUMENTS)}
                if failures or written:
                    print(f"collector: {name}: " + (', '.join(f'{what} {n}' for what, n in written.items()) or 'read again'), flush=True)
                failures, said = 0, None
                stop.wait(max(0.0, PASS_MIN_S - (time.monotonic() - began)))
            except Exception as exc:  # noqa: BLE001  one wrapper's failure is said and tried again; the others go on
                memory.pop('changes', None)             # the next pass reads its state at once, without waiting on it
                failures += 1
                why = f'{type(exc).__name__}: {exc}'
                if why != said:
                    print(f'collector: {name}: {why}', flush=True)
                    said = why
                try:
                    note_failure(name, why)
                except Exception as noted:  # noqa: BLE001  the database is busy: the next failure notes it
                    print(f'collector: {name}: the failure was not noted ({noted})', flush=True)
                stop.wait(min(RETRY_MAX_S, 2 ** min(failures, 5)))
    finally:
        conn.close()


def run(stop: threading.Event) -> None:
    """Follow the saved connections until ``stop``: a thread for every wrapper that is switched on, ended when
    its connection is switched off, forgotten or changed (a changed one is read again as it is now)."""
    active = {}
    try:
        while not stop.is_set():
            try:
                wanted = {row['name']: row for row in registry.connected()}
            except Exception as exc:  # noqa: BLE001  the saved connections could not be read: the next look reads them
                print(f'collector: the saved connections were not read ({type(exc).__name__}: {exc})', flush=True)
                wanted = {name: row for name, (row, _, _) in active.items()}
            for name in list(active):
                row, ending, _ = active[name]
                if wanted.get(name) != row:
                    # its thread is told to end and is left to: it keeps nothing more (a state it is waiting on
                    # is let finish, unread). A connection that changed gets a thread of its own below, at once
                    ending.set()
                    del active[name]
                    if name not in wanted:
                        print(f'collector: {name}: no longer read', flush=True)
            for name, row in wanted.items():
                if name not in active:
                    ending = threading.Event()
                    thread = threading.Thread(target=follow, args=(row, ending), daemon=True, name=f'collect {name}')
                    active[name] = (row, ending, thread)
                    thread.start()
                    print(f"collector: {name}: reading {'its link' if row['link'] else row['url']}", flush=True)
            _WAKE.wait(REGISTRY_LOOK_S)
            _WAKE.clear()
    finally:
        for _, ending, _ in active.values():
            ending.set()


__all__ = ['collect', 'follow', 'run', 'wake']
