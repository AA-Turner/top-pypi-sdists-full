"""A client that leaves BEFORE the body starts must not stop the work.

THE BREAK THIS GUARDS (FX-N, 2026-09-30, reproduced from web chat ``265953a3``):
a person opened an agent run and the page reloaded while the server was still
preparing the turn (tool merge, surface context). The conversation row was
published with its start claim (``last_request_status='pending'``) — and then
nothing: no user_request, no messages, no request, no error, no log line.

``create_streaming_response`` started the work task INSIDE the response body
generator, after the opening frames. A client that is already gone when the
route returns never drives that generator far enough: Starlette's
``StreamingResponse`` (ASGI spec 2.3, what uvicorn serves) sees
``http.disconnect`` and cancels the body before the task exists; on spec 2.4
the first ``send`` raises and the body is never entered at all. The run, and
every write queued into its lane during prep, vanished silently — against the
platform law that a disconnect never stops server work.

These tests drive the REAL Starlette ``StreamingResponse.__call__`` with a
receive channel whose client is already gone, and assert the route's run_fn
still runs to completion and the lane still drains.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_connect.context.app_context import AppContext, get_app_context
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.lane import RequestLane
from matrx_connect.streaming import journal as journal_mod
from matrx_connect.streaming.response import create_streaming_response

ORG = "5b0e4a51-8d2f-4c52-9d0a-2f3c1e7a9b10"


def _ctx(emitter: StreamEmitter, request_id: str) -> AppContext:
    return AppContext(
        emitter=emitter,
        user_id="user-front-desk",
        auth_type="token",
        is_authenticated=True,
        organization_id=ORG,
        organization_admission="verified",
        request_id=request_id,
        conversation_id="conv-reloaded-mid-prep",
    )


async def _gone_receive() -> dict[str, Any]:
    # The page reloaded during prep: the very first thing the server hears is
    # that the client is gone.
    return {"type": "http.disconnect"}


async def _run(emitter: Any, done: asyncio.Event, seen: dict[str, Any]) -> None:
    await asyncio.sleep(0.05)  # real work takes a moment (provider call, tools)
    seen["organization_id"] = get_app_context().organization_id
    await emitter.send_end()
    done.set()


@pytest.fixture(autouse=True)
def _host_journal(monkeypatch: pytest.MonkeyPatch) -> None:
    """The host's journal opens with a real round trip (aidream: a Postgres insert),
    so opening it is an await the disconnect can land on."""

    async def factory(_ctx: AppContext) -> None:
        await asyncio.sleep(0.01)
        return None

    monkeypatch.setattr(journal_mod, "_sink_factory", factory)


async def _serve(response: Any, spec_version: str) -> None:
    sent: list[dict[str, Any]] = []

    async def send(message: dict[str, Any]) -> None:
        if spec_version >= "2.4":
            raise OSError("client went away")  # what 2.4 servers surface
        sent.append(message)

    scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": spec_version}}
    try:
        await response(scope, _gone_receive, send)
    except Exception:  # noqa: BLE001 — Starlette's ClientDisconnect on 2.4
        pass


@pytest.mark.asyncio
@pytest.mark.parametrize("spec_version", ["2.3", "2.4"])
async def test_work_runs_when_the_client_left_before_the_body(
    spec_version: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    drains: list[dict[str, Any]] = []
    real_drain = RequestLane.begin_drain

    async def recording_drain(self: RequestLane, **kwargs: Any) -> Any:
        drains.append(kwargs)
        return await real_drain(self, **kwargs)

    monkeypatch.setattr(RequestLane, "begin_drain", recording_drain)
    emitter = StreamEmitter(heartbeat_interval=600)
    ctx = _ctx(emitter, f"req-gone-{spec_version}")
    done = asyncio.Event()
    seen: dict[str, Any] = {}

    response = create_streaming_response(ctx, _run, done, seen, debug_label="gone-before-body")
    await _serve(response, spec_version)

    try:
        await asyncio.wait_for(done.wait(), timeout=5)
    except TimeoutError:
        pytest.fail(
            "the client left before the response body started and the route's work "
            "NEVER RAN — a disconnect stopped server work (the 265953a3 run)."
        )
    assert seen["organization_id"] == ORG, "the detached run lost the ctx it was handed"
    for _ in range(50):  # the supervisor drains right after the work finishes
        if drains:
            break
        await asyncio.sleep(0.02)
    assert drains == [{"failed": False, "soft": False}], (
        "the lane holding prep's queued writes (user_request, the user message) was "
        f"never drained after the detached run: {drains!r}"
    )
    assert emitter.has_ended, "the detached run never terminalized its stream"
