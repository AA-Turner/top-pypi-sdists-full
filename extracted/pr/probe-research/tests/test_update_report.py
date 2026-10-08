"""Auto-update outcomes reach the server, per component, and never cost the caller.

`perform_update` used to tell only the machine it ran on how it went
(`autoupdate.json`). In production that hid WHY machines with auto-update on
kept a current CLI while the transcript tap sat at 0.9.3: no PATH to `claude`
in the detached updater, a tap under a retired id, a failed marketplace
refresh, or a run holding the lock all looked the same -- like nothing. Every
test here pins one of those causes to its own code on the wire, or pins that a
report can never break, slow, or block what triggered it.

Nothing reaches a real `claude`, `codex` or server: the plugin CLIs are faked,
and the report's one network door (`update_report._deliver`) is either the
conftest's offline recorder or a local HTTP server this file starts.
"""

from __future__ import annotations

import http.server
import json
import socket
import threading
import time

import pytest

from probe.cli import autoupdate, claude_cli, update_report, updater, upgrading, versions

MANIFEST = {
    "cli": {"latest": "0.221.0"},
    "plugin": {"latest": "0.120.0"},
    "tap": {"latest": "0.9.11"},
}
TOKEN = "probe_pat_" + "0" * 32
#: The real network door, taken at import: the conftest swaps it for an offline
#: recorder before every test, and the wire tests below put it back.
REAL_DELIVER = update_report._deliver


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe" / "config.json"))
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(tmp_path / "state" / "device.json"))
    monkeypatch.setenv("PROBE_TOKEN", TOKEN)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv(autoupdate.WAIT_FOR_PID_ENV, raising=False)
    monkeypatch.delenv(autoupdate.TRIGGER_ENV, raising=False)
    # A faked upgrade records its "installed" CLI process-wide
    # (`versions.record_installed_cli`); left set, it grades every later test's
    # CLI in this worker as that version.
    monkeypatch.setattr(versions, "_installed_cli", None)


@pytest.fixture
def sent(monkeypatch):
    """Every report `flush` hands to the network, answered 202."""
    bodies: list[dict] = []

    def _accept(base_url, headers, body, timeout):
        bodies.append(body)
        return 202

    monkeypatch.setattr(update_report, "_deliver", _accept)
    return bodies


def _ledger(home, plugins: dict[str, str]) -> None:
    path = home / ".claude" / "plugins" / "installed_plugins.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"plugins": {key: [{"version": v}] for key, v in plugins.items()}})
    )


def _stub_cli(monkeypatch, *, cli_after="0.221.0"):
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: MANIFEST)
    monkeypatch.setattr(
        upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL)
    )
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda install, current, target: updater.CliResult(
            True, True, True, current, cli_after, f"CLI upgraded {current} → {cli_after}"
        ),
    )


def _which(monkeypatch, *present: str):
    """`shutil.which` that finds exactly `present`: the updater's PATH."""
    monkeypatch.setattr(
        updater.shutil, "which", lambda name: f"/usr/local/bin/{name}" if name in present else None
    )


def _claude(monkeypatch, *, fail_on: str | None = None, detail: str = "fatal: no network"):
    """A fake `claude` that succeeds at everything but the command containing
    `fail_on` and moves nothing."""

    def _run(args, *, timeout):
        command = " ".join(["claude", *args])
        if fail_on and fail_on in command:
            return claude_cli.Result(ok=False, detail=detail, command=command)
        return claude_cli.Result(ok=True, command=command)

    monkeypatch.setattr(updater.claude_cli, "run", _run)


def _update(trigger=update_report.Trigger.SESSION_START):
    return upgrading.perform_update(base_url="https://api.test", include_plugin=True,
                                    trigger=trigger)


# ---------------------------------------------------------------------------
# One report per attempt, each cause its own code
# ---------------------------------------------------------------------------


