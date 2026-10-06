"""pi with Probe's tracking switched off while capture keeps running.

pi has ONE package for tracking (skills + MCP) and capture (the extension), so
"tracking off" cannot be an uninstall: it is the settings entry narrowed to no
package skills plus `probeTracking: false`, which the extension enforces
(src/trackingSetting.ts). One writer (`pi_config._entry_for`) owns the
entry's skills, so the daemon profile and tracking-off cannot clobber each
other's stash of the researcher's own filter.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import capabilities, capture, pi_config
from probe.cli import setup as wizard
from probe.cli.claude_cli import Result

MIRROR = pi_config.MIRROR_GIT_SOURCE
DAEMON_FILTER = ["plugins/probe-research-pi/skills/instrument-code"]


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path / "pi-tap"))
    for name in ("PROBE_AGENT", "PROBE_TAP_SOURCE", "PI_SESSION_ID", "PI_CODING_AGENT", "PROBE_PI_TAP_TOKEN",
                 "CLAUDE_CODE_SESSION_ID", "CLAUDECODE", "CODEX_THREAD_ID", "PROBE_PI_PACKAGE_ROOT"):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / "home").mkdir()
    monkeypatch.chdir(tmp_path / "home")
    return tmp_path


def _settings(isolate) -> Path:
    return isolate / "pi-agent" / "settings.json"


def _write_entry(isolate, entry: object) -> None:
    path = _settings(isolate)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"theme": "dark", "packages": ["npm:other-thing", entry]}))


def _entry(isolate) -> object:
    return json.loads(_settings(isolate).read_text())["packages"][1]


@pytest.mark.parametrize(
    ("tracking", "daemon", "expected"),
    [
        (True, False, MIRROR),
        (True, True, {"source": MIRROR, "skills": DAEMON_FILTER}),
        (False, False, {"source": MIRROR, "skills": [], "probeTracking": False}),
        (False, True, {"source": MIRROR, "skills": [], "probeTracking": False}),
    ],
)
def test_the_entry_matrix(tracking, daemon, expected):
    assert pi_config._entry_for(MIRROR, MIRROR, tracking=tracking, daemon=daemon) == expected


def test_the_researchers_filter_survives_off_then_daemon_then_on(isolate):
    """Two writers of `skills` would stash `[]` as the researcher's filter on
    off -> daemon, and restore `[]` on the way back: every skill silently gone."""
    mine = ["plugins/probe-research-pi/skills/track-work"]
    _write_entry(isolate, {"source": MIRROR, "skills": mine})

    assert pi_config.set_tracking(False, daemon=False).ok
    assert _entry(isolate) == {"source": MIRROR, "skills": [], "probeTracking": False,
                               pi_config.AGENT_SKILLS_STASH_KEY: mine}
    assert pi_config.set_tracking(True, daemon=True).ok  # tracking back, onto the daemon profile
    assert _entry(isolate)["skills"] == DAEMON_FILTER
    assert pi_config.set_profile(False).ok
    assert _entry(isolate) == {"source": MIRROR, "skills": mine}


def test_a_filter_changed_while_tracking_is_off_is_the_researchers(isolate):
    _write_entry(isolate, {"source": MIRROR, "skills": ["x"], "probeTracking": False,
                           pi_config.AGENT_SKILLS_STASH_KEY: ["old"]})
    assert pi_config.set_tracking(True, daemon=False).ok
    assert _entry(isolate) == {"source": MIRROR, "skills": ["x"]}


def test_tracking_off_drops_an_extensions_filter_that_stops_capture(isolate):
    """Without the extension neither capture nor the tracking-off enforcement
    runs, so a filter that excludes it cannot stay beside `probeTracking`."""
    _write_entry(isolate, {"source": MIRROR, "extensions": []})
    assert pi_config.set_tracking(False, daemon=False).ok
    assert "extensions" not in _entry(isolate)


def test_the_merged_entry_reports_tracking_off_and_a_project_override(isolate):
    _write_entry(isolate, {"source": MIRROR, "skills": [], "probeTracking": False})
    assert pi_config.merged_package_entry(cwd=isolate / "home").tracking_off is True

    project = isolate / "home" / ".pi" / "settings.json"
    project.parent.mkdir(parents=True)
    project.write_text(json.dumps({"packages": [MIRROR]}))
    merged = pi_config.merged_package_entry(cwd=isolate / "home")
    assert merged.scope == "project" and merged.tracking_off is False
    assert pi_config.entry_profile() == pi_config.PROFILE_TRACKING_OFF  # the global entry, untouched


def test_capture_alone_installs_with_tracking_off(isolate):
    assert pi_config.install_package_entry(tracking=False).ok
    entry = json.loads(_settings(isolate).read_text())["packages"][0]
    assert entry["probeTracking"] is False and entry["skills"] == []


def test_installed_plugins_reports_tracking_from_the_entry(isolate, monkeypatch):
    monkeypatch.setattr(capabilities, "tracking_plugin_name", lambda source=None: capabilities.TRACKING_PLUGIN_NAME)
    _write_entry(isolate, MIRROR)
    assert {capabilities.TAP_PLUGIN_NAME, capabilities.TRACKING_PLUGIN_NAME} <= set(
        capabilities.installed_plugins(source="pi").names
    )
    _write_entry(isolate, {"source": MIRROR, "skills": [], "probeTracking": False})
    names = set(capabilities.installed_plugins(source="pi").names)
    assert capabilities.TAP_PLUGIN_NAME in names and capabilities.TRACKING_PLUGIN_NAME not in names


@pytest.mark.parametrize("capture_on", [True, False])
def test_unticking_tracking_keeps_the_entry_while_capture_runs(isolate, monkeypatch, capture_on):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, MIRROR)
    monkeypatch.setattr(wizard, "_settings_capture_on", lambda source: capture_on)
    monkeypatch.setattr(wizard, "_settings_tracking_ready", lambda: Result(ok=True, detail=""))

    messages = wizard.apply_tracking(False)

    packages = json.loads(_settings(isolate).read_text())["packages"]
    if capture_on:
        assert packages[1]["probeTracking"] is False, messages
    else:
        assert packages == ["npm:other-thing"], messages


def test_ticking_tracking_turns_an_off_entry_back_on(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, {"source": MIRROR, "skills": [], "probeTracking": False})
    assert wizard.apply_tracking(True) == []
    assert _entry(isolate) == MIRROR


def test_turning_tracking_off_waits_for_an_extension_that_honours_it(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, MIRROR)
    monkeypatch.setattr(wizard, "_settings_capture_on", lambda source: True)
    monkeypatch.setattr(
        wizard, "_settings_tracking_ready", lambda: Result(ok=False, detail="pi's Probe package is 0.3.0")
    )
    messages = wizard.apply_tracking(False)
    assert _entry(isolate) == MIRROR
    assert any("0.3.0" in line for line in messages)


def test_removing_capture_keeps_tracking(isolate, monkeypatch):
    """The mirror image: `probe capture off --remove` on pi deleted the whole
    package, Probe's tracking included."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, MIRROR)
    ok, notes = capture._uninstall_plugin()
    assert ok and notes == []
    assert _entry(isolate) == MIRROR

    _write_entry(isolate, {"source": MIRROR, "skills": [], "probeTracking": False})
    ok, _ = capture._uninstall_plugin()
    assert ok and json.loads(_settings(isolate).read_text())["packages"] == ["npm:other-thing"]


