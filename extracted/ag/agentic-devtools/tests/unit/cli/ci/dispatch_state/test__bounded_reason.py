import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_returns_none_for_missing_reason() -> None:
    assert dispatch_state_module._bounded_reason(None) is None


def test_redacts_and_truncates_reason() -> None:
    bounded = dispatch_state_module._bounded_reason(
        "Authorization: Basic dXNlcjpwYXNz " + ("x" * 600),
    )

    assert bounded is not None
    assert bounded.startswith("[REDACTED]")
    assert len(bounded) == 512


def test_rejects_non_string_reason() -> None:
    with pytest.raises(ValueError, match="reason must be a string"):
        dispatch_state_module._bounded_reason(123)  # type: ignore[arg-type]
