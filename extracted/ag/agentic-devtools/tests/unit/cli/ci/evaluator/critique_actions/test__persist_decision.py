"""Tests for persisting critique adjudication decisions."""

from typing import Literal
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import CritiqueAdjudication
from agentic_devtools.cli.ci.evaluator.critique_actions import _persist_decision
from tests.unit.cli.ci.evaluator.critique_actions._support import _make_provider, _make_snapshot


@pytest.mark.parametrize(
    ("verdict", "guard"),
    [
        ("rebutted", Mock(return_value=False)),
        ("needs_human", Mock(side_effect=[True, False])),
    ],
)
def test_lock_loss_prevents_unowned_persistence_mutations(
    verdict: Literal["rebutted", "needs_human"], guard: Mock
) -> None:
    provider = _make_provider("head")
    decision = CritiqueAdjudication(verdict=verdict, rationale="The critique is addressed.")

    result = _persist_decision(provider, _make_snapshot(), "head", 100, 1, 1, decision, guard)

    assert result.success is False
    if verdict == "rebutted":
        provider.post_comment_as_pr_token.assert_not_called()
    else:
        provider.post_comment_as_pr_token.assert_called_once()
        provider.add_label.assert_not_called()
