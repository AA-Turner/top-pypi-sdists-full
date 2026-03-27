"""Tests for loop.until, fail_if_not_met (#1125) and loop.break_when (#1130).

Validates:
- until condition evaluation and early exit
- fail_if_not_met semantics on round exhaustion
- break_when early termination
- loop_end_reason artifact in all outcomes
- Backward compatibility when until/break_when are absent
- Validation errors for invalid configurations
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


def _loop_until_yaml(fail_if_not_met: bool = False) -> str:
    fail_clause = "    fail_if_not_met: true\n" if fail_if_not_met else ""
    return (
        "kind: workflow\n"
        "id: loop_until_test\n"
        "version: 0.1.0\n"
        "inputs: {}\n"
        "policies: {}\n"
        "steps:\n"
        "  - id: repair_loop\n"
        "    type: loop\n"
        "    max_rounds: 5\n"
        "    until:\n"
        "      step: run_tests\n"
        "      field: result_status\n"
        "      equals: success\n" + fail_clause + "    steps:\n"
        "      - id: fix_code\n"
        "        type: runner\n"
        "        runner: shell\n"
        '        command: "echo fixing"\n'
        "      - id: run_tests\n"
        "        type: runner\n"
        "        runner: shell\n"
        '        command: "echo testing"\n'
    )


LOOP_BREAK_WHEN = """\
kind: workflow
id: loop_break_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    break_when:
      step: fix_code
      field: result_summary
      contains: "no changes"
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

LOOP_UNTIL_AND_BREAK = """\
kind: workflow
id: loop_both_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: repair_loop
    type: loop
    max_rounds: 5
    until:
      step: run_tests
      field: result_status
      equals: success
    break_when:
      step: fix_code
      field: result_summary
      contains: "no changes"
    fail_if_not_met: true
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
# Tests: loop.until (#1125)
# ---------------------------------------------------------------------------


class TestLoopUntil:
    @pytest.mark.asyncio
    async def test_until_met_on_round_2(self, db: Any, engine: WorkflowEngine) -> None:
        """Until condition met on round 2 → early exit with success."""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                # Fail on round 1, succeed on round 2
                if call_count <= 2:
                    return RunnerResult(status="failed", summary="tests failed")
                return RunnerResult(status="success", summary="tests passed")
            return RunnerResult(status="success", summary="fixed")

        yaml = _loop_until_yaml()
        defn = load_definition(yaml)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        assert len(loop_step) == 1
        assert loop_step[0]["result_status"] == "success"
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "until_met"
        assert "condition met" in loop_step[0].get("result_summary", "").lower()

    @pytest.mark.asyncio
    async def test_until_not_met_fail_if_not_met_true(self, db: Any, engine: WorkflowEngine) -> None:
        """Until never met + fail_if_not_met → loop fails."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="tests failed")
            return RunnerResult(status="success", summary="fixed")

        yaml = _loop_until_yaml(fail_if_not_met=True)
        defn = load_definition(yaml)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        assert len(loop_step) == 1
        assert loop_step[0]["result_status"] == "failed"
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "until_not_met"

    @pytest.mark.asyncio
    async def test_until_not_met_fail_if_not_met_false(self, db: Any, engine: WorkflowEngine) -> None:
        """Until never met + no fail_if_not_met → loop succeeds (exhausted)."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "run_tests":
                return RunnerResult(status="failed", summary="tests failed")
            return RunnerResult(status="success", summary="fixed")

        yaml = _loop_until_yaml()
        defn = load_definition(yaml)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"]
        assert len(loop_step) == 1
        assert loop_step[0]["result_status"] == "success"
        artifacts = loop_step[0].get("result_artifacts") or {}
        assert artifacts.get("loop_end_reason") == "exhausted"

    @pytest.mark.asyncio
    async def test_until_met_on_round_1(self, db: Any, engine: WorkflowEngine) -> None:
        """Until condition met immediately → only one round."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="passed")

        yaml = _loop_until_yaml()
        defn = load_definition(yaml)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        nested = [s for s in steps if "_r" in s["step_id"]]
        rounds = {s["step_id"].split("_r")[-1] for s in nested}
        assert rounds == {"1"}, "Only round 1 should have executed"

    @pytest.mark.asyncio
    async def test_until_with_dotted_path(self, db: Any, engine: WorkflowEngine) -> None:
        """Until condition using dotted artifact path."""
        yaml = """\
kind: workflow
id: dotted_until
version: 0.1.0
inputs: {}
steps:
  - id: loop
    type: loop
    max_rounds: 3
    until:
      step: check
      field: result_artifacts.exit_code
      equals: "0"
    steps:
      - id: check
        type: runner
        runner: shell
        command: "echo check"
"""
        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return RunnerResult(status="success", summary="fail", artifacts={"exit_code": "1"})
            return RunnerResult(status="success", summary="pass", artifacts={"exit_code": "0"})

        defn = load_definition(yaml)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "loop"][0]
        assert (loop_step.get("result_artifacts") or {}).get("loop_end_reason") == "until_met"

    @pytest.mark.asyncio
    async def test_backward_compat_no_until(self, db: Any, engine: WorkflowEngine) -> None:
        """No until set → legacy all_succeeded behavior still works."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="ok")

        yaml = """\
