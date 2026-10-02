"""The daemon profile (daemon reads): what the main agent's instruction file
says when the daemon records and reads, and that a refresh keeps it."""

from __future__ import annotations

from pathlib import Path

from probe.cli import agent_rules

FIXTURES = Path(__file__).parent / "fixtures" / "daemon_prompts" / "reads"


def _body(name: str) -> str:
    lines = (FIXTURES / name).read_text(encoding="utf-8").split("\n")
    return "\n".join(lines[lines.index("---", 1) + 1:])


def test_the_daemon_blurb_is_the_approved_text():
    assert agent_rules.DAEMON_POINTER_BODY == _body("agent-facing/managed-block.PROPOSED.md")
    assert len(agent_rules.DAEMON_POINTER_BODY) < 1200


def test_the_daemon_block_carries_its_profile_and_a_refresh_keeps_it(tmp_path):
    memory = tmp_path / "CLAUDE.md"
    memory.write_text("# my rules\n")
    old = agent_rules.render_block(version=agent_rules.POINTER_VERSION - 1, profile=agent_rules.Profile.DAEMON)
    assert agent_rules.install(memory, block=old)
    assert agent_rules.installed_version(memory) == agent_rules.POINTER_VERSION - 1
    assert agent_rules.installed_profile(memory) == agent_rules.Profile.DAEMON
    assert agent_rules.refresh_pointer(memory) == agent_rules.POINTER_REFRESHED
    text = memory.read_text()
    assert "### ASK THE DAEMON:" in text and "### HOW TO READ" not in text, "still the daemon's body"
    assert agent_rules.installed_profile(memory) == agent_rules.Profile.DAEMON
    assert text.startswith("# my rules\n")


def test_an_agent_block_stays_an_agent_block(tmp_path):
    memory = tmp_path / "CLAUDE.md"
    agent_rules.install(memory, block=agent_rules.render_block(version=agent_rules.POINTER_VERSION - 1))
    assert agent_rules.installed_profile(memory) == agent_rules.Profile.AGENT
    agent_rules.refresh_pointer(memory)
    assert agent_rules.POINTER_BODY in memory.read_text()
    assert agent_rules.installed_profile(tmp_path / "absent.md") is None


# ---------------------------------------------------------------------------
# The guard in the daemon profile: every `probe` command but ask, exec, the
# runs' own data and session status is refused, reads included.
# ---------------------------------------------------------------------------

import json  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402

import pytest  # noqa: E402

from probe.sdk import session_marker  # noqa: E402

GUARD = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks" / "tracking_guard.py"
SID = "11111111-2222-3333-4444-555555555555"


def test_the_guard_refusal_is_the_approved_text():
    assert session_marker.DAEMON_PROFILE_DENY == _body("agent-facing/guard-refusal.NEW.md").rstrip("\n")


def _guard(tmp_path, command: str, *, state: str = "daemon", tool: str = "Bash", profile: str = "daemon"):
    sessions = tmp_path / "state" / "probe" / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / f"{SID}.state").write_text(state)
    env = {"PATH": os.environ.get("PATH", ""), "HOME": str(tmp_path), "XDG_STATE_HOME": str(tmp_path / "state"),
           "XDG_CONFIG_HOME": str(tmp_path / "config"), "PROBE_PLUGIN_PROFILE": profile}
    payload = {"hook_event_name": "PreToolUse", "session_id": SID, "cwd": str(tmp_path), "tool_name": tool,
               "tool_input": {"command": command}}
    out = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True,
                         env=env, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)["hookSpecificOutput"]["permissionDecisionReason"] if out.stdout else None


@pytest.mark.parametrize("command", ['probe ask "any prior SVM sweeps?"', "probe exec -- python train.py",
                                    "probe run start --name x", "probe run end r1", "probe session status",
                                    "probe log --run r1 acc=0.9", "probe get --help", "ls -la"])
def test_the_main_agent_keeps_its_own_commands(tmp_path, command):
    assert _guard(tmp_path, command) is None


@pytest.mark.parametrize("command,matched", [("probe get run r1", "probe get"),
                                             ("probe notes list", "probe notes list"),
                                             ("probe project create x", "probe project create"),
                                             ("cd x && probe metrics run r1", "probe metrics")])
def test_everything_else_is_the_daemons(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


def test_a_probe_mcp_call_is_refused_and_the_agent_profile_is_untouched(tmp_path):
    assert "was refused" in _guard(tmp_path, "", tool="mcp__probe-research__browse")
    assert _guard(tmp_path, "probe get run r1", profile="") is None, "the agent profile's guard is unchanged"


@pytest.mark.parametrize("command,matched", [("command probe get run r1", "probe get"),
                                             ("env FOO=1 probe notes list", "probe notes list"),
                                             ('bash -c "probe metrics run r1"', "probe metrics"),
                                             ("timeout 30 probe get run r1", "probe get"),
                                             ("python3 -m probe get run r1", "probe get"),
                                             ("python -m probe.cli project list", "probe project list"),
                                             ("python3 -m probe.cli.main get run r1", "probe get")])
def test_a_wrapped_probe_command_is_still_seen(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command", ["probe run expect r1 --metric acc --min 0.9", "probe doctor",
                                     "probe --version"])
def test_what_instrument_code_and_the_researcher_notices_name_is_allowed(tmp_path, command):
    assert _guard(tmp_path, command) is None


def test_probe_version_is_the_experiment_versions_group_not_the_version_check(tmp_path):
    """`probe version create` mints an experiment version; the guard allowed it as
    if it printed the CLI's version (live T13 on the released plugin 0.111.2)."""
    assert _guard(tmp_path, "probe version create 00000000-0000-0000-0000-000000001002 --label x") == (
        session_marker.DAEMON_PROFILE_DENY.format(matched="probe version create"))
    assert session_marker.classify_probe_args(["version", "create", "e1", "--label", "x"]) == (
        "write", "probe version create")
    assert session_marker.classify_probe_args(["version", "list", "e1"]) == ("read", "probe version list")


def test_the_daemon_stopped_line_is_the_approved_researcher_line():
    import importlib.util
    import sys

    hooks = Path(__file__).resolve().parents[1] / "plugins" / "probe-research" / "hooks"
    sys.path.insert(0, str(hooks))
    try:
        spec = importlib.util.spec_from_file_location("_vc_profile", hooks / "version_check.py")
        vc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vc)
    finally:
        sys.path.remove(str(hooks))
    from probe.daemon import mailbox

    assert vc.DAEMON_STOPPED_LINE == mailbox.FAILURE_MESSAGES[mailbox.DAEMON_STOPPED]
