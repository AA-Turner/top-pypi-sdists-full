"""`probe status --json`: the device's one Probe install, as the wizard's menu sees it.

The desktop app asks for this on every focus, so the default read must start
no process and open no socket, and a hung coding-agent binary must not slow it
down. One exception, pinned in (b2): where Probe's Codex plugins are installed,
Codex is asked which of Probe's hooks it will run, at most once per 10 minutes
and never for more than 2s. `--refresh` asks the agents' own CLIs and the server, each bounded: a
check that times out is an error on that check, never a hang. Whatever the
JSON says, the terminal wizard's menu must say too, for the same device.

Real boundaries: the coding agents are executables on PATH (shell scripts that
log every call), the files are the ones each agent and the wizard write. Stood
in for: the two network calls (`fetch_device_state`, `main._verify_read`).
"""

from __future__ import annotations

import importlib
import json
import os
import re
import signal
import socket
import subprocess
import sys
import textwrap
import threading
import time
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from probe.cli import autoupdate, capabilities, doctor, pi_config, plugin_cli, setup, versions, wizard_lock
from probe.cli import status as status_impl
from probe.cli.capabilities import DeviceState, DeviceStateOutcome, McpState
from probe.cli.versions import VersionStatus
from probe.sdk import agent_session, session_marker
from probe.sdk.config import resolve, save_context

main = importlib.import_module("probe.cli.main")

#: `plugin_cli.available` as shipped (`shutil.which`). The suite pins it off for
#: every test; these tests control PATH instead, so they put the real one back.
REAL_AVAILABLE = plugin_cli.available
#: The real network calls and pi's real sniff, for the tests that use them:
#: `machine` stands in for the first two, the suite pins the third off.
REAL_FETCH_DEVICE_STATE = capabilities.fetch_device_state
REAL_VERIFY = main._verify_read  # noqa: SLF001
REAL_PI_SNIFF = pi_config.pi_binary_available

EMAIL = "researcher@example.test"

CLAUDE_PLUGIN_LIST = (
    "Installed plugins:\n"
    "  > probe-research@research-os-agent\n"
    "    Version: 0.156.0\n"
    "  > probe-research-tap@research-os-agent\n"
    "    Version: 0.9.20\n"
)
CODEX_PLUGIN_LIST = json.dumps(
    {
        "installed": [
            {"pluginId": "probe-research-daemon@research-os-agent", "installed": True, "enabled": True},
            {"pluginId": "probe-research-tap@research-os-agent", "installed": True, "enabled": True},
        ]
    },
    indent=2,
)

#: Takes the run lock, says so, and sleeps until it is killed.
HOLDER = textwrap.dedent(
    """
    import sys, time
    from probe.cli import wizard_lock
    with wizard_lock.held():
        open(sys.argv[1], "w").close()
        time.sleep(300)
    """
)


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """A device with nothing on it: its home, config and state under tmp_path,
    and a PATH holding only the agent binaries a test puts there."""
    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(home / ".local" / "state"))
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.test")
    for variable in (
        "PROBE_CONFIG_PATH",
        "PROBE_TOKEN",
        "PROBE_MCP_TOKEN",
        "PROBE_INGEST_TOKEN",
        "PRBE_CODEX_TAP_TOKEN",
        "PROBE_PI_TAP_TOKEN",
        "PROBE_SESSION_STATE",
        "PROBE_SESSION_TRACKING",
        "PROBE_INSTALLED_PLUGINS_JSON",
    ):
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv("PATH", str(bin_dir))
    monkeypatch.setattr(plugin_cli, "available", REAL_AVAILABLE)
    calls = tmp_path / "agent-calls.log"
    calls.touch()
    answers: dict = {"device_state": None, "token": ("ok", {"email": EMAIL})}

    def fetch_device_state(request, **_):
        if answers["device_state"] is not None:
            return answers["device_state"]
        if not request.token:
            return DeviceState(DeviceStateOutcome.ANSWERED, account_valid=None)
        return DeviceState(
            DeviceStateOutcome.ANSWERED,
            account_email=EMAIL,
            account_valid=True,
            capture={source: True for source in request.capture_tokens},
        )

    monkeypatch.setattr(capabilities, "fetch_device_state", fetch_device_state)
    monkeypatch.setattr(main, "_verify_read", lambda token, base_url: answers["token"])
    # A verdict another test recorded in this process is not this device's.
    monkeypatch.setattr(capabilities, "_MCP_TOKEN_VERDICT", None)
    return SimpleNamespace(home=home, bin=bin_dir, calls=calls, answers=answers, tmp=tmp_path)


def agent_binary(machine, name: str, body: str) -> None:
    """An executable `name` on PATH that logs its argv, then runs `body`."""
    path = machine.bin / name
    path.write_text(f'#!/bin/sh\necho "{name} $*" >> "{machine.calls}"\n{body}\n')
    path.chmod(0o755)


def hung(machine, name: str) -> None:
    agent_binary(machine, name, "exec /bin/sleep 60")


def agent_calls(machine) -> list[str]:
    return machine.calls.read_text().splitlines()


