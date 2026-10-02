"""The wizard's "Who records" (daemon reads, T8): per coding agent, the agent
records (today, the full `probe-research` plugin) or the Probe daemon records
AND reads for it (the lean `probe-research-daemon` plugin).

The config key is the one fact everything else reads -- the daemon worker's
reader, `probe ask`, `probe session track`, and every install / update /
detection path that must not put the other profile's plugin back.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from probe.cli import agent_rules, capabilities, daemon_cli, plugin_cli, updater
from probe.cli import setup as wizard
from probe.cli.capabilities import Capabilities
from probe.cli.claude_cli import Result
from probe.daemon import mailbox
from probe.sdk import session_marker

SID = "44444444-5555-6666-7777-888888888888"
#: The real `probe daemon install`, taken before conftest swaps in its tripwire.
_REAL_DAEMON_INSTALL = daemon_cli.daemon_install
_AGENT_ENV = (
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CODE_SESSION_ID",
    "CODEX_SANDBOX",
    "CODEX_THREAD_ID",
    "PI_CODING_AGENT",
    "PI_SESSION_ID",
    "CURSOR_TRACE_ID",
    "PROBE_AGENT",
    "PROBE_SESSION_STATE",
    "PROBE_SESSION_TRACKING",
    mailbox.ENV_READS,
)


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    for name in _AGENT_ENV:
        monkeypatch.delenv(name, raising=False)
    return tmp_path


def _config(tmp_path: Path) -> dict:
    return json.loads((tmp_path / "probe" / "config.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# The config: `defaults.recorders`, absent = agent.
# ---------------------------------------------------------------------------


def test_recorder_round_trip(isolate):
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_AGENT
    session_marker.write_default_state(session_marker.STATE_READ_ONLY)
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_DAEMON
    assert session_marker.recorder("codex") == session_marker.RECORDER_AGENT
    defaults = _config(isolate)["defaults"]
    assert defaults["recorders"] == {"claude_code": "daemon"}
    assert defaults["session_state"] == "read-only", "the other defaults are kept"
    session_marker.write_recorder("claude_code", session_marker.RECORDER_AGENT)
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_AGENT
    assert "recorders" not in _config(isolate)["defaults"], "agent is the absence of the key"
    with pytest.raises(ValueError):
        session_marker.write_recorder("claude_code", "both")


@pytest.mark.parametrize(
    "config",
    [{}, {"defaults": []}, {"defaults": {"recorders": "daemon"}}, {"defaults": {"recorders": {"claude_code": "yes"}}}],
)
def test_an_odd_config_reads_as_the_agent(config):
    assert session_marker.recorder("claude_code", config) == session_marker.RECORDER_AGENT
    assert session_marker.recorder(None, config) == session_marker.RECORDER_AGENT


def test_the_hooks_copy_reads_the_same_key(isolate):
    """Hooks load the vendored `_session_marker.py` (stdlib only)."""
    import importlib.util

    path = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks" / "_session_marker.py"
    spec = importlib.util.spec_from_file_location("_vendored_marker_recorder", path)
    vendored = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vendored)
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    assert vendored.recorder("codex") == vendored.RECORDER_DAEMON
    assert vendored.recorder("claude_code") == vendored.RECORDER_AGENT


# ---------------------------------------------------------------------------
# The reader, `probe ask`, `probe session track`.
# ---------------------------------------------------------------------------


def test_reads_are_on_for_the_daemon_profiles_agent_only(isolate, monkeypatch):
    assert mailbox.enabled(source="claude_code") is False
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert mailbox.enabled(source="claude_code") is True
    assert mailbox.enabled(source="codex") is False
    assert mailbox.enabled() is False, "without a source only the developer override counts"
    monkeypatch.setenv(mailbox.ENV_READS, "on")
    assert mailbox.enabled(source="codex") is True and mailbox.enabled() is True, "the override still works"


def _ask(*args):
    from probe.cli.main import app

    return CliRunner().invoke(app, ["ask", *args])


def test_probe_ask_answers_by_the_calling_agents_profile(isolate, monkeypatch):
    assert session_marker.set_session_state(SID, session_marker.STATE_DAEMON)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    assert daemon_cli.ASK_NO_DAEMON in _ask("any prior SVM sweeps?").output
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    assert daemon_cli.ASK_NO_DAEMON in _ask("any prior SVM sweeps?").output, "Codex's profile is not Claude Code's"
    assert mailbox.pending_asks(SID) == []
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    res = _ask("any prior SVM sweeps?")
    assert res.exit_code == 0, res.output
    assert mailbox.pending_asks(SID)[0].question == "any prior SVM sweeps?"


def test_the_codex_thread_is_codexs(isolate, monkeypatch):
    monkeypatch.setenv("CODEX_THREAD_ID", SID)
    assert daemon_cli.calling_agent() == "codex"
    monkeypatch.delenv("CODEX_THREAD_ID")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    assert daemon_cli.calling_agent() == "claude_code"


def test_session_track_is_daemon_in_the_daemon_profile(isolate, monkeypatch):
    from probe.cli.main import app

    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    assert CliRunner().invoke(app, ["session", "track"]).exit_code == 0
    assert session_marker.session_state(SID) == session_marker.STATE_FULL
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert CliRunner().invoke(app, ["session", "untrack"]).exit_code == 0
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    assert CliRunner().invoke(app, ["session", "track"]).exit_code == 0
    assert session_marker.session_state(SID) == session_marker.STATE_DAEMON, "the daemon profile's `on`"


# ---------------------------------------------------------------------------
# One plugin name per profile, everywhere.
# ---------------------------------------------------------------------------


def test_the_lean_plugin_is_not_read_as_the_full_one(monkeypatch):
    listing = "probe-research-daemon@research-os-agent 0.107.1\nprobe-research-tap@research-os-agent 0.9.1\n"
    monkeypatch.setattr(plugin_cli, "list_plugins", lambda _source: Result(ok=True, detail=listing))
    names = capabilities.installed_plugins(source="claude_code").names
    assert names == frozenset({"probe-research-daemon", "probe-research-tap"})


def test_install_update_and_detection_follow_the_profile(isolate):
    assert capabilities.tracking_plugin_name("claude_code") == "probe-research"
    assert updater.tracking_plugin_id() == "probe-research@research-os-agent"
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert capabilities.tracking_plugin_name("claude_code") == "probe-research-daemon"
    assert capabilities.tracking_plugin_name("codex") == "probe-research"
    assert updater.tracking_plugin_id() == "probe-research-daemon@research-os-agent"
    assert "claude plugin update probe-research-daemon@research-os-agent" in updater.manual_plugin_commands()


def test_the_codex_update_re_adds_the_profiles_plugin(isolate, monkeypatch):
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    added: list[str] = []
    monkeypatch.setattr(updater.shutil, "which", lambda _name: "/usr/bin/codex")
    monkeypatch.setattr(updater.plugin_cli, "refresh_marketplace", lambda *_a: Result(ok=True))
    monkeypatch.setattr(updater.plugin_cli, "install", lambda _src, plugin_id: added.append(plugin_id) or Result(ok=True))
    monkeypatch.setattr(updater, "_codex_plugin_versions", lambda *_a: {})
    updater.update_codex_plugins()
    assert added == ["probe-research-daemon@research-os-agent", "probe-research-tap@research-os-agent"]


def test_a_rerun_of_the_rules_keeps_the_daemon_blurb(isolate, monkeypatch):
    monkeypatch.setattr(wizard, "apply_statusline", lambda: [])
    monkeypatch.setattr(wizard, "seed_team_note_block", lambda: [])
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    wizard.apply_agent_rules(True)
    path = agent_rules.memory_path("claude_code")
    assert agent_rules.installed_profile(path) is agent_rules.Profile.DAEMON
    assert agent_rules.DAEMON_POINTER_BODY in path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# apply_recorder: the wizard's apply path.
# ---------------------------------------------------------------------------


class Calls:
    def __init__(self, monkeypatch, *, fail: str | None = None, key_granted: bool = True):
        self.log: list[tuple] = []
        self.key = {"held": False}
        monkeypatch.setattr(wizard, "install_plugin", self.install)
        monkeypatch.setattr(wizard, "uninstall_plugin", self.uninstall)
        monkeypatch.setattr(wizard, "companion_token_held", lambda: self.key["held"])
        monkeypatch.setattr(wizard, "_revoke", self.revoke)
        self.fail = fail
        # A machine that can run the daemon, whatever this test runner has
        # installed, and whose agent CLI answers the plugin listing.
        from probe.cli import capabilities, daemon_cli

        monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "test")
        monkeypatch.setattr(capabilities, "installed_plugins", lambda **_kw: capabilities.PluginState(
            names=frozenset({wizard.TRACKING_PLUGIN_NAME, wizard.DAEMON_PLUGIN_NAME}), verified=True))

        def provision(base_url, **_kw):
            self.log.append(("mint", base_url))
            self.key["held"] = key_granted
            return ["The Probe daemon has its own key."] if key_granted else ["! declined"]

        from probe.cli import companion

        monkeypatch.setattr(companion, "provision_daemon", provision)

    def revoke(self, token, *, base_url, what):
        self.log.append(("revoke", base_url))
        return [f"released {what}"]

    def install(self, name, *, source=None, on_retry=None):
        self.log.append(("install", name, source))
        return Result(ok=name != self.fail, detail="boom" if name == self.fail else "")

    def uninstall(self, name, *, source=None):
        self.log.append(("uninstall", name, source))
        return Result(ok=True)


def _claude_md(isolate) -> Path:
    path = agent_rules.memory_path("claude_code")
    agent_rules.install(path)
    return path


def test_moving_an_agent_to_the_daemon(isolate, monkeypatch):
    calls = Calls(monkeypatch)
    path = _claude_md(isolate)
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True, capture_plugin_installed=False)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert calls.log == [
        ("mint", "https://api.test"),
        ("install", "probe-research-tap", "claude_code"),
        ("install", "probe-research-daemon", "claude_code"),
        ("uninstall", "probe-research", "claude_code"),
    ]
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_DAEMON
    assert agent_rules.installed_profile(path) is agent_rules.Profile.DAEMON
    assert agent_rules.POINTER_BODY not in path.read_text(encoding="utf-8")
    # The machine-wide default is left alone: the lean plugin starts an `on`
    # session in `daemon` itself, and another agent keeps its own behaviour.
    assert session_marker.default_session_state() == session_marker.STATE_FULL
    assert "Who records in Claude Code → the daemon" in lines
    assert not [line for line in lines if line.startswith("Probe in new sessions")]
    assert lines[-1] == "Takes effect in new Claude Code sessions."
    assert not [line for line in lines if line.startswith("!")]


def test_no_key_no_move(isolate, monkeypatch):
    calls = Calls(monkeypatch, key_granted=False)
    path = _claude_md(isolate)
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert calls.log == [("mint", "https://api.test")], "no plugin touched"
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_AGENT
    assert agent_rules.installed_profile(path) is agent_rules.Profile.AGENT
    assert lines[-1] == "! Claude Code stays on agent: the daemon has no key."


def test_a_failed_install_stops_before_anything_is_removed(isolate, monkeypatch):
    calls = Calls(monkeypatch, fail="probe-research-daemon")
    calls.key["held"] = True
    path = _claude_md(isolate)
    caps = Capabilities(agent_source="codex", tracking_plugin_installed=True, capture_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert calls.log == [("install", "probe-research-daemon", "codex")], "key held and tap present: neither redone"
    assert session_marker.recorder("codex") == session_marker.RECORDER_AGENT
    assert agent_rules.installed_profile(path) is agent_rules.Profile.AGENT, "Claude Code's file untouched"
    assert lines[0] == "! could not install probe-research-daemon for Codex: boom"
    assert "Nothing else changed" in lines[1]


def test_back_to_the_agent(isolate, monkeypatch):
    from probe.sdk.config import load_context, save_context

    calls = Calls(monkeypatch)
    calls.key["held"] = True
    save_context({"companion_token": "probe_pat_" + "1" * 32})
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    session_marker.write_default_state(session_marker.STATE_DAEMON)
    path = agent_rules.memory_path("claude_code")
    agent_rules.install(path, block=agent_rules.render_block(profile=agent_rules.Profile.DAEMON))
    # Read under the daemon profile: "tracking plugin installed" is the lean one.
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True, capture_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_AGENT, base_url="https://api.test")
    # Nothing records through the daemon any more: its key goes (the tracking
    # default has no `daemon` position to revoke it from since 2026-09-29).
    assert calls.log == [
        ("install", "probe-research", "claude_code"),
        ("revoke", "https://api.test"),
        ("uninstall", "probe-research-daemon", "claude_code"),
    ]
    assert not (load_context() or {}).get("companion_token")
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_AGENT
    assert agent_rules.installed_profile(path) is agent_rules.Profile.AGENT
    assert session_marker.default_session_state() == session_marker.STATE_FULL
    assert "Who records in Claude Code → the agent" in lines


def test_back_to_the_agent_keeps_the_key_while_a_daemon_session_is_open(isolate, monkeypatch):
    """Revoking now would stop a session the daemon is recording mid-way; the
    plugin swap only reaches new sessions (review of #2172)."""
    from probe.sdk.config import load_context, save_context

    calls = Calls(monkeypatch)
    calls.key["held"] = True
    save_context({"companion_token": "probe_pat_" + "1" * 32})
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    monkeypatch.setattr(wizard, "live_daemon_sessions", lambda: 2)
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True, capture_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_AGENT, base_url="https://api.test")
    assert ("revoke", "https://api.test") not in calls.log
    assert (load_context() or {}).get("companion_token")
    assert any("Kept the daemon's key: 2 open session(s)" in line for line in lines)


