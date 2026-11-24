"""WHAT THIS PERSON ASKED US TO REMEMBER — their saved memories and custom instructions, on every chat turn.

ChatGPT's champion behaviour (CGU-10): what the person told it to remember, what the assistant saved,
and two standing instructions (about me / how to respond) reach every new chat. A temporary chat
uses them only when the person opts in for that turn, and a confidential (sealed) chat never reads
them.

The gate lives HERE, pure, on the carried AppContext (``person_context_decision``); the words come
from the host's ONE source (``set_person_context_source``: aidream reads the person's own
``users.user_memory`` files and ``chat.agent_memory`` facts as them, and checks the agent's
``reads_memory`` setting). No source bound -> no block, announced once.

Placement: the per-turn context channel (slot ``person_context``), staged by the send boundary at
every loop send (``send_boundary._stage_person_context``) — never the frozen or held system prefix,
so a memory added between turns reaches the next turn of an OLD conversation without breaking its
cached prefix. Rendered once per turn (memo by ``request_id``) so a long tool loop reads the store
once.
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from matrx_utils import vcprint

#: The turn-context policy the block rides in.
PERSON_CONTEXT_SLOT = "person_context"

#: ``AppContext.metadata`` key carrying the turn's choice (aidream ``ScopedRequest.use_person_memory``):
#: True = use them (a temporary chat's opt-in), False = not on this turn, absent = the default.
USE_PERSON_MEMORY_KEY = "use_person_memory"

#: ``AppContext.metadata`` key a dry run (the Model view capture) sets: the ``store`` the REAL run carries.
#: A capture forces ``store=False`` so it writes nothing; without this the gate read every dry run as a
#: temporary chat and the preview withheld the block the real send carries (PB-07 N3, 2026-11-18).
CAPTURE_WIRE_STORE_KEY = "capture_wire_store"

_CAPTURE_WIRE_STORE: ContextVar[bool | None] = ContextVar("matrx_ai_capture_wire_store", default=None)


@contextmanager
def capturing_wire_store(wire_store: bool) -> Iterator[None]:
    """Wrap a dry run's PREPARATION: every ``store`` gate that decides what reaches the model answers as the
    REAL run would (``wire_store`` = the ``store`` the real send carries), while the run itself stays ephemeral."""
    token = _CAPTURE_WIRE_STORE.set(bool(wire_store))
    try:
        yield
    finally:
        _CAPTURE_WIRE_STORE.reset(token)


def preparing_dry_run() -> bool:
    """True inside a dry run's preparation (``capturing_wire_store``): such a run writes nothing."""
    return _CAPTURE_WIRE_STORE.get() is not None


def wire_store(ctx: Any, requested: bool | None = None) -> bool:
    """The ``store`` the REAL send carries: a dry run reports the real run's, never its own ``store=False``.

    Every gate that decides WHAT REACHES THE MODEL (observational memory, the person's saved memories) reads
    this; a gate that decides what is WRITTEN keeps reading ``ctx.store``. ``requested`` = the request's own
    ``store`` when the caller holds it (a dry run's request was already forced ephemeral)."""
    held = _CAPTURE_WIRE_STORE.get()
    if held is not None:
        return held
    metadata = getattr(ctx, "metadata", None) or {}
    if CAPTURE_WIRE_STORE_KEY in metadata:
        return bool(metadata[CAPTURE_WIRE_STORE_KEY])
    if requested is not None:
        return bool(requested) and bool(getattr(ctx, "store", True))
    return bool(getattr(ctx, "store", True))


PERSON_CONTEXT_OPEN = '<person_context source="saved by the person">'
PERSON_CONTEXT_CLOSE = "</person_context>"

#: ``(ctx)`` or ``(ctx, tool_names=frozenset)`` — the second form is called only when the run's tool set is known.
PersonContextSource = Callable[..., Awaitable[str | None]]

_SOURCE: PersonContextSource | None = None
_announced_unbound = False
_MAX_MEMO = 512
_MEMO: OrderedDict[str, str] = OrderedDict()


def set_person_context_source(source: PersonContextSource | None) -> None:
    """Install the host's ``AppContext -> framed block | None`` reader (``None`` = standalone)."""
    global _SOURCE, _announced_unbound
    _SOURCE = source
    _announced_unbound = False
    _MEMO.clear()


def get_person_context_source() -> PersonContextSource | None:
    return _SOURCE


def person_context_decision(ctx: Any) -> tuple[bool, str]:
    """May this turn read the person's memory and instructions? ``(yes, why)`` — pure.

    Order matters: sealed beats every opt-in; a machine or child run is never a person's chat."""
    if ctx is None:
        return False, "no carried request context"
    if getattr(ctx, "sealed_conversation_id", None):
        return False, "confidential chat"
    if not str(getattr(ctx, "user_id", "") or ""):
        return False, "no person"
    if getattr(ctx, "system_run", False) or getattr(ctx, "is_internal_agent", False):
        return False, "machine run"
    if getattr(ctx, "parent_request_id", None):
        return False, "child run"
    metadata = getattr(ctx, "metadata", None) or {}
    choice = metadata.get(USE_PERSON_MEMORY_KEY)
    if choice is False:
        return False, "turned off for this turn"
    # A dry run decides as the real send would (its own ``store=False`` only means "write nothing").
    if not wire_store(ctx):
        if choice is True:
            return True, "temporary chat, opted in"
        return False, "temporary chat"
    return True, "saved chat"


def frame(sections: list[tuple[str, str]]) -> str:
    """The framed block from ``(tag, text)`` sections; ``""`` when every section is blank (pure)."""
    parts = [f"<{tag}>\n{text.strip()}\n</{tag}>" for tag, text in sections if text and text.strip()]
    if not parts:
        return ""
    return PERSON_CONTEXT_OPEN + "\n" + "\n".join(parts) + "\n" + PERSON_CONTEXT_CLOSE


async def render_person_context(ctx: Any, tool_names: frozenset[str] | None = None) -> tuple[str, str]:
    """THE ONE RENDERER — ``(block, why)`` for the carried context. ``block`` is ``""`` when the gate
    says no or the person has nothing saved. A source failure raises to the caller."""
    global _announced_unbound
    allowed, why = person_context_decision(ctx)
    if not allowed:
        return "", why
    if _SOURCE is None:
        if not _announced_unbound:
            _announced_unbound = True
            vcprint(
                "[person_context] no host source bound; chats do not see the person's saved "
                "memories or instructions (bind one with set_person_context_source())",
                color="yellow",
            )
        return "", "no source bound"
    key = str(getattr(ctx, "request_id", "") or "")
    if key and tool_names:
        key += "|" + ",".join(sorted(tool_names))  # a changed tool set re-renders its flags
    if key and key in _MEMO:
        return _MEMO[key], why
    block = (await (_SOURCE(ctx, tool_names=tool_names) if tool_names else _SOURCE(ctx))) or ""
    if key:
        _MEMO[key] = block
        while len(_MEMO) > _MAX_MEMO:
            _MEMO.popitem(last=False)
    return block, why


__all__ = [
    "CAPTURE_WIRE_STORE_KEY",
    "capturing_wire_store",
    "preparing_dry_run",
    "wire_store",
    "PERSON_CONTEXT_CLOSE",
    "PERSON_CONTEXT_OPEN",
    "PERSON_CONTEXT_SLOT",
    "USE_PERSON_MEMORY_KEY",
    "frame",
    "get_person_context_source",
    "person_context_decision",
    "render_person_context",
    "set_person_context_source",
]
