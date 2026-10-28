"""`probe.core` and `python -m probe.core.run`: one facade, the same runs as the CLI.

The Probe service runs every action as a `probe.core.run` child and reads its
stdout; the desktop app runs `probe wizard --action <a> --yes --json` today.
They must be the same run: the same events, the same side effects, the same
exit status. So each parity test runs BOTH as real processes on the same fake
device, each in a home of its own, and compares what they wrote.

Real boundaries: the processes, their stdout/stderr/exit status, the config
and state files. Stood in for (inside each child, `FAKE_DEVICE`): the coding
agents' own CLIs (plugin installs), the browser approval's mint and the
server's registration -- exactly what `test_wizard_json_events.device` stands in
for, nothing the wizard decides.
"""

from __future__ import annotations

import importlib
import inspect
import json
import os
import signal
import errno
import socket
import subprocess
import sys
import textwrap
import threading
import time
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from typer.testing import CliRunner

import probe.core
from probe.core import actions, events, requests
from probe.core.requests import (
    ActionName,
    Agent,
    ConfigureRequest,
    Recorder,
    RecorderRequest,
    RequestError,
    SessionDefaultRequest,
    SessionState,
)
from tests import test_wizard_json_events as wizard_json
from tests.test_wizard_json_signals import _ApprovalNeverComes
from tests.test_wizard_lock import HOLDER

main = importlib.import_module("probe.cli.main")
device = wizard_json.device

#: A child process on a fake device: `cli ARGV...` runs `probe ARGV...`, and
#: `core ACTION` runs `python -m probe.core.run ACTION` (stdin passed through).
#: $FAKES (comma-separated) adds: `signed_in` (a saved login), `noisy_update`
#: (an update that prints every way a run can, a child writing to fd 1 included),
#: `aborted_update` (one that raises typer.Abort), `real_approval` (the browser
#: approval goes to $PROBE_BASE_URL instead of the stand-in).
FAKE_DEVICE = textwrap.dedent(
    """
    import importlib, os, subprocess, sys
    import typer
    from probe.cli import bootstrap, doctor, outbox_worker, setup, upgrading
    from probe.cli import capabilities
    from probe.cli.capabilities import Capabilities, capture_token_sources
    from probe.sdk import device as device_flow
    from probe.sdk.config import resolve, save_context
    from probe.sdk.device import DevicePrompt

    main = importlib.import_module("probe.cli.main")
    fakes = set(filter(None, os.environ.get("FAKES", "").split(",")))
    installed = set()
    PROMPT = DevicePrompt(
        user_code="WDJB-MJHT",
        verification_uri="https://app.test/device",
        verification_uri_complete="https://app.test/device?code=WDJB-MJHT",
    )

    bootstrap.ensure_persistent_install = lambda **_: bootstrap.BootstrapResult(
        installed=False, already_persistent=True, message=""
    )
    main._version_notice = lambda: None
    main._outbox_notice = lambda **_: None
    setup.detectable_sources = lambda: ("claude_code", "codex")
    setup.refresh_marketplace = lambda **_: None
    setup._record_login_account = lambda *a, **k: None
    capabilities.verify_mcp_credential = lambda **_: True
    outbox_worker.maybe_spawn = lambda *a, **k: None

    def device_authorize(base_url, *, grants=None, capture_source=None, capture_sources=None,
                         on_prompt=None, **_):
        if on_prompt is not None:
            on_prompt(PROMPT)
        sources = capture_sources or ([capture_source] if capture_source else [])
        minted = [{"grant": grant, "token": f"probe_pat_{grant}"} for grant in grants if grant != "capture"]
        if "capture" in grants:
            minted += [
                {"grant": "capture", "capture_source": source, "token": f"ros_ing_{source}"}
                for source in sources
            ]
        return {"grants": minted}

    if "real_approval" not in fakes:
        device_flow.device_authorize = device_authorize

    def collect():
        source = os.environ.get("PROBE_AGENT", "claude_code")
        settings = resolve()
        paired = capture_token_sources(source)
        return Capabilities(
            agent_source=source,
            claude_available=True,
            codex_available=True,
            logged_in_as="researcher@example.test" if settings.token else None,
            api_credential_valid=True if settings.token else None,
            mcp_token_held=bool(settings.mcp_token),
            tracking_plugin_installed=(source, "tracking") in installed,
            capture_plugin_installed=(source, "capture") in installed,
            capture_token_sources=paired,
            capture_credential_valid=True if paired else None,
            mcp_authenticated=True,
            auto_update_enabled=(source, "updates") in installed,
            agent_rules_installed=(source, "rules") in installed,
        )

    def applied(kind):
        def apply(*_a, **_k):
            installed.add((os.environ["PROBE_AGENT"], kind))
            return [f"{kind} applied."]
        return apply

    doctor.collect = collect
    setup.apply_tracking = applied("tracking")
    setup.apply_capture = applied("capture")
    setup.apply_auto_update = applied("updates")
    setup.apply_agent_rules = applied("rules")
    main._register_local_capabilities = lambda caps, **_: []

    if "signed_in" in fakes:
        save_context({"token": "probe_pat_api", "mcp_token": "probe_pat_mcp"})

    def noisy_update(**_):
        print("print noise")
        typer.echo("echo noise")
        subprocess.run(
            [sys.executable, "-c", "import os; print('child noise', flush=True); os.write(1, b'raw fd noise\\\\n')"],
            check=True,
        )
        return upgrading.UpdateOutcome(lines=["Updated."], ok=True, restart_needed=False)

    def aborted_update(**_):
        raise typer.Abort()

    if "noisy_update" in fakes:
        upgrading.perform_update = noisy_update
        upgrading.perform_updates = lambda sources, **kw: {source: noisy_update(**kw) for source in sources}
    if "aborted_update" in fakes:
        upgrading.perform_update = aborted_update
        upgrading.perform_updates = lambda sources, **kw: aborted_update(**kw)

    mode, args = sys.argv[1], sys.argv[2:]
    if mode == "cli":
        from probe.cli import main as probe_entry
        raise SystemExit(probe_entry(args))
    from probe.core import run
    raise SystemExit(run.main(args))
    """
)

