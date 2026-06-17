"""Setup / cleanup helpers for ``config_management_showcase.py``."""

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


async def setup_management_showcase(client: AsyncSmplClient) -> None:
    await cleanup_management_showcase(client)


async def cleanup_management_showcase(client: AsyncSmplClient) -> None:
    for config_id in _DEMO_CONFIG_IDS:
        try:
            await client.config.delete(config_id)
        except NotFoundError:
            pass
