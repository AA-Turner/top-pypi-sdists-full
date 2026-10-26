"""The `probe` CLI's own write gate (`probe.cli.write_gate`).

The gate is what makes the `daemon` state hold on every harness: pi has no
pre-tool hook, so the only thing that can stop the agent writing over
the daemon is the CLI refusing. These tests pin each state against each class
of command, the `--directed` escape, the degraded fallback, and -- the one that
keeps the gate honest as the CLI grows -- that every top-level command has been
sorted into a class on purpose.
"""

from __future__ import annotations

import importlib
import json
import time

import pytest
import typer.main

from probe.cli import write_gate
from probe.sdk import session_marker

# `probe.cli` re-exports the `main` FUNCTION, which shadows the module.
cli_main = importlib.import_module("probe.cli.main")

SID = "11111111-2222-3333-4444-555555555555"
ENV = {"CLAUDE_CODE_SESSION_ID": SID, "CLAUDECODE": "1"}


@pytest.fixture(autouse=True)
def _state_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    # Inside a run the gate never refuses; another test leaving the variable in
    # os.environ must not decide these.
    monkeypatch.delenv(write_gate.RUN_ID_ENV, raising=False)
    monkeypatch.chdir(tmp_path)


def _set(state: str) -> None:
    assert session_marker.set_session_state(SID, state)


def _lease(*, expires_in: float = 60.0, reason: str | None = None) -> None:
    path = session_marker.lease_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    path.write_text(
        json.dumps(
            {
                "v": session_marker.LEASE_VERSION,
                "writer": "daemon",
                "pid": 1,
                "expires_at": now + expires_in,
                "renewed_at": now,
                "reason": reason,
            }
        )
    )


def _refusal(argv: list[str], env=ENV) -> str | None:
    args, directed = write_gate.split_directed(argv)
    return write_gate.refusal(args, directed=directed, env=env)


# ---------------------------------------------------------------------------
# --directed is stripped wherever it appears, but never out of `exec`'s child.
# ---------------------------------------------------------------------------


def test_split_directed_strips_the_flag_anywhere_before_the_separator():
    assert write_gate.split_directed(["notes", "push", "x.md", "--directed"]) == (
        ["notes", "push", "x.md"],
        True,
    )
    assert write_gate.split_directed(["--directed", "run", "set", "r"]) == (["run", "set", "r"], True)
    assert write_gate.split_directed(["run", "list"]) == (["run", "list"], False)


def test_split_directed_leaves_the_launched_command_alone():
    argv = ["exec", "--", "python", "train.py", "--directed"]
    assert write_gate.split_directed(argv) == (argv, False)


# ---------------------------------------------------------------------------
# A shell with no session id is a person's terminal: never gated.
# ---------------------------------------------------------------------------


def test_no_session_id_is_never_gated():
    _set(session_marker.STATE_OFF)
    assert _refusal(["notes", "push", "x.md"], env={}) is None
    assert _refusal(["run", "list"], env={}) is None


# ---------------------------------------------------------------------------
# State x command class.
# ---------------------------------------------------------------------------


def test_full_allows_everything():
    _set(session_marker.STATE_FULL)
    assert _refusal(["notes", "push", "x.md"]) is None
    assert _refusal(["run", "list"]) is None


def test_read_only_refuses_writes_and_allows_reads():
    _set(session_marker.STATE_READ_ONLY)
    reason = _refusal(["notes", "push", "x.md"])
    assert reason is not None and "READ-ONLY" in reason and "`probe notes push`" in reason
    assert _refusal(["run", "list"]) is None
    # --directed is a daemon-state mark, not a way past read-only.
    assert _refusal(["notes", "push", "x.md", "--directed"]) is not None


def test_off_refuses_reads_and_writes():
    _set(session_marker.STATE_OFF)
    assert "OFF" in (_refusal(["notes", "push", "x.md"]) or "")
    assert "OFF" in (_refusal(["run", "list"]) or "")


def test_the_switch_and_removals_are_never_refused():
    for state in (session_marker.STATE_OFF, session_marker.STATE_READ_ONLY, session_marker.STATE_DAEMON):
        _set(state)
        _lease()
        assert _refusal(["session", "state", "on"]) is None, state
        assert _refusal(["run", "delete", "r1"]) is None, state
        # The team note's own background sync is plumbing, not a record.
        assert _refusal(["notes", "sync"]) is None, state