def configured(machine) -> None:
    """Signed in, Claude Code set up (plugin, capture), Codex recording through
    the daemon (its lean plugin, capture), new sessions defaulting to `read`:
    every file as the wizard and the agents leave it."""
    agent_binary(
        machine,
        "claude",
        'case "$1 $2" in\n'
        f"  'plugin list') /bin/cat <<'EOF'\n{CLAUDE_PLUGIN_LIST}EOF\n;;\n"
        '  *) echo "2.1.300 (Claude Code)" ;;\nesac',
    )
    agent_binary(
        machine,
        "codex",
        'case "$1 $2" in\n'
        f"  'plugin list') /bin/cat <<'EOF'\n{CODEX_PLUGIN_LIST}\nEOF\n;;\n"
        "  'mcp list') echo '[]' ;;\n"
        '  *) echo "codex-cli 0.160.1" ;;\nesac',
    )
    save_context({"base_url": "https://api.test", "token": "probe_pat_api", "mcp_token": "probe_mcp_read"})
    session_marker.write_default_state(session_marker.STATE_READ_ONLY)
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    ledger = machine.home / ".claude" / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(
        json.dumps(
            {
                "version": 2,
                "plugins": {
                    "probe-research@research-os-agent": [{"scope": "user", "version": "0.156.0"}],
                    "probe-research-tap@research-os-agent": [{"scope": "user", "version": "0.9.20"}],
                },
            }
        )
    )
    codex_config = machine.home / ".codex" / "config.toml"
    codex_config.parent.mkdir(parents=True)
    codex_config.write_text(
        '[plugins."probe-research-daemon@research-os-agent"]\nenabled = true\n\n'
        '[plugins."probe-research-tap@research-os-agent"]\nenabled = true\n'
    )
    for source in ("claude_code", "codex"):
        token = capabilities.tap_plugin_dir(source) / ".token"
        token.parent.mkdir(parents=True, exist_ok=True)
        token.write_text(f"ros_ing_{source}")


def codex_on_the_agent_profile(machine, *, mcp_list: str) -> None:
    """Codex recording itself: its full plugin (the MCP with it), logged in to
    the MCP the way `codex mcp list` reports as `mcp_list` -- an OAuth login
    leaves no header in config.toml."""
    plugins = json.dumps(
        {
            "installed": [
                {"pluginId": "probe-research@research-os-agent", "installed": True, "enabled": True},
                {"pluginId": "probe-research-tap@research-os-agent", "installed": True, "enabled": True},
            ]
        },
        indent=2,
    )
    agent_binary(
        machine,
        "codex",
        'case "$1 $2" in\n'
        f"  'plugin list') /bin/cat <<'EOF'\n{plugins}\nEOF\n;;\n"
        f"  'mcp list') echo '{mcp_list}' ;;\n"
        '  *) echo "codex-cli 0.160.1" ;;\nesac',
    )
    session_marker.write_recorder("codex", session_marker.RECORDER_AGENT)
    (machine.home / ".codex" / "config.toml").write_text(
        '[plugins."probe-research@research-os-agent"]\nenabled = true\n\n'
        '[plugins."probe-research-tap@research-os-agent"]\nenabled = true\n'
    )


def status(*args: str) -> tuple[dict, float, object]:
    started = time.monotonic()
    result = CliRunner().invoke(main.app, ["status", "--json", *args])
    elapsed = time.monotonic() - started
    assert result.exit_code == 0, (result.output, result.stderr)
    return json.loads(result.stdout), elapsed, result


def agent(state: dict, source: str) -> dict:
    return next(row for row in state["agents"] if row["agent"] == source)


def menu(machine) -> SimpleNamespace:
    """What the wizard's menu draws for this device, built the way
    `_wizard_session` builds it -- the read-token verdict, one device-state
    call, `doctor.collect()` per agent found here under both, reading plugin
    records -- and drawn by the menu's own row builders."""
    capabilities.refresh_mcp_token_verdict()
    settings = resolve()
    server = capabilities.start_device_state(
        capabilities.device_state_request(settings.base_url, settings.token, setup.INSTALLABLE_AGENT_SOURCES)
    )
    installed = setup.detectable_sources()
    caps = {}
    # The wizard reads the agents' plugin records, not their `plugin list`
    # (`plugin_records`, around the whole run): the menu must still say what
    # `status --refresh` says, which asks the CLIs.
    with capabilities.plugin_records():
        for source in installed or ("claude_code",):
            with capabilities.agent_target(source), doctor.device_state_scope(server):
                caps[source] = doctor.collect()
    header = [str(line) for line in setup.describe_state(caps, installed=installed)]
    return SimpleNamespace(
        caps=caps,
        installed=installed,
        header=header,
        recorder=setup.recorder_row(caps_by_source=caps)[0],
        default=setup.tracking_default_row()[0],
    )


def header_value(lines: list[str], label: str) -> str:
    line = next(line for line in lines if line.strip().startswith(label))
    return line.strip()[len(label):].strip()


