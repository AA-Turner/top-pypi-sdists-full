"""Tests for on_failure branches (#1127) and retry_on_result (#1129)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import RunnerResult, create_default_registry
from anteroom.services.workflow_storage import list_workflow_events, list_workflow_steps


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


@pytest.fixture(autouse=True)
def _register_test_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


# ---------------------------------------------------------------------------
# YAML fixtures
# ---------------------------------------------------------------------------

ON_FAILURE_BASIC = """\
kind: workflow
id: on_failure_test
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "echo testing"
    on_failure:
      - id: collect_logs
        type: runner
        runner: shell
        command: "echo collecting logs"
      - id: notify
        type: runner
        runner: shell
        command: "echo notifying"
  - id: deploy
    type: runner
    runner: shell
    command: "echo deploying"
"""

ON_FAILURE_BRANCH_FAILS = """\
kind: workflow
id: on_failure_branch_fail
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "echo testing"
    on_failure:
      - id: bad_handler
        type: runner
        runner: shell
        command: "echo handler fails"
  - id: deploy
    type: runner
    runner: shell
    command: "echo deploying"
"""

ON_FAILURE_WITH_CONTINUE = """\
kind: workflow
id: on_failure_continue
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "echo testing"
    on_failure:
      - id: collect_logs
        type: runner
        runner: shell
        command: "echo logs"
    continue_on: [failed]
  - id: deploy
    type: runner
    runner: shell
    command: "echo deploying"
"""

RETRY_ON_RESULT = """\
kind: workflow
id: retry_on_result_test
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo generating"
    retry:
      max_attempts: 3
      backoff: fixed
      initial_delay: 0.01
      retry_on_result:
        - field: result_artifacts.exit_code
          not_equals: "0"
