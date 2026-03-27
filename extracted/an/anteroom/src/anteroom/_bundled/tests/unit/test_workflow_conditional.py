"""Tests for workflow conditional step execution (#959).

Covers the `when` clause on WorkflowStepDef: parsing, validation,
evaluation, and skip behavior during execution.
"""

from __future__ import annotations

import json
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
from anteroom.services.workflow_storage import (
    get_pending_decision,
    list_workflow_events,
    list_workflow_steps,
    resolve_human_decision,
)

# ---------------------------------------------------------------------------
# Test workflow YAML definitions
# ---------------------------------------------------------------------------

WHEN_EQUALS_WORKFLOW = """\
kind: workflow
id: when_equals
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo conditional"
    timeout: 10
    when:
      step: first
      field: result_status
      equals: "success"
"""

WHEN_EQUALS_FALSE_WORKFLOW = """\
kind: workflow
id: when_equals_false
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo should not run"
    timeout: 10
    when:
      step: first
      field: result_status
      equals: "failed"
"""

WHEN_NOT_EQUALS_WORKFLOW = """\
kind: workflow
id: when_not_equals
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo conditional"
    timeout: 10
    when:
      step: first
      field: result_status
      not_equals: "failed"
"""

WHEN_IS_NOT_EMPTY_WORKFLOW = """\
kind: workflow
id: when_is_not_empty
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo has findings"
    timeout: 10
    when:
      step: first
      field: result_findings
      is_not_empty: true
"""

WHEN_IS_EMPTY_WORKFLOW = """\
kind: workflow
id: when_is_empty
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo no findings"
    timeout: 10
    when:
      step: first
      field: result_findings
      is_empty: true
"""

WHEN_CONTAINS_STRING_WORKFLOW = """\
kind: workflow
id: when_contains_string
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo all checks passed"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo post-check"
    timeout: 10
    when:
      step: first
      field: result_summary
      contains: "passed"
"""

WHEN_CONTAINS_LIST_WORKFLOW = """\
kind: workflow
id: when_contains_list
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo has critical"
    timeout: 10
    when:
      step: first
      field: result_findings
      contains: "critical"
"""

CASCADE_SKIP_WORKFLOW = """\
kind: workflow
id: cascade_skip
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_a
    type: runner
    runner: shell
    command: "echo success"
    timeout: 10
  - id: step_b
    type: runner
    runner: shell
    command: "echo should skip"
    timeout: 10
    when:
      step: step_a
      field: result_status
      not_equals: "success"
  - id: step_c
    type: runner
    runner: shell
    command: "echo also skip"
    timeout: 10
    when:
      step: step_b
      field: result_status
      equals: "success"
"""

WHEN_ON_GATE_WORKFLOW = """\
kind: workflow
id: when_on_gate
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: gate_step
    type: gate
    condition: always_pass
    if_false: requirement_not_met
    when:
      step: first
      field: result_status
      equals: "failed"
"""

SKIP_THEN_HUMAN_GATE_WORKFLOW = """\
kind: workflow
id: skip_then_gate
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_a
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: step_b
    type: runner
    runner: shell
    command: "echo should skip"
    timeout: 10
    when:
      step: step_a
      field: result_status
      not_equals: "success"
  - id: step_c
    type: human_gate
    prompt: "Continue?"
    options:
      - id: "yes"
        label: "Yes"
        outcome: continue
"""

WHEN_DOTTED_FIELD_WORKFLOW = """\
kind: workflow
id: when_dotted
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
  - id: second
    type: runner
    runner: shell
    command: "echo has exit code"
    timeout: 10
    when:
      step: first
      field: result_artifacts.exit_code
      equals: 0
"""

# ---------------------------------------------------------------------------
# Invalid workflow definitions for validation tests
# ---------------------------------------------------------------------------

WHEN_INVALID_STEP_REF = """\
kind: workflow
id: invalid_ref
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
    when:
      step: nonexistent
      field: result_status
      equals: "success"
"""

WHEN_INVALID_FIELD = """\
kind: workflow
id: invalid_field
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
  - id: second
    type: runner
    runner: shell
    command: "echo done"
    when:
      step: first
      field: bogus_field
      equals: "success"
"""

