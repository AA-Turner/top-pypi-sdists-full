"""Tests for workflow compensation and rollback steps (#978)."""

from __future__ import annotations

import contextlib
from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.workflow_engine import (
    WorkflowEngine,
    _build_compensate_lookup,
    _build_compensation_queue,
    load_definition,
)

WS_MOD = "anteroom.services.workflow_storage"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config() -> MagicMock:
    config = MagicMock()
    config.stale_threshold = 60
    config.heartbeat_interval = 15
    config.budget = None
    return config


def _make_runner_registry() -> MagicMock:
    return MagicMock()


def _make_engine(db: Any = None, config: Any = None) -> WorkflowEngine:
    db = db or MagicMock()
    config = config or _make_config()
    return WorkflowEngine(db, config, _make_runner_registry())


def _yaml_with_compensate(compensate_type: str = "runner") -> str:
    return f"""
kind: workflow
id: test-compensate
version: "1"
steps:
  - id: deploy
    type: runner
    runner: shell
    command: "echo deploy"
    compensate:
      type: {compensate_type}
      runner: shell
      command: "echo rollback"
  - id: verify
    type: runner
    runner: shell
    command: "echo verify"
"""


def _yaml_with_branch_compensate() -> str:
    return """
kind: workflow
id: test-branch-comp
version: "1"
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: b1
        steps:
          - id: s1
            type: runner
            runner: shell
            command: "echo s1"
            compensate:
              type: runner
              runner: shell
              command: "echo undo s1"
      - id: b2
        steps:
          - id: s2
            type: runner
            runner: shell
            command: "echo s2"
  - id: final
    type: runner
    runner: shell
    command: "echo final"
"""


def _yaml_two_compensate() -> str:
    return """
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo 1"
    compensate:
      type: runner
      runner: shell
      command: "echo undo 1"
  - id: step2
    type: runner
    runner: shell
    command: "echo 2"
    compensate:
      type: runner
      runner: shell
      command: "echo undo 2"
  - id: step3
    type: runner
    runner: shell
    command: "echo 3"
"""


# ---------------------------------------------------------------------------
# Parsing tests
# ---------------------------------------------------------------------------


