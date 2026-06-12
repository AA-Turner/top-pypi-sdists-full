"""Setup / cleanup helpers for ``flags_management_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplClient, NotFoundError

_DEMO_FLAG_IDS = ["checkout-v2", "banner-color", "max-retries", "ui-theme"]


async def setup_management_showcase(client: AsyncSmplClient) -> None:
    await cleanup_management_showcase(client)


async def cleanup_management_showcase(
    client: AsyncSmplClient,
) -> None:
    for flag_id in _DEMO_FLAG_IDS:
        try:
            await client.flags.delete(flag_id)
        except NotFoundError:
            pass