#: What the desktop app runs today for each request (`src-tauri/src/wizard.rs`
#: `WizardRequest::argv`), and the `probe.core` request that means the same.
APP_RUNS = {
    "configure": (
        ConfigureRequest(
            agents=(Agent.CLAUDE, Agent.CODEX, Agent.PI), tracking=True, capture=True, auto_update=True,
            agent_rules=True,
        ),
        ["wizard", "--action", "configure", "--yes", "--json", "--tracking", "--capture", "--auto-update",
         "--agent-rules", "--agent", "claude", "--agent", "codex", "--agent", "pi"],
    ),
    "configure-no-capture": (
        ConfigureRequest(agents=(Agent.CLAUDE,), tracking=True, capture=False, auto_update=True, agent_rules=False),
        ["wizard", "--action", "configure", "--yes", "--json", "--tracking", "--no-capture", "--auto-update",
         "--no-agent-rules", "--agent", "claude"],
    ),
    "recorder-daemon": (
        RecorderRequest(Recorder.DAEMON),
        ["wizard", "--action", "recorder", "--who-records", "daemon", "--yes", "--json"],
    ),
    "recorder-agent": (
        RecorderRequest(Recorder.AGENT),
        ["wizard", "--action", "recorder", "--who-records", "agent", "--yes", "--json"],
    ),
    "logout": (None, ["wizard", "--action", "logout", "--yes", "--json"]),
    "uninstall": (None, ["wizard", "--action", "uninstall", "--yes", "--json"]),
    "update": (None, ["wizard", "--action", "update", "--yes", "--json"]),
}


def _core_call(name: str, request, sink):
    action = name.split("-")[0]
    if action in ("configure", "recorder"):
        return getattr(probe.core, action)(request, sink)
    return getattr(probe.core, action)(sink)


# -- running both sides --------------------------------------------------------


def _side_env(tmp_path: Path, side: str, fakes: tuple[str, ...] = (), **extra: str) -> dict[str, str]:
    """The suite's isolated environment, with this side's own home, config and
    state: two runs in one test never share a file."""
    root = tmp_path / side
    for name in ("home", "config", "state", "empty-path", "tmp"):
        (root / name).mkdir(parents=True, exist_ok=True)
    # As `test_wizard_json_events.device`: a token exported where the suite runs
    # would sign both sides in, and a daemon recorder run would then install.
    inherited = {
        name: value for name, value in os.environ.items()
        if name not in ("PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_INGEST_TOKEN")
    }
    return {
        **inherited,
        "PATH": str(root / "empty-path"),
        "HOME": str(root / "home"),
        "XDG_CONFIG_HOME": str(root / "config"),
        "XDG_STATE_HOME": str(root / "state"),
        # Its own TMPDIR too: an uninstall removes Probe's $TMPDIR outboxes.
        "TMPDIR": str(root / "tmp"),
        "PROBE_CONFIG_PATH": str(root / "config.json"),
        "PROBE_BASE_URL": "http://127.0.0.1:9",
        "FAKES": ",".join(fakes),
        **extra,
    }


#: The real entry points, with nothing stood in for: `probe` and the runner.
BARE = {"cli": ["-m", "probe.cli"], "core": ["-m", "probe.core.run"]}


def _child(tmp_path: Path, side: str, mode: str, args: list[str], *, stdin: str = "",
           fakes: tuple[str, ...] = (), bare: bool = False, **extra: str) -> subprocess.CompletedProcess:
    """`mode` (cli | core) in a child on this side's own files: on the fake
    device, or `bare` for a read or a write that needs nothing stood in for."""
    entry = BARE[mode] if bare else ["-c", FAKE_DEVICE, mode]
    result = subprocess.run(
        [sys.executable, *entry, *args],
        env=_side_env(tmp_path, side, fakes, **extra), input=stdin, capture_output=True, text=True,
        timeout=120,
    )
    # The side's own paths read the same on both sides.
    root = str(tmp_path / side)
    result.stdout = result.stdout.replace(root, "<side>")
    return result


def _events(stdout: str) -> list[dict]:
    return [json.loads(line) for line in stdout.splitlines()]


def _both(tmp_path: Path, name: str, *, fakes: tuple[str, ...] = (), **extra: str):
    """The app's CLI run and the `probe.core.run` run of the same request."""
    request, argv = APP_RUNS[name]
    stdin = json.dumps(_params(request))
    cli = _child(tmp_path, "cli", "cli", argv, fakes=fakes, **extra)
    core = _child(tmp_path, "core", "core", [name.split("-")[0]], stdin=stdin, fakes=fakes, **extra)
    return cli, core


