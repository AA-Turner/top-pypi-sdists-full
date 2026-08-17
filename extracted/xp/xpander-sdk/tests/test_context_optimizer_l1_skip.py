"""Layer 1 coverage: which tools offload, and how the threshold tracks headroom.

Layer 1 used to skip every tool whose name starts with ``xp`` except
``xpworkspace-bash``. That exempted ``xp_execute_tool``, the dynamic-tools
dispatcher that proxies arbitrary external tools, so unbounded third-party
payloads stayed resident in full for the rest of the task. It also applied a
flat 8,000-char threshold regardless of how full the context was, which turned
mid-size results into context-retrieve round-trips while the window was nearly
empty. These tests pin both fixes.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from agno.models.message import Message

from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)

_BIG = "R" * 20_000
_HUGE = "R" * 90_000


def _make_optimizer(
    estimated_tokens: int = 0, context_window: int = 1_000_000
) -> XPanderContextOptimizer:
    opt = XPanderContextOptimizer(
        context_window=context_window,
        reserved_for_output=20_000,
        buffer_tokens=13_000,
        max_content_length=8_000,
        preview_length=2_000,
    )
    opt.agent = SimpleNamespace(
        id="agent-1", configuration=SimpleNamespace(organization_id="org-1")
    )
    opt.task = SimpleNamespace(id="task-1")
    opt._last_estimated_tokens = estimated_tokens
    return opt


def _tool_msg(
    content: str,
    tool_name: str,
    tool_call_id: str = "tc-1",
    tool_args: dict | None = None,
) -> Message:
    return Message(
        role="tool",
        content=content,
        tool_call_id=tool_call_id,
        tool_name=tool_name,
        tool_args=tool_args,
    )


def _dispatch_msg(content: str, inner_tool: str) -> Message:
    return _tool_msg(
        content,
        tool_name="xp_execute_tool",
        tool_args={"payload": {"name": inner_tool, "arguments": {}}},
    )


# ---- skip list ------------------------------------------------------- #


@pytest.mark.parametrize(
    "tool_name",
    [
        "xpworkspace-bash",
        "xpworkspace-grep",
        "xpworkspace-glob",
        "xpworkspace-local-db-run-query",
        "tavily_search",
        "some_mcp_tool",
    ],
)
def test_data_shaped_tools_are_offload_eligible(tool_name):
    assert XPanderContextOptimizer._l1_skip_tool(tool_name) is False


@pytest.mark.parametrize(
    "tool_name",
    [
        "think",
        "analyze",
        "xp_search_tools",
        "xp_list_tools",
        "xp_get_tool",
        "xpcreate_agent_plan",
        "xpworkspace-file-write",
        "xpworkspace-context-retrieve",
        "xpload_skill",
        "load_skill",
    ],
)
def test_control_tools_still_skip(tool_name):
    assert XPanderContextOptimizer._l1_skip_tool(tool_name) is True


# ---- dynamic dispatch unwrap ----------------------------------------- #


def test_effective_tool_name_unwraps_dynamic_dispatch():
    msg = _dispatch_msg("x", "tavily_search")
    assert XPanderContextOptimizer._effective_tool_name(msg) == "tavily_search"


def test_effective_tool_name_passes_through_normal_tools():
    msg = _tool_msg("x", "xpworkspace-bash")
    assert XPanderContextOptimizer._effective_tool_name(msg) == "xpworkspace-bash"


@pytest.mark.parametrize(
    "tool_args",
    [None, {}, {"payload": {}}, {"payload": {"name": "   "}}, {"payload": "nope"}],
)
def test_effective_tool_name_falls_back_to_meta_name(tool_args):
    msg = _tool_msg("x", "xp_execute_tool", tool_args=tool_args)
    assert XPanderContextOptimizer._effective_tool_name(msg) == "xp_execute_tool"


@pytest.mark.asyncio
async def test_dispatched_external_result_offloads():
    """The regression: a web-search payload behind xp_execute_tool must not stay resident."""
    opt = _make_optimizer(estimated_tokens=800_000)  # base band, 8K threshold
    msg = _dispatch_msg(_BIG, "tavily_search")
    with patch.object(
        opt,
        "_save_to_workspace",
        new=AsyncMock(return_value="CONTEXT_OPTIMIZATION/x.xp"),
    ) as save_mock:
        await opt.layer_1_microcompact([msg])
        save_mock.assert_awaited_once()
    assert msg.compressed_content is not None
    assert len(msg.compressed_content) < len(_BIG)


@pytest.mark.asyncio
async def test_dispatched_result_without_payload_name_still_skips():
    opt = _make_optimizer(estimated_tokens=800_000)
    msg = _tool_msg(_BIG, "xp_execute_tool", tool_args={"payload": {}})
    with patch.object(opt, "_save_to_workspace", new=AsyncMock()) as save_mock:
        await opt.layer_1_microcompact([msg])
        save_mock.assert_not_awaited()
    assert msg.compressed_content is None


# ---- headroom bands --------------------------------------------------- #


@pytest.mark.parametrize(
    "estimated_tokens,expected",
    [
        (0, 32_000),
        (100_000, 32_000),
        (349_999, 32_000),
        (350_000, 16_000),
        (599_999, 16_000),
        (600_000, 8_000),
        (950_000, 8_000),
    ],
)
def test_threshold_bands(estimated_tokens, expected):
    opt = _make_optimizer(estimated_tokens=estimated_tokens)
    assert opt._effective_max_content_length() == expected


@pytest.mark.asyncio
async def test_midsize_result_stays_inline_with_headroom():
    opt = _make_optimizer(estimated_tokens=200_000)  # 20% of 1M
    msg = _tool_msg(_BIG, "xpworkspace-bash")
    with patch.object(opt, "_save_to_workspace", new=AsyncMock()) as save_mock:
        await opt.layer_1_microcompact([msg])
        save_mock.assert_not_awaited()
    assert msg.compressed_content == _BIG


@pytest.mark.asyncio
async def test_huge_result_offloads_even_with_headroom():
    opt = _make_optimizer(estimated_tokens=0)
    msg = _tool_msg(_HUGE, "xpworkspace-bash")
    with patch.object(
        opt,
        "_save_to_workspace",
        new=AsyncMock(return_value="CONTEXT_OPTIMIZATION/y.xp"),
    ) as save_mock:
        await opt.layer_1_microcompact([msg])
        save_mock.assert_awaited_once()
    assert msg.compressed_content is not None
    assert len(msg.compressed_content) < len(_HUGE)


@pytest.mark.asyncio
async def test_same_result_offloads_under_pressure():
    opt = _make_optimizer(estimated_tokens=800_000)
    msg = _tool_msg(_BIG, "xpworkspace-bash")
    with patch.object(
        opt,
        "_save_to_workspace",
        new=AsyncMock(return_value="CONTEXT_OPTIMIZATION/z.xp"),
    ) as save_mock:
        await opt.layer_1_microcompact([msg])
        save_mock.assert_awaited_once()
    assert msg.compressed_content is not None
