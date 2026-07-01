"""Tests for testmu_selenium._route_failure.route_failure.

Covers the three-condition contract:
  - "Warn but continue executing"   -> log WARNING, swallow, return None
  - "Fail but continue executing"   -> log ERROR, swallow, return None
  - "Fail test immediately" / "" / None / unknown  -> raise RuntimeError

Also covers the defensive enum-like .value unwrapping.
"""
import logging

import pytest

from testmu_selenium._route_failure import route_failure


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _FakeCondition:
    """Mimics an enum-like object with a .value attribute."""
    def __init__(self, value):
        self.value = value


# ---------------------------------------------------------------------------
# Fail-closed cases (should raise RuntimeError)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("condition", [
    "Fail test immediately",
    "",
    None,
    "some unknown value",
    "FAIL TEST IMMEDIATELY",   # wrong capitalisation → unknown → fail closed
])
def test_raises_runtime_error_for_fail_closed_conditions(condition):
    exc = ValueError("boom")
    label = "click login"
    with pytest.raises(RuntimeError) as exc_info:
        route_failure(condition, exc, label)
    msg = str(exc_info.value)
    assert label in msg, f"expected label {label!r} in RuntimeError message, got: {msg!r}"
    assert "boom" in msg, f"expected original exc text in RuntimeError message, got: {msg!r}"


def test_raises_runtime_error_message_contains_label_and_exc():
    """Explicit check: RuntimeError message must contain both label and exc str."""
    exc = ValueError("something went wrong")
    label = "submit form"
    with pytest.raises(RuntimeError) as exc_info:
        route_failure("Fail test immediately", exc, label)
    msg = str(exc_info.value)
    assert "submit form" in msg
    assert "something went wrong" in msg


# ---------------------------------------------------------------------------
# Warn-but-continue
# ---------------------------------------------------------------------------

def test_warn_continue_does_not_raise(caplog):
    exc = ValueError("boom")
    label = "click login"
    with caplog.at_level(logging.WARNING, logger="testmu_selenium._route_failure"):
        result = route_failure("Warn but continue executing", exc, label)
    assert result is None


def test_warn_continue_logs_warning(caplog):
    exc = ValueError("boom")
    label = "click login"
    with caplog.at_level(logging.WARNING, logger="testmu_selenium._route_failure"):
        route_failure("Warn but continue executing", exc, label)
    warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert warning_records, "expected at least one WARNING log record"
    combined = " ".join(r.getMessage() for r in warning_records)
    assert label in combined, f"expected label {label!r} in WARNING log, got: {combined!r}"
    assert "boom" in combined, f"expected exc text in WARNING log, got: {combined!r}"


# ---------------------------------------------------------------------------
# Fail-but-continue
# ---------------------------------------------------------------------------

def test_fail_continue_does_not_raise(caplog):
    exc = ValueError("boom")
    label = "click login"
    with caplog.at_level(logging.ERROR, logger="testmu_selenium._route_failure"):
        result = route_failure("Fail but continue executing", exc, label)
    assert result is None


def test_fail_continue_logs_error(caplog):
    exc = ValueError("boom")
    label = "click login"
    with caplog.at_level(logging.ERROR, logger="testmu_selenium._route_failure"):
        route_failure("Fail but continue executing", exc, label)
    error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
    assert error_records, "expected at least one ERROR log record"
    combined = " ".join(r.getMessage() for r in error_records)
    assert label in combined, f"expected label {label!r} in ERROR log, got: {combined!r}"
    assert "boom" in combined, f"expected exc text in ERROR log, got: {combined!r}"


# ---------------------------------------------------------------------------
# Enum-like .value unwrapping
# ---------------------------------------------------------------------------

def test_enum_value_warn_continue_does_not_raise(caplog):
    """condition with .value == 'Warn but continue executing' should swallow."""
    cond = _FakeCondition("Warn but continue executing")
    exc = ValueError("boom")
    with caplog.at_level(logging.WARNING, logger="testmu_selenium._route_failure"):
        result = route_failure(cond, exc, "enum step")
    assert result is None


def test_enum_value_fail_immediately_raises():
    """condition with .value == 'Fail test immediately' should raise."""
    cond = _FakeCondition("Fail test immediately")
    exc = ValueError("boom")
    with pytest.raises(RuntimeError):
        route_failure(cond, exc, "enum step")


# ---------------------------------------------------------------------------
# Pending-failure accumulator
#
# Without an accumulator, "Fail but continue executing" was indistinguishable
# from "Warn but continue" at end-of-run — fn(driver) returned cleanly and
# run() reported the LT session as passed. A regression repro confirmed that
# a Fail-but-continue step was swallowed silently, the generated test exited 0,
# and HE marked the build passed.
# ---------------------------------------------------------------------------

from testmu_selenium._route_failure import (  # noqa: E402
    _has_pending_failures,
    _pending_failures_summary,
    _reset_pending_failures,
)


@pytest.fixture(autouse=True)
def _reset_pending_failures_between_tests():
    _reset_pending_failures()
    yield
    _reset_pending_failures()


def test_fail_continue_appends_to_pending_failures():
    assert not _has_pending_failures()
    route_failure("Fail but continue executing", ValueError("boom"), "click login")
    assert _has_pending_failures()
    summary = _pending_failures_summary()
    assert "click login" in summary
    assert "boom" in summary


def test_warn_continue_does_not_append_to_pending_failures(caplog):
    with caplog.at_level(logging.WARNING, logger="testmu_selenium._route_failure"):
        route_failure("Warn but continue executing", ValueError("warn"), "label")
    assert not _has_pending_failures(), (
        "Warn-but-continue must not contribute to the pending-failure list — "
        "it is the silent variant by design."
    )


def test_fail_immediately_does_not_append_to_pending_failures():
    """Fail-immediately raises before reaching the accumulator path."""
    with pytest.raises(RuntimeError):
        route_failure("Fail test immediately", ValueError("boom"), "label")
    assert not _has_pending_failures()


def test_multiple_fail_continue_calls_accumulate():
    route_failure("Fail but continue executing", ValueError("first"), "step A")
    route_failure("Fail but continue executing", ValueError("second"), "step B")
    summary = _pending_failures_summary()
    assert "step A" in summary and "step B" in summary
    assert "first" in summary and "second" in summary


def test_reset_pending_failures_clears_accumulator():
    route_failure("Fail but continue executing", ValueError("boom"), "label")
    assert _has_pending_failures()
    _reset_pending_failures()
    assert not _has_pending_failures()


def test_enum_value_fail_continue_appends_to_pending_failures():
    """Enum-like .value unwrap path also feeds the accumulator."""
    cond = _FakeCondition("Fail but continue executing")
    route_failure(cond, ValueError("boom"), "enum step")
    assert _has_pending_failures()
    assert "enum step" in _pending_failures_summary()