def _params(request) -> dict:
    if isinstance(request, ConfigureRequest):
        named = {
            "tracking": request.tracking, "capture": request.capture, "auto_update": request.auto_update,
            "agent_rules": request.agent_rules,
        }
        return {
            "agents": [agent.value for agent in request.agents],
            **{name: value for name, value in named.items() if value is not None},
        }
    if isinstance(request, RecorderRequest):
        return {"who_records": request.who_records.value}
    return {}


def _assert_same_run(cli: subprocess.CompletedProcess, core: subprocess.CompletedProcess) -> None:
    assert _events(cli.stdout), cli.stderr
    assert (core.returncode, _events(core.stdout)) == (cli.returncode, _events(cli.stdout)), core.stderr


# -- parity: the same run as `probe wizard --action <a> --yes --json` ----------


@pytest.mark.parametrize("name", ["configure", "configure-no-capture"])
def test_configure_is_the_same_run_as_the_apps_wizard_command(tmp_path, name):
    """Every agent the app offers, one approval; and a run that turns two off."""
    _assert_same_run(*_both(tmp_path, name))


def test_a_configure_that_did_everything_ends_complete(tmp_path):
    """The control for the parity above: it compared a run that did the work."""
    _, core = _both(tmp_path, "configure-no-capture")
    done = _events(core.stdout)[-1]
    assert (done["event"], done["ok"], done["complete"]) == ("done", True, True), core.stderr


@pytest.mark.parametrize("name", ["recorder-agent", "recorder-daemon"])
def test_recorder_is_the_same_run_as_the_apps_wizard_command(tmp_path, name):
    """`agent` where every agent already is; `daemon` on a machine not signed in."""
    _assert_same_run(*_both(tmp_path, name))


class _RevokesTokens(BaseHTTPRequestHandler):
    """A Probe server that releases a token (`DELETE /v1/tokens/current`) and
    answers nothing else: the device-state call falls back, as offline."""

    seen: list[str]

    def log_message(self, *_args):
        pass

    def _answer(self, status: int) -> None:
        self.seen.append(f"{self.command} {self.path.split('?')[0]}")
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_DELETE(self):  # noqa: N802 - http.server's name
        self._answer(204 if self.path.startswith("/v1/tokens/current") else 404)

    def do_GET(self):  # noqa: N802
        self._answer(404)

    def do_POST(self):  # noqa: N802
        self.rfile.read(int(self.headers.get("Content-Length") or 0))
        self._answer(404)


def test_logout_is_the_same_run_as_the_apps_wizard_command(tmp_path):
    handler = type("Handler", (_RevokesTokens,), {"seen": []})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        cli, core = _both(
            tmp_path, "logout", fakes=("signed_in",), PROBE_BASE_URL=f"http://127.0.0.1:{server.server_port}"
        )
    finally:
        server.shutdown()
    _assert_same_run(cli, core)
    # Both released the API and MCP tokens on the server ...
    assert handler.seen.count("DELETE /v1/tokens/current") == 4, handler.seen
    # ... and signed the device out.
    for side in ("cli", "core"):
        saved = json.loads((tmp_path / side / "config.json").read_text())
        assert all(not context.get("token") for context in saved["contexts"].values()), side


def test_update_is_the_same_run_as_the_apps_wizard_command(tmp_path):
    _assert_same_run(*_both(tmp_path, "update", fakes=("noisy_update",)))


@pytest.mark.heavy
def test_uninstall_is_the_same_run_as_the_apps_wizard_command(tmp_path):
    _assert_same_run(*_both(tmp_path, "uninstall", fakes=("signed_in",)))


def test_status_is_byte_for_byte_probe_status_json(tmp_path):
    cli = _child(tmp_path, "cli", "cli", ["status", "--json"], bare=True)
    core = _child(tmp_path, "core", "core", ["status"], bare=True)
    assert (core.returncode, core.stdout) == (cli.returncode, cli.stdout)
    assert json.loads(core.stdout)["v"] == 1


def test_status_with_refresh_is_probe_status_json_refresh(tmp_path):
    cli = _child(tmp_path, "cli", "cli", ["status", "--json", "--refresh", "--timeout", "2"], bare=True)
    core = _child(tmp_path, "core", "core", ["status"], stdin='{"refresh": true}', bare=True)
    assert (json.loads(core.stdout)["refreshed"], core.returncode) == (json.loads(cli.stdout)["refreshed"], 0)


def test_version_is_what_a_fresh_process_imports(tmp_path):
    """`probe.core.run version`: the Probe service asks it after an update,
    because its own `probe.__version__` is the one it started with."""
    import probe

    core = _child(tmp_path, "core", "core", ["version"], bare=True)
    assert core.returncode == 0, core.stderr
    answer = json.loads(core.stdout)
    assert answer["cli_version"] == probe.__version__
    # The newest release, when the manifest says (the service asks before it
    # stops daemon workers for an update, D7); unknown here.
    assert set(answer) == {"cli_version", "cli_latest"}
    refused = _child(tmp_path, "core", "core", ["version"], stdin='{"x": 1}', bare=True)
    assert refused.returncode == 2


@pytest.mark.parametrize("stdin", [
    '{"op": "analytics_policy"}', '{"op": "shell"}', '{"op": "jobs", "extra": 1}', '{"op": "jobs", "op": "jobs"}',
    "not json", "", '{"op": "set_capture", "source": "pi", "enabled": false}',
], ids=["ok", "unknown-op", "unknown-field", "repeated-field", "not-json", "empty", "unsupported"])
def test_desktop_is_byte_for_byte_probe_desktop_request(tmp_path, stdin):
    """`probe.core.run desktop`: the Probe service's `desktop.request` child.
    The same envelope and exit status as the command the app runs today."""
    cli = _child(tmp_path, "cli", "cli", ["desktop", "request", "--json"], stdin=stdin, bare=True)
    core = _child(tmp_path, "core", "core", ["desktop"], stdin=stdin, bare=True)
    assert (core.returncode, core.stdout) == (cli.returncode, cli.stdout), core.stderr
    envelope = json.loads(core.stdout)
    assert envelope["v"] == 1 and isinstance(envelope["ok"], bool)


