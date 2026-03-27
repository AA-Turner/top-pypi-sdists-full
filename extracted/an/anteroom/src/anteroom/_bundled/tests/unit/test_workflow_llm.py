"""Tests for workflow LLM steps (#983).

Tests cover validation, execution, per-step model override, context_from,
template resolution, error handling, and provider complete_with_usage().
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

LLM_BASIC_WORKFLOW = """\
kind: workflow
id: test_llm_basic
version: 0.1.0
inputs:
  topic:
    type: string
    required: true
steps:
  - id: summarize
    type: llm
    prompt: "Summarize {topic}"
"""

LLM_WITH_MODEL_WORKFLOW = """\
kind: workflow
id: test_llm_model
version: 0.1.0
inputs: {}
steps:
  - id: classify
    type: llm
    prompt: "Classify this"
    model: gpt-4o-mini
    temperature: 0.2
    max_tokens: 512
"""

LLM_WITH_CONTEXT_WORKFLOW = """\
kind: workflow
id: test_llm_context
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo raw data"
  - id: analyze
    type: llm
    prompt: "Analyze the following"
    context_from:
      - step: generate
        field: result_summary
"""

LLM_WITH_SYSTEM_PROMPT_WORKFLOW = """\
kind: workflow
id: test_llm_system
version: 0.1.0
inputs: {}
steps:
  - id: translate
    type: llm
    system_prompt: "You are a translator."
    prompt: "Translate: hello world"
"""

LLM_MISSING_PROMPT_WORKFLOW = """\
kind: workflow
id: test_llm_no_prompt
version: 0.1.0
steps:
  - id: bad_step
    type: llm
"""

LLM_WITH_WHEN_WORKFLOW = """\
kind: workflow
id: test_llm_when
version: 0.1.0
inputs: {}
steps:
  - id: check
    type: runner
    runner: shell
    command: "echo ok"
  - id: conditional_llm
    type: llm
    prompt: "Only if check passed"
    when:
      step: check
      field: result_status
      equals: "nonexistent"
"""

LLM_IN_LOOP_WORKFLOW = """\
kind: workflow
id: test_llm_loop
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
      - id: review_gate
        type: gate
        condition: always_pass
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


@pytest.fixture()
def engine_no_ai(db: Any) -> WorkflowEngine:
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
# Validation tests
# ---------------------------------------------------------------------------


class TestLlmValidation:
    def test_llm_step_parses(self) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        assert defn.steps[0].type == "llm"
        assert defn.steps[0].prompt == "Summarize {topic}"

    def test_llm_requires_prompt(self) -> None:
        with pytest.raises(ValueError, match="requires a 'prompt' field"):
            load_definition(LLM_MISSING_PROMPT_WORKFLOW)

    def test_llm_model_optional(self) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        assert defn.steps[0].model is None

    def test_llm_model_temperature_max_tokens_parsed(self) -> None:
        defn = load_definition(LLM_WITH_MODEL_WORKFLOW)
        step = defn.steps[0]
        assert step.model == "gpt-4o-mini"
        assert step.temperature == 0.2
        assert step.max_tokens == 512


# ---------------------------------------------------------------------------
# Execution tests
# ---------------------------------------------------------------------------


