"""Flow tracing on the aiwatch hook path: spool wiring + stdout protocol safety."""

import io
import json
import sys

import httpx
import pytest

from runlayer_cli import flow_spool, flow_trace
from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook import hook_io
from runlayer_cli.hook import messages
from runlayer_cli.hook import relay
from runlayer_cli.hook.clients import Client
from runlayer_cli.mdm_config import AIWatchMode


@pytest.fixture(autouse=True)
def _clean_flow_state(monkeypatch, tmp_path):
    monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path)
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()
    yield tmp_path
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


def _run_hook(
    monkeypatch,
    payload: dict,
    *,
    enforcement: bool = False,
    mode: AIWatchMode | None = None,
    daemon_served: bool = False,
    daemon_fallback: bool = False,
) -> None:
    monkeypatch.setattr(hook_dispatch, "detect_client", lambda: Client.CLAUDE_CODE)
    if mode is None:
        mode = AIWatchMode.ENFORCE if enforcement else AIWatchMode.MONITOR
    monkeypatch.setattr(hook_dispatch, "_resolve_mode", lambda: mode)
    monkeypatch.setattr(hook_dispatch, "forward_event", lambda *a, **k: None)
    monkeypatch.setattr(hook_dispatch, "start_transcript_stream", lambda *a, **k: True)
    monkeypatch.delenv("HOOK_EVENT_NAME", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    with hook_io.scoped(
        hook_io.HookIO(
            daemon_served=daemon_served,
            daemon_fallback=daemon_fallback,
        )
    ):
        hook_dispatch.run_hook()


def _spooled_flows() -> list[dict]:
    envelope = flow_spool.spool_drain()
    return envelope["flows"] if envelope else []


class TestRunHookFlow:
    def test_event_hook_spools_one_flow(self, monkeypatch, capsys):
        _run_hook(
            monkeypatch,
            {"hook_event_name": "UserPromptSubmit", "session_id": "sess-123"},
        )
        flows = _spooled_flows()
        assert len(flows) == 1
        assert flows[0]["operation"] == "cli.hook_event"
        assert flows[0]["session_id"] == "sess-123"
        assert flows[0]["status"] == "ok"

    def test_stop_hook_operation(self, monkeypatch, capsys):
        monkeypatch.setattr(hook_dispatch, "forward_stop_event", lambda *a, **k: None)
        _run_hook(monkeypatch, {"hook_event_name": "Stop"})
        flows = _spooled_flows()
        assert flows[0]["operation"] == "cli.hook_stop"

    def test_daemon_served_flow_has_ipc_marker_and_inline_flow_does_not(
        self,
        monkeypatch,
        capsys,
    ):
        payload = {"hook_event_name": "UserPromptSubmit"}

        _run_hook(monkeypatch, payload)
        inline = _spooled_flows()[0]
        _run_hook(monkeypatch, payload, daemon_served=True)
        daemon = _spooled_flows()[0]

        assert "daemon_ipc" not in [step["name"] for step in inline["steps"]]
        assert [step["name"] for step in daemon["steps"]] == ["daemon_ipc"]
        assert daemon["steps"][0]["duration_ms"] == 0.0

    def test_daemon_fallback_flow_has_fallback_marker(self, monkeypatch, capsys):
        _run_hook(
            monkeypatch,
            {"hook_event_name": "UserPromptSubmit"},
            daemon_fallback=True,
        )

        flow = _spooled_flows()[0]
        assert [step["name"] for step in flow["steps"]] == ["daemon_fallback"]

    def test_policy_deny_spools_ok_flow_with_policy_step(self, monkeypatch, capsys):
        # Shell policy deny exits via sys.exit(0); the flow still emits with
        # status="ok" (a deny is an outcome, not a failure).
        payload = {
            "hook_event_name": "beforeShellExecution",
            "command": "cat .env",
        }
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, payload, enforcement=True)
        flows = _spooled_flows()
        assert len(flows) == 1
        assert flows[0]["operation"] == "cli.hook_event"
        assert flows[0]["status"] == "ok"
        assert [s["name"] for s in flows[0]["steps"]] == ["policy_check"]
        assert flows[0]["steps"][0]["status"] == "ok"

    def test_stdout_identical_with_tracing_on_and_off(self, monkeypatch, capsys):
        payload = {"hook_event_name": "UserPromptSubmit"}

        _run_hook(monkeypatch, payload)
        out_traced = capsys.readouterr().out
        assert _spooled_flows()  # tracing was on

        monkeypatch.setenv("RUNLAYER_FLOW_TRACE", "0")
        _run_hook(monkeypatch, payload)
        out_untraced = capsys.readouterr().out

        assert out_traced == out_untraced

    def test_kill_switch_writes_nothing(self, monkeypatch, capsys, tmp_path):
        monkeypatch.setenv("RUNLAYER_FLOW_TRACE", "0")
        _run_hook(monkeypatch, {"hook_event_name": "UserPromptSubmit"})
        assert _spooled_flows() == []
        assert not (tmp_path / "flow-spool.jsonl").exists()