def test_desktop_waits_out_an_update_barrier_then_answers_busy(monkeypatch, capfd):
    """As `probe` itself (`probe._entry`): nothing is imported from files an
    update is replacing; the app reads the busy envelope and asks again."""
    import io

    from probe.core import run
    from probe.service import barrier

    monkeypatch.setattr(barrier, "wait", lambda timeout=None: False)
    assert run.main(["desktop"], stdin=io.StringIO('{"op": "jobs"}')) == barrier.BUSY_EXIT_CODE == 75
    out, _ = capfd.readouterr()
    assert json.loads(out) == {"v": 1, "ok": False, "error": f"{barrier.MESSAGE}."}


def test_desktop_refuses_what_the_cli_refuses_in_a_daemon_session(monkeypatch, capfd):
    """Codex P1: the entry point applies the CLI's own gate (`write_gate`), so
    a session the daemon records cannot reach a backfill, a job change or the
    onboarding acknowledgement through it, registered with the service or not."""
    import io

    from probe.cli import desktop, write_gate
    from probe.core import run
    from probe.sdk import session_marker

    session_marker.mark_session_profile(AGENT_SESSION, session_marker.RECORDER_DAEMON)
    session_marker.set_session_state(AGENT_SESSION, session_marker.STATE_DAEMON)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", AGENT_SESSION)
    monkeypatch.setattr(desktop, "dispatch", lambda request: pytest.fail(f"ran {request}"))
    expected = write_gate.refusal(["desktop", "request", "--json"], directed=False)
    assert expected and "probe desktop" in expected
    code = run.main(["desktop"], stdin=io.StringIO('{"op": "onboarding_complete", "userId": "u", "customerId": "c"}'))
    out, err = capfd.readouterr()
    assert (code, json.loads(out)) == (write_gate.EXIT_REFUSED, {"v": 1, "ok": False, "error": expected})
    assert expected in err


def test_desktop_stdout_is_the_envelope_alone(monkeypatch, capfd):
    """What a request's code prints goes to stderr: the reader parses stdout whole."""
    import io

    from probe.cli import desktop
    from probe.core import run

    def noisy(request):
        print("a library said hello")
        return {"seen": request}

    monkeypatch.setattr(desktop, "dispatch", noisy)
    assert run.main(["desktop"], stdin=io.StringIO('{"op": "jobs"}')) == 0
    out, err = capfd.readouterr()
    assert json.loads(out) == {"v": 1, "ok": True, "data": {"seen": {"op": "jobs"}}}
    assert out.count("\n") == 1 and "a library said hello" in err


#: `probe status` for a person, on a fresh device: captured from origin/main
#: (cd807ea4b) with this same environment. Its read now goes through
#: `probe.core.reads`; what it prints did not change. The CLI's version and
#: install method move every release, so they read `<cli>`. One line added on
#: purpose since: the Probe service's own view (`service_calls.summary`).
GOLDEN_STATUS = (
    "Probe CLI          <cli>\n"
    "Account            not signed in · default · http://127.0.0.1:9\n"
    "Who records        agent\n"
    "New sessions       on\n"
    "Automatic updates  off\n"
    "Versions           unknown\n"
    "Setup running      no\n"
    "Probe service      not running (it starts with the next coding-agent session, or run `probe service start`)\n"
    "Coding agents      none found on this device\n"
)


def test_probe_status_for_a_person_prints_exactly_what_it_printed_before(tmp_path):
    result = _child(tmp_path, "cli", "cli", ["status"], bare=True)
    lines = result.stdout.splitlines(keepends=True)
    assert lines[0].startswith("Probe CLI          "), result.stdout
    assert (result.returncode, "".join(["Probe CLI          <cli>\n", *lines[1:]])) == (0, GOLDEN_STATUS)


@pytest.mark.parametrize("state", list(SessionState))
def test_session_default_writes_what_probe_session_default_writes(tmp_path, state):
    cli = _child(tmp_path, "cli", "cli", ["session", "default", state.value], bare=True)
    core = _child(tmp_path, "core", "core", ["session_default"], stdin=json.dumps({"state": state.value}), bare=True)
    assert (core.returncode, cli.returncode) == (0, 0), core.stderr
    assert (tmp_path / "core" / "config.json").read_text() == (tmp_path / "cli" / "config.json").read_text()


def test_session_default_reports_the_state_it_set(tmp_path):
    core = _child(tmp_path, "core", "core", ["session_default"], stdin='{"state": "off"}', bare=True)
    events_out = _events(core.stdout)
    row = events_out[-2]["agents"][0]
    assert (row["requested"], row["actual"], row["ok"], events_out[-1]["complete"]) == (
        {"session_default": "off"}, {"session_default": "off"}, True, True,
    )


def test_session_default_status_reads_back_what_it_set(tmp_path):
    """Set through one door, read through the other: the app's two calls."""
    _child(tmp_path, "core", "core", ["session_default"], stdin='{"state": "read"}', bare=True)
    status = _child(tmp_path, "core", "core", ["status"], bare=True)
    assert json.loads(status.stdout)["session_default"]["state"] == "read"


