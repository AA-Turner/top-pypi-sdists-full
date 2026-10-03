"""pi on the Probe daemon ("Who records" = daemon).

pi has one package, so its daemon profile is the package's settings entry
(narrowed to the daemon's skills) plus the extension switching itself from the
profile `probe session initialize` reports. These tests cover the CLI half:
the wizard's switch, the session seed, and doctor.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from probe.cli import agent_rules, pi_config
from probe.cli import setup as wizard
from probe.cli.capabilities import Capabilities
from probe.cli.claude_cli import Result
from probe.sdk import session_marker

AGENT = Path(__file__).resolve().parents[1]
SID = "0f8c6a1e-7b2d-4c3e-9a1f-5d6e7f8a9b0c"


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path / "pi-tap"))
    for name in ("PROBE_AGENT", "PROBE_TAP_SOURCE", "PI_SESSION_ID", "PI_CODING_AGENT", "PROBE_PI_TAP_TOKEN",
                 "CLAUDE_CODE_SESSION_ID", "CLAUDECODE", "CODEX_THREAD_ID", "PROBE_PI_PACKAGE_ROOT"):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / "home").mkdir()
    return tmp_path


def _settings(isolate) -> Path:
    return isolate / "pi-agent" / "settings.json"


def _install_mirror_entry(isolate, *, version="0.3.0", extra: dict | None = None):
    """Our mirror entry in pi's settings, and pi's clone of it at `version`."""
    entry: object = pi_config.MIRROR_GIT_SOURCE if extra is None else {"source": pi_config.MIRROR_GIT_SOURCE, **extra}
    path = _settings(isolate)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"theme": "dark", "packages": ["npm:other-thing", entry]}))
    clone = isolate / "pi-agent" / "git" / "github.com" / "prbe-ai/research-os-agent" / "plugins" / "probe-research-pi"
    clone.mkdir(parents=True, exist_ok=True)
    (clone / "package.json").write_text(json.dumps({"name": "probe-research-pi", "version": version}))
    return clone


def test_the_package_skills_are_the_daemon_profile_less_the_extensions_own_probe():
    profiles = json.loads((AGENT / "skills" / "profiles.json").read_text())
    assert list(pi_config.DAEMON_PACKAGE_SKILLS) == [s for s in profiles["daemon"] if s != "probe"]


def test_set_profile_narrows_and_restores_the_mirror_entry(isolate):
    _install_mirror_entry(isolate)

    assert pi_config.set_profile(True).ok
    data = json.loads(_settings(isolate).read_text())
    assert data["theme"] == "dark" and data["packages"][0] == "npm:other-thing"
    assert data["packages"][1] == {
        "source": pi_config.MIRROR_GIT_SOURCE,
        "skills": ["plugins/probe-research-pi/skills/instrument-code"],
    }
    assert pi_config.entry_profile() == "daemon"
    assert pi_config.set_profile(True).detail == "no change"

    assert pi_config.set_profile(False).ok
    assert json.loads(_settings(isolate).read_text())["packages"][1] == pi_config.MIRROR_GIT_SOURCE
    assert pi_config.entry_profile() == "agent"


def test_set_profile_repairs_a_filter_that_drops_the_extension_and_keeps_other_keys(isolate):
    _install_mirror_entry(isolate, extra={"extensions": [], "prompts": ["x.md"]})
    assert pi_config.set_profile(True).ok
    entry = json.loads(_settings(isolate).read_text())["packages"][1]
    assert "extensions" not in entry, "the extension IS the daemon profile's runtime"
    assert entry["prompts"] == ["x.md"]


def test_a_local_checkout_entry_names_skills_relative_to_the_package(isolate, tmp_path):
    package = tmp_path / "checkout" / "probe-research-pi"
    package.mkdir(parents=True)
    (package / "package.json").write_text(json.dumps({"name": "probe-research-pi", "version": "0.3.1"}))
    _settings(isolate).parent.mkdir(parents=True, exist_ok=True)
    _settings(isolate).write_text(json.dumps({"packages": [str(package)]}))
    assert pi_config.set_profile(True).ok
    assert json.loads(_settings(isolate).read_text())["packages"][0]["skills"] == ["skills/instrument-code"]
    assert pi_config.installed_package_version() == (0, 3, 1)


def test_set_profile_refuses_an_unreadable_settings_file(isolate):
    _settings(isolate).parent.mkdir(parents=True, exist_ok=True)
    _settings(isolate).write_text("{not json")
    assert not pi_config.set_profile(True).ok
    assert _settings(isolate).read_text() == "{not json"


def test_the_installed_version_is_read_from_pis_clone_of_the_mirror(isolate):
    _install_mirror_entry(isolate, version="0.2.0")
    assert pi_config.installed_package_version() == (0, 2, 0)


class _Moves:
    """The switch's outside calls, recorded: key, libraries, plugins."""

    def __init__(self, monkeypatch, *, update_to=None):
        from probe.cli import companion, daemon_cli

        self.log: list = []
        monkeypatch.setattr(wizard, "companion_token_held", lambda: True)
        monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "test")
        monkeypatch.setattr(companion, "provision_daemon", lambda *a, **k: [])
        monkeypatch.setattr(wizard, "install_plugin", lambda name, **kw: self.log.append(("install", name)) or Result(ok=True))
        monkeypatch.setattr(wizard, "uninstall_plugin",
                            lambda name, **kw: self.log.append(("uninstall", name)) or Result(ok=True))
        monkeypatch.setattr(wizard, "live_daemon_sessions", lambda: 0)
        self.update_to = update_to

        def update(env=None):
            self.log.append(("pi update",))
            if update_to is None:
                return Result(ok=False, detail="offline")
            clone = Path(str(pi_config.installed_package_dir()))
            (clone / "package.json").write_text(json.dumps({"name": "probe-research-pi", "version": update_to}))
            return Result(ok=True, detail="updated")

        monkeypatch.setattr(pi_config, "update_package", update)


