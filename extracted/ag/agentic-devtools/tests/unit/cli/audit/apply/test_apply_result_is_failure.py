"""Tests for apply_result_is_failure()."""

from agentic_devtools.cli.audit.apply import (
    OUTCOME_INVALID_OUTPUT,
    OUTCOME_MISSING_OUTPUT,
    OUTCOME_NO_CHANGES,
    OUTCOME_OVERSIZED_INSTRUCTIONS,
    OUTCOME_PR_FAILED,
    OUTCOME_PR_READY,
    OUTCOME_READ_ERROR,
    apply_result_is_failure,
)


class TestApplyResultIsFailure:
    """Failure classification for apply outcomes."""

    def test_missing_output_is_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_MISSING_OUTPUT}) is True

    def test_invalid_output_is_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_INVALID_OUTPUT}) is True

    def test_pr_failed_is_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_PR_FAILED}) is True

    def test_oversized_instructions_is_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_OVERSIZED_INSTRUCTIONS}) is True

    def test_read_error_is_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_READ_ERROR}) is True

    def test_no_changes_is_not_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_NO_CHANGES}) is False

    def test_pr_ready_is_not_failure(self) -> None:
        assert apply_result_is_failure({"outcome": OUTCOME_PR_READY}) is False

    def test_missing_outcome_key_is_failure(self) -> None:
        # A result without an outcome key is itself an invalid/partial result and
        # must fail loudly rather than silently passing.
        assert apply_result_is_failure({"status": "applied"}) is True

    def test_unknown_outcome_is_failure(self) -> None:
        # An unrecognised outcome string fails loudly rather than silently passing.
        assert apply_result_is_failure({"outcome": "something-else"}) is True
