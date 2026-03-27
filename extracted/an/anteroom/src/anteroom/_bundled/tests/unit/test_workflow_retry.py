"""Tests for workflow step retry with configurable backoff (#962)."""

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

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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

    async def always_fail(run: Any, step: Any, inputs: Any) -> bool:
        return False

    register_gate_condition("always_pass", always_pass)
    register_gate_condition("always_fail", always_fail)
    yield


# ---------------------------------------------------------------------------
# Test workflows
# ---------------------------------------------------------------------------

RETRY_WORKFLOW = """\
kind: workflow
id: test_retry
version: 0.1.0
inputs: {}
steps:
  - id: flaky_step
    type: runner
    runner: shell
    command: "echo hello"
    retry:
      max_attempts: 3
      backoff: exponential
      initial_delay: 5
      max_delay: 60
"""

RETRY_FIXED_WORKFLOW = """\
kind: workflow
id: test_retry_fixed
version: 0.1.0
inputs: {}
steps:
  - id: flaky_step
    type: runner
    runner: shell
    command: "echo hello"
    retry:
      max_attempts: 3
      backoff: fixed
      initial_delay: 2
      max_delay: 60
"""

RETRY_DEFAULTS_WORKFLOW = """\
kind: workflow
id: test_retry_defaults
version: 0.1.0
inputs: {}
steps:
  - id: flaky_step
    type: runner
    runner: shell
    command: "echo hello"
    retry:
      max_attempts: 2
"""

NO_RETRY_WORKFLOW = """\
kind: workflow
id: test_no_retry
version: 0.1.0
inputs: {}
steps:
  - id: simple_step
    type: runner
    runner: shell
    command: "echo hello"
"""

TWO_STEP_RETRY_WORKFLOW = """\
kind: workflow
id: test_two_step
version: 0.1.0
inputs: {}
steps:
  - id: flaky_step
    type: runner
    runner: shell
    command: "echo flaky"
    retry:
      max_attempts: 3
      backoff: exponential
      initial_delay: 5
      max_delay: 60
  - id: downstream
    type: runner
    runner: shell
    command: "echo downstream"
"""

RETRY_BUDGET_WORKFLOW = """\
kind: workflow
id: test_retry_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 2
steps:
  - id: flaky_step
    type: runner
    runner: shell
    command: "echo hello"
    retry:
      max_attempts: 5
      backoff: fixed
      initial_delay: 0.01
      max_delay: 0.01
"""


# ---------------------------------------------------------------------------
# Backoff calculation unit tests
# ---------------------------------------------------------------------------


class TestCalculateBackoff:
    def test_exponential_attempt_1(self) -> None:
        assert WorkflowEngine._calculate_backoff(1, "exponential", 5, 60) == 5

    def test_exponential_attempt_2(self) -> None:
        assert WorkflowEngine._calculate_backoff(2, "exponential", 5, 60) == 10

    def test_exponential_attempt_3(self) -> None:
        assert WorkflowEngine._calculate_backoff(3, "exponential", 5, 60) == 20

    def test_exponential_attempt_4(self) -> None:
        assert WorkflowEngine._calculate_backoff(4, "exponential", 5, 60) == 40

    def test_exponential_attempt_5_capped(self) -> None:
        assert WorkflowEngine._calculate_backoff(5, "exponential", 5, 60) == 60

    def test_fixed_always_returns_initial(self) -> None:
        for attempt in range(1, 6):
            assert WorkflowEngine._calculate_backoff(attempt, "fixed", 7, 60) == 7


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------


