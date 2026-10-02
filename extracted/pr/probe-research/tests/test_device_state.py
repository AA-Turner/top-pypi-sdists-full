"""The setup wizard's ONE server call (`POST /v1/device-state`).

Driven against a REAL local HTTP server, never a mocked client: the two ways
this call can silently go wrong are both about bytes on the wire -- the SDK
transport would have scrubbed every capture credential to `<redacted>`, and a
credential batched to the wrong server leaks it. A fake transport would hide
both. The wizard end-to-end test counts requests the same way: exactly one
before the answer.
"""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
import threading
import time
from concurrent.futures import Future
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe import version_policy
from probe.cli import capabilities as caps_mod
from probe.cli import doctor

cli_main = importlib.import_module("probe.cli.main")

#: Captured at import, before conftest's `_no_real_device_state` replaces it.
_REAL_FETCH = caps_mod.fetch_device_state

CLAUDE_TOKEN = "ros_ing_" + "a" * 48
CODEX_TOKEN = "ros_ing_" + "b" * 48
CLI_TOKEN = "probe_pat_" + "c" * 32
EMAIL = "ada@example.test"
MANIFEST = {"cli": {"latest": "9.9.9", "min": "0.1.0"}, "plugin": {}, "tap": {}}


class _Served:
    def __init__(self) -> None:
        self.requests: list[tuple[str, str, dict[str, str], bytes]] = []
        self.status = 200
        self.delay = 0.0
        self.raw: bytes | None = None
        self.answer: dict = {
            "account": {"email": EMAIL, "customer_id": "acme", "role": "owner"},
            "account_status": "ok",
            "capture": {"claude_code": "ok", "codex": "rejected", "pi": "unknown"},
            "versions": MANIFEST,
        }
        #: Answers for the OLD calls, for an older server without the route.
        self.legacy = False
        #: Serve the unfiled-runs list even when the route exists.
        self.legacy_runs = False
        #: Serve `/v1/me` even when the route exists.
        self.legacy_me = False
        #: Answer these paths with this status (and an empty object), whatever else.
        self.status_by_path: dict[str, int] = {}
        #: Answers for later calls, in order (the first call gets `answer`).
        self.then: list[dict] = []
        #: Send this many body bytes, then hang up (a truncated response).
        self.truncate: int | None = None
        #: Extra response headers (a redirect's Location).
        self.headers: dict[str, str] = {}
        self.url = ""

    def paths(self) -> list[str]:
        return [f"{method} {path.split('?')[0]}" for method, path, _h, _b in self.requests]


@pytest.fixture
def server():
    yield from _serve()


@pytest.fixture
def elsewhere_server():
    """A second host: where a redirect would take the request."""
    yield from _serve()