def test_back_to_the_agent_keeps_the_default_another_agent_still_needs(isolate, monkeypatch):
    from probe.sdk.config import save_context

    calls = Calls(monkeypatch)
    calls.key["held"] = True
    save_context({"companion_token": "probe_pat_" + "1" * 32})
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    session_marker.write_default_state(session_marker.STATE_DAEMON)
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True)
    wizard.apply_recorder(caps, session_marker.RECORDER_AGENT, base_url="https://api.test")
    assert session_marker.default_session_state() == session_marker.STATE_DAEMON, "Codex still records by daemon"
    assert ("revoke", "https://api.test") not in calls.log, "Codex still needs the daemon's key"
    assert not agent_rules.is_installed(agent_rules.memory_path("claude_code")), "an opted-out file stays opted out"


# ---------------------------------------------------------------------------
# The row: Defaults › Who records on the main menu, ONE value for the machine,
# switched with ←/→ and applied at once (Richard 2026-09-29).
# ---------------------------------------------------------------------------


def test_the_row_sits_above_the_default_for_new_sessions():
    from probe.cli.actions import ACTION_GROUPS, Action, DEVICE_ACTIONS

    assert dict(ACTION_GROUPS)["Defaults"] == (Action.RECORDER, Action.DEFAULTS)
    assert Action.RECORDER in DEVICE_ACTIONS, "one value for the device, not one per agent"


