"""Said once per request: the one holder a "tell the person once" guard uses.

A tool loop re-runs every send-boundary step on each provider call; a line the person reads (a
history trimmed to fit, an image converted to text) is said once per request, not once per call.
The holder always exists: the request's ``AppContext.metadata`` when there is one (shared by every
task of the request), else a context-local holder made on first use (a headless or batch run, a
test, a host with no app context). It never falls through to "say it again".
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Any

#: ``AppContext.metadata`` key holding what this request already said, by scope.
SAID_KEY = "said_this_request"

_SAID: ContextVar[dict[str, list[str]] | None] = ContextVar("matrx_ai_said_this_request", default=None)


def _holder() -> dict[str, list[str]]:
    try:
        from matrx_ai.context.app_context import try_get_app_context

        metadata: Any = getattr(try_get_app_context(), "metadata", None)
    except Exception:  # noqa: BLE001 — no context system wired: the local holder below
        metadata = None
    if isinstance(metadata, dict):
        held = metadata.get(SAID_KEY)
        if isinstance(held, dict):
            return held
        if held is None:
            fresh: dict[str, list[str]] = {}
            metadata[SAID_KEY] = fresh
            return fresh
    local = _SAID.get()
    if local is None:
        local = {}
        _SAID.set(local)
    return local


def first_time_this_request(scope: str, key: str = "") -> bool:
    """True the first time ``(scope, key)`` is asked in this request; False every time after."""
    said = _holder().setdefault(scope, [])
    if key in said:
        return False
    said.append(key)
    return True