def _serve():
    served = _Served()

    class Handler(BaseHTTPRequestHandler):
        def _serve(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            served.requests.append((self.command, self.path, dict(self.headers), body))
            if served.delay:
                time.sleep(served.delay)
            path = self.path.split("?")[0]
            if path in served.status_by_path:
                status, payload = served.status_by_path[path], b"{}"
            elif path == "/v1/device-state" and not served.legacy:
                answer = served.answer
                if served.then and sum(1 for r in served.requests if r[1] == path) > 1:
                    answer = served.then.pop(0)
                    served.answer = answer
                status, payload = served.status, served.raw or json.dumps(answer).encode()
            elif (served.legacy or served.legacy_me) and path == "/v1/me":
                status, payload = 200, json.dumps({"email": "old-way@example.test"}).encode()
            elif served.legacy and path == "/ingest/v1/sessions/status":
                status, payload = 200, b'{"ingest_enabled": true}'
            elif (served.legacy or served.legacy_runs) and path == "/v1/runs":
                status, payload = 200, b'{"items": [], "next_cursor": null}'
            else:
                status, payload = 404, b'{"detail": "Not Found"}'
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            for name, value in served.headers.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(payload[: served.truncate] if served.truncate else payload)

        do_GET = do_POST = _serve

        def log_message(self, *_args) -> None:
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    served.url = f"http://127.0.0.1:{httpd.server_port}"
    yield served
    httpd.shutdown()
    httpd.server_close()


@pytest.fixture
def home(tmp_path, monkeypatch):
    """Every probe state path in a tmpdir: config, state, each agent's tap dir."""
    for var, sub in (
        ("PROBE_CONFIG_PATH", "probe/config.json"),
        ("XDG_CONFIG_HOME", "."),
        ("XDG_STATE_HOME", "state"),
        ("XDG_CACHE_HOME", "cache"),
        (caps_mod.ENV_TAP_PLUGIN_DIR, "tap-claude"),
        (caps_mod.ENV_CODEX_TAP_PLUGIN_DIR, "tap-codex"),
        (caps_mod.ENV_PI_TAP_PLUGIN_DIR, "tap-pi"),
        ("PI_CODING_AGENT_DIR", "pi-agent"),
    ):
        monkeypatch.setenv(var, str(tmp_path / sub))
    for var in (
        "PROBE_BASE_URL",
        "PROBE_TOKEN",
        caps_mod.ENV_INGEST_TOKEN,
        caps_mod.ENV_CODEX_INGEST_TOKEN,
        caps_mod.ENV_PI_INGEST_TOKEN,
    ):
        monkeypatch.delenv(var, raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _sign_in(url: str, token: str | None = CLI_TOKEN) -> None:
    from probe.sdk.config import save_context

    save_context({"base_url": url, **({"token": token} if token else {})})


def _pair(source: str, token: str, *, base_url: str | None = None) -> None:
    tap = caps_mod.tap_plugin_dir(source)
    tap.mkdir(parents=True, exist_ok=True)
    (tap / ".token").write_text(token)
    if base_url:
        (tap / ".config").write_text(json.dumps({"api_base_url": base_url}))


def _request(url: str, token: str | None = CLI_TOKEN) -> caps_mod.DeviceStateRequest:
    return caps_mod.device_state_request(url, token, ("claude_code", "codex", "pi"))


# --- the wire: one request, real credentials, only to their own server -----------


def test_one_request_carries_every_agents_real_credential(home, server) -> None:
    """CRITICAL. The SDK transport would have scrubbed these to `<redacted>`."""
    _pair("claude_code", CLAUDE_TOKEN)
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url)

    state = _REAL_FETCH(_request(server.url))

    assert server.paths() == ["POST /v1/device-state"]
    _method, _path, headers, body = server.requests[0]
    assert json.loads(body) == {"capture_tokens": {"claude_code": CLAUDE_TOKEN, "codex": CODEX_TOKEN}}
    assert headers["Authorization"] == f"Bearer {CLI_TOKEN}"
    assert headers["X-Probe-Client"] == "cli"
    assert state.answered
    assert state.account_email == EMAIL
    assert state.account_valid is True
    assert state.capture == {"claude_code": True, "codex": False}


def test_signed_out_sends_no_authorization(home, server) -> None:
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url, token=None)
    server.answer["account_status"] = "signed_out"
    server.answer["account"] = None

    state = _REAL_FETCH(_request(server.url, token=None))

    assert "Authorization" not in server.requests[0][2]
    assert state.answered and state.account_valid is None and state.account_email is None


def test_a_credential_for_another_server_is_never_sent(home, server, monkeypatch) -> None:
    """CRITICAL. Codex is paired to a different API (plugin `.config`): its key
    must not ride to this server, and the answer claims nothing about it."""
    _pair("claude_code", CLAUDE_TOKEN)
    _pair("codex", CODEX_TOKEN, base_url="https://staging.example.test")
    _sign_in(server.url)

    request = _request(server.url)
    state = _REAL_FETCH(request)

    assert request.elsewhere == ("codex",)
    assert CODEX_TOKEN.encode() not in server.requests[0][3]
    assert state.capture == {"claude_code": True}


@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_a_redirect_is_never_followed_and_never_carries_the_token(
    home, server, elsewhere_server, status
) -> None:
    """CRITICAL. urllib's default opener follows a redirect and copies the
    bearer to whatever host `Location` names (an SSO proxy in front of a
    self-hosted API). The call must stop at the 3xx."""
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url)
    server.status = status
    server.headers = {"Location": f"{elsewhere_server.url}/login"}

    state = _REAL_FETCH(_request(server.url))

    # Not followed; something in front of the route answered, so the wizard
    # asks the old way -- as it did in this network before.
    assert state.outcome is caps_mod.DeviceStateOutcome.UNSUPPORTED
    assert elsewhere_server.requests == []


@pytest.mark.parametrize("status", [401, 403])
def test_a_proxy_refusing_the_route_means_the_old_way(home, server, status) -> None:
    _sign_in(server.url)
    server.status = status
    assert _REAL_FETCH(_request(server.url)).outcome is caps_mod.DeviceStateOutcome.UNSUPPORTED