def assert_menu_agrees(drawn: SimpleNamespace, state: dict) -> None:
    """Every row the menu draws says what the JSON says."""
    assert f"‹ {state['who_records']} ›" in drawn.recorder
    assert f"‹ {state['session_default']['state']} ›" in drawn.default
    assert header_value(drawn.header, "Account") == (state["account"]["email"] or "not signed in")
    assert header_value(drawn.header, "Automatic updates") == ("on" if state["auto_update"]["enabled"] else "off")
    verdict = setup._VERDICT_COPY[VersionStatus(state["versions"]["status"])][1]  # noqa: SLF001
    assert verdict in header_value(drawn.header, "Versions")
    found = [row for row in state["agents"] if row["installed"]]
    assert [row["agent"] for row in found] == sorted(drawn.installed, key=[row["agent"] for row in state["agents"]].index)
    for row in found:
        line = next(line for line in drawn.header if line.strip().startswith(row["label"]))
        assert f"MCP {setup._MCP_WORDS[McpState(row['mcp_state'])]}" in line  # noqa: SLF001
        assert f"capture {'on' if row['capture_on'] else 'off'}" in line
        assert drawn.caps[row["agent"]].tracking_plugin_installed is row["plugin_installed"]
        # NOT the menu's `Capabilities.configured`, on purpose (the schema's
        # `configured`): that one counts the device's own evidence too -- the
        # sign-in, automatic updates -- so it is true for every agent on a
        # signed-in device. The JSON's is the same snapshot's per-agent half.
        assert drawn.caps[row["agent"]].agent_configured is row["configured"]
    if not found:
        assert header_value(drawn.header, "Coding agents") == "none found on this device"


#: The fields the menu and both status reads must agree on, per agent.
AGENT_FIELDS = ("agent", "installed", "configured", "plugin_installed", "capture_on", "mcp_state", "recorder")


def same_state(local: dict, refreshed: dict, *, unread_mcp: tuple[str, ...] = ()) -> None:
    """The default read, from files alone, says what --refresh says -- but for
    the MCP of each agent in `unread_mcp`, whose login only its CLI can read."""
    for key in ("who_records", "session_default", "auto_update", "versions", "wizard_running"):
        assert local[key] == refreshed[key], key
    for key in ("signed_in", "context", "base_url"):
        assert local["account"][key] == refreshed["account"][key], key

    def fields(row):
        return {k: row[k] for k in AGENT_FIELDS if not (k == "mcp_state" and row["agent"] in unread_mcp)}

    assert [fields(row) for row in local["agents"]] == [fields(row) for row in refreshed["agents"]]


# -- (a) parity with the wizard's menu ---------------------------------------


def test_a_fresh_device_reads_as_the_menu_draws_it(machine):
    local, _, _ = status()
    refreshed, _, _ = status("--refresh")
    assert_menu_agrees(menu(machine), refreshed)
    same_state(local, refreshed)
    assert local["account"] == {
        "signed_in": False,
        "email": None,
        "context": "default",
        "base_url": "https://api.test",
        "credential_valid": None,
        "workspace_limit": None,
    }
    assert not any(row["installed"] for row in local["agents"])
    assert (local["who_records"], local["session_default"]) == ("agent", {"state": "on", "env_override": None})
    assert local["errors"] == [] and local["wizard_running"] is False


def test_a_configured_device_reads_as_the_menu_draws_it(machine):
    configured(machine)
    refreshed, _, _ = status("--refresh")
    assert_menu_agrees(menu(machine), refreshed)
    assert refreshed["account"]["email"] == EMAIL
    assert refreshed["account"]["credential_valid"] is True
    # Agreement on a real answer, not on two shrugs.
    assert {row["agent"]: row["plugins"]["checked"] for row in refreshed["agents"] if row["installed"]} == {
        "claude_code": True,
        "codex": True,
    }


def test_the_default_read_says_what_refresh_says_from_files_alone(machine):
    configured(machine)
    local, _, _ = status()
    assert agent_calls(machine) == []
    refreshed, _, _ = status("--refresh")
    assert "claude plugin list" in agent_calls(machine)  # --refresh did ask the agents
    same_state(local, refreshed)


def test_the_configured_device_reads_as_set_up(machine):
    configured(machine)
    state, _, _ = status()
    claude, codex = agent(state, "claude_code"), agent(state, "codex")
    assert (claude["installed"], claude["plugin_installed"], claude["capture_on"]) == (True, True, True)
    assert (claude["mcp_state"], claude["recorder"]) == ("on", "agent")
    assert (codex["plugin_installed"], codex["mcp_state"], codex["recorder"]) == (True, "daemon", "daemon")
    assert state["who_records"] == "daemon"
    assert state["session_default"] == {"state": "read", "env_override": None}
    assert state["account"]["signed_in"] is True and state["account"]["email"] is None
    assert claude["plugins"] == {"state": "verified", "checked": False, "error": None}


def test_refresh_says_the_agents_cli_answered(machine):
    configured(machine)
    state, _, _ = status("--refresh")
    assert agent(state, "claude_code")["plugins"] == {"state": "verified", "checked": True, "error": None}
    assert state["checks"]["device_state"] == {"state": "answered", "checked": True, "error": None}
    assert state["checks"]["mcp_token"] == {"state": "ok", "checked": True, "error": None}


def test_an_environment_override_is_named(machine, monkeypatch):
    monkeypatch.setenv("PROBE_SESSION_STATE", "off")
    state, _, _ = status()
    assert state["session_default"] == {"state": "off", "env_override": "off"}
    assert "Locked by an environment variable." in setup.tracking_default_row()[1]


# -- (b) the default read starts nothing and sends nothing --------------------


