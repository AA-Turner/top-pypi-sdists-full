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
    # 1,131 approved 09-27; the `probe session inline` line (10-05) out again 10-06;
    # 1,365 with the PLAN FIRST section (10-11); 1,624 with PAPERS (10-12);
    # 1,816 with FEEDBACK (10-13); 1,969 with `probe ask --writer` (10-13).
    assert len(agent_rules.DAEMON_POINTER_BODY) < 2000


def test_the_paper_search_hold_is_the_approved_text():
    from probe.sdk import session_marker

    assert session_marker.PAPER_SEARCH_HOLD == _body("agent-facing/paper-search-hold.NEW.md")
    # Claude Code previews hook text past ~2 KB; the hold must arrive whole.
    assert len(session_marker.PAPER_SEARCH_HOLD) < 2000


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


def test_the_switch_refusal_is_the_approved_text():
    assert session_marker.RESEARCHER_SWITCH_DENY == _body("agent-facing/switch-refusal.NEW.md").rstrip("\n")


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


@pytest.mark.parametrize("command", ['probe ask "any prior SVM sweeps?"', 'probe ask --writer "group the arms"',
                                     'probe ask --writer --wait "file the score runs"', "probe exec -- python train.py",
                                    "probe run start --name x", "probe run end r1", "probe session status",
                                    "probe log --run r1 acc=0.9", "probe get --help", "ls -la"])
def test_the_main_agent_keeps_its_own_commands(tmp_path, command):
    assert _guard(tmp_path, command) is None


@pytest.mark.parametrize("command,matched", [("probe get run r1", "probe get"),
                                             ("probe notes list", "probe notes list"),
                                             ("cd x && probe metrics run r1", "probe metrics")])
def test_everything_else_is_the_daemons(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command", ["probe approvals --list", "probe approvals"])
def test_the_agent_lists_the_questions_the_daemon_holds(tmp_path, command):
    """It was refused, so the agent could not tell the researcher what waits for
    them. Listing is safe: in an agent's shell the CLI answers nothing."""
    assert _guard(tmp_path, command) is None


def test_saying_no_stays_the_researchers(tmp_path):
    assert _guard(tmp_path, "probe deny 7f3a09c1") == session_marker.DAEMON_PROFILE_DENY.format(matched="probe deny")


@pytest.mark.parametrize("command,matched", [("probe project create x", "probe project create"),
                                             ("probe notes push n.md", "probe notes push"),
                                             ("probe companion feedback 'wrong project'", "probe companion feedback")])
def test_a_write_is_told_that_directed_runs_it(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY_WRITE.format(matched=matched)


@pytest.mark.parametrize("command", ["probe project move willow-dictation-training --workspace willow --directed",
                                     "probe --directed project create x",
                                     "probe ask x && probe notes push n.md --directed",
                                     "probe companion feedback 'wrong project' --directed",
                                     "probe project contributors p1 --add a@b.c --directed"])
def test_a_write_the_researcher_asked_for_runs(tmp_path, command):
    """`probe session status` and the session-start context tell the agent to add
    `--directed` to a write the researcher asks for; the guard refused it anyway
    (plugin 0.129.0, a `probe project move ... --directed` from ~/willow)."""
    assert _guard(tmp_path, command) is None


@pytest.mark.parametrize("command,matched", [("probe workspace list --directed", "probe workspace"),
                                             ("probe run list --directed", "probe run list"),
                                             ("probe get run r1 --directed", "probe get"),
                                             ("probe project contributors p1 --directed", "probe project contributors")])
def test_directed_admits_no_read(tmp_path, command, matched):
    """Reads go through `probe ask` here, so the flag changes nothing."""
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command,matched", [("probe session state on --directed", "probe session state"),
                                             ("probe --directed session default off", "probe session default")])