def test_help_is_never_refused():
    _set(session_marker.STATE_OFF)
    assert _refusal(["notes", "push", "--help"]) is None
    # `-h` is not a flag this CLI has, so it proves nothing about intent.
    assert _refusal(["wandb", "import-local", "-h"]) is not None


@pytest.mark.parametrize("state", [session_marker.STATE_READ_ONLY, session_marker.STATE_DAEMON])
def test_help_as_an_options_value_is_still_the_write_it_names(state):
    """`--title --help` titles the note `--help`: click creates it. A token search
    for `--help` let the write past the gate under read-only and daemon."""
    _set(state)
    _lease()
    assert _refusal(["notes", "create", "--run", "R", "--title", "--help", "eval.md"]) is not None
    assert _refusal(["notes", "create", "--run", "R", "--title=--help", "eval.md"]) is not None
    # Help as click reads it, on a command, a group or `probe` itself, is still only help.
    for argv in (["notes", "create", "--help"], ["notes", "create", "--run", "R", "eval.md", "--help"],
                 ["notes", "--help"], ["project", "code", "--help"], ["--sync", "--help"]):
        assert _refusal(argv) is None, argv


@pytest.mark.parametrize(
    "argv",
    [
        ["--base-url", "https://api.example", "notes", "push", "n.md"],
        ["--spool-dir", "/tmp/x", "notes", "push", "n.md"],
        ["--", "notes", "push", "n.md"],
        ["notes", "--", "push", "n.md"],
    ],
)
def test_argv_shapes_click_still_dispatches_are_classified(argv):
    _set(session_marker.STATE_READ_ONLY)
    assert _refusal(argv) is not None


def test_a_runs_own_data_is_not_gated_but_other_writes_are():
    _set(session_marker.STATE_OFF)
    inside = {**ENV, "PROBE_RUN_ID": "r"}
    assert _refusal(["log", "loss=1"], env=inside) is None
    assert _refusal(["notes", "push", "x.md"], env=inside) is not None


@pytest.mark.parametrize(
    "argv",
    [
        ["artifact", "add", "r1", "plot.png"],
        ["artifact", "add", "r1", "ckpt.pt", "--reference", "--kind", "checkpoint"],
    ],
)
def test_inside_a_run_artifact_add_is_the_runs_own_data_under_a_live_lease(argv):
    # The SDK's `log_artifact` in the same script was never gated; the CLI spelling
    # of the same write was refused (seen with CLI 0.179.2).
    _set(session_marker.STATE_DAEMON)
    _lease()
    assert _refusal(argv, env={**ENV, "PROBE_RUN_ID": "r1"}) is None
    # From the agent's own shell it is still the daemon's.
    assert _refusal(argv) is not None


@pytest.mark.parametrize(
    "flag",
    [["--project", "p"], ["--project=p"], ["--experiment", "e"], ["--workspace", "w"], ["--shared"],
     ["--from-manifest", "m.jsonl"]],
)
def test_inside_a_run_an_artifact_filed_elsewhere_is_still_the_daemons(flag):
    _set(session_marker.STATE_DAEMON)
    _lease()
    inside = {**ENV, "PROBE_RUN_ID": "r1"}
    assert _refusal(["artifact", "add", "report.md", *flag], env=inside) is not None


@pytest.mark.parametrize(
    "state", [session_marker.STATE_READ_ONLY, session_marker.STATE_OFF, session_marker.STATE_DAEMON]
)
@pytest.mark.parametrize(
    "argv",
    [
        ["artifact", "add", "r1", "plot.png"],
        ["artifact", "add", "id:r1", "plot.png"],
        ["artifact", "add", "--name", "loss", "r1", "plot.png"],
        ["artifact", "add", "--notes=why", "--reference", "r1", "ckpt.pt"],
        ["--base-url", "https://api.example", "artifact", "add", "r1", "plot.png"],
    ],
)
def test_inside_a_run_its_own_artifact_passes_in_every_state(state, argv):
    """The run's own file, like `probe log` there: the switch never governed it."""
    _set(state)
    assert _refusal(argv, env={**ENV, "PROBE_RUN_ID": "r1"}) is None


