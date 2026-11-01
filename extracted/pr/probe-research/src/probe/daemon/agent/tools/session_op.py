"""the session tool: validate op and its own arguments, then run the op's handler from the registry."""

from __future__ import annotations
from probe.foundation.compat.compat import StrEnum
from typing import Callable, Literal
from probe.shared.harness.events import Kind


# ---------------------------------------------------------------------------
# session(op=...): the chat log, the logbook, the state of the record
# ---------------------------------------------------------------------------


class SessionOp(StrEnum):
    OPEN = "open"
    OUTLINE = "outline"
    SEARCH = "search"
    LOGBOOK = "logbook"
    STATUS = "status"


#: The ops as the tool's schema names them: an inline `enum` (a StrEnum would be a `$ref`).
SessionOpName = Literal[tuple(op.value for op in SessionOp)]  # type: ignore[valid-type]
#: `kind` of op=search, the same way: a free string let a guessed kind ("output")
#: answer "no event matches" for text that IS in the session.
KindName = Literal[tuple(k.value for k in Kind)]  # type: ignore[valid-type]


#: The arguments each op of `session` takes. The tool's schema is the union of
#: them all, so an argument that belongs to another op is REFUSED before
#: anything runs, never dropped: dropped, it answers a question nobody asked
#: (the lesson of #735; the old `session_search(logbook=true)` dropped `kind`
#: and the turn range that way).
SESSION_OPTIONS: dict[SessionOp, tuple[str, ...]] = {
    SessionOp.OPEN: ("event_id", "turn", "page"),
    SessionOp.OUTLINE: ("page",),
    SessionOp.SEARCH: ("query", "kind", "turn_from", "turn_to"),
    SessionOp.LOGBOOK: ("query",),
    SessionOp.STATUS: (),
}


#: The reader's ops: the session itself, and the writer's logbook (read only: so the
#: reader can say what the writer filed). `status` is the writer's own.
READER_SESSION_OPS: frozenset[SessionOp] = frozenset({SessionOp.OPEN, SessionOp.OUTLINE, SessionOp.SEARCH,
                                                      SessionOp.LOGBOOK})
ReaderSessionOpName = Literal[tuple(op.value for op in SessionOp if op in READER_SESSION_OPS)]  # type: ignore[valid-type]


def session(deps: Deps, op: str, *, status: Callable[[], str] | None = None, event_id: str | None = None,
            turn: int | None = None, page: int | None = None, query: str | None = None, kind: str | None = None,
            turn_from: int | None = None, turn_to: int | None = None) -> str:
    """The `session` tool: `op` picks what it reads, and only that op's
    arguments (`SESSION_OPTIONS`) may be given -- None or "" is not given.
    `status`: plain code's state of the record (`Worker.state_of_record`)."""
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    allowed = READER_SESSION_OPS if deps.reader else frozenset(SessionOp)
    raw = op
    try:
        op = SessionOp(op)
    except ValueError:
        op = None
    if op is None or op not in allowed:
        return f"not run: op {raw!r} is not one of: {', '.join(o.value for o in SessionOp if o in allowed)}"
    given = {"event_id": event_id, "turn": turn, "page": page, "query": query, "kind": kind,
             "turn_from": turn_from, "turn_to": turn_to}
    foreign = [name for name, value in given.items() if value not in (None, "") and name not in SESSION_OPTIONS[op]]
    if foreign:
        named = ", ".join(f"`{name}`" for name in foreign)
        options = ", ".join(SESSION_OPTIONS[op]) or "none"
        return (f"not run: {named} {'is not an option' if len(foreign) == 1 else 'are not options'} of op={op}; "
                f"its options are: {options}")
    if op in (SessionOp.SEARCH, SessionOp.LOGBOOK) and not (query or "").strip():
        return f"not run: op={op} needs `query`"
    if kind and kind not in {k.value for k in Kind}:
        return f"not run: kind {kind!r} is not one of: {', '.join(k.value for k in Kind)}"
    if op == SessionOp.OPEN:
        return session_open(deps, event_id, turn, False, page or 0)
    if op == SessionOp.OUTLINE:
        text = _outline(deps.store)
        # One line per turn has no end of its own: past a page it pages like `open`
        # (it was left to the harness's spill to a file, which is gone).
        return text if len(text) <= OPEN_PAGE_CHARS else _page(text, page or 0, "outline")
    if op == SessionOp.SEARCH:
        return session_search(deps, query or "", kind, turn_from, turn_to)
    if op == SessionOp.LOGBOOK:
        return session_search(deps, query or "", logbook=True)
    if status is None:
        return "not run: the state of the record is not available here"
    return _cap(status())
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.session_ops.open import _page, session_open  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.session_ops.outline import _outline  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.session_ops.search import session_search  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, OPEN_PAGE_CHARS, _cap  # noqa: E402 -- pieces need each other; the front door loads this one first