def test_the_capture_check_never_follows_a_redirect_either(
    home, server, elsewhere_server
) -> None:
    """The pre-existing per-agent check carries a capture key too: a redirect
    must neither carry it on nor read a login page's 200 as "accepted"."""
    _pair("codex", CODEX_TOKEN, base_url=server.url)
    server.status_by_path["/ingest/v1/sessions/status"] = 302
    server.headers = {"Location": f"{elsewhere_server.url}/login"}
    assert caps_mod.verify_capture_credential("codex") is None
    assert elsewhere_server.requests == []


def test_all_proxy_is_honoured(home, server, monkeypatch) -> None:
    """urllib ignores ALL_PROXY; httpx (the calls this replaced) honours it."""
    for var in ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("ALL_PROXY", server.url)
    _REAL_FETCH(_request("http://api.nowhere.invalid"))
    assert server.requests and server.requests[0][1].startswith("http://api.nowhere.invalid/")


@pytest.mark.parametrize("proxy", ["https://proxy.example.test:8443", "socks5://proxy.example.test:1080"])
def test_a_proxy_urllib_cannot_speak_means_the_old_way(home, server, monkeypatch, proxy) -> None:
    """httpx (the SDK, the old calls) speaks TLS and SOCKS proxies; urllib does
    not. Such a machine asks the old way from the start, sending nothing here."""
    for var in ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("ALL_PROXY", proxy)
    state = _REAL_FETCH(_request("https://api.example.test"))
    assert state.outcome is caps_mod.DeviceStateOutcome.UNSUPPORTED


def test_proxies_urllib_can_use_are_used(monkeypatch) -> None:
    for var in ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HTTPS_PROXY", "proxy.example.test:8080")  # scheme-less = plain HTTP
    assert caps_mod._urllib_cannot_reach("https://api.example.test") is False
    monkeypatch.setenv("HTTPS_PROXY", "https://proxy.example.test:8443")
    monkeypatch.setenv("NO_PROXY", "api.example.test:8443")  # bypass names the port
    assert caps_mod._urllib_cannot_reach("https://api.example.test:8443") is False
    assert caps_mod._urllib_cannot_reach("https://api.example.test") is True


def test_the_worker_writes_no_cache_after_the_readers_gave_up(home, server, monkeypatch) -> None:
    """One deadline for worker and readers: a worker delayed past it (slow
    start, a slow opener) must not write the cache the readers graded against."""
    import threading as _threading

    _sign_in(server.url)
    version_policy.write_cache({"cli": {"latest": "1.0.0"}}, True)
    monkeypatch.setattr(caps_mod, "fetch_device_state", _REAL_FETCH)
    monkeypatch.setattr(caps_mod, "DEVICE_STATE_TIMEOUT_S", 0.2)
    monkeypatch.setattr(caps_mod, "DEVICE_STATE_GRACE_S", 0.0)
    gate = _threading.Event()
    real_opener = caps_mod._credential_opener
    monkeypatch.setattr(caps_mod, "_credential_opener", lambda: gate.wait(5) and real_opener())

    resolve = caps_mod.start_device_state(_request(server.url))
    assert resolve().outcome is caps_mod.DeviceStateOutcome.UNREACHABLE
    gate.set()
    resolve._future.result(timeout=5)  # the worker has finished, late answer and all
    assert version_policy.read_cache()[0] == {"cli": {"latest": "1.0.0"}}


def test_an_invalid_header_value_never_echoes_the_token(home, server) -> None:
    broken = CLI_TOKEN + "\nX-Injected: 1"
    state = _REAL_FETCH(caps_mod.device_state_request(server.url, broken, ()))
    assert state.outcome is caps_mod.DeviceStateOutcome.UNREACHABLE
    assert CLI_TOKEN not in (state.error or "")


def test_the_request_hides_its_secrets_from_repr(home) -> None:
    _pair("codex", CODEX_TOKEN)
    _sign_in("http://api.test")
    shown = repr(_request("http://api.test"))
    assert CODEX_TOKEN not in shown and CLI_TOKEN not in shown


def test_a_trailing_slash_is_still_this_server(home, server) -> None:
    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url + "/")
    request = caps_mod.device_state_request(server.url + "/", CLI_TOKEN, ("claude_code",))
    assert request.capture_tokens == {"claude_code": CLAUDE_TOKEN}
    assert request.elsewhere == ()


