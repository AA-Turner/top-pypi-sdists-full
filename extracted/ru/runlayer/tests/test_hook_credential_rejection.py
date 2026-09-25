"""Hook behaviour when the Runlayer API rejects this device's credentials.

Monitor: the admin has not turned enforcement on, so a revoked/rotated key must
never stop the editor — allow, record the rejection, tell the user once an
hour, and stop hammering the API for a few minutes. Enforce: fail-closed as
before, with a deny that names the device and who can fix it.
"""

from __future__ import annotations

import io
import json
import socket
import sys
import threading
import time
from pathlib import Path

import httpx
import pytest

from runlayer_cli import flow_spool, flow_trace
from runlayer_cli.hook import credential_state, dispatch as hook_dispatch, hook_io
from runlayer_cli.hook import messages, relay
from runlayer_cli.hook.clients import Client
from runlayer_cli.mdm_config import AIWatchMode

_HOST = "https://t.example"
_FP = credential_state.credential_fingerprint(_HOST, "revoked")
_MANAGED = {"host": _HOST, "org_api_key": "revoked", "device_name": "LAPTOP-42"}

_PRE_TOOL = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Edit",
    "tool_input": {"file_path": "/tmp/x"},
    "session_id": "sess-cred",
}
_MCP_PRE_TOOL = {
    "hook_event_name": "PreToolUse",
    "tool_name": "mcp__jira__search",
    "tool_input": {"query": "x"},
    "session_id": "sess-cred-mcp",
}
_CURSOR_MCP = {
    "hook_event_name": "beforeMCPExecution",
    "tool_name": "search",
    "tool_input": {"query": "x"},
    "conversation_id": "conv-cred",
    "url": "https://mcp.example/sse",
}


@pytest.fixture(autouse=True)
def _clean_flow_state(monkeypatch, tmp_path, isolated_credential_state):
    monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path)
    monkeypatch.setenv("RUNLAYER_HOOK_RETRIES", "0")
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()
    yield
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


@pytest.fixture
def state_dir(isolated_credential_state) -> Path:
    return isolated_credential_state / "state"


# Response shapes the relay must tell apart. Runlayer's error handlers answer
# the JSON error envelope with a request id (and, once the origin marker
# ships, X-Runlayer-Origin); an intermediary (WAF IP-allowlist block, ALB error
# page, proxy) answers the same status with an HTML page and neither header.
_RUNLAYER_HEADERS = {"X-Runlayer-Origin": "backend", "X-Request-ID": "req-0001"}
_LEGACY_RUNLAYER_HEADERS = {"X-Request-ID": "req-legacy"}
_RUNLAYER_BODY = '{"detail": "Invalid API key"}'
_WAF_HEADERS = {"server": "awselb/2.0", "content-type": "text/html"}
_WAF_BODY = "<html>\n<head><title>403 Forbidden</title></head>\n<body></body>\n</html>"


class _Resp:
    is_success = False

    def __init__(
        self, status_code: int, text: str = "", headers: dict[str, str] | None = None
    ) -> None:
        self.status_code = status_code
        self.text = text
        self.headers = httpx.Headers(headers or {})


def _install_api(
    monkeypatch,
    status_code: int,
    *,
    intermediary: bool = False,
    headers: dict[str, str] | None = None,
) -> list[str]:
    """Route every relay POST to a fake API answering ``status_code``; returns
    the list of targets posted so tests can count real calls. Runlayer-shaped
    by default; ``intermediary=True`` answers like a WAF/ALB block page;
    ``headers`` overrides the Runlayer headers (e.g. a backend without the
    origin marker)."""
    posted: list[str] = []
    text = _WAF_BODY if intermediary else _RUNLAYER_BODY
    resp_headers = _WAF_HEADERS if intermediary else (headers or _RUNLAYER_HEADERS)

    class _Client:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def post_target(self, target, payload, *, timeout=None):
            posted.append(target)
            return _Resp(status_code, text, resp_headers)

    monkeypatch.setattr(relay, "HookAPIClient", _Client)
    monkeypatch.setattr(relay, "_maybe_attach_device", lambda p: p)
    monkeypatch.setattr(relay, "_maybe_stamp_client_time", lambda p, t: p)
    monkeypatch.setattr(relay, "_maybe_attach_client_flows", lambda p, t, h: p)
    monkeypatch.setattr(relay, "_load_credentials_uncached", lambda: (_HOST, "revoked"))
    monkeypatch.setattr(relay, "read_managed_config", lambda: dict(_MANAGED))
    return posted


