"""Tests for _validate_policy_data() internal helper."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_devtools.orchestration.execution.decision_policy import (
    DecisionPolicyError,
    _validate_policy_data,
    load_decision_policy,
)


class TestValidatePolicyData:
    """Tests for _validate_policy_data() validation."""

    def test_valid_dict(self) -> None:
        """Valid dict passes."""
        _validate_policy_data({"version": 1, "default_action": "autonomous"})

    def test_non_dict_raises(self) -> None:
        """Non-dict raises DecisionPolicyError."""
        with pytest.raises(DecisionPolicyError, match="Policy must be a mapping"):
            _validate_policy_data([1, 2, 3])

    def test_invalid_version_raises(self) -> None:
        """Version != 1 raises."""
        with pytest.raises(DecisionPolicyError, match="Unsupported version"):
            _validate_policy_data({"version": 99})

    def test_version_1_passes(self) -> None:
        """Version 1 does not raise."""
        _validate_policy_data({"version": 1})

    def test_no_version_passes(self) -> None:
        """Missing version is fine (defaulted elsewhere)."""
        _validate_policy_data({"default_action": "autonomous"})


class TestLoadDecisionPolicyJson:
    """Additional tests for load_decision_policy() JSON error paths."""

    def test_malformed_json_raises(self, tmp_path: Path) -> None:
        """Malformed JSON raises DecisionPolicyError."""
        path = tmp_path / "bad.json"
        path.write_text("{not valid json")

        with pytest.raises(DecisionPolicyError, match="Failed to parse JSON"):
            load_decision_policy(path)

    def test_invalid_structure_raises(self, tmp_path: Path) -> None:
        """Unsupported policy version is re-raised as an invalid structure error."""
        path = tmp_path / "bad_structure.json"
        # version=2 passes JSON parsing but fails DecisionPolicy validation, which
        # load_decision_policy() catches and re-raises as "Invalid policy structure".
        path.write_text(json.dumps({"version": 2, "default_action": "autonomous"}))

        with pytest.raises(DecisionPolicyError, match="Invalid policy structure"):
            load_decision_policy(path)
