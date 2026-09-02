"""Tests for the slim client-side flow_trace port."""

import threading

import pytest

from runlayer_cli import flow_trace
from runlayer_cli.flow_contract import MAX_STEPS_PER_FLOW
from runlayer_cli.flow_summary import build_summary, merge_intervals_ms
from runlayer_cli.flow_trace import (
    FlowTrace,
    _NULL_STEP,
    StepRecord,
    current_flow,
    disable_flow_tracing,
    enable_flow_tracing,
    flow,
    is_enabled,
    mark_error,
    operation,
    reset_flow,
    step,
)
from runlayer_cli.hook import hook_io


@pytest.fixture(autouse=True)
def _clean_flow_state():
    disable_flow_tracing()
    flow_trace.set_error_classifier(None)
    flow_trace.set_server_id(None)
    reset_flow()
    yield
    disable_flow_tracing()
    flow_trace.set_error_classifier(None)
    flow_trace.set_server_id(None)
    reset_flow()


@pytest.fixture
def sink():
    summaries: list[dict] = []
    enable_flow_tracing(summaries.append)
    return summaries


class TestMergeIntervals:
    def test_empty(self):
        assert merge_intervals_ms([]) == 0.0

    def test_disjoint(self):
        assert merge_intervals_ms([(0.0, 10.0), (20.0, 30.0)]) == 20.0

    def test_overlapping_counted_once(self):
        assert merge_intervals_ms([(0.0, 10.0), (5.0, 15.0)]) == 15.0

    def test_nested_counted_once(self):
        assert merge_intervals_ms([(0.0, 100.0), (10.0, 20.0)]) == 100.0

    def test_unsorted_input(self):
        assert merge_intervals_ms([(20.0, 30.0), (0.0, 10.0)]) == 20.0


