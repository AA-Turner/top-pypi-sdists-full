"""Setup / cleanup helpers for ``logging_management_showcase.py``."""

from __future__ import annotations

from smplkit import AsyncSmplClient, NotFoundError

_DEMO_LOGGER_IDS = [
    "showcase",
    "showcase.db",
    "showcase.payments",
]


async def setup_management_showcase(client: AsyncSmplClient) -> None:
    await cleanup_management_showcase(client)


async def cleanup_management_showcase(
    client: AsyncSmplClient,
) -> None:
    for logger_id in _DEMO_LOGGER_IDS:
        try:
            await client.logging.loggers.delete(logger_id)
        except NotFoundError:
            pass
