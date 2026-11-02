"""Provider errors report useful details without credentials."""

from agentic_devtools.cli.speckit.progression_recovery import _error_reason


def test_error_reason_redacts_token():
    assert _error_reason(RuntimeError("workflow-token failed"), "workflow-token") == "RuntimeError: [redacted] failed"


def test_error_reason_without_token_and_truncation():
    assert _error_reason(ValueError("invalid"), "") == "ValueError: invalid"
    assert len(_error_reason(RuntimeError("x" * 1000), "")) == len("RuntimeError: ") + 500
