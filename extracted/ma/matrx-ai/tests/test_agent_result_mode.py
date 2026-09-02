"""Tests for result_mode on agent tool calls (Pattern 2 — descriptor returns).

reference: the child's output goes to the host's value store (injected writer)
and the caller's tool_result carries ONLY the bounded descriptor; the child's
stream is suppressed. inline_once: full output now AND stored. No writer
configured → loud degrade to inline (standalone matrx-ai has no store).
"""
from __future__ import annotations

from typing import Any

import pytest

import matrx_ai._ext as ext
from matrx_ai.tools.agent_projection import _variable_definitions_to_parameters
from matrx_ai.tools.agent_tool import (
    _capture_agent_tool_boundary_failure,
    execute_agent_tool,
)
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType


@pytest.fixture()
def writer_capture():
    captured: dict[str, Any] = {}

    async def fake_writer(**kwargs):
        captured.update(kwargs)
        return {
            "key": "stored-key",
            "description": kwargs["description"],
            "kind": "text",
            "chars": len(str(kwargs["value"])),
            "truncated": False,
            "preview": str(kwargs["value"])[:20],
            "json_keys": None,
            "fence": "```matrx\n{...}\n```",
        }

    before = ext._registry.get("conversation_value_writer")
    ext.configure_ext(conversation_value_writer=fake_writer)
    yield captured
    if before is None:
        ext._registry.pop("conversation_value_writer", None)
    else:
        ext._registry["conversation_value_writer"] = before


def _reference_tool(result_mode: str = "reference") -> ToolDefinition:
    params = _variable_definitions_to_parameters(None)
    params["result_key"] = {"type": "string", "required": False, "description": "x"}
    params["result_description"] = {"type": "string", "required": False, "description": "x"}
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        prompt_id="abc-123",
        result_mode=result_mode,
        parameters=params,
    )


def _patch_agent(monkeypatch, captured: dict[str, Any], output: str = "A" * 5000):
    class _FakeAgent:
        name = "researcher"
        source_id = "abc-123"
        output_schema = None

    async def fake_from_agent(agent_id, is_version=False, variables=None, **kw):
        captured["variables"] = variables
        return _FakeAgent()

    async def fake_run_agent(agent, *, label, source_feature, user_input, suppress_stream=False, **_kw):
        captured["suppress_stream"] = suppress_stream
        captured["allow_client_delegation"] = _kw.get("allow_client_delegation")
        captured["require_complete_output"] = _kw.get("require_complete_output")
        captured["user_input"] = user_input
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(success=True, output=output)

    import matrx_ai.agents.definition as definition_mod
    import matrx_ai.agents.executor as executor_mod

    monkeypatch.setattr(
        definition_mod.Agent, "from_agent", classmethod(
            lambda cls, agent_id, is_version=False, variables=None, **kw: fake_from_agent(
                agent_id, is_version=is_version, variables=variables, **kw
            )
        ),
    )
    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)


@pytest.mark.asyncio
async def test_reference_mode_returns_descriptor_only(monkeypatch, writer_capture):
    run_capture: dict[str, Any] = {}
    _patch_agent(monkeypatch, run_capture)

    result = await execute_agent_tool(
        _reference_tool("reference"),
        {
            "input": "pull the transcript",
            "result_key": "acme-transcript",
            "result_description": "Full ACME Q3 call transcript",
        },
        ToolContext(call_id="call-9", recursion_depth=1),
    )

    assert result.success is True
    assert result.output_self_capped is True
    # The caller sees the descriptor, never the 5000-char output.
    assert result.output["key"] == "stored-key"
    assert "A" * 100 not in str(result.output)
    # The writer received the dispatch-consumed naming args…
    assert writer_capture["key"] == "acme-transcript"
    assert writer_capture["description"] == "Full ACME Q3 call transcript"
    assert writer_capture["source_call_id"] == "call-9"
    # …which were NOT routed as agent variables.
    assert run_capture["variables"] == {}
    # The child's stream was suppressed.
    assert run_capture["suppress_stream"] is True
    assert run_capture["allow_client_delegation"] is False
    assert run_capture["require_complete_output"] is True


@pytest.mark.asyncio
async def test_inline_once_returns_both(monkeypatch, writer_capture):
    run_capture: dict[str, Any] = {}
    _patch_agent(monkeypatch, run_capture, output="short answer")

    result = await execute_agent_tool(
        _reference_tool("inline_once"),
        {"input": "do it"},
        ToolContext(call_id="c", recursion_depth=1),
    )
    assert result.success is True
    assert result.output["result"] == "short answer"
    assert result.output["stored"]["key"] == "stored-key"
    # inline_once still streams (only pure reference mode silences the child).
    assert run_capture["suppress_stream"] is False
    assert run_capture["allow_client_delegation"] is False


@pytest.mark.asyncio
async def test_inline_agent_tool_returns_structured_json_natively(monkeypatch):
    run_capture: dict[str, Any] = {}
    _patch_agent(
        monkeypatch,
        run_capture,
        output='{"__kind":"electronics_intake_analysis","products":[]}',
    )

    result = await execute_agent_tool(
        _reference_tool("inline"),
        {"input": "inspect"},
        ToolContext(call_id="structured-call", recursion_depth=1),
    )

    assert result.success is True
    assert result.output == {
        "__kind": "electronics_intake_analysis",
        "products": [],
    }