def test_the_row_wears_the_machines_value(isolate):
    assert wizard.machine_recorder() == session_marker.RECORDER_AGENT
    title, detail = wizard.recorder_row()
    assert title == "Who records  ‹ agent ›" and detail
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    assert wizard.machine_recorder() == session_marker.RECORDER_DAEMON, "no per-agent split"
    assert wizard.recorder_row()[0] == "Who records  ‹ daemon ›"
    choices = wizard.action_choices()
    assert any("Who records  ‹ daemon ›" in str(getattr(c, "title", "")) for c in choices)


class _Tel:
    """The telemetry context, as the list of events it was asked to emit."""

    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def emit(self, event, **props):
        self.events.append((event, props))


def _recorder(monkeypatch, *, chosen, offered=True, page=None, key=True, spins=None, tel=None, stuck=(),
              yes=False, libraries="test", signed_in=True, refused=False):
    import contextlib

    from probe.cli import daemon_cli, tui

    if signed_in:
        monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "1" * 32)
    else:
        monkeypatch.delenv("PROBE_TOKEN", raising=False)

    # "test" pins the libraries installed, False pins them missing, None leaves
    # `ai_libraries` to the test.
    if libraries is not None:
        monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: libraries or None)

    cli_main = importlib.import_module("probe.cli.main")
    applied: list = []
    pages: list = []
    events = spins if spins is not None else []

    @contextlib.contextmanager
    def working(label):
        events.append(("spin", label))
        yield
        events.append(("done", label))

    monkeypatch.setattr(tui, "working", working)
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(wizard, "companion_token_held", key if callable(key) else (lambda: key))
    monkeypatch.setattr(wizard, "daemon_availability",
                        lambda base_url=None: events.append(("ask", None)) or (offered, None))

    def apply(caps, value, *, base_url):
        applied.append((caps.agent_source, value))
        if caps.agent_source in stuck:
            return [f"! could not install for {caps.agent_source}"]
        session_marker.write_recorder(caps.agent_source, value)
        return [f"moved {caps.agent_source}"]

    monkeypatch.setattr(wizard, "apply_recorder", apply)
    monkeypatch.setattr(cli_main, "_run_daemon_page", lambda **kw: pages.append(1) or page)
    monkeypatch.setattr(cli_main, "_daemon_key_refused", lambda base: refused)
    caps = {"claude_code": Capabilities(), "codex": Capabilities(agent_source="codex")}
    lines = cli_main._run_recorder_action(
        yes=yes, caps_by_source=caps, base_now="https://api.test", chosen=chosen, telemetry=tel
    )
    return applied, pages, lines


