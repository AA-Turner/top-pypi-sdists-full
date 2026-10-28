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
    # 1,816 with FEEDBACK (10-13); 1,969 with `probe ask --writer` (10-13);
    # 1,608 with `probe doctor --send` (10-23), after the 10-14 and 10-22 rewrites.
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


@pytest.mark.parametrize("command,matched", [("probe run list", "probe run list"),
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


@pytest.mark.parametrize("command,matched", [("probe run list --directed", "probe run list"),
                                             ("probe artifact list --run r1 --directed", "probe artifact list"),
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
    assert _guard(tmp_path, "probe run list", profile="") is None, "the agent profile's guard is unchanged"


@pytest.mark.parametrize("command,matched", [("command probe run list", "probe run list"),
                                             ("env FOO=1 probe notes list", "probe notes list"),
                                             ('bash -c "probe metrics run r1"', "probe metrics"),
                                             ("timeout 30 probe run list", "probe run list"),
                                             ("python3 -m probe run list", "probe run list"),
                                             ("python -m probe.cli project list", "probe project list"),
                                             ("python3 -m probe.cli.main run list", "probe run list")])
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


@pytest.mark.parametrize("command,matched", [("probe daemon override x", "probe daemon"),
                                             ("probe artifact list --run r1", "probe artifact list")])
def test_the_rest_of_those_groups_stays_refused(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command", ["probe update --check", "probe update --yes",
                                     "probe wizard --action update --yes", "probe setup --action=diagnose",
                                     "probe status --json", "probe service status", "probe token list",
                                     "probe outbox retry op1", "probe wandb key set k", "probe workspace list",
                                     "probe statusline status", "probe notes sync", "probe wizard --help",
                                     "probe file preview data/train.csv", "probe draft edit n.md < edit.txt"])
def test_the_clis_own_upkeep_runs(tmp_path, command):
    """A daemon-profile agent could not run `probe update --check` (2026-10-21):
    every command that neither reads nor writes research content was refused
    with the reads and writes. Only tracking is the daemon's."""
    assert _guard(tmp_path, command) is None


@pytest.mark.parametrize("command", ["probe run get r1", "probe run metrics r1 --key loss", "probe run series r1",
                                     "probe metrics plot r1", "probe metrics wide r1 --keys loss,acc",
                                     "probe get run r1", "probe events run r1", "probe span list r1",
                                     "probe trial get r1 t1", "probe artifact tree r1 --path ckpt",
                                     "probe snapshot-show r1", "cd x && probe run upstream r1 --depth 2"])
def test_the_agent_reads_a_run_by_its_id(tmp_path, command):
    """The agent launched the run and logged to it but could not look at it: is
    the loss falling, did the checkpoint land (Richard 2026-10-21)."""
    assert _guard(tmp_path, command) is None


@pytest.mark.parametrize("command,matched", [("probe series latest --project p1", "probe series"),
                                             ("probe artifact list --project p1", "probe artifact list"),
                                             ("probe provenance r1", "probe provenance"),
                                             ("probe artifact pin-impact a1", "probe artifact pin-impact")])
def test_a_listing_across_the_teams_work_stays_the_daemons(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command,matched", [("probe run set r1 --title x", "probe run set"),
                                             ("probe run tag r1 good", "probe run tag")])
def test_naming_and_filing_its_run_stays_the_daemons(tmp_path, command, matched):
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY_WRITE.format(matched=matched)


def test_no_run_read_is_a_write():
    """The set opens reads, never a write the daemon owns."""
    for key in session_marker.DAEMON_PROFILE_RUN_READS:
        assert session_marker.classify_probe_args([*key.split(), "r1"])[0] != "write", key


@pytest.mark.parametrize("command,matched", [("probe run delete r1", "probe run"),
                                             ("probe project reference remove p1 r1", "probe project reference"),
                                             ("probe shared delete f1", "probe shared"),
                                             ("probe commits --project p1", "probe commits"),
                                             ("probe snapshot-restore r1", "probe snapshot-restore"),
                                             ("probe session export s1", "probe session"),
                                             ("probe mcp call search_runs", "probe mcp"),
                                             ("probe mcp tools", "probe mcp"),
                                             ("probe session inline", "probe session"),
                                             ("probe install --yes", "probe install"),
                                             ("probe desktop request < req.json", "probe desktop"),
                                             ("probe wizard", "probe wizard"),
                                             ("probe wizard --action recorder --yes", "probe wizard"),
                                             ("probe wizard --action $ACTION", "probe wizard"),
                                             ("probe wizard --action update --who-records agent", "probe wizard"),
                                             ("probe wizard --action update --action recorder", "probe wizard"),
                                             ("probe wizard --action update --action", "probe wizard"),
                                             ("probe setup --action=update --no-tracking", "probe setup"),
                                             ("probe wizard --action update --who-records=agent", "probe wizard"),
                                             ("probe wizard --action update --folder ~/runs", "probe wizard"),
                                             ("probe wizard --action update $FLAGS", "probe wizard"),
                                             ("probe wizard --action login --no-browser", "probe wizard"),
                                             ("probe login", "probe login"),
                                             ("PROBE_BASE_URL=http://x.example probe login", "probe login"),
                                             ("probe token create", "probe token"),
                                             ("probe outbox resume", "probe outbox"),
                                             ("probe wizard --action logout --yes", "probe wizard"),
                                             ("probe --base-url https://x.example wizard --action update", "probe wizard"),
                                             ("probe login --token t", "probe login"),
                                             ("probe login --base-url https://x.example", "probe login"),
                                             ("probe logout", "probe logout"),
                                             ("probe context use other-team", "probe context"),
                                             ("probe context delete default", "probe context"),
                                             ("probe workspace use ws", "probe workspace"),
                                             ("probe workspace limit ws --yes", "probe workspace"),
                                             ("probe workspace limit --team", "probe workspace"),
                                             ("probe project use p1", "probe project use"),
                                             ("probe token revoke t1", "probe token"),
                                             ("probe session initialize --session s1 --cwd .", "probe session"),
                                             ("probe outbox discard --held", "probe outbox"),
                                             ("probe outbox pause", "probe outbox"),
                                             ("probe workspace delete ws --yes", "probe workspace"),
                                             ("probe workspace create ws", "probe workspace"),
                                             ("probe workspace writers set ws --open", "probe workspace"),
                                             ("probe access-group add g1 u1", "probe access-group"),
                                             ("probe access-group remove g1 u1", "probe access-group"),
                                             ("probe mcp headers", "probe mcp"),
                                             ("probe statusline install --plugin-root /tmp/x", "probe statusline"),
                                             ("probe companion authorize", "probe companion"),
                                             ("probe companion trace --session s1", "probe companion"),
                                             ("probe daemon install", "probe daemon"),
                                             ("probe snapshot-prune-refs --force", "probe snapshot-prune-refs"),
                                             ("probe run reproduce r1 --materialize ./tree", "probe run reproduce"),
                                             ("probe run reproduce r1 --export=rec.json", "probe run reproduce")])
def test_tracking_that_reads_as_neither_stays_the_daemons(tmp_path, command, matched):
    """Removals (the daemon asks before deleting another researcher's work),
    record reads the classifier does not sort, the agent taking Probe over
    (`session inline`, CLIs of 2026-10-05..06), the researcher's own settings in
    the wizard, and what moves the key, account, server or folder the daemon
    records with (signing in included), holds its queue, or changes the team's
    permissions."""
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command,matched", [("probe $G delete r1", "probe $G"),
                                             ("probe ${G:-run} delete r1", "probe ${G:-run}"),
                                             ('probe "$G" list', "probe $G"),
                                             ("probe brand-new-command", "probe brand-new-command")])
