"""A cancel STOPS a provider call that is generating — not just the next turn.

Page-pass 2026-09-27 (/agent-apps/[id]/run, conversation e23b3153): Stop was
pressed 3.5s into a single-turn Fact Checker run; POST /ai/cancel landed, but
the executor only polled cancellation at iteration boundaries, so the one
provider call generated to the end and the run was recorded complete.

`_execute_stoppable` runs the call beside a stop poll: a cancel cancels the
provider task (generation stops) and raises ProviderCallStopped. The fake
provider below proves the call was really interrupted, not awaited to the end.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect.request_controls import RequestControlRegistry

from matrx_ai.orchestrator import executor


@pytest.mark.asyncio
async def test_cancel_during_generation_stops_the_provider_call():
    request_id = "stop-test-generating"
    progress = {"chunks": 0, "finished": False, "cancelled": False}

    async def fake_provider_call():
        try:
            for _ in range(200):  # ~10s of "generation"
                await asyncio.sleep(0.05)
                progress["chunks"] += 1
            progress["finished"] = True
            return "full answer"
        except asyncio.CancelledError:
            progress["cancelled"] = True
            raise

    async def press_stop():
        await asyncio.sleep(0.4)
        await RequestControlRegistry.get_instance().cancel(request_id)

    stopper = asyncio.create_task(press_stop())
    with pytest.raises(executor.ProviderCallStopped):
        await executor._execute_stoppable(fake_provider_call(), request_id)
    await stopper

    assert progress["cancelled"] is True
    assert progress["finished"] is False
    # Stopped within about one poll interval of the cancel, not after 10s.
    assert progress["chunks"] < 30


@pytest.mark.asyncio
async def test_an_uncancelled_call_returns_its_result():
    async def fake_provider_call():
        await asyncio.sleep(0.3)
        return "full answer"

    assert await executor._execute_stoppable(fake_provider_call(), "stop-test-normal") == "full answer"


@pytest.mark.asyncio
async def test_a_stopped_call_carries_what_the_provider_billed():
    """A stop (person, tree budget, deadline) cuts a call that already spent
    tokens. The adapter stamps that usage on the call's CancelledError; it must
    ride ProviderCallStopped out so the stopped run's cost is not $0."""
    from matrx_ai.config import TokenUsage
    from matrx_ai.providers.errors import attach_billed_usage, get_billed_usage

    request_id = "stop-test-billed"
    billed = TokenUsage(input_tokens=900, output_tokens=40, matrx_model_name="m", api="xai")

    async def fake_provider_call():
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError as exc:
            attach_billed_usage(exc, billed)
            raise

    async def press_stop():
        await asyncio.sleep(0.3)
        await RequestControlRegistry.get_instance().cancel(request_id)

    stopper = asyncio.create_task(press_stop())
    with pytest.raises(executor.ProviderCallStopped) as stopped:
        await executor._execute_stoppable(fake_provider_call(), request_id)
    await stopper

    assert get_billed_usage(stopped.value) is billed