def _run_hook(
    monkeypatch,
    payload: dict,
    *,
    mode: AIWatchMode,
    client: Client = Client.CLAUDE_CODE,
) -> None:
    monkeypatch.setattr(hook_dispatch, "detect_client", lambda: client)
    monkeypatch.setattr(hook_dispatch, "should_noop_for_cursor", lambda c: False)
    monkeypatch.setattr(
        hook_dispatch, "resolve_cursor_before_mcp_payload", lambda payload: payload
    )
    monkeypatch.setattr(hook_dispatch, "_resolve_mode", lambda: mode)
    monkeypatch.setattr(hook_dispatch, "start_transcript_stream", lambda *a, **k: True)
    monkeypatch.setattr(
        hook_dispatch,
        "lookup_mcp_server",
        lambda name, cwd: {"name": name, "command": "npx foo"},
    )
    monkeypatch.delenv("HOOK_EVENT_NAME", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    with hook_io.scoped(hook_io.HookIO()):
        hook_dispatch.run_hook()


def _flows() -> list[dict]:
    envelope = flow_spool.spool_drain()
    return envelope["flows"] if envelope else []


def _state(state_dir: Path) -> dict | None:
    path = state_dir / "credential_rejected.json"
    return json.loads(path.read_text()) if path.exists() else None


def _step_names(flow: dict) -> list[str]:
    return [step["name"] for step in flow["steps"]]


def _assert_cached_allow_flow(flow: dict) -> None:
    """A cached allow is a healthy flow with the cohort marker, never a 401."""
    assert flow["status"] == "ok"
    assert "credential_rejected_cached" in _step_names(flow)
    assert flow.get("error_category") is None
    assert flow.get("error_type") is None


def _assert_seed_rejection_flow(flow: dict) -> None:
    """The flow whose relay call was actually answered 401."""
    assert flow["status"] == "error"
    assert flow["error_type"] == "HookCredentialRejectedMonitor"
    assert flow["error_category"] == "http_401"
    assert flow["error_http_status"] == 401
    assert "credential_rejected_cached" not in _step_names(flow)


def _deny_reason(out: str) -> str:
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


class TestMonitorAllows:
    def test_first_rejection_allows_and_records(self, monkeypatch, capsys, state_dir):
        posted = _install_api(monkeypatch, 401)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        assert capsys.readouterr().out == ""
        assert posted  # the first call really asked the API
        flow = _flows()[-1]
        assert flow["status"] == "error"
        assert flow["error_type"] == "HookCredentialRejectedMonitor"
        assert flow["error_category"] == "http_401"
        assert flow["error_http_status"] == 401
        assert _state(state_dir) == {
            "at": pytest.approx(time.time(), abs=5),
            "status": 401,
            "fingerprint": _FP,
        }

    def test_mcp_tool_first_rejection_allows(self, monkeypatch, capsys):
        _install_api(monkeypatch, 401)
        _run_hook(monkeypatch, _MCP_PRE_TOOL, mode=AIWatchMode.MONITOR)
        assert capsys.readouterr().out == ""
        assert _flows()[-1]["error_type"] == "HookCredentialRejectedMonitor"

    def test_negative_cache_skips_api_and_notifies_once_per_hour(
        self, monkeypatch, capsys
    ):
        posted = _install_api(monkeypatch, 401)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        first_calls = len(posted)
        assert first_calls >= 1

        # Second call inside the TTL: no API call, allow + one user notice.
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        out = capsys.readouterr().out
        assert len(posted) == first_calls
        assert json.loads(out) == {
            "systemMessage": messages.MONITOR_CREDENTIALS_REJECTED_NOTICE
        }
        _assert_cached_allow_flow(_flows()[-1])

        # Third call: still cached, but the notice is rate-limited to one/hour.
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        assert capsys.readouterr().out == ""
        assert len(posted) == first_calls

    def test_one_window_reports_exactly_one_failure(self, monkeypatch, capsys):
        """N hooks inside one TTL window: the seed flow is the only http_401
        error; the cached allows are ok flows carrying the marker."""
        posted = _install_api(monkeypatch, 401)
        hooks = 6
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        seed_calls = len(posted)
        for _ in range(hooks - 1):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
            capsys.readouterr()
        assert len(posted) == seed_calls, "cached allows must not call the API"
        flows = _flows()
        assert len(flows) == hooks
        seed, *cached = flows
        _assert_seed_rejection_flow(seed)
        for flow in cached:
            _assert_cached_allow_flow(flow)

    def test_expired_window_reports_one_more_failure(self, monkeypatch, capsys):
        posted = _install_api(monkeypatch, 401)
        now = 1_000_000.0
        monkeypatch.setattr(time, "time", lambda: now)
        for _ in range(3):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
            capsys.readouterr()
        calls_in_first_window = len(posted)

        monkeypatch.setattr(
            time, "time", lambda: now + credential_state.NEGATIVE_CACHE_TTL_S + 1
        )
        for _ in range(3):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
            capsys.readouterr()
        assert len(posted) > calls_in_first_window, "the lapsed TTL must re-ask"

        flows = _flows()
        assert [flow["status"] for flow in flows] == ["error", "ok", "ok"] * 2
        for flow in flows:
            if flow["status"] == "error":
                _assert_seed_rejection_flow(flow)
            else:
                _assert_cached_allow_flow(flow)

    def test_notice_repeats_after_an_hour(self, monkeypatch, capsys):
        _install_api(monkeypatch, 401)
        now = 1_000_000.0
        monkeypatch.setattr(time, "time", lambda: now)
        credential_state.record_rejection(401, _FP)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        assert "systemMessage" in capsys.readouterr().out

        later = now + credential_state.NOTICE_INTERVAL_S + 1
        monkeypatch.setattr(time, "time", lambda: later)
        credential_state.record_rejection(401, _FP)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        assert "systemMessage" in capsys.readouterr().out

    def test_negative_cache_expires_after_ttl(self, monkeypatch, capsys):
        posted = _install_api(monkeypatch, 401)
        now = 1_000_000.0
        monkeypatch.setattr(time, "time", lambda: now)
        credential_state.record_rejection(401, _FP)
        monkeypatch.setattr(
            time, "time", lambda: now + credential_state.NEGATIVE_CACHE_TTL_S + 1
        )
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        assert posted, "an expired negative cache must let the real call through"

    def test_re_minted_key_bypasses_negative_cache(
        self, monkeypatch, capsys, state_dir
    ):
        posted = _install_api(monkeypatch, 401)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        before = len(posted)
        # The check-in re-minted the key: the record is for the old one.
        monkeypatch.setattr(
            relay, "_load_credentials_uncached", lambda: (_HOST, "fresh")
        )
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        assert len(posted) > before
        assert _state(state_dir)[
            "fingerprint"
        ] == credential_state.credential_fingerprint(_HOST, "fresh")

    def test_clients_without_message_channel_allow_silently(self, monkeypatch, capsys):
        _install_api(monkeypatch, 401)
        credential_state.record_rejection(401, _FP)
        _run_hook(
            monkeypatch, _CURSOR_MCP, mode=AIWatchMode.MONITOR, client=Client.CURSOR
        )
        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}

    def test_short_circuit_keeps_post_hook_shapes(self, monkeypatch, capsys):
        _install_api(monkeypatch, 401)
        credential_state.record_rejection(401, _FP)
        _run_hook(
            monkeypatch,
            {"hook_event_name": "afterMCPExecution", "tool_name": "search"},
            mode=AIWatchMode.MONITOR,
            client=Client.CURSOR,
        )
        assert capsys.readouterr().out == "{}"
        _run_hook(
            monkeypatch,
            {"hook_event_name": "PostToolUse", "tool_name": "read_file"},
            mode=AIWatchMode.MONITOR,
            client=Client.CLINE_CLI,
        )
        assert capsys.readouterr().out == ""

    def test_intermediary_401_does_not_arm_the_negative_cache(
        self, monkeypatch, capsys, state_dir
    ):
        """Monitor keeps calling the API through a proxy's 401s: nothing is
        recorded, so the next hook posts again instead of synthesizing a
        cached credential rejection for the TTL."""
        posted = _install_api(monkeypatch, 401, intermediary=True)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        first_calls = len(posted)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        assert _state(state_dir) is None
        assert len(posted) > first_calls, (
            "an intermediary 401 must not arm the negative cache"
        )
        for flow in _flows():
            # Best-effort Monitor relay: the call was allowed, so the flow is
            # not a failure and carries no credential-rejection label.
            assert flow.get("error_type") is None
            assert flow["status"] == "ok"
            assert "credential_rejected_cached" not in _step_names(flow)

    @pytest.mark.parametrize("status", [403, 500])
    def test_other_http_errors_keep_todays_behaviour(
        self, monkeypatch, capsys, state_dir, status
    ):
        posted = _install_api(monkeypatch, status)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        assert _state(state_dir) is None
        first_calls = len(posted)
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        assert len(posted) > first_calls, f"a {status} must not arm the negative cache"
        assert _flows()[-1].get("error_type") != "HookCredentialRejectedMonitor"

    def test_corrupt_state_file_is_treated_as_absent(
        self, monkeypatch, capsys, state_dir
    ):
        posted = _install_api(monkeypatch, 401)
        state_dir.mkdir(parents=True)
        (state_dir / "credential_rejected.json").write_text("{not json")
        _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.MONITOR)
        capsys.readouterr()
        assert posted
        assert _state(state_dir)["status"] == 401