AGENT_SESSION = "0b6f2c1e-5a8d-4d9e-9f3a-2c7b1e4d6a90"


def test_an_agent_the_daemon_records_cannot_move_the_default_through_either_door(tmp_path, monkeypatch):
    """The researcher's switch: `probe session default` refuses it from inside a
    session the Probe daemon records, however the call is wrapped, and the
    runner is one more wrapper. Both exit 2 and write nothing."""
    from probe.sdk import session_marker

    runs = {}
    for side, mode, args, stdin in (
        ("cli", "cli", ["session", "default", "off"], ""),
        ("core", "core", ["session_default"], '{"state": "off"}'),
    ):
        # The lean plugin's mark, in this side's state dir.
        monkeypatch.setenv("XDG_STATE_HOME", _side_env(tmp_path, side)["XDG_STATE_HOME"])
        session_marker.mark_session_profile(AGENT_SESSION, session_marker.RECORDER_DAEMON)
        assert session_marker.session_profile(AGENT_SESSION) == session_marker.RECORDER_DAEMON
        monkeypatch.delenv("XDG_STATE_HOME")
        runs[side] = _child(tmp_path, side, mode, args, stdin=stdin, bare=True, CLAUDE_CODE_SESSION_ID=AGENT_SESSION)
    assert [(runs[side].returncode, (tmp_path / side / "config.json").exists()) for side in runs] == [
        (2, False), (2, False),
    ], runs["core"].stderr
    row = _events(runs["core"].stdout)[-2]["agents"][0]
    assert (row["ok"], "moves the researcher's Probe switch" in row["message"]) == (False, True)


#: Each wizard action's request, for the refusal below.
WIZARD_ACTION_REQUESTS = {
    "configure": '{"agents": ["claude"], "capture": false}',
    "recorder": '{"who_records": "agent"}',
    "logout": "",
    "uninstall": "",
    "update": "",
}


@pytest.mark.parametrize("action", sorted(WIZARD_ACTION_REQUESTS))
def test_an_agent_the_daemon_records_cannot_run_a_wizard_action_through_the_runner(tmp_path, monkeypatch, action):
    """The daemon profile's guard refuses `probe wizard` (typed, or as `python
    -m probe.cli`) from inside a session the Probe daemon records. The runner is
    one more way to run the same actions, and no guard copy knows its name, so
    it refuses them itself, however it was wrapped: exit 2, nothing changed."""
    from probe.sdk import session_marker

    monkeypatch.setenv("XDG_STATE_HOME", _side_env(tmp_path, "core")["XDG_STATE_HOME"])
    session_marker.mark_session_profile(AGENT_SESSION, session_marker.RECORDER_DAEMON)
    result = _child(
        tmp_path, "core", "core", [action], stdin=WIZARD_ACTION_REQUESTS[action], fakes=("signed_in", "noisy_update"),
        CLAUDE_CODE_SESSION_ID=AGENT_SESSION,
    )
    out = _events(result.stdout)
    assert (result.returncode, [(e["event"], e.get("code")) for e in out]) == (
        2, [("error", "usage"), ("done", None)],
    ), result.stderr
    assert "The Probe daemon records this session" in out[0]["message"]
    # Still signed in, and nothing it ran says otherwise: the run stopped first.
    saved = json.loads((tmp_path / "core" / "config.json").read_text())
    assert (saved["contexts"]["default"]["token"], "Updated." in result.stderr) == ("probe_pat_api", False)


def test_a_session_the_daemon_does_not_record_runs_a_wizard_action(tmp_path):
    """The control for the refusal above: the same session id, unmarked."""
    result = _child(
        tmp_path, "core", "core", ["update"], fakes=("noisy_update",), CLAUDE_CODE_SESSION_ID=AGENT_SESSION,
    )
    assert (result.returncode, _events(result.stdout)[-1]["ok"]) == (0, True), result.stderr


def test_session_default_daemon_is_refused_as_probe_session_default_refuses_it(tmp_path):
    cli = _child(tmp_path, "cli", "cli", ["session", "default", "daemon"], bare=True)
    core = _child(tmp_path, "core", "core", ["session_default"], stdin='{"state": "daemon"}', bare=True)
    assert (core.returncode, cli.returncode, (tmp_path / "core" / "config.json").exists()) == (2, 2, False)


# -- the runner's own contract ---------------------------------------------------


@pytest.fixture
def noisy_core_update(tmp_path):
    return _child(tmp_path, "core", "core", ["update"], fakes=("noisy_update",))


def test_every_stdout_line_of_a_core_run_is_one_json_event(noisy_core_update):
    assert noisy_core_update.stdout.strip(), noisy_core_update.stderr
    assert all(json.loads(line)["v"] == 1 for line in noisy_core_update.stdout.splitlines())


def test_what_a_core_run_and_its_child_print_reaches_stderr(noisy_core_update):
    for noise in ("print noise", "echo noise", "child noise", "raw fd noise"):
        assert noise in noisy_core_update.stderr, noise


def test_done_is_the_last_line_of_a_core_run(noisy_core_update):
    assert (_events(noisy_core_update.stdout)[-1]["event"], noisy_core_update.returncode) == ("done", 0)


