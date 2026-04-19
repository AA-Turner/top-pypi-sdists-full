"""Unit tests for ``services.lineage`` (#925)."""

from __future__ import annotations

import logging
from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.services.audit import AuditEntry
from anteroom.services.lineage import (
    emit_memory_promotion,
    emit_workflow_approval,
    emit_workflow_cancel,
    emit_workflow_decision,
    emit_workflow_run_lifecycle,
    resolve_memory_lineage,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _capture_writer() -> tuple[Any, list[AuditEntry]]:
    """Return a mock writer and a list capturing every emit() call."""
    captured: list[AuditEntry] = []
    writer = MagicMock()
    writer.emit.side_effect = captured.append
    return writer, captured


# ---------------------------------------------------------------------------
# emit_workflow_approval
# ---------------------------------------------------------------------------


class TestEmitWorkflowApproval:
    def test_approved_emits_workflow_approved_event(self) -> None:
        writer, captured = _capture_writer()
        emit_workflow_approval(
            writer,
            run_id="r1",
            request_id="req1",
            outcome="approved",
            resolved_by="alice",
            tool_name="bash",
        )
        assert len(captured) == 1
        entry = captured[0]
        assert entry.event_type == "workflow.approved"
        assert entry.severity == "info"
        assert entry.user_id == "alice"
        assert entry.details["run_id"] == "r1"
        assert entry.details["request_id"] == "req1"
        assert entry.details["outcome"] == "approved"
        assert entry.details["tool_name"] == "bash"

    def test_denied_emits_workflow_denied_event(self) -> None:
        writer, captured = _capture_writer()
        emit_workflow_approval(
            writer,
            run_id="r1",
            request_id="req1",
            outcome="denied",
            resolved_by="bob",
        )
        assert len(captured) == 1
        assert captured[0].event_type == "workflow.denied"
        assert captured[0].severity == "info"

    def test_unknown_outcome_drops_silently(self, caplog: pytest.LogCaptureFixture) -> None:
        writer, captured = _capture_writer()
        with caplog.at_level(logging.WARNING):
            emit_workflow_approval(
                writer,
                run_id="r1",
                request_id="req1",
                outcome="garbage",
                resolved_by="alice",
            )
        assert captured == []
        assert any("unknown outcome" in m for m in caplog.messages)

    def test_none_writer_is_noop(self) -> None:
        # Must not raise.
        emit_workflow_approval(
            None,
            run_id="r1",
            request_id="req1",
            outcome="approved",
            resolved_by="alice",
        )

    def test_writer_emit_raises_does_not_propagate(self, caplog: pytest.LogCaptureFixture) -> None:
        writer = MagicMock()
        writer.emit.side_effect = RuntimeError("disk full")
        with caplog.at_level(logging.WARNING):
            emit_workflow_approval(
                writer,
                run_id="r1",
                request_id="req1",
                outcome="approved",
                resolved_by="alice",
            )
        assert any("Failed to emit" in m for m in caplog.messages)


# ---------------------------------------------------------------------------
# emit_workflow_decision
# ---------------------------------------------------------------------------


class TestEmitWorkflowDecision:
    def test_emits_workflow_decision_resolved(self) -> None:
        writer, captured = _capture_writer()
        emit_workflow_decision(
            writer,
            run_id="r1",
            decision_id="d1",
            option_id="opt-a",
            resolved_by="alice",
        )
        assert len(captured) == 1
        entry = captured[0]
        assert entry.event_type == "workflow.decision_resolved"
        assert entry.severity == "info"
        assert entry.user_id == "alice"
        assert entry.details == {
            "run_id": "r1",
            "decision_id": "d1",
            "option_id": "opt-a",
        }

    def test_none_writer_is_noop(self) -> None:
        emit_workflow_decision(
            None,
            run_id="r1",
            decision_id="d1",
            option_id="opt-a",
            resolved_by="alice",
        )


# ---------------------------------------------------------------------------
# emit_workflow_cancel
# ---------------------------------------------------------------------------


class TestEmitWorkflowCancel:
    def test_emits_workflow_cancel_requested(self) -> None:
        writer, captured = _capture_writer()
        emit_workflow_cancel(
            writer,
            run_id="r1",
            cancelled_by="alice",
            reason="user requested stop",
            from_status="running",
        )
        assert len(captured) == 1
        entry = captured[0]
        assert entry.event_type == "workflow.cancel_requested"
        assert entry.severity == "info"
        assert entry.user_id == "alice"
        assert entry.details["reason"] == "user requested stop"
        assert entry.details["from_status"] == "running"

    def test_optional_fields_default_to_empty(self) -> None:
        writer, captured = _capture_writer()
        emit_workflow_cancel(writer, run_id="r1", cancelled_by="alice")
        assert captured[0].details["reason"] == ""
        assert captured[0].details["from_status"] == ""

    def test_none_writer_is_noop(self) -> None:
        emit_workflow_cancel(None, run_id="r1", cancelled_by="alice")


# ---------------------------------------------------------------------------
# emit_workflow_run_lifecycle
# ---------------------------------------------------------------------------


class TestEmitWorkflowRunLifecycle:
    @pytest.mark.parametrize(
        ("event", "severity"),
        [
            ("started", "info"),
            ("completed", "info"),
            ("failed", "warning"),
            ("cancelled", "warning"),
        ],
    )
    def test_emits_each_lifecycle_event(self, event: str, severity: str) -> None:
        writer, captured = _capture_writer()
        emit_workflow_run_lifecycle(writer, event, run_id="r1", user_id="alice")
        assert len(captured) == 1
        assert captured[0].event_type == f"workflow.run.{event}"
        assert captured[0].severity == severity
        assert captured[0].user_id == "alice"
        assert captured[0].details == {"run_id": "r1"}

    def test_details_merged_into_payload(self) -> None:
        writer, captured = _capture_writer()
        emit_workflow_run_lifecycle(
            writer,
            "completed",
            run_id="r1",
            details={"duration_ms": 12345, "step_count": 7},
        )
        details = captured[0].details
        assert details["run_id"] == "r1"
        assert details["duration_ms"] == 12345
        assert details["step_count"] == 7

    def test_unknown_event_drops_silently(self, caplog: pytest.LogCaptureFixture) -> None:
        writer, captured = _capture_writer()
        with caplog.at_level(logging.WARNING):
            emit_workflow_run_lifecycle(writer, "weird", run_id="r1")
        assert captured == []
        assert any("unknown event" in m for m in caplog.messages)

    def test_none_writer_is_noop(self) -> None:
        emit_workflow_run_lifecycle(None, "started", run_id="r1")


# ---------------------------------------------------------------------------
# emit_memory_promotion
# ---------------------------------------------------------------------------


class TestEmitMemoryPromotion:
    @pytest.mark.parametrize(
        ("event", "severity"),
        [
            ("proposed", "info"),
            ("approved", "info"),
            ("rejected", "warning"),
        ],
    )
    def test_emits_each_event(self, event: str, severity: str) -> None:
        writer, captured = _capture_writer()
        emit_memory_promotion(writer, event, fqn="@user/memory/x", reviewer_id="alice")
        assert len(captured) == 1
        assert captured[0].event_type == f"memory.{event}"
        assert captured[0].severity == severity
        assert captured[0].user_id == "alice"
        assert captured[0].details == {"fqn": "@user/memory/x"}

    def test_details_merged_into_payload(self) -> None:
        writer, captured = _capture_writer()
        emit_memory_promotion(
            writer,
            "rejected",
            fqn="@user/memory/x",
            reviewer_id="alice",
            details={"reason": "duplicate", "previous_status": "candidate"},
        )
        details = captured[0].details
        assert details["fqn"] == "@user/memory/x"
        assert details["reason"] == "duplicate"
        assert details["previous_status"] == "candidate"

    def test_unknown_event_drops_silently(self, caplog: pytest.LogCaptureFixture) -> None:
        writer, captured = _capture_writer()
        with caplog.at_level(logging.WARNING):
            emit_memory_promotion(writer, "vaporized", fqn="@u/memory/x")
        assert captured == []
        assert any("unknown event" in m for m in caplog.messages)

    def test_none_writer_is_noop(self) -> None:
        emit_memory_promotion(None, "proposed", fqn="@user/memory/x")


# ---------------------------------------------------------------------------
# resolve_memory_lineage
# ---------------------------------------------------------------------------


class TestResolveMemoryLineage:
    def test_missing_memory_returns_empty_view(self) -> None:
        db = MagicMock()
        # get_memory returns None for missing
        from anteroom.services import lineage as lineage_mod

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "anteroom.services.memory_service.get_memory",
                lambda _db, _fqn: None,
            )
            mp.setattr(
                "anteroom.services.memory_service.list_memories",
                lambda *_a, **_k: [],
            )
            result = lineage_mod.resolve_memory_lineage(db, "@user/memory/missing")
        assert result == {
            "fqn": "@user/memory/missing",
            "provenance": None,
            "lineage": [],
            "related_memories": [],
        }

    def test_returns_provenance_and_lineage_for_existing_memory(self) -> None:
        db = MagicMock()
        target = {
            "fqn": "@user/memory/x",
            "metadata": {
                "memory_status": "active",
                "provenance": {"conversation_id": "conv1", "message_id": "msg1"},
                "lineage": [
                    {"event": "proposed", "actor": "agent"},
                    {"event": "approved", "actor": "alice"},
                ],
            },
            "created_at": "2026-04-18T00:00:00Z",
        }
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "anteroom.services.memory_service.get_memory",
                lambda _db, _fqn: target,
            )
            mp.setattr(
                "anteroom.services.memory_service.list_memories",
                lambda *_a, **_k: [target],
            )
            result = resolve_memory_lineage(db, "@user/memory/x")
        assert result["fqn"] == "@user/memory/x"
        assert result["provenance"] == {"conversation_id": "conv1", "message_id": "msg1"}
        assert len(result["lineage"]) == 2
        assert result["lineage"][1]["event"] == "approved"
        # The target itself is filtered out of related_memories
        assert result["related_memories"] == []

    def test_related_memories_share_conversation(self) -> None:
        target_meta = {
            "memory_status": "active",
            "provenance": {"conversation_id": "conv1"},
            "lineage": [],
        }
        sibling_meta = {
            "memory_status": "candidate",
            "memory_category": "preference",
            "provenance": {"conversation_id": "conv1"},
        }
        unrelated_meta = {
            "memory_status": "active",
            "provenance": {"conversation_id": "conv-other"},
        }
        target = {"fqn": "@u/memory/x", "metadata": target_meta, "created_at": "t1"}
        sibling = {"fqn": "@u/memory/y", "metadata": sibling_meta, "created_at": "t2"}
        unrelated = {"fqn": "@u/memory/z", "metadata": unrelated_meta, "created_at": "t3"}
        db = MagicMock()
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "anteroom.services.memory_service.get_memory",
                lambda _db, _fqn: target,
            )
            mp.setattr(
                "anteroom.services.memory_service.list_memories",
                lambda *_a, **_k: [target, sibling, unrelated],
            )
            result = resolve_memory_lineage(db, "@u/memory/x")
        related_fqns = {item["fqn"] for item in result["related_memories"]}
        assert related_fqns == {"@u/memory/y"}
        item = result["related_memories"][0]
        assert item["memory_status"] == "candidate"
        assert item["memory_category"] == "preference"

    def test_related_memories_capped_at_50(self) -> None:
        target = {
            "fqn": "@u/memory/main",
            "metadata": {
                "memory_status": "active",
                "provenance": {"conversation_id": "convX"},
            },
            "created_at": "t",
        }
        siblings = [
            {
                "fqn": f"@u/memory/sib{i}",
                "metadata": {
                    "memory_status": "candidate",
                    "provenance": {"conversation_id": "convX"},
                },
                "created_at": f"t{i}",
            }
            for i in range(75)
        ]
        all_mems = [target, *siblings]
        db = MagicMock()
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "anteroom.services.memory_service.get_memory",
                lambda _db, _fqn: target,
            )
            mp.setattr(
                "anteroom.services.memory_service.list_memories",
                lambda *_a, **_k: all_mems,
            )
            result = resolve_memory_lineage(db, "@u/memory/main")
        assert len(result["related_memories"]) == 50

    def test_no_provenance_returns_no_related(self) -> None:
        target = {
            "fqn": "@u/memory/x",
            "metadata": {"memory_status": "active"},
            "created_at": "t",
        }
        db = MagicMock()
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "anteroom.services.memory_service.get_memory",
                lambda _db, _fqn: target,
            )
            mp.setattr(
                "anteroom.services.memory_service.list_memories",
                lambda *_a, **_k: [target],
            )
            result = resolve_memory_lineage(db, "@u/memory/x")
        assert result["provenance"] is None
        assert result["related_memories"] == []