@pytest.mark.parametrize(
    "state", [session_marker.STATE_READ_ONLY, session_marker.STATE_OFF, session_marker.STATE_DAEMON]
)
@pytest.mark.parametrize(
    "argv",
    [
        # Another run: a write ABOUT a run, not the run recording itself.
        ["artifact", "add", "r2", "plot.png"],
        ["artifact", "add", "id:r2", "plot.png"],
        # `--name r1` is an option value, not the RUN argument.
        ["artifact", "add", "--name", "r1", "r2", "plot.png"],
        # No RUN argument found at all.
        ["artifact", "add"],
    ],
)
def test_inside_a_run_an_artifact_for_another_run_is_gated(state, argv):
    # daemon with NO lease is degraded (the agent writes freely), so the daemon
    # case is checked under a live lease, where the gate refuses.
    _set(state)
    if state == session_marker.STATE_DAEMON:
        _lease()
    assert _refusal(argv, env={**ENV, "PROBE_RUN_ID": "r1"}) is not None


def test_inside_a_run_notes_stay_the_daemons():
    _set(session_marker.STATE_DAEMON)
    _lease()
    inside = {**ENV, "PROBE_RUN_ID": "r1"}
    assert _refusal(["notes", "create", "r1"], env=inside) is not None
    assert _refusal(["notes", "push", "x.md"], env=inside) is not None
    assert _refusal(["artifact", "version-add", "a1", "f.txt"], env=inside) is not None


def test_daemon_feedback_needs_directed_in_every_state():
    _set(session_marker.STATE_FULL)
    assert _refusal(["companion", "feedback", "3", "--wrong"]) is not None
    assert _refusal(["companion", "feedback", "3", "--wrong", "--directed"]) is None


def test_a_refused_exec_runs_its_command_unrecorded():
    assert write_gate.exec_child(["exec", "--name", "x", "--", "python", "t.py"]) == ["python", "t.py"]
    assert write_gate.exec_child(["exec", "--name", "x"]) is None
    assert write_gate.exec_child(["notes", "push", "--", "x"]) is None


def test_daemon_with_a_live_lease_refuses_ambient_writes():
    _set(session_marker.STATE_DAEMON)
    _lease()
    reason = _refusal(["notes", "push", "x.md"])
    assert reason is not None and "--directed" in reason and "`probe notes push`" in reason
    assert _refusal(["run", "set", "r1", "--description", "d"]) is not None
    assert _refusal(["artifact", "add", "r1", "f.txt"]) is not None
    assert _refusal(["group", "set", "g1", "--name", "n"]) is not None


def test_the_daemon_refusal_names_what_stays_the_agents():
    _set(session_marker.STATE_DAEMON)
    _lease()
    reason = _refusal(["notes", "push", "x.md"]) or ""
    for word in ("project", "experiment", "group", "run end", "probe session status", "--directed"):
        assert word in reason, word


def test_daemon_lets_the_researchers_own_writes_through_with_directed():
    _set(session_marker.STATE_DAEMON)
    _lease()
    assert _refusal(["notes", "push", "x.md", "--directed"]) is None


@pytest.mark.parametrize(
    "argv",
    [
        ["exec", "--", "python", "train.py"],
        ["log", "r1", "loss=0.1"],
        ["snapshot"],
        ["run", "start", "--name", "x"],
        ["run", "end", "r1"],
        ["run", "fork", "r1", "--step", "4"],
        ["span", "add", "r1"],
        ["trial", "add", "r1", "dir"],
        ["trial", "stage", "dir", "--to", "out"],
    ],
)
def test_daemon_leaves_launches_and_run_data_to_the_agent(argv):
    _set(session_marker.STATE_DAEMON)
    _lease()
    assert _refusal(argv) is None


@pytest.mark.parametrize(
    "argv",
    [
        ["project", "create", "p"],
        ["experiment", "create", "e"],
        ["group", "create", "e", "--name", "lr-sweep"],
    ],
)
def test_daemon_creates_the_containers_runs_are_filed_in(argv):
    """Daemon v2 (D2, S11): runs start floating and the daemon creates the
    project, experiment and group it files them in, so the agent's creates are
    refused like any other daemon write -- and pass with `--directed`."""
    _set(session_marker.STATE_DAEMON)
    _lease()
    assert _refusal(argv) is not None
    assert _refusal([*argv, "--directed"]) is None


def test_daemon_allows_reads():
    _set(session_marker.STATE_DAEMON)
    _lease()
    assert _refusal(["run", "list"]) is None
    assert _refusal(["metrics", "r1"]) is None


@pytest.mark.parametrize(
    "lease",
    [None, {"expires_in": -1.0}, {"reason": "unauthorized"}],
    ids=["never-started", "expired", "released"],
)
def test_degraded_daemon_hands_writing_back_to_the_agent(lease):
    _set(session_marker.STATE_DAEMON)
    if lease is not None:
        _lease(**lease)
    assert _refusal(["notes", "push", "x.md"]) is None


