"""Setup / cleanup helpers for ``flags_runtime_showcase.py``."""

from __future__ import annotations

from smplkit import (
    AsyncSmplManagementClient,
    FlagValue,
    Op,
    Rule,
    NotFoundError,
)

_DEMO_FLAG_IDS = ["checkout-v2", "banner-color", "max-retries"]


async def setup_runtime_showcase(manage: AsyncSmplManagementClient) -> None:
    await cleanup_runtime_showcase(manage)

    checkout = manage.flags.new_boolean_flag(
        "checkout-v2",
        default=False,
        description="Controls rollout of the new checkout experience.",
    )
    checkout.enable_rules(environment="production")
    checkout.add_rule(
        Rule("Enable for enterprise users in US region", environment="production")
        .when("user.plan", Op.EQ, "enterprise")
        .when("account.region", Op.EQ, "us")
        .serve(True)
    )
    checkout.add_rule(
        Rule("Enable for beta testers", environment="production")
        .when("user.beta_tester", Op.EQ, True)
        .serve(True)
    )
    await checkout.save()

    banner = manage.flags.new_string_flag(
        "banner-color",
        default="red",
        name="Banner Color",
        description="Controls the banner color shown to users.",
        values=[
            FlagValue(name="Red", value="red"),
            FlagValue(name="Green", value="green"),
            FlagValue(name="Blue", value="blue"),
        ],
    )
    banner.enable_rules(environment="production")
    banner.add_rule(
        Rule("Blue for enterprise users", environment="production")
        .when("user.plan", Op.EQ, "enterprise")
        .serve("blue")
    )
    banner.add_rule(
        Rule("Green for technology companies", environment="production")
        .when("account.industry", Op.EQ, "technology")
        .serve("green")
    )
    await banner.save()

    retries = manage.flags.new_number_flag(
        "max-retries",
        default=3,
        description="Maximum number of API retries before failing.",
    )
    retries.enable_rules(environment="production")
    retries.add_rule(
        Rule("High retries for large accounts", environment="production")
        .when("account.employee_count", Op.GT, 100)
        .serve(5)
    )
    await retries.save()


async def cleanup_runtime_showcase(manage: AsyncSmplManagementClient) -> None:
    for flag_id in _DEMO_FLAG_IDS:
        try:
            await manage.flags.delete(flag_id)
        except NotFoundError:
            pass
