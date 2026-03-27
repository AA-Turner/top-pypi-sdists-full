"""Tests for workflow cost and token tracking (#963).

Token tracking is always-on (not gated on budget). Cost estimation
uses model_costs rates passed to WorkflowEngine.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from anteroom.config import WorkflowBudgetConfig, WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import WorkflowEngine, load_definition
from anteroom.services.workflow_runners import RunnerResult, create_default_registry
from anteroom.services.workflow_storage import get_workflow_run

# ---------------------------------------------------------------------------
# Test YAML (domain-neutral)
# ---------------------------------------------------------------------------

ONE_STEP_WORKFLOW = """\
kind: workflow
id: test_cost
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hello"
"""

TWO_STEP_WORKFLOW = """\
kind: workflow
id: test_cost_two
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo two"
"""

BUDGET_WORKFLOW = """\
kind: workflow
id: test_cost_budget
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 10
    max_tokens: 100000
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo one"
  - id: step_two
    type: runner
    runner: shell
    command: "echo two"
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
def registry():
    return create_default_registry()


def _make_engine(
    db: Any,
    config: WorkflowConfig,
    registry: Any,
    *,
    model_costs: dict[str, dict[str, float]] | None = None,
) -> WorkflowEngine:
    return WorkflowEngine(db, config, registry, model_costs=model_costs)


async def _token_runner(**kwargs: Any) -> RunnerResult:
    return RunnerResult(
        status="success",
        summary="done",
        duration_ms=10,
        artifacts={
            "total_tokens": 100,
            "prompt_tokens": 70,
            "completion_tokens": 30,
            "model": "gpt-4o",
        },
    )


async def _zero_token_runner(**kwargs: Any) -> RunnerResult:
    return RunnerResult(status="success", summary="done", duration_ms=10)


# ===========================================================================
# Token tracking without budget
# ===========================================================================


