"""Tests for existing critique adjudication results."""

from unittest.mock import Mock

from agentic_devtools.cli.ci.evaluator.critique_actions import _existing_result
from tests.unit.cli.ci.evaluator.critique_actions._support import _make_snapshot


def test_lock_loss_prevents_restoring_needs_human_label() -> None:
    provider = Mock()

    result = _existing_result(
        provider,
        _make_snapshot(),
        1,
        existing_needs_human=True,
        dry_run=False,
        ownership_guard=Mock(return_value=False),
    )

    assert result.success is False
    provider.add_label.assert_not_called()
