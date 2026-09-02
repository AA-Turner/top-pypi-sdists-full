"""Tests for DecisionResult dataclass."""

from __future__ import annotations

import json
from types import MappingProxyType

import pytest

from agentic_devtools.orchestration.policies.types import (
    ApprovalDecision,
    BudgetDecision,
    DecisionResult,
)


class TestDecisionResult:
    """Test DecisionResult validation and generic typing."""

    def test_valid_creation(self) -> None:
        result = DecisionResult(
            decision=ApprovalDecision.approve,
            rationale="All good.",
            metadata={"key": "value"},
        )
        assert result.decision == ApprovalDecision.approve
        assert result.rationale == "All good."
        assert result.metadata == {"key": "value"}

    def test_empty_rationale_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            DecisionResult(decision=ApprovalDecision.approve, rationale="")

    def test_whitespace_only_rationale_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            DecisionResult(decision=ApprovalDecision.approve, rationale="   ")

    def test_rationale_over_500_chars_raises(self) -> None:
        long_rationale = "x" * 501
        with pytest.raises(ValueError, match="500"):
            DecisionResult(decision=ApprovalDecision.approve, rationale=long_rationale)

    def test_rationale_exactly_500_chars_ok(self) -> None:
        rationale = "x" * 500
        result = DecisionResult(decision=ApprovalDecision.approve, rationale=rationale)
        assert len(result.rationale) == 500

    def test_default_metadata_empty_dict(self) -> None:
        result = DecisionResult(decision=BudgetDecision.continue_, rationale="ok")
        assert result.metadata == {}

    def test_frozen_immutability(self) -> None:
        result = DecisionResult(decision=ApprovalDecision.approve, rationale="ok")
        with pytest.raises(Exception):
            result.rationale = "changed"  # type: ignore[misc]

    def test_generic_typing_with_different_enums(self) -> None:
        r1: DecisionResult[ApprovalDecision] = DecisionResult(decision=ApprovalDecision.escalate, rationale="escalate")
        r2: DecisionResult[BudgetDecision] = DecisionResult(decision=BudgetDecision.halt, rationale="halt")
        assert r1.decision == ApprovalDecision.escalate
        assert r2.decision == BudgetDecision.halt

    def test_metadata_is_immutable_after_creation(self) -> None:
        """metadata dict is frozen in-place; callers cannot mutate it."""
        result = DecisionResult(
            decision=ApprovalDecision.approve,
            rationale="All good.",
            metadata={"key": "value"},
        )
        with pytest.raises(TypeError):
            result.metadata["key"] = "mutated"  # type: ignore[index]

    def test_metadata_equality_with_plain_dict(self) -> None:
        """Frozen metadata compares equal to an equivalent plain dict."""
        result = DecisionResult(
            decision=ApprovalDecision.approve,
            rationale="ok",
            metadata={"count": 3},
        )
        assert result.metadata == {"count": 3}

    def test_metadata_original_dict_mutation_not_reflected(self) -> None:
        """Mutating the original metadata dict after creation does not affect the stored copy."""
        original: dict[str, object] = {"key": "value"}
        result = DecisionResult(
            decision=ApprovalDecision.approve,
            rationale="All good.",
            metadata=original,
        )
        original["key"] = "mutated"
        assert result.metadata["key"] == "value"

    def test_metadata_is_mappingproxytype_not_dict(self) -> None:
        """metadata is a MappingProxyType after construction, not a plain dict."""
        result = DecisionResult(
            decision=ApprovalDecision.approve,
            rationale="ok",
            metadata={"a": 1},
        )
        assert isinstance(result.metadata, MappingProxyType)
        assert not isinstance(result.metadata, dict)

    def test_metadata_dict_conversion_is_json_serializable(self) -> None:
        """dict(result.metadata) produces a plain JSON-serializable dict."""
        result = DecisionResult(
            decision=ApprovalDecision.approve,
            rationale="ok",
            metadata={"count": 3, "label": "x"},
        )
        plain = dict(result.metadata)
        assert isinstance(plain, dict)
        # Must not raise
        serialized = json.dumps(plain)
        assert '"count": 3' in serialized