def test_claude_missing_from_the_updaters_path(tmp_path, monkeypatch, sent):
    """The leading suspect in production: the hook-spawned updater has no
    `claude` on PATH. The tap is still installed and readable from the ledger,
    so the report says both halves: tap 0.9.3, `claude` not found."""
    _stub_cli(monkeypatch)
    _which(monkeypatch)  # neither claude nor codex
    _ledger(tmp_path / "home", {
        "probe-research@research-os-agent": "0.112.0",
        "probe-research-tap@research-os-agent": "0.9.3",
    })

    outcome = _update()

    assert outcome.ok  # unchanged: a missing `claude` is not an update failure
    [report] = sent
    assert report["trigger"] == "session_start"
    assert report["outcome"] == "ok"
    assert report["cli"]["result"] == "updated"
    assert report["plugin"]["result"] == "not_found_on_path"
    assert "`claude` not found on PATH" in report["plugin"]["detail"]
    assert report["tap"] == {
        "before": "0.9.3",
        "after": "0.9.3",
        "target": "0.9.11",
        "result": "not_found_on_path",
        "detail": "`claude` not found on PATH (skipping plugin update)",
        "harness": "claude_code",
    }
    assert (report["claude_found"], report["codex_found"]) == (False, False)


def test_a_tap_installed_only_under_a_retired_id(tmp_path, monkeypatch, sent):
    """`tap_verdict` calls this "not installed (skipped)": the update looks for
    `probe-research-tap@research-os-agent` and finds nothing. The report names
    the copy that is actually there."""
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")
    _claude(monkeypatch)
    _ledger(tmp_path / "home", {
        "probe-research@research-os-agent": "0.120.0",
        "prbe-cc-tap-plugin@prbe-ai": "0.9.3",
    })

    outcome = _update()

    assert any("transcript tap not installed (skipped)" in line for line in outcome.lines)
    [report] = sent
    assert report["tap"]["result"] == "legacy_installed"
    assert "prbe-cc-tap-plugin@prbe-ai" in report["tap"]["detail"]
    assert report["legacy_plugin_ids"] == ["prbe-cc-tap-plugin@prbe-ai"]
    assert report["plugin"]["result"] == "current"
    assert report["claude_found"] is True


def test_a_tap_from_another_marketplace_is_legacy_too(tmp_path, monkeypatch, sent):
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")
    _claude(monkeypatch)
    _ledger(tmp_path / "home", {
        "probe-research@research-os-agent": "0.120.0",
        "probe-research-tap@prbe-ai": "0.9.3",
    })

    _update()

    [report] = sent
    assert report["tap"]["result"] == "legacy_installed"
    assert report["legacy_plugin_ids"] == ["probe-research-tap@prbe-ai"]


def test_no_tap_at_all_is_not_installed(tmp_path, monkeypatch, sent):
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")
    _claude(monkeypatch)
    _ledger(tmp_path / "home", {"probe-research@research-os-agent": "0.120.0"})

    _update()

    [report] = sent
    assert report["tap"]["result"] == "not_installed"
    assert report["legacy_plugin_ids"] == []


def test_a_failed_marketplace_refresh(tmp_path, monkeypatch, sent):
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")
    _claude(monkeypatch, fail_on="marketplace update", detail="fatal: unable to access github")
    _ledger(tmp_path / "home", {
        "probe-research@research-os-agent": "0.112.0",
        "probe-research-tap@research-os-agent": "0.9.3",
    })

    outcome = _update()

    assert not outcome.ok
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == "refresh_failed"
    assert report["tap"]["result"] == "refresh_failed"
    assert "unable to access github" in report["tap"]["detail"]


def test_a_tap_still_behind_after_a_clean_update(tmp_path, monkeypatch, sent):
    """Every command exited 0 and the tap did not move: behind, with the no-op's
    own explanation -- distinct from every failure above."""
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")
    _claude(monkeypatch)
    _ledger(tmp_path / "home", {
        "probe-research@research-os-agent": "0.120.0",
        "probe-research-tap@research-os-agent": "0.9.3",
    })

    _update()

    [report] = sent
    assert report["tap"]["result"] == "behind"
    assert report["tap"]["detail"] == updater.TAP_NOOP
    assert report["plugin"]["result"] == "current"
    assert report["plugin"]["detail"] == ""