def _changed(tel: _Tel) -> list[dict]:
    from probe.cli import telemetry as tm

    return [props for event, props in tel.events if event == tm.EVENT_WIZARD_RECORDER_CHANGED]


def test_turning_the_daemon_on_is_reported_with_the_agents_that_moved(isolate, monkeypatch):
    from probe.cli import telemetry as tm

    tel = _Tel()
    _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel)
    (props,) = _changed(tel)
    assert props["recorder"] == "daemon" and props["outcome"] == tm.RecorderOutcome.MOVED
    assert props["agents"] == ["claude_code", "codex"] and props["agent_count"] == 2
    assert props["duration_seconds"] >= 0


def test_turning_the_daemon_off_is_reported_too(isolate, monkeypatch):
    from probe.cli import telemetry as tm

    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    tel = _Tel()
    _recorder(monkeypatch, chosen=session_marker.RECORDER_AGENT, tel=tel)
    (props,) = _changed(tel)
    assert (props["recorder"], props["outcome"]) == ("agent", tm.RecorderOutcome.MOVED)


def test_an_agent_that_did_not_move_makes_it_partial(isolate, monkeypatch):
    """Read back from each agent's saved config: `apply_recorder` reports a
    failure as a line and carries on, so the steps that ran prove nothing."""
    from probe.cli import telemetry as tm

    tel = _Tel()
    _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel, stuck=("codex",))
    (props,) = _changed(tel)
    assert props["outcome"] == tm.RecorderOutcome.PARTIAL and props["agents"] == ["claude_code"]
    session_marker.write_recorder("claude_code", session_marker.RECORDER_AGENT)
    tel = _Tel()
    _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel, stuck=("claude_code", "codex"))
    assert _changed(tel)[0]["outcome"] == tm.RecorderOutcome.FAILED


