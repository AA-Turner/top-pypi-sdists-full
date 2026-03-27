"""Tests for human_gate step type and approval-related storage."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    check_approval_timeouts,
    check_decision_timeouts,
    create_approval_request,
    create_human_decision,
    get_human_decision,
    get_pending_decision,
    list_workflow_events,
    resolve_human_decision,
)

HUMAN_GATE_WORKFLOW = """\
kind: workflow
id: test_human_gate
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo generated report"
    timeout: 10
  - id: approve_report
    type: human_gate
    prompt: "Review the generated report and choose next action."
    context_from:
      - step: generate
        field: result_summary
    options:
      - id: approve
        label: Approve
        outcome: continue
      - id: revise
        label: Request revision
        outcome: branch
        next_step: revise_step
      - id: cancel
        label: Cancel
        outcome: stop
        stop_reason: operator_cancelled
  - id: publish
    type: runner
    runner: shell
    command: "echo publishing"
    timeout: 10
  - id: revise_step
    type: runner
    runner: shell
    command: "echo revising"
    timeout: 10
"""


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
# Human Decision Storage CRUD
# ---------------------------------------------------------------------------


class TestHumanDecisionStorage:
    def test_create_decision(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        decision = create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="Choose an action",
            options=[{"id": "yes", "label": "Yes", "outcome": "continue"}],
        )
        assert decision["status"] == "pending"
        assert decision["prompt"] == "Choose an action"
        assert len(decision["options"]) == 1

    def test_get_decision(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        decision = create_human_decision(db, run_id=run["id"], step_id="s1", prompt="test", options=[{"id": "a"}])
        fetched = get_human_decision(db, decision["id"])
        assert fetched is not None
        assert fetched["prompt"] == "test"

    def test_get_pending_decision(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        create_human_decision(db, run_id=run["id"], step_id="s1", prompt="test", options=[{"id": "a"}])
        pending = get_pending_decision(db, run["id"])
        assert pending is not None

    def test_resolve_decision(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        decision = create_human_decision(db, run_id=run["id"], step_id="s1", prompt="test", options=[{"id": "a"}])
        resolved = resolve_human_decision(db, decision["id"], selected_option="a", resolved_by="op")
        assert resolved is not None
        assert resolved["status"] == "resolved"
        assert resolved["selected_option"] == "a"

    def test_double_resolve_raises(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        decision = create_human_decision(db, run_id=run["id"], step_id="s1", prompt="test", options=[{"id": "a"}])
        resolve_human_decision(db, decision["id"], selected_option="a")
        with pytest.raises(ValueError, match="already resolved"):
            resolve_human_decision(db, decision["id"], selected_option="b")


# ---------------------------------------------------------------------------
# On-demand timeouts
# ---------------------------------------------------------------------------


class TestOnDemandTimeouts:
    def test_approval_timeout(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="s1",
            tool_name="bash",
            tool_args={},
            risk_tier="EXECUTE",
            timeout_at="2020-01-01T00:00:00Z",  # Past
        )
        expired = check_approval_timeouts(db)
        assert expired == 1

    def test_decision_timeout(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(db, workflow_id="test", workflow_version="0.1.0", target_kind="task", target_ref="t1")
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="test",
            options=[{"id": "a"}],
            timeout_at="2020-01-01T00:00:00Z",
        )
        expired = check_decision_timeouts(db)
        assert expired == 1


# ---------------------------------------------------------------------------
# Human Gate Load-time Validation
# ---------------------------------------------------------------------------


class TestHumanGateValidation:
    def test_valid_human_gate_loads(self) -> None:
        defn = load_definition(HUMAN_GATE_WORKFLOW)
        gate_step = next(s for s in defn.steps if s.type == "human_gate")
        assert gate_step.prompt
        assert len(gate_step.options) == 3

    def test_missing_prompt_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: gate
    type: human_gate
    options:
      - id: ok
        label: OK
        outcome: continue
"""
        with pytest.raises(ValueError, match="requires a 'prompt' field"):
            load_definition(yaml_str)

    def test_missing_options_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: gate
    type: human_gate
    prompt: "Choose"
"""
        with pytest.raises(ValueError, match="requires an 'options' field"):
            load_definition(yaml_str)

    def test_branch_backward_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: target
    type: runner
    runner: shell
    command: "echo"
  - id: gate
    type: human_gate
    prompt: "Choose"
    options:
      - id: back
        label: Go back
        outcome: branch
        next_step: target
"""
        with pytest.raises(ValueError, match="forward-only"):
            load_definition(yaml_str)

    def test_branch_nonexistent_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: gate
    type: human_gate
    prompt: "Choose"
    options:
      - id: go
        label: Go
        outcome: branch
        next_step: nowhere
"""
        with pytest.raises(ValueError, match="not found"):
            load_definition(yaml_str)


# ---------------------------------------------------------------------------
# Engine Execution — human_gate pauses the run
# ---------------------------------------------------------------------------


class TestHumanGateExecution:
    @pytest.mark.asyncio
    async def test_human_gate_pauses_run(self, db: Any, engine: WorkflowEngine) -> None:
        """A workflow with a human_gate step pauses at that step."""
        defn = load_definition(HUMAN_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "waiting_for_input"

        # Decision should be pending
        pending = get_pending_decision(db, run["id"])
        assert pending is not None
        assert "report" in pending["prompt"].lower()

    @pytest.mark.asyncio
    async def test_human_gate_emits_event(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(HUMAN_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t2")
        events = list_workflow_events(db, run["id"])
        event_types = [e["event_type"] for e in events]
        assert "waiting_for_input" in event_types

    @pytest.mark.asyncio
    async def test_resume_after_continue_decision(self, db: Any, engine: WorkflowEngine) -> None:
        """Resume after 'continue' decision proceeds to next step."""
        defn = load_definition(HUMAN_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t3")
        assert run["status"] == "waiting_for_input"

        # Resolve the decision
        pending = get_pending_decision(db, run["id"])
        resolve_human_decision(db, pending["id"], selected_option="approve", resolved_by="op")

        # Resume
        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_resume_after_stop_decision(self, db: Any, engine: WorkflowEngine) -> None:
        """Resume after 'stop' decision terminates the run."""
        defn = load_definition(HUMAN_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t4")

        pending = get_pending_decision(db, run["id"])
        resolve_human_decision(db, pending["id"], selected_option="cancel", resolved_by="op")

        result = await engine.resume_run(run["id"], defn)
        assert result["status"] in ("completed", "cancelled")
        assert "operator_cancelled" in (result.get("stop_reason") or "")

    @pytest.mark.asyncio
    async def test_resume_with_unresolved_raises(self, db: Any, engine: WorkflowEngine) -> None:
        """Resume with pending decision raises error."""
        defn = load_definition(HUMAN_GATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t5")

        with pytest.raises(ValueError, match="still pending"):
            await engine.resume_run(run["id"], defn)
