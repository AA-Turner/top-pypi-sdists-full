"""Tests for workflow LLM fallback and routing policies (#986).

Tests cover fallback field parsing/validation, primary-succeeds, primary-fails-fallback-succeeds,
all-fail, retry+fallback composition, cost accounting, event emission, empty fallback,
per-entry overrides, fallback inside loop, and fallback inside parallel branch.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import list_workflow_steps

# ---------------------------------------------------------------------------
# Test YAML definitions
# ---------------------------------------------------------------------------

LLM_FALLBACK_WORKFLOW = """\
kind: workflow
id: test_llm_fallback
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    fallback:
      - model: fallback-model-1
      - model: fallback-model-2
"""

LLM_NO_FALLBACK_WORKFLOW = """\
kind: workflow
id: test_llm_no_fallback
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
"""

LLM_FALLBACK_WITH_OVERRIDES_WORKFLOW = """\
kind: workflow
id: test_llm_fallback_overrides
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    temperature: 0.5
    max_tokens: 1024
    fallback:
      - model: fallback-model-1
        temperature: 0.0
        max_tokens: 2048
"""

LLM_FALLBACK_IN_LOOP_WORKFLOW = """\
kind: workflow
id: test_llm_fallback_loop
version: 0.1.0
inputs: {}
steps:
  - id: refine_loop
    type: loop
    max_rounds: 2
    steps:
      - id: draft
        type: llm
        prompt: "Write a draft"
        model: primary-model
        fallback:
          - model: fallback-model-1
      - id: review_gate
        type: gate
        condition: always_pass
"""

LLM_FALLBACK_IN_PARALLEL_WORKFLOW = """\
kind: workflow
id: test_llm_fallback_parallel
version: 0.1.0
inputs: {}
steps:
  - id: parallel_step
    type: parallel
    branches:
      - id: branch_a
        steps:
          - id: gen_a
            type: llm
            prompt: "Generate A"
            model: primary-model
            fallback:
              - model: fallback-model-1
      - id: branch_b
        steps:
          - id: gen_b
            type: llm
            prompt: "Generate B"
"""

LLM_FALLBACK_INVALID_NO_MODEL = """\
kind: workflow
id: test_llm_fallback_invalid
version: 0.1.0
inputs: {}
steps:
  - id: bad
    type: llm
    prompt: "Do something"
    fallback:
      - temperature: 0.5
"""

LLM_FALLBACK_ON_RUNNER = """\
kind: workflow
id: test_fallback_on_runner
version: 0.1.0
inputs: {}
steps:
  - id: bad
    type: runner
    runner: shell
    command: "echo hi"
    fallback:
      - model: nope
