import pytest

from matrx_connect.chat_timing import (
    ChatTimingTrace,
    chat_timing_finish,
    chat_timing_mark,
    stamp_inbound_request,
    start_chat_timing,
)


@pytest.fixture(autouse=True)
def _arm_chat_timing(monkeypatch):
    # CHAT_TIME_CHECK_ENABLED is a debug default (off in prod); the gated entry
    # points (start_chat_timing / chat_timing_mark / stamp_inbound_request) no-op
    # when it's off. These tests validate that gated logic, so arm it regardless
    # of the shipped default.
    monkeypatch.setattr("matrx_connect.chat_timing.CHAT_TIME_CHECK_ENABLED", True)


def _sample_trace() -> ChatTimingTrace:
    trace = ChatTimingTrace()
    trace._start = trace._start - 47.9022
    marks = [
        ("route_entry", "agent route entry", 0.0),
        ("prep_begin", "streaming prep begin", 0.0),
        ("prepare_entry", "prepare_agent_run entry", 0.0001),
        ("agx_loaded", "agx.load_for_execution complete", 0.2036),
        ("sandbox_armed", "sandbox resolve_and_arm_run complete", 0.6784),
        ("skills_merged", "apply_unified_skills complete", 1.2071),
        ("tools_merged", "apply_unified_tools complete", 1.2079),
        ("prep_complete", "streaming prep complete", 1.6376),
        ("run_ai_task_entry", "run_ai_task entry", 1.639),
        ("run_ai_task_ready", "pre-execute hooks complete", 1.6394),
        ("pre_provider_execute", "calling UnifiedAIClient.execute", 2.0235),
        ("payload_captured", "provider payload captured", 2.0293),
        ("provider_sdk_call", "anthropic messages.stream", 2.0295),
        ("provider_sdk_complete", "anthropic messages.stream complete", 47.85),
        ("provider_execute_complete", "UnifiedAIClient.execute complete", 47.86),
        ("turn_complete", "execute_ai_request complete", 47.9022),
    ]
    for key, label, elapsed in marks:
        trace.points.append(
            {
                "seq": len(trace.points) + 1,
                "key": key,
                "label": label,
                "elapsed_s": elapsed,
                "delta_s": 0.0,
            }
        )
    for i in range(1, len(trace.points)):
        trace.points[i]["delta_s"] = round(
            trace.points[i]["elapsed_s"] - trace.points[i - 1]["elapsed_s"],
            4,
        )
    return trace


def test_summary_uses_payload_captured_boundary() -> None:
    trace = _sample_trace()
    summary = trace.summary()

    assert summary["prep_s"] == 2.0293
    assert summary["controllable_s"] == 2.0293
    assert summary["prep_complete"] is True
    assert summary["point_count"] == 12
    assert "prep 2.03s" in trace.headline()
    table = trace.block_table()
    assert "prep total" not in table
    assert "Post-provider" not in table
    assert "  total" in table
    assert "  DB" in table
    assert "  local" in table


def test_slowest_segments_exclude_provider_api_block() -> None:
    trace = _sample_trace()
    slowest = trace.summary()["slowest_controllable_segments"]

    assert slowest
    assert all(s["from_key"] != "provider_sdk_call" for s in slowest)
    assert all(s["to_key"] != "provider_sdk_complete" for s in slowest)
    assert slowest[0]["from_key"] == "sandbox_armed"
    assert slowest[0]["to_key"] == "skills_merged"


def test_provider_only_trace_has_zero_prep() -> None:
    trace = ChatTimingTrace()
    trace.points = [
        {"key": "provider_sdk_call", "label": "call 1", "elapsed_s": 1.0, "delta_s": 1.0},
        {"key": "provider_sdk_complete", "label": "done 1", "elapsed_s": 6.0, "delta_s": 5.0},
        {"key": "provider_sdk_call", "label": "call 2", "elapsed_s": 7.0, "delta_s": 1.0},
        {
            "key": "provider_execute_complete",
            "label": "execute done",
            "elapsed_s": 10.0,
            "delta_s": 3.0,
        },
        {"key": "turn_complete", "label": "turn done", "elapsed_s": 10.5, "delta_s": 0.5},
    ]
    summary = trace.summary()

    assert summary["controllable_s"] == 0.0
    assert summary["prep_complete"] is False


def test_controllable_block_percentages_sum_to_100() -> None:
    trace = _sample_trace()
    blocks = [
        block
        for block in trace.summary()["blocks"]
        if not (block["seconds"] <= 0.0 and block["io"] == "local")
    ]
    assert blocks
    assert sum(int(block["pct_controllable"]) for block in blocks) == 100