def test_a_malformed_lease_fails_open():
    _set(session_marker.STATE_DAEMON)
    session_marker.lease_path(SID).parent.mkdir(parents=True, exist_ok=True)
    session_marker.lease_path(SID).write_text("{not json")
    assert _refusal(["notes", "push", "x.md"]) is None


def test_a_session_with_no_stored_state_is_not_gated(tmp_path, monkeypatch):
    # A person's own terminal can carry an id-shaped variable (a stale export) with
    # no session behind it. Only a harness session -- seeded at start -- is gated,
    # whatever the folder or machine default says.
    folder = tmp_path / "repo"
    (folder / ".probe").mkdir(parents=True)
    (folder / ".probe" / "config.json").write_text(json.dumps({"defaults": {"session_state": "off"}}))
    monkeypatch.chdir(folder)
    assert _refusal(["notes", "push", "x.md"]) is None


# ---------------------------------------------------------------------------
# main() refuses before any command runs, and strips --directed before parsing.
# ---------------------------------------------------------------------------


def test_main_refuses_with_its_own_exit_code(monkeypatch, capsys):
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    _set(session_marker.STATE_READ_ONLY)
    assert cli_main.main(["notes", "push", "x.md"]) == write_gate.EXIT_REFUSED
    assert "READ-ONLY" in capsys.readouterr().err


def test_main_strips_directed_so_the_subcommand_parser_never_sees_it(monkeypatch, capsys):
    # `whoami` is not a research command, so the gate lets it through; with the
    # flag left in, click would fail it as an unknown option (exit 2).
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    _set(session_marker.STATE_DAEMON)
    assert cli_main.main(["--directed", "whoami", "--help"]) == 0


# ---------------------------------------------------------------------------
# Every top-level command is sorted on purpose.
# ---------------------------------------------------------------------------

#: Top-level commands that record nothing about the research: machine setup,
#: credentials, the switch itself, outbox plumbing, local views. A new command
#: must land in a class in `session_marker` or here -- deciding by omission is
#: how a write slips past the daemon state unnoticed.
NOT_RESEARCH = frozenset(
    {
        "access-group",
        "agent-rules",
        # Local daemon tooling (daemon v2): `probe daemon worker` is spawned by
        # capture and must never be refused; `approvals` / `deny` answer the
        # daemon's local questions. None of them writes research to Probe.
        "approvals",
        # `probe ignore check` tests a path against the local `.probe.config`
        # files: nothing is sent, nothing is recorded.
        "ignore",
        # `probe ask` files a question for the daemon's reader in a local mailbox
        # (daemon reads); it writes nothing to Probe.
        "ask",
        # `probe capy` is hidden: it only takes down what removed Capy capture
        # left on a machine, never a research write.
        "capy",
        "commits",
        "companion",
        "context",
        "daemon",
        "deny",
        # The desktop app's JSON interface over the import engine; imports run
        # only after the researcher approves them in the app.
        "desktop",
        "doctor",
        # `probe draft edit` changes a checked-out draft on disk (the push is the
        # write) and `probe file preview` prints a local file: nothing reaches Probe.
        "draft",
        "file",
        # `probe feedback send` holds feedback for the Probe team as a question
        # for the researcher; the CLI refuses it under `off` itself.
        "feedback",
        "flush",
        "install",
        "login",
        "logout",
        "mcp",
        "outbox",
        "session",
        "setup",
        # Local `.git` housekeeping (plan 2.6): deletes old shadow refs, writes
        # nothing to Probe.
        "snapshot-prune-refs",
        "snapshot-restore",
        "snapshot-show",
        # `probe service`: the machine-wide Probe service's own plumbing.
        "service",
        # `probe status`: this device's install as data, like `doctor`.
        "status",
        "statusline",
        # Delivers runs recorded with PROBE_MODE=offline: outbox plumbing like
        # `flush`, for queues nothing else drains (plan 2.12).
        "sync",
        "token",
        "update",
        "version",
        "whoami",
        "wizard",
        "workspace",
    }
)


def test_every_top_level_command_is_classified():
    command = typer.main.get_command(cli_main.app)
    classified = (
        session_marker.TOP_LEVEL_WRITES
        | session_marker.WRITE_GROUPS
        | session_marker.READ_GROUPS
        | NOT_RESEARCH
    )
    unclassified = sorted(set(command.commands) - classified)
    assert not unclassified, (
        f"{unclassified}: sort each into TOP_LEVEL_WRITES / WRITE_GROUPS / READ_GROUPS in "
        "session_marker, or into NOT_RESEARCH here"
    )


