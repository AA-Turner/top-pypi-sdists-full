"""Which conversation `probe session ...` thinks it is, per agent.

The switch used to name Claude Code's and Codex's session variables inline in
the CLI, so an agent added to `AGENTS` did not become an agent the switch could
name. pi shipped with `PI_SESSION_ID` already in that table and every
`probe session` subcommand still exited 1 under it -- and because the
track-work skill tells an agent to read `probe session status` before its first
write, an unreadable status is indistinguishable from a session that was
deliberately turned off.
"""

from __future__ import annotations

import json

import pytest

from probe import cli
from probe.sdk.agent_session import resolve_agent_session, session_id_from_env

PI = "pi-4444-5555-666666666666"
DAEMON_WATCHES = "d6a1c0de-0000-4000-8000-000000000001"
NO_SESSION = "no session id: pass --session, or run inside a coding agent"


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
        "PI_CODING_AGENT",
        "PI_SESSION_ID",
        "PROBE_DAEMON_SESSION",
    ):
        monkeypatch.delenv(spec_env, raising=False)


def test_a_pi_session_can_name_itself(isolated, monkeypatch, capsys):
    """The bug this file exists for: pi was in the table and resolved to nothing."""
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", PI)
    assert cli.main(["session", "status"]) in (0, None)
    assert json.loads(capsys.readouterr().out)["session_id"] == PI


def test_capture_does_not_gate_the_switch(isolated, monkeypatch, tmp_path):
    """An unpaired Codex is not attributed and still has tracking to turn off.

    `resolve_agent_session` refuses a session whose transcripts cannot reach us
    because an unattributable session must not be stamped on a run. Reusing it
    here would make the switch unreadable wherever capture is not paired.
    """
    monkeypatch.delenv("PRBE_CODEX_TAP_TOKEN", raising=False)
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(tmp_path / "unpaired"))  # no .token
    monkeypatch.setenv("CODEX_THREAD_ID", "codex-7777-8888-999999999999")
    assert resolve_agent_session() is None
    assert session_id_from_env() == "codex-7777-8888-999999999999"


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
    assert NO_SESSION in capsys.readouterr().err


# ---------------------------------------------------------------------------
# The Probe daemon's own reads. Its `probe` calls carry no coding agent's
# variables, only the session it watches (`PROBE_DAEMON_SESSION`), and its
# `probe session status` used to answer "no session id" -- 62 times in 14 days
# for one pi user -- after which it hunted for the id with `printenv`, each hunt
# a question for the researcher.
# ---------------------------------------------------------------------------


def test_the_daemons_status_read_names_the_session_it_watches(isolated, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", DAEMON_WATCHES)
    assert cli.main(["session", "status"]) in (0, None)
    assert json.loads(capsys.readouterr().out)["session_id"] == DAEMON_WATCHES


def test_an_explicit_session_still_wins_over_the_daemons(isolated, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", DAEMON_WATCHES)
    assert cli.main(["session", "status", "--session", PI]) in (0, None)
    assert json.loads(capsys.readouterr().out)["session_id"] == PI


def test_the_agents_own_session_wins_over_a_stray_daemon_variable(isolated, monkeypatch, capsys):
    """A fallback, never a preference: an agent's shell resolves as before."""
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", PI)
    monkeypatch.setenv("PROBE_DAEMON_SESSION", DAEMON_WATCHES)
    assert cli.main(["session", "status"]) in (0, None)
    payload = json.loads(capsys.readouterr().out)
    assert payload["session_id"] == PI
    # The agent's own read: its capture and its writes, as before.
    assert isinstance(payload["capture"], dict) and isinstance(payload["writes_allowed"], bool)
    assert "note" not in payload


def test_the_daemons_companion_reads_name_the_session_too(isolated, monkeypatch, capsys):
    """The same read door: past "no session id" to the session's own ledger."""
    monkeypatch.setenv("PROBE_DAEMON_SESSION", DAEMON_WATCHES)
    assert cli.main(["companion", "trace"]) == 1
    err = capsys.readouterr().err
    assert NO_SESSION not in err and DAEMON_WATCHES in err


@pytest.mark.parametrize("args", [["session", "untrack"], ["session", "track"], ["session", "toggle"],
                                  ["session", "state"]])
def test_the_daemons_session_never_names_the_switch(isolated, monkeypatch, capsys, args):
    """Only reads fall back: the switch stays the researcher's, however it is run."""
    monkeypatch.setenv("PROBE_DAEMON_SESSION", DAEMON_WATCHES)
    assert cli.main(args) == 1
    assert NO_SESSION in capsys.readouterr().err


def test_a_malformed_daemon_variable_is_ignored(isolated, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "../../etc/passwd")
    assert cli.main(["session", "status"]) == 1
    assert NO_SESSION in capsys.readouterr().err
