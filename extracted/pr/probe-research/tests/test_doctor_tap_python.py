"""Doctor names a tap that has no Python to run on.

The tap needs Python 3.11 or newer, and its hooks used to run it on the first
`python3` on PATH: Apple's 3.9 on a stock Mac. Every `python3 -m tap` died on an
ImportError the hooks swallow, so nothing was recorded, while the plugin, the
pairing and the credential all read healthy and this said "capturing". The tap's
SessionStart now looks further (hooks/tap-python.sh) and, when it finds nothing,
leaves what it found in `.python-missing` beside `.disabled`; this reads it.
"""

from __future__ import annotations

import pytest

from probe.cli import doctor
from probe.cli.capabilities import Capabilities, PluginState, TokenSource


@pytest.fixture
def tap_state(tmp_path, monkeypatch):
    state = tmp_path / "tap-state"
    state.mkdir()
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(state))
    return state


def test_the_hooks_verdict_is_read_from_the_tap_state_folder(tap_state):
    assert doctor.capture_python_missing("claude_code") is None
    (tap_state / doctor.TAP_PYTHON_MISSING).write_text("python3 3.9.6\n", encoding="utf-8")
    assert doctor.capture_python_missing("claude_code") == "python3 3.9.6"


def test_an_empty_or_unreadable_verdict_still_says_capture_cannot_run(tap_state):
    (tap_state / doctor.TAP_PYTHON_MISSING).write_text("", encoding="utf-8")
    assert doctor.capture_python_missing("claude_code") == "no python3 that runs"
    (tap_state / doctor.TAP_PYTHON_MISSING).write_bytes(b"\xff\xfe")
    assert doctor.capture_python_missing("claude_code") is None


def test_a_source_without_a_tap_has_no_verdict():
    assert doctor.capture_python_missing("not-a-harness") is None


def test_collect_warns_and_carries_the_verdict(tap_state):
    (tap_state / ".token").write_text("ros_ing_faketoken", encoding="utf-8")
    (tap_state / doctor.TAP_PYTHON_MISSING).write_text("python3 3.9.6\n", encoding="utf-8")
    caps = doctor.collect(local=True, plugins=PluginState(names=frozenset({"probe-research-tap"})))
    assert caps.capture_python_missing == "python3 3.9.6"
    assert any("needs Python 3.11 or newer" in w and "python3 3.9.6" in w for w in caps.warnings)


def test_collect_says_nothing_once_the_hook_found_an_interpreter(tap_state):
    (tap_state / ".token").write_text("ros_ing_faketoken", encoding="utf-8")
    caps = doctor.collect(local=True, plugins=PluginState(names=frozenset({"probe-research-tap"})))
    assert caps.capture_python_missing is None
    assert not any("Python 3.11" in w for w in caps.warnings)


def _status_row(rendered: str) -> str:
    section = rendered.split("Session capture", 1)[1]
    return next(line for line in section.splitlines() if line.strip().startswith("Status"))


def test_a_paired_tap_with_no_interpreter_is_not_called_capturing():
    caps = Capabilities(
        capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        capture_python_missing="python3 3.9.6",
    )
    row = _status_row(doctor.render(caps))
    assert "capturing" not in row
    assert "needs Python 3.11 or newer (python3 3.9.6)" in row


def test_a_paired_tap_with_an_interpreter_still_reads_capturing():
    caps = Capabilities(capture_plugin_installed=True, capture_token_sources=(TokenSource.PAIRED_FILE,))
    assert "capturing" in _status_row(doctor.render(caps))