def test_the_capture_step_installs_pi_with_tracking_off(isolate, monkeypatch):
    """The capture step installs pi's package under its own name
    (`CAPTURE_PLUGIN_LABEL["pi"]`), never a tracking name: that install must
    not switch Probe's skills and MCP on."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    assert wizard.install_plugin(wizard.CAPTURE_PLUGIN_LABEL["pi"], source="pi").ok
    entry = json.loads(_settings(isolate).read_text())["packages"][0]
    assert entry["probeTracking"] is False and entry["skills"] == []

    assert wizard.install_plugin(wizard.TRACKING_PLUGIN_NAME, source="pi").ok
    assert wizard.apply_tracking(True) == []
    entry = json.loads(_settings(isolate).read_text())["packages"][0]
    assert isinstance(entry, str), entry  # the plain entry: skills and MCP on


def test_removing_both_halves_in_one_run_never_waits_on_the_version_floor(isolate, monkeypatch):
    """`--no-tracking --no-capture`: the floor guards a package that STAYS;
    one leaving with capture needs no extension that honours the flag."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, MIRROR)
    monkeypatch.setattr(wizard, "_settings_capture_on", lambda source: True)  # the device, before this run
    monkeypatch.setattr(wizard, "_settings_tracking_ready", lambda: Result(ok=False, detail="pi's Probe package is 0.3.0"))
    messages = wizard.apply_tracking(False, keep_capture=False)
    assert json.loads(_settings(isolate).read_text())["packages"] == ["npm:other-thing"], messages