def _pi_caps():
    return Capabilities(agent_source="pi", tracking_plugin_installed=True, capture_plugin_installed=True)


def test_moving_pi_to_the_daemon_keeps_its_package_and_narrows_it(isolate, monkeypatch):
    """The trap the audit found: the generic tail uninstalls `drop` when the
    listing is unverified, and pi's listing is ALWAYS unverified, so adding pi
    to the recorder list alone would have deleted pi's only package."""
    moves = _Moves(monkeypatch)
    _install_mirror_entry(isolate)
    monkeypatch.setenv("PROBE_PI_TAP_TOKEN", "ros_ing_pi")
    path = agent_rules.memory_path("pi")
    agent_rules.install(path)

    lines = wizard.apply_recorder(_pi_caps(), session_marker.RECORDER_DAEMON, base_url="https://api.test")

    assert moves.log == [], "no plugin installed or removed for pi"
    assert session_marker.recorder("pi") == session_marker.RECORDER_DAEMON
    assert pi_config.entry_profile() == "daemon"
    assert pi_config.MIRROR_GIT_SOURCE in _settings(isolate).read_text()
    assert agent_rules.installed_profile(path) is agent_rules.Profile.DAEMON
    assert "Who records in pi → the daemon" in lines
    assert not [line for line in lines if line.startswith("!")], lines

    lines = wizard.apply_recorder(_pi_caps(), session_marker.RECORDER_AGENT, base_url="https://api.test")
    assert session_marker.recorder("pi") == session_marker.RECORDER_AGENT
    assert pi_config.entry_profile() == "agent"
    assert agent_rules.installed_profile(path) is agent_rules.Profile.AGENT


