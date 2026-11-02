"""Unit tests for ProviderConfigurationPlan."""

from agentic_devtools.cli.setup.provider_configuration import plan_provider_configuration


def test_providerconfigurationplan_report_details_for_skipped_plan() -> None:
    plan = plan_provider_configuration(None)

    details = plan.report_details()

    assert details["status"] == "skipped"
    assert details["reason"] == "no_git_root"