def test_a_failed_tap_command_is_an_error(tmp_path, monkeypatch, sent):
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")
    _claude(monkeypatch, fail_on=f"update {updater.TAP_PLUGIN_ID}", detail="Error: EACCES")
    _ledger(tmp_path / "home", {
        "probe-research@research-os-agent": "0.120.0",
        "probe-research-tap@research-os-agent": "0.9.3",
    })

    _update()

    [report] = sent
    assert report["tap"]["result"] == "error"
    assert "EACCES" in report["tap"]["detail"]


def test_codex_missing_from_the_updaters_path(monkeypatch, sent):
    monkeypatch.setenv("PROBE_AGENT", "codex")
    _stub_cli(monkeypatch)
    _which(monkeypatch, "claude")

    _update(update_report.Trigger.CLI)

    [report] = sent
    assert report["harness"] == "codex"
    assert report["trigger"] == "cli"
    assert report["plugin"]["result"] == "not_found_on_path"
    assert report["tap"]["result"] == "not_found_on_path"
    assert (report["claude_found"], report["codex_found"]) == (True, False)


def test_a_retired_codex_tap_is_reported(monkeypatch, sent):
    monkeypatch.setenv("PROBE_AGENT", "codex")
    _stub_cli(monkeypatch)
    _which(monkeypatch, "codex")
    ok = claude_cli.Result(ok=True)
    monkeypatch.setattr(updater.plugin_cli, "refresh_marketplace", lambda source, market: ok)
    monkeypatch.setattr(updater.plugin_cli, "install", lambda source, plugin_id: ok)
    listed = {"probe-research": "0.120.0", "prbe-codex-tap-plugin": "0.9.3"}
    monkeypatch.setattr(updater, "_codex_plugin_versions", lambda codex=None: dict(listed))

    _update()

    [report] = sent
    assert report["legacy_plugin_ids"] == ["prbe-codex-tap-plugin"]
    assert report["tap"]["result"] == "legacy_installed"


def test_an_editable_cli_is_behind_with_the_reason(tmp_path, monkeypatch, sent):
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: MANIFEST)
    monkeypatch.setattr(
        upgrading.updater,
        "detect_install",
        lambda: updater.Install(updater.Method.EDITABLE, detail="editable / source checkout"),
    )
    monkeypatch.setattr(upgrading, "__version__", "0.218.1")
    _which(monkeypatch)

    _update(update_report.Trigger.MANUAL)

    [report] = sent
    assert report["trigger"] == "manual"
    assert report["cli"]["result"] == "behind"
    assert report["cli"]["before"] == "0.218.1"
    assert "editable/source install" in report["cli"]["detail"]


def test_a_broken_report_never_breaks_a_finished_update(monkeypatch, sent):
    _stub_cli(monkeypatch)
    _which(monkeypatch)

    def _boom(**kwargs):
        raise RuntimeError("report bug")

    monkeypatch.setattr(update_report, "attempt_report", _boom)
    outcome = _update()

    assert outcome.ok
    assert autoupdate.load().last_attempt.to_version == "0.221.0"
    assert sent == []


def test_the_report_is_dated_when_the_attempt_ran(monkeypatch, sent):
    _stub_cli(monkeypatch)
    _which(monkeypatch)

    _update()

    [report] = sent
    assert report["attempted_at"] == autoupdate.load().last_attempt.at


def test_the_local_record_is_written_as_before(tmp_path, monkeypatch, sent):
    """The report is IN ADDITION to `autoupdate.json`, which `probe doctor` reads."""
    _stub_cli(monkeypatch)
    _which(monkeypatch)

    _update()

    attempt = autoupdate.load().last_attempt
    assert attempt is not None and attempt.to_version == "0.221.0"
    assert sent


# ---------------------------------------------------------------------------
# Skips
# ---------------------------------------------------------------------------


def test_a_run_in_flight_skip_is_reported_with_its_trigger(monkeypatch, sent):
    from probe.cli import run_lock

    monkeypatch.setattr(run_lock, "any_live", lambda: True)

    outcome = _update(update_report.Trigger.SESSION_START)

    assert outcome.ok and "a run is in flight" in outcome.lines[0]
    assert sent == [{
        "schema_version": 1,
        "trigger": "session_start",
        "outcome": "skipped",
        "skip_reason": "run_in_flight",
        "skip_count": 1,
    }]


