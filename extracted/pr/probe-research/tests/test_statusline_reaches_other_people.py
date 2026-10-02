"""Does the status line actually reach anyone other than the person who built it?

`statusLine` is a single key in the researcher's OWN settings file. Nothing in a
release can put the segment there, so a feature that depends on someone reading a
changelog and running `probe statusline install` is a feature almost nobody ends
up with. The wizard is the one moment we are already editing that machine with
permission, so it has to be the moment this happens.

These tests all run against a SIMULATED FRESH MACHINE — empty settings, empty
state, plugin on disk — and assert on the file the researcher would actually end
up with, not on our intent to write it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import setup as wizard
from probe.cli import statusline

_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def fresh_machine(tmp_path, monkeypatch):
    """A machine that has never seen Probe: no settings, no state, plugin present."""
    claude = tmp_path / "claude"
    claude.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_PLUGIN_ROOT", str(_ROOT / "plugins" / "probe-research"))
    return claude


def _settings(home: Path) -> dict:
    path = home / "settings.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def test_a_fresh_machine_has_no_status_line(fresh_machine) -> None:
    """The premise: without us, nothing is there."""
    assert wizard.statusline_installed() is False
    assert "statusLine" not in _settings(fresh_machine)


def test_writing_the_rules_also_registers_the_status_line(fresh_machine) -> None:
    """THE WHOLE POINT. The wizard step a new user actually runs must leave the
    segment configured, without them having read anything about it."""
    messages = wizard.apply_agent_rules(True)

    command = _settings(fresh_machine)["statusLine"]["command"]
    assert statusline.MARKER in command, "the wizard did not register the segment"
    assert wizard.statusline_installed() is True
    assert any("status line" in m.lower() for m in messages), (
        f"the wizard must SAY it configured the status line: {messages}"
    )


def test_it_keeps_a_status_line_the_researcher_already_had(fresh_machine) -> None:
    """Nobody's existing prompt gets evicted to make room for ours."""
    (fresh_machine / "settings.json").write_text(
        json.dumps({"statusLine": {"type": "command", "command": "my-prompt --fancy"}}),
        encoding="utf-8",
    )
    wizard.apply_agent_rules(True)

    command = _settings(fresh_machine)["statusLine"]["command"]
    assert "my-prompt --fancy" in command
    assert statusline.MARKER in command


def test_declining_the_rules_does_not_touch_the_status_line(fresh_machine) -> None:
    """Someone who says no to the standing rules has said no to this too."""
    wizard.apply_agent_rules(False)
    assert "statusLine" not in _settings(fresh_machine)


def test_re_running_does_not_stack_copies(fresh_machine) -> None:
    wizard.apply_agent_rules(True)
    first = _settings(fresh_machine)["statusLine"]["command"]
    wizard.apply_agent_rules(True)
    assert _settings(fresh_machine)["statusLine"]["command"] == first
    assert first.count(statusline.MARKER) == 1


def test_a_missing_plugin_is_reported_not_crashed(tmp_path, monkeypatch) -> None:
    """A machine where the plugin is not on disk yet must still finish the
    wizard, and must say what it skipped rather than silently doing nothing."""
    claude = tmp_path / "claude"
    claude.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_PLUGIN_ROOT", str(tmp_path / "nowhere"))
    monkeypatch.setattr(statusline, "discover_plugin_root", lambda: None)

    messages = wizard.apply_statusline()

    assert any("skipped" in m.lower() for m in messages), messages
    assert "statusLine" not in _settings(claude)


def test_the_registered_command_actually_renders(fresh_machine) -> None:
    """Registration is worthless if the command it wrote does not run. Executes
    the composed status-line command exactly as the agent would."""
    import subprocess

    wizard.apply_agent_rules(True)
    command = _settings(fresh_machine)["statusLine"]["command"]

    session = "32fae7ad-a401-43d0-bfef-ea032058769e"
    from probe.sdk import session_marker

    session_marker.write(session, {"project": "bird-sql-sft"})
    session_marker.set_tracking(session, True)

    result = subprocess.run(
        ["/bin/sh", "-c", command],
        input=json.dumps({"session_id": session}),
        capture_output=True,
        text=True,
        timeout=30,
        env={
            "PATH": "/usr/bin:/bin",
            "XDG_STATE_HOME": str(Path(fresh_machine).parent / "state"),
            "HOME": str(Path(fresh_machine).parent),
            "PROBE_TOKEN": "probe_pat_fake",
        },
    )
    assert result.returncode == 0, result.stderr
    assert "tracking" in result.stdout, f"registered command rendered nothing: {result.stdout!r}"
    assert "bird-sql-sft" in result.stdout
