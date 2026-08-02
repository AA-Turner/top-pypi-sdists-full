"""Layer 1 re-offload of stale xpworkspace-context-retrieve payloads.

A no-query context-retrieve returns the full offloaded payload inline. The
model must see it once, but before this fix the payload then sat on context
forever: the inline offload path skips context-optimization reads and
``_l1_skip_tool`` exempts every xp* tool. These tests pin the new behavior:
first compress pass leaves the payload intact, the second collapses it back
to a preview pointing at the ORIGINAL context_id, with no new workspace blob.
The collapse is gated on the headroom-banded threshold, so a payload that fits
comfortably in a mostly-empty window is kept for good.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from agno.models.message import Message

from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)


def _make_optimizer(estimated_tokens: int = 160_000) -> XPanderContextOptimizer:
    opt = XPanderContextOptimizer(
        context_window=200_000,
        reserved_for_output=20_000,
        buffer_tokens=13_000,
        max_content_length=8_000,
        preview_length=2_000,
    )
    opt.agent = SimpleNamespace(
        id="agent-1", configuration=SimpleNamespace(organization_id="org-1")
    )
    opt.task = SimpleNamespace(id="task-1")
    # Default to a pressured context (80% of the window) so these tests exercise
    # the re-offload mechanic at the base threshold rather than the wide
    # low-headroom band. Retention under headroom is covered separately below.
    opt._last_estimated_tokens = estimated_tokens
    return opt


def _retrieve_msg(
    content: str,
    tool_call_id: str = "tc-1",
    context_id: str = "ctx-abc-123",
    tool_args: dict | None = ...,
) -> Message:
    if tool_args is ...:
        tool_args = {"payload": {"body_params": {"context_id": context_id}}}
    return Message(
        role="tool",
        content=content,
        tool_call_id=tool_call_id,
        tool_name="xpworkspace-context-retrieve",
        tool_args=tool_args,
    )


_BIG = "R" * 20_000  # above max_content_length=8K


@pytest.mark.asyncio
async def test_first_pass_leaves_full_payload():
    opt = _make_optimizer()
    msg = _retrieve_msg(_BIG)
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is None
    assert msg.content == _BIG


@pytest.mark.asyncio
async def test_second_pass_reoffloads_to_original_context_id():
    opt = _make_optimizer()
    msg = _retrieve_msg(_BIG, context_id="ctx-original")
    with patch.object(
        opt, "_save_to_workspace", new=AsyncMock(return_value="SHOULD-NOT-BE-CALLED")
    ) as save_mock:
        await opt.layer_1_microcompact([msg])
        await opt.layer_1_microcompact([msg])
        save_mock.assert_not_awaited()
    assert msg.compressed_content is not None
    assert "CONTEXT_OPTIMIZATION/ctx-original.xp" in msg.compressed_content
    assert 'context_id="ctx-original"' in msg.compressed_content
    # Preview keeps the head of the payload, not the whole thing.
    assert len(msg.compressed_content) < len(_BIG)


@pytest.mark.asyncio
async def test_small_retrieve_never_reoffloaded():
    opt = _make_optimizer()
    msg = _retrieve_msg("small filtered result")
    await opt.layer_1_microcompact([msg])
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is None


@pytest.mark.asyncio
async def test_missing_tool_args_left_untouched():
    opt = _make_optimizer()
    msg = _retrieve_msg(_BIG, tool_args=None)
    await opt.layer_1_microcompact([msg])
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is None


@pytest.mark.asyncio
async def test_top_level_context_id_fallback():
    opt = _make_optimizer()
    msg = _retrieve_msg(_BIG, tool_args={"context_id": "ctx-top-level"})
    await opt.layer_1_microcompact([msg])
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is not None
    assert "CONTEXT_OPTIMIZATION/ctx-top-level.xp" in msg.compressed_content


@pytest.mark.asyncio
async def test_retrieved_payload_retained_while_headroom_is_ample():
    """The agent asked for this data; evicting it at 5% usage just buys another retrieve."""
    opt = _make_optimizer(estimated_tokens=10_000)  # 5% of a 200K window
    msg = _retrieve_msg(_BIG)
    await opt.layer_1_microcompact([msg])
    await opt.layer_1_microcompact([msg])
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is None
    assert msg.content == _BIG


@pytest.mark.asyncio
async def test_other_xp_tools_still_skipped():
    opt = _make_optimizer()
    msg = Message(
        role="tool",
        content=_BIG,
        tool_call_id="tc-2",
        tool_name="xpget_agent_plan",
    )
    await opt.layer_1_microcompact([msg])
    await opt.layer_1_microcompact([msg])
    assert msg.compressed_content is None
