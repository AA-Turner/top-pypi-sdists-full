"""Tests for the workflow engine core.

These tests use a GENERIC test workflow — not issue_delivery — to prove the
engine is domain-neutral. The test workflow has runner, gate, and loop steps
that process arbitrary data, not GitHub-specific data.
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
    _resolve_dotted_refs,
    _resolve_summary_template,
    load_definition,
    register_gate_condition,
    resolve_context_from,
    resolve_context_from_failed_step,
    resolve_template,
    validate_approval_mode,
)
from anteroom.services.workflow_runners import RunnerResult, create_default_registry, create_stub_registry
from anteroom.services.workflow_storage import get_workflow_run, list_workflow_events, list_workflow_steps

# ---------------------------------------------------------------------------
# Generic test workflow YAML (domain-neutral — no GitHub/PR/issue concepts)
# ---------------------------------------------------------------------------

GENERIC_WORKFLOW = """\
kind: workflow
id: test_pipeline
version: 0.1.0
inputs:
  target_name:
    type: string
    required: true
  threshold:
    type: integer
    required: false
policies:
  max_review_rounds: 2
steps:
  - id: validate_input
    type: runner
    runner: shell
    command: "echo Validating {target_name}"
    timeout: 10
  - id: gate_ready
    type: gate
    condition: always_pass
    if_false: not_ready
  - id: process_data
    type: runner
    runner: shell
    command: "echo Processing data for {target_name}"
    timeout: 30
"""

LOOP_WORKFLOW = """\
kind: workflow
id: test_loop
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: refine_loop
    type: loop
    max_rounds: 3
    steps:
      - id: check
        type: runner
        runner: shell
        command: "echo checking round"
      - id: fix
        type: runner
        runner: shell
        command: "echo fixing round"
"""

GATE_FAIL_WORKFLOW = """\
kind: workflow
id: test_gate_fail
version: 0.1.0
inputs: {}
steps:
  - id: pre_check
    type: runner
    runner: shell
    command: "echo pre-check"
  - id: gate_block
    type: gate
    condition: always_fail
    if_false: requirement_not_met
  - id: should_not_run
    type: runner
    runner: shell
    command: "echo should not reach here"
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
    """Register generic test gate conditions."""

    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    async def always_fail(run: Any, step: Any, inputs: Any) -> bool:
        return False

    register_gate_condition("always_pass", always_pass)
    register_gate_condition("always_fail", always_fail)
    yield


# ---------------------------------------------------------------------------
# Definition loading
# ---------------------------------------------------------------------------


class TestLoadDefinition:
    def test_load_valid_yaml(self) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        assert defn.id == "test_pipeline"
        assert defn.version == "0.1.0"
        assert len(defn.steps) == 3
        assert defn.inputs["target_name"]["required"] is True

    def test_load_with_loop(self) -> None:
        defn = load_definition(LOOP_WORKFLOW)
        assert defn.steps[0].type == "loop"
        assert defn.steps[0].max_rounds == 3
        assert len(defn.steps[0].steps) == 2

    def test_missing_kind_raises(self) -> None:
        yaml_str = (
            "id: test\nversion: 0.1.0\nsteps:\n  - id: s1\n    type: runner\n    runner: shell\n    command: echo"
        )
        with pytest.raises(ValueError, match="kind: workflow"):
            load_definition(yaml_str)

    def test_missing_id_raises(self) -> None:
        with pytest.raises(ValueError, match="'id'"):
            load_definition("kind: workflow\nversion: 0.1.0\nsteps:\n  - id: s1\n    type: runner")

    def test_empty_steps_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one step"):
            load_definition("kind: workflow\nid: test\nversion: 0.1.0\nsteps: []")

    def test_invalid_step_type_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid type"):
            load_definition("kind: workflow\nid: t\nversion: 0.1.0\nsteps:\n  - id: s1\n    type: invalid")

    def test_step_missing_id_raises(self) -> None:
        with pytest.raises(ValueError, match="'id'"):
            load_definition("kind: workflow\nid: t\nversion: 0.1.0\nsteps:\n  - type: runner")

    def test_load_from_file(self, tmp_path: Path) -> None:
        f = tmp_path / "test.yaml"
        f.write_text(GENERIC_WORKFLOW)
        defn = load_definition(f)
        assert defn.id == "test_pipeline"


# ---------------------------------------------------------------------------
# Template resolution
# ---------------------------------------------------------------------------


class TestTemplateResolution:
    def test_resolve_simple(self) -> None:
        result = resolve_template("hello {name}", {"name": "world"})
        assert result == "hello world"

    def test_resolve_shell_quoted(self) -> None:
        result = resolve_template("echo {val}", {"val": "foo bar; rm -rf /"}, shell_quote=True)
        assert "rm -rf" not in result or "'" in result

    def test_missing_variable_raises(self) -> None:
        with pytest.raises(KeyError):
            resolve_template("hello {missing}", {})


class TestResolveSummaryTemplate:
    def test_step_result_reference(self) -> None:
        result = _resolve_summary_template(
            "PR {step.create_pr.result_summary} done",
            {},
            {"create_pr": {"result_summary": "#42 opened"}},
        )
        assert result == "PR #42 opened done"

    def test_nested_step_field(self) -> None:
        result = _resolve_summary_template(
            "number={step.work.result_artifacts.pr_number}",
            {},
            {"work": {"result_artifacts": {"pr_number": "99"}}},
        )
        assert result == "number=99"

    def test_stop_reason_and_failing_step(self) -> None:
        result = _resolve_summary_template(
            "Failed: {stop_reason} at {failing_step}",
            {},
            {},
            stop_reason="step_failed:deploy",
            failing_step="deploy",
        )
        assert result == "Failed: step_failed:deploy at deploy"

    def test_inputs_and_step_refs_combined(self) -> None:
        result = _resolve_summary_template(
            "{project}: {step.build.result_summary}",
            {"project": "acme"},
            {"build": {"result_summary": "success"}},
        )
        assert result == "acme: success"

    def test_unknown_step_left_unresolved(self) -> None:
        result = _resolve_summary_template(
            "val={step.missing.result_summary}",
            {},
            {},
        )
        assert result == "val={step.missing.result_summary}"

    def test_unknown_field_left_unresolved(self) -> None:
        result = _resolve_summary_template(
            "val={step.work.no_such_field}",
            {},
            {"work": {"result_summary": "ok"}},
        )
        assert result == "val={step.work.no_such_field}"

    def test_unknown_input_graceful(self) -> None:
        result = _resolve_summary_template(
            "Done with {nonexistent}",
            {},
            {},
        )
        assert result == "Done with {nonexistent}"


class TestContextFromResolution:
    def test_resolve_simple(self) -> None:
        refs = [{"step": "step1", "field": "result_summary"}]
        results = {"step1": {"result_summary": "All checks passed"}}
        ctx = resolve_context_from(refs, results)
        assert "All checks passed" in ctx

    def test_resolve_dotted_path(self) -> None:
        refs = [{"step": "step1", "field": "result_artifacts.count"}]
        results = {"step1": {"result_artifacts": {"count": 42}}}
        ctx = resolve_context_from(refs, results)
        assert "42" in ctx

    def test_missing_step_skipped(self) -> None:
        refs = [{"step": "nonexistent", "field": "summary"}]
        ctx = resolve_context_from(refs, {})
        assert ctx == ""


# ---------------------------------------------------------------------------
# Approval mode validation
# ---------------------------------------------------------------------------