class TestEnforceStaysFailClosed:
    def test_enforce_denies_with_hostname_and_admin_guidance(self, monkeypatch, capsys):
        _install_api(monkeypatch, 401)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        out = json.loads(capsys.readouterr().out)
        reason = out["hookSpecificOutput"]["permissionDecisionReason"]
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert "HTTP 401" in reason
        assert "- Device hostname: LAPTOP-42" in reason
        assert "Settings → MDM configuration and the audit log" in reason
        assert "re-deploy a current configuration to this device" in reason
        assert "Runlayer administrator" in reason
        assert "runlayer login" not in reason
        flow = _flows()[-1]
        assert flow["error_type"] == "HookInfraDeny"
        assert flow["error_category"] == "http_401"

    def test_user_key_install_is_told_to_log_in(self, monkeypatch, capsys):
        """No org key on the device: the per-user secret was rejected, and a
        fresh ``runlayer login`` is exactly what refreshes it."""
        _install_api(monkeypatch, 401)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {})
        monkeypatch.setenv("RUNLAYER_HOSTNAME", "USERBOX")
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        reason = _deny_reason(capsys.readouterr().out)
        assert "Run 'runlayer login'" in reason
        assert "device management" not in reason
        assert "- Device hostname: USERBOX" in reason

    def test_enforce_never_uses_the_negative_cache(self, monkeypatch, capsys):
        posted = _install_api(monkeypatch, 401)
        credential_state.record_rejection(401, _FP)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        assert posted, "Enforce must re-verify so a re-minted key recovers"

    def test_hostname_lookup_failure_still_denies(self, monkeypatch, capsys):
        _install_api(monkeypatch, 401)
        monkeypatch.setattr(relay, "read_managed_config", lambda: {"org_api_key": "k"})
        monkeypatch.delenv("RUNLAYER_HOSTNAME", raising=False)

        def _no_hostname() -> str:
            raise OSError("gethostname failed")

        monkeypatch.setattr(socket, "gethostname", _no_hostname)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        out = capsys.readouterr().out
        assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert "Device hostname" not in _deny_reason(out)

    def test_runlayer_403_keeps_the_generic_http_deny_with_request_id(
        self, monkeypatch, capsys, state_dir
    ):
        """Runlayer's own 403 is not a credential answer: no cache, no
        credential wording, but the request id and detail ride along so
        support can find the server-side log line."""
        _install_api(monkeypatch, 403)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        reason = _deny_reason(capsys.readouterr().out)
        assert "was answered with HTTP 403" in reason
        assert "Security Violation Detected" in reason
        assert "- Request ID: req-0001" in reason
        assert '- Detail: "Invalid API key"' in reason
        assert "credentials" not in reason
        assert "Block type: Network" not in reason
        assert _state(state_dir) is None
        flow = _flows()[-1]
        assert flow["error_type"] == "HookInfraDeny"
        assert flow["error_category"] == "http_403"
        assert flow["error_http_status"] == 403

    def test_intermediary_403_is_a_network_block_not_a_policy_violation(
        self, monkeypatch, capsys, state_dir
    ):
        """An AWS WAF source-IP allowlist answers 403 with an HTML page and no
        Runlayer markers. The deny must say the network rejected it, point at
        the VPN, and never claim a policy decision."""
        _install_api(monkeypatch, 403, intermediary=True)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        reason = out["hookSpecificOutput"]["permissionDecisionReason"]
        assert "Runlayer Verification Blocked by Network" in reason
        assert "- Block type: Network" in reason
        assert "- Tool: Edit" in reason
        assert "- Device hostname: LAPTOP-42" in reason
        assert "answered with HTTP 403 by a network device" in reason
        assert "VPN or zero-trust client" in reason
        assert "Security Violation Detected" not in reason
        assert "enforced by Runlayer" not in reason
        assert "security policy" not in reason
        assert "Request ID" not in reason
        assert "<html>" not in reason
        assert _state(state_dir) is None
        flow = _flows()[-1]
        assert flow["error_type"] == "HookNetworkDeny"
        assert flow["error_category"] == "http_403"

    def test_intermediary_401_is_network_wording_and_arms_nothing(
        self, monkeypatch, capsys, state_dir
    ):
        """A proxy's 401 says nothing about the Runlayer credential: no
        credential wording, no hostname-and-admin remedy, and the negative
        cache stays unarmed."""
        _install_api(monkeypatch, 401, intermediary=True)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        reason = _deny_reason(capsys.readouterr().out)
        assert "- Block type: Network" in reason
        assert "HTTP 401" in reason
        assert "credentials" not in reason
        assert "runlayer login" not in reason
        assert "MDM configuration" not in reason
        assert _state(state_dir) is None
        flow = _flows()[-1]
        assert flow["error_type"] == "HookNetworkDeny"
        assert flow["error_category"] == "http_401"
        assert flow["error_http_status"] == 401

    def test_legacy_backend_401_without_marker_still_counts_as_runlayer(
        self, monkeypatch, capsys, state_dir
    ):
        """Backends without the origin marker: request id + JSON envelope is
        enough to keep the credential behaviour."""
        _install_api(monkeypatch, 401, headers=_LEGACY_RUNLAYER_HEADERS)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _PRE_TOOL, mode=AIWatchMode.ENFORCE)
        reason = _deny_reason(capsys.readouterr().out)
        assert "HTTP 401" in reason
        assert "- Device hostname: LAPTOP-42" in reason
        assert "Block type: Network" not in reason
        assert _state(state_dir) is not None