def test_a_word_the_guard_cannot_read_stays_refused(tmp_path, command, matched):
    """`probe $G delete r1` runs `run delete` once the shell expands it; a
    command the guard does not know may be anything."""
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


@pytest.mark.parametrize("command,matched", [("probe wizard --who-records agent --folder --help", "probe wizard"),
                                             ("probe run list --fields --help", "probe run list")])
def test_a_help_flag_click_takes_as_a_value_is_no_help_request(tmp_path, command, matched):
    """Click hands `--help` to the bare option before it and runs the command."""
    assert _guard(tmp_path, command) == session_marker.DAEMON_PROFILE_DENY.format(matched=matched)


#: Commands the classifier reads as neither a read nor a write that stay the
#: daemon's or the researcher's in the daemon profile, beyond removals and the
#: switch. Sorting a new command means adding it here or to
#: `session_marker.DAEMON_PROFILE_ALLOWED`.
DAEMONS = {
    # The daemon's own commands, its ledger (full model requests, any session),
    # its install and the key the researcher approves for it.
    "daemon override", "daemon session", "daemon task", "daemon worker", "daemon install",
    "companion authorize", "companion log", "companion trace", "companion report",
    # Record reads the classifier does not sort, and the MCP the profile removes
    # (`headers` and `env` print its token into the transcript).
    "commits", "snapshot-restore", "session export", "mcp call", "mcp tools", "mcp headers", "mcp env",
    "mcp token set", "mcp token unset",
    # What moves the key, account or folder the daemon records with, or holds
    # and drops its queued writes.
    "login", "logout", "context use", "workspace use", "workspace limit", "project use", "token revoke",
    "token create",
    "session initialize", "outbox adopt", "outbox discard", "outbox pause", "outbox resume",
    "snapshot-prune-refs",
    # The team's permissions and workspaces.
    "workspace create", "workspace rename", "workspace writers set", "access-group create",
    "access-group rename", "access-group add",
    # The researcher's: a no, their agent settings, the guided install, the
    # desktop app's interface (it starts imports), and the agent taking Probe
    # over in CLIs of 2026-10-05..06.
    "deny", "statusline install", "statusline uninstall", "install", "uninstall", "desktop", "session inline",
    "session daemon",
    # The install pipeline in repair mode: it may re-approve the daemon's key
    # and change the researcher's agent settings, as the guided install does.
    "repair",
}


