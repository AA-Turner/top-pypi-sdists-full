"""Tests for workflow engine audit integration (#953)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.db import init_db
from anteroom.services.workflow_engine import WorkflowEngine
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import create_workflow_run


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_engine(db: Any, audit_writer: Any = None) -> WorkflowEngine:
    from anteroom.config import WorkflowConfig

    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry, audit_writer=audit_writer)


class TestWorkflowAuditIntegration:
    def test_engine_accepts_audit_writer_param(self, db: Any) -> None:
        mock_writer = MagicMock()
        engine = _make_engine(db, audit_writer=mock_writer)
        assert engine._audit_writer is mock_writer

    def test_engine_works_without_audit_writer(self, db: Any) -> None:
        engine = _make_engine(db)
        assert engine._audit_writer is None

    @pytest.mark.asyncio
    async def test_emit_event_calls_audit_writer(self, db: Any) -> None:
        mock_writer = MagicMock()
        engine = _make_engine(db, audit_writer=mock_writer)
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="test",
            target_ref="123",
        )
        await engine._emit_event(run["id"], "run_started", payload={"workflow_id": "test"})
        assert mock_writer.emit.call_count == 1
        entry = mock_writer.emit.call_args[0][0]
        assert entry.event_type == "workflow.run_started"
        assert entry.severity == "info"
        assert entry.details["run_id"] == run["id"]
        assert entry.details["workflow_id"] == "test"

    @pytest.mark.asyncio
    async def test_emit_event_skips_when_no_audit_writer(self, db: Any) -> None:
        engine = _make_engine(db)
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="test",
            target_ref="123",
        )
        # Should not raise
        await engine._emit_event(run["id"], "run_started")

    @pytest.mark.asyncio
    async def test_emit_event_includes_step_id(self, db: Any) -> None:
        mock_writer = MagicMock()
        engine = _make_engine(db, audit_writer=mock_writer)
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="test",
            target_ref="123",
        )
        await engine._emit_event(run["id"], "step_started", step_id="build")
        entry = mock_writer.emit.call_args[0][0]
        assert entry.details["step_id"] == "build"

    @pytest.mark.asyncio
    async def test_emit_event_uses_workflow_prefix(self, db: Any) -> None:
        mock_writer = MagicMock()
        engine = _make_engine(db, audit_writer=mock_writer)
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="test",
            target_ref="123",
        )
        await engine._emit_event(run["id"], "step_finished")
        entry = mock_writer.emit.call_args[0][0]
        assert entry.event_type.startswith("workflow.")

    @pytest.mark.asyncio
    async def test_audit_error_does_not_break_event_emission(self, db: Any) -> None:
        mock_writer = MagicMock()
        mock_writer.emit.side_effect = RuntimeError("audit failure")
        engine = _make_engine(db, audit_writer=mock_writer)
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="test",
            target_ref="123",
        )
        # Should not raise despite audit failure
        await engine._emit_event(run["id"], "run_started")

    @pytest.mark.asyncio
    async def test_multiple_events_produce_multiple_audit_entries(self, db: Any) -> None:
        mock_writer = MagicMock()
        engine = _make_engine(db, audit_writer=mock_writer)
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="test",
            target_ref="123",
        )
        await engine._emit_event(run["id"], "run_started")
        await engine._emit_event(run["id"], "step_started", step_id="s1")
        await engine._emit_event(run["id"], "step_finished", step_id="s1")
        await engine._emit_event(run["id"], "run_completed")
        assert mock_writer.emit.call_count == 4
        event_types = [c[0][0].event_type for c in mock_writer.emit.call_args_list]
        assert event_types == [
            "workflow.run_started",
            "workflow.step_started",
            "workflow.step_finished",
            "workflow.run_completed",
        ]


class TestAuditWriterThreading:
    """Verify audit_writer is threaded through all WorkflowEngine constructor sites."""

    def test_all_engine_constructors_pass_audit_writer(self) -> None:
        """Grep all WorkflowEngine(...) calls and verify audit_writer is present.

        This is a source-level assertion that prevents regression —
        any new constructor site without audit_writer will fail this test.
        """
        from pathlib import Path

        src_root = Path(__file__).resolve().parent.parent.parent / "src" / "anteroom"
        constructor_files = []

        for py_file in src_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            content = py_file.read_text()
            if "WorkflowEngine(" not in content:
                continue
            # Skip the class definition itself and test files
            rel = str(py_file.relative_to(src_root))
            if rel == "services/workflow_engine.py":
                continue
            if rel == "services/workflow_simulator.py":
                continue  # simulator intentionally omits audit for temp DBs
            constructor_files.append((rel, content))

        assert len(constructor_files) > 0, "No WorkflowEngine constructor sites found"

        missing = []
        for rel, content in constructor_files:
            if "WorkflowEngine(" in content and "audit_writer" not in content:
                missing.append(rel)

        assert missing == [], (
            f"WorkflowEngine constructors missing audit_writer: {missing}. "
            "All production engine constructors must thread audit_writer."
        )