# --- the answer ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("account_status", "valid"),
    [("ok", True), ("rejected", False), ("signed_out", None), ("unknown", None), ("new", None)],
)
def test_only_a_refusal_reads_as_an_invalid_account(home, server, account_status, valid) -> None:
    """The wizard forces sign-in on `False`; nothing but a refusal may produce it."""
    _sign_in(server.url)
    server.answer["account_status"] = account_status
    assert _REAL_FETCH(_request(server.url)).account_valid is valid


def test_the_answer_refreshes_the_version_cache(home, server) -> None:
    _sign_in(server.url)
    _REAL_FETCH(_request(server.url))
    manifest, _fetched_at, ok = version_policy.read_cache()
    assert manifest == MANIFEST and ok


def test_a_cold_servers_empty_manifest_never_blanks_a_good_cache(home, server) -> None:
    _sign_in(server.url)
    version_policy.write_cache(MANIFEST, True)
    server.answer["versions"] = {"cli": {"latest": None}, "plugin": {}, "tap": {}}
    _REAL_FETCH(_request(server.url))
    assert version_policy.read_cache()[0] == MANIFEST


def test_an_older_server_is_unsupported_and_refreshes_the_manifest(home, server, monkeypatch) -> None:
    from probe.cli import versions

    _sign_in(server.url)
    server.status = 404
    warmed: list[bool] = []
    monkeypatch.setattr(versions, "warm_manifest", lambda **_: warmed.append(True))

    monkeypatch.setattr(caps_mod, "fetch_device_state", _REAL_FETCH)
    state = caps_mod.start_device_state(_request(server.url))()
    assert state.outcome is caps_mod.DeviceStateOutcome.UNSUPPORTED
    time.sleep(0.2)
    assert warmed == []
    state = caps_mod.start_device_state(_request(server.url), warm_manifest_on_fallback=True)()
    assert state.outcome is caps_mod.DeviceStateOutcome.UNSUPPORTED
    for _ in range(50):
        if warmed:
            break
        time.sleep(0.05)
    assert warmed == [True]


def test_unsupported_is_published_before_the_manifest_is_warmed(home, server, monkeypatch) -> None:
    """A slow manifest fetch must not hold an older server's verdict past the
    readers' deadline -- they would read UNREACHABLE and skip the old calls."""
    from probe.cli import versions

    _sign_in(server.url)
    server.status = 404
    release = threading.Event()
    monkeypatch.setattr(versions, "warm_manifest", lambda **_: release.wait(10))
    monkeypatch.setattr(caps_mod, "fetch_device_state", _REAL_FETCH)
    try:
        started = time.monotonic()
        state = caps_mod.start_device_state(_request(server.url), warm_manifest_on_fallback=True)()
        assert time.monotonic() - started < 3.0
        assert state.outcome is caps_mod.DeviceStateOutcome.UNSUPPORTED
    finally:
        release.set()


def test_an_oversized_answer_is_unreachable(home, server) -> None:
    _sign_in(server.url)
    server.raw = b'{"pad": "' + b"x" * (caps_mod.DEVICE_STATE_MAX_BYTES + 10) + b'"}'
    assert _REAL_FETCH(_request(server.url)).outcome is caps_mod.DeviceStateOutcome.UNREACHABLE


def test_an_answer_past_the_deadline_is_nobodys_and_writes_no_cache(home, server, monkeypatch) -> None:
    _sign_in(server.url)
    version_policy.write_cache({"cli": {"latest": "1.0.0"}}, True)
    monkeypatch.setattr(caps_mod, "DEVICE_STATE_GRACE_S", -60.0)  # already late
    state = _REAL_FETCH(_request(server.url))
    assert state.outcome is caps_mod.DeviceStateOutcome.UNREACHABLE
    assert version_policy.read_cache()[0] == {"cli": {"latest": "1.0.0"}}


@pytest.mark.parametrize(
    "answer",
    [
        {"account_status": []},
        {"account_status": {"ok": True}},
        {"capture": {"codex": {}}},
        {"capture": {"codex": ["ok"]}},
        {"account": {"email": 7}},
        {"capture": "ok"},
    ],
)
def test_a_malformed_field_is_unknown_never_a_raise(home, server, answer) -> None:
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url)
    server.answer.update(answer)
    state = _REAL_FETCH(_request(server.url))
    assert state.answered
    assert state.account_valid in (True, None)
    assert state.capture.get("codex") in (None, False)


