"""Setup / cleanup helpers for ``logging_management_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplManagementClient, NotFoundError

_DEMO_LOGGER_IDS = [
    "showcase",
    "showcase.db",
    "showcase.payments",
]


async def setup_management_showcase(manage: AsyncSmplManagementClient) -> None:
    await cleanup_management_showcase(manage)


async def cleanup_management_showcase(
    manage: AsyncSmplManagementClient,
) -> None:
    for logger_id in _DEMO_LOGGER_IDS:
        try:
            await manage.loggers.delete(logger_id)
        except NotFoundError:
            pass
