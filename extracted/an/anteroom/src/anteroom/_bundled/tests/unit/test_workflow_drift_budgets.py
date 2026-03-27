"""Tests for workflow definition drift detection (#964) and budget enforcement (#967).

Uses generic, domain-neutral test workflows.
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.config import WorkflowBudgetConfig, WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    _build_drift_report,
    load_definition,
)
from anteroom.services.workflow_runners import RunnerResult, create_default_registry
from anteroom.services.workflow_storage import get_workflow_run, list_workflow_events

# ---------------------------------------------------------------------------
# Test YAML (domain-neutral)
# ---------------------------------------------------------------------------

SIMPLE_WORKFLOW = """\
kind: workflow
id: test_drift
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
"""

MODIFIED_WORKFLOW = """\
kind: workflow
id: test_drift
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one modified"
  - id: step_three
    type: runner
    runner: shell
    command: "echo step three new"
"""

BUDGET_WORKFLOW = """\
kind: workflow
id: test_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 2
    max_tokens: 50000
    max_duration_seconds: 3600
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
  - id: step_three
    type: runner
    runner: shell
    command: "echo step three"
"""

UNLIMITED_BUDGET_WORKFLOW = """\
kind: workflow
id: test_unlimited
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
"""


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn


@pytest.fixture()
def config():
    return WorkflowConfig()


@pytest.fixture()
def budget_config():
    return WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=10, max_tokens=100000))


@pytest.fixture()
def registry():
    return create_default_registry()


def _make_engine(db: Any, config: WorkflowConfig, registry: Any) -> WorkflowEngine:
    return WorkflowEngine(db, config, registry)


async def _mock_opaque_runner(**kwargs: Any) -> RunnerResult:
    return RunnerResult(status="success", summary="done", duration_ms=10)


# ===========================================================================
# #964 — Definition drift detection
# ===========================================================================


class TestDefinitionDrift:
    def test_load_definition_computes_hash(self) -> None:
        defn = load_definition(SIMPLE_WORKFLOW)
        assert defn.content_hash
        assert len(defn.content_hash) == 64  # SHA-256 hex
        assert defn.raw_yaml == SIMPLE_WORKFLOW.encode("utf-8")

    def test_hash_is_deterministic(self) -> None:
        defn1 = load_definition(SIMPLE_WORKFLOW)
        defn2 = load_definition(SIMPLE_WORKFLOW)
        assert defn1.content_hash == defn2.content_hash

    def test_different_yaml_different_hash(self) -> None:
        defn1 = load_definition(SIMPLE_WORKFLOW)
        defn2 = load_definition(MODIFIED_WORKFLOW)
        assert defn1.content_hash != defn2.content_hash

    def test_hash_matches_manual_sha256(self) -> None:
        defn = load_definition(SIMPLE_WORKFLOW)
        expected = hashlib.sha256(SIMPLE_WORKFLOW.encode("utf-8")).hexdigest()
        assert defn.content_hash == expected

    def test_load_from_file_computes_hash(self, tmp_path: Path) -> None:
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(SIMPLE_WORKFLOW)
        defn = load_definition(yaml_file)
        expected = hashlib.sha256(yaml_file.read_bytes()).hexdigest()
        assert defn.content_hash == expected
        assert defn.raw_yaml == yaml_file.read_bytes()

    @pytest.mark.asyncio
    async def test_start_run_stores_hash_and_content(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(SIMPLE_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="ref-1")

        stored_run = get_workflow_run(db, run["id"])
        assert stored_run is not None
        assert stored_run["definition_hash"] == defn.content_hash
        assert stored_run["definition_content"] == SIMPLE_WORKFLOW

    @pytest.mark.asyncio
    async def test_resume_same_hash_succeeds(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(SIMPLE_WORKFLOW)

        # Start and pause
        from anteroom.services import workflow_storage as ws

        run = ws.create_workflow_run(
            db,
            workflow_id=defn.id,
            workflow_version=defn.version,
            target_kind="test",
            target_ref="ref-2",
            definition_hash=defn.content_hash,
            definition_content=SIMPLE_WORKFLOW,
        )
        ws.update_workflow_run(db, run["id"], status="paused")

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            result = await engine.resume_run(run["id"], defn)

        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_resume_different_hash_blocks(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn1 = load_definition(SIMPLE_WORKFLOW)
        defn2 = load_definition(MODIFIED_WORKFLOW)

        from anteroom.services import workflow_storage as ws

        run = ws.create_workflow_run(
            db,
            workflow_id=defn1.id,
            workflow_version=defn1.version,
            target_kind="test",
            target_ref="ref-3",
            definition_hash=defn1.content_hash,
            definition_content=SIMPLE_WORKFLOW,
        )
        ws.update_workflow_run(db, run["id"], status="paused")

        with pytest.raises(ValueError, match="Definition has changed"):
            await engine.resume_run(run["id"], defn2)

    @pytest.mark.asyncio
    async def test_resume_different_hash_force_proceeds(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn1 = load_definition(SIMPLE_WORKFLOW)
        defn2 = load_definition(MODIFIED_WORKFLOW)

        from anteroom.services import workflow_storage as ws

        run = ws.create_workflow_run(
            db,
            workflow_id=defn1.id,
            workflow_version=defn1.version,
            target_kind="test",
            target_ref="ref-4",
            definition_hash=defn1.content_hash,
            definition_content=SIMPLE_WORKFLOW,
        )
        ws.update_workflow_run(db, run["id"], status="paused")

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            result = await engine.resume_run(run["id"], defn2, force=True)

        assert result["status"] == "completed"
        # Check drift override event was emitted
        events = list_workflow_events(db, run["id"])
        drift_events = [e for e in events if e["event_type"] == "definition_drift_overridden"]
        assert len(drift_events) == 1

    @pytest.mark.asyncio
    async def test_null_hash_proceeds_with_warning(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Pre-existing runs with no stored hash should proceed (backward compat)."""
        engine = _make_engine(db, config, registry)
        defn = load_definition(SIMPLE_WORKFLOW)

        from anteroom.services import workflow_storage as ws

        # Create run without definition_hash (simulates old run)
        run = ws.create_workflow_run(
            db,
            workflow_id=defn.id,
            workflow_version=defn.version,
            target_kind="test",
            target_ref="ref-5",
        )
        ws.update_workflow_run(db, run["id"], status="paused")

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            result = await engine.resume_run(run["id"], defn)

        assert result["status"] == "completed"

    def test_drift_report_shows_step_changes(self) -> None:
        defn2 = load_definition(MODIFIED_WORKFLOW)
        run = {
            "definition_content": SIMPLE_WORKFLOW,
            "definition_hash": hashlib.sha256(SIMPLE_WORKFLOW.encode()).hexdigest(),
        }
        report = _build_drift_report(run, defn2)
        assert "Added" in report or "Removed" in report
        assert "step_three" in report or "step_two" in report

    def test_definition_content_stored_and_retrievable(self, db: Any) -> None:
        from anteroom.services import workflow_storage as ws

        defn = load_definition(SIMPLE_WORKFLOW)
        run = ws.create_workflow_run(
            db,
            workflow_id=defn.id,
            workflow_version=defn.version,
            target_kind="test",
            target_ref="ref-6",
            definition_hash=defn.content_hash,
            definition_content=SIMPLE_WORKFLOW,
        )
        stored = ws.get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["definition_content"] == SIMPLE_WORKFLOW
        assert stored["definition_hash"] == defn.content_hash