class TestDenySpoolsErrorStatus:
    def test_relay_deny_spools_flow_with_error_status(self, monkeypatch, capsys):
        """A fail-closed deny must not spool status="ok" — the per-customer
        failure alert counts runlayer_flow_count_total{status!="ok"}."""
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *a, **k: (_ for _ in ()).throw(relay.RelayError(2, "network error")),
        )
        with pytest.raises(SystemExit):
            _run_hook(
                monkeypatch,
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                    "session_id": "sess-deny",
                },
                enforcement=True,
            )
        flows = _spooled_flows()
        assert flows, "deny did not spool a flow"
        assert flows[-1]["status"] == "error"
        assert flows[-1]["error_type"] == "HookInfraDeny"

    def test_relay_auth_failure_spools_auth_required(self, monkeypatch, capsys):
        """Missing credentials (RelayError exit_code=1) is user-actionable,
        not an infra outage — it gets its own error type."""
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *a, **k: (_ for _ in ()).throw(
                relay.RelayError(1, "no secret for host")
            ),
        )
        with pytest.raises(SystemExit):
            _run_hook(
                monkeypatch,
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "/tmp/x"},
                    "session_id": "sess-auth",
                },
                enforcement=True,
            )
        flows = _spooled_flows()
        assert flows, "auth deny did not spool a flow"
        assert flows[-1]["status"] == "error"
        assert flows[-1]["error_type"] == "HookAuthRequired"

    def test_protect_fail_open_spools_infra_fail_open(self, monkeypatch, capsys):
        """Protect mode allows through an unreachable API by design; the flow
        must record that as HookInfraFailOpen — countable fail-opens, not
        lumped in with fail-closed denies (and not status=ok)."""
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")
        monkeypatch.setattr(
            hook_dispatch,
            "lookup_mcp_server",
            lambda name, cwd: {"name": name, "command": "npx foo"},
        )
        monkeypatch.setattr(
            hook_dispatch,
            "enforce",
            lambda *a, **k: (_ for _ in ()).throw(relay.RelayError(2, "network error")),
        )
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *a, **k: '{"permission": "allow"}',
        )
        _run_hook(
            monkeypatch,
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "mcp__jira__search",
                "tool_input": {"query": "x"},
                "session_id": "sess-protect",
            },
            mode=AIWatchMode.PROTECT,
        )
        flows = _spooled_flows()
        assert flows, "protect fail-open did not spool a flow"
        assert flows[-1]["status"] == "error"
        assert flows[-1]["error_type"] == "HookInfraFailOpen"
        # The hook still allowed the call (fail-open is the Protect
        # contract): _run_hook returned without the deny path's SystemExit
        # and wrote no deny decision.
        assert "deny" not in capsys.readouterr().out

    def test_protect_fail_open_then_scanner_deny_spools_infra_deny(
        self, monkeypatch, capsys
    ):
        """Protect + deferred allow: an enforce failure provisionally marks
        HookInfraFailOpen, but the flow then continues into the scanner
        tool-pre. If that also fails, the action is DENIED — the terminal
        outcome must win over the provisional fail-open mark."""
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")
        monkeypatch.setattr(
            hook_dispatch,
            "lookup_mcp_server",
            lambda name, cwd: {"name": name, "command": "npx foo"},
        )
        monkeypatch.setattr(
            hook_dispatch,
            "enforce",
            lambda *a, **k: (_ for _ in ()).throw(relay.RelayError(2, "network error")),
        )
        monkeypatch.setattr(
            hook_dispatch,
            "check_tool_lifecycle",
            lambda *a, **k: (_ for _ in ()).throw(relay.RelayError(2, "network error")),
        )
        with pytest.raises(SystemExit):
            _run_hook(
                monkeypatch,
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "mcp__jira__search",
                    "tool_input": {"query": "x"},
                    "session_id": "sess-protect-deny",
                },
                mode=AIWatchMode.PROTECT,
            )
        flows = _spooled_flows()
        assert flows, "protect deny did not spool a flow"
        assert flows[-1]["status"] == "error"
        assert flows[-1]["error_type"] == "HookInfraDeny"


class TestEventPostAttachment:
    def test_event_payload_carries_spooled_flows(self):
        flow_trace.enable_flow_tracing(flow_spool.spool_append)
        flow_spool.spool_append({"operation": "cli.hook_event", "status": "ok"})
        payload = json.dumps(
            {"client": "claude_code", "event_name": "e", "payload": {}}
        )

        attached = json.loads(relay._maybe_attach_client_flows(payload, "event"))

        assert attached["client_flows"]["flows"][0]["operation"] == "cli.hook_event"
        # Spool drained: the next event POST carries nothing.
        again = json.loads(relay._maybe_attach_client_flows(payload, "event"))
        assert "client_flows" not in again

    def test_enforce_target_untouched(self):
        flow_trace.enable_flow_tracing(flow_spool.spool_append)
        flow_spool.spool_append({"operation": "cli.hook_event", "status": "ok"})
        payload = json.dumps({"hook_event_name": "beforeMCPExecution"})

        assert relay._maybe_attach_client_flows(payload, "enforce") == payload
        # Spool NOT drained by a non-event target.
        assert _spooled_flows() != []

    def test_disabled_tracing_untouched_and_not_drained(self):
        flow_spool.spool_append({"operation": "cli.hook_event", "status": "ok"})
        payload = json.dumps({"payload": {}})

        assert relay._maybe_attach_client_flows(payload, "event") == payload
        assert _spooled_flows() != []

    def test_non_dict_payload_untouched_and_not_drained(self):
        flow_trace.enable_flow_tracing(flow_spool.spool_append)
        flow_spool.spool_append({"operation": "cli.hook_event", "status": "ok"})

        assert relay._maybe_attach_client_flows("[1]", "event") == "[1]"
        assert _spooled_flows() != []


