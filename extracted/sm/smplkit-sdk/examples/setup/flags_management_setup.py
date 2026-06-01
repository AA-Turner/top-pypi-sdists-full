"""Setup / cleanup helpers for ``flags_management_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplManagementClient, NotFoundError

_DEMO_FLAG_IDS = ["checkout-v2", "banner-color", "max-retries", "ui-theme"]


async def setup_management_showcase(manage: AsyncSmplManagementClient) -> None:
    await cleanup_management_showcase(manage)


async def cleanup_management_showcase(
    manage: AsyncSmplManagementClient,
) -> None:
    for flag_id in _DEMO_FLAG_IDS:
        try:
            await manage.flags.delete(flag_id)
        except NotFoundError:
            pass