"""


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_ai_service(
    response_text: str = "LLM response",
    usage: dict[str, int] | None = None,
    model: str = "test-model",
) -> MagicMock:
    if usage is None:
        usage = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    svc = MagicMock()
    svc.config = MagicMock()
    svc.config.model = model
    svc.config.provider = "openai"
    svc.complete_with_usage = AsyncMock(return_value=(response_text, usage))
    return svc


@pytest.fixture()
def ai_service() -> MagicMock:
    return _make_ai_service()


@pytest.fixture()
def engine(db: Any, ai_service: MagicMock) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry, ai_service=ai_service)


@pytest.fixture(autouse=True)
def _register_test_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


# ---------------------------------------------------------------------------
# 1. Fallback field parsing
# ---------------------------------------------------------------------------


class TestFallbackParsing:
    def test_fallback_list_parsed(self) -> None:
        defn = load_definition(LLM_FALLBACK_WORKFLOW)
        step = defn.steps[0]
        assert step.fallback is not None
        assert len(step.fallback) == 2
        assert step.fallback[0]["model"] == "fallback-model-1"
        assert step.fallback[1]["model"] == "fallback-model-2"

    def test_no_fallback_field_is_none(self) -> None:
        defn = load_definition(LLM_NO_FALLBACK_WORKFLOW)
        assert defn.steps[0].fallback is None

    def test_fallback_entry_missing_model_raises(self) -> None:
        with pytest.raises(ValueError, match="must be a mapping with at least a 'model' key"):
            load_definition(LLM_FALLBACK_INVALID_NO_MODEL)

    def test_fallback_on_non_llm_step_raises(self) -> None:
        with pytest.raises(ValueError, match="'fallback' is only allowed on llm steps"):
            load_definition(LLM_FALLBACK_ON_RUNNER)

    def test_fallback_with_overrides_parsed(self) -> None:
        defn = load_definition(LLM_FALLBACK_WITH_OVERRIDES_WORKFLOW)
        step = defn.steps[0]
        assert step.fallback is not None
        assert step.fallback[0]["temperature"] == 0.0
        assert step.fallback[0]["max_tokens"] == 2048


# ---------------------------------------------------------------------------
# 2. Primary succeeds, no fallback triggered
# ---------------------------------------------------------------------------


class TestPrimarySucceeds:
    @pytest.mark.asyncio
    async def test_primary_succeeds_no_fallback(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_WORKFLOW)

        with patch("anteroom.services.ai_service.create_ai_service") as mock_create:
            primary_svc = _make_ai_service(model="primary-model")
            mock_create.return_value = primary_svc
            run = await engine.start_run(defn, target_kind="test", target_ref="t1")
            assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["fallback_used"] is False
        assert artifacts["fallback_index"] == 0
        assert artifacts["model"] == "primary-model"
        assert artifacts["primary_model"] == "primary-model"


# ---------------------------------------------------------------------------
# 3. Primary fails, fallback succeeds
# ---------------------------------------------------------------------------


class TestPrimaryFailsFallbackSucceeds:
    @pytest.mark.asyncio
    async def test_fallback_on_primary_failure(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_WORKFLOW)

        primary_svc = _make_ai_service(model="primary-model")
        primary_svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("primary down"))
        fallback_svc = _make_ai_service(response_text="fallback response", model="fallback-model-1")

        call_count = 0

        def create_side_effect(cfg: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return primary_svc
            return fallback_svc

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t2")
            assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        assert llm_step["result_status"] == "success"
        assert llm_step["result_summary"] == "fallback response"
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["fallback_used"] is True
        assert artifacts["fallback_index"] == 1
        assert artifacts["model"] == "fallback-model-1"
        assert artifacts["primary_model"] == "primary-model"


# ---------------------------------------------------------------------------
# 4. All models fail
# ---------------------------------------------------------------------------


class TestAllModelsFail:
    @pytest.mark.asyncio
    async def test_all_models_fail(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_WORKFLOW)

        failing_svc = _make_ai_service(model="any")
        failing_svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("all down"))

        with patch("anteroom.services.ai_service.create_ai_service", return_value=failing_svc):
            run = await engine.start_run(defn, target_kind="test", target_ref="t3")
            assert run["status"] == "failed"

        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        assert llm_step["result_status"] == "failed"
        assert "model(s) failed" in (llm_step["result_summary"] or "")


# ---------------------------------------------------------------------------
# 5. Retry + fallback composition (each retry runs the full chain)
# ---------------------------------------------------------------------------


LLM_FALLBACK_WITH_RETRY_WORKFLOW = """\
kind: workflow
id: test_llm_fallback_retry
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    retry:
      max_attempts: 2
      backoff: fixed
      initial_delay: 0.01
      max_delay: 0.01
    fallback:
      - model: fallback-model-1
