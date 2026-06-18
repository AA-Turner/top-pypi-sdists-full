"""
Demonstrates the smplkit management SDK for Smpl Flags.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/flags_management_showcase.py
"""

import asyncio

from smplkit import AsyncSmplClient, FlagValue, Op, Rule

from setup.flags_management_setup import (
    cleanup_management_showcase,
    setup_management_showcase,
)


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncSmplClient() as client:
        await setup_management_showcase(client)
        try:
            # create a boolean flag
            checkout_flag = client.flags.new_boolean_flag(
                "checkout-v2",
                default=False,
                description="Controls rollout of the new checkout experience.",
            )
            await checkout_flag.save()
            print(f"Created flag: {checkout_flag.id}")

            # create a string flag (constrained)
            banner_flag = client.flags.new_string_flag(
                "banner-color",
                default="red",
                description="Controls the banner color shown to users.",
                name="Banner Color",
                values=[
                    FlagValue(name="Red", value="red"),
                    FlagValue(name="Green", value="green"),
                    FlagValue(name="Blue", value="blue"),
                ],
            )
            await banner_flag.save()
            print(f"Created flag: {banner_flag.id}")

            # create a numeric flag (unconstrained)
            retry_flag = client.flags.new_number_flag(
                "max-retries",
                default=3,
                description="Maximum number of API retries before failing.",
            )
            await retry_flag.save()
            print(f"Created flag: {retry_flag.id}")

            # create a JSON flag (constrained)
            theme_flag = client.flags.new_json_flag(
                "ui-theme",
                default={"mode": "light", "accent": "#0066cc"},
                description="Controls the UI theme configuration.",
                values=[
                    FlagValue(
                        name="Light",
                        value={"mode": "light", "accent": "#0066cc"},
                    ),
                    FlagValue(
                        name="Dark",
                        value={"mode": "dark", "accent": "#66ccff"},
                    ),
                    FlagValue(
                        name="High Contrast",
                        value={"mode": "dark", "accent": "#ffffff"},
                    ),
                ],
            )
            await theme_flag.save()
            print(f"Created flag: {theme_flag.id}")

            # checkout_flag (serve true in production to enterprise US users)
            checkout_flag.enable_rules(environment="production")
            checkout_flag.add_rule(
                Rule(
                    "Enable for enterprise users in US region",
                    environment="production",
                )
                .when("user.plan", Op.EQ, "enterprise")
                .when("account.region", Op.EQ, "us")
                .serve(True)
            )

            # checkout_flag (serve true in production for beta testers)
            checkout_flag.add_rule(
                Rule("Enable for beta testers", environment="production")
                .when("user.beta_tester", Op.EQ, True)
                .serve(True)
            )

            await checkout_flag.save()
            print(f"Updated flag: {checkout_flag.id}")

            # list flags
            flags = await client.flags.list()
            print(f"Total flags: {len(flags)}")
            for f in flags:
                envs = list(f.environments.keys()) if f.environments else []
                print(
                    f"  {f.id} ({f.type}) — default={f.default}, "
                    f"environments={envs}"
                )

            # get a flag
            fetched = await client.flags.get("checkout-v2")
            print(f"\nFetched by id: {fetched.id}")
            prod_rules = len(fetched.environments["production"].rules)
            prod_enabled = fetched.environments["production"].enabled
            print(f"  production rules: {prod_rules}")
            print(f"  production enabled: {prod_enabled}")

            # update a flag
            banner_flag.add_value("Purple", "purple")
            banner_flag.default = "blue"
            banner_flag.description = "Controls the banner color — updated"
            banner_flag.add_rule(
                Rule("Purple for enterprise users", environment="production")
                .when("user.plan", Op.EQ, "enterprise")
                .serve("purple")
            )
            await banner_flag.save()
            print(f"Updated flag: {banner_flag.id}'")

            # delete all the rules of a flag
            checkout_flag.clear_rules(environment="production")
            await checkout_flag.save()
            print(f"Updated flag: {checkout_flag.id}'")

            # clear values (flag becomes unconstrained)
            banner_flag.clear_values()
            await banner_flag.save()
            print(f"Updated flag: {banner_flag.id}'")

            # delete flags
            await client.flags.delete("checkout-v2")
            await banner_flag.delete()
            print("Deleted flags")

            print("Done!")
        finally:
            await cleanup_management_showcase(client)


if __name__ == "__main__":
    asyncio.run(main())
