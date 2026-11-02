"""Tests for _build_combined_filter."""

from agentic_devtools.cli.azure.app_insights_commands import _build_combined_filter


def test_builds_known_workbench_filter_with_management_and_dataproduct():
    result = _build_combined_filter("2h", "dp-42", "stnd", include_mgmt=True)

    assert "timestamp > ago(2h)" in result
    assert "cloud_RoleName has 'stndfabric'" in result
    assert "app-restapi-mgmt-dev-chn-1" in result
    assert "message contains 'dp-42'" in result
    assert "tostring(customDimensions) contains 'dp-42'" in result


def test_builds_fallback_workbench_filter_without_management():
    result = _build_combined_filter("30m", workbench="custom", include_mgmt=False)

    assert "cloud_RoleName has 'customfabric'" in result
    assert "app-restapi-mgmt-dev-chn-1" not in result


def test_builds_default_fabric_filter_without_optional_dataproduct():
    result = _build_combined_filter("1h")

    assert "cloud_RoleName contains 'fabric'" in result
    assert "message contains" not in result