@pytest.fixture
def no_io(monkeypatch):
    """Every way to open a connection or start a process, recorded and refused.
    Recorded, not only raised: fail-soft code would swallow the refusal."""
    attempts: list[str] = []

    def refuse(what):
        def guard(*args, **kwargs):
            attempts.append(f"{what} {args[1:2] or args[:1]}")
            raise OSError(f"status test: {what} is not allowed")

        return guard

    monkeypatch.setattr(socket.socket, "connect", refuse("socket.connect"))
    monkeypatch.setattr(socket.socket, "connect_ex", refuse("socket.connect_ex"))
    monkeypatch.setattr(socket, "create_connection", refuse("socket.create_connection"))
    monkeypatch.setattr(socket, "getaddrinfo", refuse("socket.getaddrinfo"))
    monkeypatch.setattr(subprocess.Popen, "__init__", refuse("subprocess.Popen"))
    for name in ("system", "posix_spawn", "posix_spawnp", "fork", "forkpty"):
        if hasattr(os, name):
            monkeypatch.setattr(os, name, refuse(f"os.{name}"))
    return attempts


def test_the_default_read_opens_no_socket_and_starts_no_process(machine, no_io):
    configured(machine)
    state, _, _ = status()
    assert no_io == []
    assert agent_calls(machine) == []
    assert agent(state, "claude_code")["plugin_installed"] is True


def test_the_every_command_notices_start_nothing_for_status(machine, no_io):
    """Auto-update on and its manifest cache stale: any other command would
    start the background refresher here."""
    from probe.cli import autoupdate

    configured(machine)
    autoupdate.save(enabled=True)
    status()
    assert no_io == []


def test_a_hung_agent_binary_does_not_slow_the_default_read(machine):
    configured(machine)
    hung(machine, "claude")
    hung(machine, "codex")
    state, elapsed, _ = status()
    assert elapsed < 2.0
    assert agent_calls(machine) == []
    assert agent(state, "claude_code")["installed"] is True


def test_a_hung_agent_binary_does_not_slow_the_cli_either(machine):
    """The same read as its own process, the way the app runs it."""
    configured(machine)
    hung(machine, "claude")
    started = time.monotonic()
    done = subprocess.run(
        [sys.executable, "-m", "probe.cli", "status", "--json"],
        capture_output=True,
        text=True,
        timeout=50,
        env={**os.environ, "PATH": str(machine.bin)},
    )
    elapsed = time.monotonic() - started
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["agents"][0]["installed"] is True
    assert elapsed < 30  # interpreter start on a loaded box; the hung binary would take 60
    assert agent_calls(machine) == []


# -- (b2) the one exception: Codex's hook approvals ------------------------------
#
# Codex skips a hook it has not approved without a word, and nothing of
# Probe's runs to report it, so the default read asks Codex itself -- only
# where Probe's Codex plugins are installed, at most once per 10 minutes.

CODEX_TAP_END = "probe-research-tap@research-os-agent:hooks/hooks.json:sessionEnd:0:0"


def codex_answering_hooks(machine, trust: str) -> None:
    """`configured`'s Codex, which also answers `hooks/list` (its app-server)
    with the tap's SessionEnd hook `trust`ed or not, and has Probe's plugins in
    its cache."""
    answer = machine.tmp / "hooks-list.json"
    answer.write_text(json.dumps({"jsonrpc": "2.0", "id": 2, "result": {"data": [{"hooks": [
        {"key": CODEX_TAP_END, "trustStatus": trust, "enabled": True}], "warnings": []}]}}))
    agent_binary(
        machine,
        "codex",
        'if [ "$1" = app-server ]; then\n'
        f"  while read -r line; do case \"$line\" in *hooks/list*) /bin/cat '{answer}'; echo;; esac; done\n"
        "  exit 0\nfi\n"
        'case "$1 $2" in\n'
        f"  'plugin list') /bin/cat <<'EOF'\n{CODEX_PLUGIN_LIST}\nEOF\n;;\n"
        "  'mcp list') echo '[]' ;;\n"
        '  *) echo "codex-cli 0.163.0" ;;\nesac',
    )
    for plugin, version in (("probe-research-daemon", "0.161.1"), ("probe-research-tap", "0.9.25")):
        (machine.home / ".codex" / "plugins" / "cache" / "research-os-agent" / plugin / version).mkdir(parents=True)


def test_hooks_codex_will_not_run_reach_the_json_and_the_person(machine):
    configured(machine)
    codex_answering_hooks(machine, "untrusted")
    state, _, _ = status()
    assert state["codex_hooks"]["state"] == "needs_approval"
    assert state["codex_hooks"]["untrusted"] == [CODEX_TAP_END]
    assert agent_calls(machine) == ["codex app-server"]
    result = CliRunner().invoke(main.app, ["status"])
    line = next(line for line in result.stdout.splitlines() if line.startswith("Codex hooks"))
    assert "type /hooks and approve the Probe Research hooks" in line
    assert agent_calls(machine) == ["codex app-server"], "the second read used the kept answer"


def test_approved_hooks_read_as_approved(machine):
    configured(machine)
    codex_answering_hooks(machine, "trusted")
    state, _, _ = status("--refresh")
    assert state["codex_hooks"]["state"] == "approved" and state["codex_hooks"]["checked_at"]
    assert "codex app-server" in agent_calls(machine)