kind: workflow
id: legacy_loop
version: 0.1.0
inputs: {}
steps:
  - id: loop
    type: loop
    max_rounds: 3
    steps:
      - id: step_a
        type: runner
        runner: shell
        command: "echo a"
"""
        defn = load_definition(yaml)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "loop"][0]
        assert (loop_step.get("result_artifacts") or {}).get("loop_end_reason") == "all_succeeded"


# ---------------------------------------------------------------------------
# Tests: loop.break_when (#1130)
# ---------------------------------------------------------------------------


class TestLoopBreakWhen:
    @pytest.mark.asyncio
    async def test_break_when_met(self, db: Any, engine: WorkflowEngine) -> None:
        """break_when condition met → immediate success."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "fix_code":
                return RunnerResult(status="success", summary="no changes needed")
            return RunnerResult(status="success", summary="passed")

        defn = load_definition(LOOP_BREAK_WHEN)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"][0]
        assert (loop_step.get("result_artifacts") or {}).get("loop_end_reason") == "break_when"
        assert "break_when" in loop_step.get("result_summary", "").lower()

    @pytest.mark.asyncio
    async def test_break_when_not_met_falls_through(self, db: Any, engine: WorkflowEngine) -> None:
        """break_when not met → loop continues to exhaustion."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="some changes made")

        defn = load_definition(LOOP_BREAK_WHEN)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"][0]
        assert (loop_step.get("result_artifacts") or {}).get("loop_end_reason") == "all_succeeded"

    @pytest.mark.asyncio
    async def test_break_when_fires_before_until(self, db: Any, engine: WorkflowEngine) -> None:
        """break_when has higher priority than until — fires first."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "fix_code":
                return RunnerResult(status="success", summary="no changes needed")
            return RunnerResult(status="success", summary="tests passed")

        defn = load_definition(LOOP_UNTIL_AND_BREAK)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"][0]
        assert (loop_step.get("result_artifacts") or {}).get("loop_end_reason") == "break_when"

    @pytest.mark.asyncio
    async def test_until_fires_when_break_not_matched(self, db: Any, engine: WorkflowEngine) -> None:
        """until matched, break_when not matched → until takes effect."""

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            step_id = kwargs.get("step_id", "?")
            if step_id == "fix_code":
                return RunnerResult(status="success", summary="changes made")
            return RunnerResult(status="success", summary="tests passed")

        defn = load_definition(LOOP_UNTIL_AND_BREAK)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        loop_step = [s for s in steps if s["step_id"] == "repair_loop"][0]
        assert (loop_step.get("result_artifacts") or {}).get("loop_end_reason") == "until_met"


# ---------------------------------------------------------------------------
# Tests: Validation
# ---------------------------------------------------------------------------


class TestLoopConditionValidation:
    def test_until_on_non_loop_step_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo hi"
    until:
      step: step1
      field: result_status
      equals: success
"""
        with pytest.raises(ValueError, match="only allowed on loop"):
            load_definition(yaml)

    def test_fail_if_not_met_without_until_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: loop
    type: loop
    max_rounds: 3
    fail_if_not_met: true
    steps:
      - id: s1
        type: runner
        runner: shell
        command: "echo hi"
"""
        with pytest.raises(ValueError, match="requires 'until'"):
            load_definition(yaml)

    def test_until_references_outer_step_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: pre
    type: runner
    runner: shell
    command: "echo pre"
  - id: loop
    type: loop
    max_rounds: 3
    until:
      step: pre
      field: result_status
      equals: success
    steps:
      - id: s1
        type: runner
        runner: shell
        command: "echo hi"
"""
        with pytest.raises(ValueError, match="not a nested step"):
            load_definition(yaml)

    def test_until_with_invalid_operator_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: loop
    type: loop
    max_rounds: 3
    until:
      step: s1
      field: result_status
      greater_than: 5
    steps:
      - id: s1
        type: runner
        runner: shell
        command: "echo hi"
"""
        with pytest.raises(ValueError, match="operator"):
            load_definition(yaml)

    def test_break_when_on_non_loop_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo hi"
    break_when:
      step: step1
      field: result_status
      equals: success
"""
        with pytest.raises(ValueError, match="only allowed on loop"):
            load_definition(yaml)

    def test_break_when_references_outer_step_rejected(self) -> None:
        yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: pre
    type: runner
    runner: shell
    command: "echo pre"
  - id: loop
    type: loop
    max_rounds: 3
    break_when:
      step: pre
      field: result_status
      equals: success
    steps:
      - id: s1
        type: runner
        runner: shell
        command: "echo hi"
"""
        with pytest.raises(ValueError, match="not a nested step"):
            load_definition(yaml)

    def test_valid_until_and_break_when_accepted(self) -> None:
        """Valid combination of until + break_when + fail_if_not_met parses without error."""
        defn = load_definition(LOOP_UNTIL_AND_BREAK)
        loop_step = defn.steps[0]
        assert loop_step.until is not None
        assert loop_step.break_when is not None
        assert loop_step.fail_if_not_met is True
