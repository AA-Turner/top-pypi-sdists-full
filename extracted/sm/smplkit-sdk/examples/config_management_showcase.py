"""
Demonstrates the smplkit management SDK for Smpl Config.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/config_management_showcase.py
"""

import asyncio

from smplkit import AsyncSmplClient

from setup.config_management_setup import (
    cleanup_management_showcase,
    setup_management_showcase,
)


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncSmplClient() as client:
        # Start-of-run cleanup removes any residue from a prior run. The
        # matching cleanup in the ``finally`` below guarantees we also tear
        # down our resources even if an error occurs mid-showcase, so a failed
        # run never leaves orphaned configs for the next run.
        await setup_management_showcase(client)
        try:
            # create a "parent" configuration that all other configs inherit from
            shared = client.config.new(
                "showcase-common",
                name="Showcase Common",
                description="Showcase-only shared configuration.",
            )
            shared.set_string("app_name", "Acme SaaS Platform")
            shared.set_string("support_email", "support@acme.dev")
            shared.set_number("max_retries", 3)
            shared.set_number("request_timeout_ms", 5000)
            shared.set_number("pagination_default_page_size", 25)
            shared.set_number("max_retries", 5, environment="production")
            shared.set_number(
                "request_timeout_ms", 10000, environment="production"
            )
            await shared.save()
            print(f"Created config: {shared.id}")

            # create a config (inherits from showcase-common)
            user_service = client.config.new(
                "showcase-user-service",
                name="Showcase User Service",
                description="Configuration for the user microservice.",
                parent=shared,
            )
            user_service.set_string("database.host", "localhost")
            user_service.set_number("database.port", 5432)
            user_service.set_string("database.name", "users_dev")
            user_service.set_number("database.pool_size", 5)
            user_service.set_number("cache_ttl_seconds", 300)
            user_service.set_boolean("enable_signup", True)
            user_service.set_number("pagination_default_page_size", 50)
            await user_service.save()

            # update a config
            user_service.set_string(
                "database.host",
                "prod-users-rds.internal.acme.dev",
                environment="production",
            )
            user_service.set_string(
                "database.name", "users_prod", environment="production"
            )
            user_service.set_number(
                "database.pool_size", 20, environment="production"
            )
            user_service.set_number(
                "cache_ttl_seconds", 600, environment="production"
            )
            user_service.set_boolean(
                "enable_signup", False, environment="production"
            )
            await user_service.save()
            print(f"Updated config: {user_service.id}")

            # list configs
            configs = await client.config.list()
            for cfg in configs:
                parent_info = (
                    f" (parent: {cfg.parent})" if cfg.parent else " (root)"
                )
                print(f"  {cfg.id}{parent_info}")

            # get a config
            fetched = await client.config.get("showcase-user-service")
            print(f"Fetched: id={fetched.id}, name={fetched.name}")
            print(f"  description={fetched.description}")
            print(f"  parent={fetched.parent or '(none)'}")
            print(f"  items: {list(fetched.items.keys())}")

            # delete configs
            await user_service.delete()
            await shared.delete()
            print("Deleted configs")

            print("Done!")
        finally:
            await cleanup_management_showcase(client)


if __name__ == "__main__":
    asyncio.run(main())
