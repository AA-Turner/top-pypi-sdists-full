"""Regression coverage for provider-enforced typed agent output."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from typing import Literal

import pytest
from pydantic import BaseModel, Field

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.response_format import response_format_for_model


class _Finding(BaseModel):
    finding_type: Literal[
        "fact",
        "claim",
        "statistic",
        "expert_opinion",
        "definition",
        "trend",
        "example",
        "counterpoint",
    ] = "claim"


class _Claim(BaseModel):
    is_well_supported: bool = False


class _PageAnalysis(BaseModel):
    core_findings: list[_Finding] = Field(default_factory=list)
    notable_claims: list[_Claim] = Field(default_factory=list)


def test_response_format_for_model_preserves_literal_and_boolean_contract() -> None:
    response_format = response_format_for_model(_PageAnalysis).model_dump(
        mode="json", by_alias=True, exclude_none=True
    )

    assert response_format["type"] == "json_schema"
    assert response_format["json_schema"]["strict"] is True
    schema = response_format["json_schema"]["schema"]
    assert schema["$defs"]["_Finding"]["properties"]["finding_type"]["enum"] == [
        "fact",
        "claim",
        "statistic",
        "expert_opinion",
        "definition",
        "trend",
        "example",
        "counterpoint",
    ]
    assert schema["$defs"]["_Claim"]["properties"]["is_well_supported"]["type"] == "boolean"


@pytest.mark.asyncio
async def test_run_agent_replaces_schema_placeholder_before_model_call() -> None:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="structured-output-test"))
    config = UnifiedConfig.from_dict(
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Analyze this page"}],
            "response_format": {"type": "json_schema"},
        }
    )
    seen: dict[str, object] = {}

    async def execute(user_input=None):
        seen["response_format"] = config.response_format
        seen["output_schema"] = agent.output_schema
        return SimpleNamespace(
            output=json.dumps(
                {
                    "core_findings": [{"finding_type": "fact"}],
                    "notable_claims": [{"is_well_supported": True}],
                }
            ),
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="page-summary",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="Page Summary",
        source_app="test",
        source_feature="page_summary",
        json_schema=_PageAnalysis,
        emit_lifecycle=False,
    )

    assert result.success is True
    assert isinstance(result.parsed, _PageAnalysis)
    response_format = seen["response_format"]
    assert isinstance(response_format, dict)
    assert response_format["json_schema"]["schema"]
    assert seen["output_schema"] == response_format["json_schema"]


@pytest.mark.asyncio
async def test_run_agent_accepts_persisted_schema_dictionary() -> None:
    """Mandates bind the saved agent row's dictionary schema at dispatch."""
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="persisted-schema-test"))
    config = UnifiedConfig.from_dict(
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Assign topics"}],
        }
    )
    persisted_schema = {
        "type": "object",
        "properties": {"assignments": {"type": "array", "items": {"type": "object"}}},
        "required": ["assignments"],
        "additionalProperties": False,
    }

    async def execute(user_input=None):
        return SimpleNamespace(
            output=json.dumps({"assignments": []}),
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="topic-assigner",
        config=config,
        output_schema=persisted_schema,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="mandate:seo.topic_assigner",
        source_app="aidream",
        source_feature="mandate:seo.topic_assigner",
        json_schema=persisted_schema,
        emit_lifecycle=False,
    )

    assert result.success is True
    assert result.parse_error is None
    assert agent.config.response_format["json_schema"]["schema"]["properties"][
        "assignments"
    ]


