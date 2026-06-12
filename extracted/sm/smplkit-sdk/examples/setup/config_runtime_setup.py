"""Setup and simulation helpers for ``config_runtime_showcase.py``.
"""

from __future__ import annotations

from smplkit import AsyncSmplClient, NotFoundError

_DEMO_CONFIG_IDS = [
    "showcase-billing",
    "showcase-common",
    "showcase-database",
]


async def simulate_admin_override(client: AsyncSmplClient) -> None:
    await client.config.flush()
    billing = await client.config.get("showcase-billing")
    billing.set_number("plan.max_seats", 25, environment="production")
    await billing.save()


async def cleanup_runtime_showcase(client: AsyncSmplClient) -> None:
    for config_id in _DEMO_CONFIG_IDS:
        try:
            await client.config.delete(config_id)
        except NotFoundError:
            pass
