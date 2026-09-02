"""Tests for PolicyConfig frozen dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.config import (
    PolicyConfig,
    PRReviewPolicy,
    SharedBudgetPolicy,
    WorkOnIssuePolicy,
)


class TestPolicyConfig:
    """Test PolicyConfig immutability and nested sections."""

    def test_default_construction(self) -> None:
        config = PolicyConfig()
        assert isinstance(config.pr_review, PRReviewPolicy)
        assert isinstance(config.work_on_issue, WorkOnIssuePolicy)
        assert isinstance(config.shared, SharedBudgetPolicy)

    def test_frozen_immutability(self) -> None:
        config = PolicyConfig()
        with pytest.raises(Exception):
            config.pr_review = PRReviewPolicy(max_high_severity=5)  # type: ignore[misc]

    def test_custom_nested_values(self) -> None:
        config = PolicyConfig(
            pr_review=PRReviewPolicy(max_high_severity=2),
            work_on_issue=WorkOnIssuePolicy(retry_budget=5),
            shared=SharedBudgetPolicy(max_tokens=1000000),
        )
        assert config.pr_review.max_high_severity == 2
        assert config.work_on_issue.retry_budget == 5
        assert config.shared.max_tokens == 1000000
