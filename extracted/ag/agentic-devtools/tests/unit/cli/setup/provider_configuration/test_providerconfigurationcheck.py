"""Unit tests for ProviderConfigurationCheck."""

from pathlib import Path

from agentic_devtools.cli.setup.provider_configuration import check_provider_configuration


def test_providerconfigurationcheck_report_details_for_missing_file(tmp_path: Path) -> None:
    result = check_provider_configuration(tmp_path)

    details = result.report_details()

    assert details["status"] == "failed"
    assert details["source"] == "none"
