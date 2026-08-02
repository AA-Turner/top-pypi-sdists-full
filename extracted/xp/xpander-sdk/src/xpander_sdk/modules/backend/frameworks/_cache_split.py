"""Where to cut the system prompt so a changing tail does not cost the whole prefix.

agno appends ``additional_context`` into the system message, and both cache
wrappers put their breakpoint after the whole block. Prompt caching matches an
exact prefix, so an agent whose per-request context changes between turns misses
on system AND on every message after it — the conversation breakpoint sits
downstream of the system block. The gateway rebuilds that context every turn,
which makes its whole prompt full-price input at 10x the cache-read rate.

Splitting the block puts a breakpoint between the stable instructions and the
per-request tail. A breakpoint is a caching directive, not content: the rendered
prompt is byte-identical either way.
"""

from __future__ import annotations

import contextvars
from typing import Optional, Tuple

# Providers bill a cache write and enforce a minimum cacheable size, so a tiny
# stable half would burn a breakpoint for nothing. ~4K chars ≈ the 1024-token floor.
MIN_STABLE_CHARS = 4_000

# Below this the tail is not worth isolating — the single breakpoint already works.
MIN_VOLATILE_CHARS = 500

# Per-request override for callers that share one model instance across concurrent
# runs — the agent gateway caches its models in a process-wide LRU, so an attribute
# on the instance would be overwritten by whichever conversation ran last.
current_volatile_system: "contextvars.ContextVar[Optional[str]]" = (
    contextvars.ContextVar("xp_volatile_system", default=None)
)


def resolve_volatile(fallback: Optional[str]) -> Optional[str]:
    """The per-request tail: context var first, then the instance attribute."""
    return current_volatile_system.get() or fallback


# "<task_id>:<agent_id>" for the run this request belongs to. The cache wrappers see
# the real wire payload but not the run, and their model instances are shared, so the
# owner has to ride the request rather than the object.
current_prompt_owner: "contextvars.ContextVar[str]" = contextvars.ContextVar(
    "xp_prompt_owner", default=""
)


def split_system_text(
    text: Optional[str], volatile: Optional[str]
) -> Optional[Tuple[str, str]]:
    """``(stable, volatile_tail)`` when *volatile* is worth isolating, else None.

    Returning None means "leave the caller's existing single-breakpoint behaviour
    alone", which is what every guard below falls back to.
    """
    if not text or not volatile:
        return None
    tail = volatile.strip()
    if len(tail) < MIN_VOLATILE_CHARS:
        return None
    index = text.find(tail)
    # index 0 means the whole system message is volatile — nothing to cache before it.
    if index <= 0:
        return None
    stable = text[:index]
    if len(stable) < MIN_STABLE_CHARS:
        return None
    return stable, text[index:]