@pytest.mark.parametrize("failure", ["500", "garbled", "not-an-object", "slow", "truncated"])
def test_every_failure_is_unreachable_and_never_raises(home, server, failure) -> None:
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url)
    if failure == "500":
        server.status = 500
    elif failure == "garbled":
        server.raw = b"<html>proxy login</html>"
    elif failure == "not-an-object":
        server.raw = b"[1, 2]"
    elif failure == "truncated":
        server.truncate = 10  # IncompleteRead: an http.client error, not an OSError
    else:
        server.delay = 2.0
    started = time.monotonic()
    state = _REAL_FETCH(_request(server.url), timeout=0.5)
    assert time.monotonic() - started < 2.0
    assert state.outcome is caps_mod.DeviceStateOutcome.UNREACHABLE
    assert state.error
    assert len(server.requests) == 1, "one call, never retried"


def test_nothing_listening_is_unreachable(home) -> None:
    import socket

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    state = _REAL_FETCH(_request(f"http://127.0.0.1:{port}"), timeout=0.5)
    assert state.outcome is caps_mod.DeviceStateOutcome.UNREACHABLE


def test_a_pending_call_is_bounded(home) -> None:
    never: Future = Future()
    started = time.monotonic()
    state = caps_mod.device_state_result(never, timeout=0.2)
    assert time.monotonic() - started < 1.0
    assert state.outcome is caps_mod.DeviceStateOutcome.UNREACHABLE


def test_every_reader_shares_one_deadline_and_one_answer() -> None:
    """Several agents read one call: a stuck call must cost its deadline once,
    not once per agent, and every agent must see the same answer."""
    never: Future = Future()
    resolve = caps_mod.device_state_resolver(never, timeout=0.3)
    started = time.monotonic()
    first = resolve()
    second = resolve()
    never.set_result(caps_mod.DeviceState(caps_mod.DeviceStateOutcome.ANSWERED))
    third = resolve()
    assert time.monotonic() - started < 1.0
    assert first.outcome is caps_mod.DeviceStateOutcome.UNREACHABLE
    assert second is first and third is first


def test_start_answers_from_a_background_thread(home, server, monkeypatch) -> None:
    monkeypatch.setattr(caps_mod, "fetch_device_state", _REAL_FETCH)
    _sign_in(server.url)
    assert caps_mod.start_device_state(_request(server.url))().answered


# --- doctor.collect() inside the wizard's scope ---------------------------------------


def _state(**overrides) -> caps_mod.DeviceState:
    fields = {
        "outcome": caps_mod.DeviceStateOutcome.ANSWERED,
        "account_email": EMAIL,
        "account_valid": True,
        "capture": {"codex": True},
    }
    fields.update(overrides)
    return caps_mod.DeviceState(**fields)


@pytest.fixture
def codex_paired(home, monkeypatch):
    _sign_in("http://api.test")
    _pair("codex", CODEX_TOKEN)
    monkeypatch.setenv("PROBE_AGENT", "codex")
    return home


@pytest.fixture
def old_way(monkeypatch):
    """Record every old-way server call `collect()` makes."""
    calls: list[str] = []

    def login(settings):
        calls.append("login")
        return doctor._LoginCheck(logged_in_as="old-way@example.test", api_credential_valid=True)

    monkeypatch.setattr(doctor, "_check_login", login)
    monkeypatch.setattr(
        caps_mod, "verify_capture_credential", lambda *a, **k: calls.append("capture") or True
    )
    return calls


def test_an_answer_means_collect_asks_nothing_of_its_own(codex_paired, old_way) -> None:
    with doctor.device_state_scope(lambda: _state()):
        caps = doctor.collect()
    assert old_way == []
    assert caps.logged_in_as == EMAIL
    assert caps.api_credential_valid is True
    assert caps.capture_credential_valid is True
    assert caps.unfiled_runs is None  # the wizard never shows it; nobody fetched it


def test_a_refused_account_is_the_only_false(codex_paired, old_way) -> None:
    with doctor.device_state_scope(lambda: _state(account_valid=False, account_email=None)):
        caps = doctor.collect()
    assert caps.api_credential_valid is False
    assert caps.logged_in_as is None
    assert any("refused" in warning for warning in caps.warnings)


