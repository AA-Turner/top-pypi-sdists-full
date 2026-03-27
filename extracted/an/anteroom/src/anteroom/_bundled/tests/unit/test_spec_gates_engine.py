"""Engine-level integration tests — workflow with spec gates blocks until phase approved."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from anteroom.services.workflow_engine import load_definition

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""

GATED_WORKFLOW = """\
kind: workflow
id: test-gated
version: "1.0"
steps:
  - id: check-requirements
    type: gate
    condition: spec_requirements_approved
    if_false: "Requirements not yet approved"
  - id: check-design
    type: gate
    condition: spec_design_approved
    if_false: "Design not yet approved"
  - id: final-step
    type: gate
    condition: always_pass
"""

SINGLE_GATE_WORKFLOW = """\
kind: workflow
id: test-single-gate
version: "1.0"
steps:
  - id: check-reqs
    type: gate
    condition: spec_requirements_approved
  - id: done
    type: gate
    condition: always_pass
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture(autouse=True)
def _register_gates(db: Any) -> None:
    from anteroom.services.spec_gates import register_spec_gates
    from anteroom.services.workflow_engine import register_gate_condition

    register_spec_gates(db)

    async def always_pass(run: dict, step: Any, inputs: dict) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)


@pytest.fixture()
def engine(db: Any) -> Any:
    from anteroom.config import WorkflowConfig
    from anteroom.services.workflow_engine import WorkflowEngine
    from anteroom.services.workflow_runners import create_default_registry

    return WorkflowEngine(db, WorkflowConfig(), create_default_registry())


@pytest.fixture()
def spec_fqn(db: Any) -> str:
    from anteroom.services.spec_service import create_spec

    create_spec(db, "ns", "feat", VALID_SPEC_YAML)
    return "@ns/spec/feat"


# ---------------------------------------------------------------------------
# Full engine execution
# ---------------------------------------------------------------------------


class TestSpecGateEngineIntegration:
    @pytest.mark.asyncio
    async def test_gate_blocks_on_draft(self, engine: Any, spec_fqn: str) -> None:
        """Workflow should block at first gate when phase is draft."""
        definition = load_definition(SINGLE_GATE_WORKFLOW)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={"spec_fqn": spec_fqn})
        assert run["status"] == "blocked"
        assert run.get("stop_reason") is not None

    @pytest.mark.asyncio
    async def test_gate_passes_after_approval(self, db: Any, engine: Any, spec_fqn: str) -> None:
        """Workflow should pass gate and complete when phase is approved."""
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, spec_fqn, "requirements", "troy")

        definition = load_definition(SINGLE_GATE_WORKFLOW)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={"spec_fqn": spec_fqn})
        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_multi_gate_blocks_at_second(self, db: Any, engine: Any, spec_fqn: str) -> None:
        """Workflow with multiple gates blocks at the first unapproved phase."""
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, spec_fqn, "requirements", "troy")
        # design is still draft

        definition = load_definition(GATED_WORKFLOW)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={"spec_fqn": spec_fqn})
        assert run["status"] == "blocked"
        stop = run.get("stop_reason") or ""
        assert "design" in stop.lower()
        assert "draft" in stop.lower()

    @pytest.mark.asyncio
    async def test_multi_gate_passes_all(self, db: Any, engine: Any, spec_fqn: str) -> None:
        """Workflow completes when all gated phases are approved."""
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, spec_fqn, "requirements", "troy")
        approve_phase(db, spec_fqn, "design", "troy")

        definition = load_definition(GATED_WORKFLOW)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={"spec_fqn": spec_fqn})
        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_gate_blocks_with_dynamic_reason(self, engine: Any, spec_fqn: str) -> None:
        """GateResult.reason is used when if_false is not set on the step."""
        definition = load_definition(SINGLE_GATE_WORKFLOW)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={"spec_fqn": spec_fqn})
        # The SINGLE_GATE_WORKFLOW has no if_false, so the GateResult.reason should be used
        assert run["status"] == "blocked"
        stop = run.get("stop_reason") or ""
        assert "requirements" in stop.lower()
        assert "draft" in stop.lower()

    @pytest.mark.asyncio
    async def test_gate_blocks_missing_spec(self, engine: Any) -> None:
        """Workflow blocks with clear reason when spec doesn't exist."""
        definition = load_definition(SINGLE_GATE_WORKFLOW)
        run = await engine.start_run(
            definition,
            target_kind="spec",
            target_ref="test",
            inputs={"spec_fqn": "@ns/spec/nonexistent"},
        )
        assert run["status"] == "blocked"
        assert "not found" in (run.get("stop_reason") or "")

    @pytest.mark.asyncio
    async def test_gate_blocks_missing_input(self, engine: Any) -> None:
        """Workflow blocks when spec_fqn is not in inputs."""
        definition = load_definition(SINGLE_GATE_WORKFLOW)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={})
        assert run["status"] == "blocked"
        assert "spec_fqn" in (run.get("stop_reason") or "")


# ---------------------------------------------------------------------------
# GateResult backward compat in engine execution
# ---------------------------------------------------------------------------


class TestGateResultEngineBackwardCompat:
    @pytest.mark.asyncio
    async def test_bool_gate_still_works_in_engine(self, engine: Any) -> None:
        """Bool-returning gates must still pass through the engine."""
        workflow = """\
kind: workflow
id: test-bool
version: "1.0"
steps:
  - id: pass
    type: gate
    condition: always_pass
"""
        definition = load_definition(workflow)
        run = await engine.start_run(definition, target_kind="spec", target_ref="test", inputs={})
        assert run["status"] == "completed"


# ---------------------------------------------------------------------------
# Bootstrap registration — verifies gates are available without manual setup
# ---------------------------------------------------------------------------


class TestSpecGateBootstrapRegistration:
    def test_gates_registered_after_register_spec_gates(self, db: Any) -> None:
        """Verify register_spec_gates wires all three conditions into the registry."""
        from anteroom.services.workflow_engine import _gate_registry

        # Clear any test-registered gates to simulate fresh state
        for name in ["spec_requirements_approved", "spec_design_approved", "spec_tasks_approved"]:
            _gate_registry.pop(name, None)

        from anteroom.services.spec_gates import register_spec_gates

        register_spec_gates(db)

        from anteroom.services.workflow_engine import get_gate_condition

        assert get_gate_condition("spec_requirements_approved") is not None
        assert get_gate_condition("spec_design_approved") is not None
        assert get_gate_condition("spec_tasks_approved") is not None

    def test_idempotent_registration(self, db: Any) -> None:
        """Calling register_spec_gates twice does not error."""
        from anteroom.services.spec_gates import register_spec_gates

        register_spec_gates(db)
        register_spec_gates(db)

        from anteroom.services.workflow_engine import get_gate_condition

        assert get_gate_condition("spec_requirements_approved") is not None