class TestProtectUnchanged:
    """Protect is out of scope: its source-governance step stays fail-open and
    its scanner step stays fail-closed on a credential rejection, exactly as
    on main. Pinned so the Monitor change cannot drift into Protect."""

    def test_protect_source_governance_fails_open_as_before(self, monkeypatch, capsys):
        posted = _install_api(monkeypatch, 401)
        _run_hook(
            monkeypatch, _CURSOR_MCP, mode=AIWatchMode.PROTECT, client=Client.CURSOR
        )
        assert json.loads(capsys.readouterr().out) == {"permission": "allow"}
        assert posted
        flow = _flows()[-1]
        assert flow["status"] == "error"
        assert flow["error_type"] == "HookInfraFailOpen"
        assert flow["error_category"] == "http_401"
        # Protect never consults the negative cache either.
        credential_state.record_rejection(401, _FP)
        before = len(posted)
        _run_hook(
            monkeypatch, _CURSOR_MCP, mode=AIWatchMode.PROTECT, client=Client.CURSOR
        )
        assert len(posted) > before

    def test_protect_scanner_step_still_denies_as_before(self, monkeypatch, capsys):
        # Today's behaviour, unchanged here: after the fail-open enforce step
        # Protect continues into the scanner tool-pre, which is fail-closed.
        _install_api(monkeypatch, 401)
        with pytest.raises(SystemExit):
            _run_hook(monkeypatch, _MCP_PRE_TOOL, mode=AIWatchMode.PROTECT)
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert _flows()[-1]["error_type"] == "HookInfraDeny"


