"""The ctx handed to ``create_streaming_response`` is the ctx the task runs under.

THE BREAK THIS GUARDS (census 2026-09-20, six live routes): a route derived a
ctx — ``ctx = ctx.with_overrides(organization_id=run_org)`` — and passed it to
``create_streaming_response`` without calling ``set_app_context`` first, which
the builder's docstring said was the caller's job. ``with_overrides`` never
touches the ContextVar by design, so the spawned task read the MIDDLEWARE ctx
ambiently: an organization_id of ``None`` or a conversation_id of ``""``, and
downstream persistence refused or crashed. Seven call sites grew "re-read the
organization from the run row" workarounds to survive it.

The builder now installs what it is handed before spawning the task. These
tests prove it from the task's own point of view — ``get_app_context()`` inside
the task must return the derived ctx — and prove the guard is falsifiable by
planting the old behavior (skipping the install) and watching the same
assertion fail.

Pure asyncio + matrx-connect: a real AppContext, a real StreamEmitter, the real
builder, the real body iterator. No DB.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_connect.context.app_context import (
    AppContext,
    _app_context,
    get_app_context,
    set_app_context,
)
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.lane import get_current_lane
from matrx_connect.streaming import response as response_mod
from matrx_connect.streaming.response import create_streaming_response, open_route_lane

MIDDLEWARE_ORG = "11111111-1111-4111-8111-111111111111"
DERIVED_ORG = "22222222-2222-4222-8222-222222222222"


def _middleware_ctx(emitter: StreamEmitter) -> AppContext:
    return AppContext(
        emitter=emitter,
        user_id="user-1",
        auth_type="token",
        is_authenticated=True,
        organization_id=MIDDLEWARE_ORG,
        organization_admission="verified",
        request_id="req-ctx-install-1",
    )


async def _drain(response: Any) -> None:
    async for _ in response.body_iterator:
        pass


async def _never_run(_emitter: Any) -> None:
    raise AssertionError("startup failure must stop before the work handler runs")


async def _run(_emitter: Any, seen: dict[str, Any]) -> None:
    """The streaming task: record what the AMBIENT context says, the way every
    downstream persistence helper reads it."""
    seen["organization_id"] = get_app_context().organization_id
    seen["conversation_id"] = get_app_context().conversation_id


@pytest.mark.asyncio
async def test_task_sees_the_derived_ctx_not_the_middleware_one() -> None:
    emitter = StreamEmitter(heartbeat_interval=600)
    base = _middleware_ctx(emitter)
    # What AuthMiddleware does: install the request ctx.
    token = set_app_context(base)
    try:
        # What the six broken routes did: derive, and DO NOT set_app_context.
        derived = base.with_overrides(
            organization_id=DERIVED_ORG, conversation_id="conv-derived"
        )
        seen: dict[str, Any] = {}
        response = create_streaming_response(derived, _run, seen, debug_label="ctx-guard")
        await _drain(response)
    finally:
        _app_context.reset(token)

    assert seen["organization_id"] == DERIVED_ORG, (
        "the streaming task read the MIDDLEWARE organization, not the one the "
        f"route derived: got {seen['organization_id']!r}. The builder did not "
        "install the ctx it was handed."
    )
    assert seen["conversation_id"] == "conv-derived"


@pytest.mark.asyncio
async def test_install_is_scoped_to_the_response_and_does_not_leak() -> None:
    """After the response finishes, the caller's ContextVar is what it was."""
    emitter = StreamEmitter(heartbeat_interval=600)
    base = _middleware_ctx(emitter)
    token = set_app_context(base)
    try:
        derived = base.with_overrides(organization_id=DERIVED_ORG)
        seen: dict[str, Any] = {}
        response = create_streaming_response(derived, _run, seen, debug_label="ctx-leak")
        await _drain(response)
        assert get_app_context().organization_id == MIDDLEWARE_ORG, (
            "the builder's install leaked past the response — the request ctx "
            "now carries the task's override"
        )
    finally:
        _app_context.reset(token)