def test_every_command_that_neither_reads_nor_writes_is_sorted():
    """The ratchet the stale allowlist lacked (`probe update --check` refused,
    2026-10-21): every command the classifier reads as neither a read nor a
    write runs in the daemon profile (`DAEMON_PROFILE_ALLOWED`, or plainly as
    the wizard) or is the daemon's (`DAEMONS`, a removal, the
    switch). A new one fails here until it is sorted, rather than being refused
    unnoticed or allowed by default."""
    import importlib

    import typer.main

    cli_main = importlib.import_module("probe.cli.main")

    def walk(node, path):
        subs = getattr(node, "commands", None)
        if not subs:
            yield path
            return
        for name, sub in subs.items():
            yield from walk(sub, [*path, name])

    def daemons(path):
        keys = {" ".join(path[:3]), " ".join(path[:2]), path[0]}
        return (bool(keys & DAEMONS) or path[-1] in session_marker.REMOVAL_VERBS
                or " ".join(path[:2]) in session_marker.RESEARCHER_SWITCH)

    root = typer.main.get_command(cli_main.app)
    unsorted, both = [], []
    for path in walk(root, []):
        if session_marker.classify_probe_args(path)[0] is not None:
            continue
        runs = session_marker.daemon_profile_allows(path)[0] or path[0] in session_marker.DAEMON_PROFILE_PLAIN_FLAGS
        if runs and daemons(path):
            both.append(" ".join(path))
        elif not runs and not daemons(path):
            unsorted.append(" ".join(path))
    assert not unsorted, f"{unsorted}: sort each into session_marker.DAEMON_PROFILE_ALLOWED or DAEMONS here"
    assert not both, both
    for key in (DAEMONS - {"session inline", "session daemon"}) | session_marker.DAEMON_PROFILE_ALLOWED:
        node = root
        for word in key.split():
            node = getattr(node, "commands", {}).get(word)
            assert node is not None, key
    assert session_marker.daemon_profile_allows(["update", "--check"]) == (True, "probe update")


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
    # instrument-code: the researcher mints a remote job's token (browser approval).
    "probe token",
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


# ---------------------------------------------------------------------------
# The per-session-state folder: a tripwire like the approvals one. Those files
# decide the guard's own verdict, so forging `on (inline)` would turn it off.
# ---------------------------------------------------------------------------


def test_the_sessions_folder_is_a_tripwire_like_approvals():
    import os

    root = str(session_marker.sessions_dir())
    # A Write/Edit whose file is inside the folder.
    for tool, field in [("Write", "file_path"), ("Edit", "file_path"), ("NotebookEdit", "notebook_path")]:
        target = os.path.join(root, f"{SID}.state")
        assert session_marker.touches_sessions_dir(tool, {field: target}) == target
    assert session_marker.touches_sessions_dir("Write", {"file_path": os.path.join(root, f"{SID}.inline")})
    # A relative path resolved against the session's cwd.
    assert session_marker.touches_sessions_dir("Write", {"file_path": f"{SID}.profile"}, cwd=root)
    # A Bash command that names the folder.
    assert session_marker.touches_sessions_dir("Bash", {"command": f"printf full > {root}/{SID}.state"})
    assert session_marker.touches_sessions_dir("Bash", {"command": "echo x > state/probe/sessions/s.inline"})
    # A command that does not name it is not caught.
    assert session_marker.touches_sessions_dir("Bash", {"command": "probe run get r1"}) is None
    assert session_marker.touches_sessions_dir("Read", {"file_path": os.path.join(root, f"{SID}.state")}) is None


def test_the_hook_refuses_forging_the_session_state(tmp_path):
    # The whole point: a Bash write into the sessions folder is refused before it
    # can flip the session to `on (inline)` and switch the guard off.
    reason = _guard(tmp_path, "printf full > state/probe/sessions/x.inline")
    assert reason is not None and "turn the guard off" in reason


def test_the_sessions_tripwire_fires_in_the_agent_profile_too(tmp_path):
    reason = _guard(tmp_path, "printf full > state/probe/sessions/x.state", profile="")
    assert reason is not None and "turn the guard off" in reason
