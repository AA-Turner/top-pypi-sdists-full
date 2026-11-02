"""Tests for NodeStatus dataclass — FR-010."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.orchestration.node_status import NodeStatus


class TestNodeStatus:
    """Tests for NodeStatus construction and invariants."""

    def test_completed_status_construction(self) -> None:
        ns = NodeStatus(status="completed", attempt_count=1)
        assert ns.status == "completed"
        assert ns.attempt_count == 1
        assert ns.error_summary is None

    def test_failed_status_requires_error_summary(self) -> None:
        with pytest.raises(ValueError, match="error_summary must be non-empty"):
            NodeStatus(status="failed", attempt_count=1, error_summary=None)

    def test_failed_status_with_empty_string_raises(self) -> None:
        with pytest.raises(ValueError, match="error_summary must be non-empty"):
            NodeStatus(status="failed", attempt_count=1, error_summary="")

    def test_failed_permanent_requires_error_summary(self) -> None:
        with pytest.raises(ValueError, match="error_summary must be non-empty"):
            NodeStatus(status="failed_permanent", attempt_count=3, error_summary=None)

    def test_completed_with_error_summary_raises(self) -> None:
        with pytest.raises(ValueError, match="error_summary must be None"):
            NodeStatus(status="completed", attempt_count=1, error_summary="oops")

    def test_attempt_count_must_be_at_least_1(self) -> None:
        with pytest.raises(ValueError, match="attempt_count must be >= 1"):
            NodeStatus(status="completed", attempt_count=0)

    def test_invalid_status_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid status"):
            NodeStatus(status="unknown", attempt_count=1)

    def test_to_dict_serialization(self) -> None:
        ns = NodeStatus(status="failed", attempt_count=2, error_summary="timeout")
        d = ns.to_dict()
        assert d == {"status": "failed", "attempt_count": 2, "error_summary": "timeout"}

    def test_from_dict_deserialization(self) -> None:
        d = {"status": "completed", "attempt_count": 1, "error_summary": None}
        ns = NodeStatus.from_dict(d)
        assert ns.status == "completed"
        assert ns.attempt_count == 1

    def test_json_roundtrip(self) -> None:
        ns = NodeStatus(status="failed_permanent", attempt_count=4, error_summary="budget exhausted")
        serialized = json.dumps(ns.to_dict())
        deserialized = NodeStatus.from_dict(json.loads(serialized))
        assert deserialized == ns

    def test_frozen_immutability(self) -> None:
        ns = NodeStatus(status="completed", attempt_count=1)
        with pytest.raises(AttributeError):
            ns.status = "failed"  # type: ignore[misc]
