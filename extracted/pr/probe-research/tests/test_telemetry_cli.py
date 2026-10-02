"""CLI telemetry: the core contract and the in-process async sender.

The failure mode every test here guards is SILENT WRONGNESS: telemetry is
fail-silent by contract, so a gate that mutes the wrong population, a sender
that reorders events, or an identity that flips on the sign-in transition
never errors — it just makes the funnel lie.
"""

from __future__ import annotations

import json
import re
import threading
import time

import pytest

from probe.sdk import _telemetry_core as core
from probe.cli import telemetry as tm


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    """Every state/config path into a tmpdir; never a developer's real install.

    Env credentials are cleared too: effective_token/effective_base_url honor
    PROBE_TOKEN/PROBE_MCP_TOKEN/PROBE_BASE_URL, so a developer's exported shell
    would otherwise flip identity_mode and gate assertions."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for var in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_MCP_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture()
def telemetry_on(monkeypatch):
    monkeypatch.setenv("PROBE_TELEMETRY", "on")


@pytest.fixture()
def captured(monkeypatch, telemetry_on):
    """Capture emit() records at the queue seam: no thread, no network."""
    records: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)  # keep atexit out of tests
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def _write_config(tmp_path, data: dict) -> None:
    (tmp_path / "probe" / "config.json").write_text(json.dumps(data))


# --- killswitch + hosted gate ----------------------------------------------


@pytest.mark.parametrize(
    ("value", "disabled"),
    [
        ("off", True),
        ("0", True),
        ("false", True),
        ("no", True),
        ("disabled", True),
        ("", False),
        ("on", False),
        ("1", False),
    ],
)
def test_killswitch_values(monkeypatch, value, disabled):
    monkeypatch.setenv("PROBE_TELEMETRY", value)
    assert core.telemetry_disabled() is disabled


@pytest.mark.parametrize(
    ("base_url", "hosted"),
    [
        ("https://api.research.prbe.ai", True),
        ("https://api.research.prbe.ai:8443/v1", True),  # our host, any port/path
        ("https://prbe.ai", True),
        (None, True),  # unset resolves to the hosted default — fresh installs MUST emit
        ("", True),
        ("http://api.research.prbe.ai", False),  # https only: a bearer rides to this URL
        ("http://localhost:8000", False),
        ("https://research.internal.example.com", False),  # self-host
        ("https://evil-notprbe.ai", False),  # dot-boundary, not substring
        ("https://xprbe.ai", False),
        ("https://evil.com/api.research.prbe.ai", False),  # host wins, not path
        ("not a url", False),
    ],
)
def test_hosted_gate(base_url, hosted):
    assert core.hosted_base_url(base_url) is hosted


# --- config + identity ------------------------------------------------------


def test_read_cli_config_v1_and_v2(tmp_path):
    _write_config(tmp_path, {"token": "t1", "base_url": "https://api.research.prbe.ai"})
    assert core.read_cli_config()["token"] == "t1"
    _write_config(
        tmp_path,
        {
            "contexts": {"default": {"token": "t2"}, "other": {"token": "t3"}},
            "current_context": "other",
        },
    )
    assert core.read_cli_config()["token"] == "t3"


def test_read_cli_config_corrupt_and_missing(tmp_path):
    assert core.read_cli_config() == {}
    (tmp_path / "probe" / "config.json").write_text("{nope")
    assert core.read_cli_config() == {}


def test_machine_id_minted_once_and_reused(tmp_path):
    first = core.machine_id()
    assert re.fullmatch(r"[0-9a-f]{32}", first)
    assert core.machine_id() == first
    state = tmp_path / "state" / "probe-telemetry"
    assert (state.stat().st_mode & 0o777) == 0o700
    assert ((state / "machine_id").stat().st_mode & 0o777) == 0o600


def test_machine_id_mint_race_yields_the_winner(monkeypatch, tmp_path):
    """First-writer-wins: a concurrent mint (wizard sender vs plugin hook on
    the very first session) must converge on ONE id, not last-write-wins."""
    winner = "a" * 32
    real_open = core.os.open

    def contended_open(path, flags, mode=0o777):
        if str(path).endswith("machine_id") and flags & core.os.O_EXCL:
            (tmp_path / "state" / "probe-telemetry" / "machine_id").write_text(winner)
            raise FileExistsError(path)
        return real_open(path, flags, mode)

    (tmp_path / "state" / "probe-telemetry").mkdir(parents=True)
    monkeypatch.setattr(core.os, "open", contended_open)
    assert core.machine_id() == winner


def test_machine_id_without_resolvable_home_is_ephemeral(monkeypatch, tmp_path):
    """No HOME (arbitrary-uid container): never create a literal ./~/ tree."""
    monkeypatch.chdir(tmp_path)
    # context(): the expanduser patch must not outlive the test body — the
    # shared monkeypatch instance otherwise keeps it alive into conftest's
    # teardown asserts, which resolve real paths.
    with monkeypatch.context() as m:
        m.delenv("XDG_STATE_HOME", raising=False)
        m.setattr(core.os.path, "expanduser", lambda p: p)
        assert core._state_home() is None
        mid = core.machine_id()
    assert re.fullmatch(r"[0-9a-f]{32}", mid)
    assert not (tmp_path / "~").exists()


def test_resolve_identity_without_token_is_machine_keyed():
    ident = core.resolve_identity({})
    assert ident["distinct_id"] == f"machine:{core.machine_id()}"
    assert ident["authenticated"] is False


def test_resolve_identity_caches_and_invalidates_on_token_change(monkeypatch):
    calls = []

    class _Resp:
        def __init__(self, body: dict):
            self._body = json.dumps(body).encode()

        def read(self):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=None, context=None):
        calls.append(req.full_url)
        return _Resp({"user_id": "user-uuid-1", "email": "r@prbe.ai", "customer_id": "acme"})

    monkeypatch.setattr(core.urllib.request, "urlopen", fake_urlopen)
    cfg = {"token": "tok-a", "base_url": "https://api.research.prbe.ai"}
    first = core.resolve_identity(cfg)
    assert first["distinct_id"] == "user-uuid-1" and first["authenticated"] is True
    core.resolve_identity(cfg)
    assert len(calls) == 1, "second resolve must hit the 24h disk cache"
    core.resolve_identity({**cfg, "token": "tok-b"})
    assert len(calls) == 2, "a login-minted token must invalidate the cache"


def test_resolve_identity_falls_back_on_rejected_token(monkeypatch):
    def rejected(req, timeout=None, context=None):
        raise OSError("401")

    monkeypatch.setattr(core.urllib.request, "urlopen", rejected)
    ident = core.resolve_identity({"token": "revoked", "base_url": core.DEFAULT_BASE})
    assert ident["distinct_id"].startswith("machine:")
    assert ident["authenticated"] is False


def test_resolve_identity_never_sends_a_bearer_off_the_hosted_service(monkeypatch):
    """The /v1/me call requires the hosted gate: a token must not be POSTed to
    a URL telemetry would refuse to emit for (incl. plain http)."""
    calls: list[str] = []
    monkeypatch.setattr(
        core.urllib.request,
        "urlopen",
        lambda req, timeout=None, context=None: calls.append(req.full_url),
    )
    for base in ("http://api.research.prbe.ai", "https://selfhost.example.com"):
        ident = core.resolve_identity({"token": "tok", "base_url": base})
        assert ident["authenticated"] is False
    assert calls == []


def test_resolve_identity_cache_writes_are_private(monkeypatch, tmp_path):
    class _Resp:
        def __init__(self):
            self._body = json.dumps({"user_id": "u1"}).encode()

        def read(self):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(
        core.urllib.request, "urlopen", lambda req, timeout=None, context=None: _Resp()
    )
    core.resolve_identity({"token": "tok", "base_url": core.DEFAULT_BASE})
    cache = tmp_path / "state" / "probe-telemetry" / "identity.json"
    assert (cache.stat().st_mode & 0o777) == 0o600


def test_resolve_identity_ignores_a_future_dated_cache(monkeypatch, tmp_path):
    """A skewed clock must not pin stale identity fresh forever."""
    state = tmp_path / "state" / "probe-telemetry"
    state.mkdir(parents=True)
    cfg = {"token": "tok", "base_url": core.DEFAULT_BASE}
    key = core.hashlib.sha256(f"{core.effective_base_url(cfg)}|tok".encode()).hexdigest()[:16]
    (state / "identity.json").write_text(
        json.dumps({"key": key, "fetched_at": time.time() + 9999, "user_id": "stale"})
    )
    calls: list[str] = []

    def refetch(req, timeout=None, context=None):
        calls.append(req.full_url)
        raise OSError("network")

    monkeypatch.setattr(core.urllib.request, "urlopen", refetch)
    core.resolve_identity(cfg)
    assert calls, "future-dated cache must be treated as expired, not fresh"


def test_resolve_identity_honors_env_token(monkeypatch):
    monkeypatch.setenv("PROBE_TOKEN", "env-tok")
    calls: list[str] = []

    def attempted(req, timeout=None, context=None):
        calls.append(req.get_header("Authorization"))
        raise OSError("offline")

    monkeypatch.setattr(core.urllib.request, "urlopen", attempted)
    core.resolve_identity({})
    assert calls == ["Bearer env-tok"], "PROBE_TOKEN must authenticate like resolve()"


# --- batch building ---------------------------------------------------------


def test_build_batch_anonymous_cli_event():
    (entry,) = core.build_batch(
        [
            {
                "event": "wizard.started",
                "timestamp": "2026-08-13T00:00:00.000+00:00",
                "properties": {"session_id": "s1"},
            }
        ],
        {
            "distinct_id": "machine:abc",
            "authenticated": False,
            "customer_id": None,
            "workspace_id": None,
        },
        client_kind="cli",
        lib="probe-cli",
        client_version="0.75.0",
        machine="abc",
    )
    props = entry["properties"]
    assert entry["timestamp"] == "2026-08-13T00:00:00.000+00:00"
    assert props["$process_person_profile"] is False
    assert props["client_kind"] == "cli"
    assert props["machine_id"] == "abc"
    assert "team" not in props and "$groups" not in props  # omitted, never null


def test_build_batch_authenticated_cli_event_merges_with_server_events():
    (entry,) = core.build_batch(
        [{"event": "wizard.signed_in", "properties": {"session_id": "s1"}}],
        {
            "distinct_id": "user-uuid",
            "email": "r@prbe.ai",
            "customer_id": "acme",
            "workspace_id": "ws",
            "authenticated": True,
        },
        client_kind="cli",
        lib="probe-cli",
        client_version="0.75.0",
        machine="abc",
    )
    props = entry["properties"]
    assert entry["distinct_id"] == "user-uuid"
    assert props["$groups"] == {"team": "acme"} and props["$set"] == {"email": "r@prbe.ai"}
    assert "$process_person_profile" not in props


# --- TelemetryContext -------------------------------------------------------


def test_context_disabled_by_killswitch(monkeypatch):
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    ctx = tm.TelemetryContext.start(via="wizard", interactive=True, base_url=None)
    assert ctx.enabled is False


def test_context_disabled_off_hosted(telemetry_on):
    ctx = tm.TelemetryContext.start(
        via="wizard", interactive=True, base_url="http://localhost:8000"
    )
    assert ctx.enabled is False


def test_emit_stamps_time_identity_and_session(captured):
    ctx = tm.TelemetryContext.start(via="wizard", interactive=True, base_url=None)
    assert ctx.enabled and ctx.invoked_by == "human"
    ctx.emit(
        tm.EVENT_WIZARD_STARTED,
        identity_mode=tm.IdentityMode.AUTHENTICATED,
        fresh_install=True,
        skipped_prop=None,
    )
    (rec,) = captured
    assert rec["event"] == tm.EVENT_WIZARD_STARTED
    assert rec["identity_mode"] == "authenticated"
    # millisecond ISO-8601 UTC — second resolution would re-race the funnel
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+00:00", rec["timestamp"])
    props = rec["properties"]
    assert props["session_id"] == ctx.session_id and props["via"] == "wizard"
    assert props["invoked_by"] == "human" and props["fresh_install"] is True
    assert "skipped_prop" not in props  # None props are dropped, never null


def test_emit_marks_non_tty_as_automation(captured):
    ctx = tm.TelemetryContext.start(via="wizard", interactive=False, base_url=None)
    ctx.emit(tm.EVENT_WIZARD_INVOKED)
    assert captured[0]["properties"]["invoked_by"] == "automation"


def test_null_context_emits_nothing(captured):
    tm.null_context().emit(tm.EVENT_WIZARD_INVOKED)
    assert captured == []


def test_emit_defaults_identity_mode_from_current_config(captured, tmp_path):
    """A forgotten identity_mode kwarg must never mislabel an authenticated
    event: the default computes from the config AT EMIT TIME."""
    ctx = tm.TelemetryContext.start(via=tm.Via.WIZARD, interactive=True, base_url=None)
    ctx.emit("wizard.started")
    _write_config(tmp_path, {"token": "t"})
    ctx.emit("wizard.signed_in")
    assert captured[0]["identity_mode"] == "anonymous"
    assert captured[1]["identity_mode"] == "authenticated"


def test_identity_mode_from_config(tmp_path):
    assert tm.identity_mode_from_config() == tm.IdentityMode.ANONYMOUS
    _write_config(tmp_path, {"mcp_token": "t"})
    assert tm.identity_mode_from_config() == tm.IdentityMode.AUTHENTICATED


# --- the sender thread ------------------------------------------------------


def _record(event: str, mode: str = "anonymous") -> dict:
    return {
        "event": event,
        "identity_mode": mode,
        "timestamp": "2026-08-13T00:00:00.000+00:00",
        "properties": {"session_id": "s"},
    }


def test_sender_delivers_in_order_and_flushes(telemetry_on):
    sender = tm._Sender()
    batches: list[list[dict]] = []
    sender.transport = lambda entries: batches.append(entries)
    for i in range(3):
        sender.put(_record(f"e{i}"))
    sender.start()
    sender.request_flush()
    sent = [entry["event"] for batch in batches for entry in batch]
    assert sent == ["e0", "e1", "e2"]
    assert all(e["distinct_id"].startswith("machine:") for b in batches for e in b)


def test_sender_survives_transport_failure_and_stays_silent(telemetry_on, capsys):
    sender = tm._Sender()
    first_call = threading.Event()
    calls: list[list[str]] = []

    def flaky(entries):
        calls.append([e["event"] for e in entries])
        first_call.set()
        raise OSError("posthog down")

    sender.transport = flaky
    sender.put(_record("first"))
    sender.start()
    # Synchronize on the first (failed) send so the second put genuinely
    # exercises delivery AFTER a transport failure — a sleep would let both
    # records coalesce into one batch under CI contention and verify nothing.
    assert first_call.wait(5), "first batch never reached the transport"
    sender.put(_record("second"))
    sender.request_flush()
    assert len(calls) >= 2, "a failed POST must not kill the thread"
    assert "second" in calls[-1]
    out = capsys.readouterr()
    assert out.out == "" and out.err == ""  # a traceback would corrupt the TUI frame


def test_sender_send_time_gate_mutes_a_self_host_config(telemetry_on, tmp_path):
    """The gate is re-checked against the config the identity resolver reads:
    a hosted --base-url over a self-host config must not ship that instance's
    identity to the vendor (the context gate alone cannot see this)."""
    _write_config(tmp_path, {"base_url": "https://research.internal.example.com"})
    sender = tm._Sender()
    batches: list[list[dict]] = []
    sender.transport = lambda entries: batches.append(entries)
    sender.put(_record("leaky", mode="authenticated"))
    sender.start()
    sender.request_flush()
    assert batches == [], "self-host config at send time must mute the batch"


def test_queue_overflow_drops_and_flush_stays_bounded(telemetry_on):
    """put() past QUEUE_MAX must neither raise nor block, and request_flush on
    a full queue (stop sentinel cannot enqueue) must still return promptly."""
    sender = tm._Sender()  # thread never started: queue only fills
    for i in range(tm.QUEUE_MAX + 10):
        sender.put(_record(f"e{i}"))
    assert sender.q.qsize() == tm.QUEUE_MAX
    t0 = time.monotonic()
    sender.request_flush(timeout=0.2)
    assert time.monotonic() - t0 < 3.0


def test_flush_is_bounded_when_the_network_hangs(telemetry_on):
    sender = tm._Sender()
    release = threading.Event()
    sender.transport = lambda entries: release.wait(5)
    sender.put(_record("stuck"))
    sender.start()
    t0 = time.monotonic()
    sender.request_flush(timeout=0.2)
    # Generous bound (join is 0.2s): timing asserts flake badly under
    # contended CI; the property is "far below the 5s transport hang".
    assert time.monotonic() - t0 < 3.0, "exit must never wait on a dead network"
    release.set()


def test_send_time_login_cannot_reclassify_an_anonymous_event(telemetry_on, tmp_path, monkeypatch):
    """The D8.3 invariant: identity_mode is decided at emit, honored at send."""
    _write_config(tmp_path, {"token": "tok", "base_url": core.DEFAULT_BASE})
    monkeypatch.setattr(
        core,
        "resolve_identity",
        lambda cfg, **kw: {
            "distinct_id": "user-uuid",
            "authenticated": True,
            "customer_id": "acme",
            "workspace_id": None,
        },
    )
    sender = tm._Sender()
    batches: list[list[dict]] = []
    sender.transport = lambda entries: batches.append(entries)
    sender.put(_record("pre-login", mode="anonymous"))
    sender.put(_record("post-login", mode="authenticated"))
    sender.start()
    sender.request_flush()
    by_event = {e["event"]: e for b in batches for e in b}
    assert by_event["pre-login"]["distinct_id"].startswith("machine:")
    assert by_event["post-login"]["distinct_id"] == "user-uuid"


def test_post_batch_shape(telemetry_on, monkeypatch):
    posted: dict = {}

    class _Resp:
        def read(self):
            return b"ok"

    def fake_urlopen(req, timeout=None, context=None):
        posted["url"] = req.full_url
        posted["body"] = json.loads(req.data.decode())
        posted["timeout"] = timeout
        return _Resp()

    # The wire shape lives in the shared core; the CLI's _post_batch is it.
    monkeypatch.setattr(core.urllib.request, "urlopen", fake_urlopen)
    tm._post_batch([{"event": "e", "distinct_id": "d", "properties": {}}])
    assert posted["url"].endswith("/batch/")
    assert posted["body"]["api_key"] == core.POSTHOG_KEY
    assert posted["timeout"] == core.SEND_TIMEOUT