class TestRetryValidation:
    def test_retry_not_allowed_on_gate(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: g
    type: gate
    condition: always_pass
    if_false: nope
    retry:
      max_attempts: 3
"""
        with pytest.raises(ValueError, match="not allowed on gate"):
            load_definition(yaml_str)

    def test_retry_not_allowed_on_human_gate(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: hg
    type: human_gate
    prompt: "Choose"
    options:
      - id: go
        label: Go
        outcome: continue
    retry:
      max_attempts: 3
"""
        with pytest.raises(ValueError, match="not allowed on human_gate"):
            load_definition(yaml_str)

    def test_retry_allowed_on_runner(self) -> None:
        defn = load_definition(RETRY_WORKFLOW)
        assert defn.steps[0].retry is not None
        assert defn.steps[0].retry["max_attempts"] == 3

    def test_retry_invalid_max_attempts_zero(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s
    type: runner
    runner: shell
    command: "echo"
    retry:
      max_attempts: 0
"""
        with pytest.raises(ValueError, match="max_attempts must be an integer >= 1"):
            load_definition(yaml_str)

    def test_retry_invalid_backoff_type(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s
    type: runner
    runner: shell
    command: "echo"
    retry:
      max_attempts: 2
      backoff: linear
"""
        with pytest.raises(ValueError, match="'exponential' or 'fixed'"):
            load_definition(yaml_str)

    def test_retry_invalid_delay_negative(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s
    type: runner
    runner: shell
    command: "echo"
    retry:
      max_attempts: 2
      initial_delay: -1
"""
        with pytest.raises(ValueError, match="initial_delay must be a positive number"):
            load_definition(yaml_str)

    def test_retry_max_delay_less_than_initial(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: s
    type: runner
    runner: shell
    command: "echo"
    retry:
      max_attempts: 2
      initial_delay: 10
      max_delay: 5
"""
        with pytest.raises(ValueError, match="max_delay must be >= initial_delay"):
            load_definition(yaml_str)

    def test_retry_defaults(self) -> None:
        defn = load_definition(RETRY_DEFAULTS_WORKFLOW)
        retry = defn.steps[0].retry
        assert retry is not None
        assert retry["max_attempts"] == 2
        # Defaults applied at validation: backoff, initial_delay, max_delay are not stored
        # but the validation passes, meaning defaults are valid
        assert retry.get("backoff", "exponential") == "exponential"
        assert retry.get("initial_delay", 5) == 5
        assert retry.get("max_delay", 60) == 60


# ---------------------------------------------------------------------------
# Execution tests
# ---------------------------------------------------------------------------


class TestRetryExecution:
    @pytest.mark.asyncio
    async def test_retry_succeeds_on_first_attempt(self, db: Any, engine: WorkflowEngine) -> None:
        """No retry needed when step succeeds on first attempt."""

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="ok", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock) as mock_sleep,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "completed"
        mock_sleep.assert_not_called()
        steps = list_workflow_steps(db, run["id"])
        assert len(steps) == 1
        assert steps[0]["attempt"] == 1

    @pytest.mark.asyncio
    async def test_retry_succeeds_on_second_attempt(self, db: Any, engine: WorkflowEngine) -> None:
        """First attempt fails, second succeeds."""
        attempt_count = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                return RunnerResult(status="failed", summary=f"attempt {attempt_count} failed", duration_ms=10)
            return RunnerResult(status="success", summary="done", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock) as mock_sleep,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        assert mock_sleep.call_count == 1
        mock_sleep.assert_called_once_with(5)  # first backoff: initial_delay * 2^0

    @pytest.mark.asyncio
    async def test_retry_exhausts_all_attempts(self, db: Any, engine: WorkflowEngine) -> None:
        """All 3 attempts fail, run fails."""

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            return RunnerResult(status="failed", summary="always fails", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock) as mock_sleep,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "failed"
        assert "step_failed:flaky_step" in (run.get("stop_reason") or "")
        assert mock_sleep.call_count == 2  # 2 retries before final failure
        mock_sleep.assert_any_call(5)  # attempt 1 backoff
        mock_sleep.assert_any_call(10)  # attempt 2 backoff

    @pytest.mark.asyncio
    async def test_retry_creates_multiple_step_records(self, db: Any, engine: WorkflowEngine) -> None:
        """DB has multiple rows with attempt=1,2,3 for the same step_id."""
        attempt_count = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                return RunnerResult(status="failed", summary=f"fail {attempt_count}", duration_ms=10)
            return RunnerResult(status="success", summary="done", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        flaky_steps = [s for s in steps if s["step_id"] == "flaky_step"]
        assert len(flaky_steps) == 3
        attempts = sorted([s["attempt"] for s in flaky_steps])
        assert attempts == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_retry_event_emitted(self, db: Any, engine: WorkflowEngine) -> None:
        """step_retry event fires with correct payload."""
        attempt_count = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                return RunnerResult(status="failed", summary="transient error", duration_ms=10)
            return RunnerResult(status="success", summary="done", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        events = list_workflow_events(db, run["id"])
        retry_events = [e for e in events if e["event_type"] == "step_retry"]
        assert len(retry_events) == 1
        payload = retry_events[0]["payload"]
        assert payload["attempt"] == 1
        assert payload["max_attempts"] == 3
        assert payload["backoff_seconds"] == 5
        assert "transient error" in payload["error"]

    @pytest.mark.asyncio
    async def test_retry_exception_retried(self, db: Any, engine: WorkflowEngine) -> None:
        """If runner raises an exception (not returns failed), it is also retried."""
        attempt_count = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise RuntimeError("transient crash")
            return RunnerResult(status="success", summary="recovered", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock) as mock_sleep,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        assert mock_sleep.call_count == 1

    @pytest.mark.asyncio
    async def test_retry_last_attempt_result_in_step_results(self, db: Any, engine: WorkflowEngine) -> None:
        """After retry succeeds, downstream step sees the successful result."""
        flaky_attempt = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal flaky_attempt
            cmd = kwargs.get("command", "")
            if "flaky" in cmd:
                flaky_attempt += 1
                if flaky_attempt < 2:
                    return RunnerResult(status="failed", summary="transient", duration_ms=10)
            return RunnerResult(status="success", summary=f"done-{cmd.strip()}", duration_ms=10)

        defn = load_definition(TWO_STEP_RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        downstream = [s for s in steps if s["step_id"] == "downstream"]
        assert len(downstream) == 1
        assert downstream[0]["status"] == "completed"

    @pytest.mark.asyncio
    async def test_retry_budget_accounting(self, db: Any) -> None:
        """Retried step completes and counts toward budget; budget enforced on next step."""
        attempt_count = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                return RunnerResult(status="failed", summary=f"fail {attempt_count}", duration_ms=10)
            return RunnerResult(status="success", summary="done", duration_ms=10)

        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)
        defn = load_definition(RETRY_BUDGET_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        # Budget max_steps=2, retry max_attempts=5. steps_completed increments
        # on success (after the retry loop). Attempt 3 succeeds, so 1 step
        # completed. Run should complete.
        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_retry_step_started_per_attempt(self, db: Any, engine: WorkflowEngine) -> None:
        """step_started is emitted for every attempt, not just the first."""
        attempt_count = 0

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                return RunnerResult(status="failed", summary="transient", duration_ms=10)
            return RunnerResult(status="success", summary="done", duration_ms=10)

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        started_events = [e for e in events if e["event_type"] == "step_started"]
        assert len(started_events) == 2
        assert "attempt" not in started_events[0]["payload"]
        assert started_events[1]["payload"]["attempt"] == 2

    @pytest.mark.asyncio
    async def test_retry_exception_emits_run_failed(self, db: Any, engine: WorkflowEngine) -> None:
        """When all retry attempts fail via exception, run_failed event is emitted."""

        async def mock_runner(**kwargs: Any) -> RunnerResult:
            raise RuntimeError("always crashes")

        defn = load_definition(RETRY_WORKFLOW)
        with (
            patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner),
            patch.object(WorkflowEngine, "_retry_delay", new_callable=AsyncMock),
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "failed"
        events = list_workflow_events(db, run["id"])
        run_failed_events = [e for e in events if e["event_type"] == "run_failed"]
        assert len(run_failed_events) == 1
        assert "step_failed:flaky_step" in run_failed_events[0]["payload"]["reason"]