def test_a_hot_path_skip_touches_no_network_and_reaches_the_next_flush(monkeypatch, sent):
    """`record_skip` runs inside training loops: it writes its local record and
    nothing else. The detached refresher's flush sends it, once."""
    for _ in range(3):
        autoupdate.record_skip(autoupdate.SKIP_NOT_A_TTY, available="0.221.0")
    assert sent == []

    update_report.flush("https://api.test")
    update_report.flush("https://api.test")

    assert sent == [{
        "schema_version": 1,
        "trigger": "cli",
        "outcome": "skipped",
        "skip_reason": "not_a_tty",
        "skip_count": 3,
    }]
    autoupdate.record_skip(autoupdate.SKIP_NOT_A_TTY, available="0.221.0")
    update_report.flush("https://api.test")
    assert [body["skip_count"] for body in sent] == [3, 4]


def test_the_refresher_flushes_waiting_reports(monkeypatch, sent):
    from probe import version_policy
    from probe.cli import version_refresh

    monkeypatch.setattr(version_policy, "refresh", lambda context=None: None)
    monkeypatch.setattr(version_policy, "base_url", lambda: "https://api.test")
    autoupdate.record_skip(autoupdate.SKIP_HOT_PATH_COMMAND)

    version_refresh._refresh()

    assert [body["skip_reason"] for body in sent] == ["hot_path_command"]


def test_an_unknown_skip_reason_is_sent_as_other(sent):
    autoupdate.record_skip("some reason a newer CLI invented")
    update_report.flush("https://api.test")
    assert sent[0]["skip_reason"] == "other"


def test_an_attempt_and_a_later_skip_go_oldest_first(monkeypatch, sent):
    update_report.queue_attempt({"schema_version": 1, "outcome": "ok"}, now=int(time.time()) - 5)
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)

    update_report.flush("https://api.test")

    assert [body["outcome"] for body in sent] == ["ok", "skipped"]


# ---------------------------------------------------------------------------
# Never fails, never waits long, never resends what landed
# ---------------------------------------------------------------------------


def test_an_unreachable_server_keeps_the_report_and_raises_nothing(monkeypatch, _no_real_update_reports):
    """The conftest's door answers nothing, like a laptop on a plane."""
    update_report.submit_attempt({"schema_version": 1, "outcome": "ok"}, base_url="https://x")
    assert _no_real_update_reports  # it tried
    assert "attempt" in json.loads(update_report.pending_path().read_text())


def test_a_door_that_raises_is_contained(monkeypatch):
    def _explode(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(update_report, "_deliver", _explode)
    update_report.submit_attempt({"schema_version": 1, "outcome": "ok"})  # no exception


@pytest.mark.parametrize(("status", "kept"), [(202, False), (404, False), (422, False),
                                               (429, True), (503, True)])
def test_what_is_kept_for_later(monkeypatch, status, kept):
    monkeypatch.setattr(update_report, "_deliver", lambda *args: status)

    update_report.submit_attempt({"schema_version": 1, "outcome": "ok"})

    pending = json.loads(update_report.pending_path().read_text())
    assert ("attempt" in pending) is kept


def test_signed_out_sends_nothing(monkeypatch, sent):
    monkeypatch.delenv("PROBE_TOKEN")
    update_report.submit_attempt({"schema_version": 1, "outcome": "ok"})
    assert sent == []
    assert "attempt" in json.loads(update_report.pending_path().read_text())


def test_a_week_old_report_is_dropped_not_sent(sent):
    update_report.queue_attempt({"schema_version": 1}, now=int(time.time()) - 8 * 24 * 3600)
    update_report.flush("https://api.test")
    assert sent == []


class _Server:
    """A local HTTP server recording what it is sent; `hang` accepts and never answers."""

    def __init__(self, *, hang: bool = False):
        self.requests: list[tuple[str, dict, dict]] = []
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802 - http.server's name
                if hang:
                    time.sleep(10)
                    return
                length = int(self.headers.get("content-length", 0))
                body = json.loads(self.rfile.read(length))
                outer.requests.append((self.path, dict(self.headers), body))
                payload = b'{"recorded": true}'
                self.send_response(202)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args):
                pass

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.httpd.daemon_threads = True
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def test_the_wire(monkeypatch):
    """The real door, end to end: route, credential, machine and version headers,
    and the queued report removed once it landed."""
    monkeypatch.setattr(update_report, "_deliver", REAL_DELIVER)
    server = _Server()
    try:
        monkeypatch.setattr(update_report.versions, "cli_version", lambda: "0.221.0")
        update_report.submit_attempt({"schema_version": 1, "outcome": "ok"}, base_url=server.url)
    finally:
        server.close()

    [(path, headers, body)] = server.requests
    headers = {k.lower(): v for k, v in headers.items()}
    assert path == update_report.ROUTE
    assert headers["authorization"] == f"Bearer {TOKEN}"
    assert headers["x-probe-client"] == "cli"
    assert headers["x-probe-client-version"] == "0.221.0"  # the INSTALLED one
    assert len(headers["x-probe-device"]) >= 16
    assert body == {"schema_version": 1, "outcome": "ok"}
    assert "attempt" not in json.loads(update_report.pending_path().read_text())