@pytest.mark.asyncio
async def test_run_agent_does_not_alarm_on_unstamped_parent_when_child_source_is_explicit(
    monkeypatch,
) -> None:
    """The child boundary owns its source tags; the parent may legitimately have none."""
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    captured: list[dict[str, object]] = []

    async def record_error(_error: BaseException, **kwargs: object) -> None:
        captured.append(kwargs)

    monkeypatch.setattr(
        "matrx_ai._ext.get_ext",
        lambda name: record_error if name == "record_error" else None,
    )
    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="source-test"))
    config = UnifiedConfig.from_dict(
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Track this child"}],
        }
    )

    async def execute(user_input=None):
        return SimpleNamespace(
            output="tracked",
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="tracked-child",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="mandate:content_plan.p3_family",
        source_app="aidream",
        source_feature="mandate:content_plan.p3_family",
        system_run=True,
        emit_lifecycle=False,
    )

    await asyncio.sleep(0)
    assert result.success is True
    assert captured == []


@pytest.mark.asyncio
async def test_run_agent_still_rejects_invalid_typed_payload_after_call() -> None:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="structured-output-test"))
    config = UnifiedConfig.from_dict(
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Analyze this page"}],
        }
    )

    async def execute(user_input=None):
        return SimpleNamespace(
            output=json.dumps(
                {
                    "core_findings": [{"finding_type": "recommendation"}],
                    "notable_claims": [{"is_well_supported": "partially"}],
                }
            ),
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="page-summary",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="Page Summary",
        source_app="test",
        source_feature="page_summary",
        json_schema=_PageAnalysis,
        emit_lifecycle=False,
    )

    assert result.success is True
    assert result.parsed is None
    assert result.error_kind == "parse"
    assert result.parse_error is not None
    assert "literal_error" in result.parse_error
    assert "bool_parsing" in result.parse_error


@pytest.mark.asyncio
async def test_run_agent_does_not_parse_a_failed_completed_request() -> None:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="structured-output-test"))
    config = UnifiedConfig.from_dict(
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Analyze this oversized page"}],
        }
    )

    async def execute(user_input=None):
        return SimpleNamespace(
            output='{"partial": "provider buffer"}',
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={
                "status": "failed",
                "error_type": "context_length_exceeded",
                "error": "Your input exceeds the context window of this model.",
            },
        )

    agent = SimpleNamespace(
        name="page-summary",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="Page Summary",
        source_app="test",
        source_feature="page_summary",
        json_schema=_PageAnalysis,
        emit_lifecycle=False,
    )

    assert result.success is False
    assert result.error_kind == "execution"
    assert result.error == "Your input exceeds the context window of this model."
    assert result.output == '{"partial": "provider buffer"}'
    assert result.parsed is None
    assert result.parse_error is None


# ── extract_json_block: the whole message wins over an inner fence ───────────
# Regression, 2026-08-16: a valid raw-JSON answer whose string values CONTAIN a
# ```json fence (an agent proposing "do not wrap your answer like ```json {...}
# ```") had the inner fragment extracted and the real answer discarded. Cost: a
# $0.18 Hindsight review of ten real conversations, reported as unparseable
# while the structured-output event upstream said success.


def test_whole_message_json_beats_an_inner_json_fence():
    from matrx_ai.agents import extract_json_block

    payload = {
        "summary": "ok",
        "section_content": "Do NOT wrap your answer like this: ```json {...} ``` — output raw JSON.",
    }
    raw = json.dumps(payload)
    assert json.loads(extract_json_block(raw)) == payload


def test_whole_message_json_array_also_wins():
    from matrx_ai.agents import extract_json_block

    payload = [{"note": "``` json {\"nope\": 1} ```"}]
    raw = json.dumps(payload)
    assert json.loads(extract_json_block(raw)) == payload


def test_fenced_extraction_still_wins_when_prose_wraps_the_json():
    from matrx_ai.agents import extract_json_block

    raw = 'Here you go:\n```json\n{"a": 1}\n```\nHope that helps.'
    assert json.loads(extract_json_block(raw)) == {"a": 1}


def test_brace_scan_still_recovers_json_embedded_in_prose():
    from matrx_ai.agents import extract_json_block

    raw = 'The answer is {"a": 1} and nothing else.'
    assert json.loads(extract_json_block(raw)) == {"a": 1}
