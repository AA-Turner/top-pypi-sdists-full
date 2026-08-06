"""Unit tests for the shared tool-call activity reporting utility and its
integration with ``Tool.ainvoke`` and the agno hook.

These tests avoid live HTTP by patching ``APIClient.make_request``; they do
not require real credentials or a running backend.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any, Dict, List

import pytest
from unittest.mock import AsyncMock, patch

from xpander_sdk.models.events import (
    TaskUpdateEventType,
    ToolCallRequestReasoning,
)
from xpander_sdk.modules.backend.utils.tool_call_events import (
    AGNO_INTERNAL_TEAM_TOOLS,
    DEFAULT_MAX_CONTENT_LENGTH,
    DEFAULT_PREVIEW_LENGTH,
    PLANNING_TOOLS,
    REASONING_TOOLS,
    TOOL_CALL_SUMMARY_PRESET,
    coerce_json_like,
    extract_plan_task_id,
    extract_reasoning,
    is_agent_gateway_task,
    is_reasoning_tool,
    report_reasoning_event,
    report_tool_call_request,
    report_tool_call_result,
    resolve_plan_task_id,
    shape_result_for_activity,
    should_skip_tool_report,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _FakeTask(SimpleNamespace):
    """Minimal Task stand-in. The helper only reads id/org/configuration."""


def _make_fake_task(
    task_id: str = "task-1", org_id: str = "org-1", payload_extension=None
) -> _FakeTask:
    # Configuration only needs to be a simple object that APIClient can accept.
    from xpander_sdk.models.configuration import Configuration

    return _FakeTask(
        id=task_id,
        organization_id=org_id,
        payload_extension=payload_extension,
        configuration=Configuration(api_key="test", organization_id=org_id),
    )


def _make_gateway_task(task_id: str = "task-1", org_id: str = "org-1") -> _FakeTask:
    """Fake task carrying the agent-gateway header in payload_extension."""
    return _make_fake_task(
        task_id=task_id,
        org_id=org_id,
        payload_extension={"headers": {"x-is-from-agent-gateway": "true"}},
    )


async def _wait_for_background_tasks() -> None:
    """Yield enough times to let asyncio.create_task-scheduled coroutines run."""
    for _ in range(6):
        await asyncio.sleep(0)


# ---------------------------------------------------------------------------
# shape_result_for_activity
# ---------------------------------------------------------------------------


def test_shape_result_returns_small_values_unchanged():
    assert shape_result_for_activity("hello") == "hello"
    assert shape_result_for_activity({"a": 1}) == {"a": 1}
    assert shape_result_for_activity(None) is None


def test_shape_result_truncates_large_strings():
    big = "x" * (DEFAULT_MAX_CONTENT_LENGTH + 500)
    shaped = shape_result_for_activity(big)
    assert isinstance(shaped, str)
    assert "[TRUNCATED OUTPUT" in shaped
    # The preview portion is exactly preview_length characters of the input.
    assert shaped.startswith("x" * DEFAULT_PREVIEW_LENGTH)
    assert len(shaped) < len(big)


def test_shape_result_truncates_large_dicts_via_json():
    big_dict = {"items": ["y" * 20] * 1000}
    shaped = shape_result_for_activity(big_dict)
    assert isinstance(shaped, str)
    assert "[TRUNCATED OUTPUT" in shaped


def test_shape_result_with_skip_truncation_keeps_full_content():
    big = "z" * (DEFAULT_MAX_CONTENT_LENGTH + 5_000)
    shaped = shape_result_for_activity(big, skip_truncation=True)
    # Full content preserved, no truncation marker.
    assert shaped == big
    assert "[TRUNCATED OUTPUT" not in shaped


# ---------------------------------------------------------------------------
# coerce_json_like
# ---------------------------------------------------------------------------


def test_coerce_json_like_parses_json_string_dict():
    assert coerce_json_like('{"a": 1, "b": [2, 3]}') == {"a": 1, "b": [2, 3]}


def test_coerce_json_like_parses_json_string_list():
    assert coerce_json_like('[1, 2, {"x": "y"}]') == [1, 2, {"x": "y"}]


def test_coerce_json_like_parses_python_literal_dict():
    # Single-quoted Python literal; json.loads would fail, ast.literal_eval should handle it.
    assert coerce_json_like("{'a': 1, 'b': 'two'}") == {"a": 1, "b": "two"}


def test_coerce_json_like_leaves_plain_strings_alone():
    assert coerce_json_like("hello world") == "hello world"
    # Looks like an identifier, not a dict/list.
    assert coerce_json_like("42") == "42"


def test_coerce_json_like_recurses_into_dicts_and_lists():
    value = {
        "outer": '{"inner": 5}',
        "list": ["[1, 2]", {"nested_str": '{"k": "v"}'}],
    }
    assert coerce_json_like(value) == {
        "outer": {"inner": 5},
        "list": [[1, 2], {"nested_str": {"k": "v"}}],
    }


def test_coerce_json_like_pass_through_primitives():
    assert coerce_json_like(None) is None
    assert coerce_json_like(123) == 123
    assert coerce_json_like(1.5) == 1.5
    assert coerce_json_like(True) is True


def test_coerce_json_like_returns_original_on_parse_failure():
    # Starts with { but is not a valid JSON/literal dict.
    assert coerce_json_like("{not valid") == "{not valid"


def test_coerce_json_like_parses_payload_with_literal_control_chars():
    # The LLM sometimes emits a tool ``payload`` as a JSON string whose nested
    # ``content`` carries raw newlines/tabs (e.g. file-write of HTML). Strict
    # json.loads rejects those control chars; the strict=False fallback must
    # recover the dict so it never leaks as a raw str to pydantic / wcache.
    payload = (
        '{"body_params": {"path": "a.html", "content": "<html>\n\t<body/>\n</html>"}}'
    )
    assert coerce_json_like(payload) == {
        "body_params": {"path": "a.html", "content": "<html>\n\t<body/>\n</html>"}
    }


# ---------------------------------------------------------------------------
# extract_reasoning
# ---------------------------------------------------------------------------


def test_extract_reasoning_from_top_level_headers():
    reasoning = extract_reasoning(
        {
            "headers": {
                "toolcallreasoningtitle": "Do X",
                "toolcallreasoningdescription": "because Y",
            }
        }
    )
    assert isinstance(reasoning, ToolCallRequestReasoning)
    assert reasoning.title == "Do X"
    assert reasoning.description == "because Y"


def test_extract_reasoning_from_nested_body_params_headers():
    reasoning = extract_reasoning(
        {
            "payload": {
                "body_params": {
                    "headers": {
                        "toolcallreasoningtitle": "Compact",
                        "toolcallreasoningdescription": "free space",
                    }
                }
            }
        }
    )
    assert reasoning is not None
    assert reasoning.title == "Compact"
    assert reasoning.description == "free space"


def test_extract_reasoning_missing_returns_none():
    assert extract_reasoning(None) is None
    assert extract_reasoning({}) is None
    assert extract_reasoning({"unrelated": "value"}) is None


# ---------------------------------------------------------------------------
# extract_plan_task_id / resolve_plan_task_id
# ---------------------------------------------------------------------------


def test_extract_plan_task_id_from_top_level_headers():
    assert (
        extract_plan_task_id({"headers": {"toolcallplantaskid": "uuid-1"}}) == "uuid-1"
    )


def test_extract_plan_task_id_from_nested_body_params_headers():
    assert (
        extract_plan_task_id(
            {"payload": {"body_params": {"headers": {"toolcallplantaskid": "uuid-2"}}}}
        )
        == "uuid-2"
    )


def test_extract_plan_task_id_empty_or_missing_returns_none():
    assert extract_plan_task_id(None) is None
    assert extract_plan_task_id({}) is None
    assert extract_plan_task_id({"headers": {"toolcallplantaskid": ""}}) is None
    assert extract_plan_task_id({"headers": {"toolcallplantaskid": "   "}}) is None


def _make_plan_task(tasks, started=True):
    """Build a Task stand-in carrying a deep_planning object."""
    items = [SimpleNamespace(id=tid, completed=done) for tid, done in tasks]
    deep_planning = SimpleNamespace(enabled=True, started=started, tasks=items)
    return SimpleNamespace(deep_planning=deep_planning)


def test_resolve_plan_task_id_prefers_llm_header():
    task = _make_plan_task([("step-a", False), ("step-b", False)])
    args = {"headers": {"toolcallplantaskid": "step-b"}}
    assert resolve_plan_task_id(args, task) == "step-b"


def test_resolve_plan_task_id_falls_back_to_first_incomplete_step():
    task = _make_plan_task([("step-a", True), ("step-b", False), ("step-c", False)])
    # No header → derive the active (first incomplete) step.
    assert resolve_plan_task_id({}, task) == "step-b"


def test_resolve_plan_task_id_honors_completed_but_real_step():
    # A header naming a real step is trusted even when that step is already
    # completed — a call can legitimately belong to a step just finished.
    task = _make_plan_task([("step-a", True), ("step-b", False)])
    args = {"headers": {"toolcallplantaskid": "step-a"}}
    assert resolve_plan_task_id(args, task) == "step-a"


def test_resolve_plan_task_id_unknown_id_snaps_to_active():
    # An id absent from the plan is junk → snap to the active (first-incomplete) step.
    task = _make_plan_task([("step-a", True), ("step-b", False)])
    args = {"headers": {"toolcallplantaskid": "does-not-exist"}}
    assert resolve_plan_task_id(args, task) == "step-b"


def test_resolve_plan_task_id_empty_header_snaps_to_active():
    # Empty/blank header on a started plan → the current (first-incomplete) step.
    task = _make_plan_task([("step-a", False)])
    assert (
        resolve_plan_task_id({"headers": {"toolcallplantaskid": ""}}, task) == "step-a"
    )
    assert (
        resolve_plan_task_id({"headers": {"toolcallplantaskid": "   "}}, task)
        == "step-a"
    )


def test_resolve_plan_task_id_no_fallback_before_plan_started():
    # enabled but not started → no active step to attribute work to.
    task = _make_plan_task([("step-a", False)], started=False)
    assert resolve_plan_task_id({}, task) is None


def test_resolve_plan_task_id_none_when_no_plan_or_all_complete():
    assert resolve_plan_task_id({}, None) is None
    all_done = _make_plan_task([("step-a", True), ("step-b", True)])
    assert resolve_plan_task_id({}, all_done) is None
    disabled = SimpleNamespace(
        deep_planning=SimpleNamespace(
            enabled=False,
            started=True,
            tasks=[SimpleNamespace(id="x", completed=False)],
        )
    )
    assert resolve_plan_task_id({}, disabled) is None


# ---------------------------------------------------------------------------
# should_skip_tool_report (deep-planning tools)
# ---------------------------------------------------------------------------


def test_planning_tools_skip_set_matches_mono():
    # Must cover every deep-planning tool the backend currently skips.
    expected = {
        "xpcreate_agent_plan",
        "xpget_agent_plan",
        "xpadd_new_agent_plan_item",
        "xpupdate_agent_plan_item",
        "xpdelete_agent_plan_item",
        "xpcomplete_agent_plan_items",
        "xpstart_execution_plan",
    }
    assert set(PLANNING_TOOLS) == expected


def test_should_skip_tool_report_flags_planning_and_reasoning_tools():
    for tool in PLANNING_TOOLS:
        assert should_skip_tool_report(tool) is True
    # Reasoning tools are also skipped for regular tool-call reporting; they
    # are emitted via the dedicated reasoning event instead.
    for tool in REASONING_TOOLS:
        assert should_skip_tool_report(tool) is True
    # Non-planning / non-reasoning tools should not be skipped.
    assert should_skip_tool_report("my_tool") is False
    assert should_skip_tool_report("xpworkspace-bash") is False
    assert should_skip_tool_report("xpcompact_context") is False
    assert should_skip_tool_report(None) is False
    assert should_skip_tool_report("") is False


def test_agno_internal_team_tools_skip_set():
    # Agno's team-orchestration tools must be fully hidden from activity
    # (PRO-1383). They are framework plumbing, not real agent actions.
    expected = {
        "delegate_task_to_member",
        "delegate_task_to_members",
        "execute_task",
        "execute_tasks_parallel",
        "get_member_information",
    }
    assert set(AGNO_INTERNAL_TEAM_TOOLS) == expected
    for tool in AGNO_INTERNAL_TEAM_TOOLS:
        assert should_skip_tool_report(tool) is True


# ---------------------------------------------------------------------------
# Reasoning tools (think / analyze)
# ---------------------------------------------------------------------------


def test_reasoning_tools_set_is_think_and_analyze():
    assert set(REASONING_TOOLS) == {"think", "analyze"}


def test_is_reasoning_tool_flag():
    assert is_reasoning_tool("think") is True
    assert is_reasoning_tool("analyze") is True
    assert is_reasoning_tool("my_tool") is False
    assert is_reasoning_tool(None) is False


@pytest.mark.asyncio
async def test_report_reasoning_event_emits_think_with_input_payload():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_reasoning_event(
            task=task,
            tool_name="think",
            arguments={
                "title": "Consider options",
                "confidence": 0.85,
                "thought": "let's evaluate",
                "action": "compare",
            },
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 1
        event = events[0]
        # Consumer expects the dedicated Think event type.
        assert event["type"] == TaskUpdateEventType.Think.value
        # And the reasoning fields wrapped under payload["input"].
        payload_input = event["data"]["payload"]["input"]
        assert payload_input["title"] == "Consider options"
        assert payload_input["confidence"] == 0.85
        assert payload_input["thought"] == "let's evaluate"
        assert payload_input["action"] == "compare"


@pytest.mark.asyncio
async def test_report_reasoning_event_emits_analyze():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_reasoning_event(
            task=task,
            tool_name="analyze",
            arguments={"title": "Review", "confidence": 0.5, "analysis": "looks fine"},
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 1
        assert events[0]["type"] == TaskUpdateEventType.Analyze.value
        assert events[0]["data"]["payload"]["input"]["analysis"] == "looks fine"


@pytest.mark.asyncio
async def test_report_reasoning_event_accepts_already_wrapped_input():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_reasoning_event(
            task=task,
            tool_name="think",
            arguments={"input": {"title": "T", "confidence": 1.0, "thought": "x"}},
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 1
        assert events[0]["data"]["payload"]["input"]["title"] == "T"


@pytest.mark.asyncio
async def test_report_reasoning_event_carries_plan_task_id():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_reasoning_event(
            task=task,
            tool_name="think",
            arguments={"title": "T", "confidence": 1.0},
            plan_task_id="step-9",
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 1
        assert events[0]["data"]["plan_task_id"] == "step-9"


@pytest.mark.asyncio
async def test_report_request_and_result_carry_plan_task_id():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_request(
            task=task,
            request_id="r1",
            operation_id="my_tool",
            payload={"a": 1},
            plan_task_id="step-7",
        )
        await report_tool_call_result(
            task=task,
            request_id="r1",
            operation_id="my_tool",
            result="ok",
            plan_task_id="step-7",
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 2
        assert events[0]["data"]["plan_task_id"] == "step-7"
        assert events[1]["data"]["plan_task_id"] == "step-7"


@pytest.mark.asyncio
async def test_report_reasoning_event_ignores_unknown_tool():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_reasoning_event(
            task=task, tool_name="not_a_reasoning_tool", arguments={"x": 1}
        )

        assert mock_client.make_request.await_count == 0


# ---------------------------------------------------------------------------
# report_tool_call_request / report_tool_call_result
# ---------------------------------------------------------------------------


def _captured_payloads(mock_make_request) -> List[Dict[str, Any]]:
    """Collect the single event dict passed to each make_request call."""
    out = []
    for call in mock_make_request.await_args_list:
        kwargs = call.kwargs or {}
        payload = kwargs.get("payload")
        if isinstance(payload, list) and payload:
            out.append(payload[0])
    return out


@pytest.mark.asyncio
async def test_report_tool_call_coerces_string_json_payload_and_result():
    """Stringified JSON payloads / results should be reported as structured
    dicts in the activity event."""
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_request(
            task=task,
            request_id="req-json",
            operation_id="my_tool",
            payload='{"a": 1, "nested": {"b": [2, 3]}}',
        )
        await report_tool_call_result(
            task=task,
            request_id="req-json",
            operation_id="my_tool",
            # Python-literal style result, should still parse via ast.literal_eval.
            result="{'ok': True, 'items': [1, 2]}",
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 2
        assert events[0]["data"]["payload"] == {"a": 1, "nested": {"b": [2, 3]}}
        assert events[1]["data"]["result"] == {"ok": True, "items": [1, 2]}


@pytest.mark.asyncio
async def test_report_request_and_result_push_correct_event_shapes():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_request(
            task=task,
            request_id="req-1",
            operation_id="my_tool",
            tool_name="my_tool",
            payload={"x": 1},
        )
        await report_tool_call_result(
            task=task,
            request_id="req-1",
            operation_id="my_tool",
            tool_name="my_tool",
            payload={"x": 1},
            result={"ok": True},
            is_error=False,
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 2
        assert events[0]["type"] == TaskUpdateEventType.ToolCallRequest.value
        assert events[1]["type"] == TaskUpdateEventType.ToolCallResult.value
        assert events[0]["data"]["request_id"] == "req-1"
        assert events[1]["data"]["request_id"] == "req-1"
        assert events[1]["data"]["is_error"] is False
        assert events[1]["data"]["result"] == {"ok": True}


@pytest.mark.asyncio
async def test_report_result_truncates_large_payload():
    task = _make_fake_task()
    big = "a" * (DEFAULT_MAX_CONTENT_LENGTH + 1000)
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_result(
            task=task,
            request_id="req-big",
            operation_id="my_tool",
            result=big,
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 1
        result_field = events[0]["data"]["result"]
        assert "[TRUNCATED OUTPUT" in result_field
        assert len(result_field) < len(big)


@pytest.mark.asyncio
async def test_report_result_with_skip_truncation_keeps_full():
    """Reading a previously-offloaded CONTEXT_OPTIMIZATION file must not be
    re-truncated in the activity log; the agent explicitly asked for the
    full content.
    """
    task = _make_fake_task()
    big = "a" * (DEFAULT_MAX_CONTENT_LENGTH + 5_000)
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_result(
            task=task,
            request_id="req-full",
            operation_id="xpworkspace-file-read",
            result=big,
            skip_truncation=True,
        )

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 1
        result_field = events[0]["data"]["result"]
        assert result_field == big
        assert "[TRUNCATED OUTPUT" not in result_field


@pytest.mark.asyncio
async def test_report_push_failure_is_swallowed():
    task = _make_fake_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(side_effect=RuntimeError("boom"))

        # Must not raise despite the backend failure.
        await report_tool_call_request(
            task=task,
            request_id="req-x",
            operation_id="my_tool",
        )
        await report_tool_call_result(
            task=task,
            request_id="req-x",
            operation_id="my_tool",
            result="done",
        )


# ---------------------------------------------------------------------------
# Tool.ainvoke with report_activity flag
# ---------------------------------------------------------------------------


def _make_local_tool(name: str = "greet") -> Any:
    from xpander_sdk.models.configuration import Configuration
    from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool

    async def _fn(name: str):
        return f"hello {name}"

    return Tool(
        id=name,
        name=name,
        method="GET",
        path=f"/tools/{name}",
        is_local=True,
        is_synced=True,
        description=name,
        parameters={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
        fn=_fn,
        configuration=Configuration(api_key="test", organization_id="org-1"),
    )


@pytest.mark.asyncio
async def test_tool_ainvoke_without_flag_does_not_emit():
    tool = _make_local_tool()
    task = _make_fake_task()
    tool.configuration.state.task = task

    with (
        patch(
            "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
        ) as mock_api_cls,
        patch.object(
            type(tool), "agraph_preflight_check", new=AsyncMock(return_value=None)
        ),
    ):
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        result = await tool.ainvoke(
            agent_id="agent-1",
            payload={"name": "Moriel"},
            task_id=task.id,
            report_activity=False,
        )
        await _wait_for_background_tasks()

        assert result.is_success is True
        assert mock_client.make_request.await_count == 0


@pytest.mark.asyncio
async def test_tool_ainvoke_with_flag_emits_request_and_result_with_same_uuid():
    tool = _make_local_tool()
    task = _make_fake_task()
    tool.configuration.state.task = task

    with (
        patch(
            "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
        ) as mock_api_cls,
        patch.object(
            type(tool), "agraph_preflight_check", new=AsyncMock(return_value=None)
        ),
    ):
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await tool.ainvoke(
            agent_id="agent-1",
            payload={"name": "Moriel"},
            task_id=task.id,
            report_activity=True,
        )
        await _wait_for_background_tasks()

        events = _captured_payloads(mock_client.make_request)
        assert len(events) == 2
        assert events[0]["type"] == TaskUpdateEventType.ToolCallRequest.value
        assert events[1]["type"] == TaskUpdateEventType.ToolCallResult.value
        assert events[0]["data"]["request_id"] == events[1]["data"]["request_id"]
        assert events[1]["data"]["is_error"] is False


@pytest.mark.asyncio
async def test_tool_ainvoke_two_calls_produce_distinct_uuids():
    tool = _make_local_tool()
    task = _make_fake_task()
    tool.configuration.state.task = task

    with (
        patch(
            "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
        ) as mock_api_cls,
        patch.object(
            type(tool), "agraph_preflight_check", new=AsyncMock(return_value=None)
        ),
    ):
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await tool.ainvoke(
            agent_id="agent-1",
            payload={"name": "A"},
            task_id=task.id,
            report_activity=True,
        )
        await tool.ainvoke(
            agent_id="agent-1",
            payload={"name": "B"},
            task_id=task.id,
            report_activity=True,
        )
        await _wait_for_background_tasks()

        events = _captured_payloads(mock_client.make_request)
        # Two invocations => 4 events (request+result each).
        assert len(events) == 4
        request_events = [
            e for e in events if e["type"] == TaskUpdateEventType.ToolCallRequest.value
        ]
        uuids = {e["data"]["request_id"] for e in request_events}
        assert len(uuids) == 2


@pytest.mark.asyncio
async def test_tool_ainvoke_skips_planning_tools():
    """Deep-planning tools must never produce activity events, even with the flag on."""
    from xpander_sdk.models.configuration import Configuration
    from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool

    async def _fn(**kwargs):
        return "ok"

    tool = Tool(
        id="xpcreate_agent_plan",
        name="xpcreate_agent_plan",
        method="GET",
        path="/tools/xpcreate_agent_plan",
        is_local=True,
        is_synced=True,
        description="create plan",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "string"}},
        },
        fn=_fn,
        configuration=Configuration(api_key="test", organization_id="org-1"),
    )
    task = _make_fake_task()
    tool.configuration.state.task = task

    with (
        patch(
            "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
        ) as mock_api_cls,
        patch.object(
            type(tool), "agraph_preflight_check", new=AsyncMock(return_value=None)
        ),
    ):
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await tool.ainvoke(
            agent_id="agent-1",
            payload={"x": "y"},
            task_id=task.id,
            report_activity=True,
        )
        await _wait_for_background_tasks()

        assert mock_client.make_request.await_count == 0


@pytest.mark.asyncio
async def test_tool_ainvoke_reasoning_tool_emits_reasoning_event():
    """think/analyze called through Tool.ainvoke should produce a Think/Analyze
    activity event and no ToolCallRequest/ToolCallResult events.
    """
    from xpander_sdk.models.configuration import Configuration
    from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool

    async def _fn(**kwargs):
        return "ok"

    tool = Tool(
        id="think",
        name="think",
        method="GET",
        path="/tools/think",
        is_local=True,
        is_synced=True,
        description="think",
        parameters={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "confidence": {"type": "number"},
                "thought": {"type": "string"},
            },
        },
        fn=_fn,
        configuration=Configuration(api_key="test", organization_id="org-1"),
    )
    task = _make_fake_task()
    tool.configuration.state.task = task

    with (
        patch(
            "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
        ) as mock_api_cls,
        patch.object(
            type(tool), "agraph_preflight_check", new=AsyncMock(return_value=None)
        ),
    ):
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await tool.ainvoke(
            agent_id="agent-1",
            payload={"title": "X", "confidence": 1.0, "thought": "hmm"},
            task_id=task.id,
            report_activity=True,
        )
        await _wait_for_background_tasks()

        events = _captured_payloads(mock_client.make_request)
        # Exactly one Think event, no ToolCallRequest/ToolCallResult.
        assert len(events) == 1
        assert events[0]["type"] == TaskUpdateEventType.Think.value
        assert events[0]["data"]["payload"]["input"]["title"] == "X"


@pytest.mark.asyncio
async def test_tool_ainvoke_error_still_reports_is_error_true():
    from xpander_sdk.models.configuration import Configuration
    from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool

    async def _failing(name: str):
        raise RuntimeError("boom")

    tool = Tool(
        id="boom",
        name="boom",
        method="GET",
        path="/tools/boom",
        is_local=True,
        is_synced=True,
        description="boom",
        parameters={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
        fn=_failing,
        configuration=Configuration(api_key="test", organization_id="org-1"),
    )
    task = _make_fake_task()
    tool.configuration.state.task = task

    with (
        patch(
            "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
        ) as mock_api_cls,
        patch.object(
            type(tool), "agraph_preflight_check", new=AsyncMock(return_value=None)
        ),
    ):
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        result = await tool.ainvoke(
            agent_id="agent-1",
            payload={"name": "Moriel"},
            task_id=task.id,
            report_activity=True,
        )
        await _wait_for_background_tasks()

        # The tool implementation catches exceptions into the result object,
        # so ainvoke returns rather than raising. The event must still be
        # emitted with is_error=True.
        assert result.is_error is True

        events = _captured_payloads(mock_client.make_request)
        result_events = [
            e for e in events if e["type"] == TaskUpdateEventType.ToolCallResult.value
        ]
        assert len(result_events) == 1
        assert result_events[0]["data"]["is_error"] is True
        assert "boom" in str(result_events[0]["data"]["result"])


# ---------------------------------------------------------------------------
# is_agent_gateway_task
# ---------------------------------------------------------------------------


def test_is_agent_gateway_task_true_for_header():
    task = _make_gateway_task()
    assert is_agent_gateway_task(task) is True


def test_is_agent_gateway_task_case_and_whitespace_insensitive():
    assert (
        is_agent_gateway_task(
            _make_fake_task(
                payload_extension={"headers": {"x-is-from-agent-gateway": " TRUE "}}
            )
        )
        is True
    )


def test_is_agent_gateway_task_false_cases():
    assert is_agent_gateway_task(_make_fake_task(payload_extension=None)) is False
    assert is_agent_gateway_task(_make_fake_task(payload_extension={})) is False
    assert (
        is_agent_gateway_task(_make_fake_task(payload_extension={"headers": {}}))
        is False
    )
    assert (
        is_agent_gateway_task(
            _make_fake_task(
                payload_extension={"headers": {"x-is-from-agent-gateway": "false"}}
            )
        )
        is False
    )
    # Non-dict payload_extension / headers must not raise.
    assert is_agent_gateway_task(_make_fake_task(payload_extension="nope")) is False
    assert (
        is_agent_gateway_task(_make_fake_task(payload_extension={"headers": "nope"}))
        is False
    )
    assert is_agent_gateway_task(None) is False


# ---------------------------------------------------------------------------
# Tool-call summary pre-warm (gateway tasks)
# ---------------------------------------------------------------------------


def _captured_summarizer_calls(mock_make_request) -> List[Dict[str, Any]]:
    """Collect the request bodies of pre-warm calls to the summarizer endpoint.

    The activity push sends a list payload; the summarizer pre-warm sends a
    dict payload carrying ``preset`` — that's how we tell them apart.
    """
    out = []
    for call in mock_make_request.await_args_list:
        kwargs = call.kwargs or {}
        payload = kwargs.get("payload")
        if isinstance(payload, dict) and "preset" in payload:
            out.append(payload)
    return out


@pytest.mark.asyncio
async def test_gateway_task_prewarms_tool_call_summary():
    task = _make_gateway_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_result(
            task=task,
            request_id="req-gw",
            operation_id="my_tool",
            tool_name="my_tool",
            payload={"q": "since 09:00"},
            result={"unread": 47},
        )
        await _wait_for_background_tasks()

        summaries = _captured_summarizer_calls(mock_client.make_request)
        assert len(summaries) == 1
        body = summaries[0]
        assert body["preset"] == TOOL_CALL_SUMMARY_PRESET
        assert body["use_cache"] is True
        # Same {tool_name, request, response} shape the chat-backend wrapper
        # sends, using the coerced request payload + shaped result just logged.
        assert body["payload"]["tool_name"] == "my_tool"
        assert body["payload"]["request"] == {"q": "since 09:00"}
        assert body["payload"]["response"] == {"unread": 47}


@pytest.mark.asyncio
async def test_gateway_prewarm_unwraps_envelope_and_normalizes_floats():
    """The pre-warm must match the chat web-app's later request: the request is
    unwrapped from its ``payload`` envelope and integral floats collapse to ints
    (mirroring the UI's JS JSON round-trip)."""
    task = _make_gateway_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_result(
            task=task,
            request_id="req-env",
            operation_id="WebSearch",
            tool_name="WebSearch",
            # Envelope-wrapped request, mirroring agno's {"payload": {...}} kwargs.
            payload={
                "payload": {
                    "body_params": {"query": "x", "max_results": 5},
                    "headers": {"toolcallplantaskid": ""},
                }
            },
            # Integral float in the result must serialize as int, like the UI.
            result={"response_time": 0.0, "score": 0.87},
        )
        await _wait_for_background_tasks()

        summaries = _captured_summarizer_calls(mock_client.make_request)
        assert len(summaries) == 1
        body = summaries[0]["payload"]
        # Envelope stripped -> inner data only.
        assert body["request"] == {
            "body_params": {"query": "x", "max_results": 5},
            "headers": {"toolcallplantaskid": ""},
        }
        # 0.0 -> 0 (int); non-integral float untouched.
        assert body["response"] == {"response_time": 0, "score": 0.87}
        assert isinstance(body["response"]["response_time"], int)


@pytest.mark.asyncio
async def test_non_gateway_task_does_not_prewarm():
    task = _make_fake_task()  # no gateway header
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_result(
            task=task,
            request_id="req-plain",
            operation_id="my_tool",
            tool_name="my_tool",
            payload={"q": "x"},
            result={"ok": True},
        )
        await _wait_for_background_tasks()

        assert _captured_summarizer_calls(mock_client.make_request) == []


@pytest.mark.asyncio
async def test_gateway_task_skips_prewarm_for_skipped_tools():
    """Planning/reasoning/team-internal tools never reach report_tool_call_result
    in production, but guard against pre-warming them if they do."""
    task = _make_gateway_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        await report_tool_call_result(
            task=task,
            request_id="req-plan",
            operation_id="xpcreate_agent_plan",
            tool_name="xpcreate_agent_plan",
            payload={"x": 1},
            result={"ok": True},
        )
        await _wait_for_background_tasks()

        assert _captured_summarizer_calls(mock_client.make_request) == []


@pytest.mark.asyncio
async def test_prewarm_failure_does_not_break_result_reporting():
    """A failing summarizer pre-warm must not affect the activity push."""
    task = _make_gateway_task()
    with patch(
        "xpander_sdk.modules.backend.utils.tool_call_events.APIClient"
    ) as mock_api_cls:
        mock_client = mock_api_cls.return_value
        mock_client.make_request = AsyncMock(side_effect=RuntimeError("boom"))

        # Must not raise even though both the push and the pre-warm fail.
        await report_tool_call_result(
            task=task,
            request_id="req-fail",
            operation_id="my_tool",
            tool_name="my_tool",
            payload={"x": 1},
            result={"ok": True},
        )
        await _wait_for_background_tasks()


# --------------------------------------------------------------------------- #
# resolve_plan_task_id — last-trusted-header fallback (batched completions)
# --------------------------------------------------------------------------- #


def _make_plan_task_with_id(task_id: str, tasks, started: bool = True):
    """Plan task stand-in that also carries a task id (enables the trusted cache)."""
    items = [SimpleNamespace(id=tid, completed=done) for tid, done in tasks]
    deep_planning = SimpleNamespace(enabled=True, started=started, tasks=items)
    return SimpleNamespace(id=task_id, deep_planning=deep_planning)


def test_resolve_plan_task_id_headerless_falls_back_to_last_trusted():
    """Mid-phase header-less call attributes to the last real header, not the
    phase's first incomplete step (which stays uncompleted under batching)."""
    from xpander_sdk.modules.backend.utils import tool_call_events as tce

    tce._LAST_TRUSTED_PLAN_TASK_ID.clear()
    task = _make_plan_task_with_id(
        "task-1", [("step-a", False), ("step-b", False), ("step-c", False)]
    )
    # Model works step-b (header present), then a header-less call arrives.
    assert (
        resolve_plan_task_id({"headers": {"toolcallplantaskid": "step-b"}}, task)
        == "step-b"
    )
    assert resolve_plan_task_id({}, task) == "step-b"


def test_resolve_plan_task_id_no_trusted_header_uses_first_incomplete():
    """With no trusted header recorded yet, fall back to the first-incomplete step."""
    from xpander_sdk.modules.backend.utils import tool_call_events as tce

    tce._LAST_TRUSTED_PLAN_TASK_ID.clear()
    task = _make_plan_task_with_id("task-2", [("step-a", True), ("step-b", False)])
    assert resolve_plan_task_id({}, task) == "step-b"


def test_resolve_plan_task_id_trusted_cache_is_per_task():
    """A trusted header from one task never leaks into another task's fallback."""
    from xpander_sdk.modules.backend.utils import tool_call_events as tce

    tce._LAST_TRUSTED_PLAN_TASK_ID.clear()
    task_a = _make_plan_task_with_id("task-a", [("step-1", False), ("step-2", False)])
    task_b = _make_plan_task_with_id("task-b", [("step-1", False), ("step-2", False)])
    resolve_plan_task_id({"headers": {"toolcallplantaskid": "step-2"}}, task_a)
    assert resolve_plan_task_id({}, task_b) == "step-1"


def test_resolve_plan_task_id_stale_trusted_id_dropped_after_plan_reshape():
    """A remembered id no longer in the plan (step deleted) is ignored."""
    from xpander_sdk.modules.backend.utils import tool_call_events as tce

    tce._LAST_TRUSTED_PLAN_TASK_ID.clear()
    task = _make_plan_task_with_id("task-3", [("step-a", False), ("step-b", False)])
    resolve_plan_task_id({"headers": {"toolcallplantaskid": "step-b"}}, task)
    task.deep_planning.tasks = [SimpleNamespace(id="step-a", completed=False)]
    assert resolve_plan_task_id({}, task) == "step-a"