class TestParseCompensateBlock:
    def test_compensate_parsed(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        step = defn.steps[0]
        assert step.compensate is not None
        assert step.compensate.type == "runner"
        assert step.compensate.id == "deploy_compensate"
        assert step.compensate.runner == "shell"

    def test_compensate_auto_id(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        assert defn.steps[0].compensate is not None
        assert defn.steps[0].compensate.id == "deploy_compensate"

    def test_compensate_custom_id(self) -> None:
        yaml_str = """
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
    compensate:
      id: my_rollback
      type: runner
      runner: shell
      command: "echo rollback"
"""
        defn = load_definition(yaml_str)
        assert defn.steps[0].compensate is not None
        assert defn.steps[0].compensate.id == "my_rollback"

    def test_no_compensate(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        assert defn.steps[1].compensate is None

    def test_nested_compensate_rejected(self) -> None:
        yaml_str = """
kind: workflow
id: test-nested
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
    compensate:
      type: runner
      runner: shell
      command: "echo rollback"
      compensate:
        type: runner
        runner: shell
        command: "echo nested"
"""
        with pytest.raises(ValueError, match="nested compensate"):
            load_definition(yaml_str)

    def test_invalid_compensate_type_rejected(self) -> None:
        yaml_str = """
kind: workflow
id: test-bad-type
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
    compensate:
      type: gate
      condition: always_true
"""
        with pytest.raises(ValueError, match="compensate type must be 'runner' or 'llm'"):
            load_definition(yaml_str)

    def test_llm_compensate_parsed(self) -> None:
        yaml_str = """
kind: workflow
id: test-llm-comp
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
    compensate:
      type: llm
      prompt: "Undo the deployment"
"""
        defn = load_definition(yaml_str)
        comp = defn.steps[0].compensate
        assert comp is not None
        assert comp.type == "llm"
        assert comp.prompt == "Undo the deployment"

    def test_compensate_not_mapping_rejected(self) -> None:
        yaml_str = """
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
    compensate: "not a mapping"
"""
        with pytest.raises(ValueError, match="compensate.*must be a mapping"):
            load_definition(yaml_str)

    def test_compensate_type_restriction(self) -> None:
        for bad_type in ("gate", "loop", "parallel", "human_gate", "publish"):
            yaml_str = f"""
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
    compensate:
      type: {bad_type}
      condition: always_true
"""
            with pytest.raises(ValueError, match="compensate type must be 'runner' or 'llm'"):
                load_definition(yaml_str)


# ---------------------------------------------------------------------------
# Queue building tests
# ---------------------------------------------------------------------------


class TestBuildCompensateLookup:
    def test_top_level_steps(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        lookup = _build_compensate_lookup(defn)
        assert "deploy" in lookup
        assert "verify" not in lookup
        assert lookup["deploy"].id == "deploy_compensate"

    def test_branch_steps_qualified_ids(self) -> None:
        defn = load_definition(_yaml_with_branch_compensate())
        lookup = _build_compensate_lookup(defn)
        assert "b1/s1" in lookup
        assert "b2/s2" not in lookup
        assert lookup["b1/s1"].command == "echo undo s1"

    def test_loop_steps(self) -> None:
        yaml_str = """
kind: workflow
id: test-loop
version: "1"
steps:
  - id: retry_loop
    type: loop
    max_rounds: 3
    steps:
      - id: attempt
        type: runner
        runner: shell
        command: "echo try"
        compensate:
          type: runner
          runner: shell
          command: "echo undo"
"""
        defn = load_definition(yaml_str)
        lookup = _build_compensate_lookup(defn)
        assert "attempt" in lookup

    def test_empty_when_no_compensate(self) -> None:
        yaml_str = """
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
"""
        defn = load_definition(yaml_str)
        lookup = _build_compensate_lookup(defn)
        assert len(lookup) == 0


class TestBuildCompensationQueue:
    def test_only_completed_steps_with_compensate(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        db = MagicMock()
        now = datetime.now(timezone.utc).isoformat()

        step_rows = [
            {
                "step_id": "deploy",
                "status": "completed",
                "is_compensation": 0,
                "completed_at": now,
                "branch_id": None,
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
            {
                "step_id": "verify",
                "status": "failed",
                "is_compensation": 0,
                "completed_at": now,
                "branch_id": None,
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
        ]

        with patch(f"{WS_MOD}.list_workflow_steps", return_value=step_rows):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 1
        assert queue[0]["original_step_id"] == "deploy"
        assert queue[0]["compensate_step_id"] == "deploy_compensate"

    def test_reverse_chronological_order(self) -> None:
        defn = load_definition(_yaml_two_compensate())
        db = MagicMock()

        step_rows = [
            {
                "step_id": "step1",
                "status": "completed",
                "is_compensation": 0,
                "completed_at": "2024-01-01T00:00:00",
                "branch_id": None,
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
            {
                "step_id": "step2",
                "status": "completed",
                "is_compensation": 0,
                "completed_at": "2024-01-01T00:01:00",
                "branch_id": None,
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
        ]

        with patch(f"{WS_MOD}.list_workflow_steps", return_value=step_rows):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 2
        assert queue[0]["original_step_id"] == "step2"
        assert queue[1]["original_step_id"] == "step1"

    def test_empty_queue_when_no_compensate_blocks(self) -> None:
        yaml_str = """
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
"""
        defn = load_definition(yaml_str)
        db = MagicMock()

        with patch(
            f"{WS_MOD}.list_workflow_steps",
            return_value=[
                {
                    "step_id": "step1",
                    "status": "completed",
                    "is_compensation": 0,
                    "completed_at": "2024-01-01T00:00:00",
                    "branch_id": None,
                    "result_artifacts_json": None,
                    "result_findings_json": None,
                },
            ],
        ):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 0

    def test_excludes_compensation_steps(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        db = MagicMock()

        step_rows = [
            {
                "step_id": "deploy",
                "status": "completed",
                "is_compensation": 0,
                "completed_at": "2024-01-01T00:00:00",
                "branch_id": None,
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
            {
                "step_id": "deploy_compensate",
                "status": "completed",
                "is_compensation": 1,
                "completed_at": "2024-01-01T00:01:00",
                "branch_id": None,
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
        ]

        with patch(f"{WS_MOD}.list_workflow_steps", return_value=step_rows):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 1
        assert queue[0]["original_step_id"] == "deploy"

    def test_branch_qualified_ids(self) -> None:
        defn = load_definition(_yaml_with_branch_compensate())
        db = MagicMock()

        step_rows = [
            {
                "step_id": "s1",
                "status": "completed",
                "is_compensation": 0,
                "completed_at": "2024-01-01T00:00:00",
                "branch_id": "b1",
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
            {
                "step_id": "s2",
                "status": "completed",
                "is_compensation": 0,
                "completed_at": "2024-01-01T00:00:00",
                "branch_id": "b2",
                "result_artifacts_json": None,
                "result_findings_json": None,
            },
        ]

        with patch(f"{WS_MOD}.list_workflow_steps", return_value=step_rows):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 1
        assert queue[0]["original_step_id"] == "s1"
        assert queue[0]["branch_id"] == "b1"

    def test_no_completed_steps_empty_queue(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        db = MagicMock()

        with patch(f"{WS_MOD}.list_workflow_steps", return_value=[]):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 0

    def test_fail_on_first_step_no_compensation(self) -> None:
        defn = load_definition(_yaml_with_compensate())
        db = MagicMock()

        with patch(
            f"{WS_MOD}.list_workflow_steps",
            return_value=[
                {
                    "step_id": "deploy",
                    "status": "failed",
                    "is_compensation": 0,
                    "completed_at": None,
                    "branch_id": None,
                    "result_artifacts_json": None,
                    "result_findings_json": None,
                },
            ],
        ):
            queue = _build_compensation_queue(db, "run-1", defn)

        assert len(queue) == 0


# ---------------------------------------------------------------------------
# Terminal status tests
# ---------------------------------------------------------------------------


class TestTerminalStatuses:
    def test_compensated_is_terminal(self) -> None:
        from anteroom.services.workflow_storage import _TERMINAL_RUN_STATUSES

        assert "compensated" in _TERMINAL_RUN_STATUSES

    def test_compensation_failed_is_terminal(self) -> None:
        from anteroom.services.workflow_storage import _TERMINAL_RUN_STATUSES

        assert "compensation_failed" in _TERMINAL_RUN_STATUSES

    def test_compensating_is_valid(self) -> None:
        from anteroom.services.workflow_storage import _VALID_RUN_STATUSES

        assert "compensating" in _VALID_RUN_STATUSES

    def test_compensated_is_valid(self) -> None:
        from anteroom.services.workflow_storage import _VALID_RUN_STATUSES

        assert "compensated" in _VALID_RUN_STATUSES

    def test_compensation_failed_is_valid(self) -> None:
        from anteroom.services.workflow_storage import _VALID_RUN_STATUSES

        assert "compensation_failed" in _VALID_RUN_STATUSES

    def test_compensating_not_terminal(self) -> None:
        from anteroom.services.workflow_storage import _TERMINAL_RUN_STATUSES

        assert "compensating" not in _TERMINAL_RUN_STATUSES


# ---------------------------------------------------------------------------
# Execution tests
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def _patch_ws_for_execution(overrides: dict[str, Any] | None = None):
    """Patch ws functions for compensation execution tests. Yields dict of mock objects."""
    defaults = {
        "update_workflow_run": MagicMock(return_value={"id": "run-1", "status": "compensating"}),
        "get_workflow_run": MagicMock(
            return_value={
                "id": "run-1",
                "status": "compensating",
                "budget_usage": {"steps_completed": 0, "total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0},
            }
        ),
        "create_workflow_step": MagicMock(
            return_value={
                "id": "step-rec-1",
                "run_id": "run-1",
                "step_id": "deploy_compensate",
                "step_type": "runner",
                "runner_type": "shell",
                "status": "pending",
                "attempt": 1,
                "is_compensation": 1,
            }
        ),
        "update_workflow_step": MagicMock(return_value=None),
        "create_checkpoint": MagicMock(return_value={"id": "cp-1"}),
        "create_workflow_event": MagicMock(return_value=None),
    }
    if overrides:
        defaults.update(overrides)

    with contextlib.ExitStack() as stack:
        mocks = {}
        for name, mock_obj in defaults.items():
            m = stack.enter_context(patch(f"{WS_MOD}.{name}", mock_obj))
            mocks[name] = m
        yield mocks


class TestExecuteCompensation:
    @pytest.mark.asyncio
    async def test_all_succeed_compensated(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_with_compensate())

        comp_def = defn.steps[0].compensate
        assert comp_def is not None
        queue = [
            {
                "original_step_id": "deploy",
                "compensate_step_id": "deploy_compensate",
                "compensate_def": comp_def,
                "branch_id": None,
            }
        ]
        run = {"id": "run-1", "status": "failed", "params": None, "inputs": None}

        mock_result = MagicMock(
            status="success",
            summary="Rolled back",
            artifacts={},
            findings=[],
            raw_output_path=None,
        )

        with _patch_ws_for_execution() as mocks:
            with patch.object(engine, "_execute_runner_step", return_value=mock_result):
                await engine._execute_compensation(run, queue, defn, {}, {})

            update_calls = mocks["update_workflow_run"].call_args_list
            statuses = [c.kwargs.get("status") for c in update_calls if c.kwargs.get("status")]
            assert "compensated" in statuses

    @pytest.mark.asyncio
    async def test_one_fails_compensation_failed(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_with_compensate())

        comp_def = defn.steps[0].compensate
        assert comp_def is not None
        queue = [
            {
                "original_step_id": "deploy",
                "compensate_step_id": "deploy_compensate",
                "compensate_def": comp_def,
                "branch_id": None,
            }
        ]
        run = {"id": "run-1", "status": "failed", "params": None, "inputs": None}

        with _patch_ws_for_execution() as mocks:
            with patch.object(engine, "_execute_runner_step", side_effect=RuntimeError("boom")):
                await engine._execute_compensation(run, queue, defn, {}, {})

            update_calls = mocks["update_workflow_run"].call_args_list
            statuses = [c.kwargs.get("status") for c in update_calls if c.kwargs.get("status")]
            assert "compensation_failed" in statuses

    @pytest.mark.asyncio
    async def test_best_effort_continues_on_failure(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_two_compensate())

        queue = [
            {
                "original_step_id": "step2",
                "compensate_step_id": "step2_compensate",
                "compensate_def": defn.steps[1].compensate,
                "branch_id": None,
            },
            {
                "original_step_id": "step1",
                "compensate_step_id": "step1_compensate",
                "compensate_def": defn.steps[0].compensate,
                "branch_id": None,
            },
        ]
        run = {"id": "run-1", "status": "failed", "params": None, "inputs": None}

        call_count = 0

        async def mock_runner(step_def: Any, *args: Any, **kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("first fails")
            return MagicMock(status="success", summary="OK", artifacts={}, findings=[], raw_output_path=None)

        with _patch_ws_for_execution():
            with patch.object(engine, "_execute_runner_step", side_effect=mock_runner):
                await engine._execute_compensation(run, queue, defn, {}, {})

        assert call_count == 2

    @pytest.mark.asyncio
    async def test_empty_queue_not_called(self) -> None:
        defn = load_definition("""
kind: workflow
id: test
version: "1"
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo deploy"
""")
        lookup = _build_compensate_lookup(defn)
        assert len(lookup) == 0


# ---------------------------------------------------------------------------
# Events tests
# ---------------------------------------------------------------------------


class TestCompensationEvents:
    @pytest.mark.asyncio
    async def test_compensation_started_event(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_with_compensate())

        comp_def = defn.steps[0].compensate
        assert comp_def is not None
        queue = [
            {
                "original_step_id": "deploy",
                "compensate_step_id": "deploy_compensate",
                "compensate_def": comp_def,
                "branch_id": None,
            }
        ]
        run = {"id": "run-1", "status": "failed", "params": None, "inputs": None}

        emitted_events: list[str] = []

        async def track_emit(run_id: str, event_type: str, **kwargs: Any) -> None:
            emitted_events.append(event_type)

        mock_result = MagicMock(status="success", summary="OK", artifacts={}, findings=[], raw_output_path=None)

        with _patch_ws_for_execution():
            with patch.object(engine, "_emit_event", side_effect=track_emit):
                with patch.object(engine, "_execute_runner_step", return_value=mock_result):
                    await engine._execute_compensation(run, queue, defn, {}, {})

        assert "compensation_started" in emitted_events
        assert "compensation_step_completed" in emitted_events
        assert "run_compensated" in emitted_events

    @pytest.mark.asyncio
    async def test_compensation_failed_events(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_with_compensate())

        comp_def = defn.steps[0].compensate
        assert comp_def is not None
        queue = [
            {
                "original_step_id": "deploy",
                "compensate_step_id": "deploy_compensate",
                "compensate_def": comp_def,
                "branch_id": None,
            }
        ]
        run = {"id": "run-1", "status": "failed", "params": None, "inputs": None}

        emitted_events: list[str] = []

        async def track_emit(run_id: str, event_type: str, **kwargs: Any) -> None:
            emitted_events.append(event_type)

        with _patch_ws_for_execution():
            with patch.object(engine, "_emit_event", side_effect=track_emit):
                with patch.object(engine, "_execute_runner_step", side_effect=RuntimeError("boom")):
                    await engine._execute_compensation(run, queue, defn, {}, {})

        assert "compensation_started" in emitted_events
        assert "compensation_step_failed" in emitted_events
        assert "run_compensation_failed" in emitted_events


# ---------------------------------------------------------------------------
# Resume tests
# ---------------------------------------------------------------------------


class TestResumeFromCompensating:
    @pytest.mark.asyncio
    async def test_compensating_is_resumable(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_with_compensate())

        run = {
            "id": "run-1",
            "status": "compensating",
            "target_kind": "generic",
            "target_ref": "test",
            "definition_hash": defn.content_hash,
            "params": None,
            "inputs": None,
            "budget_usage": None,
        }

        overrides = {
            "get_workflow_run": MagicMock(return_value=run),
            "acquire_lock": MagicMock(return_value=True),
            "release_lock": MagicMock(return_value=True),
            "list_completed_step_ids": MagicMock(return_value=set()),
            "list_workflow_steps": MagicMock(
                return_value=[
                    {
                        "step_id": "deploy",
                        "status": "completed",
                        "is_compensation": 0,
                        "completed_at": "2024-01-01T00:00:00",
                        "branch_id": None,
                        "result_artifacts_json": None,
                        "result_findings_json": None,
                        "result_status": "success",
                        "result_summary": "OK",
                    },
                ]
            ),
            "list_checkpoints": MagicMock(
                return_value=[
                    {
                        "label": "compensation_queue",
                        "step_results": {"queue": ["deploy"], "completed": [], "failed": []},
                        "budget_usage": None,
                    }
                ]
            ),
        }

        mock_result = MagicMock(status="success", summary="OK", artifacts={}, findings=[], raw_output_path=None)

        with _patch_ws_for_execution(overrides) as mocks:
            with patch.object(engine, "_execute_runner_step", return_value=mock_result):
                with patch.object(engine, "_heartbeat_loop", return_value=AsyncMock()):
                    await engine.resume_run("run-1", defn)

            mocks["release_lock"].assert_called()


# ---------------------------------------------------------------------------
# Stale recovery tests
# ---------------------------------------------------------------------------


class TestStaleRecovery:
    def test_find_stale_compensating_runs(self) -> None:
        from anteroom.services.workflow_storage import find_stale_runs

        db = MagicMock()
        db.execute_fetchall.return_value = [
            {
                "id": "run-1",
                "workflow_id": "wf",
                "workflow_version": "1",
                "status": "compensating",
                "target_kind": "generic",
                "target_ref": "test",
                "current_step_id": None,
                "attempt_count": 0,
                "stop_reason": None,
                "inputs_json": None,
                "params_json": None,
                "space_id": None,
                "created_at": "2024-01-01",
                "updated_at": "2024-01-01",
                "started_at": None,
                "completed_at": None,
                "heartbeat_at": "2024-01-01T00:00:00",
                "definition_hash": None,
                "definition_content": None,
                "budget_json": None,
                "budget_usage_json": None,
                "trigger_source": None,
                "trigger_meta_json": None,
                "claimed_by": None,
                "claimed_at": None,
            }
        ]
        runs = find_stale_runs(db, 60)
        assert len(runs) == 1
        assert runs[0]["status"] == "compensating"

        call_args = db.execute_fetchall.call_args
        sql = call_args[0][0]
        assert "compensating" in sql

    @pytest.mark.asyncio
    async def test_recover_compensating_transitions_to_paused(self) -> None:
        engine = _make_engine()

        fake_run = {"id": "run-1", "status": "paused", "stop_reason": "stale_heartbeat_reclaimed_during_compensation"}
        with patch(
            f"{WS_MOD}.reclaim_stale_locks",
            return_value=[("run-1", "target-ref", True)],
        ):
            with patch(f"{WS_MOD}.get_workflow_run", return_value=fake_run):
                with patch(f"{WS_MOD}.create_workflow_event"):
                    recovered = await engine.recover_interrupted_runs()

        assert len(recovered) == 1
        assert recovered[0]["status"] == "paused"
        assert "during_compensation" in recovered[0]["stop_reason"]


# ---------------------------------------------------------------------------
# Budget tests
# ---------------------------------------------------------------------------


class TestBudgetDuringCompensation:
    @pytest.mark.asyncio
    async def test_compensation_updates_budget_not_blocked(self) -> None:
        engine = _make_engine()
        defn = load_definition(_yaml_with_compensate())

        comp_def = defn.steps[0].compensate
        assert comp_def is not None
        queue = [
            {
                "original_step_id": "deploy",
                "compensate_step_id": "deploy_compensate",
                "compensate_def": comp_def,
                "branch_id": None,
            }
        ]
        run = {
            "id": "run-1",
            "status": "failed",
            "budget": {"max_steps": 1},
            "budget_usage": {"steps_completed": 5, "total_tokens": 10000},
            "params": None,
            "inputs": None,
        }

        mock_result = MagicMock(
            status="success",
            summary="OK",
            artifacts={"total_tokens": 500, "prompt_tokens": 200, "completion_tokens": 300},
            findings=[],
            raw_output_path=None,
        )

        with _patch_ws_for_execution() as mocks:
            with patch.object(engine, "_execute_runner_step", return_value=mock_result):
                await engine._execute_compensation(run, queue, defn, {}, {})

            update_calls = mocks["update_workflow_run"].call_args_list
            statuses = [c.kwargs.get("status") for c in update_calls if c.kwargs.get("status")]
            assert "compensated" in statuses


# ---------------------------------------------------------------------------
# Storage tests
# ---------------------------------------------------------------------------


class TestStorageChanges:
    def test_create_workflow_step_with_is_compensation(self) -> None:
        from anteroom.services.workflow_storage import create_workflow_step

        db = MagicMock()
        db.execute = MagicMock()
        db.commit = MagicMock()

        result = create_workflow_step(
            db,
            run_id="run-1",
            step_id="comp_step",
            step_type="runner",
            runner_type="shell",
            is_compensation=1,
        )
        assert result["is_compensation"] == 1

        call_args = db.execute.call_args
        sql = call_args[0][0]
        assert "is_compensation" in sql

    def test_list_compensation_steps(self) -> None:
        from anteroom.services.workflow_storage import list_compensation_steps

        db = MagicMock()
        db.execute_fetchall.return_value = [
            {
                "id": "s1",
                "run_id": "run-1",
                "step_id": "comp",
                "step_type": "runner",
                "runner_type": "shell",
                "status": "completed",
                "attempt": 1,
                "result_status": "success",
                "result_summary": "OK",
                "result_artifacts_json": None,
                "result_findings_json": None,
                "raw_output_path": None,
                "duration_ms": 100,
                "idempotency_key": None,
                "branch_id": None,
                "is_compensation": 1,
                "created_at": "2024-01-01",
                "started_at": "2024-01-01",
                "completed_at": "2024-01-01",
            }
        ]

        steps = list_compensation_steps(db, "run-1")
        assert len(steps) == 1

        call_args = db.execute_fetchall.call_args
        sql = call_args[0][0]
        assert "is_compensation = 1" in sql