class TestApprovalModeValidation:
    def test_equal_strictness_passes(self) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        validate_approval_mode(defn, "ask_for_writes")

    def test_stricter_passes(self) -> None:
        extra = (
            "steps:\n  - id: strict_step\n    type: runner\n"
            "    runner: shell\n    command: echo\n    approval_mode: ask"
        )
        yaml_str = GENERIC_WORKFLOW.replace("steps:", extra)
        defn = load_definition(yaml_str)
        validate_approval_mode(defn, "ask_for_writes")

    def test_more_permissive_raises(self) -> None:
        extra = (
            "steps:\n  - id: lax_step\n    type: runner\n    runner: shell\n    command: echo\n    approval_mode: auto"
        )
        yaml_str = GENERIC_WORKFLOW.replace("steps:", extra)
        defn = load_definition(yaml_str)
        with pytest.raises(ValueError, match="more permissive"):
            validate_approval_mode(defn, "ask_for_writes")

    def test_policy_level_too_permissive_raises(self) -> None:
        yaml_str = GENERIC_WORKFLOW.replace("policies:", "policies:\n  approval_mode: auto")
        defn = load_definition(yaml_str)
        with pytest.raises(ValueError, match="more permissive"):
            validate_approval_mode(defn, "ask_for_writes")


# ---------------------------------------------------------------------------
# Engine execution — generic workflows
# ---------------------------------------------------------------------------


class TestEngineExecution:
    @pytest.mark.asyncio
    async def test_run_generic_workflow(self, db: Any, engine: WorkflowEngine) -> None:
        """Engine executes a generic pipeline workflow with no domain-specific concepts."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="dataset",
            target_ref="sales_q4",
            inputs={"target_name": "sales_q4"},
        )
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        assert len(steps) == 3
        assert all(s["status"] == "completed" for s in steps)

    @pytest.mark.asyncio
    async def test_gate_blocks_workflow(self, db: Any, engine: WorkflowEngine) -> None:
        """Gate step blocks the workflow when condition returns False."""
        defn = load_definition(GATE_FAIL_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "blocked"
        assert "requirement_not_met" in (run.get("stop_reason") or "")

        steps = list_workflow_steps(db, run["id"])
        completed = [s for s in steps if s["status"] == "completed"]
        assert len(completed) == 2  # pre_check + gate_block

    @pytest.mark.asyncio
    async def test_loop_respects_max_rounds(self, db: Any, engine: WorkflowEngine) -> None:
        """Loop step exits after max_rounds."""
        defn = load_definition(LOOP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="batch", target_ref="b1")
        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_concurrency_lock_rejects_duplicate(self, db: Any, engine: WorkflowEngine) -> None:
        """Second run on same target is rejected while first holds the lock."""
        from anteroom.services.workflow_storage import acquire_lock, create_workflow_run, release_lock

        # Create a real run record so the FK constraint is satisfied
        blocker = create_workflow_run(
            db,
            workflow_id="blocker",
            workflow_version="0.1.0",
            target_kind="doc",
            target_ref="d1",
        )
        acquire_lock(db, target_kind="doc", target_ref="d1", run_id=blocker["id"])

        defn = load_definition(GENERIC_WORKFLOW)
        with pytest.raises(RuntimeError, match="already locked"):
            await engine.start_run(defn, target_kind="doc", target_ref="d1", inputs={"target_name": "x"})

        release_lock(db, run_id=blocker["id"])

    @pytest.mark.asyncio
    async def test_missing_required_input_raises(self, db: Any, engine: WorkflowEngine) -> None:
        """Missing required input raises ValueError before execution starts."""
        defn = load_definition(GENERIC_WORKFLOW)
        with pytest.raises(ValueError, match="Missing required input"):
            await engine.start_run(defn, target_kind="task", target_ref="t1")

    @pytest.mark.asyncio
    async def test_events_emitted(self, db: Any, engine: WorkflowEngine) -> None:
        """Engine emits durable events for each state transition."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="task",
            target_ref="t1",
            inputs={"target_name": "test"},
        )
        events = list_workflow_events(db, run["id"])
        event_types = [e["event_type"] for e in events]
        assert "run_started" in event_types
        assert "step_started" in event_types
        assert "step_finished" in event_types
        assert "run_completed" in event_types

    @pytest.mark.asyncio
    async def test_step_results_stored(self, db: Any, engine: WorkflowEngine) -> None:
        """Step results are persisted in storage."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="task",
            target_ref="t1",
            inputs={"target_name": "test"},
        )
        steps = list_workflow_steps(db, run["id"])
        for step in steps:
            assert step["result_status"] is not None
            assert step["duration_ms"] is not None
            assert step["completed_at"] is not None

    @pytest.mark.asyncio
    async def test_lock_released_on_completion(self, db: Any, engine: WorkflowEngine) -> None:
        """Lock is released after successful completion."""
        from anteroom.services.workflow_storage import get_lock

        defn = load_definition(GENERIC_WORKFLOW)
        await engine.start_run(
            defn,
            target_kind="task",
            target_ref="t1",
            inputs={"target_name": "test"},
        )
        assert get_lock(db, target_kind="task", target_ref="t1") is None

    @pytest.mark.asyncio
    async def test_lock_released_on_failure(self, db: Any, engine: WorkflowEngine) -> None:
        """Lock is released even when the run fails."""
        from anteroom.services.workflow_storage import get_lock

        defn = load_definition(GATE_FAIL_WORKFLOW)
        await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert get_lock(db, target_kind="task", target_ref="t1") is None


FAILING_WORKFLOW = """\
kind: workflow
id: test_fail
version: 0.1.0
inputs: {}
steps:
  - id: will_fail
    type: runner
    runner: shell
    command: "exit 7"
    timeout: 10
"""


class TestRunnerFailurePropagation:
    """Failed runner results must fail the workflow, not silently continue."""

    @pytest.mark.asyncio
    async def test_failed_runner_fails_workflow(self, db: Any, engine: WorkflowEngine) -> None:
        """A shell step that exits non-zero must fail the entire run."""
        defn = load_definition(FAILING_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "failed"
        assert "step_failed:will_fail" in (run.get("stop_reason") or "")

    @pytest.mark.asyncio
    async def test_failed_runner_emits_run_failed_event(self, db: Any, engine: WorkflowEngine) -> None:
        """A failed run must emit a run_failed durable event for SSE/webhook consumers."""
        defn = load_definition(FAILING_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t2")
        events = list_workflow_events(db, run["id"])
        event_types = [e["event_type"] for e in events]
        assert "run_failed" in event_types

    @pytest.mark.asyncio
    async def test_failed_step_stops_subsequent_steps(self, db: Any, engine: WorkflowEngine) -> None:
        """Steps after a failed step should not execute."""
        yaml_str = """\
kind: workflow
id: test_fail_stops
version: 0.1.0
inputs: {}
steps:
  - id: fail_step
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
  - id: should_not_run
    type: runner
    runner: shell
    command: "echo should not reach here"
    timeout: 10
