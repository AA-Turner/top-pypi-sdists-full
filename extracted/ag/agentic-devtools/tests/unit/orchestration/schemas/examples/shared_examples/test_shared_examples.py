"""Tests for shared domain example factories."""

from agentic_devtools.orchestration.schemas.examples import (
    make_confidence_score,
    make_escalation_reason,
    make_stop_condition,
)
from agentic_devtools.orchestration.schemas.shared import (
    EscalationReason,
    StopCondition,
)


class TestSharedExamples:
    """Tests for shared domain example factories."""

    def test_make_escalation_reason_returns_valid(self):
        result = make_escalation_reason()
        assert isinstance(result, EscalationReason)
        assert result.description != ""

    def test_make_stop_condition_returns_valid(self):
        result = make_stop_condition()
        assert isinstance(result, StopCondition)
        assert result.reason != ""

    def test_make_confidence_score_returns_valid(self):
        score = make_confidence_score()
        assert 0.0 <= score <= 1.0

    def test_factories_return_new_instances(self):
        a = make_escalation_reason()
        b = make_escalation_reason()
        assert a is not b

    def test_kwargs_override(self):
        result = make_escalation_reason(description="Custom reason")
        assert result.description == "Custom reason"