def test_an_unchecked_account_is_unknown_not_refused(codex_paired, old_way) -> None:
    """The headline promise: a server that could not check the credential never
    reads as a refusal (which would send the person back through sign-in)."""
    with doctor.device_state_scope(lambda: _state(account_valid=None, account_email=None)):
        caps = doctor.collect()
    assert old_way == []
    assert caps.api_credential_valid is None
    assert any("could not check" in warning for warning in caps.warnings)


def test_signed_out_in_scope_warns_about_no_login(home, monkeypatch, old_way) -> None:
    _sign_in("http://api.test", token=None)
    _pair("codex", CODEX_TOKEN)
    monkeypatch.setenv("PROBE_AGENT", "codex")
    with doctor.device_state_scope(lambda: _state(account_valid=None, account_email=None)):
        caps = doctor.collect()
    assert caps.api_credential_valid is None and caps.logged_in_as is None
    assert not any("could not verify login" in warning for warning in caps.warnings)


def test_an_agent_paired_elsewhere_is_asked_of_its_own_server(codex_paired, old_way) -> None:
    """No verdict in the answer (the key never rode in it): the old way, for
    that agent only."""
    with doctor.device_state_scope(lambda: _state(capture={"claude_code": True})):
        caps = doctor.collect()
    assert old_way == ["capture"]
    assert caps.capture_credential_valid is True


def test_no_answer_reads_like_an_offline_machine(codex_paired, old_way) -> None:
    unreachable = caps_mod.DeviceState(caps_mod.DeviceStateOutcome.UNREACHABLE, error="timed out")
    with doctor.device_state_scope(lambda: unreachable):
        caps = doctor.collect()
    assert old_way == []
    assert caps.api_credential_valid is None
    assert caps.capture_credential_valid is None
    assert any(w.startswith("could not verify login against") for w in caps.warnings)
    assert any(w.startswith("could not verify the capture credential") for w in caps.warnings)


def test_an_older_server_falls_back_to_the_old_calls(codex_paired, old_way) -> None:
    older = caps_mod.DeviceState(caps_mod.DeviceStateOutcome.UNSUPPORTED)
    with doctor.device_state_scope(lambda: older):
        caps = doctor.collect()
    assert old_way == ["login", "capture"]
    assert caps.logged_in_as == "old-way@example.test"


def test_the_answer_is_awaited_after_the_local_checks(codex_paired, old_way, monkeypatch) -> None:
    """The plugin-CLI check is the slow local one; it must run while the
    request is in flight, not after it."""
    order: list[str] = []
    real_plugins = caps_mod.installed_plugins
    monkeypatch.setattr(
        caps_mod,
        "installed_plugins",
        lambda **kw: order.append("plugins") or real_plugins(**kw),
    )
    with doctor.device_state_scope(lambda: order.append("remote") or _state()):
        doctor.collect()
    assert order == ["plugins", "remote"]


def test_probe_doctor_still_asks_the_old_way(codex_paired, old_way) -> None:
    doctor.collect()
    assert old_way == ["login", "capture"]


# --- the wizard, end to end -------------------------------------------------------------


def _run_wizard(server, monkeypatch, *argv: str):
    from typer.testing import CliRunner

    from probe.cli import bootstrap

    monkeypatch.setattr(caps_mod, "fetch_device_state", _REAL_FETCH)
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda: SimpleNamespace(message=""))
    if not argv:
        argv = ("--action", "diagnose", "--yes")
    return CliRunner().invoke(cli_main.app, ["wizard", "--agent", "both", *argv])


def test_the_wizard_asks_the_server_exactly_once(home, server, monkeypatch) -> None:
    """THE CONTRACT: account, both agents' capture and the manifest, one request.
    Diagnose is the one screen that also shows the unfiled-runs count, so it
    adds exactly that list -- once, for both agents' reports -- and nothing of
    the old per-agent calls."""
    _pair("claude_code", CLAUDE_TOKEN)
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url)

    result = _run_wizard(server, monkeypatch)

    assert result.exit_code == 0, result.output
    assert server.paths() == ["POST /v1/device-state", "GET /v1/runs"]
    assert EMAIL in result.output


def test_diagnose_still_shows_the_unfiled_runs(home, server, monkeypatch) -> None:
    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url)
    server.legacy_runs = True

    result = _run_wizard(server, monkeypatch)

    assert result.exit_code == 0, result.output
    assert "Unfiled runs" in result.output


