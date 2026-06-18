"""
Demonstrates the smplkit management SDK for Smpl Logging.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/logging_management_showcase.py
"""

import asyncio

from smplkit import AsyncSmplClient, LogLevel

from setup.logging_management_setup import (
    cleanup_management_showcase,
    setup_management_showcase,
)


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncSmplClient() as client:
        await setup_management_showcase(client)
        try:
            # create a parent logger with a default level
            root = client.logging.loggers.new("showcase")
            root.set_level(LogLevel.INFO)
            await root.save()
            print(f"Created: {root.id} (level={root.level})")
            assert root.level == LogLevel.INFO

            # child logger with no level (inherits from parent)
            db = client.logging.loggers.new("showcase.db")
            await db.save()
            print(f"Created: {db.id} (inherits)")
            assert db.level is None

            # child logger with explicit level (overrides parent)
            payments = client.logging.loggers.new("showcase.payments")
            payments.set_level(LogLevel.WARN)
            await payments.save()
            print(f"Created: {payments.id} (level={payments.level})")
            assert payments.level == LogLevel.WARN

            # override log level for the production environment
            root.set_level(LogLevel.ERROR, environment="production")
            await root.save()
            print(f"Set environment overrides: {root.environments}")
            assert root.environments["production"].level == LogLevel.ERROR

            # clear environment override (inherits from the default level again)
            root.clear_level(environment="production")
            await root.save()
            print(f"Cleared production override: {root.environments}")
            assert "production" not in root.environments

            # get a logger
            fetched = await client.logging.loggers.get("showcase")
            assert fetched.level == LogLevel.INFO
            print("Done!")
        finally:
            await cleanup_management_showcase(client)


if __name__ == "__main__":
    asyncio.run(main())