def test_a_plan_refusal_and_a_missing_key_are_reported_before_anything_moves(isolate, monkeypatch):
    """Someone asked for the daemon and was told no: the sales signal."""
    from probe.cli import telemetry as tm

    tel = _Tel()
    _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel, offered=False)
    (props,) = _changed(tel)
    assert (props["outcome"], props["agents"]) == (tm.RecorderOutcome.REFUSED_PLAN, [])
    monkeypatch.setattr("probe.cli.companion.provision_daemon", lambda base, **_kw: ["declined"])
    tel = _Tel()
    applied, _pages, _lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel, key=False)
    assert applied == [] and _changed(tel)[0]["outcome"] == tm.RecorderOutcome.NO_KEY


def test_enter_on_the_row_reports_nothing(isolate, monkeypatch):
    tel = _Tel()
    _recorder(monkeypatch, chosen=None, tel=tel)
    assert tel.events == []


def test_switching_to_the_daemon_moves_every_agent_then_asks_what_it_sees(isolate, monkeypatch):
    applied, pages, lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, page=["reasoning → on"])
    assert applied == [("claude_code", "daemon"), ("codex", "daemon")], "no codex/claude split"
    assert pages == [1], "the daemon's page, straight after the switch"
    assert lines == ["moved claude_code", "moved codex", "reasoning → on"]


def test_the_check_and_the_move_show_the_spinner_never_a_blank_screen(isolate, monkeypatch):
    spins: list = []
    _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, spins=spins)
    assert spins[:3] == [
        ("spin", "Checking the Probe daemon is open to your team"),
        ("ask", None),
        ("done", "Checking the Probe daemon is open to your team"),
    ], "the paid-plan answer is awaited under the spinner"
    assert spins[3][0] == "spin" and "daemon" in spins[3][1], "and so are the plugin moves"


def test_the_daemons_sign_in_runs_before_the_spinner(isolate, monkeypatch):
    """It prints the approval link and waits on the browser: never under a spinner."""
    from probe.cli import companion

    spins: list = []
    held = {"key": False}

    def provision(base_url, **_kw):
        spins.append(("sign-in", None))
        held["key"] = True
        return ["The Probe daemon has its own key."]

    monkeypatch.setattr(companion, "provision_daemon", provision)
    applied, _pages, lines = _recorder(
        monkeypatch, chosen=session_marker.RECORDER_DAEMON, spins=spins, key=lambda: held["key"]
    )
    order = [kind for kind, _ in spins]
    assert order[:4] == ["spin", "ask", "done", "sign-in"], "checked, THEN signed in, outside any spinner"
    assert order[4] == "spin", "the plugin moves come after, under the spinner"
    assert applied == [("claude_code", "daemon"), ("codex", "daemon")]
    assert lines[0] == "The Probe daemon has its own key."