class TestPostFailureContext:
    """RelayError carries what failed so the deny message can say so (ENG-5197)."""

    def _post_raising(self, monkeypatch, exc):
        return self._post_raising_payload(monkeypatch, exc, '{"k": "v"}')

    def _post_raising_payload(self, monkeypatch, exc, payload):
        # Single-attempt classification contract; retry behavior is
        # TestPostRetries' concern (and backoff sleeps would slow this class).
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")

        class _Client:
            def __init__(self, *args, **kwargs):
                pass

            def post_target(self, target, payload, *, timeout=None):
                raise exc

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", payload, target="tool-pre")
        return ei.value

    def test_write_timeout_classified_as_upload_with_size_and_elapsed(
        self, monkeypatch
    ):
        err = self._post_raising(monkeypatch, httpx.WriteTimeout("w"))
        assert err.failure.kind == "upload_timeout"
        assert err.failure.payload_bytes == len('{"k": "v"}'.encode())
        assert err.failure.elapsed_s is not None and err.failure.elapsed_s >= 0

    def test_connect_error_classified(self, monkeypatch):
        assert (
            self._post_raising(monkeypatch, httpx.ConnectError("c")).failure.kind
            == "connect"
        )

    def test_connect_timeout_classified_as_connect_not_timeout(self, monkeypatch):
        assert (
            self._post_raising(monkeypatch, httpx.ConnectTimeout("t")).failure.kind
            == "connect"
        )

    def test_pool_timeout_classified_as_connect_not_timeout(self, monkeypatch):
        """Pool exhaustion means the request was never sent; rendering it as
        'the API did not respond' would misdirect toward API latency."""
        assert (
            self._post_raising(monkeypatch, httpx.PoolTimeout("p")).failure.kind
            == "connect"
        )

    def test_write_error_classified_as_upload_failed(self, monkeypatch):
        assert (
            self._post_raising(monkeypatch, httpx.WriteError("reset")).failure.kind
            == "upload_failed"
        )

    def test_read_timeout_classified(self, monkeypatch):
        assert (
            self._post_raising(monkeypatch, httpx.ReadTimeout("r")).failure.kind
            == "timeout"
        )

    def test_unknown_exception_stays_unclassified(self, monkeypatch):
        err = self._post_raising(monkeypatch, RuntimeError("boom"))
        assert err.failure.kind is None
        # Size is not encoded for kinds that never render it.
        assert err.failure.payload_bytes is None

    def test_encode_failure_still_raises_relay_error_fail_closed(self, monkeypatch):
        """If sizing the body fails (e.g. MemoryError on a multi-MB payload),
        the deny path must still raise RelayError — size is garnish, fail-
        closed is the contract (Bugbot finding on #8958)."""

        class _BoomStr(str):
            def encode(self, *args, **kwargs):
                raise MemoryError("no room to copy the body")

        err = self._post_raising_payload(
            monkeypatch, httpx.WriteTimeout("w"), _BoomStr('{"k": "v"}')
        )
        assert err.failure.kind == "upload_timeout"
        assert err.failure.payload_bytes is None

    def test_non_2xx_carries_http_kind_and_status(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")

        class _Resp:
            text = "server error"
            status_code = 503
            is_success = False

        class _Client:
            def __init__(self, *args, **kwargs):
                pass

            def post_target(self, target, payload, *, timeout=None):
                return _Resp()

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")
        assert ei.value.failure.kind == "http"
        assert ei.value.failure.status_code == 503


class TestPostPayloadBytes:
    def test_post_records_wire_size_of_posted_body(self, monkeypatch):
        """The recorded size is the UTF-8 length of the body actually POSTed
        (after device/time/flow attachment), not the caller's input."""
        summaries: list[dict] = []
        flow_trace.enable_flow_tracing(summaries.append)
        posted: dict[str, str] = {}

        class _Resp:
            text = "{}"
            status_code = 200
            is_success = True

        class _Client:
            def __init__(self, *args, **kwargs):
                pass

            def post_target(self, target, payload, *, timeout=None):
                posted["payload"] = payload
                return _Resp()

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        # Stub the payload mutators for hermeticity (no real device metadata).
        # The device stub GROWS the body so a regression that measures the
        # caller's input instead of the mutated body fails the equality below.
        marker = json.dumps({"device": {"hostname": "test-host"}})
        monkeypatch.setattr(
            relay, "_maybe_attach_device", lambda p: p[:-1] + "," + marker[1:]
        )
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        # Multibyte content so a char count would differ from the byte count.
        body = json.dumps({"payload": {"text": "é" * 32}}, ensure_ascii=False)

        with flow_trace.flow("cli.hook_pre_tool"):
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        (summary,) = summaries
        step = next(s for s in summary["steps"] if s["name"] == "tool_pre")
        assert step["payload_bytes"] == len(posted["payload"].encode("utf-8"))
        # The posted body is what was measured — not the caller's input.
        assert step["payload_bytes"] != len(body.encode("utf-8"))
        # Multibyte guard: byte length must exceed char length, proving the
        # recorded value is a wire size, not a character count.
        assert step["payload_bytes"] > len(posted["payload"])

    def test_gzip_payload_bytes_records_compressed_wire_size(self, monkeypatch):
        """With gzip active, the recorded size is the compressed body actually
        sent, not the uncompressed input (ENG-5113)."""
        import gzip

        summaries: list[dict] = []
        flow_trace.enable_flow_tracing(summaries.append)
        posted: dict = {}

        class _Resp:
            text = "{}"
            status_code = 200
            is_success = True

        class _Client:
            def __init__(self, *args, **kwargs):
                posted["headers"] = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                posted["payload"] = payload
                return _Resp()

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {"gzip_hooks": True})
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        with flow_trace.flow("cli.hook_pre_tool"):
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert isinstance(posted["payload"], bytes)
        assert posted["headers"]["Content-Encoding"] == "gzip"
        assert gzip.decompress(posted["payload"]).decode("utf-8") == body

        (summary,) = summaries
        step = next(s for s in summary["steps"] if s["name"] == "tool_pre")
        # Telemetry records the WIRE size: the compressed body, not the input.
        assert step["payload_bytes"] == len(posted["payload"])
        assert step["payload_bytes"] < len(body.encode("utf-8"))

    def test_gzip_kill_switch_env_wins_over_managed_gate(self, monkeypatch):
        posted: dict = {}

        class _Resp:
            text = "{}"
            status_code = 200
            is_success = True

        class _Client:
            def __init__(self, *args, **kwargs):
                posted["headers"] = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                posted["payload"] = payload
                return _Resp()

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {"gzip_hooks": True})
        monkeypatch.setenv("RUNLAYER_HOOK_GZIP", "0")
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert posted["payload"] == body
        assert "Content-Encoding" not in posted["headers"]

    def test_gzip_gate_default_off_sends_identity_encoding(self, monkeypatch):
        """Without the managed GzipHooks opt-in, even oversized bodies go out
        uncompressed — older backends can't parse gzip they didn't opt into."""
        posted: dict = {}

        class _Resp:
            text = "{}"
            status_code = 200
            is_success = True

        class _Client:
            def __init__(self, *args, **kwargs):
                posted["headers"] = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                posted["payload"] = payload
                return _Resp()

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {})
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert posted["payload"] == body
        assert "Content-Encoding" not in posted["headers"]

    def test_gzip_encode_failure_raises_relay_error_fail_closed(self, monkeypatch):
        """A MemoryError from the UTF-8 copy or gzip of a multi-MB body must
        surface as RelayError: dispatch only converts RelayError into the
        explicit deny, so anything else crashes the hook fail-open."""
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {"gzip_hooks": True})
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)

        def _boom(payload, *, compress=False):
            raise MemoryError("no room to copy the body")

        monkeypatch.setattr(relay, "encode_wire_body", _boom)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="enforce")

        assert ei.value.exit_code == 2
        assert ei.value.failure is not None and ei.value.failure.kind is None

    def test_gzip_kill_switch_survives_deferred_worker_thread(self, monkeypatch):
        """The deferred send runs on the daemon queue worker thread, outside the
        request-scoped ``hook_io`` env. The gzip kill switch must be captured at
        enqueue time (on the request thread) so it still wins there, even though
        a send-time ``hook_io.getenv`` re-read on the worker thread cannot see
        the client's ``RUNLAYER_HOOK_GZIP=0`` (ENG-5113)."""
        import threading

        posted: dict = {}

        class _Resp:
            text = "{}"
            status_code = 200
            is_success = True

        class _Client:
            def __init__(self, *args, **kwargs):
                posted["headers"] = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                posted["payload"] = payload
                return _Resp()

        queued: list = []
        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {"gzip_hooks": True})
        # Daemon process env lacks the kill switch: it only reaches the request
        # thread via the client-forwarded ``hook_io`` env.
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)
        monkeypatch.setattr(
            relay, "_deferred_event_sender", lambda send: queued.append(send) or True
        )
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://example.invalid", "sk"),
        )

        # Body must clear GZIP_MIN_PAYLOAD_BYTES (16 KiB) so gzip WOULD fire if
        # the kill switch were dropped — otherwise the small-payload short
        # circuit hides the bug.
        big_payload = {"tool_name": "Bash", "transcript": "x" * (32 * 1024)}

        # Request thread: kill switch present in the request-scoped env. This
        # captures the send closure without hitting the wire.
        with hook_io.scoped(hook_io.HookIO(env={"RUNLAYER_HOOK_GZIP": "0"})):
            relay.forward_event("claude_code", "PostToolUse", big_payload)

        assert len(queued) == 1
        # Run the queued send on a worker thread, outside the request scope —
        # exactly how ``DeferredEventQueue`` drains it. The ContextVar does not
        # propagate, so a send-time re-read would miss the kill switch.
        worker = threading.Thread(target=queued[0])
        worker.start()
        worker.join()

        assert "Content-Encoding" not in posted["headers"]
        assert isinstance(posted["payload"], str)

    def test_no_flow_skips_size_computation(self, monkeypatch):
        """Outside a flow (or with tracing killed) the hot path must not pay
        the O(n) encode: _post passes payload_bytes=None through."""
        captured: dict = {}
        real_step = flow_trace.step

        def _capturing_step(name, *, kind="local", blocking=None, payload_bytes=None):
            captured["payload_bytes"] = payload_bytes
            return real_step(name, kind=kind, blocking=blocking)

        class _Resp:
            text = "{}"
            status_code = 200
            is_success = True

        class _Client:
            def __init__(self, *args, **kwargs):
                pass

            def post_target(self, target, payload, *, timeout=None):
                return _Resp()

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay.flow_trace, "step", _capturing_step)

        relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert captured["payload_bytes"] is None


