"""`probe wizard --json`: stdout carries only NDJSON events, every line, flushed.

The desktop app runs its own onboarding screens and makes every change through
these commands, reading stdout line by line. Anything else a run prints -- the
wizard's own text, `typer.echo`, a child process writing to fd 1 -- goes to
stderr. Without `--json` the terminal output is unchanged, byte for byte.
"""

from __future__ import annotations

import importlib
import io
import json
import os
import re
import signal
import subprocess
import sys
import textwrap
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace

import pytest
import typer
from typer.testing import CliRunner

from probe.cli import bootstrap, doctor, json_events, outbox_worker, setup, upgrading
from probe.cli.capabilities import Capabilities, capture_token_sources
from probe.sdk import device as device_flow
from probe.sdk.config import resolve, save_context
from probe.sdk.device import DevicePrompt, OnboardingRequired

main = importlib.import_module("probe.cli.main")

PROMPT = DevicePrompt(
    user_code="WDJB-MJHT",
    verification_uri="https://app.test/device",
    verification_uri_complete="https://app.test/device?code=WDJB-MJHT",
)


def plain(text: str) -> str:
    """What a person reads in typer's output: no styling, no panel borders,
    whitespace collapsed to single spaces.

    On GitHub Actions typer forces a coloured rich terminal (`GITHUB_ACTIONS`
    sets `typer.rich_utils.FORCE_TERMINAL`), so `--agent` reaches a usage error
    as `-` and `-agent` in two styled runs and a long message wraps inside the
    error panel's border. A plain `in` check passes locally and fails there.
    """
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    return " ".join(text.translate({ord(c): " " for c in "│╭╮╰╯─"}).split())