"""
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert "fail_step" in step_ids
        assert "should_not_run" not in step_ids


# ---------------------------------------------------------------------------
# Anti-overfitting check: engine has no GitHub-specific types
# ---------------------------------------------------------------------------


class TestDomainNeutrality:
    """These tests explicitly verify the engine is domain-neutral."""

    @pytest.mark.asyncio
    async def test_arbitrary_target_kind(self, db: Any, engine: WorkflowEngine) -> None:
        """target_kind can be anything — not just 'issue'."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="document",
            target_ref="quarterly_report",
            inputs={"target_name": "quarterly_report"},
        )
        assert run["status"] == "completed"
        assert run["target_kind"] == "document"

    @pytest.mark.asyncio
    async def test_non_coding_workflow(self, db: Any, engine: WorkflowEngine) -> None:
        """A workflow with no coding concepts runs successfully."""
        yaml_str = """\
kind: workflow
id: data_pipeline
version: 0.1.0
inputs:
  dataset:
    type: string
    required: true
steps:
  - id: validate
    type: runner
    runner: shell
    command: "echo Validating {dataset}"
  - id: quality_gate
    type: gate
    condition: always_pass
    if_false: quality_check_failed
  - id: transform
    type: runner
    runner: shell
    command: "echo Transforming {dataset}"
"""
        defn = load_definition(yaml_str)
        run = await engine.start_run(
            defn,
            target_kind="dataset",
            target_ref="sales_2026",
            inputs={"dataset": "sales_2026"},
        )
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        assert len(steps) == 3


# ---------------------------------------------------------------------------
# Blocker fixes — approval validation, loop persistence, agent runner
# ---------------------------------------------------------------------------


PERMISSIVE_WORKFLOW = """\
kind: workflow
id: test_permissive
version: 0.1.0
inputs: {}
policies:
  approval_mode: auto
steps:
  - id: do_thing
    type: runner
    runner: shell
    command: "echo hello"
"""


class TestApprovalModeEnforcement:
    """validate_approval_mode() must be called and block permissive workflows."""

    @pytest.mark.asyncio
    async def test_permissive_policy_blocked_at_start(self, db: Any) -> None:
        """Workflow with policies.approval_mode: auto rejected under ask_for_writes."""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(
            db,
            config,
            registry,
            effective_approval_mode="ask_for_writes",
        )
        defn = load_definition(PERMISSIVE_WORKFLOW)
        with pytest.raises(ValueError, match="more permissive"):
            await engine.start_run(defn, target_kind="task", target_ref="t1")

    @pytest.mark.asyncio
    async def test_permissive_step_blocked_at_start(self, db: Any) -> None:
        """Step with approval_mode: auto rejected under ask_for_writes."""
        yaml_str = """\
kind: workflow
id: test_step_permissive
version: 0.1.0
inputs: {}
steps:
  - id: lax
    type: runner
    runner: shell
    command: "echo"
    approval_mode: auto
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(
            db,
            config,
            registry,
            effective_approval_mode="ask_for_writes",
        )
        defn = load_definition(yaml_str)
        with pytest.raises(ValueError, match="more permissive"):
            await engine.start_run(defn, target_kind="task", target_ref="t1")


class TestLoopStepPersistence:
    """Loop nested steps must create workflow_steps rows and events."""

    @pytest.mark.asyncio
    async def test_loop_nested_steps_persisted(self, db: Any, engine: WorkflowEngine) -> None:
        """Each nested step in each round creates a step record."""
        defn = load_definition(LOOP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="batch", target_ref="b1")
        assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        nested_steps = [s for s in steps if "_r" in s["step_id"]]
        assert len(nested_steps) >= 2  # at least 1 round with 2 steps

        for ns in nested_steps:
            assert ns["status"] == "completed"
            assert ns["result_status"] is not None
            assert ns["duration_ms"] is not None

    @pytest.mark.asyncio
    async def test_loop_nested_events_emitted(self, db: Any, engine: WorkflowEngine) -> None:
        """Events are emitted for each nested step start/finish."""
        defn = load_definition(LOOP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="batch", target_ref="b1")

        events = list_workflow_events(db, run["id"])
        nested_events = [e for e in events if e.get("step_id") and "_r" in e["step_id"]]
        # at least 2 starts + 2 finishes for round 1
        assert len(nested_events) >= 4


# ---------------------------------------------------------------------------
# Load-time validation and fail-closed behavior
# ---------------------------------------------------------------------------


class TestLoadTimeValidation:
    """Bad step payloads and context_from refs must be rejected at load time."""

    def test_shell_runner_missing_command_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_shell
version: 0.1.0
inputs: {}
steps:
  - id: no_cmd
    type: runner
    runner: shell
"""
        with pytest.raises(ValueError, match="requires a 'command' field"):
            load_definition(yaml_str)

    def test_python_script_missing_command_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_pyscript
version: 0.1.0
inputs: {}
steps:
  - id: no_cmd
    type: runner
    runner: python_script
"""
        with pytest.raises(ValueError, match="requires a 'command' field"):
            load_definition(yaml_str)

    def test_agent_runner_missing_prompt_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_agent
version: 0.1.0
inputs: {}
steps:
  - id: no_prompt
    type: runner
    runner: cli_claude
"""
        with pytest.raises(ValueError, match="requires a 'prompt' or 'skill_name' field"):
            load_definition(yaml_str)

    def test_agent_runner_max_iterations_parsed(self) -> None:
        yaml_str = """\
kind: workflow
id: agent_iterations
version: 0.1.0
inputs: {}
steps:
  - id: do_ai
    type: runner
    runner: cli_claude
    prompt: "Do something"
    max_iterations: 42
"""
        defn = load_definition(yaml_str)
        assert defn.steps[0].max_iterations == 42

    def test_non_agent_runner_max_iterations_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_shell_iterations
version: 0.1.0
inputs: {}
steps:
  - id: shell_step
    type: runner
    runner: shell
    command: "echo hi"
    max_iterations: 42
"""
        with pytest.raises(ValueError, match="max_iterations is only allowed on agent runner steps"):
            load_definition(yaml_str)

    def test_gate_missing_condition_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_gate
version: 0.1.0
inputs: {}
steps:
  - id: no_cond
    type: gate
"""
        with pytest.raises(ValueError, match="requires a 'condition' field"):
            load_definition(yaml_str)

    def test_context_from_nonexistent_step_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_ctx
version: 0.1.0
inputs: {}
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo hi"
    context_from:
      - step: nonexistent
        field: summary
"""
        with pytest.raises(ValueError, match="has not appeared before"):
            load_definition(yaml_str)

    def test_context_from_forward_reference_rejected(self) -> None:
        """context_from can't reference a step that comes later."""
        yaml_str = """\
kind: workflow
id: forward_ref
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo"
    context_from:
      - step: second
        field: summary
  - id: second
    type: runner
    runner: shell
    command: "echo"
"""
        with pytest.raises(ValueError, match="has not appeared before"):
            load_definition(yaml_str)

    def test_context_from_valid_back_reference_passes(self) -> None:
        """context_from referencing an earlier step is fine."""
        yaml_str = """\
kind: workflow
id: valid_ctx
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo first"
  - id: second
    type: runner
    runner: shell
    command: "echo second"
    context_from:
      - step: first
        field: result_summary
"""
        defn = load_definition(yaml_str)
        assert len(defn.steps) == 2

    def test_context_from_missing_step_field_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_ref
version: 0.1.0
inputs: {}
steps:
  - id: first
    type: runner
    runner: shell
    command: "echo"
  - id: second
    type: runner
    runner: shell
    command: "echo"
    context_from:
      - field: summary
"""
        with pytest.raises(ValueError, match="missing 'step' field"):
            load_definition(yaml_str)


class TestAgentRunnerFailClosed:
    """Agent runner must fail when AI service is not configured."""

    @pytest.mark.asyncio
    async def test_agent_runner_no_ai_service_fails(self, db: Any) -> None:
        """Engine with no ai_service fails on agent runner steps, not succeeds."""
        yaml_str = """\
