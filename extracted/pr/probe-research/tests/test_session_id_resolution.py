"""Which conversation `probe session ...` thinks it is, per agent.

The switch used to name Claude Code's and Codex's session variables inline in
the CLI, so an agent added to `AGENTS` did not become an agent the switch could
name. pi shipped with `PI_SESSION_ID` already in that table and every
`probe session` subcommand still exited 1 under it -- and because the
track-work skill tells an agent to read `probe session status` before its first
write, an unreadable status is indistinguishable from a session that was
deliberately turned off. Cursor was in the same position.
"""

from __future__ import annotations

import json

import pytest

from probe import cli
from probe.sdk.agent_session import session_id_from_env

PI = "pi-4444-5555-666666666666"


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    for spec_env in (
        "CLAUDECODE",
        "CLAUDE_CODE_ENTRYPOINT",
        "CLAUDE_CODE_SESSION_ID",
        "CODEX_SANDBOX",
        "CODEX_THREAD_ID",
        "CURSOR_TRACE_ID",
        "PI_CODING_AGENT",
        "PI_SESSION_ID",
    ):
        monkeypatch.delenv(spec_env, raising=False)


def test_a_pi_session_can_name_itself(isolated, monkeypatch, capsys):
    """The bug this file exists for: pi was in the table and resolved to nothing."""
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", PI)
    assert cli.main(["session", "status"]) in (0, None)
    assert json.loads(capsys.readouterr().out)["session_id"] == PI


def test_capture_does_not_gate_the_switch(isolated, monkeypatch):
    """Cursor is `captured=False` and still has tracking to turn off.

    `resolve_agent_session` refuses an uncaptured agent because an
    unattributable session must not be stamped on a run. Reusing it here would
    have re-broken Cursor while fixing pi.
    """
    monkeypatch.setenv("CURSOR_TRACE_ID", "cursor-7777-8888-999999999999")
    assert session_id_from_env() == "cursor-7777-8888-999999999999"


def test_a_bare_session_variable_still_resolves(isolated, monkeypatch):
    """No agent marker, one known session var -- what the hardcoded pair did.

    Narrowing this to "marker AND session var" would break every hand-made
    shell that exports only the id, so detection is a preference, not a gate.
    """
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "claude-1111-2222-333333333333")
    assert session_id_from_env() == "claude-1111-2222-333333333333"


def test_detection_wins_over_a_stray_variable(isolated, monkeypatch):
    """Under pi, a leftover Codex id in the environment must not win."""
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", PI)
    monkeypatch.setenv("CODEX_THREAD_ID", "codex-stale-0000-000000000000")
    assert session_id_from_env() == PI


def test_no_agent_is_still_an_error(isolated, capsys):
    """The failure mode stays a loud exit 1, never a guessed id."""
    assert cli.main(["session", "status"]) == 1
    assert "no session id" in capsys.readouterr().err
