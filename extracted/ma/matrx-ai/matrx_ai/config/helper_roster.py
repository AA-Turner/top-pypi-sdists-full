"""THE HELPER ROSTER SLOT — the agent's helpers, restated on every send.

An agent that starts helpers (sub-agents) must know, on every model call, which of them are still
running, which finished and whether their reports reached it, which failed and which wait on the
person (Arman, 2026-10-28). The host knows its helpers; this package only places the block: one
slot of the per-turn context channel (``MessageList.attach_turn_context``), rebuilt on every loop
send, never persisted, after the prompt-cache line on providers that place it there. A send with
no helpers clears the slot.

The host installs ONE async source at boot (``set_helper_roster_source``) that returns the block
text for a conversation, or None. No source → no block (standalone posture).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

#: The turn-context slot the roster rides in.
HELPER_ROSTER_SLOT = "helpers"

#: ``async (conversation_id, organization_id) -> str | None``.
HelperRosterSource = Callable[[str, str | None], Awaitable["str | None"]]

_SOURCE: HelperRosterSource | None = None


def set_helper_roster_source(source: HelperRosterSource | None) -> None:
    """Install the host's per-conversation roster reader (``None`` = standalone)."""
    global _SOURCE
    _SOURCE = source


def get_helper_roster_source() -> HelperRosterSource | None:
    return _SOURCE


async def stage_helper_roster(
    config: Any, *, conversation_id: str | None, organization_id: str | None
) -> bool:
    """Attach (or clear) this send's roster. True when a block went out."""
    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_turn_context", None)
    if attach is None:
        return False
    source = _SOURCE
    if source is None or not conversation_id:
        attach("", slot=HELPER_ROSTER_SLOT)
        return False
    try:
        text = await source(str(conversation_id), organization_id)
    except Exception:
        # The slot never carries a stale roster: cleared, then the failure goes to the caller.
        attach("", slot=HELPER_ROSTER_SLOT)
        raise
    attach(text or "", slot=HELPER_ROSTER_SLOT)
    return bool(text)


__all__ = [
    "HELPER_ROSTER_SLOT",
    "HelperRosterSource",
    "get_helper_roster_source",
    "set_helper_roster_source",
    "stage_helper_roster",
]