kind: workflow
id: agent_no_ai
version: 0.1.0
inputs: {}
steps:
  - id: do_ai
    type: runner
    runner: cli_claude
    prompt: "Do something"
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)  # no ai_service
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        # The run must fail, not succeed with synthetic data
        assert run["status"] == "failed"
        assert run.get("stop_reason") is not None


# ---------------------------------------------------------------------------
# continue_on: step-level failure continuation (#1126)
# ---------------------------------------------------------------------------

CONTINUE_ON_WORKFLOW = """\
kind: workflow
id: test_continue_on
version: 0.1.0
inputs: {}
steps:
  - id: will_fail
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
    continue_on: [failed]
  - id: after_fail
    type: runner
    runner: shell
    command: "echo still running"
    timeout: 10
"""

CONTINUE_ON_THEN_BRANCH_WORKFLOW = """\
kind: workflow
id: test_continue_on_branch
version: 0.1.0
inputs: {}
steps:
  - id: lint_check
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
    continue_on: [failed]
  - id: deploy_on_success
    type: runner
    runner: shell
    command: "echo deploying"
    timeout: 10
    when:
      step: lint_check
      field: result_status
      equals: success
  - id: report_failure
    type: runner
    runner: shell
    command: "echo lint failed"
    timeout: 10
    when:
      step: lint_check
      field: result_status
      equals: failed
"""


class TestContinueOn:
    """continue_on: [failed] allows workflows to proceed past failed steps (#1126)."""

    @pytest.mark.asyncio
    async def test_continue_on_failed_run_completes(self, db: Any, engine: WorkflowEngine) -> None:
        """A step with continue_on: [failed] that fails should not abort the run."""
        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_continued_step_marked_failed_in_db(self, db: Any, engine: WorkflowEngine) -> None:
        """The failed step should still be recorded as failed, not rewritten to success."""
        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t2")
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "will_fail")
        assert fail_step["result_status"] == "failed"

    @pytest.mark.asyncio
    async def test_subsequent_step_executes(self, db: Any, engine: WorkflowEngine) -> None:
        """Steps after a continued failure should execute."""
        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t3")
        steps = list_workflow_steps(db, run["id"])
        step_ids = [s["step_id"] for s in steps]
        assert "after_fail" in step_ids
        after = next(s for s in steps if s["step_id"] == "after_fail")
        assert after["result_status"] == "success"

    @pytest.mark.asyncio
    async def test_step_continued_event_emitted(self, db: Any, engine: WorkflowEngine) -> None:
        """A step_continued event must be emitted when continue_on triggers."""
        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t4")
        events = list_workflow_events(db, run["id"])
        continued = [e for e in events if e["event_type"] == "step_continued"]
        assert len(continued) == 1
        assert continued[0]["step_id"] == "will_fail"

    @pytest.mark.asyncio
    async def test_downstream_when_branches_on_failed_status(self, db: Any, engine: WorkflowEngine) -> None:
        """Downstream steps can branch on the continued-failed step's result_status."""
        defn = load_definition(CONTINUE_ON_THEN_BRANCH_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t5")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        step_map = {s["step_id"]: s for s in steps}
        assert "deploy_on_success" in step_map
        assert step_map["deploy_on_success"]["status"] == "skipped"
        assert "report_failure" in step_map
        assert step_map["report_failure"]["result_status"] == "success"

    @pytest.mark.asyncio
    async def test_without_continue_on_still_aborts(self, db: Any, engine: WorkflowEngine) -> None:
        """A step without continue_on that fails must still abort the run (backward compat)."""
        defn = load_definition(FAILING_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t6")
        assert run["status"] == "failed"

    @pytest.mark.asyncio
    async def test_continue_on_with_retry_exhaustion(self, db: Any, engine: WorkflowEngine) -> None:
        """Retry is attempted first; continue_on kicks in after exhaustion."""
        yaml_str = """\
kind: workflow
id: test_retry_then_continue
version: 0.1.0
inputs: {}
steps:
  - id: flaky
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
    retry:
      max_attempts: 2
      backoff: fixed
      initial_delay: 0.01
      max_delay: 0.01
    continue_on: [failed]
  - id: next_step
    type: runner
    runner: shell
    command: "echo ok"
    timeout: 10
"""
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="t7")
        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        retry_events = [e for e in events if e["event_type"] == "step_retry"]
        assert len(retry_events) >= 1
        continued = [e for e in events if e["event_type"] == "step_continued"]
        assert len(continued) == 1

    @pytest.mark.asyncio
    async def test_later_non_continued_failure_aborts(self, db: Any, engine: WorkflowEngine) -> None:
        """A non-continued failure after a continued one should abort the run."""
        yaml_str = """\
kind: workflow
id: test_later_fail
version: 0.1.0
inputs: {}
steps:
  - id: first_fail
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
    continue_on: [failed]
  - id: second_fail
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
"""
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="t8")
        assert run["status"] == "failed"
        assert "step_failed:second_fail" in (run.get("stop_reason") or "")

    @pytest.mark.asyncio
    async def test_checkpoint_created_at_continued_failure(self, db: Any, engine: WorkflowEngine) -> None:
        """A checkpoint should be created when continue_on triggers."""
        from anteroom.services.workflow_storage import get_latest_checkpoint

        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t9")
        assert run["status"] == "completed"
        # There should be a checkpoint labeled continued:will_fail
        cp = get_latest_checkpoint(db, run["id"])
        assert cp is not None


# ---------------------------------------------------------------------------
# continue_on validation (#1126)
# ---------------------------------------------------------------------------


class TestContinueOnValidation:
    """Load-time validation for continue_on field."""

    def test_continue_on_gate_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_gate_continue
version: 0.1.0
inputs: {}
steps:
  - id: gated
    type: gate
    condition: always_pass
    continue_on: [failed]
"""
        with pytest.raises(ValueError, match="not allowed on gate"):
            load_definition(yaml_str)

    def test_continue_on_blocked_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_blocked_continue
version: 0.1.0
inputs: {}
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo"
    continue_on: [blocked]
"""
        with pytest.raises(ValueError, match="only supports"):
            load_definition(yaml_str)

    def test_continue_on_human_gate_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_hg_continue
version: 0.1.0
inputs: {}
steps:
  - id: hg
    type: human_gate
    prompt: "Approve?"
    options:
      - id: yes
        label: "Yes"
        outcome: continue
    continue_on: [failed]
