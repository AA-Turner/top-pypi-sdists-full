"""Offload preview: raised inline budget, [STRUCTURE] line, async [SUMMARY] splice.

A head truncation says nothing about a payload's shape, so the model retrieves
everything "just in case" and the offload saves no context at all. The preview
now carries a deterministic structure line, and a gateway summary that resolves
after the fact is spliced into the same block on a later microcompact pass.
"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace

import pytest

from agno.models.message import Message

from xpander_sdk.core.context_optimizer.constants import (
    L1_HEADROOM_BANDS,
    OFFLOAD_SUMMARY_MAX_CHARS,
    PENDING_SUMMARY_MAX_PASSES,
)
from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)


def _make_optimizer(**kwargs) -> XPanderContextOptimizer:
    opt = XPanderContextOptimizer(context_window=200_000, **kwargs)
    opt.agent = SimpleNamespace(
        id="agent-1", configuration=SimpleNamespace(organization_id="org-1")
    )
    opt.task = SimpleNamespace(id="task-1")
    return opt


def test_layer_1_defaults_keep_mid_size_results_inline():
    opt = _make_optimizer()
    assert opt.max_content_length == 16_000
    assert opt.preview_length == 4_000
    # Bands multiply the base while the window is mostly empty.
    opt._last_estimated_tokens = 0
    assert opt._effective_max_content_length() == 16_000 * L1_HEADROOM_BANDS[0][1]
    opt._last_estimated_tokens = 100_000
    assert opt._effective_max_content_length() == 16_000 * L1_HEADROOM_BANDS[1][1]
    opt._last_estimated_tokens = 180_000
    assert opt._effective_max_content_length() == 16_000


def test_json_preview_carries_a_structure_line():
    opt = _make_optimizer()
    payload = json.dumps([{"id": f"u{i}", "name": "x"} for i in range(400)])
    preview = opt._build_offload_preview(
        content=payload,
        workspace_path="CONTEXT_OPTIMIZATION/ctx-1.xp",
        original_len=len(payload),
    )
    assert "[STRUCTURE] JSON array of 400 objects" in preview
    assert 'context_id="ctx-1"' in preview


def test_plain_text_preview_has_no_structure_line():
    opt = _make_optimizer()
    content = "log line\n" * 5_000
    preview = opt._build_offload_preview(
        content=content,
        workspace_path="CONTEXT_OPTIMIZATION/ctx-2.xp",
        original_len=len(content),
    )
    assert "[STRUCTURE]" not in preview
    assert "[TRUNCATED OUTPUT -" in preview
    # No structure line to read, so the guidance must not point at one.
    assert "Decide from the preview first" in preview
    assert "structure line" not in preview


def test_preview_points_at_targeted_retrieval():
    opt = _make_optimizer()
    content = json.dumps([{"id": i} for i in range(2_000)])
    preview = opt._build_offload_preview(
        content=content,
        workspace_path="CONTEXT_OPTIMIZATION/ctx-3.xp",
        original_len=len(content),
    )
    assert 'query="<regex>"' in preview
    assert 'semantic_query="<text>"' in preview
    assert "multiple times on the same context_id" in preview
    assert "Decide from the preview and the structure line first" in preview


def _offloaded_msg(context_id: str = "ctx-9") -> Message:
    opt = _make_optimizer()
    preview = opt._build_offload_preview(
        content="y" * 40_000,
        workspace_path=f"CONTEXT_OPTIMIZATION/{context_id}.xp",
        original_len=40_000,
    )
    return Message(
        role="tool",
        content=preview,
        tool_call_id="tc-summary",
        tool_name="some-connector-call",
    )


async def _resolved(value):
    return value


async def _never():
    await asyncio.Event().wait()


@pytest.mark.asyncio
async def test_ready_summary_is_spliced_under_the_truncation_marker():
    opt = _make_optimizer()
    msg = _offloaded_msg()
    opt._inline_offloaded_tool_call_ids.add("tc-summary")
    task = asyncio.create_task(_resolved("Listed 400 users; 12 are archived."))
    await task
    opt.register_pending_summary("ctx-9", task)

    await opt.layer_1_microcompact([msg])

    lines = msg.content.split("\n")
    marker_idx = next(
        i for i, line in enumerate(lines) if line.startswith("[TRUNCATED OUTPUT -")
    )
    assert lines[marker_idx + 1] == "[SUMMARY] Listed 400 users; 12 are archived."
    assert not opt._pending_offload_summaries


@pytest.mark.asyncio
async def test_spliced_summary_stays_one_bounded_line():
    opt = _make_optimizer()
    msg = _offloaded_msg()
    opt._inline_offloaded_tool_call_ids.add("tc-summary")
    task = asyncio.create_task(_resolved("line one\nline two   " + "z" * 2_000))
    await task
    opt.register_pending_summary("ctx-9", task)

    await opt.layer_1_microcompact([msg])

    summary_line = next(
        line for line in msg.content.split("\n") if line.startswith("[SUMMARY]")
    )
    assert summary_line.startswith("[SUMMARY] line one line two z")
    assert len(summary_line) <= len("[SUMMARY] ") + OFFLOAD_SUMMARY_MAX_CHARS


@pytest.mark.asyncio
async def test_splice_happens_only_once():
    opt = _make_optimizer()
    msg = _offloaded_msg()
    opt._inline_offloaded_tool_call_ids.add("tc-summary")
    task = asyncio.create_task(_resolved("One summary."))
    await task
    opt.register_pending_summary("ctx-9", task)

    await opt.layer_1_microcompact([msg])
    opt.register_pending_summary("ctx-9", task)
    await opt.layer_1_microcompact([msg])

    assert msg.content.count("[SUMMARY]") == 1


@pytest.mark.asyncio
async def test_pending_summary_expires_without_blocking():
    opt = _make_optimizer()
    msg = _offloaded_msg()
    opt._inline_offloaded_tool_call_ids.add("tc-summary")
    task = asyncio.create_task(_never())
    opt.register_pending_summary("ctx-9", task)

    for _ in range(PENDING_SUMMARY_MAX_PASSES):
        await opt.layer_1_microcompact([msg])

    assert not opt._pending_offload_summaries
    assert "[SUMMARY]" not in msg.content
    task.cancel()


@pytest.mark.asyncio
async def test_failed_summary_is_dropped_silently():
    opt = _make_optimizer()
    msg = _offloaded_msg()
    opt._inline_offloaded_tool_call_ids.add("tc-summary")

    async def _boom():
        raise RuntimeError("summarizer down")

    task = asyncio.create_task(_boom())
    await asyncio.gather(task, return_exceptions=True)
    opt.register_pending_summary("ctx-9", task)

    await opt.layer_1_microcompact([msg])

    assert not opt._pending_offload_summaries
    assert "[SUMMARY]" not in msg.content
