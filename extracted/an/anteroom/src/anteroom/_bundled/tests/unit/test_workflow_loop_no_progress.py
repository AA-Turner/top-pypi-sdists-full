"""Tests for loop no-progress detection (#1152).

Validates:
- stop_after_unchanged: repeated failure signature stops loop early
- Signature computation from failure_triage and fallback to summary
- Priority order: break_when/until win over no-progress
- Validation: stop_after_unchanged only on loops, minimum 2
- Progress resets counter when failure changes
- All-success rounds don't trigger no-progress
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    WorkflowStepDef,
    _compute_round_signature,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import RunnerResult, create_default_registry
from anteroom.services.workflow_storage import list_workflow_steps

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

    register_gate_condition("always_pass", always_pass)
    yield


# ---------------------------------------------------------------------------
# YAML templates
# ---------------------------------------------------------------------------

LOOP_STOP_AFTER_UNCHANGED = """\
kind: workflow
id: no_progress_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    stop_after_unchanged: 2
    steps:
      - id: fix_code
        type: runner
        runner: shell
        command: "echo fixing"
      - id: run_tests
        type: runner
        runner: shell
        command: "echo testing"
"""

LOOP_STOP_AFTER_UNCHANGED_3 = """\
kind: workflow
id: no_progress_test_3
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 6
    stop_after_unchanged: 3
    steps:
      - id: fix_code
        type: runner
        runner: shell
        command: "echo fixing"
      - id: run_tests
        type: runner
        runner: shell
        command: "echo testing"
"""

LOOP_STOP_WITH_UNTIL = """\
kind: workflow
id: no_progress_until_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    stop_after_unchanged: 2
    until:
      step: run_tests
      field: result_status
      equals: success
    steps:
      - id: fix_code
        type: runner
        runner: shell
        command: "echo fixing"
      - id: run_tests
        type: runner
        runner: shell
        command: "echo testing"
"""

LOOP_STOP_WITH_BREAK_WHEN = """\
kind: workflow
id: no_progress_break_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    stop_after_unchanged: 2
    break_when:
      step: run_tests
      field: result_status
      equals: success
    steps:
      - id: fix_code
        type: runner
        runner: shell
        command: "echo fixing"
      - id: run_tests
        type: runner
        runner: shell
        command: "echo testing"
"""


# ---------------------------------------------------------------------------
# Tests: stop_after_unchanged detection
# ---------------------------------------------------------------------------


class TestNoProgressDetection:
    @pytest.mark.asyncio
    async def test_same_failure_stops_after_threshold(self, db: Any, engine: WorkflowEngine) -> None:
        """Same failure N times → stops at round N with loop_end_reason: no_progress."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="tests failed: assert x == 1")
            return RunnerResult(status="success", summary="fixed")

        defn = load_definition(LOOP_STOP_AFTER_UNCHANGED)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        assert len(loop_step) == 1
        assert loop_step[0]["result_status"] == "failed"
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "no_progress"
        assert "no progress" in loop_step[0].get("result_summary", "").lower()

    @pytest.mark.asyncio
    async def test_below_threshold_does_not_stop_early(self, db: Any, engine: WorkflowEngine) -> None:
        """Same failure (N-1) times → does NOT stop early, exhausts normally."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                # Change failure on rounds to prevent hitting threshold=3
                # Round 1: fail A, Round 2: fail B, Round 3: fail A, ...
                round_num = (call_count + 1) // 2  # 2 steps per round
                if round_num % 2 == 0:
                    return RunnerResult(status="failed", summary="tests failed: different error")
                return RunnerResult(status="failed", summary="tests failed: original error")
            return RunnerResult(status="success", summary="fixed")

        defn = load_definition(LOOP_STOP_AFTER_UNCHANGED_3)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        # Should exhaust all rounds without no-progress (alternating failures reset counter)
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") != "no_progress"

    @pytest.mark.asyncio
    async def test_progress_resets_counter(self, db: Any, engine: WorkflowEngine) -> None:
        """Failure changes mid-loop → counter resets, doesn't stop early."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                round_num = (call_count + 1) // 2
                if round_num <= 2:
                    return RunnerResult(status="failed", summary="error A")
                return RunnerResult(status="failed", summary="error B")
            return RunnerResult(status="success", summary="fixed")

        defn = load_definition(LOOP_STOP_AFTER_UNCHANGED_3)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        artifacts = loop_step[0].get("result_artifacts") or {}
        # Counter resets when error changes at round 3; error B repeats rounds 3-6 → hits threshold at round 5
        assert artifacts.get("loop_end_reason") == "no_progress"

    @pytest.mark.asyncio
    async def test_all_success_does_not_trigger(self, db: Any, engine: WorkflowEngine) -> None:
        """All rounds succeed → no no-progress, succeeds with all_succeeded."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(LOOP_STOP_AFTER_UNCHANGED)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "all_succeeded"


class TestNoProgressPriority:
    @pytest.mark.asyncio
    async def test_until_wins_over_no_progress(self, db: Any, engine: WorkflowEngine) -> None:
        """until fires on same round as unchanged threshold → success, not failure.

        With threshold=2 and same failure on rounds 1 and 2, the counter hits 2
        on round 2. If until also fires on round 2, until must win.
        We achieve this by having run_tests succeed on round 2 (until checks
        run_tests.result_status == success). fix_code still fails, so the
        round is not all_succeeded, but until is satisfied.
        """
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                round_num = (call_count + 1) // 2
                if round_num < 2:
                    return RunnerResult(status="failed", summary="tests failed")
                return RunnerResult(status="success", summary="tests passed")
            # fix_code always fails — keeps all_succeeded false and signature stable
            return RunnerResult(status="failed", summary="fix failed")

        defn = load_definition(LOOP_STOP_WITH_UNTIL)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "until_met"

    @pytest.mark.asyncio
    async def test_break_when_wins_over_no_progress(self, db: Any, engine: WorkflowEngine) -> None:
        """break_when fires on same round as unchanged threshold → success, not failure.

        break_when checks run_tests.result_status == success. On round 2
        run_tests succeeds, matching break_when, while the unchanged counter
        also hits 2 from fix_code failures.
        """
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                round_num = (call_count + 1) // 2
                if round_num < 2:
                    return RunnerResult(status="failed", summary="tests failed")
                return RunnerResult(status="success", summary="tests passed")
            return RunnerResult(status="failed", summary="fix failed")

        defn = load_definition(LOOP_STOP_WITH_BREAK_WHEN)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "break_when"

    @pytest.mark.asyncio
    async def test_no_progress_fires_before_exhaustion(self, db: Any, engine: WorkflowEngine) -> None:
        """No-progress fires before rounds exhaust."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="same error every time")
            return RunnerResult(status="success", summary="fixed")

        defn = load_definition(LOOP_STOP_AFTER_UNCHANGED)  # 5 rounds, threshold 2

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "no_progress"
        # Should stop at round 2, not 5
        assert artifacts.get("rounds_completed") == 2


