"""Unit tests for _credential_status_for_reason."""

import pytest

from agentic_devtools.cli.setup import provider_configuration


@pytest.mark.parametrize(
    ("provider_type", "reason", "default", "expected"),
    [
        ("copilot", "credential_missing", "unknown", "not_required"),
        ("custom", "credential_missing", "unknown", "missing"),
        ("custom", "credential_reference_missing", "unknown", "missing"),
        ("custom", "configuration_invalid", "unknown", "unknown"),
        (None, None, "not_checked", "not_checked"),
    ],
)
def test__credential_status_for_reason(
    provider_type: str | None,
    reason: str | None,
    default: str,
    expected: str,
) -> None:
    assert (
        provider_configuration._credential_status_for_reason(
            provider_type,
            reason,
            default=default,
        )
        == expected
    )