def test_an_older_server_gets_the_old_calls_through_the_wizard(home, server, monkeypatch) -> None:
    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url)
    server.legacy = True

    result = _run_wizard(server, monkeypatch)

    assert result.exit_code == 0, result.output
    assert server.paths()[0] == "POST /v1/device-state"
    assert "GET /v1/me" in server.paths()
    assert "old-way@example.test" in result.output


def test_uninstall_reads_the_next_agent_fresh(home, server, monkeypatch) -> None:
    """Uninstall revokes each agent's key as it goes (two agents can share
    one), so the second agent is read with a fresh call -- and only then."""
    _pair("claude_code", CLAUDE_TOKEN)
    _pair("codex", CODEX_TOKEN)
    _sign_in(server.url)
    seen: list[tuple[str, bool | None]] = []

    def uninstall(action, *, caps, **_kwargs):
        seen.append((caps.agent_source, caps.capture_credential_valid))
        return ["Removed."]

    from probe.cli import setup

    monkeypatch.setattr(cli_main, "_run_wizard_action", uninstall)
    monkeypatch.setattr(setup, "finish_removal", lambda: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    server.answer["capture"] = {"claude_code": "ok", "codex": "ok"}
    server.then = [dict(server.answer, capture={"claude_code": "rejected", "codex": "rejected"})]

    result = _run_wizard(server, monkeypatch, "--action", "uninstall", "--yes")

    assert result.exit_code == 0, result.output
    assert [p for p in server.paths() if p.endswith("/v1/device-state")] == [
        "POST /v1/device-state",
        "POST /v1/device-state",
    ]
    assert "GET /v1/me" not in server.paths()
    assert seen == [("claude_code", True), ("codex", False)]


def test_signing_in_asks_again_and_clears_the_refusal(home, server, monkeypatch) -> None:
    """Before sign-in the server refuses the old credential; the wizard signs
    in, asks once more, and the new answer -- not the stale refusal -- decides."""
    from probe.cli import setup

    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url)
    server.answer = dict(server.answer, account_status="rejected", account=None)
    server.then = [dict(server.answer, account_status="ok", account={"email": EMAIL})]
    signed: list[bool] = []

    def sign_in(**_kwargs):
        signed.append(True)
        return setup.SignInResult(ok=True, lines=[])

    monkeypatch.setattr(setup, "sign_in", sign_in)

    result = _run_wizard(server, monkeypatch, "ABCDEFGHJK", "--action", "diagnose", "--yes")

    assert result.exit_code == 0, result.output
    assert signed == [True]
    assert [p for p in server.paths() if p.endswith("/v1/device-state")] == [
        "POST /v1/device-state",
        "POST /v1/device-state",
    ]
    assert "GET /v1/me" not in server.paths()
    assert EMAIL in result.output


def test_an_install_code_names_the_account_the_old_way_before_switching(
    home, server, monkeypatch
) -> None:
    """CRITICAL. Redeeming a code switches the account irreversibly and is
    refused headless when the account being replaced can be NAMED. The one call
    could not name it (unknown), so the wizard must ask the old way rather than
    decide there is nothing to switch from."""
    from probe.cli import setup

    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url)
    server.answer = dict(server.answer, account_status="unknown", account=None)
    server.legacy_me = True

    def must_not_sign_in(**_kwargs):
        raise AssertionError("switched accounts without confirmation")

    monkeypatch.setattr(setup, "sign_in", must_not_sign_in)

    result = _run_wizard(server, monkeypatch, "ABCDEFGHJK", "--action", "diagnose")

    assert result.exit_code == 1, result.output
    assert "old-way@example.test" in result.output
    assert "GET /v1/me" in server.paths()


def test_diagnose_asks_again_when_the_held_answer_was_not_one(home, server, monkeypatch) -> None:
    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url)
    server.status = 500  # launch: no answer
    first = server.answer

    def recover(*_a, **_k):
        server.status = 200
        return None

    # The menu snapshot is taken on the failed answer; Diagnose must re-ask.
    real_fetch = _REAL_FETCH
    calls: list[int] = []

    def fetch(request, **kwargs):
        calls.append(1)
        if len(calls) == 2:
            recover()
        return real_fetch(request, **kwargs)

    monkeypatch.setattr(caps_mod, "fetch_device_state", fetch)
    from probe.cli import bootstrap
    from typer.testing import CliRunner

    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda: SimpleNamespace(message=""))
    result = CliRunner().invoke(
        cli_main.app, ["wizard", "--agent", "claude", "--action", "diagnose", "--yes"]
    )

    assert result.exit_code == 0, result.output
    assert len(calls) == 2
    assert first["account"]["email"] in result.output
    assert "Unfiled runs" in result.output  # the single-agent path shows it too