class _ScriptedResp:
    def __init__(self, status_code: int, text: str = "{}", headers: dict | None = None):
        self.status_code = status_code
        self.text = text
        self.is_success = 200 <= status_code < 300
        self.headers = headers or {}


class TestPostRetries:
    """Retry with a split timeout budget on enforcement/tool POSTs (ENG-5112)."""

    def _wire_client(self, monkeypatch, outcomes) -> list[dict]:
        """Install a HookAPIClient stub that replays `outcomes` (exceptions or
        responses; the last one repeats) and records each attempt."""
        calls: list[dict] = []

        class _Client:
            def __init__(self, host, *, headers, http_client_factory=None):
                self._headers = dict(headers)

            def post_target(self, target, payload, *, timeout=None):
                calls.append({"timeout": timeout, "headers": dict(self._headers)})
                outcome = outcomes[min(len(calls) - 1, len(outcomes) - 1)]
                if isinstance(outcome, Exception):
                    raise outcome
                return outcome

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {})
        return calls

    def _no_sleep(self, monkeypatch) -> list[float]:
        slept: list[float] = []
        monkeypatch.setattr(relay.time, "sleep", slept.append)
        return slept

    def test_transient_503_then_200_recovers(self, monkeypatch):
        calls = self._wire_client(
            monkeypatch, [_ScriptedResp(503), _ScriptedResp(200, '{"ok": true}')]
        )
        self._no_sleep(monkeypatch)

        text = relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert text == '{"ok": true}'
        assert len(calls) == 2

    def test_connection_reset_then_200_recovers(self, monkeypatch):
        calls = self._wire_client(
            monkeypatch, [httpx.ReadError("connection reset"), _ScriptedResp(200)]
        )
        self._no_sleep(monkeypatch)

        relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 2

    def test_permanent_failure_exhausts_attempts_with_backoff(self, monkeypatch):
        calls = self._wire_client(monkeypatch, [httpx.ConnectError("refused")])
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert ei.value.failure.kind == "connect"
        assert ei.value.failure.attempts == 3
        assert len(calls) == 3
        # ~0.2s then ~1s, jittered.
        assert len(slept) == 2
        assert 0.15 <= slept[0] <= 0.25
        assert 0.75 <= slept[1] <= 1.25

    def test_429_with_retry_after_within_budget_retries(self, monkeypatch):
        calls = self._wire_client(
            monkeypatch,
            [
                _ScriptedResp(429, "throttled", headers={"Retry-After": "1"}),
                _ScriptedResp(200, '{"ok": true}'),
            ],
        )
        slept = self._no_sleep(monkeypatch)

        text = relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert text == '{"ok": true}'
        assert len(calls) == 2
        # Server-scheduled sleep, not the default jittered backoff.
        assert slept == [1.0]

    def test_429_without_retry_after_is_terminal(self, monkeypatch):
        calls = self._wire_client(monkeypatch, [_ScriptedResp(429, "throttled")])
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.kind == "http"
        assert ei.value.failure.status_code == 429
        assert ei.value.failure.attempts == 1

    def test_429_with_retry_after_beyond_budget_is_terminal(self, monkeypatch):
        """Sleeping 60s would bust the 28s wall; deny now instead of later."""
        calls = self._wire_client(
            monkeypatch,
            [_ScriptedResp(429, "throttled", headers={"Retry-After": "60"})],
        )
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.attempts == 1

    def test_429_with_unparseable_retry_after_is_terminal(self, monkeypatch):
        calls = self._wire_client(
            monkeypatch,
            [
                _ScriptedResp(
                    429,
                    "throttled",
                    headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"},
                )
            ],
        )
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError):
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert slept == []

    @pytest.mark.parametrize("raw", ["nan", "inf", "-inf"])
    def test_429_with_non_finite_retry_after_is_terminal(self, monkeypatch, raw):
        """float() parses nan/inf, and NaN slips past every comparison guard
        (IEEE 754) into time.sleep(nan) -> ValueError; treat both as
        unparseable so the 429 stays terminal with an http failure kind."""
        calls = self._wire_client(
            monkeypatch,
            [_ScriptedResp(429, "throttled", headers={"Retry-After": raw})],
        )
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.kind == "http"
        assert ei.value.failure.status_code == 429

    def test_400_is_never_retried(self, monkeypatch):
        calls = self._wire_client(monkeypatch, [_ScriptedResp(400, "bad request")])
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.attempts == 1

    def test_kill_switch_disables_retries_and_keeps_wire_behavior(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")
        calls = self._wire_client(monkeypatch, [httpx.ConnectError("refused")])
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.attempts == 1
        # Pre-retry wire behavior: the target's own timeout, not a split one.
        assert calls[0]["timeout"] is None

    def test_event_target_gets_no_retries(self, monkeypatch):
        calls = self._wire_client(monkeypatch, [httpx.ConnectError("refused")])
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError):
            relay._post("https://example.invalid", "sk", "{}", target="event")

        assert len(calls) == 1
        assert slept == []
        assert calls[0]["timeout"] is None

    def test_first_attempt_gets_full_remaining_budget(self, monkeypatch):
        """Pin the ENG-5112 budget redesign: attempt 1's read/write timeout is
        the full remaining wall budget (≥24s — slow uploads that succeed at
        10–25s today must not be starved by per-attempt splits), and the
        configured budget never exceeds the 28s wall cap (the CLI must give
        up before the tightest harness ceiling, Goose's 30s kill)."""
        calls = self._wire_client(monkeypatch, [_ScriptedResp(200)])
        self._no_sleep(monkeypatch)

        relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        t = calls[0]["timeout"]
        assert isinstance(t, httpx.Timeout)
        assert t.connect == 3.0
        assert t.pool == 3.0
        assert t.read is not None and t.read >= 24.0
        assert t.write == t.read
        # Total configured budget (connect + read/write) stays within the cap.
        assert t.connect + t.read <= 28.0
        assert relay._MAX_WALL_BUDGET_S <= 28.0

    def test_retry_attempt_gets_remaining_budget_not_a_fixed_split(self, monkeypatch):
        """Attempt 2 gets whatever is left of the wall budget at that moment,
        not an even share carved out up front."""
        clock = {"t": 0.0}
        timeouts: list = []

        class _Client:
            def __init__(self, host, *, headers, http_client_factory=None):
                pass

            def post_target(self, target, payload, *, timeout=None):
                timeouts.append(timeout)
                if len(timeouts) == 1:
                    clock["t"] += 10.0
                    raise httpx.ConnectError("refused")
                return _ScriptedResp(200)

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay.time, "monotonic", lambda: clock["t"])
        monkeypatch.setattr(
            relay.time,
            "sleep",
            lambda delay: clock.__setitem__("t", clock["t"] + delay),
        )
        # Pin jitter so the backoff is exactly the 0.2s base.
        monkeypatch.setattr(relay.random, "random", lambda: 0.5)

        relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        # Attempt 2 starts at t=10.2 (10s burned + 0.2s backoff); read/write
        # is the remaining wall budget minus connect: 28 - 10.2 - 3 = 14.8.
        second = timeouts[1]
        assert second.read == pytest.approx(28.0 - 10.2 - 3.0)
        assert second.write == second.read

    def test_idempotency_header_constant_per_invocation_and_fresh_across(
        self, monkeypatch
    ):
        # A connect failure (provably unsent) is tool-post's only retryable
        # class; it must reuse the same idempotency key on the retry.
        calls = self._wire_client(
            monkeypatch, [httpx.ConnectError("refused"), _ScriptedResp(200)]
        )
        self._no_sleep(monkeypatch)

        relay._post("https://example.invalid", "sk", "{}", target="tool-post")
        first_keys = [c["headers"]["x-runlayer-idempotency-key"] for c in calls[:2]]
        assert len(calls) == 2
        assert first_keys[0] == first_keys[1]

        calls.clear()
        relay._post("https://example.invalid", "sk", "{}", target="tool-post")
        second_key = calls[-1]["headers"]["x-runlayer-idempotency-key"]
        assert second_key != first_keys[0]

    def test_tool_pre_carries_idempotency_header_and_event_does_not(self, monkeypatch):
        calls = self._wire_client(monkeypatch, [_ScriptedResp(200)])

        relay._post("https://example.invalid", "sk", "{}", target="tool-pre")
        relay._post("https://example.invalid", "sk", "{}", target="event")

        assert "x-runlayer-idempotency-key" in calls[0]["headers"]
        assert "x-runlayer-idempotency-key" not in calls[1]["headers"]

    def test_enforce_carries_idempotency_header(self, monkeypatch):
        """enforce retries include the response-lost class, and /hooks/cursor
        emits audit-log/device events — the additive key lets backend dedupe
        cover a lost-response replay when it lands."""
        calls = self._wire_client(monkeypatch, [_ScriptedResp(200)])

        relay._post("https://example.invalid", "sk", "{}", target="enforce")

        assert "x-runlayer-idempotency-key" in calls[0]["headers"]

    def test_no_attempt_starts_with_under_two_seconds_of_budget(self, monkeypatch):
        """Each attempt burns 15s of the 28s wall budget; after the second
        there is no room for a third (starting it would overshoot the
        deadline)."""
        clock = {"t": 0.0}

        class _Client:
            def __init__(self, host, *, headers, http_client_factory=None):
                pass

            def post_target(self, target, payload, *, timeout=None):
                clock["t"] += 15.0
                raise httpx.ConnectError("refused")

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay.time, "monotonic", lambda: clock["t"])

        def _sleep(delay):
            clock["t"] += delay

        monkeypatch.setattr(relay.time, "sleep", _sleep)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert ei.value.failure.attempts == 2

    def test_deadline_checked_before_starting_an_attempt(self, monkeypatch):
        """Even when backoff overshoots (slow wakeup past the deadline), no
        attempt starts with under the 2s floor left — the failure already in
        hand is raised instead."""
        clock = {"t": 0.0}
        calls: list = []

        class _Client:
            def __init__(self, host, *, headers, http_client_factory=None):
                pass

            def post_target(self, target, payload, *, timeout=None):
                calls.append(timeout)
                clock["t"] += 5.0
                raise httpx.ConnectError("refused")

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay.time, "monotonic", lambda: clock["t"])
        # Sleep overshoots the whole remaining budget.
        monkeypatch.setattr(
            relay.time, "sleep", lambda _d: clock.__setitem__("t", clock["t"] + 25.0)
        )

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 1
        assert ei.value.failure.kind == "connect"
        assert ei.value.failure.attempts == 1

    def test_deadline_after_retryable_status_reports_latest_http_failure(
        self, monkeypatch
    ):
        """A stale transport error from attempt 1 must not mask attempt 2's
        HTTP failure: when the budget dies after a retryable 503 (slow backoff
        wakeup past the deadline), the terminal RelayError carries the 503,
        not the earlier connect error."""
        clock = {"t": 0.0}
        calls: list = []
        sleeps: list[float] = []

        class _Client:
            def __init__(self, host, *, headers, http_client_factory=None):
                pass

            def post_target(self, target, payload, *, timeout=None):
                calls.append(timeout)
                clock["t"] += 5.0
                if len(calls) == 1:
                    raise httpx.ConnectError("refused")
                return _ScriptedResp(503, "upstream unavailable")

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay.time, "monotonic", lambda: clock["t"])
        # Pin jitter so backoff arithmetic passes the pre-sleep budget check.
        monkeypatch.setattr(relay.random, "random", lambda: 0.5)

        def _sleep(delay):
            sleeps.append(delay)
            # First backoff (after the connect error) behaves; the second
            # (after the 503) overshoots the whole remaining budget, so the
            # top-of-loop deadline check decides the terminal failure.
            clock["t"] += delay if len(sleeps) == 1 else 25.0

        monkeypatch.setattr(relay.time, "sleep", _sleep)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 2
        assert ei.value.failure.kind == "http"
        assert ei.value.failure.status_code == 503
        assert ei.value.failure.attempts == 2
        assert ei.value.body == "upstream unavailable"

    def test_tool_post_read_timeout_is_terminal(self, monkeypatch):
        """A read timeout means the request may have arrived and been
        recorded; without backend idempotency-key dedupe a replay could
        double-apply the tool-post."""
        calls = self._wire_client(monkeypatch, [httpx.ReadTimeout("r")])
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-post")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.attempts == 1

    @pytest.mark.parametrize("status", [503, 429])
    def test_tool_post_transient_status_is_terminal(self, monkeypatch, status):
        """5xx/429 prove the request arrived — terminal for tool-post until
        the backend dedupes on the idempotency key."""
        calls = self._wire_client(
            monkeypatch, [_ScriptedResp(status, headers={"Retry-After": "1"})]
        )
        slept = self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-post")

        assert len(calls) == 1
        assert slept == []
        assert ei.value.failure.status_code == status

    @pytest.mark.parametrize(
        "exc",
        [
            httpx.ConnectError("refused"),
            httpx.ConnectTimeout("t"),
            httpx.PoolTimeout("p"),
            httpx.WriteError("reset"),
            httpx.WriteTimeout("w"),
        ],
        ids=lambda e: type(e).__name__,
    )
    def test_tool_post_provably_unsent_failures_still_retry(self, monkeypatch, exc):
        """Failures where the request never reached the backend stay safe to
        retry even for the non-idempotent tool-post target."""
        calls = self._wire_client(monkeypatch, [exc, _ScriptedResp(200)])
        self._no_sleep(monkeypatch)

        relay._post("https://example.invalid", "sk", "{}", target="tool-post")

        assert len(calls) == 2

    def test_tool_pre_read_timeout_still_retries(self, monkeypatch):
        """tool-pre keeps the broader retry set: a duplicate pre-check is
        harmless, so read timeouts remain retryable there."""
        calls = self._wire_client(
            monkeypatch, [httpx.ReadTimeout("r"), _ScriptedResp(200)]
        )
        self._no_sleep(monkeypatch)

        relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        assert len(calls) == 2

    def test_retry_failure_message_renders_attempts(self, monkeypatch):
        """End-to-end: the exhausted-retries FailureContext reaches the deny
        message as ', after N attempts'."""
        self._wire_client(monkeypatch, [httpx.ConnectError("refused")])
        self._no_sleep(monkeypatch)

        with pytest.raises(relay.RelayError) as ei:
            relay._post("https://example.invalid", "sk", "{}", target="tool-pre")

        _, agent = messages.tool_api_unreachable(failure=ei.value.failure)
        assert "Could not connect to the Runlayer API, after 3 attempts." in agent