@pytest.mark.parametrize(
    ("args", "stdin"),
    [
        (["install"], ""),  # not an action
        ([], ""),
        (["configure", "logout"], ""),
        (["--help"], ""),
        (["configure"], "{not json"),
        (["configure"], "[]"),
        (["configure"], '{"agents": []}'),
        (["configure"], '{"agents": ["claude"], "captur": false}'),  # a typo must not turn capture on
        (["configure"], '{"agents": ["claude"], "capture": 0}'),
        (["configure"], '{"agents": ["not_a_registered_agent"]}'),
        (["recorder"], "{}"),
        (["recorder"], '{"who_records": "both"}'),
        (["session_default"], '{"state": "inline"}'),
        (["logout"], '{"yes": true}'),
        (["status"], '{"refresh": "yes"}'),
        # `json.loads` keeps the last of a repeated key: this would turn capture on.
        (["configure"], '{"agents": ["claude"], "capture": false, "capture": true}'),
        pytest.param(["logout"], "[" * 100_000 + "]" * 100_000, id="nested-deeper-than-the-decoder-recurses"),
    ],
)
def test_a_refused_request_is_a_usage_error_that_changes_nothing(tmp_path, args, stdin):
    result = _child(tmp_path, "core", "core", args, stdin=stdin, bare=True)
    out = _events(result.stdout)
    assert (result.returncode, [(e["event"], e.get("code")) for e in out], out[-1]["exit_code"]) == (
        2, [("error", "usage"), ("done", None)], 2,
    ), result.stderr
    assert not (tmp_path / "core" / "config.json").exists()


def test_an_empty_stdin_is_an_empty_request(tmp_path):
    result = _child(tmp_path, "core", "core", ["session_default"], stdin="", bare=True)
    assert "state is required" in _events(result.stdout)[0]["message"]


def test_a_request_that_is_not_utf8_is_a_usage_error_in_any_locale(tmp_path):
    """JSON is UTF-8 whatever the locale says. A strict stdin (a person's own
    `en_US.UTF-8`, here forced) raised UnicodeDecodeError: no events at all."""
    result = subprocess.run(
        [sys.executable, "-m", "probe.core.run", "logout"], input=b"\xff\xfe{}",
        env=_side_env(tmp_path, "core", PYTHONIOENCODING="utf-8:strict"), capture_output=True, timeout=120,
    )
    out = _events(result.stdout.decode())
    assert (result.returncode, [(e["event"], e.get("code")) for e in out]) == (
        2, [("error", "usage"), ("done", None)],
    ), result.stderr


def test_an_aborted_core_run_exits_1_as_failed(tmp_path):
    cli, core = _both(tmp_path, "update", fakes=("aborted_update",))
    _assert_same_run(cli, core)
    assert (core.returncode, _events(core.stdout)[-1]["exit_code"]) == (1, 1)


def test_a_core_run_while_another_setup_runs_exits_75_and_changes_nothing(tmp_path):
    env = _side_env(tmp_path, "core")
    marker = tmp_path / "held"
    holder = subprocess.Popen([sys.executable, "-c", HOLDER, str(marker)], env=env)
    try:
        deadline = time.monotonic() + 60
        while not marker.exists():
            assert holder.poll() is None and time.monotonic() < deadline
            time.sleep(0.02)
        result = _child(tmp_path, "core", "core", ["logout"], fakes=("signed_in",))
    finally:
        holder.kill()
        holder.wait(timeout=30)
    out = _events(result.stdout)
    assert (result.returncode, out[0]["code"], out[-1]["exit_code"]) == (75, "busy", 75), result.stderr
    saved = json.loads((tmp_path / "core" / "config.json").read_text())
    assert saved["contexts"]["default"]["token"] == "probe_pat_api"