#: Every command inside a write group whose verb only reads. A verb the gate does
#: not know counts as a write, so a new read command is refused in `read` and
#: `daemon` until it is sorted here -- how `probe artifact tree` came to be
#: refused as the daemon's write in the second daemon trial.
WRITE_GROUP_READS = frozenset(
    {
        "version list",
        "summary checkout", "visuals options",
        "checkpoint list", "dataset download", "dataset list", "dataset show", "source list", "source show",
        "artifact download", "artifact list", "artifact pin-impact", "artifact tree",
        "artifact versions",
        "experiment branch", "experiment edges", "experiment get", "experiment inherited",
        "experiment lineage", "experiment list",
        "experiment reproduce",
        "group get", "group list",
        "notes audit-advisory", "notes checkout", "notes find", "notes list", "notes show", "notes status",
        "notes team",
        "paper citations", "paper edges", "paper find", "paper graph", "paper list",
        "project branches", "project code list", "project contributors", "project get",
        "project lineage", "project list",
        "run check", "run get", "run inputs", "run list", "run metrics", "run reproduce", "run series",
        "run upstream",
        "span get", "span list",
        "trial get", "trial list",
        "views data", "views list", "views preview", "views show",
    }
)

#: Commands inside a write group that the gate lets through in every state:
#: cleanup (REMOVAL_VERBS) and machine plumbing (UNGATED_COMMANDS).
WRITE_GROUP_UNGATED = frozenset(
    {
        "artifact delete", "edge remove", "experiment delete", "notes delete", "paper remove",
        "project delete", "project reference remove", "run delete", "views delete",
        "notes sync", "project use", "wandb discover", "wandb key set", "wandb key status",
    }
)

#: Every command inside a write group that records research. Listed so that a
#: command missing from EVERY list fails the test below: the gate would call it
#: a write by default, and a new read would be refused without anyone deciding.
WRITE_GROUP_WRITES = frozenset(
    {
        "version create",
        "summary push", "visuals set",
        "checkpoint use", "dataset add", "dataset use", "source add",
        "artifact add", "artifact gc-uploads", "artifact move", "artifact set",
        "artifact version-add",
        "edge add",
        "experiment create", "experiment fork", "experiment freeze", "experiment move",
        "experiment set",
        "experiment tag",
        "group create", "group set",
        "notes append", "notes create", "notes edit", "notes push", "notes rename", "notes write",
        "paper add", "paper tag", "paper update",
        "project code attach", "project code confirm", "project code detach",
        "project create", "project move", "project patch", "project reference add", "project set",
        "project tag",
        # `run move` files a floating run: the daemon's in `daemon` state.
        "run child", "run end", "run expect", "run fork", "run move", "run set", "run start", "run tag",
        "span add",
        # `trial export` uploads a staged trial; `export` read as a read verb
        # let `read` through it.
        "trial add", "trial drain", "trial expand", "trial export", "trial reconcile", "trial set", "trial stage",
        "trial watch",
        "views create", "views rename", "views update",
        "wandb import-hosted", "wandb import-local",
    }
)


def test_every_write_group_command_is_sorted_on_purpose():
    command = typer.main.get_command(cli_main.app)
    declared = {
        "read": WRITE_GROUP_READS,
        None: WRITE_GROUP_UNGATED,
        "write": WRITE_GROUP_WRITES,
    }
    lists = list(declared.values())
    for i, one in enumerate(lists):
        for other in lists[i + 1:]:
            assert not (one & other), f"sorted twice: {sorted(one & other)}"
    actual = set()
    unsplit = []
    for group in session_marker.WRITE_GROUPS:
        for verb, node in command.commands[group].commands.items():
            key = f"{group} {verb}"
            if hasattr(node, "commands"):
                if key not in session_marker.SUBGROUPS:
                    unsplit.append(key)
                actual |= {f"{key} {sub}" for sub in node.commands}
            else:
                actual.add(key)
    # A subgroup the classifier reads two words deep is one write, so its reads
    # are refused: how `project code list` was refused before SUBGROUPS existed.
    assert not unsplit, f"{unsplit}: add each to session_marker.SUBGROUPS"
    undeclared = sorted(actual - set().union(*lists))
    assert not undeclared, (
        f"{undeclared}: sort each into WRITE_GROUP_READS (and its verb into session_marker.READ_VERBS, "
        "or the command into READ_UNLESS_FLAGS), WRITE_GROUP_UNGATED or WRITE_GROUP_WRITES"
    )
    gone = sorted(set().union(*lists) - actual)
    assert not gone, f"{gone}: no longer a command; drop it from the lists here"
    wrong = []
    for want, keys in declared.items():
        for key in sorted(keys):
            kind, _ = session_marker.classify_probe_args(key.split())
            if kind != want:
                wrong.append(f"{key}: gate says {kind}, declared {want}")
    assert not wrong, (
        f"{wrong}: a command that only reads needs its verb in session_marker.READ_VERBS "
        "(or, if a flag makes it write, an entry in READ_UNLESS_FLAGS); one that writes must "
        "not share a read verb"
    )