class TestNoProgressValidation:
    def test_stop_after_unchanged_on_non_loop_raises(self) -> None:
        yaml = """\
kind: workflow
id: bad_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: my_step
    type: runner
    runner: shell
    command: "echo hello"
    stop_after_unchanged: 3
"""
        with pytest.raises(ValueError, match="only allowed on loop steps"):
            load_definition(yaml)

    def test_stop_after_unchanged_value_1_raises(self) -> None:
        yaml = """\
kind: workflow
id: bad_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    stop_after_unchanged: 1
    steps:
      - id: run_tests
        type: runner
        runner: shell
        command: "echo testing"
"""
        with pytest.raises(ValueError, match="must be an integer >= 2"):
            load_definition(yaml)

    def test_stop_after_unchanged_value_0_raises(self) -> None:
        yaml = """\
kind: workflow
id: bad_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    stop_after_unchanged: 0
    steps:
      - id: run_tests
        type: runner
        runner: shell
        command: "echo testing"
"""
        with pytest.raises(ValueError, match="must be an integer >= 2"):
            load_definition(yaml)


class TestComputeRoundSignature:
    def test_uses_failure_signature_when_available(self) -> None:
        nested_steps = [WorkflowStepDef(id="test", type="runner")]
        step_results = {
            "test": {
                "result_status": "failed",
                "result_summary": "tests failed",
                "result_artifacts": {"failure_triage": {"failure_signature": "abc123"}},
            }
        }
        sig = _compute_round_signature(step_results, nested_steps)
        assert sig  # non-empty
        # Should be deterministic
        assert sig == _compute_round_signature(step_results, nested_steps)

    def test_falls_back_to_summary(self) -> None:
        nested_steps = [WorkflowStepDef(id="test", type="runner")]
        step_results = {
            "test": {
                "result_status": "failed",
                "result_summary": "some error message",
                "result_artifacts": {},
            }
        }
        sig = _compute_round_signature(step_results, nested_steps)
        assert sig

    def test_different_failures_produce_different_signatures(self) -> None:
        nested_steps = [WorkflowStepDef(id="test", type="runner")]
        results_a = {
            "test": {
                "result_status": "failed",
                "result_summary": "error A",
                "result_artifacts": {},
            }
        }
        results_b = {
            "test": {
                "result_status": "failed",
                "result_summary": "error B",
                "result_artifacts": {},
            }
        }
        sig_a = _compute_round_signature(results_a, nested_steps)
        sig_b = _compute_round_signature(results_b, nested_steps)
        assert sig_a != sig_b

    def test_empty_summary_still_produces_signature(self) -> None:
        nested_steps = [WorkflowStepDef(id="test", type="runner")]
        step_results = {
            "test": {
                "result_status": "failed",
                "result_summary": "",
                "result_artifacts": {},
            }
        }
        sig = _compute_round_signature(step_results, nested_steps)
        assert sig


class TestRoundsCompletedInCheckpoint:
    def test_rounds_completed_survives_sanitization(self) -> None:
        """rounds_completed must be in _SAFE_ARTIFACT_KEYS so it survives checkpoint."""
        step_results = {
            "repair_loop": {
                "result_status": "failed",
                "result_summary": "no progress",
                "result_artifacts": {
                    "loop_end_reason": "no_progress",
                    "rounds_completed": 2,
                },
            }
        }
        sanitized = WorkflowEngine._sanitize_checkpoint_data(step_results)
        arts = sanitized["repair_loop"]["result_artifacts"]
        assert arts["rounds_completed"] == 2
        assert arts["loop_end_reason"] == "no_progress"
