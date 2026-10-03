"""Switching a wizard setting saves it (2026-10-02).

The main menu's "Probe in new sessions" row saved only on Enter: moving off it
reverted the value, and the Settings screen, the daemon page and the Defaults
picker dropped what you switched when you left with `←`/Escape. A researcher
who switched a value and moved on found it reverted, with no word.
"""

from __future__ import annotations

import pytest

from probe.cli import setup, tui
from probe.cli.actions import Action
from probe.sdk import session_marker


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe" / "config.json"))
    for name in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING"):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / "home").mkdir()


class _Row:
    value = Action.DEFAULTS


def test_the_defaults_row_saves_on_each_press():
    switch = setup._DefaultSwitch([_Row()])
    start = switch.saved

    switch.step(1)

    assert switch.saved == switch.shown != start
    assert setup.setting_state(session_marker.default_session_state()) == switch.saved
    assert switch.hint(Action.DEFAULTS) == "← → switch"


def test_a_failed_save_keeps_the_row_on_what_is_saved_and_says_why(monkeypatch):
    switch = setup._DefaultSwitch([_Row()])
    start = switch.saved

    def refuse(state):
        raise OSError("read-only config")

    monkeypatch.setattr(session_marker, "write_default_state", refuse)
    switch.step(1)

    assert switch.shown == switch.saved == start
    assert switch.error is not None and "read-only config" in switch.error


class _Control:
    def __init__(self, selected, cycle=None):
        self.selected_options = list(selected)
        self.probe_cycle = dict(cycle or {})


def _drive(monkeypatch, *, selected, cycle=None):
    """Run a picker whose user changed rows and then left with `←`: the key
    binding calls `on_back(control)` before the prompt answers BACK."""
    seen = {}

    def bind(question, rows, **kwargs):
        seen["on_back"] = kwargs.get("on_back")
        return _Control(selected, cycle)

    def ask(question, **kwargs):
        if seen.get("on_back") is not None:
            seen["on_back"](_Control(selected, cycle))
        return tui.BACK

    monkeypatch.setattr(setup, "_bind_menu_keys", bind)
    monkeypatch.setattr(setup, "dress_band", lambda question, control: None)
    monkeypatch.setattr(tui, "ask", ask)


def test_leaving_the_settings_screen_keeps_a_switched_row(monkeypatch):
    current = dict.fromkeys(setup.Setting, True)
    _drive(monkeypatch, selected=[])  # Automatic updates switched off, then `←`

    assert setup.run_settings_menu(current) == {setup.Setting.AUTO_UPDATE: False}


def test_leaving_the_daemon_page_keeps_a_switched_row(monkeypatch):
    current = {**dict.fromkeys(setup.Setting, True), setup.Setting.REASONING_SUMMARIES: False}
    _drive(monkeypatch, selected=[setup.Setting.REASONING_SUMMARIES])

    assert setup.run_settings_menu(current, groups=setup.DAEMON_GROUPS) == {
        setup.Setting.REASONING_SUMMARIES: True
    }


def test_leaving_the_settings_screen_unchanged_is_still_back(monkeypatch):
    current = dict.fromkeys(setup.Setting, True)
    _drive(monkeypatch, selected=[setup.Setting.AUTO_UPDATE])

    assert setup.run_settings_menu(current) is tui.BACK


def test_leaving_the_defaults_picker_keeps_the_ticked_state(monkeypatch):
    current = setup.setting_state(session_marker.default_session_state())
    other = next(s for s in setup.cycling_settings()[setup.Setting.TRACKING_DEFAULT] if s != current)
    _drive(monkeypatch, selected=[other])

    assert setup.run_defaults_menu(current) == other


def test_leaving_the_defaults_picker_on_the_saved_state_is_still_back(monkeypatch):
    current = setup.setting_state(session_marker.default_session_state())
    _drive(monkeypatch, selected=[current])

    assert setup.run_defaults_menu(current) is tui.BACK
