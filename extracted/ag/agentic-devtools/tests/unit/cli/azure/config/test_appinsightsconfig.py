"""Tests for AppInsightsConfig."""

from agentic_devtools.cli.azure.config import AppInsightsConfig


def test_resource_id_uses_subscription_group_and_component():
    config = AppInsightsConfig(
        name="appi-test",
        resource_group="rg-test",
        subscription="test-subscription",
        subscription_id="subscription-id",
        environment="DEV",
    )

    assert (
        config.resource_id == "/subscriptions/subscription-id/resourceGroups/rg-test/providers/"
        "Microsoft.Insights/components/appi-test"
    )