def test_directed_never_moves_the_researchers_switch(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.RESEARCHER_SWITCH_DENY.format(matched=matched)
    args = command.split()[1:]
    assert session_marker.daemon_profile_allows(args)[0] is False


@pytest.mark.parametrize("state", ["daemon", "read-only"])
def test_the_agent_runs_the_paper_search_itself(tmp_path, state):
    """`probe paper find` reads the research literature, an outside index: the
    one read the daemon profile leaves to the agent (Richard 2026-10-12)."""
    assert _guard(tmp_path, 'probe paper find "why GRPO collapses at zero variance"', state=state) is None
    assert _guard(tmp_path, "probe paper find --mode read --paper-id arxiv:2610.02140", state=state) is None


def test_off_refuses_the_paper_search_too(tmp_path):
    """`off` is decided before the daemon profile's allowlist: no Probe call at all."""
    refusal = _guard(tmp_path, 'probe paper find "why GRPO collapses at zero variance"', state="off")
    assert refusal is not None and refusal.startswith("Probe is OFF for this conversation")


def test_the_paper_search_opens_no_other_read(tmp_path):
    assert _guard(tmp_path, "probe paper list --project p1") == session_marker.DAEMON_PROFILE_DENY.format(
        matched="probe paper list")
    assert _guard(tmp_path, "probe mcp call find_papers '{}'") == session_marker.DAEMON_PROFILE_DENY.format(
        matched="probe mcp")


def test_directed_past_a_double_dash_is_not_the_researchers(tmp_path):
    """The CLI strips `--directed` only before `--` (`write_gate.split_directed`)."""
    assert _guard(tmp_path, "probe notes push n.md -- --directed") == (
        session_marker.DAEMON_PROFILE_DENY_WRITE.format(matched="probe notes push"))
    assert session_marker.carries_directed(["exec", "--", "python", "--directed"]) is False


def test_read_only_still_refuses_a_directed_write(tmp_path):
    """`read only (daemon)`: the flag gets a write past the profile, not past the switch."""
    command = "probe project move p1 --workspace w --directed"
    assert _guard(tmp_path, command, state="read-only") == session_marker.DENY_REASON.format(
        matched="probe project move")


def test_the_write_refusal_is_the_approved_text_and_the_daemon_states_retry():
    approved = _body("agent-facing/guard-refusal.NEW.md").rstrip("\n")
    assert session_marker.DAEMON_PROFILE_DENY_WRITE == (approved + "\n\n" + session_marker.DIRECTED_RETRY + " "
                                                         + session_marker.WRITER_RETRY)
    # Richard's approved text (2026-10-13, ~/plans/writer-channel).
    assert session_marker.WRITER_RETRY == 'Otherwise ask the daemon\'s writer: `probe ask --writer "<request>"`.'
    assert session_marker.DENY_REASON_DAEMON.endswith("\n\n" + session_marker.DIRECTED_RETRY)


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


@pytest.mark.parametrize("command", ["probe outbox status --verbose", "probe run check r1", "probe sync",
                                     "probe artifact download --run r1 --checkpoint best -o ckpt",
                                     "probe daemon status", "probe whoami", "probe context list",
                                     "probe wandb discover ./wandb", "probe wandb key status"])
def test_what_probes_own_messages_send_the_agent_to_is_allowed(tmp_path, command):
    """The CLI's outbox banner says "see `probe outbox status`" on every command,
    and the guard refused it (2026-10-16); the SDK's capture warning names
    `probe run check`, an offline run `probe sync`, `instrument-code`
    `probe artifact download`. The rest are this machine's diagnostics."""
    assert _guard(tmp_path, command) is None


@pytest.mark.parametrize("command,matched", [("probe outbox discard op1", "probe outbox"),
                                             ("probe outbox retry op1", "probe outbox"),
                                             ("probe context use other-team", "probe context"),
                                             ("probe wandb key set k", "probe wandb key set"),
                                             ("probe daemon override x", "probe daemon"),
                                             ("probe artifact list --run r1", "probe artifact list")])
def test_the_rest_of_those_groups_stays_refused(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


def test_a_read_groups_write_is_a_write_the_researcher_can_direct(tmp_path):
    """`shared add` uploads: read as a read, `--directed` could never run it."""
    assert _guard(tmp_path, "probe shared add results.csv") == session_marker.DAEMON_PROFILE_DENY_WRITE.format(
        matched="probe shared add")
    assert _guard(tmp_path, "probe shared add results.csv --directed") is None


#: `probe` commands the daemon plugin's skills name that the guard refuses, each
#: with why that is right. Anything else they name must run.
SKILL_NAMES_REFUSED = {
    # Writes: each refusal names `--directed` and `probe ask --writer`.
    "probe edge add", "probe dataset use", "probe checkpoint use",
    # `probe edge remove` (instrument-code: a wrong data link): with the daemon
    # on it is the daemon's, which removes its own links (`daemon/tools.py`
    # `_own_link`); the refusal names `/probe inline`.
    "probe edge",
    # Where the researcher turns the daemon on or off.
    "probe wizard",
}


def test_every_probe_command_the_daemon_skills_name_is_allowed():
    import re
    import shlex

    skills = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-daemon" / "agent-skills"
    named = refused = 0
    for path in sorted(skills.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        spans = re.findall(r"`(probe [^`]+)`", text)
        spans += [line.strip() for line in text.splitlines() if line.strip().startswith("probe ")]
        for span in spans:
            try:
                args = shlex.split(span, comments=True)[1:]
            except ValueError:
                args = span.split()[1:]
            if session_marker.HELP_FLAG in args:
                continue
            named += 1
            allowed, matched = session_marker.daemon_profile_allows(args)
            if not allowed:
                refused += 1
                assert matched in SKILL_NAMES_REFUSED, f"{path.relative_to(skills)}: `{span}` is refused"
    assert named > 20 and refused, "the scan found the skills' commands"


def test_probe_version_is_the_experiment_versions_group_not_the_version_check(tmp_path):
    """`probe version create` mints an experiment version; the guard allowed it as
    if it printed the CLI's version (live T13 on the released plugin 0.111.2)."""
    assert _guard(tmp_path, "probe version create 00000000-0000-0000-0000-000000001002 --label x") == (
        session_marker.DAEMON_PROFILE_DENY_WRITE.format(matched="probe version create"))
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
