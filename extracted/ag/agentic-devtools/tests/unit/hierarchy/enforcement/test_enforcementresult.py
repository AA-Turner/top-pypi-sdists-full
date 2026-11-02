"""Tests for EnforcementResult.allowed property."""

from __future__ import annotations

from agentic_devtools.hierarchy.enforcement import EnforcementAction, EnforcementResult


class TestEnforcementResult:
    """Cover the allowed property on EnforcementResult."""

    def test_allowed_true_when_action_allow(self):
        result = EnforcementResult(
            action=EnforcementAction.ALLOW,
            reason="test",
        )
        assert result.allowed is True

    def test_allowed_false_when_action_reject(self):
        result = EnforcementResult(
            action=EnforcementAction.REJECT,
            reason="test",
        )
        assert result.allowed is False