"""
        with pytest.raises(ValueError, match="not allowed on human_gate"):
            load_definition(yaml_str)


# ---------------------------------------------------------------------------
# context_from_failed_step (#1128)
# ---------------------------------------------------------------------------


class TestResolveContextFromFailedStep:
    """Unit tests for the resolve_context_from_failed_step function (#1128)."""

    def test_failed_step_context_all_fields(self) -> None:
        """All 4 result fields should appear in the XML block."""
        step_results = {
            "run_tests": {
                "result_status": "failed",
                "result_summary": "3 tests failed",
                "result_artifacts": {"exit_code": 1},
                "result_findings": [{"type": "test_failure"}],
            }
        }
        ctx = resolve_context_from_failed_step("run_tests", step_results)
        assert '<failed_step_context step="run_tests">' in ctx
        assert "<status>failed</status>" in ctx
        assert "<summary>3 tests failed</summary>" in ctx
        assert "<artifacts>" in ctx
        assert "<findings>" in ctx

    def test_non_failed_step_includes_note(self) -> None:
        """If the referenced step succeeded, context is still included with a note."""
        step_results = {
            "run_tests": {
                "result_status": "success",
                "result_summary": "All passed",
                "result_artifacts": {},
                "result_findings": None,
            }
        }
        ctx = resolve_context_from_failed_step("run_tests", step_results)
        assert "Step did not fail" in ctx
        assert "<status>success</status>" in ctx

    def test_missing_step_returns_empty(self) -> None:
        """If the referenced step is not in results, return empty string."""
        ctx = resolve_context_from_failed_step("missing", {})
        assert ctx == ""

    def test_coexistence_with_context_from(self) -> None:
        """context_from and context_from_failed_step both produce output."""
        step_results = {
            "step_a": {
                "result_status": "success",
                "result_summary": "OK",
                "result_artifacts": {},
                "result_findings": None,
            },
            "step_b": {
                "result_status": "failed",
                "result_summary": "broke",
                "result_artifacts": {},
                "result_findings": None,
            },
        }
        ctx_from = resolve_context_from([{"step": "step_a", "field": "result_summary"}], step_results)
        failed_ctx = resolve_context_from_failed_step("step_b", step_results)
        assert "OK" in ctx_from
        assert "broke" in failed_ctx

    def test_xml_special_chars_escaped(self) -> None:
        """XML special characters in summary must be escaped to prevent injection."""
        step_results = {
            "evil": {
                "result_status": "failed",
                "result_summary": "</summary><injected>evil</injected><summary>",
                "result_artifacts": {"key": "<script>alert(1)</script>"},
                "result_findings": None,
            }
        }
        ctx = resolve_context_from_failed_step("evil", step_results)
        assert "</summary><injected>" not in ctx
        assert "&lt;/summary&gt;" in ctx
        assert "&lt;script&gt;" in ctx


class TestContextFromFailedStepValidation:
    """Load-time validation for context_from_failed_step field."""

    def test_forward_reference_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_forward
version: 0.1.0
inputs: {}
steps:
  - id: repair
    type: runner
    runner: shell
    command: "echo fix"
    context_from_failed_step: run_tests
  - id: run_tests
    type: runner
    runner: shell
    command: "exit 1"
"""
        with pytest.raises(ValueError, match="has not appeared before"):
            load_definition(yaml_str)

    def test_undeclared_step_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_ref
version: 0.1.0
inputs: {}
steps:
  - id: repair
    type: runner
    runner: shell
    command: "echo fix"
    context_from_failed_step: nonexistent
"""
        with pytest.raises(ValueError, match="has not appeared before"):
            load_definition(yaml_str)

    def test_gate_step_rejected(self) -> None:
        yaml_str = """\
kind: workflow
id: bad_gate
version: 0.1.0
inputs: {}
steps:
  - id: fail_step
    type: runner
    runner: shell
    command: "exit 1"
  - id: gated
    type: gate
    condition: always_pass
    context_from_failed_step: fail_step
"""
        with pytest.raises(ValueError, match="only allowed on runner, llm, human_gate, and publish"):
            load_definition(yaml_str)

    def test_valid_back_reference_passes(self) -> None:
        yaml_str = """\
kind: workflow
id: valid_ref
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "exit 1"
    continue_on: [failed]
  - id: repair
    type: runner
    runner: shell
    command: "echo fix"
    context_from_failed_step: run_tests
"""
        defn = load_definition(yaml_str)
        assert defn.steps[1].context_from_failed_step == "run_tests"


class TestContinueOnWithContextFromFailedStep:
    """Integration: continue_on + context_from_failed_step end-to-end (#1126 + #1128)."""

    @pytest.mark.asyncio
    async def test_repair_step_receives_failure_context(self, db: Any, engine: WorkflowEngine) -> None:
        """A repair step with context_from_failed_step should execute after a continued failure."""
        yaml_str = """\
kind: workflow
id: test_repair_flow
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
    continue_on: [failed]
  - id: report
    type: runner
    runner: shell
    command: "echo reporting"
    timeout: 10
    context_from_failed_step: run_tests
"""
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        report = next(s for s in steps if s["step_id"] == "report")
        assert report["result_status"] == "success"


# ---------------------------------------------------------------------------
# Regression: continued flag in result_artifacts (#1126)
# ---------------------------------------------------------------------------


class TestContinuedArtifactsFlag:
    """Verify the 'continued' flag is set in result_artifacts for continued steps."""

    @pytest.mark.asyncio
    async def test_continued_flag_in_artifacts(self, db: Any, engine: WorkflowEngine) -> None:
        """A continued-after-failure step must have continued=True in result_artifacts."""
        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="flag1")
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "will_fail")
        assert fail_step["result_status"] == "failed"
        artifacts = fail_step.get("result_artifacts") or {}
        assert artifacts.get("continued") is True

    @pytest.mark.asyncio
    async def test_budget_tracked_for_continued_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Budget usage must include continued-after-failure steps."""
        defn = load_definition(CONTINUE_ON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="budget1")
        budget = run.get("budget_usage") or {}
        # Both steps (will_fail + after_fail) should be counted
        assert budget.get("steps_completed", 0) >= 2


class TestRenderStepLineContinued:
    """Verify render_step_line shows (continued) suffix for continued-failed steps."""

    def test_continued_suffix_from_artifacts(self) -> None:
        from anteroom.cli.workflow_fmt import render_step_line

        step = {
            "step_id": "lint",
            "result_status": "failed",
            "result_artifacts": {"continued": True},
            "status": "failed",
        }
        line = render_step_line(step)
        assert "(continued)" in line

    def test_no_continued_suffix_for_normal_failure(self) -> None:
        from anteroom.cli.workflow_fmt import render_step_line

        step = {
            "step_id": "lint",
            "result_status": "failed",
            "result_artifacts": {},
            "status": "failed",
        }
        line = render_step_line(step)
        assert "(continued)" not in line


# ---------------------------------------------------------------------------
# Failure triage enrichment (#1151)
# ---------------------------------------------------------------------------

TRIAGE_PYTEST_WORKFLOW = """\
kind: workflow
id: test_triage_pytest
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "printf 'FAILED tests/unit/test_foo.py::test_bar - assert 1 == 2\\n1 failed in 0.5s' && exit 1"
    timeout: 10
"""

TRIAGE_GENERIC_WORKFLOW = """\
kind: workflow
id: test_triage_generic
version: 0.1.0
inputs: {}
steps:
  - id: run_step
    type: runner
    runner: shell
    command: "echo 'something went wrong' && exit 1"
    timeout: 10
"""

TRIAGE_CONTEXT_WORKFLOW = """\
kind: workflow
id: test_triage_context
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "printf 'FAILED tests/unit/test_foo.py::test_bar - AssertionError\\n1 failed' && exit 1"
    timeout: 10
    continue_on: [failed]
  - id: repair
    type: runner
    runner: shell
    command: "echo repairing"
    timeout: 10
    context_from_failed_step: run_tests