class TestCredentialState:
    def test_fresh_equivalent_record_is_not_rewritten(self, monkeypatch, state_dir):
        monkeypatch.setattr(time, "time", lambda: 100.0)
        credential_state.record_rejection(401, _FP)
        monkeypatch.setattr(time, "time", lambda: 200.0)
        credential_state.record_rejection(401, _FP)
        assert _state(state_dir)["at"] == 100.0
        # A different credential is a new fact and is written.
        credential_state.record_rejection(401, "other-fingerprint")
        assert _state(state_dir) == {
            "at": 200.0,
            "status": 401,
            "fingerprint": "other-fingerprint",
        }

    def test_claim_notice_once_per_hour_bucket(self, monkeypatch, state_dir):
        monkeypatch.setattr(time, "time", lambda: 7200.0)
        assert credential_state.claim_notice() is True
        assert credential_state.claim_notice() is False
        monkeypatch.setattr(time, "time", lambda: 7200.0 + 3600.0)
        assert credential_state.claim_notice() is True
        markers = sorted(p.name for p in state_dir.glob("credential_notice.*"))
        assert markers == ["credential_notice.3"]

    def test_parallel_claims_yield_exactly_one_notice(self, state_dir):
        results: list[bool] = []
        barrier = threading.Barrier(8)

        def claim() -> None:
            barrier.wait()
            results.append(credential_state.claim_notice())

        threads = [threading.Thread(target=claim) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert results.count(True) == 1

    def test_write_failure_never_raises(self, isolated_credential_state):
        isolated_credential_state.mkdir(parents=True, exist_ok=True)
        (isolated_credential_state / "state").write_text(
            "a file where the dir should be"
        )
        credential_state.record_rejection(401, _FP)
        assert credential_state.recent_rejection(_FP) is None
        assert credential_state.claim_notice() is False
