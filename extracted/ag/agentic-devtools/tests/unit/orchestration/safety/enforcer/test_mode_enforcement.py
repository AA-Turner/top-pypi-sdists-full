"""Tests for mode enforcement — FR-003 rules."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    ClassificationEntry,
    ClassificationRegistry,
)
from agentic_devtools.orchestration.safety.enforcer import SafetyEnforcer, SafetyPolicy
from agentic_devtools.orchestration.safety.exceptions import PolicyViolationError
from agentic_devtools.orchestration.safety.mode import ExecutionMode


def _make_enforcer(mode: ExecutionMode, allow_destructive: bool = False) -> SafetyEnforcer:
    """Create a SafetyEnforcer with a minimal registry for testing."""
    registry = ClassificationRegistry()
    registry.register(ClassificationEntry("read_tool", ActionClassification.read_only))
    registry.register(ClassificationEntry("local_tool", ActionClassification.local_mutation))
    registry.register(ClassificationEntry("ext_tool", ActionClassification.external_mutation))
    registry.register(ClassificationEntry("destroy_tool", ActionClassification.destructive))

    policy = SafetyPolicy(
        execution_mode=mode,
        allow_destructive=allow_destructive,
    )
    # Disable branch/worktree guards for mode enforcement tests
    from unittest.mock import MagicMock

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


class TestModeEnforcement:
    """Tests for FR-003 mode enforcement rules."""

    def test_live_allows_read_only(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.live)
        decision = enforcer.evaluate("read_tool")
        assert decision.action == "execute"

    def test_live_allows_local_mutation(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.live)
        decision = enforcer.evaluate("local_tool")
        assert decision.action == "execute"

    def test_live_allows_external_mutation(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.live)
        decision = enforcer.evaluate("ext_tool", node_name="test_node")
        assert decision.action == "execute"

    def test_live_blocks_destructive_without_opt_in(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.live, allow_destructive=False)
        with pytest.raises(PolicyViolationError, match="destructive"):
            enforcer.evaluate("destroy_tool", node_name="test_node")

    def test_live_allows_destructive_with_opt_in(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.live, allow_destructive=True)
        decision = enforcer.evaluate("destroy_tool", node_name="test_node")
        assert decision.action == "execute"

    def test_dry_run_allows_read_only(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.dry_run)
        decision = enforcer.evaluate("read_tool")
        assert decision.action == "execute"

    def test_dry_run_allows_local_mutation(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.dry_run)
        decision = enforcer.evaluate("local_tool")
        assert decision.action == "execute"

    def test_dry_run_simulates_external_mutation(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.dry_run)
        decision = enforcer.evaluate("ext_tool", node_name="test_node")
        assert decision.action == "simulate"

    def test_dry_run_simulates_destructive(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.dry_run)
        decision = enforcer.evaluate("destroy_tool", node_name="test_node")
        assert decision.action == "simulate"


class TestRestrictedMode:
    """Tests for restricted mode — blocks all mutations."""

    def test_restricted_allows_read_only(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.restricted)
        decision = enforcer.evaluate("read_tool")
        assert decision.action == "execute"

    def test_restricted_blocks_local_mutation(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.restricted)
        with pytest.raises(PolicyViolationError, match="restricted"):
            enforcer.evaluate("local_tool")

    def test_restricted_blocks_external_mutation(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.restricted)
        with pytest.raises(PolicyViolationError, match="restricted"):
            enforcer.evaluate("ext_tool", node_name="test_node")

    def test_restricted_blocks_destructive(self) -> None:
        enforcer = _make_enforcer(ExecutionMode.restricted)
        with pytest.raises(PolicyViolationError, match="restricted"):
            enforcer.evaluate("destroy_tool", node_name="test_node")
