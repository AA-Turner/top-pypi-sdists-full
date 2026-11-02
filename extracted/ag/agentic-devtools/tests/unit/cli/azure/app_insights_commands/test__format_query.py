"""Tests for _format_query."""

from agentic_devtools.cli.azure.app_insights_commands import _format_query


def test_formats_query_template_with_combined_filter_and_limit():
    result = _format_query(
        "union traces\n{combined_filter}\n| take {limit}",
        timespan="4h",
        limit=25,
        dataproduct_id="dp-42",
        workbench="STND",
        include_mgmt=False,
    )

    assert "timestamp > ago(4h)" in result
    assert "cloud_RoleName has 'stndfabric'" in result
    assert "message contains 'dp-42'" in result
    assert "| take 25" in result
