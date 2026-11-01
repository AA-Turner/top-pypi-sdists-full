"""The daemon's own tools (D13): `shell`, `read` and `session`.

(The Probe MCP tools are loaded from the start beside them.) Thin by design:
judgment lives in the skills, checks live in plain code (`shell.classify`,
`precheck`). Each tool caps its own output: nothing is spilled to a file.

`shell(command, why)`:
    a `probe ...` command   -> the pre-checks (`precheck`), then the real CLI with
                               the daemon's key and an Idempotency-Key; the
                               commonest reads (`host_reads.MOVED`) run the CLI
                               command's own body in this process instead
    several commands with   -> run in order by the daemon itself (`_run_steps`):
    `probe` among them         each probe command as above, in the folder the
                               `cd` parts set, `&&` / `||` / `;` as bash, and
                               `probe X | F` feeding X's stdout to F; each other
                               part as the rows below
    a known-safe command    -> runs at once (`shell.run`, minimal environment)
    a note write            -> `cat > FILE <<'TAG'` into a checked-out note: its body
                               is secret-scanned; into the team note it is a question
                               (`team_note.edit`, with the diff) unless bypass mode
    anything else           -> a question for the researcher (`shell.unsafe_command`),
                               unless the session runs in bypass mode; outside
                               bypass, Jev is asked first (`command_check`), and
                               its yes runs it unasked

`read(path, offset, limit)`: a file, nothing run (`read_file`).
`session(op, ...)`: the chat log, the logbook, the state of the record; each op
takes only its own arguments (`SESSION_OPTIONS`).

EVERY tool call first asks `lease.may_write`: once the researcher moves the
switch, or the lease is released or taken, each tool answers the stop message
(`NO_LEASE`) and sets `Deps.stopped`, so the worker ends the bite without
marking its events covered. A command already running is watched the same way
(every `LEASE_POLL_S`) and its whole process group killed when the answer
changes. When Probe refuses the daemon's key (a 401, or a 403 naming the
credential: `KEY_REFUSED_LINE` from the CLI, `probe_api.KeyRefused` from the
daemon's own reads) the tool sets `Deps.key_refused` too, and the worker releases
the lease. A held
action the researcher says yes to later runs from the worker: it calls
`held_refusal(deps, req)` first (the lease again, `approvals.verify_held`, and
for the team note the document itself, re-read; for a shell command, the
scripts it runs, re-hashed).

A delete Probe cannot undo (`precheck.PERMANENT_DELETES`: no trash behind it) is
a question too (`delete.permanent`), unless the session runs in bypass mode.

THE TEAM-NOTE AUDIT (`Deps.audit`, daemon-team-note-audit; Richard 2026-10-11:
"dont ask for approval or anything") asks nothing, in any mode. It edits its own
copy of the note (its only write folder, `audit.draft_dir`), which the daemon
publishes when it ends; a `probe` command runs only when it reads; any other
command that is not on the safe list is refused (`AUDIT_REFUSED`), never held.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from probe.shared.mailbox import approvals as appr
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.store.store import Store
#: The tools that can write -- run a `probe` write, or a shell command that
#: changes files. Their calls run one at a time, in the order the model made
#: them; every other tool only reads, and may run beside the others.
WRITE_TOOLS: frozenset[str] = frozenset({"shell", "bash", "edit"})
#: The program a shell command runs under, as the logbook and the held question
#: record it (`shell.run`: `/bin/bash --noprofile --norc -c`). Rows written before
#: 2026-10-18 say `sh`; readers take both (`store.jev_approved`).
SHELL_ARGV0 = "bash"


def shell_argv(command: str) -> list[str]:
    return [SHELL_ARGV0, "-c", command]


SEARCH_LIMIT = 20
OPEN_PAGE_CHARS = 24_000
#: A persisted tool output larger than this is not read back.
MAX_SIDE_FILE_BYTES = 20 * 1024 * 1024


@dataclass
class Deps:
    """What a bite's tools need. Built once per bite by the worker."""

    store: Store
    board: appr.Board
    session_id: str
    cwd: Path
    workdirs: list[Path]
    home: Path
    write_dirs: list[Path]
    probe_env: dict[str, str]  # PROBE_TOKEN, PROBE_BASE_URL, PROBE_DAEMON_SESSION, ...
    bypass: bool
    mode_known: bool
    bite_id: int | None = None
    blocks: dict[str, precheck.Block] = field(default_factory=dict)
    protected: list[Path] = field(default_factory=list)
    replay: Any = None  # the bench's hook: runs `probe` commands against a recorded Probe
    #: Set by the first tool call that found this process may no longer act for the
    #: session (`lease.may_write`'s reason). The worker then ends the bite WITHOUT
    #: marking its events covered: the next writer records them.
    stopped: str | None = None
    #: Probe refused the daemon's key (a 401, or a 403 naming the credential):
    #: `stopped` says so too, and the worker releases the lease as unauthorized.
    key_refused: bool = False
    #: Seeds the operation ids (each command's Idempotency-Key): with it, the same
    #: command in a retry of the same bite sends the same key, so a write that
    #: landed is replayed, not made twice. The worker sets "<session>:<first seq>";
    #: None: a fresh random id per command.
    op_seed: str | None = None
    #: Per argv sent in this bite: (digest of the files it sent, how many times
    #: that digest changed). `_op_id` reads and advances it.
    sent: dict[str, tuple[str, int]] = field(default_factory=dict)
    #: The daemon's READER (daemon reads): its tools never check or renew the
    #: writer's lease (the reader runs while the session is in daemon mode and
    #: reads are on), its `read` stays in the session's folders and the main
    #: agent's memory and instruction files even in bypass mode, and its lookups
    #: stay out of the writer's logbook.
    reader: bool = False
    #: The team-note AUDIT (daemon-team-note-audit): nothing it does is ever a
    #: question -- anything that would wait for a yes is refused (`AUDIT_REFUSED`).
    #: Its `write_dirs` is its draft folder alone (`audit.AuditLane._deps`).
    audit: bool = False
    #: Writes that failed or were not run (`_probe_command`, `_shell_command`,
    #: `_run_steps`). A write the researcher was asked about is not one: it waits
    #: for them (`asked`). The writer's shell tool compares this count before and
    #: after a call, so a run that ends in the same response as a write that did
    #: not land goes on (B2, `agent.lost_write_retry`).
    lost_writes: int = 0
    #: Questions put to the researcher that did not come back yes (`_hold`).
    asked: int = 0
    #: What this run owes is the session's owed ledger (`probe.shared.notes.owed`, notes
    #: parity N3: the CLI keeps it for the daemon and an inline agent alike) read
    #: from this `seq` on, the daemon's own items only: a summary for a project or
    #: experiment it created or an experiment it concluded (plan 3.5), a note for
    #: a run it tagged invalid. The writer's output validator sends the run back
    #: once for each kind (`agent.SUMMARY_OWED`, `agent.NOTE_OWED`).
    ledger_from: int = 0
    #: A summary command said the team's summaries are the lane's (mode lane, a
    #: 503): no summary is owed.
    summaries_off: bool = False
    #: The run was already sent back once for owed summaries, and for owed notes.
    summaries_owed_asked: bool = False
    notes_owed_asked: bool = False
    #: Experiments whose conclusion this run set (`kind:ref`), what the last
    #: `summary checkout` of each entity said about its tables and charts
    #: ({"eligible", "count"}), and the `visuals set` calls that landed: an
    #: eligible experiment concluded with none set owes them (plan 3.8).
    concluded: set[str] = field(default_factory=set)
    visuals_state: dict[str, dict] = field(default_factory=dict)
    visuals_landed: set[str] = field(default_factory=set)
    visuals_owed_asked: bool = False
    #: The tally above was read from the store (`SUMMARY_TALLY`): a run paused
    #: after ROUNDS_BEFORE_YIELD carries on in a new bite with new Deps.
    tally_loaded: bool = False
    #: The watched session's harness (`Worker.session.source`): the reader's MCP
    #: reads and its feedback name it.
    harness: str = ""
    #: Plain code's state of the record (`agent.RunState.status`), for `probe
    #: daemon session status`; None where there is none (the reader, the audit).
    record_status: Callable[[], str] | None = None
    #: A daemon TASK (`probe daemon task`, `agent.run_task`): the child agent a
    #: writer, reader or audit started for one long read. Its `bash` runs only
    #: what `reads_only` proves reads (`agent.build_task_agent`), it starts no
    #: task of its own, and its lookups stay out of the logbook (the task itself
    #: is one line there).
    task: bool = False
    #: Runs `probe daemon task <text>` for the agent whose bash call this is
    #: (`agent.run_task`, bound to its model, usage and run); None: no task runs
    #: here (a task's own deps, a command run outside an agent).
    task_runner: Callable[[str], Any] | None = None


