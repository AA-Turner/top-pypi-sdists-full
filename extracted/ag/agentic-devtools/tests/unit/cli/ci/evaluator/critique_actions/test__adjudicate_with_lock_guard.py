"""Tests for lock-guarded critique adjudication."""

from unittest.mock import Mock, patch

from agentic_devtools.cli.ci.evaluator.critique_actions import _adjudicate_with_lock_guard
from agentic_devtools.cli.ci.evaluator.models import EvaluationResult
from tests.unit.cli.ci.evaluator.critique_actions._support import _make_snapshot


def test_lock_loss_before_adjudication_skips_ai_call() -> None:
    with patch("agentic_devtools.cli.ci.evaluator.critique_actions._adjudicate_snapshot") as adjudicate_snapshot:
        result = _adjudicate_with_lock_guard(_make_snapshot(), "head", 100, 1, 1, Mock(return_value=False))

    assert isinstance(result, EvaluationResult)
    assert result.success is False
    adjudicate_snapshot.assert_not_called()