"""


class TestFailureTriageEnrichment:
    """Verify failure triage extraction in workflow engine (#1151)."""

    @pytest.mark.asyncio
    async def test_failed_runner_step_has_failure_triage(self, db: Any, engine: WorkflowEngine) -> None:
        """A runner step with pytest-style output should have failure_triage in artifacts."""
        defn = load_definition(TRIAGE_PYTEST_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="triage1")
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "run_tests")
        artifacts = fail_step.get("result_artifacts") or {}
        assert "failure_triage" in artifacts
        triage = artifacts["failure_triage"]
        assert triage["first_failing_test"] == "tests/unit/test_foo.py::test_bar"
        assert "failure_signature" in triage

    @pytest.mark.asyncio
    async def test_triage_none_when_no_parseable_output(self, db: Any, engine: WorkflowEngine) -> None:
        """A runner step with generic failure text should not have failure_triage."""
        defn = load_definition(TRIAGE_GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="triage2")
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "run_step")
        artifacts = fail_step.get("result_artifacts") or {}
        # exit_code produces triage, but no test/assertion/traceback fields
        # The triage should still exist because exit_code is present
        if "failure_triage" in artifacts:
            triage = artifacts["failure_triage"]
            assert "first_failing_test" not in triage

    @pytest.mark.asyncio
    async def test_context_from_failed_step_includes_triage(self, db: Any, engine: WorkflowEngine) -> None:
        """The XML envelope from context_from_failed_step must include failure_triage."""
        defn = load_definition(TRIAGE_CONTEXT_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="triage3")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "run_tests")
        artifacts = fail_step.get("result_artifacts") or {}
        assert "failure_triage" in artifacts
        # Verify the resolve_context_from_failed_step function includes triage
        step_results = {
            "run_tests": {
                "result_status": "failed",
                "result_summary": "FAILED tests/unit/test_foo.py::test_bar",
                "result_artifacts": artifacts,
                "result_findings": None,
            }
        }
        xml_ctx = resolve_context_from_failed_step("run_tests", step_results)
        assert "<failure_triage>" in xml_ctx
        assert "first_failing_test" in xml_ctx

    def test_triage_in_safe_artifact_keys(self) -> None:
        """failure_triage must be in _SAFE_ARTIFACT_KEYS for checkpoint sanitization."""
        assert "failure_triage" in WorkflowEngine._SAFE_ARTIFACT_KEYS

    @pytest.mark.asyncio
    async def test_triage_enrichment_continue_on(self, db: Any, engine: WorkflowEngine) -> None:
        """Triage is enriched AND workflow continues when continue_on: [failed]."""
        yaml_str = """\
kind: workflow
id: test_triage_continue
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "echo placeholder"
    timeout: 10
    continue_on: [failed]
  - id: next_step
    type: runner
    runner: shell
    command: "echo after"
    timeout: 10
"""
        pytest_summary = "FAILED tests/unit/test_foo.py::test_bar - AssertionError: assert 1 == 2\n1 failed in 0.5s"

        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return RunnerResult(
                    status="failed",
                    summary=pytest_summary,
                    artifacts={"exit_code": 1},
                    findings=[],
                    duration_ms=100,
                )
            return RunnerResult(status="success", summary="ok", duration_ms=50)

        defn = load_definition(yaml_str)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="triage_co")

        assert run["status"] == "completed", f"Expected completed, got {run['status']}"
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "run_tests")
        artifacts = fail_step.get("result_artifacts") or {}
        assert "failure_triage" in artifacts, "continue_on path must enrich with failure_triage"
        assert artifacts["failure_triage"]["first_failing_test"] == "tests/unit/test_foo.py::test_bar"
        assert artifacts.get("continued") is True

    @pytest.mark.asyncio
    async def test_triage_enrichment_on_failure_branch(self, db: Any, engine: WorkflowEngine) -> None:
        """Triage is enriched on the failed step when on_failure branch runs."""
        yaml_str = """\
kind: workflow
id: test_triage_on_failure
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: "echo placeholder"
    timeout: 10
    on_failure:
      - id: handle_failure
        type: runner
        runner: shell
        command: "echo handling"
        timeout: 10
  - id: after
    type: runner
    runner: shell
    command: "echo done"
    timeout: 10
"""
        pytest_summary = "FAILED tests/unit/test_foo.py::test_bar - AssertionError: assert 1 == 2\n1 failed in 0.5s"

        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return RunnerResult(
                    status="failed",
                    summary=pytest_summary,
                    artifacts={"exit_code": 1},
                    findings=[],
                    duration_ms=100,
                )
            return RunnerResult(status="success", summary="ok", duration_ms=50)

        defn = load_definition(yaml_str)
        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            side_effect=mock_runner,
        ):
            run = await engine.start_run(defn, target_kind="task", target_ref="triage_of")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        fail_step = next(s for s in steps if s["step_id"] == "run_tests")
        artifacts = fail_step.get("result_artifacts") or {}
        assert "failure_triage" in artifacts, "on_failure path must enrich with failure_triage"
        assert artifacts["failure_triage"]["first_failing_test"] == "tests/unit/test_foo.py::test_bar"
        assert artifacts.get("on_failure_handled") is True

    @pytest.mark.asyncio
    async def test_triage_enrichment_loop_nested_failure(self, db: Any) -> None:
        """Triage is enriched when a step fails inside a loop."""
        yaml_str = """\
kind: workflow
id: test_triage_loop
version: 0.1.0
inputs: {}
steps:
  - id: retry_loop
    type: loop
    max_rounds: 1
    steps:
      - id: run_tests
        type: runner
        runner: stub
        command: "echo placeholder"
"""
        config = WorkflowConfig()
        registry = create_stub_registry()
        engine = WorkflowEngine(db, config, registry)
        engine._stub_results = {  # type: ignore[attr-defined]
            "run_tests": {
                "status": "failed",
                "summary": "FAILED tests/unit/test_foo.py::test_bar - AssertionError: assert 1 == 2\n1 failed",
                "artifacts": {"exit_code": 1},
                "findings": [],
            },
        }
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="triage_loop")

        steps = list_workflow_steps(db, run["id"])
        nested_steps = [s for s in steps if "_r" in s["step_id"]]
        assert len(nested_steps) >= 1
        nested_fail = next(s for s in nested_steps if "run_tests" in s["step_id"])
        artifacts = nested_fail.get("result_artifacts") or {}
        assert "failure_triage" in artifacts, "loop nested step must have failure_triage"
        assert artifacts["failure_triage"]["first_failing_test"] == "tests/unit/test_foo.py::test_bar"

    @pytest.mark.asyncio
    async def test_triage_enrichment_parallel_branch_failure(self, db: Any) -> None:
        """Triage is enriched when a step fails in a parallel branch."""
        yaml_str = """\
kind: workflow
id: test_triage_parallel
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: lint
        steps:
          - id: run_lint
            type: runner
            runner: stub
            command: "echo lint"
      - id: test
        steps:
          - id: run_tests
            type: runner
            runner: stub
            command: "echo test"
"""
        config = WorkflowConfig()
        registry = create_stub_registry()
        engine = WorkflowEngine(db, config, registry)
        engine._stub_results = {  # type: ignore[attr-defined]
            "run_tests": {
                "status": "failed",
                "summary": "FAILED tests/unit/test_foo.py::test_bar - AssertionError: assert 1 == 2\n1 failed",
                "artifacts": {"exit_code": 1},
                "findings": [],
            },
        }
        defn = load_definition(yaml_str)
        run = await engine.start_run(defn, target_kind="task", target_ref="triage_par")

        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        branch_step = next(s for s in steps if s["step_id"] == "test/run_tests")
        artifacts = branch_step.get("result_artifacts") or {}
        assert "failure_triage" in artifacts, "parallel branch step must have failure_triage"
        assert artifacts["failure_triage"]["first_failing_test"] == "tests/unit/test_foo.py::test_bar"

    def test_triage_survives_checkpoint_sanitization(self) -> None:
        """failure_triage in _SAFE_ARTIFACT_KEYS means it survives _sanitize_checkpoint_data."""
        step_results = {
            "run_tests": {
                "result_status": "failed",
                "result_summary": "FAILED tests/unit/test_foo.py::test_bar",
                "result_artifacts": {
                    "exit_code": 1,
                    "failure_triage": {
                        "first_failing_test": "tests/unit/test_foo.py::test_bar",
                        "first_assertion": "AssertionError: assert 1 == 2",
                        "failure_signature": "abc123",
                    },
                    "secret_should_be_stripped": "sensitive-value",
                },
                "result_findings": None,
                "result_outputs": None,
            }
        }
        sanitized = WorkflowEngine._sanitize_checkpoint_data(step_results)
        arts = sanitized["run_tests"]["result_artifacts"]
        assert "failure_triage" in arts, "failure_triage must survive checkpoint sanitization"
        assert arts["failure_triage"]["first_failing_test"] == "tests/unit/test_foo.py::test_bar"
        assert "secret_should_be_stripped" not in arts, "non-safe keys must be stripped"
        assert "exit_code" in arts