def test_with_no_codex_binary_the_hooks_are_read_from_files_alone(machine, no_io):
    """Probe's plugins in Codex's cache but no `codex` on PATH (the Codex app's
    own binary, say): the heartbeat files speak, and nothing starts."""
    configured(machine)
    codex_answering_hooks(machine, "untrusted")
    (machine.bin / "codex").unlink()
    expect = machine.home / ".local" / "state" / "probe" / "hooks" / "expect"
    expect.mkdir(parents=True)
    (expect / "codex-session").write_text("1\n")
    os.utime(expect / "codex-session", (time.time() - 300,) * 2)
    state, _, _ = status()
    assert no_io == []
    assert state["codex_hooks"] == {
        "state": "needs_approval", "untrusted": [], "checked_at": None, "unheard_session": "codex-session",
    }


# -- (c) --refresh bounds every check ------------------------------------------


def test_refresh_with_a_hung_agent_returns_within_its_timeout(machine):
    configured(machine)
    hung(machine, "claude")
    (machine.bin / "codex").unlink()
    state, elapsed, _ = status("--refresh", "--timeout", "1")
    assert elapsed < 5.0
    assert agent(state, "claude_code")["plugins"] == {
        "state": "unverified",
        "checked": False,
        "error": "timed out after 1s",
    }
    # Asked once: its `--version` is not a second wait on the same hung binary.
    assert agent_calls(machine) == ["claude plugin list"]


def test_a_hung_token_check_is_an_error_not_a_hang(machine, monkeypatch):
    configured(machine)

    def stuck(token, base_url):
        time.sleep(5)
        return ("rejected", None)

    monkeypatch.setattr(main, "_verify_read", stuck)
    state, elapsed, _ = status("--refresh", "--timeout", "1")
    assert elapsed < 10.0
    assert state["checks"]["mcp_token"] == {"state": None, "checked": False, "error": "timed out after 1s"}
    # A late answer is never recorded: the MCP reads as it would with no verdict.
    assert agent(state, "claude_code")["mcp_state"] == "on"


def test_an_unreachable_server_is_a_check_error(machine):
    configured(machine)
    machine.answers["device_state"] = DeviceState(DeviceStateOutcome.UNREACHABLE, error="timed out")
    state, _, _ = status("--refresh")
    assert state["checks"]["device_state"] == {"state": "unreachable", "checked": False, "error": "timed out"}
    assert state["account"]["email"] is None and state["account"]["signed_in"] is True


def test_a_refused_read_token_reads_login_needed(machine):
    configured(machine)
    machine.answers["token"] = ("rejected", None)
    state, _, _ = status("--refresh")
    assert state["checks"]["mcp_token"] == {"state": "rejected", "checked": True, "error": None}
    assert agent(state, "claude_code")["mcp_state"] == "login-needed"


# -- (d) an unreadable install is never a fresh one ----------------------------


def test_a_corrupt_config_is_an_error_and_still_exits_0(machine):
    path = machine.home / ".config" / "probe" / "config.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"contexts": {"default": {"token": ')
    state, _, _ = status()
    assert [error["field"] for error in state["errors"]] == ["config"]
    assert str(path) in state["errors"][0]["message"]


def test_an_unreadable_plugin_record_is_unknown_never_not_installed(machine):
    configured(machine)
    (machine.home / ".claude" / "plugins" / "installed_plugins.json").write_text("{trunc")
    state, _, _ = status()
    claude = agent(state, "claude_code")
    assert claude["plugins"]["state"] == "unverified"
    assert claude["mcp_state"] == "unknown"
    assert [error["field"] for error in state["errors"]] == ["agents.claude_code.plugin_installed"]


# -- (e) a wizard run in progress ----------------------------------------------


def test_wizard_running_while_another_process_holds_the_lock(machine):
    assert status()[0]["wizard_running"] is False
    marker = machine.tmp / "held"
    holder = subprocess.Popen(
        [sys.executable, "-c", HOLDER, str(marker)],
        env={**os.environ, "PATH": os.defpath},
    )
    try:
        deadline = time.monotonic() + 60
        while not marker.exists():
            assert time.monotonic() < deadline and holder.poll() is None
            time.sleep(0.02)
        assert status()[0]["wizard_running"] is True
        holder.send_signal(signal.SIGKILL)
        holder.wait(timeout=30)
        assert status()[0]["wizard_running"] is False
    finally:
        holder.kill()


