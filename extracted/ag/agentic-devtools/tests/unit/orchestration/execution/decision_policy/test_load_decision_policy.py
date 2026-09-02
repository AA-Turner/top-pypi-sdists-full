"""Tests for DecisionPolicy and load_decision_policy()."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_devtools.orchestration.execution.decision_policy import (
    DecisionPolicy,
    DecisionPolicyError,
    get_action_for_tool,
    load_decision_policy,
)


class TestDecisionPolicy:
    """Tests for DecisionPolicy dataclass validation."""

    def test_valid_construction(self) -> None:
        """Valid policy is created successfully."""
        policy = DecisionPolicy(
            version=1,
            default_action="autonomous",
            tool_actions={"dangerous_tool": "requires_confirmation"},
        )
        assert policy.version == 1
        assert policy.default_action == "autonomous"
        assert policy.tool_actions["dangerous_tool"] == "requires_confirmation"

    def test_invalid_version_raises(self) -> None:
        """Version != 1 raises DecisionPolicyError."""
        with pytest.raises(DecisionPolicyError, match="Unsupported policy version"):
            DecisionPolicy(version=2, default_action="autonomous")

    def test_invalid_default_action_raises(self) -> None:
        """Invalid default_action raises DecisionPolicyError."""
        with pytest.raises(DecisionPolicyError, match="Invalid default_action"):
            DecisionPolicy(version=1, default_action="invalid_action")

    def test_invalid_tool_action_raises(self) -> None:
        """Invalid tool action raises DecisionPolicyError."""
        with pytest.raises(DecisionPolicyError, match="Invalid action"):
            DecisionPolicy(
                version=1,
                default_action="autonomous",
                tool_actions={"tool_x": "bad_action"},
            )

    def test_non_dict_tool_actions_raises(self) -> None:
        """Non-dict tool_actions raises DecisionPolicyError (not AttributeError)."""
        with pytest.raises(DecisionPolicyError, match="tool_actions must be a mapping"):
            DecisionPolicy(
                version=1,
                default_action="autonomous",
                tool_actions=["push", "pull"],  # type: ignore[arg-type]
            )

    def test_null_tool_actions_raises(self) -> None:
        """None tool_actions raises DecisionPolicyError."""
        with pytest.raises(DecisionPolicyError, match="tool_actions must be a mapping"):
            DecisionPolicy(
                version=1,
                default_action="autonomous",
                tool_actions=None,  # type: ignore[arg-type]
            )

    def test_frozen(self) -> None:
        """Policy is frozen."""
        policy = DecisionPolicy(version=1, default_action="autonomous")
        with pytest.raises(AttributeError):
            policy.version = 2  # type: ignore[misc]


class TestLoadDecisionPolicy:
    """Tests for load_decision_policy() from files."""

    def test_load_json_policy(self, tmp_path: Path) -> None:
        """Loads a valid JSON policy file."""
        policy_data = {
            "version": 1,
            "default_action": "autonomous",
            "tool_actions": {"git_push": "requires_confirmation"},
        }
        path = tmp_path / "policy.json"
        path.write_text(json.dumps(policy_data))

        policy = load_decision_policy(path)
        assert policy.default_action == "autonomous"
        assert policy.tool_actions["git_push"] == "requires_confirmation"

    def test_load_yaml_policy(self, tmp_path: Path) -> None:
        """Loads a valid YAML policy file."""
        yaml_content = """
version: 1
default_action: requires_confirmation
tool_actions:
  read_file: autonomous
  delete_branch: denied
"""
        path = tmp_path / "policy.yml"
        path.write_text(yaml_content)

        policy = load_decision_policy(path)
        assert policy.default_action == "requires_confirmation"
        assert policy.tool_actions["read_file"] == "autonomous"
        assert policy.tool_actions["delete_branch"] == "denied"

    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        """Missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_decision_policy(tmp_path / "nonexistent.json")

    def test_malformed_yaml_raises(self, tmp_path: Path) -> None:
        """Malformed YAML raises DecisionPolicyError."""
        path = tmp_path / "bad.yml"
        path.write_text(": invalid: yaml: {{[")

        with pytest.raises(DecisionPolicyError, match="Failed to parse YAML"):
            load_decision_policy(path)

    def test_non_dict_raises(self, tmp_path: Path) -> None:
        """Non-dict content raises DecisionPolicyError."""
        path = tmp_path / "list.json"
        path.write_text("[1, 2, 3]")

        with pytest.raises(DecisionPolicyError, match="Policy must be a mapping"):
            load_decision_policy(path)


class TestGetActionForTool:
    """Tests for get_action_for_tool() lookup."""

    def test_returns_specific_action(self) -> None:
        """Returns tool-specific action when configured."""
        policy = DecisionPolicy(
            version=1,
            default_action="autonomous",
            tool_actions={"push": "requires_confirmation"},
        )
        assert get_action_for_tool(policy, "push") == "requires_confirmation"

    def test_returns_default_for_unknown_tool(self) -> None:
        """Returns default_action for unlisted tools."""
        policy = DecisionPolicy(version=1, default_action="autonomous")
        assert get_action_for_tool(policy, "unknown_tool") == "autonomous"