@pytest.mark.asyncio
async def test_planted_old_behaviour_fails_the_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    """Falsifiability: remove the install (the pre-2026-09-20 body) and the
    first guard's exact assertion must fail, naming the middleware org."""
    monkeypatch.setattr(
        response_mod, "set_app_context", lambda _ctx: _app_context.set(_app_context.get())
    )
    emitter = StreamEmitter(heartbeat_interval=600)
    base = _middleware_ctx(emitter)
    token = set_app_context(base)
    try:
        derived = base.with_overrides(organization_id=DERIVED_ORG)
        seen: dict[str, Any] = {}
        response = create_streaming_response(derived, _run, seen, debug_label="ctx-planted")
        await _drain(response)
    finally:
        _app_context.reset(token)

    with pytest.raises(AssertionError) as failure:
        assert seen["organization_id"] == DERIVED_ORG, (
            f"got {seen['organization_id']!r}"
        )
    assert MIDDLEWARE_ORG in str(failure.value)


@pytest.mark.asyncio
async def test_create_task_startup_failure_unregisters_stream_and_drains_lane(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failure after active-stream registration but before task allocation keeps its cause."""
    from matrx_connect.context.app_context import _app_context
    from matrx_connect.emitters.stream_emitter import get_active_stream

    emitter = StreamEmitter(heartbeat_interval=600)
    ctx = AppContext(
        emitter=emitter,
        user_id="user-1",
        auth_type="token",
        is_authenticated=True,
        organization_id=MIDDLEWARE_ORG,
        organization_admission="verified",
        request_id="req-start-before-task",
    )
    monkeypatch.setattr(response_mod, "create_stream_journal_sink", lambda _ctx: _no_journal())

    class StartupError(RuntimeError):
        pass

    def fail_create_task(_coro):
        raise StartupError("create task failed")

    monkeypatch.setattr(response_mod.asyncio, "create_task", fail_create_task)
    fired: list[str] = []
    async with open_route_lane(ctx) as route_lane:
        async def finalizer(fctx):
            fired.append(fctx.outcome)

        route_lane.lane.add_finalizer(finalizer, name="startup-drain-proof")
        response = create_streaming_response(
            ctx,
            _never_run,
            existing_lane=route_lane.lane,
            existing_lane_token=route_lane.token,
        )
        route_lane.hand_off()
        with pytest.raises(StartupError, match="create task failed"):
            await _drain(response)

    assert fired == ["error"]
    assert get_current_lane() is None
    assert _app_context.get() is None
    assert get_active_stream(ctx.request_id) is None


@pytest.mark.asyncio
async def test_emitter_task_hook_failure_cancels_allocated_task_and_drains_lane(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A task allocated before a broken emitter hook is joined, not detached or orphaned."""
    from matrx_connect.context.app_context import _app_context
    from matrx_connect.emitters.stream_emitter import get_active_stream

    class RejectingEmitter(StreamEmitter):
        allocated: asyncio.Task[None] | None = None

        def set_task(self, task: asyncio.Task[None]) -> None:
            self.allocated = task
            raise RuntimeError("emitter rejected task")

    emitter = RejectingEmitter(heartbeat_interval=600)
    ctx = AppContext(
        emitter=emitter,
        user_id="user-1",
        auth_type="token",
        is_authenticated=True,
        organization_id=MIDDLEWARE_ORG,
        organization_admission="verified",
        request_id="req-start-after-task",
    )

    async def no_journal(_ctx):
        return None

    monkeypatch.setattr(response_mod, "create_stream_journal_sink", no_journal)
    fired: list[str] = []
    async with open_route_lane(ctx) as route_lane:
        async def finalizer(fctx):
            fired.append(fctx.outcome)

        route_lane.lane.add_finalizer(finalizer, name="startup-drain-proof")
        response = create_streaming_response(
            ctx,
            _never_run,
            existing_lane=route_lane.lane,
            existing_lane_token=route_lane.token,
        )
        route_lane.hand_off()
        with pytest.raises(RuntimeError, match="emitter rejected task"):
            await _drain(response)

    await asyncio.sleep(0)
    assert emitter.allocated is not None and emitter.allocated.cancelled()
    assert fired == ["error"]
    assert get_current_lane() is None
    assert _app_context.get() is None
    assert get_active_stream(ctx.request_id) is None


async def _no_journal():
    return None
