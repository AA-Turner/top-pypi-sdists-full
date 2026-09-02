"""Tests for ``_build_execution_order`` (T038)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.jira.creation_pipeline import (
    PipelineValidationError,
    _build_execution_order,
)
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode

from .conftest import make_context, make_tree


class TestBuildExecutionOrderHappyPath:
    def test_parent_precedes_children(self):
        ctx = make_context(make_tree(empty_feature=True))
        order = _build_execution_order(ctx)
        assert order.index("e1") < order.index("f1")
        assert order.index("f1") < order.index("s1")
        assert order.index("f1") < order.index("s2")

    def test_blocker_precedes_blocked(self):
        # s1 is blockedBy s2 -> s2 must be created before s1.
        ctx = make_context(make_tree(with_blocking=True))
        order = _build_execution_order(ctx)
        assert order.index("s2") < order.index("s1")

    def test_deterministic_across_calls(self):
        ctx = make_context(make_tree(with_blocking=True, empty_feature=True))
        first = _build_execution_order(ctx)
        second = _build_execution_order(ctx)
        assert first == second


class TestBuildExecutionOrderCycleReporting:
    def test_blocking_cycle_raises_validation_error(self):
        s1 = SubtaskNode(ref="s1", title="S1", body="b", issueType="Subtask", blockedBy=("s2",))
        s2 = SubtaskNode(ref="s2", title="S2", body="b", issueType="Subtask", blockedBy=("s1",))
        f1 = FeatureNode(ref="f1", title="F1", body="b", issueType="Feature", subtasks=(s1, s2))
        epic = EpicNode(ref="e1", title="Epic", body="b", issueType="Epic", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        ctx = make_context(tree)
        with pytest.raises(PipelineValidationError) as exc_info:
            _build_execution_order(ctx)
        assert "cycle" in str(exc_info.value).lower()
        assert "s1" in str(exc_info.value) and "s2" in str(exc_info.value)