def test_a_held_key_with_missing_libraries_installs_them_without_an_approval(isolate, monkeypatch):
    """The "missing packages" failure (2026-09-29): the key was held, so the
    switch skipped provisioning, and the move then refused for the libraries it
    never installed. R12: the libraries install, visibly, with no approval."""
    from probe.cli import daemon_cli

    cli_main = importlib.import_module("probe.cli.main")
    installed = {"version": None}

    def never(*_a, **_k):
        raise AssertionError("a held key is never approved again")

    monkeypatch.setattr(cli_main, "_authorize_companion", never)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: installed["version"])
    monkeypatch.setattr(daemon_cli, "daemon_install", lambda: installed.update(version="2.51"))
    applied, _pages, _lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, libraries=None)
    assert installed["version"] == "2.51"
    assert applied == [("claude_code", "daemon"), ("codex", "daemon")]


def test_libraries_that_do_not_install_move_nothing(isolate, monkeypatch):
    from probe.cli import daemon_cli
    from probe.cli import telemetry as tm

    def fails():
        raise typer.Exit(1)

    monkeypatch.setattr(daemon_cli, "daemon_install", fails)
    tel = _Tel()
    applied, pages, lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel, libraries=False)
    assert applied == [] and pages == []
    assert lines[-1] == "! The daemon's AI libraries are missing, so nothing changed."
    assert _changed(tel)[-1]["outcome"] == tm.RecorderOutcome.NO_LIBRARIES


def _installed_probe(tmp_path: Path, *, installs: bool = True) -> Path:
    """A uv tool install as `~/.local/bin/probe` reaches it: `bin/probe`, whose
    `daemon install` adds the extra (or fails), and `bin/python`, which imports
    the AI libraries only once that ran."""
    env = tmp_path / "tools" / "probe-research" / "bin"
    env.mkdir(parents=True)
    marker = tmp_path / "daemon-extra"
    (env / "probe").write_text(
        '#!/bin/sh\n[ "$1 $2" = "daemon install" ] || exit 64\n'
        + (f'touch "{marker}"\n' if installs else "exit 1\n")
    )
    (env / "python").write_text(f'#!/bin/sh\n[ -f "{marker}" ] && echo 2.51\n')
    for script in ("probe", "python"):
        (env / script).chmod(0o755)
    link = tmp_path / "bin" / "probe"
    link.parent.mkdir()
    link.symlink_to(env / "probe")
    return link


def _run_from_npx(monkeypatch, probe_bin: Path) -> None:
    """This wizard is `npx probe-research`'s temporary copy in uv's cache, and
    `probe_bin` is the installed `probe` the tap starts the daemon from."""
    from probe.cli import bootstrap

    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.EPHEMERAL))
    monkeypatch.setattr(bootstrap, "_installed_binary", lambda: str(probe_bin))
    monkeypatch.setattr(daemon_cli, "daemon_install", _REAL_DAEMON_INSTALL)
    monkeypatch.setattr(daemon_cli, "_installed_copy_ready", {})


def test_a_switch_run_from_npx_installs_the_libraries_into_the_installed_probe(isolate, monkeypatch):
    """The update bug (2026-10-01): an installed `probe` behind the latest makes
    `npx probe-research` run the wizard from uv's cache, a copy the daemon never
    runs from. The check read that copy, and its install was refused
    (`Method.EPHEMERAL`), so every switch to the daemon said the AI libraries
    were missing until Probe was installed again. The installed `probe` is now
    asked, and installs into its own environment."""
    from probe.cli import telemetry as tm

    _run_from_npx(monkeypatch, _installed_probe(isolate))
    tel = _Tel()
    applied, _pages, _lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel,
                                        libraries=None)
    assert (isolate / "daemon-extra").exists(), "the installed probe ran its own `daemon install`"
    assert applied == [("claude_code", "daemon"), ("codex", "daemon")]
    assert _changed(tel)[-1]["outcome"] == tm.RecorderOutcome.MOVED


def test_a_failed_install_into_the_installed_probe_moves_nothing(isolate, monkeypatch):
    from probe.cli import telemetry as tm

    _run_from_npx(monkeypatch, _installed_probe(isolate, installs=False))
    tel = _Tel()
    applied, _pages, lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel,
                                       libraries=None)
    assert daemon_cli.ai_libraries() is None, "the installed copy answers, never uv's cache"
    assert applied == []
    assert lines[-1] == "! The daemon's AI libraries are missing, so nothing changed."
    assert _changed(tel)[-1]["outcome"] == tm.RecorderOutcome.NO_LIBRARIES


def test_a_headless_switch_applies_and_opens_no_page(isolate, monkeypatch):
    """R7: `probe wizard --yes --who-records daemon` moves every agent, as the
    row does, and never draws the daemon's page."""
    applied, pages, _lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, yes=True)
    assert applied == [("claude_code", "daemon"), ("codex", "daemon")] and pages == []


