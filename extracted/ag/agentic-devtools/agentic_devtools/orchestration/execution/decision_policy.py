"""Decision policy loading and enforcement.

Provides ``DecisionPolicy``, ``load_decision_policy()``, and
``get_action_for_tool()`` for classifying tool actions as autonomous,
requires_confirmation, or denied.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class DecisionPolicyError(Exception):
    """Raised when a decision policy is malformed or invalid."""


VALID_ACTIONS = frozenset({"autonomous", "requires_confirmation", "denied"})


@dataclass(frozen=True)
class DecisionPolicy:
    """Frozen policy configuration for tool action classification.

    Attributes:
        version: Schema version (must be 1).
        default_action: Default classification for unlisted tools.
        tool_actions: Mapping of tool_id → action classification.
    """

    version: int
    default_action: str
    tool_actions: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate policy fields."""
        if self.version != 1:
            raise DecisionPolicyError(f"Unsupported policy version: {self.version} (expected 1)")
        if self.default_action not in VALID_ACTIONS:
            raise DecisionPolicyError(
                f"Invalid default_action: {self.default_action!r} (expected one of {sorted(VALID_ACTIONS)})"
            )
        if not isinstance(self.tool_actions, dict):
            raise DecisionPolicyError(f"tool_actions must be a mapping, got {type(self.tool_actions).__name__}")
        for tool_id, action in self.tool_actions.items():
            if action not in VALID_ACTIONS:
                raise DecisionPolicyError(
                    f"Invalid action {action!r} for tool {tool_id!r} (expected one of {sorted(VALID_ACTIONS)})"
                )


def load_decision_policy(path: Path) -> DecisionPolicy:
    """Load a decision policy from a YAML or JSON file.

    Parses and validates policy data, emitting a warning if loading exceeds 1 second.

    Args:
        path: Path to the policy file (.yml, .yaml, or .json).

    Returns:
        A validated ``DecisionPolicy`` instance.

    Raises:
        DecisionPolicyError: If the file is malformed or invalid.
        FileNotFoundError: If the file does not exist.
    """
    start = time.monotonic()

    if not path.exists():
        raise FileNotFoundError(f"Decision policy file not found: {path}")

    content = path.read_text()

    if path.suffix in (".yml", ".yaml"):
        try:
            import yaml

            data = yaml.safe_load(content)
        except Exception as exc:
            raise DecisionPolicyError(f"Failed to parse YAML policy: {exc}") from exc
    else:
        import json

        try:
            data = json.loads(content)
        except Exception as exc:
            raise DecisionPolicyError(f"Failed to parse JSON policy: {exc}") from exc

    if not isinstance(data, dict):
        raise DecisionPolicyError(f"Policy must be a mapping, got {type(data).__name__}")

    try:
        policy = DecisionPolicy(
            version=data.get("version", 1),
            default_action=data.get("default_action", "autonomous"),
            tool_actions=data.get("tool_actions", {}),
        )
    except (TypeError, DecisionPolicyError) as exc:
        raise DecisionPolicyError(f"Invalid policy structure: {exc}") from exc

    elapsed = time.monotonic() - start
    if elapsed > 1.0:  # pragma: no cover
        import sys

        print(
            f"[DecisionPolicy] WARNING: policy loading took {elapsed:.2f}s (>1s)",
            file=sys.stderr,
        )

    return policy


def get_action_for_tool(policy: DecisionPolicy, tool_id: str) -> str:
    """Get the action classification for a tool.

    Args:
        policy: The decision policy to consult.
        tool_id: The tool identifier to look up.

    Returns:
        Action string: ``"autonomous"``, ``"requires_confirmation"``, or ``"denied"``.
    """
    return policy.tool_actions.get(tool_id, policy.default_action)


def _validate_policy_data(data: Any) -> None:
    """Validate raw policy data structure (internal helper)."""
    if not isinstance(data, dict):
        raise DecisionPolicyError(f"Policy must be a mapping, got {type(data).__name__}")
    if "version" in data and data["version"] != 1:
        raise DecisionPolicyError(f"Unsupported version: {data['version']}")