class TestEnableDisable:
    def test_disabled_by_default(self):
        assert not is_enabled()

    def test_enable_installs_sink(self):
        enable_flow_tracing(lambda s: None)
        assert is_enabled()

    def test_kill_switch_blocks_enable(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_FLOW_TRACE", "0")
        enable_flow_tracing(lambda s: None)
        assert not is_enabled()

    @pytest.mark.parametrize("value", ["false", "off", "0", " 0 ", "FALSE"])
    def test_kill_switch_values(self, monkeypatch, value):
        monkeypatch.setenv("RUNLAYER_FLOW_TRACE", value)
        enable_flow_tracing(lambda s: None)
        assert not is_enabled()

    def test_kill_switch_truthy_value_allows_enable(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_FLOW_TRACE", "1")
        enable_flow_tracing(lambda s: None)
        assert is_enabled()

    def test_kill_switch_is_request_scoped_for_daemon(self):
        summaries: list[dict] = []
        enable_flow_tracing(summaries.append)

        with hook_io.scoped(hook_io.HookIO(env={"RUNLAYER_FLOW_TRACE": "0"})):
            assert not is_enabled()
            with flow("cli.hook_event"):
                pass

        assert is_enabled()
        assert summaries == []


class TestNoSinkNoOp:
    def test_flow_without_sink_sets_no_contextvar(self):
        with flow("cli.call_tool") as trace:
            assert isinstance(trace, FlowTrace)
            assert current_flow() is None
            assert step("pre", kind="http") is _NULL_STEP

    def test_step_without_flow_is_null(self, sink):
        assert step("pre", kind="http") is _NULL_STEP
        assert sink == []

    def test_mark_error_without_flow_is_noop(self):
        mark_error("ValueError")  # must not raise


class TestStartupMs:
    def test_set_startup_ms_emits_in_summary(self, sink):
        with flow("cli.hook_pre_tool"):
            flow_trace.set_startup_ms(12.3456)
        assert sink[0]["startup_ms"] == 12.346

    def test_summary_omits_startup_when_unset(self, sink):
        with flow("cli.hook_pre_tool"):
            pass
        assert "startup_ms" not in sink[0]

    def test_negative_startup_is_dropped(self, sink):
        with flow("cli.hook_pre_tool"):
            flow_trace.set_startup_ms(-1.0)
        assert "startup_ms" not in sink[0]

    def test_set_startup_ms_without_flow_is_noop(self):
        flow_trace.set_startup_ms(5.0)  # must not raise


class TestFlowEmission:
    def test_basic_flow_emits_summary(self, sink):
        with flow("cli.call_tool"):
            with step("pre", kind="http"):
                pass
        assert len(sink) == 1
        summary = sink[0]
        assert summary["operation"] == "cli.call_tool"
        assert summary["status"] == "ok"
        assert summary["error_type"] is None
        assert summary["duration_ms"] >= 0
        assert summary["blocked_ms"] >= 0
        assert summary["steps_truncated"] is False
        assert isinstance(summary["ts"], int)
        (s,) = summary["steps"]
        assert s["name"] == "pre"
        assert s["kind"] == "http"
        assert s["status"] == "ok"
        assert s["parent"] is None
        # No payload size supplied: the key is omitted, not null.
        assert "payload_bytes" not in s

    def test_step_payload_bytes_lands_in_summary(self, sink):
        with flow("cli.hook_pre_tool"):
            with step("tool_pre", kind="http", payload_bytes=2048):
                pass
            with step("device_context", kind="local"):
                pass
        (summary,) = sink
        by_name = {s["name"]: s for s in summary["steps"]}
        assert by_name["tool_pre"]["payload_bytes"] == 2048
        assert "payload_bytes" not in by_name["device_context"]

    def test_exception_marks_flow_error(self, sink):
        with pytest.raises(ValueError):
            with flow("cli.call_tool"):
                raise ValueError("boom")
        assert sink[0]["status"] == "error"
        assert sink[0]["error_type"] == "ValueError"

    def test_mark_error_records_in_band_error(self, sink):
        with flow("cli.call_tool"):
            mark_error("ConnectError")
        assert sink[0]["status"] == "error"
        assert sink[0]["error_type"] == "ConnectError"

    def test_mark_error_first_type_wins(self, sink):
        with flow("cli.call_tool"):
            mark_error("First")
            mark_error("Second")
        assert sink[0]["error_type"] == "First"

    def test_mark_error_override_replaces_provisional_type(self, sink):
        # Terminal outcomes (fail-closed deny before process exit) must be
        # able to supersede a provisional mark from earlier in the flow.
        with flow("cli.call_tool"):
            mark_error("Provisional")
            mark_error("Terminal", override=True)
        assert sink[0]["error_type"] == "Terminal"

    def test_mark_error_override_without_type_keeps_existing(self, sink):
        with flow("cli.call_tool"):
            mark_error("First")
            mark_error(override=True)
        assert sink[0]["error_type"] == "First"

    def test_session_id_records_in_summary(self, sink):
        with flow("cli.call_tool"):
            flow_trace.set_session_id("sess-123")
        assert sink[0]["session_id"] == "sess-123"

    def test_server_id_stamped_on_every_summary(self, sink):
        flow_trace.set_server_id("12345678-1234-5678-1234-567812345678")
        with flow("cli.call_tool"):
            pass
        with flow("cli.list_tools"):
            pass
        assert sink[0]["server_id"] == "12345678-1234-5678-1234-567812345678"
        assert sink[1]["server_id"] == "12345678-1234-5678-1234-567812345678"

    def test_server_id_omitted_when_unset(self, sink):
        with flow("cli.hook_event"):
            pass
        assert "server_id" not in sink[0]

    @pytest.mark.parametrize(
        "raw",
        [
            "12345678123456781234567812345678",  # 32-hex, no hyphens
            "{12345678-1234-5678-1234-567812345678}",  # braces
            "urn:uuid:12345678-1234-5678-1234-567812345678",  # URN
            "12345678-1234-5678-1234-567812345678".upper(),  # uppercase
        ],
    )
    def test_server_id_canonicalized_to_hyphenated_uuid(self, sink, raw):
        """runlayer run accepts any uuid.UUID-parseable target verbatim, but
        backend ingest only keeps hyphenated canonical UUIDs."""
        flow_trace.set_server_id(raw)
        with flow("cli.call_tool"):
            pass
        assert sink[0]["server_id"] == "12345678-1234-5678-1234-567812345678"

    def test_non_uuid_server_id_kept_verbatim(self, sink):
        flow_trace.set_server_id("not-a-uuid")
        with flow("cli.call_tool"):
            pass
        assert sink[0]["server_id"] == "not-a-uuid"

    def test_cancelled_error_recorded_and_reraised(self, sink):
        """asyncio.CancelledError is BaseException — the plain Exception
        branch never sees it, so cancellation needs its own record path.
        It must always re-raise (never swallow cancellation)."""
        import asyncio

        from runlayer_cli.error_classification import classify_exception

        flow_trace.set_error_classifier(classify_exception)
        with pytest.raises(asyncio.CancelledError):
            with flow("cli.call_tool"):
                raise asyncio.CancelledError()
        assert sink[0]["status"] == "error"
        assert sink[0]["error_type"] == "CancelledError"
        assert sink[0]["error_category"] == "cancelled"

    def test_classifier_sets_error_category_and_status(self, sink):
        flow_trace.set_error_classifier(lambda exc: ("http_403", 403))
        with pytest.raises(RuntimeError):
            with flow("cli.list_tools"):
                raise RuntimeError("boom")
        assert sink[0]["status"] == "error"
        assert sink[0]["error_category"] == "http_403"
        assert sink[0]["error_http_status"] == 403

    def test_error_category_omitted_without_classifier(self, sink):
        with pytest.raises(RuntimeError):
            with flow("cli.list_tools"):
                raise RuntimeError("boom")
        assert "error_category" not in sink[0]
        assert "error_http_status" not in sink[0]

    def test_error_category_omitted_on_ok_flow(self, sink):
        flow_trace.set_error_classifier(lambda exc: ("other", None))
        with flow("cli.call_tool"):
            pass
        assert "error_category" not in sink[0]
        assert "error_http_status" not in sink[0]

    def test_broken_classifier_never_raises(self, sink):
        def broken(exc: BaseException) -> tuple[str | None, int | None]:
            raise RuntimeError("classifier bug")

        flow_trace.set_error_classifier(broken)
        with pytest.raises(ValueError):
            with flow("cli.call_tool"):
                raise ValueError("boom")
        assert sink[0]["status"] == "error"
        assert "error_category" not in sink[0]

    def test_mark_error_category_first_wins(self, sink):
        with flow("cli.call_tool"):
            mark_error("ConnectError", category="connect", http_status=None)
            mark_error("Other", category="timeout", http_status=504)
        assert sink[0]["error_category"] == "connect"
        # First mark carried no status, so the later one may still fill it in.
        assert sink[0]["error_http_status"] == 504

    def test_mark_error_category_beats_classifier(self, sink):
        flow_trace.set_error_classifier(lambda exc: ("other", None))
        with pytest.raises(ValueError):
            with flow("cli.call_tool"):
                mark_error("ConnectError", category="connect")
                raise ValueError("boom")
        assert sink[0]["error_category"] == "connect"

    def test_step_error_status_and_propagation(self, sink):
        with pytest.raises(RuntimeError):
            with flow("cli.call_tool"):
                with step("upstream", kind="remote"):
                    raise RuntimeError("upstream died")
        (s,) = sink[0]["steps"]
        assert s["status"] == "error"
        assert sink[0]["status"] == "error"
        assert sink[0]["error_type"] == "RuntimeError"

    def test_reentrant_flow_single_emit(self, sink):
        with flow("cli.list_tools") as outer:
            with flow("cli.sync_capabilities") as inner:
                assert inner is outer
                with step("introspect", kind="remote"):
                    pass
        assert len(sink) == 1
        assert sink[0]["operation"] == "cli.list_tools"
        assert [s["name"] for s in sink[0]["steps"]] == ["introspect"]

    def test_context_cleared_after_flow(self, sink):
        with flow("cli.call_tool"):
            assert current_flow() is not None
        assert current_flow() is None

    def test_parent_child_nesting(self, sink):
        with flow("cli.call_tool"):
            with step("post", kind="http"):
                with step("policy_check", kind="cpu"):
                    pass
        steps = {s["name"]: s for s in sink[0]["steps"]}
        assert steps["post"]["parent"] is None
        assert steps["policy_check"]["parent"] == steps["post"]["id"]

    def test_blocked_ms_only_counts_blocking_kinds(self, sink):
        trace_steps = []
        with flow("cli.call_tool") as trace:
            trace_steps = trace.steps
            with step("policy_check", kind="cpu"):
                pass
        assert all(not s.blocking for s in trace_steps)
        assert sink[0]["blocked_ms"] == 0.0

    def test_blocking_override(self, sink):
        with flow("cli.hook_event") as trace:
            with step("credentials", kind="local", blocking=True):
                pass
            assert trace.steps[0].blocking is True
        assert sink[0]["blocked_ms"] > 0.0

    def test_steps_truncated_at_cap(self, sink):
        with flow("cli.call_tool"):
            for _ in range(MAX_STEPS_PER_FLOW + 5):
                with step("pre", kind="http"):
                    pass
        assert len(sink[0]["steps"]) == MAX_STEPS_PER_FLOW
        assert sink[0]["steps_truncated"] is True

    def test_build_summary_golden_wire_shape(self, monkeypatch):
        monkeypatch.setattr("runlayer_cli.flow_summary.time.time", lambda: 1234567890)
        trace = FlowTrace(
            operation="cli.call_tool",
            started_perf=0.0,
            session_id="sess-123",
            error_type="RuntimeError",
        )
        steps = [
            StepRecord(
                id=0,
                parent_id=None,
                name="pre",
                kind="http",
                blocking=True,
                start_offset_ms=0.1114,
                duration_ms=10.5555,
                status="ok",
                error_type=None,
            ),
            StepRecord(
                id=1,
                parent_id=0,
                name="upstream",
                kind="remote",
                blocking=True,
                start_offset_ms=5.2222,
                duration_ms=10.1111,
                status="error",
                error_type="RuntimeError",
            ),
        ]
        for step_id in range(2, MAX_STEPS_PER_FLOW + 2):
            steps.append(
                StepRecord(
                    id=step_id,
                    parent_id=None,
                    name="post",
                    kind="cpu",
                    blocking=False,
                    start_offset_ms=float(step_id + 20),
                    duration_ms=1.2345,
                    status="ok",
                    error_type=None,
                )
            )

        summary = build_summary(
            trace,
            status="error",
            steps=steps,
            wall_ms=42.9876,
        )
        expected_steps = [
            {
                "id": 0,
                "parent": None,
                "name": "pre",
                "kind": "http",
                "status": "ok",
                "start_offset_ms": 0.111,
                "duration_ms": 10.556,
            },
            {
                "id": 1,
                "parent": 0,
                "name": "upstream",
                "kind": "remote",
                "status": "error",
                "start_offset_ms": 5.222,
                "duration_ms": 10.111,
            },
        ] + [
            {
                "id": step_id,
                "parent": None,
                "name": "post",
                "kind": "cpu",
                "status": "ok",
                "start_offset_ms": float(step_id + 20),
                "duration_ms": 1.234,
            }
            for step_id in range(2, MAX_STEPS_PER_FLOW)
        ]
        assert summary == {
            "operation": "cli.call_tool",
            "session_id": "sess-123",
            "status": "error",
            "error_type": "RuntimeError",
            "duration_ms": 42.988,
            "blocked_ms": 15.222,
            "ts": 1234567890,
            "steps": expected_steps,
            "steps_truncated": True,
        }

    def test_sink_exception_contained(self):
        def broken_sink(summary):
            raise RuntimeError("sink broke")

        enable_flow_tracing(broken_sink)
        with flow("cli.call_tool"):  # must not raise
            with step("pre", kind="http"):
                pass

    def test_system_exit_emits_ok(self, sink):
        # Hook handlers exit via sys.exit(0); SystemExit is not an Exception,
        # so the flow unwinds and emits with status="ok".
        with pytest.raises(SystemExit):
            with flow("cli.hook_pre_tool"):
                raise SystemExit(0)
        assert sink[0]["status"] == "ok"

    @pytest.mark.asyncio
    async def test_async_step(self, sink):
        with flow("cli.call_tool"):
            async with step("upstream", kind="remote"):
                pass
        (s,) = sink[0]["steps"]
        assert s["name"] == "upstream"

    def test_thread_concurrent_steps(self, sink):
        def worker(trace_ctx):
            ctx = trace_ctx.copy()
            ctx.run(
                lambda: step("pre", kind="http").__enter__().__exit__(None, None, None)
            )

        import contextvars as cv

        with flow("cli.call_tool"):
            ctx = cv.copy_context()
            threads = [threading.Thread(target=worker, args=(ctx,)) for _ in range(8)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        assert len(sink[0]["steps"]) == 8


class TestOperationDecorator:
    def test_sync_function(self, sink):
        @operation("cli.sync_capabilities")
        def do_sync():
            with step("upload", kind="http"):
                pass
            return 42

        assert do_sync() == 42
        assert sink[0]["operation"] == "cli.sync_capabilities"

    @pytest.mark.asyncio
    async def test_async_function(self, sink):
        @operation("cli.sync_capabilities")
        async def do_sync():
            async with step("introspect", kind="remote"):
                pass
            return "ok"

        assert await do_sync() == "ok"
        assert sink[0]["operation"] == "cli.sync_capabilities"

    @pytest.mark.asyncio
    async def test_async_nested_under_active_flow(self, sink):
        @operation("cli.sync_capabilities")
        async def do_sync():
            pass

        with flow("cli.list_tools"):
            await do_sync()
        assert len(sink) == 1
        assert sink[0]["operation"] == "cli.list_tools"


class TestResetFlow:
    def test_reset_clears_leaked_context(self, sink):
        token = flow_trace._flow_var.set(
            FlowTrace(operation="cli.call_tool", started_perf=0.0)
        )
        try:
            assert current_flow() is not None
            reset_flow()
            assert current_flow() is None
        finally:
            flow_trace._flow_var.reset(token)
            reset_flow()
