"""Unit tests for `unwrap_tool_result_content` and the inline Layer 1
offload helper used by the agno tool hook and the fallback compress loop.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
    _extract_balanced_value,
    _extract_repr_field,
    unwrap_tool_result_content,
)


def test_extract_balanced_value_handles_nested_dicts():
    content = "x={'a': {'b': {'c': 1}}, 'd': [1, 2]} y=2"
    start = content.index("{")
    value = _extract_balanced_value(content, start)
    assert value == "{'a': {'b': {'c': 1}}, 'd': [1, 2]}"


def test_extract_balanced_value_handles_quoted_strings_with_braces():
    content = "r={'text': 'hello }{ world', 'n': 1} next=ok"
    start = content.index("{")
    value = _extract_balanced_value(content, start)
    assert value == "{'text': 'hello }{ world', 'n': 1}"


def test_extract_repr_field_reads_result_from_pydantic_repr():
    repr_str = (
        "tool_id='TavilySearchServiceExecuteQueryAndReturnResults' "
        "tool_call_id=None task_id='abc' payload={'query': 'xpander'} "
        "status_code=200 result={'query': 'xpander', 'items': [1, 2]} "
        "is_success=True is_error=False is_local=False"
    )
    value = _extract_repr_field(repr_str, "result")
    assert value == {"query": "xpander", "items": [1, 2]}


def test_unwrap_tool_result_content_strips_wrapper_and_returns_json():
    repr_str = (
        "tool_id='TavilySearchServiceExecuteQueryAndReturnResults' "
        "tool_call_id=None task_id='abc' payload={'query': 'xpander'} "
        "status_code=200 result={'query': 'xpander', 'items': [1, 2]} "
        "is_success=True is_error=False is_local=False"
    )
    unwrapped = unwrap_tool_result_content(repr_str)
    # Should be clean JSON of just the result field.
    parsed = json.loads(unwrapped)
    assert parsed == {"query": "xpander", "items": [1, 2]}
    assert "tool_id=" not in unwrapped
    assert "is_success" not in unwrapped


def test_unwrap_tool_result_content_keeps_nested_dicts():
    repr_str = (
        "tool_id='x' tool_call_id=None task_id='t' payload=None "
        "status_code=200 result={'outer': {'inner': {'deep': 'value'}}, 'list': [1, 2, 3]} "
        "is_success=True"
    )
    unwrapped = unwrap_tool_result_content(repr_str)
    assert json.loads(unwrapped) == {
        "outer": {"inner": {"deep": "value"}},
        "list": [1, 2, 3],
    }


def test_unwrap_tool_result_content_handles_string_result():
    repr_str = (
        "tool_id='greet' tool_call_id=None task_id='t' payload={'name': 'Moriel'} "
        "status_code=200 result='hello Moriel' is_success=True"
    )
    unwrapped = unwrap_tool_result_content(repr_str)
    assert unwrapped == "hello Moriel"


def test_unwrap_tool_result_content_passes_through_plain_strings():
    # Agno MCP tools etc. produce plain string content, not ToolInvocationResult reprs.
    assert unwrap_tool_result_content("hello world") == "hello world"
    assert unwrap_tool_result_content("") == ""
    assert unwrap_tool_result_content(None) == ""


def test_unwrap_tool_result_content_serializes_dict_input():
    assert json.loads(unwrap_tool_result_content({"a": 1})) == {"a": 1}


# ---------------------------------------------------------------------------
# maybe_offload_content + layer_1_microcompact fallback
# ---------------------------------------------------------------------------


def _make_optimizer(workspace_path="CONTEXT_OPTIMIZATION/abc.xp"):
    opt = XPanderContextOptimizer(
        max_content_length=100,
        min_content_length=10,
        preview_length=20,
    )
    # Patch the workspace save so tests never hit the network.
    opt._save_to_workspace = AsyncMock(return_value=workspace_path)
    return opt


@pytest.mark.asyncio
async def test_maybe_offload_content_offloads_when_exceeds_max():
    opt = _make_optimizer()
    big = "x" * 500
    replacement, path = await opt.maybe_offload_content(
        content=big, tool_name="web_search"
    )
    assert path == "CONTEXT_OPTIMIZATION/abc.xp"
    assert replacement is not None
    assert "[TRUNCATED OUTPUT" in replacement
    assert "CONTEXT_OPTIMIZATION/abc.xp" in replacement
    assert 'xpworkspace-context-retrieve with context_id="abc"' in replacement
    # The workspace got the full clean content.
    opt._save_to_workspace.assert_awaited_once()
    assert opt._save_to_workspace.await_args.args[0] == big


@pytest.mark.asyncio
async def test_maybe_offload_content_passthrough_between_min_and_max():
    opt = _make_optimizer()
    mid = "y" * 50
    replacement, path = await opt.maybe_offload_content(content=mid, tool_name="t")
    assert replacement is None
    assert path is None
    opt._save_to_workspace.assert_not_called()


@pytest.mark.asyncio
async def test_maybe_offload_content_skips_below_min_and_skipped_tools():
    opt = _make_optimizer()
    # Below min.
    r, p = await opt.maybe_offload_content(content="short", tool_name="t")
    assert (r, p) == (None, None)
    # Planning / reasoning / xp-prefixed tools (except xpworkspace-bash).
    big = "x" * 500
    for skip_tool in (
        "think",
        "analyze",
        "xpcreate_agent_plan",
        "xpworkspace-file-read",
    ):
        r, p = await opt.maybe_offload_content(content=big, tool_name=skip_tool)
        assert (r, p) == (None, None), f"should skip {skip_tool}"
    opt._save_to_workspace.assert_not_called()


@pytest.mark.asyncio
async def test_maybe_offload_content_allows_xpworkspace_bash():
    opt = _make_optimizer()
    big = "x" * 500
    replacement, path = await opt.maybe_offload_content(
        content=big, tool_name="xpworkspace-bash"
    )
    assert replacement is not None
    assert path is not None


@pytest.mark.asyncio
async def test_layer_1_fallback_skips_messages_offloaded_by_hook():
    opt = _make_optimizer()
    # Two messages: one already offloaded inline by the hook, one not.
    big = "z" * 500
    inline_msg = SimpleNamespace(
        role="tool",
        tool_name="web_search",
        tool_call_id="tc-inline",
        content=big,
        compressed_content=None,
    )
    fallback_msg = SimpleNamespace(
        role="tool",
        tool_name="other_tool",
        tool_call_id="tc-fallback",
        content=big,
        compressed_content=None,
    )
    opt._inline_offloaded_tool_call_ids.add("tc-inline")

    await opt.layer_1_microcompact([inline_msg, fallback_msg])

    # Only the fallback message got offloaded by the loop.
    assert inline_msg.compressed_content is None
    assert fallback_msg.compressed_content is not None
    assert "[TRUNCATED OUTPUT" in fallback_msg.compressed_content
    # Only one workspace save (for the fallback message).
    assert opt._save_to_workspace.await_count == 1


@pytest.mark.asyncio
async def test_layer_1_fallback_offloads_session_history_messages():
    """Messages loaded from session (never seen by the hook) must still be
    offloaded by the fallback loop."""
    opt = _make_optimizer()
    msg = SimpleNamespace(
        role="tool",
        tool_name="web_search",
        tool_call_id="tc-1",
        content="z" * 500,
        compressed_content=None,
    )
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is not None
    assert "[TRUNCATED OUTPUT" in msg.compressed_content
    opt._save_to_workspace.assert_awaited_once()