def test_the_who_records_flag_reaches_the_recorder_action(isolate, monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")
    seen = {}
    monkeypatch.setattr(cli_main, "_wizard_session", lambda **kw: seen.update(kw))
    res = CliRunner().invoke(cli_main.app, ["wizard", "--yes", "--who-records", "daemon"])
    assert res.exit_code == 0, res.output
    assert (seen["action"], seen["who_records"]) == ("recorder", "daemon")


def test_switching_back_to_the_agent_moves_every_agent_and_asks_nothing(isolate, monkeypatch):
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    applied, pages, _lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_AGENT)
    assert applied == [("claude_code", "agent")], "Codex was already on the agent: left alone"
    assert pages == []


def test_a_switch_to_where_every_agent_already_is_moves_nothing(isolate, monkeypatch):
    applied, _pages, lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_AGENT, yes=True)
    assert applied == [] and lines == ["Who records: already agent for every coding agent here."]


def test_a_signed_out_machine_switches_nothing(isolate, monkeypatch):
    applied, pages, lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, signed_in=False)
    assert applied == [] and pages == []
    assert lines[0].startswith("Sign in before switching Who records") and lines[-1] == "Nothing changed."


def test_enter_on_the_daemon_row_replaces_a_refused_key(isolate, monkeypatch):
    """A key revoked on the dashboard: Enter on the row is the repair (switching
    away and back would revoke the key and ask for a second approval)."""
    from probe.cli import companion

    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    from probe.sdk.config import load_context, save_context

    save_context({"companion_token": "probe_pat_" + "9" * 32})
    seen = []

    def provision(base, **kw):
        seen.append(load_context().get("companion_token"))
        save_context({"companion_token": "probe_pat_" + "8" * 32})
        return ["The Probe daemon has its own key."]

    monkeypatch.setattr(companion, "provision_daemon", provision)
    applied, pages, lines = _recorder(monkeypatch, chosen=None, refused=True)
    assert seen == [None], "the refused key is dropped before the new approval"
    assert applied == [] and pages == [1]
    assert lines[0] == "The server refuses the Probe daemon's key, so it needs a new one."


def test_a_declined_re_approval_leaves_no_key_and_moves_nothing(isolate, monkeypatch):
    """Declining the new approval must not read as success: the refused key is
    gone, so the switch reports NO_KEY instead of moving onto a dead key."""
    from probe.cli import companion
    from probe.cli import telemetry as tm
    from probe.sdk.config import load_context, save_context

    save_context({"companion_token": "probe_pat_" + "9" * 32})
    monkeypatch.setattr(companion, "provision_daemon", lambda base, **kw: ["! approval declined"])
    tel = _Tel()
    applied, _pages, lines = _recorder(
        monkeypatch, chosen=session_marker.RECORDER_DAEMON, tel=tel, refused=True,
        key=lambda: bool(load_context().get("companion_token")),
    )
    assert applied == [] and _changed(tel)[-1]["outcome"] == tm.RecorderOutcome.NO_KEY
    assert lines[-1] == "! The daemon has no key, so nothing changed."


def test_a_signed_out_machine_can_still_leave_the_daemon(isolate, monkeypatch):
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    applied, _pages, _lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_AGENT, signed_in=False)
    assert applied == [("claude_code", "agent")]


def test_enter_on_the_daemon_row_installs_missing_libraries(isolate, monkeypatch):
    from probe.cli import daemon_cli

    cli_main = importlib.import_module("probe.cli.main")
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    installed = {"version": None}

    def never(*_a, **_k):
        raise AssertionError("a held key is never approved again")

    monkeypatch.setattr(cli_main, "_authorize_companion", never)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: installed["version"])
    monkeypatch.setattr(daemon_cli, "daemon_install", lambda: installed.update(version="2.51"))
    _recorder(monkeypatch, chosen=None, libraries=None)
    assert installed["version"] == "2.51"


def test_who_records_with_a_sign_in_flag_is_refused(isolate, monkeypatch):
    cli_main = importlib.import_module("probe.cli.main")

    def forbidden(**_kw):
        raise AssertionError("neither a sign-in nor a switch may run")

    monkeypatch.setattr(cli_main, "_login", forbidden)
    monkeypatch.setattr(cli_main, "_wizard_session", forbidden)
    for extra in (["--no-browser"], ["--context", "gpu"], ["--token", "probe_pat_x"]):
        res = CliRunner().invoke(cli_main.app, ["wizard", "--yes", "--who-records", "daemon", *extra])
        assert res.exit_code == 2, (extra, res.output)


