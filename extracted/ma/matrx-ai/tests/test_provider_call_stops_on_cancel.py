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


@pytest.mark.asyncio
async def test_a_spine_stop_that_lands_just_after_the_call_starts_stops_it_quickly(monkeypatch):
    """CGU-09 P1-2 (live, 2026-10-31): a Stop pressed ~0.15 s after Send reaches the run's control row a moment
    AFTER the run's first boundary check (the cancel landed on another server task, which stamps the row once the
    run opens it). The call is then stopped only by the mid-call spine poll — every 2 s, so a fast model wrote its
    whole 6,000-character reply in that gap and the Stop was lost. The poll must catch it within a second."""
    import time

    loop = asyncio.get_running_loop()
    stamped_at = loop.time() + 0.2

    async def spine_reason():
        return "cancel requested" if loop.time() >= stamped_at else None

    monkeypatch.setattr(executor, "_spine_stop_reason", spine_reason)

    async def fake_provider_call():
        await asyncio.sleep(10)
        return "the whole essay"

    started = time.monotonic()
    with pytest.raises(executor.ProviderCallStopped):
        await executor._execute_stoppable(fake_provider_call(), "stop-test-spine-late")
    assert time.monotonic() - started < 1.0, "the late spine stop took a full poll interval to land"


@pytest.mark.asyncio
async def test_a_spine_stop_that_lands_between_polls_still_stops_a_call_that_then_finishes(monkeypatch):
    """CGU-09 stop-during-thinking (live 2026-11-12, conversation c3842650): Stop was pressed while the model was
    still thinking; the cancel landed on another server task and stamped the run's control row at 38.30 s, the model's
    thought and its whole short answer arrived at 38.57-38.81 s, and the call returned before the next spine poll.
    The call was recorded complete, its answer saved whole and streamed out after the Stop — the phone then drew a
    second answer under "Stopped". A Stop that reached the run before its call ended is a live Stop."""
    loop = asyncio.get_running_loop()
    stamped_at = loop.time() + 0.55  # after the first spine poll (0.5 s), before the next (1.0 s)

    async def spine_reason():
        return "cancel requested" if loop.time() >= stamped_at else None

    monkeypatch.setattr(executor, "_spine_stop_reason", spine_reason)

    async def fake_provider_call():
        await asyncio.sleep(0.7)  # thinking, then the short answer all at once
        return "the whole short answer"

    with pytest.raises(executor.ProviderCallStopped):
        await executor._execute_stoppable(fake_provider_call(), "stop-test-spine-between-polls")


@pytest.mark.asyncio
async def test_an_in_process_stop_that_lands_between_ticks_still_stops_a_call_that_then_finishes():
    """The same race on the in-process registry: the cancel lands between two 0.25 s ticks and the call finishes
    before the next one."""
    request_id = "stop-test-registry-between-ticks"

    async def fake_provider_call():
        await asyncio.sleep(0.3)
        await RequestControlRegistry.get_instance().cancel(request_id)
        await asyncio.sleep(0.05)
        return "the whole short answer"

    with pytest.raises(executor.ProviderCallStopped):
        await executor._execute_stoppable(fake_provider_call(), request_id)


@pytest.mark.asyncio
async def test_a_stop_already_known_when_the_call_would_start_never_sends_it():
    """Live 2026-11-16 (F2, F4, request 583a5433): the Stop's stamp landed while the send boundary built the payload,
    after the loop's last look and before the wire. The call went out, was cut 50-170 ms later and billed the whole
    prompt (48,133 input tokens, every time). A stop known when the call would start ends it before it starts."""
    request_id = "stop-test-before-the-wire"
    started = {"call": False}

    async def fake_provider_call():
        started["call"] = True
        await asyncio.sleep(10)
        return "full answer"

    await RequestControlRegistry.get_instance().cancel(request_id)
    call = fake_provider_call()
    with pytest.raises(executor.ProviderCallStopped) as stopped:
        await executor._execute_stoppable(call, request_id)
    assert started["call"] is False, "the provider call was started after the stop was known"
    from matrx_ai.providers.errors import get_billed_usage

    assert get_billed_usage(stopped.value) is None, "nothing was sent, so nothing is billed"