def test_the_call_goes_to_the_server_collect_reports_on(home, server, monkeypatch) -> None:
    """`--base-url` does not redirect the call (or its bearer): it goes to the
    API `doctor.collect()` resolves and grades against."""
    _pair("claude_code", CLAUDE_TOKEN)
    _sign_in(server.url)
    monkeypatch.setattr(caps_mod, "fetch_device_state", _REAL_FETCH)
    from probe.cli import bootstrap
    from typer.testing import CliRunner

    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda: SimpleNamespace(message=""))
    result = CliRunner().invoke(
        cli_main.app,
        ["--base-url", "http://127.0.0.1:9", "wizard", "--agent", "claude", "--action", "diagnose", "--yes"],
    )
    assert result.exit_code == 0, result.output
    assert server.paths()[0] == "POST /v1/device-state"


# --- the local speedups -----------------------------------------------------------------


def test_the_daemon_libraries_are_located_not_imported(tmp_path) -> None:
    """Importing pydantic_ai costs ~1.5 s on every wizard launch. Stub packages
    that EXPLODE on import prove it is located, not imported -- CI has no
    `daemon` extra, so a real absence would pass either way."""
    import os

    for name in ("pydantic_ai", "pydantic_ai_harness"):
        (tmp_path / name).mkdir()
        (tmp_path / name / "__init__.py").write_text("raise RuntimeError('imported')\n")
    code = "from probe.cli.daemon_cli import located_ai_libraries; print(located_ai_libraries())"
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(tmp_path), *sys.path])}
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() not in ("", "None")


def test_a_missing_daemon_library_still_reads_missing(monkeypatch) -> None:
    import importlib.util

    from probe.cli import daemon_cli

    real = importlib.util.find_spec
    monkeypatch.setattr(
        importlib.util,
        "find_spec",
        lambda name, *a: None if name == "pydantic_ai_harness" else real(name, *a),
    )
    assert daemon_cli.located_ai_libraries() is None


def test_the_readiness_check_still_imports(tmp_path) -> None:
    """Choosing, provisioning and `probe daemon install` ask `ai_libraries`, and a
    package that is present but broken must read MISSING there."""
    import os

    for name in ("pydantic_ai", "pydantic_ai_harness"):
        (tmp_path / name).mkdir()
        (tmp_path / name / "__init__.py").write_text("raise ImportError('a dependency is missing')\n")
    code = "from probe.cli.daemon_cli import ai_libraries; print(ai_libraries())"
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(tmp_path), *sys.path])}
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "None"


def test_this_install_needs_no_version_subprocess(tmp_path, monkeypatch) -> None:
    from probe.cli import bootstrap

    prefix = tmp_path / "tools" / "probe-research"
    (prefix / "bin").mkdir(parents=True)
    entry = prefix / "bin" / "probe"
    entry.write_text("#!/bin/sh\n")
    link = tmp_path / "bin" / "probe"
    link.parent.mkdir()
    link.symlink_to(entry)
    monkeypatch.setattr(sys, "prefix", str(prefix))
    monkeypatch.setattr(bootstrap, "_installed_binary", lambda: str(link))

    def _no_subprocess(_binary):
        raise AssertionError("asked this very install for its version with a subprocess")

    monkeypatch.setattr(bootstrap, "_version_of", _no_subprocess)
    assert bootstrap._resolves_on_path() is True


def test_another_install_is_still_asked_its_version(tmp_path, monkeypatch) -> None:
    from probe import __version__
    from probe.cli import bootstrap

    other = tmp_path / "elsewhere" / "bin" / "probe"
    other.parent.mkdir(parents=True)
    other.write_text("#!/bin/sh\n")
    monkeypatch.setattr(sys, "prefix", str(tmp_path / "this-env"))
    monkeypatch.setattr(bootstrap, "_installed_binary", lambda: str(other))
    asked: list[str] = []
    monkeypatch.setattr(bootstrap, "_version_of", lambda b: asked.append(b) or "0.0.1")
    assert bootstrap._resolves_on_path() is (__version__ == "0.0.1")
    assert asked == [str(other)]
    assert Path(asked[0]).name == "probe"
