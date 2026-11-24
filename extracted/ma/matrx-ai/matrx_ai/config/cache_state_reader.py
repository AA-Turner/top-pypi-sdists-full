"""Read-only view of a conversation's persisted ``cache_state`` as the send boundary loaded it at resolve.

The final-outbound snapshot (a provider-side OBSERVER) needs two facts from it — whether the conversation finished a
turn before, and its persisted seal state — and nothing else. Providers never import the send boundary itself (the
seam ``tests/package_host_contracts/test_send_boundary_guard.py`` closes: a provider that can reach the boundary can
shape the prompt at render time), so they read through this copy-returning accessor instead.
"""

from __future__ import annotations

from typing import Any


def persisted_cache_state(conversation_id: Any) -> dict[str, Any]:
    """A COPY of the conversation's memoised ``cache_state`` (``{}`` when none was loaded). Never raises."""
    try:
        from matrx_ai.config import send_boundary

        state = send_boundary._CACHE_STATE_MEMO.get(str(conversation_id))
    except Exception:  # noqa: BLE001 — an observer read never touches the call
        return {}
    return dict(state) if isinstance(state, dict) else {}


__all__ = ["persisted_cache_state"]
