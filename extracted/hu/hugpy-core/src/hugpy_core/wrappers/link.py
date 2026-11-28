"""Wrappers Core cannot open a connection to: the wrapper connects out, and Core asks over that link.

A host on another network reaches Core the way it reaches anything it downloads from; Core does not reach it. So
the wrapper holds a poll open at Core's door (hugpy-wrapper queue/link.py) and Core puts what it would have sent
on it. The wrapper sends each request to its own front door, where its own admission and queue decide: Core
suggests, the host decides.

    register(name)                  a link for the wrapper ``name``: its secret (saved as the connection's key)
    take(name, wait)                the wrapper's poll: the requests waiting for it, held up to ``wait`` s for one
    answer(name, id, ...)           the wrapper's answer to one request, whole
    answer_stream(name, id, ...)    the same, its bytes passed on as they arrive
    suggest(name, method, path ...) one request to the wrapper over its link -> its answer
    exchange(...)                   suggest, with the answer read whole -> (status, content type, bytes)

The link's state is this process's memory: Core is one process. A wrapper whose Core restarted polls again and
its link stands again; a request that was on it then is lost and its caller is told.
"""
from ..imports import (
    LINK_ALIVE_S,
    LINK_ANSWER_WAIT_S,
    LINK_MAX_BATCH,
    LINK_POLL_WAIT_S,
    LINK_STREAM_BLOCK,
    LINK_STREAM_STALL_S,
    LINK_URL,
    NAME_CHARS,
    base64,
    queue,
    secrets,
    threading,
    time,
    uuid,
)
from . import registry
from .connect import answers_as


class _Link:
    def __init__(self):
        self.cond = threading.Condition()
        self.pending = []           # requests not yet taken by a poll
        self.waiting = {}           # id -> [Event, answer or None]
        self.last_poll = 0.0


_LINKS: dict = {}
_LOCK = threading.Lock()


def _link(name: str) -> _Link:
    with _LOCK:
        return _LINKS.setdefault(name, _Link())


def alive(name: str) -> bool:
    """Whether the wrapper polled recently enough that a request put on its link will be taken."""
    return time.time() - _link(name).last_poll < LINK_ALIVE_S


def last_poll(name: str):
    return _link(name).last_poll or None


def register(name: str, by: str = None) -> dict:
    """A link for the wrapper ``name``: a new secret, saved as that connection's key. ValueError for a name that
    cannot be one; LookupError when a wrapper Core reaches directly still answers under the name."""
    name = str(name or '').strip()
    if not name or not set(name) <= NAME_CHARS:
        raise ValueError('name: letters, digits, dot, underscore or dash')
    existing = registry.get(name)
    if existing and not existing['link'] and answers_as(existing['url'], existing['key'], name):
        raise LookupError(f"{name} is connected directly at {existing['url']} and answers there: give this host "
                          f"its own name (sudo hugpy-wrapper system set worker NAME)")
    secret = 'hlk_' + secrets.token_urlsafe(32)
    registry.save(name, LINK_URL, secret, link=True, by=by)
    wake(name)
    return dict(name=name, secret=secret, poll=f'/fleet-link/{name}/poll', answer=f'/fleet-link/{name}/answer',
                state='linked', message='Linked: this wrapper polls Core for its requests; what it publishes '
                                        'appears as the collector reads it.')


def secret_of(name: str):
    """The link secret of a wrapper that connects out; None for any other."""
    row = registry.get(name)
    return row['key'] if row and row['link'] and row['key'] else None


def wake(name: str) -> None:
    """Wake an outstanding poll and cancel requests it has yet to take."""
    with _LOCK:
        link = _LINKS.get(name)
    if link is None:
        return
    with link.cond:
        link.last_poll = 0.0
        for job in link.pending:
            slot = link.waiting[job['id']]
            slot[1] = LookupError(f"{name}'s worker connection changed before it took the request")
            slot[0].set()
        link.pending.clear()
        link.cond.notify_all()