@pytest.fixture
def device(tmp_path, monkeypatch):
    """A fresh machine the REAL wizard configures. Stood in for: the coding
    agents' own CLIs (the plugin installs), the browser approval's HTTP mint,
    and the server's registration -- nothing the wizard decides."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.test")
    for variable in ("PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_INGEST_TOKEN"):
        monkeypatch.delenv(variable, raising=False)
    state = SimpleNamespace(tmp=tmp_path, installed=set(), authorizations=[], registrations=[])
    monkeypatch.setattr(
        bootstrap,
        "ensure_persistent_install",
        lambda **_: bootstrap.BootstrapResult(installed=False, already_persistent=True, message=""),
    )
    monkeypatch.setattr(main, "_version_notice", lambda: None)
    monkeypatch.setattr(main, "_outbox_notice", lambda: None)
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    monkeypatch.setattr(setup, "refresh_marketplace", lambda **_: None)
    monkeypatch.setattr(setup, "_record_login_account", lambda *a, **k: None)
    monkeypatch.setattr("probe.cli.capabilities.verify_mcp_credential", lambda **_: True)
    monkeypatch.setattr(outbox_worker, "maybe_spawn", lambda *a, **k: None)

    def device_authorize(base_url, *, grants=None, capture_source=None, capture_sources=None,
                         on_prompt=None, **_):
        state.authorizations.append(list(grants or []))
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

    monkeypatch.setattr(device_flow, "device_authorize", device_authorize)

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
            tracking_plugin_installed=(source, "tracking") in state.installed,
            capture_plugin_installed=(source, "capture") in state.installed,
            capture_token_sources=paired,
            capture_credential_valid=True if paired else None,
            mcp_authenticated=True,
            auto_update_enabled=(source, "updates") in state.installed,
            agent_rules_installed=(source, "rules") in state.installed,
        )

    def applied(kind):
        def apply(*_a, **_k):
            state.installed.add((os.environ["PROBE_AGENT"], kind))
            return [f"{kind} applied."]

        return apply

    monkeypatch.setattr(doctor, "collect", collect)
    monkeypatch.setattr(setup, "apply_tracking", applied("tracking"))
    monkeypatch.setattr(setup, "apply_capture", applied("capture"))
    monkeypatch.setattr(setup, "apply_auto_update", applied("updates"))
    monkeypatch.setattr(setup, "apply_agent_rules", applied("rules"))
    monkeypatch.setattr(
        main,
        "_register_local_capabilities",
        lambda caps, **_: state.registrations.append(caps.agent_source) or [],
    )
    return state


@pytest.fixture
def browser_login(device, monkeypatch):
    """`--action login`'s browser sign-in: the device flow shows its prompt and
    mints; `/v1/me` names the account."""

    def device_login(endpoint, on_prompt=None, open_browser=True):
        on_prompt(PROMPT)
        return "probe_pat_device"

    class _Client:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def me(self):
            return {"email": "researcher@example.test", "customer_id": "lab-1", "user_id": "u-1"}

    monkeypatch.setattr(main, "device_login", device_login)
    monkeypatch.setattr(main, "_new_client", lambda **_: _Client())
    return device


def _human(result, device) -> str:
    return result.stdout.replace(str(device.tmp), "<tmp>")


def _events(stdout: str) -> list[dict]:
    return [json.loads(line) for line in stdout.splitlines()]


def _last(events: list[dict], kind: str) -> dict:
    return [event for event in events if event["event"] == kind][-1]


# -- without --json: the terminal output is byte-identical ---------------------
#
# Captured from origin/main (34865d40a) by running these same fixtures there.

GOLDEN_LOGIN = (
    "approve this device at https://api.test…\n"
    "  visit: https://app.test/device?code=WDJB-MJHT\n"
    "  code:  WDJB-MJHT\n"
    "logged in to https://api.test as researcher@example.test\n"
    "config: <tmp>/config.json (context: default)\n"
)

GOLDEN_CONFIGURE_CLAUDE = (
    "One browser approval covers everything listed (api, mcp, capture).\n"
    "  visit: https://app.test/device?code=WDJB-MJHT\n"
    "  code:  WDJB-MJHT\n"
    "[1/6] sign in (api, mcp, capture) ... ok\n"
    "Claude Code Session capture paired (device ?).\n"
    "[2/6] refresh the plugin marketplace ... ok\n"
    "[3/6] install the CLI + MCP plugin ... ok\n"
    "tracking applied.\n"
    "[4/6] install the Session capture plugin ... ok\n"
    "capture applied.\n"
    "[5/6] enable automatic updates ... ok\n"
    "updates applied.\n"
    "[6/6] write the rules into your global CLAUDE.md ... ok\n"
    "rules applied.\n"
    "Restart Claude Code to load Probe.\n"
)

GOLDEN_CONFIGURE_BOTH = (
    "One browser approval covers everything listed (api, mcp, capture).\n"
    "  visit: https://app.test/device?code=WDJB-MJHT\n"
    "  code:  WDJB-MJHT\n"
    "[1/6] sign in (api, mcp, capture) ... ok\n"
    "Claude Code Session capture paired (device ?).\n"
    "Codex Session capture paired (device ?).\n"
    "[2/6] refresh the plugin marketplace ... ok\n"
    "[3/6] install the CLI + MCP plugin ... ok\n"
    "tracking applied.\n"
    "[4/6] install the Session capture plugin ... ok\n"
    "capture applied.\n"
    "[5/6] enable automatic updates ... ok\n"
    "updates applied.\n"
    "[6/6] write the rules into your global CLAUDE.md ... ok\n"
    "rules applied.\n"
    "Restart Claude Code to load Probe.\n"
    "[1/5] refresh the plugin marketplace ... ok\n"
    "[2/5] install the CLI + MCP plugin ... ok\n"
    "tracking applied.\n"
    "[3/5] install the Session capture plugin ... ok\n"
    "capture applied.\n"
    "[4/5] enable automatic updates ... ok\n"
    "updates applied.\n"
    "[5/5] write the rules into your global AGENTS.md ... ok\n"
    "rules applied.\n"
    "Restart Codex to load Probe.\n"
    "In the new session: `/hooks` › approve Probe Session Capture.\n"
    "Until you do, capture is installed but sends nothing.\n"
)


def test_login_without_json_prints_exactly_what_it_printed_before(browser_login):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "login", "--no-browser"])
    assert _human(result, browser_login) == GOLDEN_LOGIN


def test_configure_without_json_prints_exactly_what_it_printed_before(device):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude"])
    assert _human(result, device) == GOLDEN_CONFIGURE_CLAUDE


def test_a_two_agent_configure_without_json_prints_exactly_what_it_printed_before(device):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--agent", "both"])
    assert _human(result, device) == GOLDEN_CONFIGURE_BOTH


# -- a real process: stdout is the events, all of them, and nothing else -------

#: `--action update` with the update itself replaced by one that prints every
#: way a run can: print, typer.echo, and a child process writing to fd 1.
NOISY_UPDATE = textwrap.dedent(
    """
    import importlib, subprocess, sys
    import typer
    from probe.cli import bootstrap, upgrading
    main = importlib.import_module("probe.cli.main")
    bootstrap.ensure_persistent_install = lambda **_: bootstrap.BootstrapResult(False, True, "")
    def perform_update(**_):
        print("print noise")
        typer.echo("echo noise")
        subprocess.run(
            [sys.executable, "-c", "import os; print('child noise', flush=True); os.write(1, b'raw fd noise\\\\n')"],
            check=True,
        )
        return upgrading.UpdateOutcome(lines=["Updated."], ok=True, restart_needed=False)
    upgrading.perform_update = perform_update
    raise SystemExit(main.main(sys.argv[1:]))
    """
)


def _child_env(tmp_path) -> dict[str, str]:
    """This test's isolated environment (conftest's), with no coding agent,
    uv or pipx on PATH and a server address nothing listens on."""
    empty = tmp_path / "empty-path"
    empty.mkdir(exist_ok=True)
    return {
        **os.environ,
        "PATH": str(empty),
        "XDG_STATE_HOME": str(tmp_path / "state"),
        "PROBE_CONFIG_PATH": str(tmp_path / "config.json"),
        "PROBE_BASE_URL": "http://127.0.0.1:9",
    }


@pytest.fixture
def noisy_run(tmp_path):
    return subprocess.run(
        [sys.executable, "-c", NOISY_UPDATE, "wizard", "--action", "update", "--yes", "--json"],
        env=_child_env(tmp_path), capture_output=True, text=True, timeout=120,
    )


def test_every_stdout_line_of_a_json_run_is_one_json_object(noisy_run):
    assert noisy_run.stdout.strip(), noisy_run.stderr
    for line in noisy_run.stdout.splitlines():
        assert isinstance(json.loads(line), dict), line


def test_what_the_run_prints_reaches_stderr_instead(noisy_run):
    for noise in ("print noise", "echo noise", "child noise", "raw fd noise"):
        assert noise in noisy_run.stderr, noise


def test_done_is_the_last_line(noisy_run):
    assert _events(noisy_run.stdout)[-1]["event"] == "done"


# -- device_prompt reaches the reader before the approval is polled ------------


class _DeviceServer(BaseHTTPRequestHandler):
    """The device-flow and `/me` routes of a Probe server, as one test needs them."""

    shared: SimpleNamespace

    def log_message(self, *_args):
        pass

    def _send(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):  # noqa: N802 - http.server's name
        self.rfile.read(int(self.headers.get("Content-Length") or 0))
        if self.path.endswith("/auth/device/code"):
            self._send(201, {
                "device_code": "device-code", "user_code": "WDJB-MJHT",
                "verification_uri": "https://app.test/device",
                "verification_uri_complete": "https://app.test/device?code=WDJB-MJHT",
                "expires_in": 600, "interval": 1,
            })
        elif self.path.endswith("/auth/device/token"):
            if self.shared.prompt_before_poll is None:
                # The reader gets a moment to read a flushed line; an unflushed
                # one stays in the child, which is blocked right here.
                self.shared.prompt_before_poll = self.shared.prompt_read.wait(timeout=10)
            self._send(200, {"token": "probe_pat_device", "id": "t1", "name": "cli"})
        else:
            self._send(404, {"detail": "not here"})

    def do_GET(self):  # noqa: N802
        if self.path.endswith("/me"):
            self._send(200, {"email": "researcher@example.test", "customer_id": "lab-1", "user_id": "u-1"})
        else:
            self._send(404, {"detail": "not here"})


def test_the_device_prompt_is_read_before_the_first_token_poll(tmp_path):
    shared = SimpleNamespace(prompt_read=threading.Event(), prompt_before_poll=None)
    handler = type("Handler", (_DeviceServer,), {"shared": shared})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    env = {**_child_env(tmp_path), "PROBE_BASE_URL": f"http://127.0.0.1:{server.server_port}"}
    child = subprocess.Popen(
        [sys.executable, "-m", "probe.cli", "wizard", "--action", "login", "--no-browser", "--json"],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
    )
    try:
        for line in child.stdout:
            if json.loads(line)["event"] == "device_prompt":
                shared.prompt_read.set()
        child.wait(timeout=60)
    finally:
        child.kill()
        server.shutdown()
    assert shared.prompt_before_poll is True


# -- onboarding first: exit 0 as before, but not complete ----------------------


@pytest.fixture
def onboarding_first(browser_login, monkeypatch):
    def device_login(endpoint, on_prompt=None, open_browser=True):
        raise OnboardingRequired("finish onboarding first", onboarding_url="https://app.test/onboarding")

    monkeypatch.setattr(main, "device_login", device_login)
    return CliRunner().invoke(main.app, ["wizard", "--action", "login", "--no-browser", "--json"])


def test_onboarding_required_names_the_website_page(onboarding_first):
    assert _last(_events(onboarding_first.stdout), "onboarding_required")["url"] == "https://app.test/onboarding"


def test_onboarding_required_still_exits_zero(onboarding_first):
    assert onboarding_first.exit_code == 0


def test_onboarding_required_leaves_the_run_incomplete(onboarding_first):
    assert _last(_events(onboarding_first.stdout), "done")["complete"] is False


# -- the persistent CLI is part of a complete install --------------------------


def _configure_json(device):
    return CliRunner().invoke(
        main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude", "--json"]
    )


@pytest.fixture
def no_persistent_cli(device, monkeypatch):
    monkeypatch.setattr(
        bootstrap,
        "ensure_persistent_install",
        lambda **_: bootstrap.BootstrapResult(
            installed=False,
            already_persistent=False,
            message="could not install `probe` persistently: neither uv nor pipx is available.",
        ),
    )
    return _configure_json(device)


def test_a_configure_that_did_everything_is_complete(device):
    """The control for the two below: this fixture's install is otherwise whole."""
    assert _last(_events(_configure_json(device).stdout), "done")["complete"] is True