def test_block_table_columns_align() -> None:
    import re

    from matrx_connect.chat_timing import _BLOCK_LABEL_WIDTH, _IO_TAG_COL_WIDTH

    trace = _sample_trace()
    table = trace.block_table()
    data_lines = [line for line in table.splitlines() if line.startswith("  [")]
    assert data_lines
    secs_start = 2 + _IO_TAG_COL_WIDTH + 1 + _BLOCK_LABEL_WIDTH + 1
    pct_start = secs_start + 8 + 2
    for line in data_lines:
        secs = line[secs_start : secs_start + 8]
        pct = line[pct_start : pct_start + 6]
        assert re.fullmatch(r"\s*\d+\.\d+s", secs)
        assert pct.endswith("%")


def test_prep_summary_emits_at_payload_captured(monkeypatch) -> None:
    emitted: list[str] = []

    def fake_emit(trace: ChatTimingTrace) -> None:
        emitted.append("summary")

    monkeypatch.setattr(
        "matrx_connect.chat_timing._emit_prep_summary_safe",
        lambda trace: fake_emit(trace),
    )

    trace = start_chat_timing()
    assert trace is not None
    chat_timing_mark("payload_captured", "provider payload captured — SDK call next")
    assert chat_timing_mark("provider_sdk_call", "anthropic messages.stream") is None
    assert chat_timing_mark("turn_complete", "done") is None
    assert len(trace.points) == 1

    assert emitted == ["summary"]
    assert trace.summary()["prep_complete"] is True

    finish_summary = chat_timing_finish()
    assert finish_summary is not None


def test_chat_timing_finish_skips_emit_without_boundary() -> None:
    trace = start_chat_timing()
    assert trace is not None
    chat_timing_mark("prep_begin", "streaming prep begin")

    assert chat_timing_finish() is None


def test_inbound_probe_reports_gap_to_first_mark(monkeypatch) -> None:
    base_perf = 1000.0
    clock = {"t": base_perf}

    def perf_counter() -> float:
        return clock["t"]

    monkeypatch.setattr("matrx_connect.chat_timing.time.perf_counter", perf_counter)

    stamp_inbound_request(path="/agents/test")
    clock["t"] = base_perf + 0.05
    trace = start_chat_timing()
    assert trace is not None
    clock["t"] = base_perf + 0.051
    trace.mark("route_entry", "agent route entry")

    summary = trace.summary()
    assert summary["inbound_to_first_mark_s"] == 0.051


# ---------------------------------------------------------------------------
# Always-on collection (latency reporting): the debug flag gates ONLY console output.
# ---------------------------------------------------------------------------


def test_collection_is_always_on_and_flag_defaults_off(monkeypatch, capsys) -> None:
    import importlib

    import matrx_connect.chat_timing as ct

    # The shipped default is False (this module's fixture forces True for the other tests).
    assert importlib.util.find_spec("matrx_connect.chat_timing") is not None
    src = open(ct.__file__).read()
    assert "CHAT_TIME_CHECK_ENABLED = False" in src

    monkeypatch.setattr(ct, "CHAT_TIME_CHECK_ENABLED", False)
    trace = start_chat_timing()
    assert trace is not None
    chat_timing_mark("prep_begin", "streaming prep begin")
    chat_timing_mark("payload_captured", "provider payload captured")
    assert capsys.readouterr().out == ""  # nothing printed
    summary = chat_timing_finish()
    assert summary is not None and summary["prep_complete"] is True
    assert {b["block"] for b in summary["blocks"]} >= {"entry", "agent_load", "wire_config"}


@pytest.mark.parametrize(
    "path",
    ["/v2/ai/agents/abc", "/agents/abc", "/mandates/m/run", "/conversations/c1", "/v2/conversations/c1"],
)
def test_middleware_arm_covers_every_run_route(path) -> None:
    from matrx_connect.chat_timing import arm_chat_timing, get_chat_timing_trace

    assert arm_chat_timing(path=path) is not None
    assert get_chat_timing_trace() is not None
    # a route-level start must keep the middleware's trace, not restart it
    assert start_chat_timing() is get_chat_timing_trace()
    chat_timing_finish()


def test_non_ai_route_is_not_armed() -> None:
    from matrx_connect.chat_timing import arm_chat_timing

    assert arm_chat_timing(path="/health") is None


def test_client_latency_headers_become_a_stamp() -> None:
    from matrx_connect.request_latency import (
        arm_request_latency,
        clear_request_latency,
        get_client_latency_stamp,
    )

    arm_request_latency(
        path="/v2/ai/agents/x",
        headers={"x-matrx-client-sent-at": "1000", "x-matrx-client-prep-ms": "450"},
    )
    stamp = get_client_latency_stamp()
    assert stamp is not None and stamp.client_prep_ms == 450 and stamp.client_sent_at_ms == 1000
    assert stamp.route == "/ai/agents/x"
    assert stamp.network_ms == stamp.server_arrived_at_ms - 1000
    clear_request_latency()
    assert get_client_latency_stamp() is None