def test_the_status_probe_never_turns_a_starting_wizard_away(machine):
    """`running()` holds the lock for an instant; a wizard starting in that
    instant waits it out instead of reporting another setup."""
    path = wizard_lock.lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    import fcntl

    probe = open(path, "rb")  # noqa: SIM115
    # What `running()` takes: shared, which a run's exclusive take still meets.
    fcntl.flock(probe.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
    threading.Timer(0.05, probe.close).start()
    with wizard_lock.held():
        pass


def test_the_probe_creates_nothing(machine):
    status()
    assert not wizard_lock.lock_path().exists()


# -- the contract ----------------------------------------------------------------


def _documented_schema() -> dict:
    """The SCHEMA block of `probe.cli.status`'s docstring, as a JSON shape."""
    doc = status_impl.__doc__
    block = doc[doc.index("    {\n") : doc.index("    CHECK =")]
    check = '{"state": null, "checked": null, "error": null}'
    shape = re.sub(r"\b(str|bool|int|float)( \| null)?\b", "null", block)
    shape = shape.replace("CHECK", check)
    # An object-or-null (`LIMIT | null`): compared as a scalar here, and its keys by
    # `test_the_workspace_limit_is_the_documented_object`.
    shape = shape.replace("LIMIT | null", "null")
    return json.loads(shape)


def _documented_limit() -> set[str]:
    doc = status_impl.__doc__
    line = next(row for row in doc.splitlines() if row.strip().startswith("LIMIT = "))
    return set(json.loads(re.sub(r"\b(str|bool|int|float)( \| null)?\b", "null", line.split("=", 1)[1])))


def _differences(documented, produced, path="") -> list[str]:
    """Where the output's shape leaves the documented one: a key missing or
    extra in an object, compared through every list's first element (a list
    the output leaves empty, like `errors` on a healthy device, is not entered)."""
    if isinstance(documented, dict):
        if not isinstance(produced, dict):
            return [f"{path}: not an object"]
        found = [f"{path}.{key}: undocumented" for key in produced.keys() - documented.keys()]
        found += [f"{path}.{key}: missing" for key in documented.keys() - produced.keys()]
        for key in documented.keys() & produced.keys():
            found += _differences(documented[key], produced[key], f"{path}.{key}")
        return found
    if isinstance(documented, list) and documented and isinstance(documented[0], dict):
        if not isinstance(produced, list):
            return [f"{path}: not a list"]
        return [diff for item in produced for diff in _differences(documented[0], item, f"{path}[]")]
    return []


def test_the_documented_schema_is_the_output(machine):
    configured(machine)
    healthy, _, _ = status("--refresh")
    (machine.home / ".config" / "probe" / "config.json").write_text("{")
    broken, _, _ = status()
    assert broken["errors"]  # so the `errors` rows are compared too
    for state in (healthy, broken):
        assert _differences(_documented_schema(), state) == []
    assert healthy["v"] == status_impl.SCHEMA_VERSION == 1


def test_human_output_without_json(machine):
    configured(machine)
    result = CliRunner().invoke(main.app, ["status"])
    assert result.exit_code == 0
    assert "Who records        daemon" in result.stdout
    assert "Claude Code" in result.stdout


@pytest.mark.parametrize("argv", [["status", "--json", "--bogus"], ["status", "--refresh", "--timeout", "0"]])
def test_a_usage_error_exits_2(machine, argv):
    assert CliRunner().invoke(main.app, argv).exit_code == 2


def test_stdout_is_only_the_object_even_when_a_reader_prints(machine, monkeypatch):
    real = status_impl._daemon  # noqa: SLF001

    def chatty(caps, **kwargs):
        print("a reader printing to stdout")
        return real(caps, **kwargs)

    monkeypatch.setattr(status_impl, "_daemon", chatty)
    state, _, result = status()
    assert state["v"] == 1
    assert "a reader printing to stdout" in result.stderr


# -- the real entry point: no `ps` where there is no /proc ---------------------


@pytest.fixture
def no_proc(monkeypatch):
    """A machine without /proc (macOS): finding this process's ancestors runs
    `ps` (`session_marker._ancestors`)."""
    real = os.path.isdir
    monkeypatch.setattr(os.path, "isdir", lambda path: False if str(path).startswith("/proc") else real(path))
    monkeypatch.setattr(agent_session, "_ADOPTED", False)


def harness_record() -> None:
    """A Kimi Code session recorded on this machine, so a walk has something to find."""
    folder = session_marker.harness_processes_dir()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "4242-0.json").write_text(
        json.dumps({"harness": "kimi_code", "session_id": "659a3020-6ec3-45c7-8f7b-274f811549be"})
    )


def test_the_real_entry_runs_no_ps_for_status(machine, no_proc, no_io, capfd):
    """`main.main`, not `main.app`: the harness-session adoption runs before
    the command is dispatched, and walked the ancestors with `ps`."""
    configured(machine)
    harness_record()
    assert main.main(["status", "--json"]) == 0
    state = json.loads(capfd.readouterr().out)
    assert no_io == []
    assert agent(state, "claude_code")["plugin_installed"] is True
    # Control: the walk it skipped does run `ps` here. (`no_proc` restores the flag.)
    agent_session._ADOPTED = False  # noqa: SLF001
    agent_session.adopt_harness_process_session()
    assert any("subprocess.Popen" in attempt for attempt in no_io)


def test_no_recorded_harness_session_means_no_ancestor_walk(machine, no_proc, no_io):
    """Every other command adopts; with nothing recorded there is nothing to
    find, so nothing is run to look."""
    assert agent_session.adopt_harness_process_session() == {}
    assert no_io == []


# -- --refresh: one budget for everything ---------------------------------------