class TestGzipBackendFallback:
    """A gzip-incapable backend must degrade to identity, not fail-closed.

    A GzipHooks flag flipped ahead of the backend upgrade (or against a
    dedicated tenant on an older release) previously turned every hook call
    into a fail-closed deny via HTTP 400/422 on the unparseable body.
    """

    def _client(self, monkeypatch, statuses: list[int]):
        """HookAPIClient stub answering each post with the next status."""
        calls: list[dict] = []

        class _Resp:
            def __init__(self, status: int):
                self.status_code = status
                self.is_success = status < 400
                self.text = "{}" if self.is_success else "rejected"

        class _Client:
            def __init__(self, *args, **kwargs):
                self._headers = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                calls.append({"payload": payload, "headers": self._headers})
                return _Resp(statuses[len(calls) - 1])

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {"gzip_hooks": True})
        monkeypatch.setattr(relay, "_compression_rejected_by_backend", False)
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)
        return calls

    def test_gzip_rejection_falls_back_to_identity_and_succeeds(self, monkeypatch):
        calls = self._client(monkeypatch, [422, 200])
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        out = relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert out == "{}"
        assert len(calls) == 2
        assert isinstance(calls[0]["payload"], bytes)  # first attempt compressed
        assert calls[0]["headers"]["Content-Encoding"] == "gzip"
        assert calls[1]["payload"] == body  # retry is the identity body
        assert "Content-Encoding" not in calls[1]["headers"]
        assert relay._compression_rejected_by_backend is True

    @pytest.mark.parametrize("status", [400, 415, 422])
    def test_every_reject_status_triggers_fallback(self, monkeypatch, status):
        calls = self._client(monkeypatch, [status, 200])
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        out = relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert out == "{}"
        assert len(calls) == 2

    def test_memo_skips_compression_on_subsequent_posts(self, monkeypatch):
        calls = self._client(monkeypatch, [200])
        monkeypatch.setattr(relay, "_compression_rejected_by_backend", True)
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 1  # no failed attempt paid
        assert calls[0]["payload"] == body
        assert "Content-Encoding" not in calls[0]["headers"]

    def test_genuinely_malformed_payload_still_raises_after_identity_retry(
        self, monkeypatch
    ):
        """Same status on the identity attempt: the fallback must not loop or
        mask a real 4xx."""
        calls = self._client(monkeypatch, [422, 422])
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        with pytest.raises(relay.RelayError) as exc_info:
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 2
        assert exc_info.value.failure.kind == "http"
        assert exc_info.value.failure.status_code == 422
        # gzip was never proven the cause: the daemon must not silently
        # disable compression for the rest of its life.
        assert relay._compression_rejected_by_backend is False

    def test_identity_post_4xx_never_triggers_fallback(self, monkeypatch):
        """An uncompressed post that 4xxs has nothing to fall back to."""
        calls = self._client(monkeypatch, [422])
        monkeypatch.setenv("RUNLAYER_HOOK_GZIP", "0")  # identity from the start
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        with pytest.raises(relay.RelayError):
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 1
        assert relay._compression_rejected_by_backend is False

    def test_exhausted_wall_budget_skips_fallback_and_denies(self, monkeypatch):
        """A compressed attempt that burned the wall budget (slow upload, late
        4xx) must NOT start a fresh-budget identity retry — that would blow
        past the ~30s harness hook ceiling and get the hook killed instead of
        a clean deny."""
        import time as _time

        calls = self._client(monkeypatch, [422, 200])
        t0 = _time.monotonic()
        # After the first attempt, the clock sits past the 28s wall budget.
        ticks = iter([t0, t0 + 29.0])
        monkeypatch.setattr(relay.time, "monotonic", lambda: next(ticks, t0 + 29.0))
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        with pytest.raises(relay.RelayError) as exc_info:
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 1  # no identity retry started
        assert exc_info.value.failure.status_code == 422
        assert relay._compression_rejected_by_backend is False

    def test_credential_401_never_triggers_fallback(self, monkeypatch):
        calls = self._client(monkeypatch, [401])
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        with pytest.raises(relay.RelayError):
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 1
        assert relay._compression_rejected_by_backend is False

    def test_small_identity_body_4xx_never_sets_memo(self, monkeypatch):
        """GzipHooks on but the body is under the compression threshold: the
        wire was identity, so a 4xx proves nothing about gzip support and
        must not disable compression for the process."""
        calls = self._client(monkeypatch, [422])
        body = json.dumps({"transcript": "small"})  # < 16KB: never compressed

        with pytest.raises(relay.RelayError):
            relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 1
        assert calls[0]["payload"] == body
        assert relay._compression_rejected_by_backend is False

    def test_legacy_cursor_200_validation_deny_falls_back_to_identity(
        self, monkeypatch
    ):
        """Pre-gzip cursor backends answer an unparseable body with HTTP 200
        + permission=deny (FailClosedRoute), not a 4xx."""
        legacy_deny = json.dumps(
            {
                "permission": "deny",
                "user_message": "Hook validation failed - MCP blocked for security",
            }
        )
        allow = json.dumps({"permission": "allow"})
        calls = self._client(monkeypatch, [200, 200])
        calls_bodies = [legacy_deny, allow]

        class _Resp:
            def __init__(self, text: str):
                self.status_code = 200
                self.is_success = True
                self.text = text

        class _Client:
            def __init__(self, *args, **kwargs):
                self._headers = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                calls.append({"payload": payload, "headers": self._headers})
                return _Resp(calls_bodies[len(calls) - 1])

        calls.clear()
        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        out = relay._post("https://example.invalid", "sk", body, target="enforce")

        assert out == allow
        assert len(calls) == 2
        assert isinstance(calls[0]["payload"], bytes)
        assert calls[1]["payload"] == body
        assert relay._compression_rejected_by_backend is True

    def test_persistent_validation_deny_returned_without_memo(self, monkeypatch):
        """The identity retry gets the same validation deny: a genuine
        client/backend mismatch, not a gzip problem — return it and keep
        compression enabled."""
        legacy_deny = json.dumps(
            {
                "permission": "deny",
                "user_message": "Hook validation failed - MCP blocked for security",
            }
        )
        calls = self._client(monkeypatch, [200, 200])

        class _Resp:
            status_code = 200
            is_success = True
            text = legacy_deny

        class _Client:
            def __init__(self, *args, **kwargs):
                self._headers = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                calls.append({"payload": payload, "headers": self._headers})
                return _Resp()

        calls.clear()
        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        out = relay._post("https://example.invalid", "sk", body, target="enforce")

        assert out == legacy_deny
        assert len(calls) == 2
        assert relay._compression_rejected_by_backend is False

    def test_ordinary_deny_never_triggers_identity_retry(self, monkeypatch):
        """A policy deny (no validation marker) on a compressed post is a real
        answer — no extra round trip."""
        policy_deny = json.dumps(
            {"permission": "deny", "user_message": "Blocked by security policy"}
        )
        calls = self._client(monkeypatch, [200])

        class _Resp:
            status_code = 200
            is_success = True
            text = policy_deny

        class _Client:
            def __init__(self, *args, **kwargs):
                self._headers = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                calls.append({"payload": payload, "headers": self._headers})
                return _Resp()

        calls.clear()
        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        out = relay._post("https://example.invalid", "sk", body, target="enforce")

        assert out == policy_deny
        assert len(calls) == 1
        assert relay._compression_rejected_by_backend is False


