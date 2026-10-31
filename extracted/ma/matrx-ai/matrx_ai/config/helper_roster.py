"""THE HELPER ROSTER SLOT — the agent's helpers, restated on every send.

An agent that starts helpers (sub-agents) must know, on every model call, which of them are still
running, which finished and whether their reports reached it, which failed and which wait on the
person (Arman, 2026-10-28). The host knows its helpers; this package only places the block, rebuilt
on every loop send, never persisted, in BOTH per-send channels under the same slot name:

- the per-turn context channel (``MessageList.attach_turn_context``), which a translator renders only
  on a send whose newest message is NOT a tool result (the 2026-10-18 once-per-person-turn ruling);
- the tail channel (``MessageList.attach_tail_context``), which a translator renders only on a send
  whose newest message IS a tool result, after the conversation's last block.

Each channel renders in exactly the case the other does not, so the block reaches every send once.
The turn-context slot alone left it off every send right after a tool call — the send that follows
starting or stopping a helper (HL-PB-02 run 1, 2026-10-30: lead requests 49ad2f97 and 869bee96).
A send with no helpers clears both slots.

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
    channels = [
        attach
        for attach in (getattr(messages, "attach_turn_context", None), getattr(messages, "attach_tail_context", None))
        if attach is not None
    ]
    if not channels:
        return False

    def place(text: str) -> None:
        for attach in channels:
            attach(text, slot=HELPER_ROSTER_SLOT)

    source = _SOURCE
    if source is None or not conversation_id:
        place("")
        return False
    try:
        text = await source(str(conversation_id), organization_id)
    except Exception:
        # Neither channel ever carries a stale roster: cleared, then the failure goes to the caller.
        place("")
        raise
    place(text or "")
    return bool(text)


__all__ = [
    "HELPER_ROSTER_SLOT",
    "HelperRosterSource",
    "get_helper_roster_source",
    "set_helper_roster_source",
    "stage_helper_roster",
]