WHEN_INVALID_OPERATOR = """\
kind: workflow
id: invalid_op
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
  - id: second
    type: runner
    runner: shell
    command: "echo done"
    when:
      step: first
      field: result_status
      greater_than: 5
"""

WHEN_MISSING_STEP_KEY = """\
kind: workflow
id: missing_step
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
  - id: second
    type: runner
    runner: shell
    command: "echo done"
    when:
      field: result_status
      equals: "success"
"""

WHEN_MISSING_FIELD_KEY = """\
kind: workflow
id: missing_field
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo done"
  - id: second
    type: runner
    runner: shell
    command: "echo done"
    when:
      step: first
      equals: "success"
"""


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
    """Register generic test gate conditions."""

    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    async def always_fail(run: Any, step: Any, inputs: Any) -> bool:
        return False

    register_gate_condition("always_pass", always_pass)
    register_gate_condition("always_fail", always_fail)
    yield


# ---------------------------------------------------------------------------
# Validation tests (load_definition)
# ---------------------------------------------------------------------------


class TestWhenValidation:
    def test_when_invalid_step_reference(self) -> None:
        with pytest.raises(ValueError, match="has not appeared before"):
            load_definition(WHEN_INVALID_STEP_REF)

    def test_when_invalid_field(self) -> None:
        with pytest.raises(ValueError, match="must start with one of"):
            load_definition(WHEN_INVALID_FIELD)

    def test_when_invalid_operator(self) -> None:
        with pytest.raises(ValueError, match="exactly one operator"):
            load_definition(WHEN_INVALID_OPERATOR)

    def test_when_missing_step_key(self) -> None:
        with pytest.raises(ValueError, match="requires a 'step' field"):
            load_definition(WHEN_MISSING_STEP_KEY)

    def test_when_missing_field_key(self) -> None:
        with pytest.raises(ValueError, match="requires a 'field' field"):
            load_definition(WHEN_MISSING_FIELD_KEY)

    def test_when_parsed_on_step(self) -> None:
        defn = load_definition(WHEN_EQUALS_WORKFLOW)
        assert defn.steps[1].when == {
            "step": "first",
            "field": "result_status",
            "equals": "success",
        }

    def test_when_none_by_default(self) -> None:
        defn = load_definition(WHEN_EQUALS_WORKFLOW)
        assert defn.steps[0].when is None


# ---------------------------------------------------------------------------
# Execution tests
# ---------------------------------------------------------------------------


