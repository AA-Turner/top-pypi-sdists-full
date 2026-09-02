"""Unit tests for ``ai.agent.tool_calling`` / ``ai.agent.react`` schemas + ReAct trace builder."""

from __future__ import annotations

import pytest
from matrx_ai.graph_nodes.agent_loop_actions import (
    AgentLoopInput,
    AgentReactResult,
    ReActStep,
    _build_react_trace,
    _coerce_text,
    _extract_thought,
    _parse_tool_call,
)
from matrx_ai.graph_nodes.shared import AiExecutionResult, AiMessage, AiUsage
from pydantic import ValidationError


def test_agent_loop_input_defaults():
    inp = AgentLoopInput(model="m", user_input="u")
    assert inp.max_iterations == 100
    assert inp.tools == []


def test_agent_loop_input_max_iterations_bounds():
    AgentLoopInput(model="m", user_input="u", max_iterations=1)
    AgentLoopInput(model="m", user_input="u", max_iterations=500)
    with pytest.raises(ValidationError):
        AgentLoopInput(model="m", user_input="u", max_iterations=0)
    with pytest.raises(ValidationError):
        AgentLoopInput(model="m", user_input="u", max_iterations=501)


def test_react_step_default_observation_empty():
    s = ReActStep(iteration=0, thought="t")
    assert s.observation == ""
    assert s.action_input == {}


def test_react_step_rejects_extra():
    with pytest.raises(ValidationError):
        ReActStep(iteration=0, thought="t", extra="x")  # type: ignore[call-arg]


def test_extract_thought_strips_prefix():
    assert _extract_thought("Thought: I should use the search tool") == "I should use the search tool"
    assert _extract_thought("THOUGHT: hi") == "hi"
    assert _extract_thought("no prefix here") == "no prefix here"


def test_coerce_text_handles_none_str_list_dict():
    assert _coerce_text(None) == ""
    assert _coerce_text("hi") == "hi"
    assert _coerce_text(["a", "b"]) == "ab"
    assert _coerce_text([{"type": "text", "text": "X"}, {"type": "text", "text": "Y"}]) == "XY"
    assert _coerce_text(123) == "123"


def test_parse_tool_call_dict_with_function_shape():
    call = {"id": "c1", "function": {"name": "tool_a", "arguments": '{"k": "v"}'}}
    name, args, call_id = _parse_tool_call(call)
    assert name == "tool_a"
    assert args == {"k": "v"}
    assert call_id == "c1"


def test_parse_tool_call_dict_with_input_shape():
    call = {"tool_call_id": "x1", "name": "tool_b", "input": {"a": 1}}
    name, args, call_id = _parse_tool_call(call)
    assert name == "tool_b"
    assert args == {"a": 1}
    assert call_id == "x1"


def test_parse_tool_call_handles_string_args_that_are_not_json():
    call = {"name": "t", "input": "not-json"}
    _, args, _ = _parse_tool_call(call)
    assert args == {"raw": "not-json"}


def test_build_react_trace_empty_messages():
    assert _build_react_trace([]) == []


def test_build_react_trace_single_assistant_no_tools():
    messages = [AiMessage(role="user", content="hi"), AiMessage(role="assistant", content="Thought: I think... here is the answer")]
    trace = _build_react_trace(messages)
    assert len(trace) == 1
    assert trace[0].action is None
    assert "I think" in trace[0].thought


def test_build_react_trace_assistant_with_tool_then_observation():
    messages = [
        AiMessage(role="user", content="please search"),
        AiMessage(
            role="assistant",
            content="Thought: I will search now",
            tool_calls=[{"id": "t1", "name": "search", "input": {"q": "X"}}],
        ),
        AiMessage(role="tool", content="found Z", tool_call_id="t1"),
        AiMessage(role="assistant", content="Final answer is Z"),
    ]
    trace = _build_react_trace(messages)
    assert len(trace) == 2
    assert trace[0].action == "search"
    assert trace[0].action_input == {"q": "X"}
    assert trace[0].observation == "found Z"
    assert trace[1].action is None
    assert "Final answer is Z" in trace[1].thought


def test_agent_react_result_holds_underlying():
    underlying = AiExecutionResult(
        conversation_id="c1",
        request_id="r1",
        iterations=2,
        final_text="answer",
        usage=AiUsage(),
    )
    result = AgentReactResult(
        final_text="answer",
        react_trace=[ReActStep(iteration=0, thought="think", action=None)],
        iterations=2,
        tool_calls_made=0,
        underlying=underlying,
    )
    dumped = result.model_dump()
    assert dumped["final_text"] == "answer"
    assert dumped["underlying"]["conversation_id"] == "c1"
