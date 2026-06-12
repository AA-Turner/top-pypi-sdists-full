"""Demonstrates the smplkit runtime SDK for Smpl Config.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/config_runtime_showcase.py
"""

import asyncio

from pydantic import BaseModel, Field

from smplkit import AsyncSmplClient

from setup.config_runtime_setup import (
    cleanup_runtime_showcase,
    simulate_admin_override,
)

# Example Pydantic configuration classes to showcase how "code-first"
# configuration management works

class App(BaseModel):
    name: str = Field(default="Acme SaaS", description="Display name of the application.")


class Support(BaseModel):
    email: str = Field(default="support@acme.dev", description="Customer support contact.")


class Plan(BaseModel):
    max_seats: int = Field(default=5, description="Maximum seats per organization.")
    trial_days: int = Field(default=14, description="Trial length in days.")
    tier: str = Field(default="free", description="Plan tier identifier.")


class Common(BaseModel):
    """Shared defaults for showcase services."""

    app: App = Field(default_factory=App)
    support: Support = Field(default_factory=Support)


class Billing(BaseModel):
    """Plan-limit configuration for billing — inherits from Common."""

    app: App = Field(default_factory=App)
    support: Support = Field(default_factory=Support)
    plan: Plan = Field(default_factory=Plan)


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncSmplClient(environment="production") as client:
        await cleanup_runtime_showcase(client)

        # bind Pydantic models
        common = await client.config.bind("showcase-common", Common())
        billing = await client.config.bind(
            "showcase-billing",
            Billing(plan=Plan(max_seats=5, trial_days=14, tier="free")),
            parent=common,
        )
        print(f"common.app.name = {common.app.name}")
        print(f"billing.app.name = {billing.app.name}  # inherited from common")
        print(f"billing.plan.max_seats = {billing.plan.max_seats}")

        # add listeners if desired
        changes: list = []

        @client.config.on_change("showcase-billing", item_key="plan.max_seats")
        def on_max_seats(event):
            changes.append(event)
            print(
                f"    [CHANGE] {event.config_id}.{event.item_key}: "
                f"{event.old_value!r} -> {event.new_value!r}"
            )

        await client.wait_until_ready()

        # simulate someone making a change in smplkit console
        await simulate_admin_override(client)
        await asyncio.sleep(0.4)

        # observe changes are automatically reflected in bound models
        print(f"billing.plan.max_seats after override = {billing.plan.max_seats}")
        assert billing.plan.max_seats == 25, f"Expected 25, got {billing.plan.max_seats}"
        assert len(changes) >= 1

        # you can also bind plain-old dictionaries
        db = await client.config.bind(
            "showcase-database",
            {
                "primary": {
                    "host": "db.acme.example",
                    "port": 5432,
                },
                "pool_size": 10,
                "statement_timeout_ms": 30000,
            },
        )
        print(f"db['primary']['host'] = {db['primary']['host']}")
        print(f"db['pool_size'] = {db['pool_size']}")
        assert db["primary"]["host"] == "db.acme.example"
        assert db["pool_size"] == 10

        # or read live values via subscribe(id)
        common_view = client.config.subscribe("showcase-common")
        print("showcase-common (via get):")
        for k, v in common_view.items():
            print(f"    {k} = {v}")
        assert common_view["app.name"] == "Acme SaaS"

        # or skip the model/dict and just fetch specific keys directly
        slow_query_ms = await client.config.get_value(
            "showcase-database", "slow_query_threshold_ms", 500
        )
        print(
            f"showcase-database.slow_query_threshold_ms = {slow_query_ms}  "
            f"# default used (key absent)"
        )
        assert slow_query_ms == 500

        await cleanup_runtime_showcase(client)
        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