class TestWireCodecSelection:
    """relay._post sends the fastest codec the backend advertised; no advertisement means gzip, and rejection falls back the
    same way it does for gzip."""

    def _client(self, monkeypatch, statuses, managed):
        from runlayer_sdk import hook_transport

        calls: list[dict] = []

        class _Resp:
            def __init__(self, status: int):
                self.status_code = status
                self.is_success = status < 400
                self.text = "{}" if self.is_success else "rejected"

        class _Client:
            def __init__(self, *args, **kwargs):
                self._headers = kwargs.get("headers", {})

            def post_target(self, target, payload, *, timeout=None):
                calls.append({"payload": payload, "headers": self._headers})
                return _Resp(statuses[len(calls) - 1])

        monkeypatch.setattr(relay, "HookAPIClient", _Client)
        monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
        monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
        monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t: p)
        monkeypatch.setattr(relay, "read_managed_config", lambda: dict(managed))
        monkeypatch.setattr(relay, "_compression_rejected_by_backend", False)
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)
        # Hermetic zstd: the cli test env does not ship zstandard, and the
        # selection contract is what's under test, not the codec itself.
        monkeypatch.setattr(hook_transport, "_zstd_probed", True)
        monkeypatch.setattr(
            hook_transport, "_zstd_compress", lambda raw: b"ZSTDFAKE" + raw[:16]
        )
        return calls

    def test_advertised_zstd_is_sent_on_the_wire(self, monkeypatch):
        calls = self._client(
            monkeypatch,
            [200],
            {"gzip_hooks": True, "hook_wire_encodings": ("zstd", "gzip")},
        )
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert len(calls) == 1
        assert calls[0]["headers"]["Content-Encoding"] == "zstd"
        assert calls[0]["payload"].startswith(b"ZSTDFAKE")

    def test_no_advertisement_stays_on_gzip(self, monkeypatch):
        """Old backends never advertise: zstd availability alone must not
        change the wire."""
        calls = self._client(monkeypatch, [200], {"gzip_hooks": True})
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert calls[0]["headers"]["Content-Encoding"] == "gzip"

    def test_zstd_rejection_falls_back_to_identity(self, monkeypatch):
        """A backend that mis-advertises zstd degrades exactly like a
        gzip-incapable one: one identity retry, memo on success."""
        calls = self._client(
            monkeypatch,
            [415, 200],
            {"gzip_hooks": True, "hook_wire_encodings": ("zstd", "gzip")},
        )
        body = json.dumps({"transcript": "x" * (32 * 1024)})

        out = relay._post("https://example.invalid", "sk", body, target="tool-pre")

        assert out == "{}"
        assert len(calls) == 2
        assert calls[0]["headers"]["Content-Encoding"] == "zstd"
        assert calls[1]["payload"] == body
        assert "Content-Encoding" not in calls[1]["headers"]
        assert relay._compression_rejected_by_backend is True