@pytest.fixture
def old_slow_server(machine, monkeypatch):
    """A real server that predates `/v1/device-state` (404) and answers nothing
    else in time: `/v1/me` and the capture status sleep. Every request logged."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    seen: list[tuple[str, str, str]] = []
    release = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def _answer(self):
            seen.append((self.command, self.path.split("?")[0], self.headers.get("Authorization", "")))
            if self.path.startswith("/v1/device-state"):
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            release.wait(30)

        do_GET = do_POST = _answer

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    monkeypatch.setenv("PROBE_BASE_URL", base_url)
    monkeypatch.setattr(capabilities, "fetch_device_state", REAL_FETCH_DEVICE_STATE)
    monkeypatch.setattr(main, "_verify_read", REAL_VERIFY)
    for variable in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
        monkeypatch.delenv(variable, raising=False)
    try:
        yield SimpleNamespace(base_url=base_url, seen=seen)
    finally:
        release.set()
        server.shutdown()
        server.server_close()


def test_an_old_slow_server_is_asked_once_within_the_budget(machine, old_slow_server):
    configured(machine)
    save_context({"base_url": old_slow_server.base_url})
    state, elapsed, _ = status("--refresh", "--timeout", "1")
    assert elapsed <= 1 + 1.5, elapsed
    assert state["checks"]["device_state"] == {"state": "unsupported", "checked": True, "error": None}
    assert (state["account"]["email"], state["account"]["credential_valid"]) == (None, None)
    assert state["checks"]["mcp_token"]["error"] == "timed out after 1s"
    # The old way ONCE for every agent: one `/v1/me` with the CLI's token, one
    # capture status per paired agent -- never once per agent.
    paths = [(path, auth) for _method, path, auth in old_slow_server.seen]
    assert paths.count(("/v1/me", "Bearer probe_pat_api")) == 1
    assert sorted(auth for path, auth in paths if path == "/ingest/v1/sessions/status") == [
        "Bearer ros_ing_claude_code",
        "Bearer ros_ing_codex",
    ]


def test_hung_agents_server_and_token_check_all_fit_one_budget(machine, monkeypatch):
    """Every agent's plugin list at once, pi's sniff beside them, the server
    and the token check started first: each gets the whole second, and the
    read is not their sum."""
    configured(machine)
    hung(machine, "claude")
    hung(machine, "codex")
    hung(machine, "pi")
    REAL_PI_SNIFF.cache_clear()
    monkeypatch.setattr(setup, "pi_binary_available", REAL_PI_SNIFF)

    def slow(seconds, answer):
        def call(*_a, **_k):
            time.sleep(seconds)
            return answer

        return call

    monkeypatch.setattr(capabilities, "fetch_device_state", slow(5, DeviceState(DeviceStateOutcome.ANSWERED)))
    monkeypatch.setattr(main, "_verify_read", slow(5, ("ok", {"email": EMAIL})))
    try:
        state, elapsed, _ = status("--refresh", "--timeout", "1")
    finally:
        REAL_PI_SNIFF.cache_clear()
    assert elapsed < 3.0, elapsed
    for source in ("claude_code", "codex"):
        assert agent(state, source)["plugins"]["error"] == "timed out after 1s", source
    assert state["checks"]["mcp_token"] == {"state": None, "checked": False, "error": "timed out after 1s"}
    assert state["checks"]["device_state"]["state"] == "unreachable"
    assert sorted(agent_calls(machine)) == ["claude plugin list", "codex plugin list --json", "pi --help"]


def test_a_fractional_budget_is_said_as_it_is(machine):
    configured(machine)
    hung(machine, "claude")
    state, _, _ = status("--refresh", "--timeout", "0.5")
    assert agent(state, "claude_code")["plugins"]["error"] == "timed out after 0.5s"


@pytest.mark.skipif(not os.path.isdir("/proc"), reason="reads the child's state from /proc")
def test_a_timed_out_agent_cli_takes_its_children_with_it(machine):
    """npm's `codex` is node starting the native binary: killing the wrapper
    alone left the child running after the read had moved on."""
    configured(machine)
    child_pid = machine.tmp / "child.pid"
    agent_binary(machine, "claude", f'/bin/sleep 60 &\necho $! > "{child_pid}"\nwait')
    status("--refresh", "--timeout", "1")
    pid = int(child_pid.read_text())
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with open(f"/proc/{pid}/stat") as stat:
                if stat.read().split(")")[-1].split()[0] == "Z":
                    break  # killed; its new parent has yet to reap it
        except FileNotFoundError:
            break
        time.sleep(0.05)
    else:
        os.kill(pid, signal.SIGKILL)
        pytest.fail("the agent CLI's child outlived its timeout")


# -- the default read and --refresh agree on what they can both read -------------


def test_an_oauth_codex_on_the_agent_profile_reads_as_the_menu_draws_it(machine):
    configured(machine)
    codex_on_the_agent_profile(machine, mcp_list='[{"name": "probe-research", "auth_status": "o_auth"}]')
    refreshed, _, _ = status("--refresh")
    assert agent(refreshed, "codex")["mcp_state"] == "on"
    assert_menu_agrees(menu(machine), refreshed)
    local, _, _ = status()
    codex = agent(local, "codex")
    # Only `codex mcp list` can read an OAuth login, and the default read runs
    # nothing: unknown, and it says why -- not that the list did not answer.
    assert codex["mcp_state"] == "unknown"
    assert codex["mcp_detail"] == f"unknown: {doctor.CODEX_MCP_NOT_CHECKED}"
    same_state(local, refreshed, unread_mcp=("codex",))


# -- a config that cannot be read invalidates what it holds ---------------------


@pytest.mark.parametrize("refresh", [False, True])
def test_a_corrupt_config_leaves_what_it_holds_unknown(machine, refresh):
    """`[]` reads as an empty config everywhere else: Codex then records
    through itself, its checker looks for the wrong plugin and finds it
    "verified" absent, and Who records and the default fall back to defaults."""
    configured(machine)
    path = machine.home / ".config" / "probe" / "config.json"
    path.write_text("[]")
    state, _, _ = status(*(["--refresh"] if refresh else []))
    assert [error["field"] for error in state["errors"]] == ["config"]
    for row in state["agents"]:
        assert {key: row[key] for key in ("configured", "plugin_installed", "capture_on", "mcp_state", "recorder")} == (
            dict.fromkeys(("configured", "plugin_installed", "capture_on", "mcp_state", "recorder"))
        ), row["agent"]
        assert row["plugins"]["state"] == "unverified"
    assert agent(state, "codex")["installed"] is True
    assert set(state["account"].values()) == {None}
    assert (state["who_records"], state["session_default"], state["daemon"]["key_held"]) == (
        None,
        {"state": None, "env_override": None},
        None,
    )
    if refresh:
        assert all(check["error"] and not check["checked"] for check in state["checks"].values())


def test_an_environment_override_still_holds_the_default_with_a_corrupt_config(machine, monkeypatch):
    monkeypatch.setenv("PROBE_SESSION_STATE", "off")
    path = machine.home / ".config" / "probe" / "config.json"
    path.parent.mkdir(parents=True)
    path.write_text("[]")
    assert status()[0]["session_default"] == {"state": "off", "env_override": "off"}


def test_a_corrupt_autoupdate_file_is_an_error(machine):
    path = autoupdate.state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"enabled": tr')
    state, _, _ = status()
    assert [error["field"] for error in state["errors"]] == ["auto_update"]
    assert str(path) in state["errors"][0]["message"]
    assert state["auto_update"]["enabled"] is False  # what the menu shows for it


def test_the_versions_row_reads_the_ledger_claude_code_reads(machine, monkeypatch):
    """`CLAUDE_CONFIG_DIR` moves Claude Code's ledger; the plugin's version is
    graded off the same file the plugin row reads."""
    elsewhere = machine.tmp / "claude-config"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(elsewhere))
    ledger = elsewhere / "plugins" / "installed_plugins.json"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(
        json.dumps({"version": 2, "plugins": {"probe-research@research-os-agent": [{"version": "0.156.0"}]}})
    )
    assert versions._installed_plugins_path() == capabilities.claude_plugin_ledger() == ledger  # noqa: SLF001
    assert versions._plugin_versions().get("probe-research") == "0.156.0"  # noqa: SLF001


# -- two probes at once ---------------------------------------------------------

#: `running()` in a loop for argv[1] seconds; prints how often, and how often it said True.
PROBER = textwrap.dedent(
    """
    import sys, time
    from probe.cli import wizard_lock
    end = time.monotonic() + float(sys.argv[1])
    asked = busy = 0
    while time.monotonic() < end:
        asked += 1
        busy += wizard_lock.running() is True
    print(asked, busy)
    """
)


def test_two_probes_never_see_each_other_as_a_setup(machine):
    """The desktop app's probe and a second `probe status` at once: a shared
    lock never conflicts with another shared one (about 2% of probes in a tight
    loop did with an exclusive one)."""
    path = wizard_lock.lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    probers = [
        subprocess.Popen([sys.executable, "-c", PROBER, "2"], stdout=subprocess.PIPE, text=True)
        for _ in range(2)
    ]
    counts = [tuple(int(n) for n in prober.communicate(timeout=60)[0].split()) for prober in probers]
    assert all(asked > 1000 for asked, _ in counts), counts
    assert [busy for _, busy in counts] == [0, 0]


# -- the workspace limit (`probe workspace limit`) -----------------------------


_LIMITED = "11111111-1111-1111-1111-111111111111"


def _limit_this_computer(machine, **workspace) -> None:
    from probe.sdk.config import save_context

    save_context({"workspace": {"id": _LIMITED, "project": None, "limit": True, "name": "Eng", "slug": "eng",
                                **workspace}})


def test_the_workspace_limit_is_the_documented_object(machine):
    _limit_this_computer(machine, team_items="hide")
    local, _, _ = status()

    assert set(local["account"]["workspace_limit"]) == _documented_limit()
    assert local["account"]["workspace_limit"] == {"id": _LIMITED, "name": "Eng", "slug": "eng", "team_items": "hide"}
    assert local["v"] == status_impl.SCHEMA_VERSION == 1


def test_the_workspace_limit_is_read_locally_with_the_environment_on_top(machine, monkeypatch):
    """No network: `probe status` is read on every desktop focus. An environment
    slug is shown as a slug (its id would cost a request)."""
    _limit_this_computer(machine)
    monkeypatch.setenv("PROBE_WORKSPACE_LIMIT", "research")
    local, _, _ = status()
    assert local["account"]["workspace_limit"] == {"id": None, "name": None, "slug": "research", "team_items": "show"}

    monkeypatch.setenv("PROBE_WORKSPACE_LIMIT", "team")
    local, _, _ = status()
    assert local["account"]["workspace_limit"] is None


def test_the_whole_team_and_the_pin_alone_are_no_limit(machine):
    from probe.sdk.config import save_context

    save_context({"workspace": {"id": _LIMITED, "project": None}})
    local, _, _ = status()
    assert local["account"]["workspace_limit"] is None


def test_a_limited_computer_says_so_for_a_person(machine):
    _limit_this_computer(machine, team_items="hide")
    result = CliRunner().invoke(main.app, ["status"])
    assert result.exit_code == 0
    assert "Workspace limit    Eng (team-wide items hidden)" in result.stdout