def test_an_unpaired_pi_stays_on_agent(isolate, monkeypatch):
    _Moves(monkeypatch)
    _install_mirror_entry(isolate)
    lines = wizard.apply_recorder(_pi_caps(), session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert session_marker.recorder("pi") == session_marker.RECORDER_AGENT
    assert pi_config.entry_profile() == "agent"
    assert any("capture is not paired" in line for line in lines)


def test_an_old_pi_package_is_updated_first(isolate, monkeypatch):
    moves = _Moves(monkeypatch, update_to="0.3.0")
    _install_mirror_entry(isolate, version="0.2.0")
    monkeypatch.setenv("PROBE_PI_TAP_TOKEN", "ros_ing_pi")
    lines = wizard.apply_recorder(_pi_caps(), session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert ("pi update",) in moves.log
    assert session_marker.recorder("pi") == session_marker.RECORDER_DAEMON
    assert "pi's Probe package updated to 0.3.0." in lines


def test_a_pi_package_that_cannot_update_keeps_pi_on_agent_and_says_what_to_run(isolate, monkeypatch):
    _Moves(monkeypatch, update_to=None)
    _install_mirror_entry(isolate, version="0.2.0")
    monkeypatch.setenv("PROBE_PI_TAP_TOKEN", "ros_ing_pi")
    lines = wizard.apply_recorder(_pi_caps(), session_marker.RECORDER_DAEMON, base_url="https://api.test")
    assert session_marker.recorder("pi") == session_marker.RECORDER_AGENT
    assert pi_config.entry_profile() == "agent", "nothing switched"
    assert any(f"pi update {pi_config.MIRROR_GIT_SOURCE}" in line and "0.3.0" in line for line in lines)


def test_the_switch_pairs_pi_outside_the_spinner(isolate, monkeypatch):
    """The approval prints a link to open; inside the spinner nobody sees it."""
    import contextlib

    from probe.cli import daemon_cli, tui

    cli_main = importlib.import_module("probe.cli.main")
    events: list = []

    @contextlib.contextmanager
    def working(label):
        events.append(("spin", label))
        yield
        events.append(("done", label))

    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "1" * 32)
    monkeypatch.setattr(tui, "working", working)
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(wizard, "companion_token_held", lambda: True)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "test")
    monkeypatch.setattr(wizard, "daemon_availability", lambda base_url=None: (True, None))
    monkeypatch.setattr(cli_main, "_run_daemon_page", lambda **kw: None)
    monkeypatch.setattr(cli_main, "_daemon_key_refused", lambda base: False)
    monkeypatch.setattr(wizard, "daemon_package_ready", lambda source: wizard._Ready(True, []))
    monkeypatch.setattr(wizard, "pair_capture", lambda source, **kw: events.append(("pair", source)) or ["paired"])
    monkeypatch.setattr(wizard, "apply_recorder",
                        lambda caps, value, **kw: events.append(("apply", caps.agent_source)) or [])
    cli_main._run_recorder_action(
        yes=False, caps_by_source={"pi": _pi_caps()}, base_now="https://api.test",
        chosen=session_marker.RECORDER_DAEMON,
    )
    pair = events.index(("pair", "pi"))
    moving = events.index(("spin", "Moving your coding agents to the daemon"))
    assert pair < moving < events.index(("apply", "pi"))
    # Not inside any spinner: every spinner opened before it is closed by then.
    opened = [e[1] for e in events[:pair] if e[0] == "spin"]
    closed = [e[1] for e in events[:pair] if e[0] == "done"]
    assert opened == closed


def test_an_old_package_stops_the_switch_before_pairing(isolate, monkeypatch):
    """Pairing mints pi's own capture token: a switch that then stopped on an
    old package would leave pi capturing on agent, which it never did."""
    from probe.cli import daemon_cli

    cli_main = importlib.import_module("probe.cli.main")
    calls: list = []
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "1" * 32)
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(wizard, "companion_token_held", lambda: True)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "test")
    monkeypatch.setattr(wizard, "daemon_availability", lambda base_url=None: (True, None))
    monkeypatch.setattr(cli_main, "_run_daemon_page", lambda **kw: None)
    monkeypatch.setattr(cli_main, "_daemon_key_refused", lambda base: False)
    _install_mirror_entry(isolate, version="0.2.0")
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: Result(ok=False, detail="offline"))
    monkeypatch.setattr(wizard, "pair_capture", lambda source, **kw: calls.append(("pair", source)) or [])
    monkeypatch.setattr(wizard, "apply_recorder", lambda caps, value, **kw: calls.append(("apply", value)) or [])

    lines = cli_main._run_recorder_action(
        yes=False, caps_by_source={"pi": _pi_caps()}, base_now="https://api.test",
        chosen=session_marker.RECORDER_DAEMON,
    )
    assert calls == []
    assert any("pi stays on agent: its Probe package is 0.2.0" in line for line in lines), lines
    assert session_marker.recorder("pi") == session_marker.RECORDER_AGENT


def test_a_researchers_own_skills_filter_survives_the_round_trip(isolate):
    mine = ["plugins/probe-research-pi/skills/probe", "plugins/probe-research-pi/skills/track-work"]
    _install_mirror_entry(isolate, extra={"skills": mine})
    assert pi_config.entry_profile() == "agent", "their own filter is the agent profile, narrowed by them"

    assert pi_config.set_profile(True).ok
    entry = json.loads(_settings(isolate).read_text())["packages"][1]
    assert entry["skills"] == ["plugins/probe-research-pi/skills/instrument-code"]
    assert entry[pi_config.AGENT_SKILLS_STASH_KEY] == mine
    assert pi_config.entry_profile() == "daemon"

    assert pi_config.set_profile(False).ok
    entry = json.loads(_settings(isolate).read_text())["packages"][1]
    assert entry == {"source": pi_config.MIRROR_GIT_SOURCE, "skills": mine}


