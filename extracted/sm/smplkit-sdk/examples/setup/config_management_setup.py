"""Setup / cleanup helpers for ``config_management_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplClient, NotFoundError

_DEMO_CONFIG_IDS = ["showcase-user-service", "showcase-common"]


async def setup_management_showcase(client: AsyncSmplClient) -> None:
    await cleanup_management_showcase(client)


async def cleanup_management_showcase(client: AsyncSmplClient) -> None:
    for config_id in _DEMO_CONFIG_IDS:
        try:
            await client.config.delete(config_id)
        except NotFoundError:
            pass
