"""Tests for PolicyValidationError exception."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.exceptions import PolicyValidationError


class TestPolicyValidationError:
    """Test PolicyValidationError attributes and message formatting."""

    def test_attributes_stored(self) -> None:
        err = PolicyValidationError(
            field_path="pr_review.confidence_minimum",
            invalid_value=1.5,
            constraint="must be between 0.0 and 1.0",
        )
        assert err.field_path == "pr_review.confidence_minimum"
        assert err.invalid_value == 1.5
        assert err.constraint == "must be between 0.0 and 1.0"

    def test_message_contains_all_parts(self) -> None:
        err = PolicyValidationError(
            field_path="work_on_issue.retry_budget",
            invalid_value=-5,
            constraint="must be non-negative (>= 0)",
        )
        msg = str(err)
        assert "work_on_issue.retry_budget" in msg
        assert "-5" in msg
        assert "must be non-negative" in msg

    def test_is_exception(self) -> None:
        err = PolicyValidationError(field_path="x", invalid_value=None, constraint="c")
        assert isinstance(err, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(PolicyValidationError) as exc_info:
            raise PolicyValidationError(
                field_path="shared.max_tokens",
                invalid_value="not_a_number",
                constraint="must be a non-negative integer",
            )
        assert exc_info.value.field_path == "shared.max_tokens"
        assert exc_info.value.invalid_value == "not_a_number"
