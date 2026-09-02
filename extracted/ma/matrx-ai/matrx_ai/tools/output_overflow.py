"""Overflow cache for gated tool results — the durable-enough home for "the rest".

When the universal soft cap truncates a tool result, the head goes to the model
and the FULL payload is stashed here, keyed by call_id, so the agent can retrieve
more on demand via the ``fetch_tool_result`` tool (the same shape as how context
works: data is available, the model is told, the model fetches deliberately).

Scope: a process-wide TTL+LRU cache. It survives across the iterations of one tool
loop (the common case — the agent fetches a few turns later in the SAME request)
and across requests of the same conversation within the TTL. Beyond that, the
fetch tool falls back to ``cx_tool_call.output`` (the ≤100K DB copy).

SECURITY — call_id is NOT globally unique (Anthropic mints unique ids, Gemini
REUSES them across turns), so a cache keyed by call_id alone could, in principle,
serve one user's stash to another. Two defenses: the key includes the
conversation_id, and ``fetch_overflow`` FAILS CLOSED on an owner (user_id)
mismatch. A handle is never honored for anyone but the user who produced it.
"""

from __future__ import annotations

from pydantic import BaseModel

from matrx_ai.tools.output_caps import TOOL_RESULT_ABSOLUTE_CEILING_CHARS
from matrx_ai.utils.cache import TTLCache

_OVERFLOW_TTL_SECONDS = 1800
# Bounds worst-case resident memory: entries × OVERFLOW_STASH_MAX_CHARS. At 128 ×
# 500K ≈ 64 MB worst case (most entries are far smaller). The LRU+TTL eviction means
# a runaway loop only churns these slots (bounded), never grows unbounded.
_OVERFLOW_MAX_ENTRIES = 128

# Retain at most this much of an oversized result for paged retrieval. The agent
# can page up to this via fetch_tool_result; past it, it should re-run the tool
# with narrower args. Bounds worst-case process memory (entries × this).
OVERFLOW_STASH_MAX_CHARS = TOOL_RESULT_ABSOLUTE_CEILING_CHARS


class _OverflowEntry(BaseModel):
    content: str
    total_chars: int  # true size before any retention cap (what the agent is told)
    user_id: str | None
    conversation_id: str | None
    tool_name: str


class OverflowSlice(BaseModel):
    """One paged read of a stashed result, returned by ``fetch_tool_result``."""

    call_id: str
    tool_name: str
    total_chars: int
    retained_chars: int
    offset: int
    returned_chars: int
    next_offset: int | None
    has_more: bool
    content: str


_store: TTLCache[_OverflowEntry] = TTLCache(
    ttl_seconds=_OVERFLOW_TTL_SECONDS, max_size=_OVERFLOW_MAX_ENTRIES
)


def _key(conversation_id: str | None, call_id: str) -> str:
    return f"{conversation_id or '_'}::{call_id}"


def stash_overflow(
    *,
    call_id: str,
    content: str,
    total_chars: int,
    user_id: str | None,
    conversation_id: str | None,
    tool_name: str,
) -> bool:
    """Stash the full (up to the retention cap) result for later paged retrieval.

    Returns True if stored, False if there was no usable call_id (without one the
    agent has no handle to fetch by). Best-effort: never raises.
    """
    if not call_id:
        return False
    retained = content[:OVERFLOW_STASH_MAX_CHARS]
    _store.set(
        _key(conversation_id, call_id),
        _OverflowEntry(
            content=retained,
            total_chars=total_chars,
            user_id=user_id or None,
            conversation_id=conversation_id or None,
            tool_name=tool_name,
        ),
    )
    return True


def fetch_overflow(
    *,
    call_id: str,
    user_id: str | None,
    conversation_id: str | None,
    offset: int,
    max_chars: int,
) -> OverflowSlice | None:
    """Return one slice of a stashed result, or None if absent / not owned.

    FAILS CLOSED on owner mismatch — a stash is only ever served back to the user
    who produced it, regardless of a colliding call_id.
    """
    if not call_id:
        return None
    entry = _store.get(_key(conversation_id, call_id))
    if entry is None:
        return None
    # SECURITY boundary: the requesting user MUST own the stash.
    if (entry.user_id or None) != (user_id or None):
        return None

    offset = max(0, int(offset))
    max_chars = max(1, int(max_chars))
    window = entry.content[offset : offset + max_chars]
    consumed = offset + len(window)
    has_more = consumed < len(entry.content)
    return OverflowSlice(
        call_id=call_id,
        tool_name=entry.tool_name,
        total_chars=entry.total_chars,
        retained_chars=len(entry.content),
        offset=offset,
        returned_chars=len(window),
        next_offset=consumed if has_more else None,
        has_more=has_more,
        content=window,
    )