"""


# ---------------------------------------------------------------------------
# Tests: on_failure (#1127)
# ---------------------------------------------------------------------------


class TestOnFailureBranch:
    @pytest.mark.asyncio
    async def test_branch_runs_on_failure_and_continues(self, db: Any, engine: WorkflowEngine) -> None:
        """Step fails, on_failure branch succeeds → run continues to next step."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="tests failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_BASIC)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert "run_tests/_fail/collect_logs" in step_ids
        assert "run_tests/_fail/notify" in step_ids
        assert "deploy" in step_ids

    @pytest.mark.asyncio
    async def test_branch_fails_aborts_run(self, db: Any, engine: WorkflowEngine) -> None:
        """Step fails, on_failure branch also fails → run aborts."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="tests failed")
            if step_id == "bad_handler":
                return RunnerResult(status="failed", summary="handler failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_BRANCH_FAILS)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert "run_tests/_fail/bad_handler" in step_ids
        assert "deploy" not in step_ids

    @pytest.mark.asyncio
    async def test_branch_not_triggered_on_success(self, db: Any, engine: WorkflowEngine) -> None:
        """Step succeeds → on_failure branch does not run."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_BASIC)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert not any("_fail/" in sid for sid in step_ids)

    @pytest.mark.asyncio
    async def test_branch_step_ids_prefixed(self, db: Any, engine: WorkflowEngine) -> None:
        """Branch step IDs use parent/_fail/child convention."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_BASIC)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        steps = list_workflow_steps(db, run["id"])
        fail_steps = [s for s in steps if "_fail/" in s["step_id"]]
        assert len(fail_steps) == 2
        for s in fail_steps:
            assert s["step_id"].startswith("run_tests/_fail/")

    @pytest.mark.asyncio
    async def test_failure_branch_events_emitted(self, db: Any, engine: WorkflowEngine) -> None:
        """failure_branch_started and failure_branch_completed events emitted."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_BASIC)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        events = list_workflow_events(db, run["id"])
        event_types = [e["event_type"] for e in events]
        assert "failure_branch_started" in event_types
        assert "failure_branch_completed" in event_types

    @pytest.mark.asyncio
    async def test_on_failure_with_continue_on(self, db: Any, engine: WorkflowEngine) -> None:
        """on_failure + continue_on: branch runs, then continue_on allows progression."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_WITH_CONTINUE)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert "run_tests/_fail/collect_logs" in step_ids
        assert "deploy" in step_ids

    @pytest.mark.asyncio
    async def test_on_failure_with_retry_runs_after_exhaustion(self, db: Any, engine: WorkflowEngine) -> None:
        """retry + on_failure: retry first, branch after exhaustion."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="failed")
            return RunnerResult(status="success", summary="ok")

        yaml = """\
kind: workflow
id: retry_then_on_failure
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "echo test"
    retry:
      max_attempts: 2
      backoff: fixed
      initial_delay: 0.01
    on_failure:
      - id: handler
        type: runner
        runner: shell
        command: "echo handle"
  - id: next
    type: runner
    runner: shell
    command: "echo next"
"""
        defn = load_definition(yaml)
        with (
            patch(
                "anteroom.services.workflow_runners.execute_opaque_runner",
                side_effect=mock_runner,
            ),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert "run_tests/_fail/handler" in step_ids
        assert "next" in step_ids
        retry_events = [e for e in list_workflow_events(db, run["id"]) if e["event_type"] == "step_retry"]
        assert len(retry_events) >= 1

    @pytest.mark.asyncio
    async def test_branch_accesses_parent_via_context_from(self, db: Any, engine: WorkflowEngine) -> None:
        """Branch step can reference parent's failure via step_results."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="3 tests failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(ON_FAILURE_BASIC)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"


# ---------------------------------------------------------------------------
# Tests: on_failure validation
# ---------------------------------------------------------------------------


class TestOnFailureValidation:
    def test_nested_on_failure_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: "echo x"
    on_failure:
      - id: handler
        type: runner
        runner: shell
        command: "echo y"
        on_failure:
          - id: nested
            type: runner
            runner: shell
            command: "echo z"
"""
        with pytest.raises(ValueError, match="nested on_failure"):
            load_definition(yaml)

    def test_gate_in_on_failure_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: "echo x"
    on_failure:
      - id: bad_gate
        type: gate
        condition: always_pass
"""
        with pytest.raises(ValueError, match="'runner' or 'llm'"):
            load_definition(yaml)

    def test_on_failure_on_gate_step_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: g1
    type: gate
    condition: always_pass
    on_failure:
      - id: handler
        type: runner
        runner: shell
        command: "echo y"
"""
        with pytest.raises(ValueError, match="not allowed on gate"):
            load_definition(yaml)

    def test_valid_on_failure_accepted(self) -> None:
        defn = load_definition(ON_FAILURE_BASIC)
        assert defn.steps[0].on_failure is not None
        assert len(defn.steps[0].on_failure) == 2


# ---------------------------------------------------------------------------
# Tests: retry_on_result (#1129)
# ---------------------------------------------------------------------------


class TestRetryOnResult:
    @pytest.mark.asyncio
    async def test_result_condition_triggers_retry(self, db: Any, engine: WorkflowEngine) -> None:
        """retry_on_result condition matches → retry triggered."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return RunnerResult(status="success", summary="bad", artifacts={"exit_code": "1"})
            return RunnerResult(status="success", summary="good", artifacts={"exit_code": "0"})

        defn = load_definition(RETRY_ON_RESULT)
        with (
            patch(
                "anteroom.services.workflow_runners.execute_opaque_runner",
                side_effect=mock_runner,
            ),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_result_condition_no_match_accepts(self, db: Any, engine: WorkflowEngine) -> None:
        """retry_on_result condition doesn't match → result accepted."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="good", artifacts={"exit_code": "0"})

        defn = load_definition(RETRY_ON_RESULT)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_retry_reason_in_event_payload(self, db: Any, engine: WorkflowEngine) -> None:
        """step_retry event includes retry_reason: result_condition."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return RunnerResult(status="success", summary="bad", artifacts={"exit_code": "1"})
            return RunnerResult(status="success", summary="good", artifacts={"exit_code": "0"})

        defn = load_definition(RETRY_ON_RESULT)
        with (
            patch(
                "anteroom.services.workflow_runners.execute_opaque_runner",
                side_effect=mock_runner,
            ),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        events = list_workflow_events(db, run["id"])
        retry_events = [e for e in events if e["event_type"] == "step_retry"]
        assert len(retry_events) >= 1
        payload = retry_events[0].get("payload") or {}
        if isinstance(payload, str):
            import json

            payload = json.loads(payload)
        assert payload.get("retry_reason") == "result_condition"

    @pytest.mark.asyncio
    async def test_failed_status_retry_has_reason(self, db: Any, engine: WorkflowEngine) -> None:
        """Existing failed-status retry includes retry_reason: failed_status."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return RunnerResult(status="failed", summary="bad")
            return RunnerResult(status="success", summary="good")

        yaml = """\
kind: workflow
id: failed_retry
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: "echo x"
    retry:
      max_attempts: 2
      backoff: fixed
      initial_delay: 0.01
"""
        defn = load_definition(yaml)
        with (
            patch(
                "anteroom.services.workflow_runners.execute_opaque_runner",
                side_effect=mock_runner,
            ),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        retry_events = [e for e in events if e["event_type"] == "step_retry"]
        assert len(retry_events) >= 1
        payload = retry_events[0].get("payload") or {}
        if isinstance(payload, str):
            import json

            payload = json.loads(payload)
        assert payload.get("retry_reason") == "failed_status"


class TestRetryOnResultValidation:
    def test_retry_on_result_missing_field_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: "echo x"
    retry:
      max_attempts: 2
      retry_on_result:
        - equals: "0"
"""
        with pytest.raises(ValueError, match="missing 'field'"):
            load_definition(yaml)

    def test_retry_on_result_invalid_operator_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: "echo x"
    retry:
      max_attempts: 2
      retry_on_result:
        - field: result_status
          greater_than: 5
"""
        with pytest.raises(ValueError, match="operator"):
            load_definition(yaml)

    def test_valid_retry_on_result_accepted(self) -> None:
        defn = load_definition(RETRY_ON_RESULT)
        assert defn.steps[0].retry is not None
        assert defn.steps[0].retry.get("retry_on_result") is not None
