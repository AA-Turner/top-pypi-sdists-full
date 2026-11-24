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


def _trace_of(marks: list[tuple[str, float]]) -> ChatTimingTrace:
    trace = ChatTimingTrace()
    prev = 0.0
    for key, elapsed in marks:
        trace.points.append(
            {"seq": len(trace.points) + 1, "key": key, "label": key, "elapsed_s": elapsed,
             "delta_s": round(elapsed - prev, 4)}
        )
        prev = elapsed
    return trace


def test_a_wait_inside_context_assembly_is_named_never_hidden_in_stream_handoff() -> None:
    """2026-11-19: the phone hand-off's 10 s sandbox brief wait sat between two marks that
    closed in "stream_handoff" (a 'local' block), so the ledger called it free. Every stage of
    the context assembly and the staff door now closes its own named block."""
    trace = _trace_of(
        [
            ("prep_begin", 0.0),
            ("staff_thread_opened", 0.3),
            ("staff_admitted", 0.7),
            ("tools_merged", 2.0),
            ("u_intro_built", 2.1),
            ("c_gate_open", 2.15),
            ("c_seeded", 2.2),
            ("c_sources_resolved", 2.3),
            ("c_earlier_turn", 2.35),
            ("c_sandbox_briefing", 12.35),
            ("c_attachments", 12.4),
            ("h_dispatch_guards", 12.45),
            ("payload_captured", 12.9),
        ]
    )
    blocks = {b["block"]: b["seconds"] for b in trace.summary()["blocks"]}
    assert blocks["sandbox_briefing"] == pytest.approx(10.0)
    assert blocks["staff_door"] == pytest.approx(0.7)
    assert blocks["context_assembly"] == pytest.approx(0.3)
    assert blocks["stream_handoff"] == pytest.approx(0.05)
    # Nothing falls outside a block: every prep second is attributed.
    assert sum(blocks.values()) == pytest.approx(12.9)


def test_a_continuations_history_load_is_named_never_filed_under_tools() -> None:
    """2026-11-19, request 9c954c55: the continue path closed no mark between the staff door and
    ``tools_merge_start``, so the 3.6 s history load and the sandbox arm read as 5.56 s of "tools".
    The history load, the sandbox arm and the skills each close their own block now, and the
    context assembly's sub-stages are marks inside its own block."""
    trace = _trace_of(
        [
            ("prep_begin", 0.0),
            ("staff_admitted", 0.8),
            ("history_resolved", 4.4),
            ("sandbox_armed", 5.0),
            ("skills_merged", 5.1),
            ("tools_merge_start", 5.15),
            ("tools_merged", 5.2),
            ("c_gate_open", 5.3),
            ("c_seeded", 5.4),
            ("c_lazy_described", 8.4),
            ("c_file_blocks", 8.6),
            ("c_ref_flags", 8.7),
            ("c_sources_resolved", 9.4),
            ("payload_captured", 9.5),
        ]
    )
    blocks = {b["block"]: b["seconds"] for b in trace.summary()["blocks"]}
    assert blocks["history"] == pytest.approx(3.6)
    assert blocks["sandbox"] == pytest.approx(0.6)
    assert blocks["tools"] == pytest.approx(0.1)
    assert blocks["context_assembly"] == pytest.approx(4.2)
    assert sum(blocks.values()) == pytest.approx(9.5)


def test_a_mandated_continuation_names_every_step_never_tools_or_wire_config() -> None:
    """2026-11-19 proof round 4, the phone line's second staff ask: "tools" 1.47 s and "wire_config" 0.81 s were
    whole unmarked spans — the mandated start, the run gates, the continuation setup and the history load all closed
    at ``tools_merge_start``; the executor's pre-send checks and the send boundary's stages all closed at
    ``wire_config_built``. Each now closes its own named block."""
    trace = _trace_of(
        [
            ("prep_begin", 0.0),
            ("staff_admitted", 0.1),
            ("m_holder_resolved", 0.2),
            ("m_framing_built", 0.3),
            ("m_values_routed", 0.35),
            ("m_run_recorded", 0.4),
            ("orchestra_probed", 0.45),
            ("run_gates_passed", 0.55),
            ("cr_context_restored", 0.65),
            ("memory_resolved", 0.7),
            ("cr_scope_tracked", 0.8),
            ("h_structure_read", 0.85),
            ("h_holder_built", 0.95),
            ("h_messages_loaded", 1.25),
            ("history_resolved", 1.3),
            ("sandbox_armed", 1.35),
            ("skills_merged", 1.4),
            ("tools_merge_start", 1.42),
            ("tools_merged", 1.5),
            ("structured_inputs_resolved", 1.6),
            ("pre_send_checks", 1.65),
            ("sb_media_stored", 1.7),
            ("sb_shaped", 1.8),
            ("sb_trimmed", 1.9),
            ("sb_fit", 2.0),
            ("sb_turn_context_staged", 2.3),
            ("wire_config_built", 2.4),
            ("payload_captured", 2.45),
        ]
    )
    blocks = {b["block"]: b["seconds"] for b in trace.summary()["blocks"]}
    assert blocks["mandate_start"] == pytest.approx(0.3)
    assert blocks["run_gates"] == pytest.approx(0.15)
    assert blocks["continue_setup"] == pytest.approx(0.2)
    assert blocks["history"] == pytest.approx(0.5)
    assert blocks["tools"] == pytest.approx(0.1)
    assert blocks["send_prep"] == pytest.approx(0.7)
    assert blocks["wire_config"] == pytest.approx(0.15)
    assert sum(blocks.values()) == pytest.approx(2.45)