# ---------------------------------------------------------------------------
# Emit step tests (#1150)
# ---------------------------------------------------------------------------

EMIT_WORKFLOW = """\
kind: workflow
id: test_emit
version: 0.1.0
inputs:
  target_name:
    type: string
    required: true
steps:
  - id: notify
    type: emit
    message: "Starting work on {target_name}"
    level: info
  - id: work
    type: runner
    runner: shell
    command: "echo doing work"
  - id: done
    type: emit
    message: "Finished {target_name}"
    level: success
"""

EMIT_WORKFLOW_DEFAULT_LEVEL = """\
kind: workflow
id: test_emit_default
version: 0.1.0
inputs: {}
steps:
  - id: msg
    type: emit
    message: "Hello world"
"""

EMIT_SUMMARY_WORKFLOW = """\
kind: workflow
id: test_summary
version: 0.1.0
inputs:
  project:
    type: string
    required: true
summary:
  on_success: "Completed {project} successfully"
  on_failure: "Failed to process {project}"
steps:
  - id: work
    type: runner
    runner: shell
    command: "echo working on {project}"
"""

EMIT_SUMMARY_FAIL_WORKFLOW = """\
kind: workflow
id: test_summary_fail
version: 0.1.0
inputs:
  project:
    type: string
    required: true
summary:
  on_success: "Completed {project} successfully"
  on_failure: "Failed to process {project}"
steps:
  - id: bad_step
    type: runner
    runner: shell
    command: "exit 1"
"""

EMIT_IN_LOOP_WORKFLOW = """\
kind: workflow
id: test_emit_loop
version: 0.1.0
inputs: {}
steps:
  - id: retry_loop
    type: loop
    max_rounds: 2
    steps:
      - id: announce
        type: emit
        message: "Loop iteration"
      - id: check
        type: runner
        runner: shell
        command: "echo checking"
"""

EMIT_IN_PARALLEL_WORKFLOW = """\
kind: workflow
id: test_emit_parallel
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    branches:
      - id: branch_a
        steps:
          - id: emit_a
            type: emit
            message: "Branch A"
      - id: branch_b
        steps:
          - id: emit_b
            type: emit
            message: "Branch B"
            level: warning
"""


class TestEmitStepDefinition:
    """Tests for emit step parsing and validation (#1150)."""

    def test_emit_step_loads(self) -> None:
        defn = load_definition(EMIT_WORKFLOW)
        emit_steps = [s for s in defn.steps if s.type == "emit"]
        assert len(emit_steps) == 2
        assert emit_steps[0].message == "Starting work on {target_name}"
        assert emit_steps[0].level == "info"
        assert emit_steps[1].level == "success"

    def test_emit_step_default_level(self) -> None:
        defn = load_definition(EMIT_WORKFLOW_DEFAULT_LEVEL)
        assert defn.steps[0].type == "emit"
        assert defn.steps[0].level is None  # defaults applied at execution time

    def test_emit_step_missing_message_fails(self) -> None:
        bad_yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: no_msg
    type: emit
"""
        with pytest.raises(ValueError, match="emit steps require a 'message' field"):
            load_definition(bad_yaml)

    def test_emit_step_invalid_level_fails(self) -> None:
        bad_yaml = """\
kind: workflow
id: bad
version: 0.1.0
inputs: {}
steps:
  - id: bad_level
    type: emit
    message: "hello"
    level: critical
"""
        with pytest.raises(ValueError, match="emit level must be one of"):
            load_definition(bad_yaml)

    def test_summary_loads(self) -> None:
        defn = load_definition(EMIT_SUMMARY_WORKFLOW)
        assert defn.summary is not None
        assert defn.summary["on_success"] == "Completed {project} successfully"
        assert defn.summary["on_failure"] == "Failed to process {project}"


class TestEmitStepExecution:
    """Tests for emit step execution (#1150)."""

    @pytest.mark.asyncio
    async def test_emit_step_executes(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={"target_name": "myproject"},
        )
        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        emitted = [e for e in events if e["event_type"] == "step_emitted"]
        assert len(emitted) == 2
        assert emitted[0]["payload"]["message"] == "Starting work on myproject"
        assert emitted[0]["payload"]["level"] == "info"
        assert emitted[1]["payload"]["message"] == "Finished myproject"
        assert emitted[1]["payload"]["level"] == "success"

    @pytest.mark.asyncio
    async def test_emit_step_default_level_is_info(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_WORKFLOW_DEFAULT_LEVEL)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={},
        )
        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        emitted = [e for e in events if e["event_type"] == "step_emitted"]
        assert len(emitted) == 1
        assert emitted[0]["payload"]["level"] == "info"

    @pytest.mark.asyncio
    async def test_emit_step_stores_level_in_artifacts(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={"target_name": "proj"},
        )
        steps = list_workflow_steps(db, run["id"])
        emit_steps = [s for s in steps if s.get("step_type") == "emit"]
        assert len(emit_steps) == 2
        for step in emit_steps:
            arts = step.get("result_artifacts") or {}
            assert "level" in arts

    @pytest.mark.asyncio
    async def test_emit_in_loop(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_IN_LOOP_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={},
        )
        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        emitted = [e for e in events if e["event_type"] == "step_emitted"]
        assert len(emitted) >= 1

    @pytest.mark.asyncio
    async def test_emit_in_parallel(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_IN_PARALLEL_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={},
        )
        assert run["status"] == "completed"
        events = list_workflow_events(db, run["id"])
        emitted = [e for e in events if e["event_type"] == "step_emitted"]
        assert len(emitted) == 2

    @pytest.mark.asyncio
    async def test_summary_on_success(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_SUMMARY_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={"project": "alpha"},
        )
        assert run["status"] == "completed"
        refreshed = get_workflow_run(db, run["id"])
        assert refreshed is not None
        assert refreshed.get("result_summary") == "Completed alpha successfully"

    @pytest.mark.asyncio
    async def test_summary_on_failure(self, engine: Any, db: Any) -> None:
        defn = load_definition(EMIT_SUMMARY_FAIL_WORKFLOW)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={"project": "beta"},
        )
        assert run["status"] == "failed"
        refreshed = get_workflow_run(db, run["id"])
        assert refreshed is not None
        assert refreshed.get("result_summary") == "Failed to process beta"

    @pytest.mark.asyncio
    async def test_summary_graceful_on_unknown_variable(self, engine: Any, db: Any) -> None:
        yaml_str = """\
kind: workflow
id: test_bad_summary
version: 0.1.0
inputs: {}
summary:
  on_success: "Done with {nonexistent_var}"
steps:
  - id: work
    type: runner
    runner: shell
    command: "echo ok"
"""
        defn = load_definition(yaml_str)
        run = await engine.start_run(
            defn,
            target_kind="generic",
            target_ref="test",
            inputs={},
        )
        # Should not crash — graceful degradation
        assert run["status"] == "completed"