def test_a_failed_persistent_install_leaves_the_install_incomplete(no_persistent_cli):
    assert _last(_events(no_persistent_cli.stdout), "done")["complete"] is False


def test_a_failed_persistent_install_is_its_own_failed_step(no_persistent_cli):
    steps = {step["name"]: step["status"] for step in _last(_events(no_persistent_cli.stdout), "done")["steps"]}
    assert steps["persistent_install"] == "failed"


# -- a turn-off that did not happen, and a failed step, are not complete -------


@pytest.fixture
def signed_in_and_installed(device):
    save_context({"token": "probe_pat_api", "mcp_token": "probe_pat_mcp", "ingest_token": "ros_ing_claude_code"})
    device.installed.update(("claude_code", kind) for kind in ("tracking", "capture", "updates", "rules"))
    return device


def _capture_off(monkeypatch, apply_capture):
    monkeypatch.setattr(setup, "apply_capture", apply_capture)
    return _events(
        CliRunner().invoke(
            main.app,
            ["wizard", "--action", "configure", "--yes", "--agent", "claude", "--no-capture", "--json"],
        ).stdout
    )


@pytest.fixture
def capture_left_on(signed_in_and_installed, monkeypatch):
    return _capture_off(monkeypatch, lambda *a, **k: ["could not turn capture off: boom"])