@pytest.fixture
def signalled_during_core_approval(tmp_path, request):
    """`probe.core.run configure` sent a signal once its approval link is out:
    SIGINT is the app's Cancel, SIGTERM what stops a child. The server never
    approves."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ApprovalNeverComes)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    env = _side_env(tmp_path, "core", ("real_approval",), PROBE_BASE_URL=f"http://127.0.0.1:{server.server_port}")
    child = subprocess.Popen(
        [sys.executable, "-c", FAKE_DEVICE, "core", "configure"],
        env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
    )
    child.stdin.write('{"agents": ["claude"]}')
    child.stdin.close()
    out: list[dict] = []
    watchdog = threading.Timer(60, child.kill)  # a SIGINT that does not stop it polls for minutes
    watchdog.start()
    try:
        for line in child.stdout:
            out.append(json.loads(line))
            if out[-1]["event"] == "device_prompt":
                time.sleep(0.3)  # into the poll loop
                child.send_signal(request.param)
        child.wait(timeout=60)
    finally:
        watchdog.cancel()
        child.kill()
        server.shutdown()
    return child.returncode, out


@pytest.mark.parametrize("signalled_during_core_approval", [signal.SIGINT], indirect=True)
def test_sigint_during_a_core_approval_exits_130_interrupted(signalled_during_core_approval):
    code, out = signalled_during_core_approval
    assert (code, [(e["event"], e.get("code")) for e in out[-3:]], out[-1]["exit_code"]) == (
        130, [("error", "interrupted"), ("result", None), ("done", None)], 130,
    )


@pytest.mark.parametrize("signalled_during_core_approval", [signal.SIGTERM], indirect=True)
def test_sigterm_during_a_core_approval_ends_with_done_and_exit_143(signalled_during_core_approval):
    """What a parent stopping the child sees, as `probe wizard --json` gives it."""
    code, out = signalled_during_core_approval
    error = [e for e in out if e["event"] == "error"][-1]
    assert (code, out[-1]["event"], out[-1]["exit_code"], error["code"], error["message"]) == (
        143, "done", 143, "interrupted", "stopped by SIGTERM",
    )


# -- in process: the sink gets the wire's events ---------------------------------


def test_an_in_process_sink_gets_exactly_what_the_wire_carries(tmp_path):
    got: list[dict] = []
    assert probe.core.session_default(SessionState.READ, got.append) == 0
    wire = _child(tmp_path, "core", "core", ["session_default"], stdin='{"state": "read"}', bare=True)
    assert got == _events(wire.stdout)


def test_an_in_process_sink_leaves_stdout_alone(capfd):
    probe.core.session_default("on", lambda _event: None)
    out, err = capfd.readouterr()
    assert (out, '"machine_default":"on"' in err) == ("", True)


def test_a_sink_that_raises_loses_the_events_never_the_run():
    def broken(_event):
        raise RuntimeError("reader went away")

    assert probe.core.session_default("off", broken) == 0
    from probe.sdk import session_marker

    assert session_marker.default_session_state() == session_marker.STATE_OFF


def test_status_in_process_is_probe_status_json():
    result = CliRunner().invoke(main.app, ["status", "--json"])
    assert probe.core.status() == json.loads(result.stdout)


# -- the request is the app's command, flag for flag ------------------------------


@pytest.mark.parametrize("name", sorted(n for n in APP_RUNS if n != "uninstall"))
def test_a_core_action_reaches_the_wizard_with_the_apps_flags(device, monkeypatch, name):
    """What `probe wizard` hands its session for the app's command line, and for
    the `probe.core` request: the same, every argument."""
    request, argv = APP_RUNS[name]
    seen: list[dict] = []
    monkeypatch.setattr(main, "_wizard_session", lambda **kw: seen.append(kw))
    cli = CliRunner().invoke(main.app, argv)
    assert _core_call(name, request, lambda _event: None) == 0
    assert (cli.exit_code, len(seen), seen[0]) == (0, 2, seen[1]), cli.output


def test_the_core_uninstall_is_the_apps_probe_uninstall(device, monkeypatch):
    """Uninstall is never the wizard's session: `probe uninstall` (one
    implementation) from the app's command and from `probe.core` alike."""
    request, argv = APP_RUNS["uninstall"]
    seen: list[dict] = []
    monkeypatch.setattr(main, "_run_uninstall", lambda **kw: seen.append(kw) or 0)
    monkeypatch.setattr(main, "_wizard_session", lambda **kw: pytest.fail("uninstall reached the wizard session"))
    cli = CliRunner().invoke(main.app, argv)
    assert _core_call("uninstall", request, lambda _event: None) == 0
    assert (cli.exit_code, len(seen), seen[0]) == (0, 2, seen[1]), cli.output
    assert seen[0] == {"yes": True, "json_output": True}


def test_the_facade_names_every_wizard_parameter():
    """Called as a function, an unnamed one would be a truthy `typer.Option`."""
    assert set(actions.WIZARD_DEFAULTS) == set(inspect.signature(main.wizard).parameters)


def test_an_omitted_capability_reaches_the_wizard_as_an_omitted_flag(device, monkeypatch):
    """`probe wizard --yes` reads an omitted flag as "keep what this device has"
    (fresh: `setup.FRESH_DEFAULTS`; `setup.resolve_selection`), so no request can
    turn on a capture someone turned off by leaving it out. A capability the
    request leaves out is one the wizard is not handed."""
    seen: list[dict] = []
    monkeypatch.setattr(main, "_wizard_session", lambda **kw: seen.append(kw))
    cli = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--json", "--agent", "claude"])
    assert probe.core.configure(ConfigureRequest(agents=(Agent.CLAUDE,)), lambda _event: None) == 0
    assert (cli.exit_code, len(seen), seen[0]) == (0, 2, seen[1]), cli.output
    assert [seen[1][name] for name in ("tracking", "capture", "auto_update", "agent_rules")] == [None] * 4


def test_a_configure_that_leaves_capture_out_keeps_it_off(device):
    off = ConfigureRequest(agents=(Agent.CLAUDE,), tracking=True, capture=False, auto_update=True, agent_rules=True)
    assert probe.core.configure(off, lambda _event: None) == 0
    assert ("claude_code", "capture") not in device.installed  # the control: it is off
    assert probe.core.configure(ConfigureRequest(agents=(Agent.CLAUDE,)), lambda _event: None) == 0
    assert ("claude_code", "capture") not in device.installed


def test_every_registry_agent_and_alias_can_be_configured_through_the_service():
    from probe.harness import get_registry

    for harness in get_registry().installable():
        for word in dict.fromkeys((harness.cli_flag, *harness.names)):
            if not word:
                continue
            request = requests.parse(ActionName.CONFIGURE, {"agents": [word]})
            assert main._explicit_agent_sources([request.agents[0].value]) == (harness.id,)  # noqa: SLF001


def test_a_repeated_agent_is_configured_once():
    assert requests.parse(ActionName.CONFIGURE, {"agents": ["pi", "claude", "pi"]}).agents == (Agent.PI, Agent.CLAUDE)


@pytest.mark.parametrize(
    "build",
    [
        lambda: ConfigureRequest(agents=()),
        lambda: ConfigureRequest(agents=("not_a_registered_agent",)),
        lambda: ConfigureRequest(agents=(Agent.CLAUDE,), capture="false"),  # a truthy string
        lambda: RecorderRequest("both"),
        lambda: SessionDefaultRequest("daemon"),
    ],
)
def test_a_request_built_in_python_is_checked_like_one_read_from_json(build):
    with pytest.raises(RequestError):
        build()


