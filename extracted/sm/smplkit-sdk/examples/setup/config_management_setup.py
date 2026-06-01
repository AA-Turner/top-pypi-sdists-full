"""Setup / cleanup helpers for ``config_management_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplManagementClient, NotFoundError

_DEMO_CONFIG_IDS = ["showcase-user-service", "showcase-common"]


async def setup_management_showcase(manage: AsyncSmplManagementClient) -> None:
    await cleanup_management_showcase(manage)


async def cleanup_management_showcase(
    manage: AsyncSmplManagementClient,
) -> None:
    for config_id in _DEMO_CONFIG_IDS:
        try:
            await manage.config.delete(config_id)
        except NotFoundError:
            pass