def test_the_budget_is_wall_clock_whatever_the_network_does(monkeypatch):
    """httpx bounds each step on its own (DNS not at all). A send that takes
    far longer than the budget -- here, a door that sleeps -- is abandoned at
    the deadline, and the report stays queued."""

    def _slow(base_url, headers, body, timeout):
        time.sleep(5)
        return 202

    monkeypatch.setattr(update_report, "_deliver", _slow)
    update_report.queue_attempt({"schema_version": 1, "outcome": "ok"})
    started = time.monotonic()
    update_report.flush("https://api.test", timeout=0.5)
    assert time.monotonic() - started < 1.5
    assert "attempt" in json.loads(update_report.pending_path().read_text())


def test_nothing_waiting_touches_no_machine_identity(monkeypatch, sent):
    """Reading the identity can MINT one (and write a file): never for nothing."""
    asked: list[bool] = []
    monkeypatch.setattr(update_report, "device_instance_id", lambda: asked.append(True))

    update_report.flush("https://api.test")

    assert (asked, sent) == ([], [])


def test_a_server_that_never_answers_costs_at_most_the_timeout(monkeypatch):
    monkeypatch.setattr(update_report, "_deliver", REAL_DELIVER)
    server = _Server(hang=True)
    try:
        started = time.monotonic()
        update_report.queue_attempt({"schema_version": 1, "outcome": "ok"})
        update_report.flush(server.url, timeout=0.6)
        elapsed = time.monotonic() - started
    finally:
        server.close()
    assert elapsed < 2.0
    assert "attempt" in json.loads(update_report.pending_path().read_text())


def test_a_closed_port_fails_fast(monkeypatch):
    monkeypatch.setattr(update_report, "_deliver", REAL_DELIVER)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    started = time.monotonic()
    update_report.submit_attempt({"schema_version": 1}, base_url=f"http://127.0.0.1:{port}")
    assert time.monotonic() - started < 1.0
    assert "attempt" in json.loads(update_report.pending_path().read_text())


# ---------------------------------------------------------------------------
# What the components say, case by case
# ---------------------------------------------------------------------------


def test_details_are_scrubbed_and_clipped():
    component = update_report._component(
        "1.0.0", "1.0.0", "2.0.0", update_report.Result.ERROR,
        "failed in /home/alice/.local/bin/uv " + "x" * 400,
    )
    assert "alice" not in component["detail"]
    assert len(component["detail"]) <= update_report.DETAIL_MAX_CHARS


def test_an_unparseable_version_is_sent_as_unknown():
    component = update_report._component("dev build", "1.0.0", None, update_report.Result.CURRENT)
    assert (component["before"], component["after"]) == (None, "1.0.0")