#: Options on a READ_UNLESS_FLAGS command that only shape what it prints.
READ_ONLY_OPTIONS = frozenset({"--fields"})


#: Every command inside a read group, sorted the same way. A read group made every
#: verb a read, so `read` let `shared add` upload and `metrics backfill` store a
#: curve, and `off` refused `metrics delete`, cleanup that every other group allows.
READ_GROUP_COMMANDS = {
    "read": frozenset(
        {"metrics export", "metrics grouped", "metrics plot", "metrics wide", "series latest", "shared download",
         "shared list"}
    ),
    None: frozenset({"metrics delete", "shared delete"}),
    "write": frozenset({"metrics backfill", "shared add", "shared share", "shared unshare"}),
}


def test_every_read_group_command_is_sorted_on_purpose():
    command = typer.main.get_command(cli_main.app)
    actual = {
        f"{group} {verb}"
        for group in session_marker.READ_GROUPS
        for verb in getattr(command.commands[group], "commands", {})
    }
    assert "shared add" in actual, "the walk found no read group's commands"
    declared = set().union(*READ_GROUP_COMMANDS.values())
    assert sorted(actual - declared) == [], "sort each into READ_GROUP_COMMANDS (and session_marker)"
    assert sorted(declared - actual) == [], "no longer a command; drop it here"
    wrong = [
        f"{key}: gate says {kind}, declared {want}"
        for want, keys in READ_GROUP_COMMANDS.items()
        for key in sorted(keys)
        if (kind := session_marker.classify_probe_args(key.split())[0]) != want
    ]
    assert not wrong, f"{wrong}: a write goes in session_marker.READ_GROUP_WRITES, a removal in READ_GROUP_REMOVALS"


def test_a_read_groups_writes_are_refused_and_its_removals_never_are():
    _set(session_marker.STATE_READ_ONLY)
    for argv in (["shared", "add", "x.csv"], ["metrics", "backfill", "r1", "--file", "c.json"],
                 ["shared", "share", "a1"], ["shared", "unshare", "a1"], ["trial", "export", "req.json"]):
        assert "READ-ONLY" in (_refusal(argv) or ""), argv
    assert _refusal(["shared", "list"]) is None
    for state in (session_marker.STATE_OFF, session_marker.STATE_READ_ONLY):
        _set(state)
        assert _refusal(["metrics", "delete", "r1", "--key", "loss_ema"]) is None, state
        assert _refusal(["shared", "delete", "a1"]) is None, state


def test_read_unless_flags_name_every_option_that_writes():
    """A write flag missing from READ_UNLESS_FLAGS reads as a read and runs in
    read-only: every option is either declared a write or known to only read."""
    command = typer.main.get_command(cli_main.app)
    for key, flags in session_marker.READ_UNLESS_FLAGS.items():
        node = command
        for word in key.split():
            node = node.commands[word]
        options = {
            opt
            for param in node.params
            if param.param_type_name == "option"
            for opt in (*param.opts, *param.secondary_opts)
        }
        assert flags <= options, f"{key}: {sorted(flags - options)} is no longer an option"
        unsorted = options - flags - READ_ONLY_OPTIONS
        assert not unsorted, f"{key}: sort {sorted(unsorted)} into READ_UNLESS_FLAGS or READ_ONLY_OPTIONS"


def test_a_new_verb_under_a_subgroup_is_a_write_until_sorted():
    assert session_marker.classify_probe_args(["wandb", "key", "rotate"])[0] == "write"
    assert session_marker.classify_probe_args(["project", "code", "sync", "p1"])[0] == "write"


def test_an_empty_command_word_classifies_as_nothing():
    for argv in ([""], [" "], ["", "project"]):
        assert session_marker.classify_probe_args(argv) == (None, "probe " + argv[0]), argv


