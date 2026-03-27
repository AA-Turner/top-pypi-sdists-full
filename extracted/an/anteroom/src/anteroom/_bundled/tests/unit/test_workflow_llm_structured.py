"""Tests for structured output mode in workflow LLM steps (#984).

Tests cover response_format validation, JSON parsing, artifact storage,
provider-specific behavior, error handling, and retry recovery.
"""

from __future__ import annotations

import json
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

LLM_JSON_WORKFLOW = """\
kind: workflow
id: test_llm_json
version: 0.1.0
inputs:
  query:
    type: string
    required: true
steps:
  - id: extract
    type: llm
    prompt: "Extract entities from: {query}"
    response_format: json_object
"""

LLM_JSON_WITH_SYSTEM_WORKFLOW = """\
kind: workflow
id: test_llm_json_system
version: 0.1.0
inputs: {}
steps:
  - id: parse
    type: llm
    system_prompt: "You are a parser."
    prompt: "Parse this data"
    response_format: json_object
"""

LLM_INVALID_FORMAT_WORKFLOW = """\
kind: workflow
id: test_llm_bad_format
version: 0.1.0
steps:
  - id: bad
    type: llm
    prompt: "test"
    response_format: xml
"""

RUNNER_WITH_FORMAT_WORKFLOW = """\
kind: workflow
id: test_runner_format
version: 0.1.0
steps:
  - id: bad
    type: runner
    runner: shell
    command: "echo hi"
    response_format: json_object
"""

LLM_JSON_CONTEXT_FROM_WORKFLOW = """\
kind: workflow
id: test_llm_json_ctx
version: 0.1.0
inputs: {}
steps:
  - id: extract
    type: llm
    prompt: "Extract data"
    response_format: json_object
  - id: use_data
    type: llm
    prompt: "Use the extracted data"
    context_from:
      - step: extract
        field: result_artifacts.structured_output
"""

LLM_JSON_WITH_RETRY_WORKFLOW = """\
kind: workflow
id: test_llm_json_retry
version: 0.1.0
inputs: {}
steps:
  - id: flaky
    type: llm
    prompt: "Return JSON"
    response_format: json_object
    retry:
      max_attempts: 2
      backoff: fixed
      initial_delay: 1
"""


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_ai_service(
    response_text: str = '{"result": "ok"}',
    usage: dict[str, int] | None = None,
    model: str = "test-model",
    provider: str = "openai",
) -> MagicMock:
    if usage is None:
        usage = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    svc = MagicMock()
    svc.config = MagicMock()
    svc.config.model = model
    svc.config.provider = provider
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
# Validation tests
# ---------------------------------------------------------------------------


class TestResponseFormatValidation:
    def test_response_format_parsed(self) -> None:
        defn = load_definition(LLM_JSON_WORKFLOW)
        assert defn.steps[0].response_format == "json_object"

    def test_response_format_only_on_llm(self) -> None:
        with pytest.raises(ValueError, match="response_format is only allowed on llm steps"):
            load_definition(RUNNER_WITH_FORMAT_WORKFLOW)

    def test_response_format_only_json_object(self) -> None:
        with pytest.raises(ValueError, match="response_format must be 'json_object'"):
            load_definition(LLM_INVALID_FORMAT_WORKFLOW)


# ---------------------------------------------------------------------------
# Execution tests
# ---------------------------------------------------------------------------