def test_a_bad_word_handed_to_an_action_is_refused_before_it_runs():
    with pytest.raises(RequestError):
        probe.core.recorder("both", lambda _event: None)


# -- the import stays light -------------------------------------------------------

#: What `import probe.core` must not load: the CLI and its UI, the HTTP client,
#: the model layer. Each operation imports what it needs when it runs.
HEAVY = ("typer", "click", "questionary", "prompt_toolkit", "rich", "httpx", "pydantic")


def test_importing_probe_core_loads_no_cli_ui_or_http_client():
    code = (
        "import json, sys\n"
        "import probe.core, probe.core.events, probe.core.requests, probe.core.actions, probe.core.reads\n"
        "import probe.core.run\n"
        "print(json.dumps(sorted(sys.modules)))\n"
    )
    loaded = json.loads(subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True, timeout=60,
    ).stdout)
    heavy = [name for name in loaded if name.split(".")[0] in HEAVY or name.startswith("probe.cli")]
    assert heavy == []
    assert "probe.core.events" in loaded  # the control: the facade itself did load


def test_the_cli_json_events_module_is_the_core_events_module():
    from probe.cli import json_events

    assert json_events is events


@pytest.mark.parametrize("raised, reachable", [
    (urllib.error.URLError(socket.gaierror(8, "nodename nor servname provided")), False),
    (urllib.error.URLError(OSError(errno.ENETUNREACH, "Network is unreachable")), False),
    # An answer of a kind: the host refused, or hung; never the laptop's network.
    (urllib.error.URLError(ConnectionRefusedError(61, "Connection refused")), True),
    (TimeoutError("timed out"), True),
    (urllib.error.HTTPError("https://x.invalid", 503, "Service Unavailable", {}, None), True),
    (ValueError("manifest is not a JSON object"), True),
    (None, True),
])
def test_the_version_read_says_whether_the_manifest_answered(monkeypatch, raised, reachable):
    """The Probe service reads it after a failed update: offline (no answer at
    all) is not a failure in a row (`updater._offline`)."""
    from probe import version_policy
    from probe.core import run

    def fetch(url, *, context=None):
        if raised is not None:
            raise raised
        return {"cli": {"latest": "9.9.9"}}

    monkeypatch.setattr(version_policy, "fetch", fetch)
    assert run._cli_latest(fetch=True) == ("9.9.9" if raised is None else None, reachable)
    monkeypatch.setattr(version_policy, "read_cache", lambda: ({"cli": {"latest": "9.9.8"}}, 0, True))
    assert run._cli_latest(fetch=False) == ("9.9.8", None), "not asked: no network"


# -- workspace_limit: `probe workspace limit`, as the Probe service runs it ------

_LIMITED_CONFIG = {
    "version": 2,
    "current_context": "default",
    "contexts": {"default": {"workspace": {"id": "11111111-1111-1111-1111-111111111111", "project": None,
                                           "limit": True, "team_items": "hide", "name": "Mine"}}},
}


def _limited_side(tmp_path: Path, side: str) -> Path:
    _side_env(tmp_path, side)
    path = tmp_path / side / "config.json"
    path.write_text(json.dumps(_LIMITED_CONFIG))
    return path


def test_workspace_limit_team_is_the_same_change_as_the_cli_command(tmp_path):
    """Lifting the limit needs no network: both doors make the same change, and
    the core run's result row carries exactly the CLI's `--json` object."""
    cli_config, core_config = _limited_side(tmp_path, "cli"), _limited_side(tmp_path, "core")
    cli = _child(tmp_path, "cli", "cli", ["workspace", "limit", "--team", "--json"], bare=True)
    core = _child(tmp_path, "core", "core", ["workspace_limit"], stdin='{"workspace": null}', bare=True)

    assert (cli.returncode, core.returncode) == (0, 0), (cli.stderr, core.stderr)
    events = _events(core.stdout)
    assert [e["event"] for e in events] == ["result", "done"]
    (row,) = events[0]["agents"]
    assert (row["requested"], row["actual"]) == ({"workspace": None, "team_items": None}, json.loads(cli.stdout))
    assert json.loads(cli_config.read_text()) == json.loads(core_config.read_text())
    assert json.loads(core_config.read_text())["contexts"]["default"]["workspace"] == {
        "id": "11111111-1111-1111-1111-111111111111", "project": None,
    }


def test_an_agent_the_daemon_records_cannot_change_the_limit_through_the_runner(tmp_path, monkeypatch):
    from probe.sdk import session_marker

    config = _limited_side(tmp_path, "core")
    monkeypatch.setenv("XDG_STATE_HOME", _side_env(tmp_path, "core")["XDG_STATE_HOME"])
    session_marker.mark_session_profile(AGENT_SESSION, session_marker.RECORDER_DAEMON)
    result = _child(tmp_path, "core", "core", ["workspace_limit"], stdin='{"workspace": null}', bare=True,
                    CLAUDE_CODE_SESSION_ID=AGENT_SESSION)
    out = _events(result.stdout)
    assert result.returncode == 2 and out[-1]["event"] == "done" and not out[-1]["ok"], result.stderr
    assert "probe workspace limit" in next(e["message"] for e in out if e["event"] == "error")
    assert json.loads(config.read_text()) == _LIMITED_CONFIG