def test_nested_and_flagged_reads_are_reads():
    """`project code list` and bare `project contributors` read; two words deep
    they looked like writes, and read-only refused them."""
    _set(session_marker.STATE_READ_ONLY)
    for argv in (["project", "code", "list", "p1"], ["project", "contributors", "p1"]):
        assert _refusal(argv) is None, argv
    for argv, matched in (
        (["project", "code", "attach", "p1", "org/repo"], "`probe project code attach`"),
        (["project", "contributors", "p1", "--add", "u1"], "`probe project contributors`"),
        (["project", "contributors", "p1", "--remove=u1"], "`probe project contributors`"),
    ):
        assert matched in (_refusal(argv) or ""), argv
    _set(session_marker.STATE_OFF)
    assert "OFF" in (_refusal(["project", "code", "list", "p1"]) or "")


def test_local_wandb_commands_are_never_refused():
    """`wandb discover` scans a folder and `wandb key` a local credential;
    only the imports write to Probe."""
    for state in (session_marker.STATE_OFF, session_marker.STATE_READ_ONLY, session_marker.STATE_DAEMON):
        _set(state)
        _lease()
        for argv in (["wandb", "discover", "./runs"], ["wandb", "key", "status"],
                     ["wandb", "key", "set", "--key", "k"]):
            assert _refusal(argv) is None, (state, argv)
        assert _refusal(["wandb", "import-local", "./runs", "--project", "p1"]) is not None, state


def test_daemon_lets_the_agent_read_what_is_recorded():
    _set(session_marker.STATE_DAEMON)
    _lease()
    for argv in (["artifact", "tree", "r1"], ["run", "metrics", "r1"], ["experiment", "edges", "e1"],
                 ["views", "preview", "--spec-file", "-"], ["run", "inputs", "r1"],
                 ["run", "upstream", "r1", "--depth", "3"], ["experiment", "lineage", "e1"],
                 ["project", "lineage", "p1"]):
        assert _refusal(argv) is None, argv
    # The daemon's own shell files them as lookups, not writes (`daemon/tools.py`).
    from probe.daemon import precheck

    for argv in (["experiment", "lineage", "e1"], ["project", "lineage", "p1"]):
        assert precheck.parse(argv).owner == precheck.READ, argv
    # Correcting a read's match is a write (the researcher's), read three words deep.
    assert _refusal(["run", "input", "dismiss", "r1", "data/x.csv"]) is not None


def test_every_daemon_exemption_names_a_real_command():
    command = typer.main.get_command(cli_main.app)
    for key in (
        session_marker.DAEMON_AGENT_WRITES
        | session_marker.DAEMON_RUN_WRITES
        | session_marker.DAEMON_PROFILE_ALLOWED
        | session_marker.DAEMON_PROFILE_RUN_READS
        | session_marker.UNGATED_COMMANDS
        | session_marker.DIRECTED_ONLY
        | session_marker.READ_GROUP_WRITES
        | session_marker.READ_GROUP_REMOVALS
    ):
        node = command
        for word in key.split():
            node = getattr(node, "commands", {}).get(word)
            assert node is not None, key


def test_main_runs_a_refused_exec_without_recording(monkeypatch, capsys):
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    _set(session_marker.STATE_READ_ONLY)
    ran = []
    monkeypatch.setattr(cli_main.os, "execvp", lambda file, argv: ran.append(argv))
    cli_main.main(["exec", "--", "python", "train.py"])
    assert ran == [["python", "train.py"]]
    assert "opens no run" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# The daemon profile: the CLI refuses the same commands as the plugin hook, so
# a shell form that rebuilds the invocation (eval, $(echo probe), a renamed
# copy) cannot reach a team-records read/write/removal the hook would catch.
# ---------------------------------------------------------------------------


def _daemon_profile() -> None:
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    _set(session_marker.STATE_DAEMON)


@pytest.mark.parametrize("argv", [["run", "list"], ["series", "latest"], ["artifact", "list"],
                                  ["run", "delete", "r1"], ["run", "tag", "r1", "good"],
                                  ["notes", "push", "n.md"], ["logout"], ["token", "create"],
                                  ["context", "use", "other"], ["wizard", "--action", "recorder", "--yes"],
                                  ["outbox", "discard", "--held"], ["mcp", "headers"]])
def test_the_cli_refuses_what_the_daemon_profile_hook_refuses(argv):
    _daemon_profile()
    assert not session_marker.daemon_profile_allows(argv)[0], "fixture must be a hook-refused command"
    assert _refusal(argv) is not None