@pytest.mark.asyncio
async def test_agent_tool_boundary_failure_creates_structured_capture(monkeypatch):
    captured: list[tuple[BaseException, dict[str, Any]]] = []

    async def fake_capture(exc: BaseException, **fields: Any) -> None:
        captured.append((exc, fields))

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture,
    )
    ctx = ToolContext(call_id="boundary-call")

    await _capture_agent_tool_boundary_failure(
        RuntimeError("forced boundary failure"),
        tool_def=_reference_tool("inline"),
        ctx=ctx,
    )

    assert len(captured) == 1
    assert captured[0][1]["kind"] == "agent_tool_result_boundary_failed"
    assert captured[0][1]["route"] == "tool_executor.agent_tool_result"
    assert captured[0][1]["context"] == {
        "tool_name": "custom_tool_1",
        "call_id": "boundary-call",
    }


@pytest.mark.asyncio
async def test_reference_mode_degrades_loudly_without_writer(monkeypatch):
    before = ext._registry.pop("conversation_value_writer", None)
    try:
        run_capture: dict[str, Any] = {}
        _patch_agent(monkeypatch, run_capture, output="full text")

        result = await execute_agent_tool(
            _reference_tool("reference"),
            {"input": "go"},
            ToolContext(call_id="c", recursion_depth=1),
        )
        assert result.success is True
        assert result.output == "full text"  # inline degrade
    finally:
        if before is not None:
            ext._registry["conversation_value_writer"] = before


@pytest.mark.asyncio
async def test_truncated_child_never_stores_a_value(monkeypatch, writer_capture):
    # A truncated child (output token limit hit mid-run) is treated like
    # paused (matching the summary mapping truncated→paused, commit 6bc8bbf5a):
    # its cut-off output must never be minted as a stored value; the call
    # fails with a resumable child_truncated reason.
    class _FakeAgent:
        name = "researcher"
        source_id = "abc-123"
        output_schema = None

    async def fake_from_agent(agent_id, is_version=False, variables=None, **kw):
        return _FakeAgent()

    async def fake_run_agent(agent, *, label, source_feature, user_input, suppress_stream=False, **_kw):
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(
            success=True,
            output="A cut-off mid-sentence resul",
            metadata={"status": "truncated"},
        )

    import matrx_ai.agents.definition as definition_mod
    import matrx_ai.agents.executor as executor_mod

    monkeypatch.setattr(
        definition_mod.Agent, "from_agent", classmethod(
            lambda cls, agent_id, is_version=False, variables=None, **kw: fake_from_agent(
                agent_id, is_version=is_version, variables=variables, **kw
            )
        ),
    )
    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)

    result = await execute_agent_tool(
        _reference_tool("reference"),
        {"input": "go", "result_key": "k"},
        ToolContext(call_id="c", recursion_depth=1),
    )
    assert result.success is False
    assert result.error.error_type == "child_truncated"
    assert result.error.is_retryable is True
    # No value was stored — the writer was never called.
    assert "key" not in writer_capture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("output", "status", "error_type"),
    [
        ("partial garbage", "failed", "agent_failed"),
        ("", "completed", "agent_empty_response"),
    ],
)
async def test_incomplete_child_never_mints_a_stored_value(
    monkeypatch,
    writer_capture,
    output,
    status,
    error_type,
):
    class _FakeAgent:
        name = "researcher"
        source_id = "abc-123"
        output_schema = None

    async def fake_from_agent(agent_id, is_version=False, variables=None, **kw):
        return _FakeAgent()

    async def fake_run_agent(agent, **_kwargs):
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(
            success=True,
            output=output,
            metadata={"status": status},
        )

    import matrx_ai.agents.definition as definition_mod
    import matrx_ai.agents.executor as executor_mod

    monkeypatch.setattr(
        definition_mod.Agent,
        "from_agent",
        classmethod(
            lambda cls, agent_id, is_version=False, variables=None, **kw: fake_from_agent(
                agent_id,
                is_version=is_version,
                variables=variables,
                **kw,
            )
        ),
    )
    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)

    result = await execute_agent_tool(
        _reference_tool("reference"),
        {"input": "go", "result_key": "must-not-exist"},
        ToolContext(call_id="c", recursion_depth=1),
    )

    assert result.success is False
    assert result.error.error_type == error_type
    assert "key" not in writer_capture


@pytest.mark.asyncio
async def test_writer_failure_fails_the_tool(monkeypatch):
    async def exploding_writer(**kwargs):
        raise RuntimeError("store down")

    before = ext._registry.get("conversation_value_writer")
    ext.configure_ext(conversation_value_writer=exploding_writer)
    try:
        run_capture: dict[str, Any] = {}
        _patch_agent(monkeypatch, run_capture)

        result = await execute_agent_tool(
            _reference_tool("reference"),
            {"input": "go"},
            ToolContext(call_id="c", recursion_depth=1),
        )
        # A dangling descriptor must never be returned — the tool call fails.
        assert result.success is False
        assert "store down" in result.error.message
    finally:
        if before is None:
            ext._registry.pop("conversation_value_writer", None)
        else:
            ext._registry["conversation_value_writer"] = before