def _hold(deps: Deps, *, policy: str, facts: dict, held: dict) -> appr.Request:
    """Ask the researcher (`Board.hold`). A question that did not come back yes
    (waiting, or a no given before) is counted in `Deps.asked`: the write behind
    it did not fail, it is theirs to decide."""
    req = deps.board.hold(policy=policy, session_id=deps.session_id, facts=facts, held=held, bypass=deps.bypass,
                          mode_known=deps.mode_known)
    if req.state != appr.APPROVED:
        deps.asked += 1
    return req


def task_deps(deps: Deps) -> Deps:
    """A task's own deps (`agent.run_task`): the agent's sessions, folders, store,
    board, key and mode, as that agent's (a reader's task reads as the reader),
    with nothing of its run's bookkeeping -- no blocks, op ids, counts or tallies
    -- and no task of its own to start."""
    from dataclasses import replace

    # `bypass` off: a task never runs what bypass mode would let through (a `cd`
    # outside the working folders, a filter off the safe list), whatever reads_only said.
    return replace(deps, task=True, task_runner=None, bypass=False, blocks={}, sent={}, stopped=None,
                   lost_writes=0, asked=0,
                   concluded=set(), visuals_state={}, visuals_landed=set(), summaries_owed_asked=True,
                   notes_owed_asked=True, visuals_owed_asked=True, tally_loaded=True)


def _logs_lookups(deps: Deps) -> bool:
    """The logbook is the writer's: neither the reader's lookups nor a task's
    (the task is one line of its own) go in it."""
    return not (deps.reader or deps.task)


def _already_no(req: appr.Request) -> str:
    return f"not run: the researcher already said no to this (question {req.id})."


def _cap(text: str, limit: int = 20_000) -> str:
    if len(text) <= limit:
        return text
    half = limit // 2
    return f"{text[:half]}\n[... {len(text) - limit:,} characters cut ...]\n{text[-half:]}"