@pytest.mark.parametrize("argv", [["run", "get", "r1"], ["metrics", "wide", "r1"], ["get", "r1"],
                                  ["metrics", "plot", "r1"], ["run", "expect", "r1"],
                                  ["exec", "--", "python", "train.py"], ["run", "start"], ["ask", "x"],
                                  ["update", "--check"], ["service", "status"], ["doctor"],
                                  ["session", "initialize", "--session", SID, "--cwd", "."]])
def test_the_cli_still_runs_what_the_daemon_profile_allows(argv):
    _daemon_profile()
    assert _refusal(argv) is None


def test_the_daemon_worker_capture_starts_is_never_refused():
    """The tap's supervisor starts `probe daemon worker` with the session's own
    environment, which can name the agent's session. Refused by the profile,
    the live run's daemon session ran no worker in any sample. The hook still
    refuses an agent's own `probe daemon worker`."""
    _daemon_profile()
    argv = ["daemon", "worker", "--session-id", SID, "--transcript", "/w/t.jsonl", "--cwd", "/w",
            "--source", "claude_code"]
    assert _refusal(argv) is None
    assert not session_marker.daemon_profile_allows(argv)[0]


def test_a_daemon_profile_run_keeps_its_own_work():
    # Inside `probe exec` (PROBE_RUN_ID set) the run's own writes and reads still
    # pass in a daemon profile; a team-records write is still refused.
    _daemon_profile()
    inside = {**ENV, "PROBE_RUN_ID": "r1"}
    assert _refusal(["log", "--run", "r1", "acc=0.9"], env=inside) is None
    assert _refusal(["run", "end", "r1"], env=inside) is None
    assert _refusal(["notes", "push", "n.md"], env=inside) is not None


def test_the_cli_directs_a_daemon_profile_write():
    _daemon_profile()
    assert _refusal(["notes", "push", "n.md", "--directed"]) is None


def test_a_daemon_profile_write_the_researcher_asked_for_matches_the_hook_text():
    _daemon_profile()
    assert _refusal(["notes", "push", "n.md"]) == session_marker.daemon_profile_deny(
        ["notes", "push", "n.md"], "probe notes push")


def test_the_switch_and_mcp_calls_keep_their_own_cli_refusals(monkeypatch):
    # These have dedicated handlers (the switch message; the bridge). The profile
    # gate must not pre-empt them with the generic refusal.
    _daemon_profile()
    assert _refusal(["session", "state", "off"]) is None  # write_gate leaves the switch to its own handler
    assert _refusal(["mcp", "call", "echo"]) is None  # the bridge owns mcp call


def test_the_daemon_own_calls_are_never_gated_by_the_profile():
    # The daemon's `probe` runs carry PROBE_DAEMON_SESSION, no coding-agent var,
    # so `session_id_from_env` is unset and the gate never fires.
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    _set(session_marker.STATE_DAEMON)
    assert _refusal(["run", "list"], env={"PROBE_DAEMON_SESSION": SID}) is None


def test_an_inline_daemon_profile_session_reads_and_writes():
    session_marker.mark_session_profile(SID, session_marker.RECORDER_DAEMON)
    assert session_marker.switch_to_inline(SID)
    assert _refusal(["run", "list"]) is None
    assert _refusal(["notes", "push", "n.md"]) is None


@pytest.mark.parametrize(
    "argv",
    [
        ["workspace", "set", "main", "--best", "e1", "--reason", "beats the baseline"],
        ["workspace", "set", "main", "--best", ""],
        ["project", "set", "p", "--metric", "test/acc", "--goal", "max"],
        ["project", "set", "p", "--best", "e1", "--reason", "beats the baseline"],
        ["experiment", "set", "e1", "--metric", "test/acc", "--goal", "max"],
    ],
)
def test_a_metric_or_a_pick_is_a_write_in_every_state(argv):
    """`workspace set` is in a plumbing group, so it is named a write on its own
    (`PLUMBING_GROUP_WRITES`); the others ride their write groups."""
    assert session_marker.classify_probe_args(argv)[0] == "write"
    for state in (session_marker.STATE_OFF, session_marker.STATE_READ_ONLY):
        _set(state)
        assert _refusal(argv) is not None, state
    _set(session_marker.STATE_DAEMON)
    _lease()
    assert _refusal(argv) is not None
    assert _refusal([*argv, "--directed"]) is None
    assert session_marker.daemon_profile_allows([*argv, "--directed"])[0] is True
