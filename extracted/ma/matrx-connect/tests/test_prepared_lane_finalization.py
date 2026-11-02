"""Lane-before-prep finalization safety.

`create_prepared_streaming_response` opens the RequestLane BEFORE running prep so
prep-phase DB writes queue into the request's coordinator instead of blocking.
The load-bearing safety rule: if prep raises before a streaming response takes
ownership of the lane, the lane MUST still be drained here — otherwise a write
prep already queued would be silently lost. These tests use a registered
finalizer as a stand-in for "a queued prep write" and assert it fires exactly
once on the failure path, and that the lane never leaks in the ContextVar.

Pure asyncio + matrx-connect; no DB, no other matrx-* package.
"""

from __future__ import annotations

import types

import pytest
from fastapi import HTTPException

from matrx_connect.lane import get_current_lane
from matrx_connect.streaming.response import create_prepared_streaming_response


def _ctx(emitter=None):
    return types.SimpleNamespace(
        request_id="req-test-1",
        user_id="user-1",
        conversation_id=None,
        source_app="test",
        agent_id=None,
        emitter=emitter,
    )


async def _noop_run(emitter):  # never reached on the failure paths
    return None


@pytest.mark.asyncio
async def test_httpexception_during_prep_drains_lane_then_reraises():
    """R1: a write queued in prep flushes even when prep raises HTTPException.

    Also proves the core enabling behavior: a lane is CURRENT during prep.
    """
    fired: list[str] = []

    async def prepare():
        lane = get_current_lane()
        assert lane is not None, "a lane must be current during prep"
        assert lane.id == "req-test-1"

        async def _queued_write_finalizer(fctx):
            fired.append(fctx.outcome)

        lane.add_finalizer(_queued_write_finalizer, name="stand-in-prep-write")
        raise HTTPException(status_code=409, detail="duplicate")

    with pytest.raises(HTTPException) as excinfo:
        await create_prepared_streaming_response(_ctx(emitter=object()), prepare, _noop_run)

    assert excinfo.value.status_code == 409
    # The finalizer (stand-in for the queued prep write) fired EXACTLY once —
    # the lane was drained on the prep-HTTPException path before re-raising.
    assert len(fired) == 1


@pytest.mark.asyncio
async def test_lane_released_from_contextvar_after_prep_failure():
    """No lane leak: after a prep failure the ContextVar is back to None."""

    async def prepare():
        assert get_current_lane() is not None
        raise HTTPException(status_code=422, detail="bad")

    with pytest.raises(HTTPException):
        await create_prepared_streaming_response(_ctx(emitter=object()), prepare, _noop_run)

    assert get_current_lane() is None


@pytest.mark.asyncio
async def test_generic_exception_during_prep_also_drains():
    """A non-HTTP prep exception is deferred into the stream task, which adopts
    the lane — so the queued write still flushes (handed off, not lost)."""
    fired: list[str] = []

    async def prepare():
        lane = get_current_lane()

        async def _fin(fctx):
            fired.append(fctx.outcome)

        lane.add_finalizer(_fin, name="stand-in-write")
        raise ValueError("prep blew up")

    # Returns a StreamingResponse (the error is deferred into the task). The lane
    # is handed off to that response; it is NOT drained synchronously here, so
    # the finalizer has not fired yet at return time.
    resp = await create_prepared_streaming_response(_ctx(emitter=object()), prepare, _noop_run)
    assert resp is not None
    assert fired == []


@pytest.mark.asyncio
async def test_prep_error_ignores_stale_context_without_emitter():
    """A stale task context must not replace the explicit stream context."""
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        set_app_context,
    )

    token = set_app_context(AppContext(emitter=None, user_id="stale-user"))

    async def prepare():
        raise ValueError("prep blew up")

    try:
        resp = await create_prepared_streaming_response(
            _ctx(emitter=object()),
            prepare,
            _noop_run,
        )
        assert resp is not None
    finally:
        clear_app_context(token)


# --------------------------------------------------------------------------- #
# KD-1 Phase 2 — lane at ROUTE entry (open_route_lane + lane adoption)         #
# --------------------------------------------------------------------------- #

from matrx_connect.streaming.response import open_route_lane  # noqa: E402


@pytest.mark.asyncio
async def test_route_lane_drains_and_releases_when_not_handed_off():
    """A route-entry lane whose request never reaches a streaming response
    (404/409/422 or any raise) drains its queued prep writes and releases
    the ContextVar."""
    fired: list[str] = []

    with pytest.raises(HTTPException):
        async with open_route_lane(_ctx(emitter=object())) as route_lane:
            lane = get_current_lane()
            assert lane is route_lane.lane
            assert lane.id == "req-test-1"

            async def _fin(fctx):
                fired.append(fctx.outcome)

            lane.add_finalizer(_fin, name="stand-in-prep-write")
            raise HTTPException(status_code=409, detail="duplicate")

    assert fired == ["error"]
    assert get_current_lane() is None


@pytest.mark.asyncio
async def test_route_lane_hand_off_skips_exit_drain():
    """Once hand_off() is called, the route exit does NOT drain — the streaming
    generator owns finalization from that point."""
    fired: list[str] = []

    async with open_route_lane(_ctx(emitter=object())) as route_lane:
        async def _fin(fctx):
            fired.append(fctx.outcome)

        route_lane.lane.add_finalizer(_fin, name="stand-in-write")
        route_lane.hand_off()

    assert fired == []  # exit did not drain
    # Clean up for other tests: drain + release manually (the "generator").
    await route_lane.lane.begin_drain(failed=False, soft=False)
    assert fired == ["stream_end"]
    from matrx_connect.lane.contextvar import reset_current_lane

    reset_current_lane(route_lane.token)
    assert get_current_lane() is None


@pytest.mark.asyncio
async def test_prepared_response_adopts_route_lane_no_second_lane():
    """create_prepared_streaming_response(existing_lane=...) must ADOPT the
    route-entry lane: prep sees the SAME lane object, and a prep HTTPException
    drains it exactly once (double-drain is an idempotent no-op)."""
    fired: list[str] = []
    seen_lanes: list[object] = []

    async with open_route_lane(_ctx(emitter=object())) as route_lane:
        async def prepare():
            lane = get_current_lane()
            seen_lanes.append(lane)

            async def _fin(fctx):
                fired.append(fctx.outcome)

            lane.add_finalizer(_fin, name="stand-in-prep-write")
            raise HTTPException(status_code=404, detail="missing")

        with pytest.raises(HTTPException):
            await create_prepared_streaming_response(
                _ctx(emitter=object()),
                prepare,
                _noop_run,
                existing_lane=route_lane.lane,
                existing_lane_token=route_lane.token,
            )

    assert seen_lanes == [route_lane.lane]  # adopted, not a second lane
    assert fired == ["error"]  # drained exactly once despite two drain layers
    assert get_current_lane() is None