@pytest.fixture
def capture_turned_off(signed_in_and_installed, monkeypatch):
    def turn_off(*_a, **_k):
        # As `capture.turn_off` leaves it: the plugin gone, the credential cleared.
        signed_in_and_installed.installed.discard(("claude_code", "capture"))
        save_context({"ingest_token": None})
        return ["capture off."]

    return _capture_off(monkeypatch, turn_off)


def test_a_turn_off_that_happened_is_an_ok_row(capture_turned_off):
    """The control for the two below."""
    row = _last(capture_turned_off, "result")["agents"][0]
    assert (row["actual"]["capture"], row["ok"], _last(capture_turned_off, "done")["complete"]) == (
        False, True, True,
    )


def test_a_turn_off_that_did_not_happen_is_a_row_that_is_not_ok(capture_left_on):
    row = _last(capture_left_on, "result")["agents"][0]
    assert (row["requested"]["capture"], row["actual"]["capture"], row["ok"]) == (False, True, False)


def test_a_turn_off_that_did_not_happen_leaves_the_run_incomplete(capture_left_on):
    assert (_last(capture_left_on, "result")["complete"], _last(capture_left_on, "done")["complete"]) == (
        False, False,
    )


def _refresh_fails(monkeypatch, how):
    def refresh(**_):
        if how == "raises":
            raise RuntimeError("network down")
        return SimpleNamespace(ok=False, detail="network down")

    monkeypatch.setattr(setup, "refresh_marketplace", refresh)