def take(name: str, wait: float = LINK_POLL_WAIT_S) -> list | None:
    """The wrapper's poll: the requests waiting for it (up to LINK_MAX_BATCH), held up to ``wait`` s for one."""
    link = _link(name)
    with link.cond:
        row = registry.get(name)
        if not row or not row['link'] or not row['connected']:
            return None
        link.last_poll = time.time()
        if not link.pending:
            link.cond.wait(max(0.0, min(float(wait), 55.0)))
        current = registry.get(name)
        if not current or not current['link'] or not current['connected'] or current['key'] != row['key']:
            return None
        jobs, link.pending[:] = link.pending[:LINK_MAX_BATCH], link.pending[LINK_MAX_BATCH:]
        link.last_poll = time.time()
        return jobs


def answer(name: str, job_id: str, status, content_type, body: bytes) -> bool:
    """The wrapper's answer to one request. False when nobody waits for it any more (its caller gave up, or Core
    restarted since)."""
    link = _link(name)
    with link.cond:
        slot = link.waiting.get(job_id)
    if slot is None:
        return False
    slot[1] = (int(status), content_type or 'application/json', body)
    slot[0].set()
    return True


def answer_stream(name: str, job_id: str, status: int, content_type: str, length: int, stream) -> bool:
    """The wrapper's answer as it streams it: its bytes go to the waiting request block by block (``stream`` is
    read ``length`` bytes). LookupError when nobody waits for it; TimeoutError when the waiting request stopped
    reading. Returns whether every byte was passed on."""
    link = _link(name)
    with link.cond:
        slot = link.waiting.get(job_id)
    if slot is None:
        raise LookupError('no request is waiting for this answer (it timed out?)')
    pipe = queue.Queue(maxsize=16)
    slot[1] = ('stream', int(status), content_type or 'application/json', int(length), pipe)
    slot[0].set()
    left = int(length)
    try:
        while left > 0:
            block = stream.read(min(LINK_STREAM_BLOCK, left))
            if not block:
                break
            pipe.put(block, timeout=LINK_STREAM_STALL_S)
            left -= len(block)
        pipe.put(None, timeout=LINK_STREAM_STALL_S)
    except queue.Full:
        raise TimeoutError('the request waiting for this answer stopped reading') from None
    return left == 0


def suggest(name: str, method: str, path: str, content_type: str = 'application/json', body: bytes = b'',
            timeout: float = LINK_ANSWER_WAIT_S):
    """One request to ``name``'s wrapper over its link -> (status, content type, bytes), or
    ('stream', status, content type, length, pipe) when the wrapper streams its answer (blocks from pipe.get(),
    None at the end). LookupError when the link is down; TimeoutError when no answer came in ``timeout`` s."""
    link = _link(name)
    if not alive(name):
        ago = f'{time.time() - link.last_poll:.0f} s ago' if link.last_poll else 'not since Core started'
        raise LookupError(f"{name}'s wrapper has not polled Core for its link ({ago}): is hugpy-wrapper running there?")
    job = dict(id=uuid.uuid4().hex, method=method, path=path, content_type=content_type,
               body_b64=base64.b64encode(body or b'').decode())
    slot = [threading.Event(), None]
    with link.cond:
        if not alive(name):
            raise LookupError(f"{name}'s worker link changed before it could take the request")
        link.waiting[job['id']] = slot
        link.pending.append(job)
        link.cond.notify_all()
    deadline = time.monotonic() + timeout
    try:
        while not slot[0].wait(min(5, max(0, deadline - time.monotonic()))):
            if time.monotonic() >= deadline:
                raise TimeoutError(f"{name}'s wrapper did not answer {method} {path} in {timeout:.0f} s")
            if not alive(name):
                raise LookupError(f"{name}'s wrapper stopped polling Core while {method} {path} was on its link")
        if isinstance(slot[1], LookupError):
            raise slot[1]
        return slot[1]
    finally:
        with link.cond:
            link.waiting.pop(job['id'], None)
            if job in link.pending:
                link.pending.remove(job)


def exchange(name: str, method: str, path: str, content_type: str = 'application/json', body: bytes = b'',
             timeout: float = LINK_ANSWER_WAIT_S) -> tuple:
    """suggest, with the answer read whole -> (status, content type, bytes)."""
    found = suggest(name, method, path, content_type, body, timeout)
    if found[0] != 'stream':
        return found
    _, status, ctype, _length, pipe = found
    blocks = []
    while True:
        block = pipe.get(timeout=LINK_STREAM_STALL_S)
        if block is None:
            return status, ctype, b''.join(blocks)
        blocks.append(block)