class TestStructuredOutputExecution:
    @pytest.mark.asyncio
    async def test_json_response_stored_in_artifacts(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(LLM_JSON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="j1", inputs={"query": "test"})
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "extract"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["structured_output"] == {"result": "ok"}

    @pytest.mark.asyncio
    async def test_invalid_json_fails_step(self, db: Any) -> None:
        ai_service = _make_ai_service(response_text="not json at all")
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="j2", inputs={"query": "bad"})
        assert run["status"] == "failed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "extract"][0]
        assert llm_step["result_status"] == "failed"
        assert "not valid JSON" in (llm_step["result_summary"] or "")

    @pytest.mark.asyncio
    async def test_raw_response_in_failure_artifacts(self, db: Any) -> None:
        ai_service = _make_ai_service(response_text="oops not json")
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="j3", inputs={"query": "fail"})
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "extract"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts.get("raw_response") == "oops not json"

    @pytest.mark.asyncio
    async def test_empty_json_accepted(self, db: Any) -> None:
        ai_service = _make_ai_service(response_text="{}")
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="j4", inputs={"query": "empty"})
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "extract"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["structured_output"] == {}

    @pytest.mark.asyncio
    async def test_openai_passes_response_format(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        defn = load_definition(LLM_JSON_WORKFLOW)
        await engine.start_run(defn, target_kind="test", target_ref="j5", inputs={"query": "test"})
        call_kwargs = ai_service.complete_with_usage.call_args[1]
        assert call_kwargs["response_format"] == {"type": "json_object"}

    @pytest.mark.asyncio
    async def test_anthropic_provider_system_prompt(self, db: Any) -> None:
        ai_service = _make_ai_service(response_text='{"ok": true}', provider="anthropic")
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WORKFLOW)
        await engine.start_run(defn, target_kind="test", target_ref="j6", inputs={"query": "test"})
        messages = ai_service.complete_with_usage.call_args[0][0]
        # With no explicit system_prompt, the JSON instruction becomes the system message
        system_msgs = [m for m in messages if m["role"] == "system"]
        assert len(system_msgs) == 1
        assert "Respond with valid JSON only" in system_msgs[0]["content"]

    @pytest.mark.asyncio
    async def test_anthropic_appends_to_existing_system_prompt(self, db: Any) -> None:
        ai_service = _make_ai_service(response_text='{"ok": true}', provider="anthropic")
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WITH_SYSTEM_WORKFLOW)
        await engine.start_run(defn, target_kind="test", target_ref="j7")
        messages = ai_service.complete_with_usage.call_args[0][0]
        system_msgs = [m for m in messages if m["role"] == "system"]
        assert len(system_msgs) == 1
        assert "You are a parser." in system_msgs[0]["content"]
        assert "Respond with valid JSON only" in system_msgs[0]["content"]

    @pytest.mark.asyncio
    async def test_openai_no_extra_system_prompt(self, engine: WorkflowEngine, ai_service: MagicMock, db: Any) -> None:
        """OpenAI provider should NOT append the JSON instruction to system prompt."""
        defn = load_definition(LLM_JSON_WORKFLOW)
        await engine.start_run(defn, target_kind="test", target_ref="j8", inputs={"query": "test"})
        messages = ai_service.complete_with_usage.call_args[0][0]
        system_msgs = [m for m in messages if m["role"] == "system"]
        assert len(system_msgs) == 0  # No system prompt for OpenAI (native response_format)


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TestStructuredOutputIntegration:
    @pytest.mark.asyncio
    async def test_structured_output_in_step_results(self, db: Any) -> None:
        """Downstream step can see structured_output via context_from."""
        json_response = json.dumps({"title": "Test", "score": 42})
        ai_service = _make_ai_service(response_text=json_response)
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_CONTEXT_FROM_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="int1")
        assert run["status"] == "completed"
        # The second call should have context injected
        assert ai_service.complete_with_usage.call_count == 2
        second_call_messages = ai_service.complete_with_usage.call_args_list[1][0][0]
        user_msg = second_call_messages[-1]["content"]
        assert "Context" in user_msg

    @pytest.mark.asyncio
    async def test_engine_integration_structured(self, db: Any) -> None:
        """Full engine run with JSON structured output."""
        response = json.dumps({"entities": ["Alice", "Bob"], "count": 2})
        ai_service = _make_ai_service(response_text=response)
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WORKFLOW)
        run = await engine.start_run(defn, target_kind="test", target_ref="int2", inputs={"query": "Find entities"})
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        llm_step = [s for s in steps if s["step_id"] == "extract"][0]
        artifacts = llm_step.get("result_artifacts") or {}
        assert artifacts["structured_output"]["entities"] == ["Alice", "Bob"]
        assert artifacts["structured_output"]["count"] == 2

    @pytest.mark.asyncio
    async def test_structured_output_in_safe_artifact_keys(self) -> None:
        """Checkpoint sanitization preserves structured_output."""
        assert "structured_output" in WorkflowEngine._SAFE_ARTIFACT_KEYS

    @pytest.mark.asyncio
    async def test_retry_recovers_from_invalid_json(self, db: Any) -> None:
        """First attempt returns invalid JSON, second returns valid JSON."""
        call_count = 0
        usage = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}

        async def side_effect(*args: Any, **kwargs: Any) -> tuple[str, dict[str, int]]:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ("not json", usage)
            return ('{"recovered": true}', usage)

        ai_service = _make_ai_service()
        ai_service.complete_with_usage = AsyncMock(side_effect=side_effect)
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry, ai_service=ai_service)
        defn = load_definition(LLM_JSON_WITH_RETRY_WORKFLOW)

        async def _no_delay(seconds: float) -> None:
            pass

        with patch.object(WorkflowEngine, "_retry_delay", staticmethod(_no_delay)):
            run = await engine.start_run(defn, target_kind="test", target_ref="retry1")
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        flaky_steps = [s for s in steps if s["step_id"] == "flaky"]
        # Last attempt is the successful one
        successful = [s for s in flaky_steps if s.get("result_status") == "success"]
        assert len(successful) == 1
        artifacts = successful[0].get("result_artifacts") or {}
        assert artifacts["structured_output"] == {"recovered": True}