@pytest.mark.parametrize("how", ["reports", "raises"])
def test_a_failed_refresh_the_install_went_past_is_done_and_complete(device, monkeypatch, how):
    """The install goes on from the marketplace copy already on disk and works:
    a failed step there showed the desktop app a failed install that works. The
    step keeps the failure's own words."""
    _refresh_fails(monkeypatch, how)
    done = _last(_events(_configure_json(device).stdout), "done")
    refresh = next(step for step in done["steps"] if step["name"] == "refresh_marketplace")
    assert (refresh["status"], done["ok"], done["complete"]) == ("done", True, True)
    assert refresh["message"].startswith("used the copy already on this machine (refresh failed: ")
    assert "network down" in refresh["message"]


def test_a_failed_refresh_then_a_failed_install_is_incomplete(device, monkeypatch):
    """The copy on disk could not serve the install: the install's step fails."""
    _refresh_fails(monkeypatch, "reports")
    monkeypatch.setattr(
        setup, "apply_tracking", lambda *a, **k: ["could not install probe: not found in marketplace"]
    )
    done = _last(_events(_configure_json(device).stdout), "done")
    steps = {step["name"]: step["status"] for step in done["steps"]}
    assert (steps["refresh_marketplace"], steps["tracking_plugin"], done["complete"]) == (
        "done", "failed", False,
    )


def test_any_other_failed_step_leaves_the_run_incomplete(device, monkeypatch):
    """Even one whose outcome then reads as asked: the step said it failed."""

    def warned(*_a, **_k):
        device.installed.add((os.environ["PROBE_AGENT"], "updates"))
        return ["! could not confirm the update schedule"]

    monkeypatch.setattr(setup, "apply_auto_update", warned)
    events = _events(_configure_json(device).stdout)
    done = _last(events, "done")
    steps = {step["name"]: step["status"] for step in done["steps"]}
    assert (steps["auto_update"], _last(events, "result")["agents"][0]["ok"], done["complete"]) == (
        "failed", True, False,
    )


# -- how a run ends ------------------------------------------------------------


def test_an_aborted_run_exits_1_as_failed(device, monkeypatch):
    def abort(**_):
        raise typer.Abort()

    monkeypatch.setattr(upgrading, "perform_update", abort)
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes", "--agent", "claude", "--json"])
    events = _events(result.stdout)
    assert (result.exit_code, _last(events, "error")["code"], events[-1]["exit_code"]) == (1, "failed", 1)


def test_an_in_process_json_run_puts_the_signal_handlers_back(device):
    numbers = [signal.SIGINT, signal.SIGTERM, *([signal.SIGHUP] if hasattr(signal, "SIGHUP") else [])]
    before = [signal.getsignal(number) for number in numbers]
    _configure_json(device)
    assert [signal.getsignal(number) for number in numbers] == before


def test_probe_setup_ends_a_refused_run_with_done_too(device):
    result = CliRunner().invoke(main.app, ["setup", "--json", "--no-such-flag"])
    assert (result.exit_code, _events(result.stdout)[-1]["event"]) == (2, "done")


def test_help_is_not_a_run(device):
    """Documented in `json_events`: `--help` prints its help, and no events."""
    result = CliRunner().invoke(main.app, ["wizard", "--json", "--help"])
    assert (result.exit_code, "--json" in plain(result.stdout), '"event"' in result.stdout) == (0, True, False)


# -- giving stdout back --------------------------------------------------------


@pytest.mark.skipif(not os.path.isdir("/proc/self/fd"), reason="counts descriptors in /proc")
def test_a_redirect_that_fails_leaks_no_descriptor(monkeypatch):
    real_dup2 = os.dup2

    def dup2(fd, fd2, *args, **kwargs):
        if (fd, fd2) == (2, 1):
            raise OSError("refused")
        return real_dup2(fd, fd2, *args, **kwargs)

    monkeypatch.setattr(os, "dup2", dup2)
    before = sorted(os.listdir("/proc/self/fd"))
    with json_events.redirect_stdout():
        pass
    assert sorted(os.listdir("/proc/self/fd")) == before


def test_the_events_stream_is_closed_even_when_its_flush_fails(monkeypatch):
    class Gone(io.StringIO):
        def flush(self):
            raise OSError("reader went away")

    stream = Gone()
    monkeypatch.setattr(json_events, "_events_stream", lambda _original: (stream, True))
    with json_events.redirect_stdout():
        pass
    assert stream.closed


def test_a_process_with_no_stdout_still_runs_a_session(monkeypatch):
    monkeypatch.setattr(sys, "stdout", None)
    with json_events.session(True):
        json_events.step(json_events.Step.SIGN_IN, json_events.Status.DONE)
        print("still printable")
    assert sys.stdout is None