class TestTranscriptStreamCompression:
    """The detached transcript poster compresses like relay._post: managed
    gate + advertised codecs captured at construction, rejection memo shared
    with relay (ENG-5844)."""

    def _poster(self, monkeypatch, statuses, *, managed):
        from runlayer_cli.hook import transcript_stream

        calls: list[dict] = []

        class _Resp:
            def __init__(self, status: int):
                self.status_code = status
                self.is_success = status < 400
                self.text = "{}"

        class _Client:
            def post(self, url, *, content=None, headers=None, timeout=None):
                calls.append({"payload": content, "headers": dict(headers or {})})
                return _Resp(statuses[min(len(calls) - 1, len(statuses) - 1)])

            def close(self):
                pass

        monkeypatch.setattr(transcript_stream, "http_client", lambda: _Client())
        monkeypatch.setattr(
            transcript_stream, "read_managed_config", lambda: dict(managed)
        )
        monkeypatch.setattr(relay, "read_managed_config", lambda: dict(managed))
        monkeypatch.setattr(relay, "_compression_rejected_by_backend", False)
        monkeypatch.delenv("RUNLAYER_HOOK_GZIP", raising=False)

        class _Config:
            default_host = "https://example.invalid"

            def get_secret_for_host(self, host):
                return None

        monkeypatch.setattr(transcript_stream, "load_config", lambda: _Config())
        poster = transcript_stream._HTTPEventPoster(debug=False)
        return poster, calls

    _MANAGED = {
        "host": "https://example.invalid",
        "org_api_key": "rl_org_secret",
        "gzip_hooks": True,
    }

    def test_large_event_posts_gzip_when_gate_on(self, monkeypatch):
        poster, calls = self._poster(monkeypatch, [200], managed=self._MANAGED)

        poster("claude_code", "transcript", {"text": "x" * (32 * 1024)})

        assert len(calls) == 1
        assert calls[0]["headers"].get("Content-Encoding") == "gzip"
        import gzip

        decoded = json.loads(gzip.decompress(calls[0]["payload"]))
        assert decoded["event_name"] == "transcript"

    def test_gate_off_posts_identity(self, monkeypatch):
        managed = {**self._MANAGED, "gzip_hooks": False}
        poster, calls = self._poster(monkeypatch, [200], managed=managed)

        poster("claude_code", "transcript", {"text": "x" * (32 * 1024)})

        assert "Content-Encoding" not in calls[0]["headers"]
        assert isinstance(calls[0]["payload"], str)

    def test_advertised_zstd_is_used(self, monkeypatch):
        from runlayer_sdk import hook_transport

        managed = {**self._MANAGED, "hook_wire_encodings": ("zstd", "gzip")}
        monkeypatch.setattr(hook_transport, "_zstd_probed", True)
        monkeypatch.setattr(
            hook_transport, "_zstd_compress", lambda raw: b"ZSTDFAKE" + raw[:16]
        )
        poster, calls = self._poster(monkeypatch, [200], managed=managed)

        poster("claude_code", "transcript", {"text": "x" * (32 * 1024)})

        assert calls[0]["headers"].get("Content-Encoding") == "zstd"

    def test_rejection_retries_identity_and_memos(self, monkeypatch):
        poster, calls = self._poster(monkeypatch, [415, 200], managed=self._MANAGED)

        poster("claude_code", "transcript", {"text": "x" * (32 * 1024)})

        assert len(calls) == 2
        assert calls[0]["headers"].get("Content-Encoding") == "gzip"
        assert "Content-Encoding" not in calls[1]["headers"]
        assert relay._compression_rejected_by_backend is True

        poster("claude_code", "transcript", {"text": "y" * (32 * 1024)})
        assert "Content-Encoding" not in calls[2]["headers"]  # memo respected

    def test_small_event_stays_identity(self, monkeypatch):
        poster, calls = self._poster(monkeypatch, [200], managed=self._MANAGED)

        poster("claude_code", "transcript", {"text": "small"})

        assert "Content-Encoding" not in calls[0]["headers"]
