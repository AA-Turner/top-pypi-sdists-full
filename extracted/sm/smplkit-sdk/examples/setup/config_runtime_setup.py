"""Setup and simulation helpers for ``config_runtime_showcase.py``.
"""

from __future__ import annotations

from smplkit import AsyncSmplClient, NotFoundError

# Complete, dependency-ordered list of every config the config showcases
# create. Children are listed before the shared ``showcase-common`` parent so
# cleanup never trips the "config referenced as parent" conflict — even when a
# prior run crashed mid-way and left a sibling showcase's child orphaned.
_DEMO_CONFIG_IDS = [
    "showcase-billing",        # child of showcase-common (runtime showcase)
    "showcase-user-service",   # child of showcase-common (management showcase)
    "showcase-database",       # root (runtime showcase)
    "showcase-common",         # shared parent — must be deleted last
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
