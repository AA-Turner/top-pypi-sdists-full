"""Setup and simulation helpers for ``config_runtime_showcase.py``.
"""

from __future__ import annotations

from smplkit._errors import NotFoundError
from smplkit.management.client import AsyncSmplManagementClient

_DEMO_CONFIG_IDS = [
    "showcase-billing",
    "showcase-common",
    "showcase-database",
]


async def simulate_admin_override(manage: AsyncSmplManagementClient) -> None:
    # Real customers never read back through the management API immediately
    # after binding via the runtime client — this is a simulation-only step.
    # Push pending runtime-side registrations through so the lookup below
    # can find the freshly-declared config.
    await manage.config.flush()
    billing = await manage.config.get("showcase-billing")
    billing.set_number("plan.max_seats", 25, environment="production")
    await billing.save()


async def cleanup_runtime_showcase(manage: AsyncSmplManagementClient) -> None:
    for config_id in _DEMO_CONFIG_IDS:
        try:
            await manage.config.delete(config_id)
        except NotFoundError:
            pass