def test_a_cli_tool_missing_from_path(monkeypatch):
    """`upgrade_cli` flags it structurally; the report reads the flag, not the
    wording of the message."""
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: None)  # no `uv` at all
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    res = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.218.1", "0.221.0")
    assert res.missing_binary

    component = update_report.cli_component(res, current="0.218.1", target="0.221.0")
    assert component["result"] == "not_found_on_path"
    reworded = updater.CliResult(False, False, False, "0.218.1", "0.218.1", "no uv here",
                                 missing_binary=True)
    assert update_report.cli_component(reworded, current="0.218.1", target="0.221.0")[
        "result"
    ] == "not_found_on_path"


@pytest.mark.parametrize("step", list(update_report.PiStep))
def test_every_pi_step_has_a_result(step):
    assert step in update_report._PI_RESULTS


@pytest.mark.parametrize(
    ("home", "user", "raw", "clean"),
    [
        # A home no pattern knows: caught only by knowing it.
        ("/fsx/dave", "dave", "failed in /fsx/dave/.local/bin/uv as dave",
         "failed in ~/.local/bin/uv as <user>"),
        ("/data/users/carol", "carol", "cd /DATA/USERS/CAROL/x && whoami: carol",
         "cd ~/x && whoami: <user>"),
        # Windows: plain, Python's repr of it, forward slashes, any case.
        (r"C:\Users\Alice", "Alice", r"denied: C:\Users\Alice\AppData\uv.exe",
         r"denied: ~\AppData\uv.exe"),
        (r"C:\Users\Alice", "Alice", "OSError: 'C:\\\\Users\\\\Alice\\\\uv.exe'",
         "OSError: '~\\\\uv.exe'"),
        (r"C:\Users\Alice", "Alice", r"c:\users\alice\x and C:/Users/Alice/y",
         r"~\x and ~/y"),
        # Someone else's Windows home in the output: the pattern backstop.
        ("/home/me", "me", r"from C:\Users\bob\x", r"from ~\x"),
        # A two-letter login is left alone rather than eating every `uv`.
        ("/home/uv", "uv", "`uv` not found", "`uv` not found"),
    ],
)
def test_details_lose_this_machines_home_and_login(monkeypatch, home, user, raw, clean):
    monkeypatch.setattr(update_report, "_home_and_user", lambda: (home, user))
    assert update_report._detail(raw) == clean


def test_legacy_ids_outside_the_servers_shape_are_left_out(tmp_path):
    _ledger(tmp_path / "home", {
        "prbe-cc-tap-plugin@prbe-ai": "0.9.3",
        "probe-research-tap@My Marketplace": "0.9.3",
        "someone-elses-plugin@x": "1.0.0",
    })
    assert updater.legacy_plugin_ids() == ("prbe-cc-tap-plugin@prbe-ai",)


def test_the_spawned_updater_says_what_asked(monkeypatch):
    import importlib

    cli_main = importlib.import_module("probe.cli.main")
    spawned: list[dict] = []
    monkeypatch.setattr(cli_main, "_spawn_detached", lambda argv, env: spawned.append(env))

    cli_main._spawn_update("--apply")
    cli_main._spawn_update("--apply-if-newer", harness_pid=4242)

    assert [env[autoupdate.TRIGGER_ENV] for env in spawned] == ["cli", "session_start"]


@pytest.mark.parametrize(("value", "expected"), [("cli", "cli"), ("session_start", "session_start"),
                                                  ("", "manual"), ("bogus", "manual")])
def test_trigger_from_env(monkeypatch, value, expected):
    monkeypatch.setenv(autoupdate.TRIGGER_ENV, value)
    assert update_report.trigger_from_env(update_report.Trigger.MANUAL).value == expected


@pytest.mark.parametrize(
    ("agent", "argv", "expected"),
    [
        ("pi", ["probe", "session", "initialize"], "session_start"),
        ("pi", ["probe", "log", "loss=1"], "cli"),
        (None, ["probe", "session", "initialize"], "cli"),
    ],
)
def test_a_skip_at_pis_session_start_says_so(monkeypatch, agent, argv, expected):
    import importlib
    import sys

    cli_main = importlib.import_module("probe.cli.main")
    if agent:
        monkeypatch.setenv("PROBE_AGENT", agent)
    monkeypatch.setattr(sys, "argv", argv)
    assert cli_main._update_trigger() == expected