"""


class TestRetryFallbackComposition:
    @pytest.mark.asyncio
    async def test_retry_runs_full_fallback_chain(self, db: Any, ai_service: MagicMock) -> None:
        """On first attempt, all models fail. On retry (second attempt), primary fails but fallback succeeds."""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_WITH_RETRY_WORKFLOW)

        attempt_count = 0

        def create_side_effect(cfg: Any) -> MagicMock:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count <= 2:
                # First attempt: both primary and fallback fail
                svc = _make_ai_service(model=cfg.model)
                svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("down"))
                return svc
            elif attempt_count == 3:
                # Second attempt primary: still fails
                svc = _make_ai_service(model=cfg.model)
                svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("still down"))
                return svc
            else:
                # Second attempt fallback: succeeds
                return _make_ai_service(response_text="retry fallback ok", model=cfg.model)

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t5")
            assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        llm_steps = [s for s in steps if s["step_id"] == "summarize"]
        # With retry, multiple step records exist; the last one is the successful retry
        final_step = llm_steps[-1]
        assert final_step["result_status"] == "success"
        assert final_step["result_summary"] == "retry fallback ok"


# ---------------------------------------------------------------------------
# 6. Cost accounting — artifacts["model"] is the actual model used
# ---------------------------------------------------------------------------


class TestCostAccounting:
    @pytest.mark.asyncio
    async def test_cost_uses_actual_model(self, db: Any, ai_service: MagicMock) -> None:
        model_costs = {
            "primary-model": {"input": 30.0, "output": 60.0},
            "fallback-model-1": {"input": 1.0, "output": 2.0},
        }
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service, model_costs=model_costs)
        defn = load_definition(LLM_FALLBACK_WORKFLOW)

        primary_svc = _make_ai_service(model="primary-model")
        primary_svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("down"))
        fallback_svc = _make_ai_service(
            response_text="ok",
            model="fallback-model-1",
            usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        )

        call_count = 0

        def create_side_effect(cfg: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return primary_svc
            return fallback_svc

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t6")

        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["model"] == "fallback-model-1"
        cost = engine._estimate_step_cost(artifacts)
        expected = (100 / 1_000_000) * 1.0 + (50 / 1_000_000) * 2.0
        assert abs(cost - expected) < 1e-10


# ---------------------------------------------------------------------------
# 7. llm_fallback event emitted
# ---------------------------------------------------------------------------


class TestFallbackEventEmission:
    @pytest.mark.asyncio
    async def test_fallback_event_emitted_on_failure(self, db: Any, ai_service: MagicMock) -> None:
        from anteroom.services import workflow_storage as ws

        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_WORKFLOW)

        primary_svc = _make_ai_service(model="primary-model")
        primary_svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("primary fail"))
        fallback_svc = _make_ai_service(response_text="ok", model="fallback-model-1")

        call_count = 0

        def create_side_effect(cfg: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return primary_svc
            return fallback_svc

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t7")

        events = ws.list_workflow_events(db, run["id"])
        fallback_events = [e for e in events if e["event_type"] == "llm_fallback"]
        assert len(fallback_events) >= 1
        payload = fallback_events[0].get("payload") or {}
        assert payload["failed_model"] == "primary-model"
        assert "primary fail" in payload["error"]
        assert payload["next_index"] == 1
        assert payload["remaining"] == 2


# ---------------------------------------------------------------------------
# 8. Empty fallback list — single model, behaves like before
# ---------------------------------------------------------------------------


class TestEmptyFallback:
    @pytest.mark.asyncio
    async def test_no_fallback_behaves_like_before(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_NO_FALLBACK_WORKFLOW)

        with patch("anteroom.services.ai_service.create_ai_service") as mock_create:
            svc = _make_ai_service(model="primary-model")
            mock_create.return_value = svc
            run = await engine.start_run(defn, target_kind="test", target_ref="t8")
            assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["fallback_used"] is False
        assert artifacts["fallback_index"] == 0
        assert artifacts["model"] == "primary-model"

    @pytest.mark.asyncio
    async def test_no_fallback_error_is_immediate(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_NO_FALLBACK_WORKFLOW)

        failing_svc = _make_ai_service(model="primary-model")
        failing_svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("boom"))

        with patch("anteroom.services.ai_service.create_ai_service", return_value=failing_svc):
            run = await engine.start_run(defn, target_kind="test", target_ref="t8b")
            assert run["status"] == "failed"

        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        assert llm_step["result_status"] == "failed"
        assert "model(s) failed" in (llm_step["result_summary"] or "")


# ---------------------------------------------------------------------------
# 9. Per-entry temperature/max_tokens override
# ---------------------------------------------------------------------------


class TestPerEntryOverrides:
    @pytest.mark.asyncio
    async def test_fallback_entry_overrides_temperature_and_max_tokens(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_WITH_OVERRIDES_WORKFLOW)

        primary_svc = _make_ai_service(model="primary-model")
        primary_svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("primary down"))
        fallback_svc = _make_ai_service(response_text="fb ok", model="fallback-model-1")

        call_count = 0

        def create_side_effect(cfg: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return primary_svc
            return fallback_svc

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t9")
            assert run["status"] == "completed"

        # Verify the fallback service was called with overridden params
        call_kwargs = fallback_svc.complete_with_usage.call_args[1]
        assert call_kwargs["temperature"] == 0.0
        assert call_kwargs["max_completion_tokens"] == 2048


# ---------------------------------------------------------------------------
# 10. Fallback inside loop step
# ---------------------------------------------------------------------------


class TestFallbackInLoop:
    @pytest.mark.asyncio
    async def test_fallback_works_inside_loop(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_IN_LOOP_WORKFLOW)

        call_count = 0

        def create_side_effect(cfg: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count % 2 == 1:
                # Odd calls = primary attempt (fails)
                svc = _make_ai_service(model=cfg.model)
                svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("down"))
                return svc
            else:
                # Even calls = fallback attempt (succeeds)
                return _make_ai_service(response_text="loop fallback ok", model=cfg.model)

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t10")
            assert run["status"] == "completed"


# ---------------------------------------------------------------------------
# 11. Fallback inside parallel branch
# ---------------------------------------------------------------------------


class TestFallbackInParallel:
    @pytest.mark.asyncio
    async def test_fallback_works_inside_parallel_branch(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_FALLBACK_IN_PARALLEL_WORKFLOW)

        def create_side_effect(cfg: Any) -> MagicMock:
            if cfg.model == "primary-model":
                svc = _make_ai_service(model="primary-model")
                svc.complete_with_usage = AsyncMock(side_effect=RuntimeError("branch a primary down"))
                return svc
            return _make_ai_service(response_text="branch a fallback ok", model=cfg.model)

        with patch("anteroom.services.ai_service.create_ai_service", side_effect=create_side_effect):
            run = await engine.start_run(defn, target_kind="test", target_ref="t11")
            assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        # Parallel branch steps are stored with qualified IDs: branch_id/step_id
        gen_a_steps = [s for s in steps if s["step_id"] == "branch_a/gen_a"]
        assert len(gen_a_steps) >= 1
        artifacts = gen_a_steps[0].get("result_artifacts") or {}
        assert artifacts.get("fallback_used") is True