class TestWhenExecution:
    @pytest.mark.asyncio
    async def test_when_equals_true(self, db: Any, engine: WorkflowEngine) -> None:
        """Step executes when result_status equals expected value."""
        defn = load_definition(WHEN_EQUALS_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        assert len(steps) == 2
        assert all(s["status"] == "completed" for s in steps)

    @pytest.mark.asyncio
    async def test_when_equals_false(self, db: Any, engine: WorkflowEngine) -> None:
        """Step is skipped when condition doesn't match."""
        defn = load_definition(WHEN_EQUALS_FALSE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        assert len(steps) == 2
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["first"] == "completed"
        assert statuses["second"] == "skipped"

    @pytest.mark.asyncio
    async def test_when_not_equals(self, db: Any, engine: WorkflowEngine) -> None:
        """not_equals operator: step runs when value differs from operand."""
        defn = load_definition(WHEN_NOT_EQUALS_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "completed"

    @pytest.mark.asyncio
    async def test_when_is_not_empty_with_findings(self, db: Any, engine: WorkflowEngine) -> None:
        """is_not_empty: step runs when findings list is non-empty."""
        defn = load_definition(WHEN_IS_NOT_EMPTY_WORKFLOW)
        mock_result = RunnerResult(
            status="success",
            summary="done",
            artifacts={},
            findings=["issue1", "issue2"],
        )
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            new_callable=AsyncMock,
            return_value=mock_result,
        ):
            run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "completed"

    @pytest.mark.asyncio
    async def test_when_is_not_empty_with_empty(self, db: Any, engine: WorkflowEngine) -> None:
        """is_not_empty: step is skipped when findings list is empty."""
        defn = load_definition(WHEN_IS_NOT_EMPTY_WORKFLOW)
        # Shell runner produces empty findings by default, so no mock needed
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "skipped"

    @pytest.mark.asyncio
    async def test_when_is_empty(self, db: Any, engine: WorkflowEngine) -> None:
        """is_empty: step runs when findings list is empty."""
        defn = load_definition(WHEN_IS_EMPTY_WORKFLOW)
        # Shell runner produces empty findings by default
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "completed"

    @pytest.mark.asyncio
    async def test_when_contains_string(self, db: Any, engine: WorkflowEngine) -> None:
        """contains: substring match on result_summary."""
        defn = load_definition(WHEN_CONTAINS_STRING_WORKFLOW)
        # Shell runner sets result_summary to stdout which includes "passed"
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "completed"

    @pytest.mark.asyncio
    async def test_when_contains_list(self, db: Any, engine: WorkflowEngine) -> None:
        """contains: list membership check on result_findings."""
        defn = load_definition(WHEN_CONTAINS_LIST_WORKFLOW)
        mock_result = RunnerResult(
            status="success",
            summary="done",
            artifacts={},
            findings=["warning", "critical", "info"],
        )
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            new_callable=AsyncMock,
            return_value=mock_result,
        ):
            run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "completed"

    @pytest.mark.asyncio
    async def test_when_references_skipped_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Cascading skip: step C depends on skipped step B, so C is also skipped."""
        defn = load_definition(CASCADE_SKIP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["step_a"] == "completed"
        assert statuses["step_b"] == "skipped"
        assert statuses["step_c"] == "skipped"

    @pytest.mark.asyncio
    async def test_when_on_gate_step(self, db: Any, engine: WorkflowEngine) -> None:
        """when clause works on gate steps — skips the gate when condition is false."""
        defn = load_definition(WHEN_ON_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["first"] == "completed"
        assert statuses["gate_step"] == "skipped"

    @pytest.mark.asyncio
    async def test_step_skipped_event_emitted(self, db: Any, engine: WorkflowEngine) -> None:
        """Verify step_skipped event fires with condition_not_met reason."""
        defn = load_definition(WHEN_EQUALS_FALSE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        events = list_workflow_events(db, run["id"])
        skip_events = [e for e in events if e["event_type"] == "step_skipped"]
        assert len(skip_events) == 1
        payload = skip_events[0]["payload"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        assert payload["reason"] == "condition_not_met"
        assert payload["when"]["step"] == "first"

    @pytest.mark.asyncio
    async def test_skipped_step_not_in_results(self, db: Any, engine: WorkflowEngine) -> None:
        """Downstream step can't see a skipped step's results (used in cascade test)."""
        defn = load_definition(CASCADE_SKIP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        # step_c depends on step_b which was skipped, so step_c is also skipped
        assert statuses["step_c"] == "skipped"

    @pytest.mark.asyncio
    async def test_when_dotted_field_path(self, db: Any, engine: WorkflowEngine) -> None:
        """Dotted path like result_artifacts.exit_code resolves correctly."""
        defn = load_definition(WHEN_DOTTED_FIELD_WORKFLOW)
        mock_result = RunnerResult(
            status="success",
            summary="done",
            artifacts={"exit_code": 0},
            findings=[],
        )
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            new_callable=AsyncMock,
            return_value=mock_result,
        ):
            run = await engine.start_run(defn, target_kind="test", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        statuses = {s["step_id"]: s["status"] for s in steps}
        assert statuses["second"] == "completed"


# ---------------------------------------------------------------------------
# _evaluate_when unit tests (direct static method calls)
# ---------------------------------------------------------------------------


class TestEvaluateWhen:
    def test_missing_ref_step_returns_false(self) -> None:
        when = {"step": "missing", "field": "result_status", "equals": "success"}
        assert WorkflowEngine._evaluate_when(when, {}) is False

    def test_equals_match(self) -> None:
        when = {"step": "s1", "field": "result_status", "equals": "success"}
        results = {"s1": {"result_status": "success"}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_equals_mismatch(self) -> None:
        when = {"step": "s1", "field": "result_status", "equals": "failed"}
        results = {"s1": {"result_status": "success"}}
        assert WorkflowEngine._evaluate_when(when, results) is False

    def test_not_equals_match(self) -> None:
        when = {"step": "s1", "field": "result_status", "not_equals": "failed"}
        results = {"s1": {"result_status": "success"}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_is_not_empty_truthy(self) -> None:
        when = {"step": "s1", "field": "result_findings", "is_not_empty": True}
        results = {"s1": {"result_findings": ["item"]}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_is_not_empty_falsy(self) -> None:
        when = {"step": "s1", "field": "result_findings", "is_not_empty": True}
        results = {"s1": {"result_findings": []}}
        assert WorkflowEngine._evaluate_when(when, results) is False

    def test_is_empty_truthy(self) -> None:
        when = {"step": "s1", "field": "result_findings", "is_empty": True}
        results = {"s1": {"result_findings": []}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_is_empty_falsy(self) -> None:
        when = {"step": "s1", "field": "result_findings", "is_empty": True}
        results = {"s1": {"result_findings": ["item"]}}
        assert WorkflowEngine._evaluate_when(when, results) is False

    def test_contains_string(self) -> None:
        when = {"step": "s1", "field": "result_summary", "contains": "pass"}
        results = {"s1": {"result_summary": "all checks passed"}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_contains_list(self) -> None:
        when = {"step": "s1", "field": "result_findings", "contains": "critical"}
        results = {"s1": {"result_findings": ["warning", "critical"]}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_contains_none_value(self) -> None:
        when = {"step": "s1", "field": "result_findings", "contains": "x"}
        results = {"s1": {"result_findings": None}}
        assert WorkflowEngine._evaluate_when(when, results) is False

    def test_dotted_field_path(self) -> None:
        when = {"step": "s1", "field": "result_artifacts.exit_code", "equals": 0}
        results = {"s1": {"result_artifacts": {"exit_code": 0}}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_dotted_field_path_missing(self) -> None:
        when = {"step": "s1", "field": "result_artifacts.missing_key", "equals": 0}
        results = {"s1": {"result_artifacts": {"exit_code": 0}}}
        assert WorkflowEngine._evaluate_when(when, results) is False


# ---------------------------------------------------------------------------
# Resume-stability tests
# ---------------------------------------------------------------------------


class TestWhenResumeStability:
    @pytest.mark.asyncio
    async def test_when_skipped_step_not_duplicated_on_resume(self, db: Any, engine: WorkflowEngine) -> None:
        """Skipped steps must not be re-evaluated on resume.

        Workflow: A (shell) -> B (skipped via when) -> C (human_gate pauses).
        After resolving the gate and resuming, step B must have exactly one
        workflow_steps row and one step_skipped event.
        """
        defn = load_definition(SKIP_THEN_HUMAN_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="resume1")
        assert run["status"] == "waiting_for_input"

        # Verify step B was skipped during initial run
        steps = list_workflow_steps(db, run["id"])
        b_steps = [s for s in steps if s["step_id"] == "step_b"]
        assert len(b_steps) == 1
        assert b_steps[0]["status"] == "skipped"

        # Resolve the human_gate decision so we can resume
        pending = get_pending_decision(db, run["id"])
        assert pending is not None
        resolve_human_decision(db, pending["id"], selected_option="yes", resolved_by="test")

        # Resume the run
        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed"

        # Assert exactly ONE workflow_steps row for step B with status "skipped"
        all_steps = list_workflow_steps(db, result["id"])
        b_rows = [s for s in all_steps if s["step_id"] == "step_b"]
        assert len(b_rows) == 1, f"Expected 1 row for step_b, got {len(b_rows)}"
        assert b_rows[0]["status"] == "skipped"

        # Assert exactly ONE step_skipped event for step B
        events = list_workflow_events(db, result["id"])
        skip_events = [e for e in events if e["event_type"] == "step_skipped" and e.get("step_id") == "step_b"]
        assert len(skip_events) == 1, f"Expected 1 step_skipped event for step_b, got {len(skip_events)}"