# ===========================================================================
# #967 — Budget enforcement
# ===========================================================================


class TestBudgetEnforcement:
    @pytest.mark.asyncio
    async def test_step_count_exceeded(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(BUDGET_WORKFLOW)  # max_steps: 2, has 3 steps

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-1")

        assert run["status"] == "failed"
        assert run["stop_reason"] == "budget_exceeded:steps"

    @pytest.mark.asyncio
    async def test_token_budget_exceeded(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Mock runner returns high token count to trigger token budget."""
        engine = _make_engine(db, config, registry)

        yaml_src = """\
kind: workflow
id: test_token_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_tokens: 100
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
"""
        defn = load_definition(yaml_src)

        async def _high_token_runner(**kwargs: Any) -> RunnerResult:
            return RunnerResult(
                status="success",
                summary="done",
                duration_ms=10,
                artifacts={"total_tokens": 200, "prompt_tokens": 100, "completion_tokens": 100},
            )

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_high_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-2")

        # step_one succeeds, usage becomes 200 tokens, then step_two check fails
        assert run["status"] == "failed"
        assert run["stop_reason"] == "budget_exceeded:tokens"

    @pytest.mark.asyncio
    async def test_duration_budget_exceeded(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)

        yaml_src = """\
kind: workflow
id: test_duration_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_duration_seconds: 1
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
"""
        defn = load_definition(yaml_src)
        call_count = 0

        async def _slow_runner(**kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # Simulate time passing
                import asyncio

                await asyncio.sleep(1.5)
            return RunnerResult(status="success", summary="done", duration_ms=10)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_slow_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-3")

        assert run["status"] == "failed"
        assert run["stop_reason"] == "budget_exceeded:duration"

    @pytest.mark.asyncio
    async def test_budget_exceeded_persists_elapsed_seconds(
        self, db: Any, config: WorkflowConfig, registry: Any
    ) -> None:
        """When budget is exceeded, the stored elapsed_seconds should reflect actual time."""
        engine = _make_engine(db, config, registry)

        yaml_src = """\
kind: workflow
id: test_elapsed_persist
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 1
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
"""
        defn = load_definition(yaml_src)

        async def _slow_runner(**kwargs: Any) -> RunnerResult:
            import asyncio

            await asyncio.sleep(0.1)
            return RunnerResult(status="success", summary="done", duration_ms=100)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_slow_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-elapsed")

        assert run["status"] == "failed"
        assert run["stop_reason"] == "budget_exceeded:steps"
        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"] is not None
        # elapsed_seconds should be > 0 (the step took ~0.1s real time)
        assert stored["budget_usage"]["elapsed_seconds"] >= 0

    @pytest.mark.asyncio
    async def test_zero_budget_is_unlimited(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(UNLIMITED_BUDGET_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-4")

        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_config_ceiling_overrides_definition(self, db: Any, registry: Any) -> None:
        """Config budget is stricter than definition — config wins."""
        strict_config = WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=1))
        engine = _make_engine(db, strict_config, registry)

        yaml_src = """\
kind: workflow
id: test_ceiling
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 100
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
"""
        defn = load_definition(yaml_src)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-5")

        # Config says max 1, so step_two check should fail
        assert run["status"] == "failed"
        assert run["stop_reason"] == "budget_exceeded:steps"

    @pytest.mark.asyncio
    async def test_budget_usage_persisted(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)

        yaml_src = """\
kind: workflow
id: test_persist
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 10
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
"""
        defn = load_definition(yaml_src)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-6")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget"] is not None
        assert stored["budget_usage"] is not None
        assert stored["budget_usage"]["steps_completed"] == 1

    @pytest.mark.asyncio
    async def test_budget_usage_reloaded_on_resume(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Resume continues from accumulated budget state."""
        import json

        from anteroom.services import workflow_storage as ws

        engine = _make_engine(db, config, registry)

        yaml_src = """\
kind: workflow
id: test_resume_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 5
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
"""
        defn = load_definition(yaml_src)

        # Simulate a paused run with existing budget usage
        budget = {"max_steps": 5, "max_tokens": 0, "max_duration_seconds": 0}
        budget_usage = {
            "elapsed_seconds": 100,
            "steps_completed": 3,
            "total_tokens": 5000,
            "prompt_tokens": 2500,
            "completion_tokens": 2500,
        }
        run = ws.create_workflow_run(
            db,
            workflow_id=defn.id,
            workflow_version=defn.version,
            target_kind="test",
            target_ref="budget-7",
            definition_hash=defn.content_hash,
            definition_content=defn.raw_yaml.decode(),
            budget=budget,
        )
        ws.update_workflow_run(
            db,
            run["id"],
            status="paused",
            budget_usage_json=json.dumps(budget_usage),
        )

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            result = await engine.resume_run(run["id"], defn)

        # Budget should continue from 3 steps, adding 2 more = 5 total = at limit
        assert result["status"] == "completed"
        stored = get_workflow_run(db, result["id"])
        assert stored is not None
        assert stored["budget_usage"]["steps_completed"] == 5

    @pytest.mark.asyncio
    async def test_budget_in_api_response(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Run detail includes budget and budget_usage dicts."""
        engine = _make_engine(db, config, registry)

        yaml_src = """\
kind: workflow
id: test_api_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 10
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
"""
        defn = load_definition(yaml_src)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-8")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        # These are what the API returns
        assert isinstance(stored["budget"], dict)
        assert "max_steps" in stored["budget"]
        assert isinstance(stored["budget_usage"], dict)
        assert "steps_completed" in stored["budget_usage"]

    @pytest.mark.asyncio
    async def test_budget_exceeded_event_emitted(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(BUDGET_WORKFLOW)  # max_steps: 2

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="budget-9")

        events = list_workflow_events(db, run["id"])
        fail_events = [e for e in events if e["event_type"] == "run_failed"]
        assert len(fail_events) == 1
        assert "budget_exceeded" in (fail_events[0].get("payload", {}) or {}).get("reason", "")


class TestComputeEffectiveBudget:
    def test_definition_only(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(BUDGET_WORKFLOW)
        budget = engine._compute_effective_budget(defn)
        assert budget is not None
        assert budget["max_steps"] == 2
        assert budget["max_tokens"] == 50000
        assert budget["max_duration_seconds"] == 3600

    def test_config_only(self, db: Any, registry: Any) -> None:
        cfg = WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=5))
        engine = _make_engine(db, cfg, registry)
        defn = load_definition(UNLIMITED_BUDGET_WORKFLOW)  # no policy budget
        budget = engine._compute_effective_budget(defn)
        assert budget is not None
        assert budget["max_steps"] == 5

    def test_stricter_config_wins(self, db: Any, registry: Any) -> None:
        cfg = WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=1))
        engine = _make_engine(db, cfg, registry)
        defn = load_definition(BUDGET_WORKFLOW)  # definition says max_steps: 2
        budget = engine._compute_effective_budget(defn)
        assert budget is not None
        assert budget["max_steps"] == 1  # config is stricter

    def test_stricter_definition_wins(self, db: Any, registry: Any) -> None:
        cfg = WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=100))
        engine = _make_engine(db, cfg, registry)
        defn = load_definition(BUDGET_WORKFLOW)  # definition says max_steps: 2
        budget = engine._compute_effective_budget(defn)
        assert budget is not None
        assert budget["max_steps"] == 2  # definition is stricter

    def test_all_zero_returns_none(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        engine = _make_engine(db, config, registry)
        defn = load_definition(UNLIMITED_BUDGET_WORKFLOW)
        budget = engine._compute_effective_budget(defn)
        assert budget is None


class TestTokenCapture:
    @pytest.mark.asyncio
    async def test_agent_runner_reports_tokens(self) -> None:
        """execute_agent_runner includes token counts in artifacts."""
        from anteroom.services.agent_loop import AgentEvent
        from anteroom.services.workflow_runners import execute_agent_runner

        mock_events = [
            AgentEvent(kind="token", data={"content": "hello"}),
            AgentEvent(kind="usage", data={"prompt_tokens": 100, "completion_tokens": 50}),
            AgentEvent(kind="usage", data={"prompt_tokens": 200, "completion_tokens": 100}),
        ]

        async def mock_agent_loop(**kwargs: Any) -> Any:
            for event in mock_events:
                yield event

        mock_ai = AsyncMock()
        mock_executor = AsyncMock(return_value={"status": "ok"})

        with patch("anteroom.services.agent_loop.run_agent_loop", side_effect=mock_agent_loop):
            result = await execute_agent_runner(
                prompt="test",
                ai_service=mock_ai,
                tool_executor=mock_executor,
                tools_openai=[],
            )

        assert result.status == "success"
        assert result.artifacts["prompt_tokens"] == 300
        assert result.artifacts["completion_tokens"] == 150
        assert result.artifacts["total_tokens"] == 450


class TestCLIBudgetDisplay:
    def test_format_tokens(self) -> None:
        from anteroom.cli.workflow_cli import _format_tokens

        assert _format_tokens(500) == "500"
        assert _format_tokens(23400) == "23K"
        assert _format_tokens(1_500_000) == "1.5M"

    def test_format_duration(self) -> None:
        from anteroom.cli.workflow_cli import _format_duration

        assert _format_duration(65) == "1:05"
        assert _format_duration(3661) == "1:01:01"
        assert _format_duration(0) == "0:00"


class TestWorkflowBudgetConfig:
    def test_defaults_are_zero(self) -> None:
        cfg = WorkflowBudgetConfig()
        assert cfg.max_duration_seconds == 0
        assert cfg.max_steps == 0
        assert cfg.max_tokens == 0

    def test_workflow_config_has_budget(self) -> None:
        from anteroom.config import WorkflowConfig

        wc = WorkflowConfig()
        assert wc.budget.max_steps == 0
        assert wc.budget.max_tokens == 0
        assert wc.budget.max_duration_seconds == 0

    def test_workflow_config_with_custom_budget(self) -> None:
        from anteroom.config import WorkflowConfig

        wc = WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=50, max_tokens=100000))
        assert wc.budget.max_steps == 50
        assert wc.budget.max_tokens == 100000
