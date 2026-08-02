"""Unit tests for the per-turn context_status event stream."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from xpander_sdk.core.context_optimizer import context_optimizer as co
from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)
from xpander_sdk.models.events import TaskUpdateEventType


def _mk_msg(role: str = "user", content: str = "x"):
    return SimpleNamespace(
        role=role,
        content=content,
        tool_name=None,
        tool_call_id=None,
        to_dict=lambda r=role, c=content: {"role": r, "content": c},
    )


def _make_optimizer(estimated: int = 50_000):
    opt = XPanderContextOptimizer(
        context_window=200_000,
        reserved_for_output=20_000,
        buffer_tokens=13_000,
        chunked_compact_threshold=100_000,
    )
    opt.agent = SimpleNamespace(id="agent-1", configuration=MagicMock())
    opt.task = SimpleNamespace(id="task-1", organization_id="org-1", deep_planning=None)
    opt._push_activity_event = AsyncMock(return_value=None)
    opt._estimate_tokens = MagicMock(return_value=estimated)
    opt.layer_1_microcompact = AsyncMock(return_value=None)
    return opt


def _status_calls(opt) -> list:
    return [
        call
        for call in opt._push_activity_event.await_args_list
        if call.kwargs.get("event_type") == TaskUpdateEventType.ContextStatus
    ]


async def _drain_pending_tasks() -> None:
    """Yield so detached create_task pushes run before asserting on AsyncMock awaits."""
    for _ in range(5):
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_first_acompress_emits_one_status_event():
    opt = _make_optimizer(estimated=50_000)
    await opt.acompress(messages=[_mk_msg()])
    await _drain_pending_tasks()

    calls = _status_calls(opt)
    assert len(calls) == 1
    payload = calls[0].kwargs["data"]
    assert payload.estimated_tokens == 50_000
    assert payload.context_window == 200_000
    assert payload.percent == 25.0
    assert payload.compacting is False


@pytest.mark.asyncio
async def test_status_event_throttled_when_percent_bucket_unchanged() -> None:
    """No re-emit when the integer percent is unchanged (50_000->25.0%, 50_500->25.25%)."""
    opt = _make_optimizer(estimated=50_000)
    await opt.acompress(messages=[_mk_msg()])
    opt._estimate_tokens.return_value = 50_500
    await opt.acompress(messages=[_mk_msg()])
    await _drain_pending_tasks()

    assert len(_status_calls(opt)) == 1


@pytest.mark.asyncio
async def test_status_event_re_emitted_when_percent_bucket_changes():
    opt = _make_optimizer(estimated=50_000)
    await opt.acompress(messages=[_mk_msg()])
    opt._estimate_tokens.return_value = 60_000
    await opt.acompress(messages=[_mk_msg()])
    await _drain_pending_tasks()

    calls = _status_calls(opt)
    assert len(calls) == 2
    assert calls[1].kwargs["data"].percent == 30.0


@pytest.mark.asyncio
async def test_layer_2_brackets_with_compacting_true_then_false():
    opt = _make_optimizer(estimated=200_000)

    async def fake_call(
        system_prompt,
        user_prompt,
        run_metrics=None,
        progress_label="layer 2",
        **kwargs,
    ):
        return "digest", 5, 3

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=fake_call),
    ):
        from agno.models.message import Message

        opt.model = MagicMock(id="mock-model")
        opt.model.get_provider = lambda: "mock"
        messages = [
            Message(role="system", content="sys"),
            Message(role="user", content="u"),
        ]
        await opt.layer_2_auto_compact(messages=messages, trigger="auto")
        await _drain_pending_tasks()

    calls = _status_calls(opt)
    assert len(calls) >= 2
    assert calls[0].kwargs["data"].compacting is True
    assert calls[-1].kwargs["data"].compacting is False


@pytest.mark.asyncio
async def test_layer_2_error_path_still_drops_compacting_flag():
    opt = _make_optimizer(estimated=200_000)

    async def failing_call(*a, **kw):
        raise RuntimeError("provider exploded")

    with (
        patch.object(co, "get_model", side_effect=lambda m: m),
        patch.object(opt, "_run_llm_compaction_call", side_effect=failing_call),
    ):
        from agno.models.message import Message

        opt.model = MagicMock(id="mock-model")
        opt.model.get_provider = lambda: "mock"
        await opt.layer_2_auto_compact(
            messages=[Message(role="system", content="sys")],
            trigger="auto",
        )
        await _drain_pending_tasks()

    calls = _status_calls(opt)
    assert calls, "expected at least one context_status event"
    assert calls[-1].kwargs["data"].compacting is False


@pytest.mark.asyncio
async def test_acompress_swallows_status_publish_failure():
    opt = _make_optimizer(estimated=50_000)
    opt._push_activity_event.side_effect = RuntimeError("redis down")

    await opt.acompress(messages=[_mk_msg()])
    await _drain_pending_tasks()