# ---------------------------------------------------------------------------
# Blocked run semantics (#1141)
# ---------------------------------------------------------------------------


class TestBlockedRunSemantics:
    def test_blocked_not_in_terminal_statuses(self) -> None:
        from anteroom.services.workflow_storage import _TERMINAL_RUN_STATUSES

        assert "blocked" not in _TERMINAL_RUN_STATUSES

    @pytest.mark.asyncio
    async def test_blocked_run_no_completed_at(self, db: Any, engine: WorkflowEngine) -> None:
        """Gate blocks the workflow; completed_at should remain None."""
        defn = load_definition(GATE_FAIL_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="block-ts")
        assert run["status"] == "blocked"
        assert run.get("completed_at") is None


class TestResumableRunStatuses:
    """Tests for _RESUMABLE_RUN_STATUSES constant (#1153)."""

    def test_resumable_run_statuses_constant(self) -> None:
        from anteroom.services.workflow_storage import _RESUMABLE_RUN_STATUSES

        expected = {"paused", "waiting_for_approval", "waiting_for_input", "compensating", "failed", "blocked"}
        assert _RESUMABLE_RUN_STATUSES == expected

    def test_resumable_includes_blocked(self) -> None:
        """Regression guard: blocked must be resumable (#1141)."""
        from anteroom.services.workflow_storage import _RESUMABLE_RUN_STATUSES

        assert "blocked" in _RESUMABLE_RUN_STATUSES


# ---------------------------------------------------------------------------
# _resolve_dotted_refs tests (#1228)
# ---------------------------------------------------------------------------


class TestResolveDottedRefs:
    def test_yaml_artifact_ref_resolves(self) -> None:
        """YAML syntax: {step.artifacts.key} resolves via alias."""
        step_results = {
            "prepare_issue": {
                "result_artifacts": {"worktree_path": "/tmp/wt"},
            },
        }
        result = _resolve_dotted_refs("{prepare_issue.artifacts.worktree_path}", step_results)
        assert result == "/tmp/wt"

    def test_raw_result_artifacts_still_works(self) -> None:
        """Backward compat: {step.result_artifacts.key} still resolves."""
        step_results = {
            "prepare_issue": {
                "result_artifacts": {"worktree_path": "/tmp/wt"},
            },
        }
        result = _resolve_dotted_refs("{prepare_issue.result_artifacts.worktree_path}", step_results)
        assert result == "/tmp/wt"

    def test_env_ref_resolves(self) -> None:
        result = _resolve_dotted_refs("{env.HOME}", {}, process_env={"HOME": "/home/user"})
        assert result == "/home/user"

    def test_mixed_yaml_refs(self) -> None:
        """Shipped workflow form: {step.artifacts.key}:{env.VAR}."""
        step_results = {
            "prepare_issue": {
                "result_artifacts": {"bin": "/opt/bin"},
            },
        }
        template = "{prepare_issue.artifacts.bin}:{env.PATH}"
        result = _resolve_dotted_refs(template, step_results, process_env={"PATH": "/usr/bin"})
        assert result == "/opt/bin:/usr/bin"

    def test_shipped_workflow_working_dir(self) -> None:
        """Exact form used in shipped YAML: working_dir: '{prepare_issue.artifacts.worktree_path}'."""
        step_results = {
            "prepare_issue": {
                "result_artifacts": {"worktree_path": "/tmp/worktree"},
            },
        }
        result = _resolve_dotted_refs("{prepare_issue.artifacts.worktree_path}", step_results)
        assert result == "/tmp/worktree"

    def test_summary_alias_resolves(self) -> None:
        step_results = {"s1": {"result_summary": "all good"}}
        result = _resolve_dotted_refs("{s1.summary}", step_results)
        assert result == "all good"

    def test_status_alias_resolves(self) -> None:
        step_results = {"s1": {"result_status": "success"}}
        result = _resolve_dotted_refs("{s1.status}", step_results)
        assert result == "success"

    def test_unresolvable_left_as_is(self) -> None:
        result = _resolve_dotted_refs("{unknown.field.value}", {})
        assert result == "{unknown.field.value}"

    def test_missing_step_returns_original(self) -> None:
        result = _resolve_dotted_refs("{no_such_step.artifacts.x}", {})
        assert result == "{no_such_step.artifacts.x}"

    def test_missing_env_var_left_as_is(self) -> None:
        result = _resolve_dotted_refs("{env.NONEXISTENT_VAR_XYZ}", {}, process_env={})
        assert result == "{env.NONEXISTENT_VAR_XYZ}"

    def test_plain_braces_untouched(self) -> None:
        result = _resolve_dotted_refs("{simple_key}", {})
        assert result == "{simple_key}"

    def test_numeric_artifact_value(self) -> None:
        step_results = {"s1": {"result_artifacts": {"count": 42}}}
        result = _resolve_dotted_refs("{s1.artifacts.count}", step_results)
        assert result == "42"


# ---------------------------------------------------------------------------
# Resolved working_dir/env reach opaque runner (#1228)
# ---------------------------------------------------------------------------


class TestResolvedFieldsReachOpaqueRunner:
    @pytest.mark.asyncio
    async def test_shell_runner_receives_resolved_working_dir_and_env(self) -> None:
        """Verify that artifact refs in working_dir and env are resolved
        before being passed to execute_opaque_runner."""
        from unittest.mock import MagicMock

        from anteroom.services.workflow_runners import RunnerResult, create_default_registry

        captured: dict[str, Any] = {}

        async def fake_opaque_runner(**kwargs: Any) -> RunnerResult:
            captured.update(kwargs)
            return RunnerResult(status="success", summary="ok", duration_ms=1)

        step_def = MagicMock()
        step_def.id = "run_tests"
        step_def.runner = "shell"
        step_def.command = "echo hi"
        step_def.working_dir = "{prepare_issue.artifacts.worktree_path}"
        step_def.env = {"MY_PATH": "{prepare_issue.artifacts.bin}:{env.PATH}"}
        step_def.timeout = 30
        step_def.context_from = None
        step_def.context_from_failed_step = None
        step_def.credentials = None
        step_def.skill_name = None
        step_def.skill_args = None

        step_results = {
            "prepare_issue": {
                "result_artifacts": {
                    "worktree_path": "/tmp/worktree",
                    "bin": "/opt/bin",
                },
            },
        }

        engine = WorkflowEngine.__new__(WorkflowEngine)
        engine._config = MagicMock()
        engine._config.step_timeout = 60
        engine._config.transcript = None
        engine._runner_registry = create_default_registry()
        engine._db = MagicMock()
        engine._tool_executor = None
        engine._ai_service = None
        engine._tools_openai = None
        engine._progress_callback = None

        run = {"id": "run-1"}
        inputs: dict[str, Any] = {}

        with (
            patch(
                "anteroom.services.workflow_runners.execute_opaque_runner",
                side_effect=fake_opaque_runner,
            ),
            patch.dict("os.environ", {"PATH": "/usr/bin"}),
        ):
            await engine._execute_runner_step(step_def, run, inputs, step_results, MagicMock())

        assert captured["working_dir"] == "/tmp/worktree"
        assert captured["env"]["MY_PATH"] == "/opt/bin:/usr/bin"
