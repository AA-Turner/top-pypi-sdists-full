"""Setup / cleanup helpers for ``audit_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplClient, NotFoundError

# The forwarder the audit showcase creates. (Recorded events are an immutable
# audit trail and are intentionally not torn down.) Start-of-run cleanup clears
# residue from a prior run; the matching ``finally`` cleanup tears the forwarder
# down even when the showcase fails mid-way.
_DEMO_FORWARDER_IDS = ["showcase-forwarder"]


async def setup_showcase(client: AsyncSmplClient) -> None:
    await cleanup_showcase(client)


async def cleanup_showcase(client: AsyncSmplClient) -> None:
    for forwarder_id in _DEMO_FORWARDER_IDS:
        try:
            await client.audit.forwarders.delete(forwarder_id)
        except NotFoundError:
            pass