def test_a_team_the_daemon_is_closed_to_is_told_and_nothing_moves(isolate, monkeypatch):
    applied, pages, lines = _recorder(monkeypatch, chosen=session_marker.RECORDER_DAEMON, offered=False)
    assert applied == [] and pages == []
    assert lines == [wizard.DAEMON_PAID_ONLY_NOTE, "Nothing changed."]


def test_enter_on_the_row_opens_the_daemons_page_only_when_it_records(isolate, monkeypatch):
    applied, pages, lines = _recorder(monkeypatch, chosen=None)
    assert (applied, pages, lines) == ([], [], None), "on the agent, Enter does nothing"
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    applied, pages, _lines = _recorder(monkeypatch, chosen=None)
    assert applied == [] and pages == [1]


def test_the_menu_routes_a_switch_to_the_recorder_action():
    from probe.cli.actions import Action

    assert wizard.RecorderChoice("daemon").value == "daemon"
    switch = wizard._RecorderSwitch(wizard.action_choices())
    assert switch.row is not None and switch.row.value is Action.RECORDER
    assert switch.hint(Action.RECORDER) == "← → switch"
    assert switch.hint(Action.DEFAULTS) is None


def test_headless_says_who_records_and_where_to_switch_it(isolate):
    cli_main = importlib.import_module("probe.cli.main")
    lines = cli_main._run_recorder_action(yes=True, caps_by_source={"claude_code": Capabilities()})
    assert lines[0] == "Who records: agent" and "Defaults › Who records" in lines[-1]
    lines = cli_main._run_settings_action(yes=True, caps_by_source={"claude_code": Capabilities()})
    assert [line.split() for line in lines if "Who records" in line] == [["Who", "records", "agent"]]


def test_apply_settings_refuses_the_row():
    with pytest.raises(AssertionError, match="apply_recorder"):
        wizard.apply_settings({wizard.Setting.RECORDER_CLAUDE_CODE: "daemon"})


def test_the_wizard_still_accepts_experimental_but_does_not_advertise_it():
    from probe.cli.main import app

    import re

    res = CliRunner().invoke(app, ["wizard", "--help"], env={"NO_COLOR": "1", "COLUMNS": "200", "TERM": "dumb"})
    assert "--experimental" not in re.sub(r"\x1b\[[0-9;]*m", "", res.output)


def test_no_ai_libraries_no_move(isolate, monkeypatch):
    """Without the daemon's AI libraries the worker cannot start, and in the
    daemon profile the agent cannot record either: provisioning is tried (it
    installs them), and when they are still missing nothing moves."""
    from probe.cli import daemon_cli

    calls = Calls(monkeypatch)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: None)
    caps = Capabilities(agent_source="claude_code", tracking_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert calls.log == [("mint", "https://api.test")], "provisioned, and no plugin touched"
    assert session_marker.recorder("claude_code") == session_marker.RECORDER_AGENT
    assert "AI libraries are missing" in lines[-1]


def test_codex_on_the_daemon_loses_the_mcp_and_a_rerun_does_not_bring_it_back(isolate, monkeypatch):
    from probe.cli import codex_config

    Calls(monkeypatch)
    removed = []
    monkeypatch.setattr(codex_config, "remove_mcp_server", lambda name, **kw: removed.append(name))
    caps = Capabilities(agent_source="codex", tracking_plugin_installed=True, capture_plugin_installed=True)
    lines = wizard.apply_recorder(caps, session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert removed == ["probe-research"]
    assert wizard.sync_codex_mcp_token() == [], "the token sync leaves a daemon-profile Codex alone"
    assert lines[-1] == "In the new Codex session: `/hooks` › approve the Probe hooks.", (
        "Codex skips an untrusted hook silently: the daemon's messages would never arrive")
    back = wizard.apply_recorder(caps, session_marker.RECORDER_AGENT, base_url="https://api.test")
    assert not any("/hooks" in line for line in back)


def test_session_track_from_a_terminal_honours_the_sessions_profile(isolate, monkeypatch):
    sid = "11111111-2222-3333-4444-555555555555"
    session_marker.mark_session_profile(sid, session_marker.RECORDER_DAEMON)
    assert session_marker.session_profile(sid) == session_marker.RECORDER_DAEMON
    for var in ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID"):
        monkeypatch.delenv(var, raising=False)
    from typer.testing import CliRunner

    from probe.cli.main import app

    result = CliRunner().invoke(app, ["session", "track", "--session", sid])
    assert session_marker.session_state(sid) == session_marker.STATE_DAEMON, result.output