def test_tracking_off_says_capture_keeps_running(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, MIRROR)
    monkeypatch.setattr(wizard, "_settings_tracking_ready", lambda: Result(ok=True, detail=""))
    messages = wizard.apply_tracking(False, keep_capture=True)
    assert any("session capture keeps running" in line for line in messages), messages
    assert not any("Removed the tracking plugin" in line for line in messages)


@pytest.mark.parametrize("want", [True, False])
def test_a_project_entry_that_wins_is_named(isolate, monkeypatch, want):
    """The wizard edits pi's GLOBAL entry; a project entry in this folder wins,
    so the change cannot take effect here -- say which file, never claim it did."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    _write_entry(isolate, MIRROR if not want else {"source": MIRROR, "skills": [], "probeTracking": False})
    project = isolate / "home" / ".pi" / "settings.json"
    project.parent.mkdir(parents=True)
    project.write_text(json.dumps({"packages": [
        {"source": MIRROR, "skills": [], "probeTracking": False} if want else MIRROR]}))
    monkeypatch.setattr(wizard, "_settings_tracking_ready", lambda: Result(ok=True, detail=""))
    messages = wizard.apply_tracking(want, keep_capture=True)
    assert any(str(project) in line for line in messages), messages
    project.write_text(json.dumps({"packages": []}))
    assert not any(str(project) in line for line in wizard.apply_tracking(want, keep_capture=True))


@pytest.mark.parametrize(
    ("before", "after", "ok", "updated"),
    [
        ((0, 4, 0), None, True, False),  # already new enough: no update
        ((0, 3, 9), (0, 4, 1), True, True),  # updated past the floor
        ((0, 3, 9), (0, 3, 9), False, True),  # update did not help
        (None, None, False, True),  # version unreadable even after an update
    ],
)
def test_the_version_floor_updates_pi_first(monkeypatch, before, after, ok, updated):
    versions = iter([before, after])
    calls: list[str] = []
    monkeypatch.setattr(pi_config, "installed_package_version", lambda *a, **k: next(versions))
    monkeypatch.setattr(pi_config, "update_package", lambda *a, **k: calls.append("update"))
    result = wizard._settings_tracking_ready()
    assert result.ok is ok and (calls == ["update"]) is updated
    if not ok:
        assert "0.4.0" in result.detail and "pi update" in result.detail


@pytest.mark.parametrize(
    ("sources", "disabled", "expected"),
    [(["env"], False, True), ([], False, False), (["env"], True, False)],
)
def test_capture_on_needs_a_credential_and_no_killswitch(isolate, monkeypatch, sources, disabled, expected):
    monkeypatch.setattr(wizard, "capture_token_sources", lambda source: sources)
    tap = isolate / "pi-tap"
    tap.mkdir(exist_ok=True)
    if disabled:
        (tap / ".disabled").write_text("")
    monkeypatch.setattr(wizard, "tap_plugin_dir", lambda source: tap)
    assert wizard._settings_capture_on("pi") is expected


def test_an_unreadable_capture_state_keeps_the_package(monkeypatch):
    def boom(source):
        raise OSError("unreadable")

    monkeypatch.setattr(wizard, "capture_token_sources", boom)
    assert wizard._settings_capture_on("pi") is True
