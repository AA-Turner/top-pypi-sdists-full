"""Tests for workflow repair/edit-and-resume (#995)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import WorkflowEngine
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    _REPAIRABLE_RUN_FIELDS,
    _REPAIRABLE_RUN_STATUSES,
    _REPAIRABLE_STEP_FIELDS,
    apply_run_repair,
    apply_step_repair,
    create_workflow_run,
    create_workflow_step,
    get_workflow_run,
    get_workflow_step,
    list_repairs,
    list_workflow_events,
    update_workflow_run,
    update_workflow_step,
)


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def engine(db: Any) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


def _make_paused_run(db: Any, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
    """Create a run and set it to paused."""
    run = create_workflow_run(
        db,
        workflow_id="test_repair",
        workflow_version="0.1.0",
        target_kind="generic",
        target_ref="test",
        inputs=inputs or {"issue_number": 42},
    )
    update_workflow_run(db, run["id"], status="paused")
    return get_workflow_run(db, run["id"])


def _add_completed_step(
    db: Any,
    run_id: str,
    step_id: str,
    *,
    result_artifacts: dict[str, Any] | None = None,
    result_summary: str | None = None,
) -> dict[str, Any]:
    """Add a completed step to a run."""
    step = create_workflow_step(
        db,
        run_id=run_id,
        step_id=step_id,
        step_type="runner",
        runner_type="shell",
    )
    update_workflow_step(
        db,
        step["id"],
        status="completed",
        result_status="success",
        result_artifacts=result_artifacts or {"pr_number": 123},
        result_summary=result_summary or "Step completed",
    )
    return get_workflow_step(db, step["id"])


# ---------------------------------------------------------------------------
# Storage-level: apply_run_repair
# ---------------------------------------------------------------------------


class TestApplyRunRepair:
    def test_repair_inputs_on_paused_run(self, db: Any) -> None:
        run = _make_paused_run(db, inputs={"issue_number": 42})
        new_inputs = {"issue_number": 99}
        result = apply_run_repair(db, run["id"], "inputs", new_inputs)
        assert result["inputs"] == new_inputs

    def test_repair_records_event(self, db: Any) -> None:
        run = _make_paused_run(db)
        apply_run_repair(db, run["id"], "inputs", {"issue_number": 99})
        repairs = list_repairs(db, run["id"])
        assert len(repairs) == 1
        assert repairs[0]["event_type"] == "repair_applied"
        payload = repairs[0]["payload"]
        assert payload["scope"] == "run"
        assert payload["field"] == "inputs"
        assert payload["old_value"] == {"issue_number": 42}
        assert payload["new_value"] == {"issue_number": 99}
        assert payload["actor"] == "operator"

    def test_repair_disallowed_field_rejected(self, db: Any) -> None:
        run = _make_paused_run(db)
        with pytest.raises(ValueError, match="not repairable"):
            apply_run_repair(db, run["id"], "status", "completed")

    def test_repair_non_paused_run_rejected(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test_repair",
            workflow_version="0.1.0",
            target_kind="generic",
            target_ref="test",
            inputs={"x": 1},
        )
        update_workflow_run(db, run["id"], status="completed")
        with pytest.raises(ValueError, match="not repairable"):
            apply_run_repair(db, run["id"], "inputs", {"x": 2})

    def test_repair_nonexistent_run_rejected(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Run not found"):
            apply_run_repair(db, "nonexistent-id", "inputs", {})

    def test_repair_waiting_for_approval_run(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test_repair",
            workflow_version="0.1.0",
            target_kind="generic",
            target_ref="test",
            inputs={"x": 1},
        )
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        result = apply_run_repair(db, run["id"], "inputs", {"x": 2})
        assert result["inputs"] == {"x": 2}

    def test_repair_failed_run_allowed(self, db: Any) -> None:
        """Failed runs can be repaired (e.g. fix inputs before resuming)."""
        run = create_workflow_run(
            db,
            workflow_id="test_repair",
            workflow_version="0.1.0",
            target_kind="generic",
            target_ref="test",
            inputs={"issue": 99},
        )
        update_workflow_run(db, run["id"], status="failed", stop_reason="step_failed:bad_step")
        result = apply_run_repair(db, run["id"], "inputs", {"issue": 100})
        assert result["inputs"] == {"issue": 100}

    def test_repair_same_value_is_noop(self, db: Any) -> None:
        """Repairing to the same value still records the event (idempotent)."""
        run = _make_paused_run(db, inputs={"x": 1})
        apply_run_repair(db, run["id"], "inputs", {"x": 1})
        repairs = list_repairs(db, run["id"])
        assert len(repairs) == 1


# ---------------------------------------------------------------------------
# Storage-level: apply_step_repair
# ---------------------------------------------------------------------------


class TestApplyStepRepair:
    def test_repair_step_result_artifacts(self, db: Any) -> None:
        run = _make_paused_run(db)
        _add_completed_step(db, run["id"], "step_a", result_artifacts={"pr_number": 123})
        result = apply_step_repair(db, run["id"], "step_a", "result_artifacts", {"pr_number": 456})
        assert result["result_artifacts"] == {"pr_number": 456}

    def test_repair_step_result_summary(self, db: Any) -> None:
        run = _make_paused_run(db)
        _add_completed_step(db, run["id"], "step_a", result_summary="old summary")
        result = apply_step_repair(db, run["id"], "step_a", "result_summary", "new summary")
        assert result["result_summary"] == "new summary"

    def test_repair_step_records_event(self, db: Any) -> None:
        run = _make_paused_run(db)
        _add_completed_step(db, run["id"], "step_a")
        apply_step_repair(db, run["id"], "step_a", "result_artifacts", {"pr_number": 999})
        repairs = list_repairs(db, run["id"])
        assert len(repairs) == 1
        assert repairs[0]["payload"]["scope"] == "step"
        assert repairs[0]["payload"]["step_id"] == "step_a"

    def test_repair_step_disallowed_field(self, db: Any) -> None:
        run = _make_paused_run(db)
        _add_completed_step(db, run["id"], "step_a")
        with pytest.raises(ValueError, match="not repairable"):
            apply_step_repair(db, run["id"], "step_a", "status", "failed")

    def test_repair_step_not_completed_rejected(self, db: Any) -> None:
        run = _make_paused_run(db)
        create_workflow_step(db, run_id=run["id"], step_id="step_pending", step_type="runner")
        with pytest.raises(ValueError, match="not completed"):
            apply_step_repair(db, run["id"], "step_pending", "result_summary", "x")

    def test_repair_step_not_found(self, db: Any) -> None:
        run = _make_paused_run(db)
        with pytest.raises(ValueError, match="not found"):
            apply_step_repair(db, run["id"], "nonexistent", "result_summary", "x")

    def test_repair_step_on_terminal_run_rejected(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="generic",
            target_ref="test",
        )
        update_workflow_run(db, run["id"], status="completed")
        with pytest.raises(ValueError, match="not repairable"):
            apply_step_repair(db, run["id"], "step_a", "result_summary", "x")


# ---------------------------------------------------------------------------
# Engine-level: repair_run / repair_step
# ---------------------------------------------------------------------------


class TestEngineRepair:
    @pytest.mark.asyncio
    async def test_engine_repair_run(self, db: Any, engine: WorkflowEngine) -> None:
        run = _make_paused_run(db, inputs={"issue_number": 42})
        result = await engine.repair_run(run["id"], "inputs", {"issue_number": 99})
        assert result["inputs"] == {"issue_number": 99}

    @pytest.mark.asyncio
    async def test_engine_repair_step(self, db: Any, engine: WorkflowEngine) -> None:
        run = _make_paused_run(db)
        _add_completed_step(db, run["id"], "step_a", result_artifacts={"pr": 1})
        result = await engine.repair_step(run["id"], "step_a", "result_artifacts", {"pr": 2})
        assert result["result_artifacts"] == {"pr": 2}

    @pytest.mark.asyncio
    async def test_engine_repair_emits_events(self, db: Any, engine: WorkflowEngine) -> None:
        run = _make_paused_run(db)
        await engine.repair_run(run["id"], "inputs", {"x": 1})
        events = list_workflow_events(db, run["id"])
        repair_events = [e for e in events if e["event_type"] == "repair_applied"]
        # Storage persists exactly one durable event; engine only publishes (no duplicate)
        assert len(repair_events) == 1


# ---------------------------------------------------------------------------
# Boundary constants are correct
# ---------------------------------------------------------------------------


class TestRepairConstants:
    def test_repairable_run_fields(self) -> None:
        assert "inputs" in _REPAIRABLE_RUN_FIELDS
        assert "status" not in _REPAIRABLE_RUN_FIELDS
        assert "budget" not in _REPAIRABLE_RUN_FIELDS

    def test_repairable_step_fields(self) -> None:
        assert "result_artifacts" in _REPAIRABLE_STEP_FIELDS
        assert "result_summary" in _REPAIRABLE_STEP_FIELDS
        assert "status" not in _REPAIRABLE_STEP_FIELDS
        assert "step_type" not in _REPAIRABLE_STEP_FIELDS

    def test_repairable_statuses(self) -> None:
        assert "paused" in _REPAIRABLE_RUN_STATUSES
        assert "waiting_for_approval" in _REPAIRABLE_RUN_STATUSES
        assert "waiting_for_input" in _REPAIRABLE_RUN_STATUSES
        assert "failed" in _REPAIRABLE_RUN_STATUSES
        assert "running" not in _REPAIRABLE_RUN_STATUSES
        assert "completed" not in _REPAIRABLE_RUN_STATUSES


# ---------------------------------------------------------------------------
# Resume-after-repair honors new values
# ---------------------------------------------------------------------------


class TestResumeAfterRepair:
    def test_rebuild_step_results_uses_repaired_artifacts(self, db: Any, engine: WorkflowEngine) -> None:
        """After repairing step artifacts, _rebuild_step_results returns the new values."""
        run = _make_paused_run(db)
        _add_completed_step(db, run["id"], "step_a", result_artifacts={"pr": 1})

        # Repair the step artifacts
        apply_step_repair(db, run["id"], "step_a", "result_artifacts", {"pr": 999})

        # Rebuild should pick up repaired value
        results = engine._rebuild_step_results(run["id"])
        assert results["step_a"]["result_artifacts"] == {"pr": 999}

    def test_resume_reloads_repaired_inputs(self, db: Any) -> None:
        """After repairing inputs, get_workflow_run returns the new values."""
        run = _make_paused_run(db, inputs={"issue_number": 42})
        apply_run_repair(db, run["id"], "inputs", {"issue_number": 99})
        reloaded = get_workflow_run(db, run["id"])
        assert reloaded["inputs"] == {"issue_number": 99}


# ---------------------------------------------------------------------------
# CLI-level: _handle_repair parsing and error handling
# ---------------------------------------------------------------------------


class TestCliRepairParsing:
    """Test CLI _handle_repair field path parsing and error handling."""

    def test_cli_repair_missing_run_id(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        args = MagicMock()
        args.run_id = None
        args.field = "inputs"
        args.value = '{"x": 1}'
        config = MagicMock()

        _handle_repair(config, db, args)
        captured = capsys.readouterr()
        assert "run_id is required" in captured.out

    def test_cli_repair_missing_field(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        run = _make_paused_run(db)
        args = MagicMock()
        args.run_id = run["id"]
        args.field = None
        args.value = '{"x": 1}'
        config = MagicMock()

        _handle_repair(config, db, args)
        captured = capsys.readouterr()
        assert "--field" in captured.out

    def test_cli_repair_nonexistent_run(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        args = MagicMock()
        args.run_id = "nonexistent"
        args.field = "inputs"
        args.value = '{"x": 1}'
        config = MagicMock()

        _handle_repair(config, db, args)
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_cli_repair_invalid_field_path(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        run = _make_paused_run(db)
        args = MagicMock()
        args.run_id = run["id"]
        args.field = "a.b"  # Invalid: not "step.<id>.<field>" and not single field
        args.value = "x"
        config = MagicMock()

        _handle_repair(config, db, args)
        captured = capsys.readouterr()
        assert "Invalid field path" in captured.out

    def test_cli_repair_empty_step_id(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        run = _make_paused_run(db)
        args = MagicMock()
        args.run_id = run["id"]
        args.field = "step..result_artifacts"  # Empty step_id
        args.value = "{}"
        config = MagicMock()

        _handle_repair(config, db, args)
        captured = capsys.readouterr()
        assert "cannot be empty" in captured.out.lower()

    def test_cli_repair_json_value_parsing(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        """Verify JSON value is parsed correctly, not treated as string."""
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        run = _make_paused_run(db, inputs={"issue": 42})
        args = MagicMock()
        args.run_id = run["id"]
        args.field = "inputs"
        args.value = '{"issue": 99}'
        config = MagicMock()

        _handle_repair(config, db, args)

        reloaded = get_workflow_run(db, run["id"])
        assert reloaded["inputs"] == {"issue": 99}

    def test_cli_repair_disallowed_field_error(self, db: Any, capsys: pytest.CaptureFixture[str]) -> None:
        from unittest.mock import MagicMock

        from anteroom.cli.workflow_cli import _handle_repair

        run = _make_paused_run(db)
        args = MagicMock()
        args.run_id = run["id"]
        args.field = "status"
        args.value = "completed"
        config = MagicMock()

        _handle_repair(config, db, args)
        captured = capsys.readouterr()
        assert "not repairable" in captured.out.lower()