class TestTokenTrackingWithoutBudget:
    @pytest.mark.asyncio
    async def test_token_tracking_without_budget(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Token tracking works even when no budget is configured."""
        engine = _make_engine(db, config, registry)
        defn = load_definition(ONE_STEP_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-1")

        assert run["status"] == "completed"
        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"] is not None
        assert stored["budget_usage"]["total_tokens"] == 100
        assert stored["budget_usage"]["prompt_tokens"] == 70
        assert stored["budget_usage"]["completion_tokens"] == 30
        assert stored["budget_usage"]["steps_completed"] == 1

    @pytest.mark.asyncio
    async def test_token_tracking_with_budget(self, db: Any, registry: Any) -> None:
        """Token tracking works alongside budget enforcement."""
        cfg = WorkflowConfig(budget=WorkflowBudgetConfig(max_steps=10, max_tokens=100000))
        engine = _make_engine(db, cfg, registry)
        defn = load_definition(BUDGET_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-2")

        assert run["status"] == "completed"
        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"]["total_tokens"] == 200  # 2 steps * 100
        assert stored["budget"] is not None
        assert stored["budget"]["max_tokens"] == 100000


# ===========================================================================
# Model name in artifacts
# ===========================================================================


class TestModelNameInArtifacts:
    @pytest.mark.asyncio
    async def test_model_name_in_artifacts(self) -> None:
        """Agent runner includes model name in result artifacts."""
        from anteroom.services.agent_loop import AgentEvent
        from anteroom.services.workflow_runners import execute_agent_runner

        mock_events = [
            AgentEvent(kind="token", data={"content": "hello"}),
            AgentEvent(kind="usage", data={"prompt_tokens": 50, "completion_tokens": 25}),
        ]

        async def mock_agent_loop(**kwargs: Any) -> Any:
            for event in mock_events:
                yield event

        from unittest.mock import AsyncMock

        mock_ai = AsyncMock()
        mock_executor = AsyncMock(return_value={"status": "ok"})

        with patch("anteroom.services.agent_loop.run_agent_loop", side_effect=mock_agent_loop):
            result = await execute_agent_runner(
                prompt="test",
                ai_service=mock_ai,
                tool_executor=mock_executor,
                tools_openai=[],
                model="gpt-4o",
            )

        assert result.artifacts["model"] == "gpt-4o"

    @pytest.mark.asyncio
    async def test_model_name_defaults_to_empty(self) -> None:
        """Agent runner defaults model to empty string when not provided."""
        from anteroom.services.agent_loop import AgentEvent
        from anteroom.services.workflow_runners import execute_agent_runner

        mock_events = [AgentEvent(kind="token", data={"content": "hi"})]

        async def mock_agent_loop(**kwargs: Any) -> Any:
            for event in mock_events:
                yield event

        from unittest.mock import AsyncMock

        mock_ai = AsyncMock()
        mock_executor = AsyncMock(return_value={"status": "ok"})

        with patch("anteroom.services.agent_loop.run_agent_loop", side_effect=mock_agent_loop):
            result = await execute_agent_runner(
                prompt="test",
                ai_service=mock_ai,
                tool_executor=mock_executor,
                tools_openai=[],
            )

        assert result.artifacts["model"] == ""


# ===========================================================================
# Cost estimation
# ===========================================================================


class TestCostEstimation:
    def test_cost_estimation_known_model(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Known model with rates produces correct cost."""
        model_costs = {"gpt-4o": {"input": 2.50, "output": 10.00}}
        engine = _make_engine(db, config, registry, model_costs=model_costs)
        artifacts = {"model": "gpt-4o", "prompt_tokens": 1_000_000, "completion_tokens": 500_000}
        cost = engine._estimate_step_cost(artifacts)
        expected = (1_000_000 / 1_000_000) * 2.50 + (500_000 / 1_000_000) * 10.00
        assert cost == pytest.approx(expected)

    def test_cost_estimation_unknown_model(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Unknown model returns 0 cost."""
        model_costs = {"gpt-4o": {"input": 2.50, "output": 10.00}}
        engine = _make_engine(db, config, registry, model_costs=model_costs)
        artifacts = {"model": "unknown-model", "prompt_tokens": 1000, "completion_tokens": 500}
        assert engine._estimate_step_cost(artifacts) == 0.0

    def test_cost_estimation_no_model_costs(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Engine without model_costs returns 0 cost."""
        engine = _make_engine(db, config, registry)
        artifacts = {"model": "gpt-4o", "prompt_tokens": 1000, "completion_tokens": 500}
        assert engine._estimate_step_cost(artifacts) == 0.0

    def test_cost_estimation_missing_model_key(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Artifacts without model key returns 0 cost."""
        model_costs = {"gpt-4o": {"input": 2.50, "output": 10.00}}
        engine = _make_engine(db, config, registry, model_costs=model_costs)
        artifacts = {"prompt_tokens": 1000, "completion_tokens": 500}
        assert engine._estimate_step_cost(artifacts) == 0.0


# ===========================================================================
# Mixed runners and accumulation
# ===========================================================================


class TestTokenAccumulation:
    @pytest.mark.asyncio
    async def test_mixed_runner_tokens(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Shell steps contribute 0 tokens; agent steps contribute actual tokens."""
        engine = _make_engine(db, config, registry)
        defn = load_definition(TWO_STEP_WORKFLOW)

        call_count = 0

        async def _mixed_runner(**kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return RunnerResult(status="success", summary="done", duration_ms=10)
            return RunnerResult(
                status="success",
                summary="done",
                duration_ms=10,
                artifacts={"total_tokens": 200, "prompt_tokens": 120, "completion_tokens": 80},
            )

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mixed_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-mix")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"]["total_tokens"] == 200
        assert stored["budget_usage"]["prompt_tokens"] == 120
        assert stored["budget_usage"]["completion_tokens"] == 80

    @pytest.mark.asyncio
    async def test_token_accumulation_across_steps(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """Two steps with tokens sum correctly."""
        engine = _make_engine(db, config, registry)
        defn = load_definition(TWO_STEP_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-accum")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"]["total_tokens"] == 200
        assert stored["budget_usage"]["prompt_tokens"] == 140
        assert stored["budget_usage"]["completion_tokens"] == 60
        assert stored["budget_usage"]["steps_completed"] == 2

    @pytest.mark.asyncio
    async def test_budget_usage_always_persisted(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """budget_usage_json is never None after a step completes."""
        engine = _make_engine(db, config, registry)
        defn = load_definition(ONE_STEP_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_zero_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-persist")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"] is not None
        assert stored["budget_usage"]["steps_completed"] == 1

    @pytest.mark.asyncio
    async def test_estimated_cost_in_budget_usage(self, db: Any, config: WorkflowConfig, registry: Any) -> None:
        """estimated_cost_usd is present in stored budget_usage."""
        model_costs = {"gpt-4o": {"input": 2.50, "output": 10.00}}
        engine = _make_engine(db, config, registry, model_costs=model_costs)
        defn = load_definition(ONE_STEP_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-est")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        usage = stored["budget_usage"]
        assert "estimated_cost_usd" in usage
        expected = (70 / 1_000_000) * 2.50 + (30 / 1_000_000) * 10.00
        assert usage["estimated_cost_usd"] == pytest.approx(expected)

    @pytest.mark.asyncio
    async def test_estimated_cost_zero_without_model_costs(
        self, db: Any, config: WorkflowConfig, registry: Any
    ) -> None:
        """Without model_costs, estimated_cost_usd is 0."""
        engine = _make_engine(db, config, registry)
        defn = load_definition(ONE_STEP_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_token_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cost-zero")

        stored = get_workflow_run(db, run["id"])
        assert stored is not None
        assert stored["budget_usage"]["estimated_cost_usd"] == 0.0
