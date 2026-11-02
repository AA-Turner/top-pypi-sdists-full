"""Tests for node_name validation in SafetyEnforcer.evaluate() — FR-006."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.enforcer import SafetyEnforcer, SafetyPolicy
from agentic_devtools.orchestration.safety.mode import ExecutionMode


def _make_enforcer_with_ext_tool() -> SafetyEnforcer:
    """Create an enforcer that has external_mutation and destructive tools."""
    registry = ClassificationRegistry()
    registry.register(ClassificationEntry("ext_tool", ActionClassification.external_mutation))
    registry.register(ClassificationEntry("destroy_tool", ActionClassification.destructive))

    policy = SafetyPolicy(execution_mode=ExecutionMode.live, allow_destructive=True)

    branch_guard = MagicMock()
    branch_guard.check = MagicMock()
    worktree_guard = MagicMock()
    worktree_guard.check = MagicMock()

    return SafetyEnforcer(
        policy=policy,
        classification_registry=registry,
        branch_guard=branch_guard,
        worktree_guard=worktree_guard,
    )


class TestNodeNameValidation:
    """Tests that empty node_name raises ValueError for external/destructive tools."""

    def test_empty_node_name_raises_for_external_mutation(self) -> None:
        enforcer = _make_enforcer_with_ext_tool()
        with pytest.raises(ValueError, match="node_name must be non-empty"):
            enforcer.evaluate("ext_tool", {"key": "val"}, node_name="")

    def test_empty_node_name_raises_for_destructive_tool(self) -> None:
        enforcer = _make_enforcer_with_ext_tool()
        with pytest.raises(ValueError, match="node_name must be non-empty"):
            enforcer.evaluate("destroy_tool", {"key": "val"}, node_name="")

    def test_whitespace_only_node_name_raises_for_external_mutation(self) -> None:
        """Whitespace-only node_name is treated the same as empty — raises ValueError."""
        enforcer = _make_enforcer_with_ext_tool()
        with pytest.raises(ValueError, match="node_name must be non-empty"):
            enforcer.evaluate("ext_tool", {"key": "val"}, node_name="   ")

    def test_whitespace_only_node_name_raises_for_destructive_tool(self) -> None:
        """Whitespace-only node_name is treated the same as empty — raises ValueError."""
        enforcer = _make_enforcer_with_ext_tool()
        with pytest.raises(ValueError, match="node_name must be non-empty"):
            enforcer.evaluate("destroy_tool", {"key": "val"}, node_name="   ")
