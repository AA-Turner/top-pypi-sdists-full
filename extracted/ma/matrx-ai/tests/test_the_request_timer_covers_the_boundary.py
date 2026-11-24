"""THE REQUEST'S OWN TIMER COVERS ITS BOUNDARY (CGU-10 AND-IMG18, finding N7).

``total_duration_ms - api_duration_ms`` (the server's own time on a turn) started at the first iteration, so the work
before it — auth, body normalization, the boundary's picture resolution, history load — was on nobody's timer: live
AND-V IMG17 saw ~1.45 s of wall time minus provider time at 20 history pictures against ~0.6 s on the timer. The
first iteration now carries the seconds since the request reached the server (the auth middleware's inbound stamp),
and the request total includes them.
"""

from __future__ import annotations

import time

from matrx_ai.orchestrator.tracking import TimingUsage


def test_the_total_includes_the_boundary() -> None:
    first = TimingUsage(start_time=100.0, end_time=103.0, api_call_duration=2.0, iteration=1, boundary_duration=0.8)
    second = TimingUsage(start_time=103.0, end_time=104.0, api_call_duration=0.5, iteration=2)
    agg = TimingUsage.aggregate([first, second])
    assert agg["total_duration"] == 4.8
    assert agg["boundary_duration"] == 0.8
    assert round(agg["processing_duration"], 6) == 2.3  # the boundary is the server's own time


def test_the_first_iteration_reads_the_inbound_stamp() -> None:
    from matrx_connect.chat_timing import _inbound, _InboundStamp

    from matrx_ai.orchestrator.executor import _request_boundary_seconds

    assert _request_boundary_seconds() == 0.0  # no stamped request: nothing invented
    token = _inbound.set(_InboundStamp(perf=time.perf_counter() - 0.25, wall_utc="", path="/ai/chat"))
    try:
        assert 0.25 <= _request_boundary_seconds() < 1.0
    finally:
        _inbound.reset(token)
    stale = _inbound.set(_InboundStamp(perf=time.perf_counter() - 600, wall_utc="", path="/ai/chat"))
    try:
        assert _request_boundary_seconds() == 0.0  # a resumed run's old stamp is not this request's boundary
    finally:
        _inbound.reset(stale)


# ── CGU-10 AND-IMG19 F4: live, 0 of 287 requests carried a boundary. The user request's total is the ROLLUP of its
# iteration rows (``CxManager`` cost rollup), which summed each row's own total and never saw the boundary. The
# boundary now rides the first row's metadata and the rollup adds it; and it is taken once per request, so a
# sub-agent (same copied context) never re-counts the parent's wait.


def test_a_request_takes_its_boundary_once() -> None:
    from matrx_connect.chat_timing import _inbound, _InboundStamp

    from matrx_ai.orchestrator.executor import _request_boundary_seconds

    token = _inbound.set(_InboundStamp(perf=time.perf_counter() - 0.3, wall_utc="", path="/ai/chat"))
    try:
        assert 0.3 <= _request_boundary_seconds() < 1.0
        assert _request_boundary_seconds() == 0.0  # a sub-agent in the same request: the parent already counted it
    finally:
        _inbound.reset(token)


def _completed_with(timings: list[TimingUsage]):
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.config.usage_config import TokenUsage
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    req = AIMatrixRequest(
        conversation_id="c1",
        config=UnifiedConfig(model="gpt-oss-120b", messages=[{"role": "user", "content": "hi"}]),
        usage_history=[
            TokenUsage(input_tokens=10, output_tokens=5, matrx_model_name="gpt-oss-120b", api="together")
            for _ in timings
        ],
        timing_history=timings,
    )
    return CompletedRequest(request=req, iterations=len(timings), final_response=None)


def test_the_user_request_rollup_includes_the_boundary() -> None:
    from types import SimpleNamespace

    from matrx_ai.db._cx_managers_impl import request_boundary_ms

    first = TimingUsage(start_time=100.0, end_time=103.0, api_call_duration=2.0, iteration=1, boundary_duration=0.8)
    second = TimingUsage(start_time=103.0, end_time=104.0, api_call_duration=0.5, iteration=2)
    rows = _completed_with([first, second]).to_storage_dict()["requests"]
    assert rows[0]["metadata"]["boundary_duration_ms"] == 800
    assert "boundary_duration_ms" not in (rows[1].get("metadata") or {})
    # The rollup: each row's own total plus the boundary its metadata carries.
    summed = sum(int(r["total_duration_ms"]) + request_boundary_ms(SimpleNamespace(metadata=r.get("metadata"))) for r in rows)
    assert summed == 4800