class TestLlmExecution:
    @pytest.mark.asyncio
    async def test_basic_llm_step(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t1", inputs={"topic": "AI safety"})
        assert run["status"] == "completed"

        ai_service.complete_with_usage.assert_called_once()
        call_args = ai_service.complete_with_usage.call_args
        messages = call_args[0][0]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert "AI safety" in messages[0]["content"]

    @pytest.mark.asyncio
    async def test_llm_response_stored(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t2", inputs={"topic": "testing"})
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        assert llm_step["result_status"] == "success"
        assert llm_step["result_summary"] == "LLM response"

    @pytest.mark.asyncio
    async def test_llm_artifacts_have_tokens(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t3", inputs={"topic": "tokens"})
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["prompt_tokens"] == 10
        assert artifacts["completion_tokens"] == 20
        assert artifacts["total_tokens"] == 30
        assert artifacts["model"] == "test-model"

    @pytest.mark.asyncio
    async def test_llm_with_system_prompt(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_WITH_SYSTEM_PROMPT_WORKFLOW)
        await engine.start_run(defn, target_kind="test", target_ref="t4")
        messages = ai_service.complete_with_usage.call_args[0][0]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "translator" in messages[0]["content"]
        assert messages[1]["role"] == "user"

    @pytest.mark.asyncio
    async def test_llm_model_override_creates_new_service(self, db: Any, ai_service: MagicMock) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_WITH_MODEL_WORKFLOW)

        with patch("anteroom.services.ai_service.create_ai_service") as mock_create:
            override_svc = _make_ai_service(model="gpt-4o-mini")
            mock_create.return_value = override_svc
            run = await engine.start_run(defn, target_kind="test", target_ref="t5")
            assert run["status"] == "completed"
            mock_create.assert_called_once()
            override_svc.complete_with_usage.assert_called_once()

    @pytest.mark.asyncio
    async def test_llm_context_from_resolved(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_WITH_CONTEXT_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="t6")
        assert run["status"] == "completed"
        messages = ai_service.complete_with_usage.call_args[0][0]
        user_msg = messages[-1]["content"]
        assert "--- Context ---" in user_msg

    @pytest.mark.asyncio
    async def test_llm_template_vars_resolved(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        await engine.start_run(defn, target_kind="test", target_ref="t7", inputs={"topic": "quantum computing"})
        messages = ai_service.complete_with_usage.call_args[0][0]
        assert "quantum computing" in messages[0]["content"]

    @pytest.mark.asyncio
    async def test_llm_max_tokens_passed(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_WITH_MODEL_WORKFLOW)
        with patch("anteroom.services.ai_service.create_ai_service") as mock_create:
            override_svc = _make_ai_service(model="gpt-4o-mini")
            mock_create.return_value = override_svc
            await engine.start_run(defn, target_kind="test", target_ref="t8")
            call_kwargs = override_svc.complete_with_usage.call_args[1]
            assert call_kwargs["max_completion_tokens"] == 512


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TestLlmIntegration:
    @pytest.mark.asyncio
    async def test_full_engine_run(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="int1", inputs={"topic": "integration"})
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        assert len(steps) == 1
        assert steps[0]["step_type"] == "llm"

    @pytest.mark.asyncio
    async def test_llm_inside_loop(self, db: Any) -> None:
        ai_service = _make_ai_service()
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_IN_LOOP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="int2")
        assert run["status"] == "completed"
        assert ai_service.complete_with_usage.call_count >= 1

    @pytest.mark.asyncio
    async def test_llm_with_when_skipped(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_WITH_WHEN_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="int3")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "conditional_llm"][0]
        assert llm_step["status"] == "skipped"


# ---------------------------------------------------------------------------
# Error tests
# ---------------------------------------------------------------------------


class TestLlmErrors:
    @pytest.mark.asyncio
    async def test_ai_error_returns_failed(self, db: Any) -> None:
        ai_service = _make_ai_service()
        ai_service.complete_with_usage = AsyncMock(side_effect=RuntimeError("API down"))
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_BASIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="err1", inputs={"topic": "error"})
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        assert llm_step["result_status"] == "failed"
        assert "model(s) failed" in (llm_step["result_summary"] or "")

    @pytest.mark.asyncio
    async def test_no_ai_service_returns_failed(self, engine_no_ai: WorkflowEngine, db: Any) -> None:
        defn = load_definition(LLM_BASIC_WORKFLOW)
        run = await engine_no_ai.start_run(defn, target_kind="test", target_ref="err2", inputs={"topic": "no ai"})
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "summarize"][0]
        assert llm_step["result_status"] == "failed"
        assert "requires ai_service" in (llm_step["result_summary"] or "")


# ---------------------------------------------------------------------------
# Provider complete_with_usage tests
# ---------------------------------------------------------------------------


class TestProviderCompleteWithUsage:
    @pytest.mark.asyncio
    async def test_openai_complete_with_usage(self) -> None:
        from anteroom.services.ai_service import AIService

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 5
        mock_response.usage.completion_tokens = 3
        mock_response.usage.total_tokens = 8

        config = MagicMock()
        config.model = "gpt-4o"
        config.provider = "openai"
        config.api_key = "test-key"
        config.base_url = "https://api.openai.com/v1"
        config.api_key_command = None

        service = AIService.__new__(AIService)
        service.config = config
        service.client = MagicMock()
        service.client.chat.completions.create = AsyncMock(return_value=mock_response)
        service._token_provider = None

        text, usage = await service.complete_with_usage(
            [{"role": "user", "content": "Hi"}],
            max_completion_tokens=100,
        )
        assert text == "Hello"
        assert usage["prompt_tokens"] == 5
        assert usage["completion_tokens"] == 3
        assert usage["total_tokens"] == 8

    @pytest.mark.asyncio
    async def test_openai_complete_with_usage_no_usage(self) -> None:
        from anteroom.services.ai_service import AIService

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello"
        mock_response.usage = None

        service = AIService.__new__(AIService)
        service.config = MagicMock()
        service.config.model = "gpt-4o"
        service.client = MagicMock()
        service.client.chat.completions.create = AsyncMock(return_value=mock_response)
        service._token_provider = None

        text, usage = await service.complete_with_usage(
            [{"role": "user", "content": "Hi"}],
        )
        assert text == "Hello"
        assert usage == {}

    @pytest.mark.asyncio
    async def test_openai_complete_with_usage_temperature(self) -> None:
        from anteroom.services.ai_service import AIService

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Cold"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 1
        mock_response.usage.completion_tokens = 1
        mock_response.usage.total_tokens = 2

        service = AIService.__new__(AIService)
        service.config = MagicMock()
        service.config.model = "gpt-4o"
        service.client = MagicMock()
        service.client.chat.completions.create = AsyncMock(return_value=mock_response)
        service._token_provider = None

        await service.complete_with_usage(
            [{"role": "user", "content": "Hi"}],
            temperature=0.0,
        )
        call_kwargs = service.client.chat.completions.create.call_args[1]
        assert call_kwargs["temperature"] == 0.0
