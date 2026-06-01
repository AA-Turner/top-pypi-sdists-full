"""
Demonstrates the smplkit runtime SDK for Smpl Flags.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/flags_runtime_showcase.py
"""

import asyncio

from smplkit import AsyncSmplClient, Context, Op, Rule

from setup.flags_runtime_setup import (
    setup_runtime_showcase,
    cleanup_runtime_showcase,
)

# ---------------------------------------------------------------------------
# Note: this showcase calls client.set_context(...) inline to demonstrate
# context-driven flag evaluation.  In a real app (Flask, Django, FastAPI,
# etc.), set_context is called once per request from middleware — not
# scattered through your handlers.
# ---------------------------------------------------------------------------

_alice = {
    "beta_tester": True,
    "email": "alice.adams@acme.com",
    "first_name": "Alice",
    "last_name": "Adams",
    "plan": "enterprise",
}

_bob = {
    "beta_tester": False,
    "email": "bob.jones@acme.com",
    "first_name": "Bob",
    "last_name": "Jones",
    "plan": "free",
}

_large_technology_account = {
    "employee_count": 500,
    "id": 1234,
    "industry": "technology",
    "region": "us",
}

_small_retail_account = {
    "employee_count": 10,
    "id": 5678,
    "industry": "retail",
    "region": "eu",
}


def _create_context(user: dict, account: dict) -> list[Context]:
    """Create context within which flags will be evaluated."""
    return [
        Context(
            "user",
            user["email"],
            beta_tester=user["beta_tester"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            plan=user["plan"],
        ),
        Context(
            "account",
            str(account["id"]),
            industry=account["industry"],
            region=account["region"],
            employee_count=account["employee_count"],
        ),
    ]


async def main() -> None:

    # create the client (use SmplClient for synchronous use)
    async with AsyncSmplClient(
        environment="production", service="showcase-service"
    ) as client:
        await setup_runtime_showcase(client.manage)
        await client.wait_until_ready()

        # declare flags - default values will be used if the flag does not
        # exist or smplkit is unreachable
        checkout_v2 = client.flags.boolean_flag("checkout-v2", default=False)
        banner_color = client.flags.string_flag("banner-color", default="red")
        max_retries = client.flags.number_flag("max-retries", default=3)

        all_changes: list[dict] = []
        banner_changes: list = []

        # global listener — fires when ANY flag definition changes
        @client.flags.on_change
        def on_any_change(event):
            all_changes.append({"id": event.id, "source": event.source})
            print(
                f"    Global flag listener: '{event.id}' "
                f"updated via {event.source}"
            )

        # flag listener — fires only when a specific flag changes
        @client.flags.on_change("banner-color")
        def on_banner_change(event):
            banner_changes.append(event)
            print("    banner-color flag changed!")

        # request 1 — Alice from a large tech account
        with client.set_context(
            _create_context(_alice, _large_technology_account)
        ):
            checkout_result = checkout_v2.get()
            print(f"checkout-v2 = {checkout_result}")
            assert checkout_result is True, (
                f"Expected True, got {checkout_result}"
            )
            assert isinstance(checkout_result, bool), (
                "Expected bool return type"
            )

            banner_result = banner_color.get()
            print(f"banner-color = {banner_result}")
            assert banner_result == "blue", (
                f"Expected 'blue', got {banner_result}"
            )
            assert isinstance(banner_result, str), "Expected str return type"

            retries_result = max_retries.get()
            print(f"max-retries = {retries_result}")
            assert retries_result == 5, f"Expected 5, got {retries_result}"

        # request 2 — Bob from a small retail account
        with client.set_context(_create_context(_bob, _small_retail_account)):
            checkout_result_2 = checkout_v2.get()
            print(f"checkout-v2 = {checkout_result_2}")
            assert checkout_result_2 is False

            banner_result_2 = banner_color.get()
            print(f"banner-color = {banner_result_2}")
            assert banner_result_2 == "red"

            retries_result_2 = max_retries.get()
            print(f"max-retries = {retries_result_2}")
            assert retries_result_2 == 3

            # nested scoped override — temporarily impersonate Alice without
            # disturbing the surrounding request's context.
            with client.set_context(
                _create_context(_alice, _large_technology_account)
            ):
                scoped_result = checkout_v2.get()
                print(f"checkout-v2 (scoped: Alice) = {scoped_result}")
                assert scoped_result is True

            # context auto-reverted to Bob/small retail here
            assert checkout_v2.get() is False

        # get a flag's value (explicitly pass context)
        explicit_result = checkout_v2.get(
            context=[
                Context(
                    "user",
                    "john.smith@acme.com",
                    plan="free",
                    beta_tester=False,
                ),
                Context("account", "1111", region="jp"),
            ]
        )
        print(f"checkout-v2 (free, JP) = {explicit_result}")
        assert explicit_result is False

        # simulate someone making changes to a flag to trigger listeners
        await _update_rules(client)

        # wait a moment for the event to be delivered (typical WS
        # round-trip is well under 200ms; 400ms is plenty of headroom
        # and anything past that is a real signal, not noise to absorb).
        await asyncio.sleep(0.4)

        # verify both listeners fired
        assert len(all_changes) >= 1, (
            f"Expected at least one global change, got {len(all_changes)}"
        )
        assert len(banner_changes) >= 1, (
            f"Expected at least one banner change, got {len(banner_changes)}"
        )

        await cleanup_runtime_showcase(client.manage)
        print("Done!")


async def _update_rules(client: AsyncSmplClient):
    current_banner = await client.manage.flags.get("banner-color")
    current_banner.add_rule(
        Rule("Red for small companies", environment="production")
        .when("account.employee_count", Op.LT, 50)
        .serve("red")
    )
    await current_banner.save()


if __name__ == "__main__":
    asyncio.run(main())