def test_a_filter_changed_while_on_the_daemon_is_theirs_and_stays(isolate):
    _install_mirror_entry(isolate, extra={"skills": ["plugins/probe-research-pi/skills/probe"]})
    assert pi_config.set_profile(True).ok
    data = json.loads(_settings(isolate).read_text())
    data["packages"][1]["skills"] = ["plugins/probe-research-pi/skills/edit-notes"]
    _settings(isolate).write_text(json.dumps(data))

    assert pi_config.set_profile(False).ok
    entry = json.loads(_settings(isolate).read_text())["packages"][1]
    assert entry == {"source": pi_config.MIRROR_GIT_SOURCE, "skills": ["plugins/probe-research-pi/skills/edit-notes"]}


def test_enter_on_a_daemon_machine_brings_pi_along(isolate, monkeypatch):
    """Oded's machine: Claude Code and Codex on the daemon, pi left on agent
    after the upgrade. Enter on Who records moves pi; nothing moves on its own."""
    import contextlib

    from probe.cli import daemon_cli, tui

    cli_main = importlib.import_module("probe.cli.main")
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "1" * 32)
    monkeypatch.setenv("PROBE_PI_TAP_TOKEN", "ros_ing_pi")
    monkeypatch.setattr(tui, "working", lambda label: contextlib.nullcontext())
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(wizard, "companion_token_held", lambda: True)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "test")
    monkeypatch.setattr(wizard, "daemon_availability", lambda base_url=None: (True, None))
    monkeypatch.setattr(cli_main, "_run_daemon_page", lambda **kw: None)
    monkeypatch.setattr(cli_main, "_daemon_key_refused", lambda base: False)
    moved = []
    monkeypatch.setattr(wizard, "apply_recorder", lambda caps, value, **kw: moved.append((caps.agent_source, value)) or [])
    pi = Capabilities(agent_source="pi", tracking_plugin_installed=True, capture_plugin_installed=True)
    assert pi.configured
    cli_main._run_recorder_action(
        yes=False, caps_by_source={"claude_code": Capabilities(), "pi": pi}, base_now="https://api.test", chosen=None
    )
    assert moved == [("pi", session_marker.RECORDER_DAEMON)]


def _initialize(cwd: Path) -> dict:
    cli_main = importlib.import_module("probe.cli.main")
    result = CliRunner().invoke(cli_main.app, ["session", "initialize", "--session", SID, "--cwd", str(cwd)])
    assert result.exit_code == 0, result.output
    return json.loads(result.output)


def test_a_pi_session_seeds_on_the_daemon_with_the_extensions_real_environment(isolate, monkeypatch):
    """The extension runs `session initialize` with PROBE_AGENT=pi and NO PI_*
    variable (pi sets those only on its bash tool's children). Before, every pi
    session seeded `full` even with Who records = daemon."""
    session_marker.write_recorder("pi", session_marker.RECORDER_DAEMON)
    monkeypatch.setenv("PROBE_AGENT", "pi")
    out = _initialize(isolate)
    assert out["state"] == "daemon"
    assert out["profile"] == "daemon"
    assert session_marker.session_profile(SID) == "daemon"


def test_a_resumed_pi_session_follows_who_records_both_ways(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    assert _initialize(isolate)["state"] == "on"
    session_marker.write_recorder("pi", session_marker.RECORDER_DAEMON)
    out = _initialize(isolate)
    assert (out["state"], out["profile"]) == ("daemon", "daemon")
    session_marker.write_recorder("pi", session_marker.RECORDER_AGENT)
    out = _initialize(isolate)
    assert (out["state"], out["profile"]) == ("on", "agent")
    assert session_marker.session_state(SID) == session_marker.STATE_FULL


def test_a_paused_pi_session_stays_paused_across_a_switch(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _initialize(isolate)
    session_marker.set_session_state(SID, session_marker.STATE_READ_ONLY)
    session_marker.write_recorder("pi", session_marker.RECORDER_DAEMON)
    out = _initialize(isolate)
    assert out["state"] == "read", "read and off are the researcher's own switch"
    assert session_marker.session_state(SID) == session_marker.STATE_READ_ONLY
    assert out["profile"] == "daemon"


def test_an_old_extension_reading_the_json_still_finds_every_old_field(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    out = _initialize(isolate)
    for field in ("session_id", "tracking", "signal", "state", "seeded", "source", "capture", "effective"):
        assert field in out


def test_doctor_names_who_records_per_agent_and_pis_package(isolate, monkeypatch):
    from probe.cli import doctor

    _install_mirror_entry(isolate, version="0.2.0")
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    rows = doctor._who_records_rows()
    text = "\n".join(rows)
    assert "Who records (Claude Code)" in text and "the daemon" in text
    assert "Who records (pi)" in text and "can use the daemon now" in text
    assert "pi Probe package" in text and "the daemon needs 0.3.0+" in text
