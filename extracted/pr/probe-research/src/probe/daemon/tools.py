"""The daemon's own tools (D13): `shell`, `read` and `session`.

(The Probe MCP tools are loaded from the start beside them.) Thin by design:
judgment lives in the skills, checks live in plain code (`shell.classify`,
`precheck`). Each tool caps its own output: nothing is spilled to a file.

`shell(command, why)`:
    a `probe ...` command   -> the pre-checks (`precheck`), then the real CLI with
                               the daemon's key and an Idempotency-Key
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

import asyncio
import difflib
import hashlib
import inspect
import json
import os
import re
import shlex
import sys
import time
import uuid
from dataclasses import dataclass, field
from probe._compat import StrEnum
from pathlib import Path
from typing import Any, Callable, Literal

from probe.daemon import approvals as appr
from probe.daemon import precheck
from probe.daemon import scope
from probe.daemon.events import Kind
from probe.daemon.store import CUT_SHORT, FAILED_WHILE_RUNNING, UNRECORDED_BITE, Store, scrub
from probe.sdk.key_refusal import KEY_REFUSED_LINE
from probe.sdk.write_outcome import was_queued
from probe.tap_core import secrets

PROBE_TIMEOUT_S = 180.0
#: One `probe` command, its retries and their waits included, never takes longer
#: than this: less than the lease's life (`lease.LEASE_TTL_SECONDS`, 240s), which
#: the worker renews between tool calls, not during one.
PROBE_TOTAL_S = 200.0
#: A retry is not started with less time than this left.
PROBE_MIN_ATTEMPT_S = 15.0
#: How often a running command re-reads `lease.may_write`.
LEASE_POLL_S = 1.0
_clock = time.monotonic
#: A `probe` command that failed IN TRANSPORT (no HTTP answer at all) is retried
#: with the SAME operation id, so the server's Idempotency-Key replays a write
#: that landed (R12) -- but only where that is true (`IDEMPOTENT_COMMANDS`).
PROBE_ATTEMPTS = 3
#: How the CLI reports a transport failure: `errors.TransportError` is raised as
#: "<METHOD> <path>: <cause>" (`sdk/transport.py`) and printed by `cli.main` as
#: `error: <that>`. Words like "timeout" or "502" anywhere else in the output
#: are not a signal: a command can print them and have written.
_TRANSPORT_FAILURE = re.compile(r"^error: (GET|HEAD|POST|PATCH|PUT|DELETE) /\S*: ", re.MULTILINE)
#: The commands whose every write goes through a route on the server's
#: Idempotency-Key allowlist (research-os `app/core/idempotency.py` ALLOWLIST on
#: main), checked against the routes this client sends them to: POST /v1/projects
#: (project create), POST and PATCH /v1/projects/{P}/experiments[/{E}]
#: (experiment create, set, move -- the server names them since light
#: experiments X21), POST /v1/projects/{P}/experiments/{E}/groups, PATCH
#: /v1/projects|runs|groups|papers|views/{id}, POST
#: /v1/artifacts/{id}/move, POST /v1/projects/{id}/papers|references, POST
#: /v1/edges, POST /v1/runs/{id}/views, sub-notes (an experiment's under
#: /v1/projects/{P}/experiments/{E}/sub-notes). NOT here, on purpose:
#: `artifact add` (presign / PUT / confirm), `notes push` and `notes sync` (their
#: merge answers are not replayed), every delete, `artifact version-add`,
#: `experiment freeze`, `version create`, `project code *`,
#: `run end` (it may send
#: more than the one allowlisted PATCH), and `notes append` / `notes edit`: their
#: entity routes are allowlisted, but each READS the note and sends a document
#: built on what it read, so a retry after a write that landed builds a different
#: body -- refused as a reused key, or, after a stale-version 409 shifted the key
#: count, appended twice. Their `--team` routes (`/v1/team-note/apply/*`) are not
#: on the allowlist at all, and the daemon may not pass `--team` anyway
#: (`precheck`). A write that failed mid-way is reported,
#: and the model checks what landed before it tries again. Any other write is
#: never retried: the CLI cannot say that nothing was written. `feedback send` is
#: the one exception to the route list: it keys its POST /v1/feedback in the BODY
#: with this key (`probe.feedback.send_asked`), and anywhere else it only holds a
#: question on the local board, which `probe.feedback.hold` never doubles.
IDEMPOTENT_COMMANDS = frozenset({
    "project create", "group create",
    "experiment create", "experiment set", "experiment move", "experiment fork",
    "project set", "project tag", "project move",
    "run set", "run tag", "run move", "group set",
    "artifact move", "paper add", "paper update", "paper tag",
    "project reference add", "edge add", "views create", "views rename", "views update",
    "notes create", "notes rename", "feedback send",
})
#: The tools that can write -- run a `probe` write, or a shell command that
#: changes files. Their calls run one at a time, in the order the model made
#: them; every other tool only reads, and may run beside the others.
WRITE_TOOLS: frozenset[str] = frozenset({"shell"})


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
    #: Summaries this run owes (plan 3.5, write-summary): a project or
    #: experiment it created, or an experiment whose conclusion it set, keyed
    #: `kind:ref` as typed (`summary_cli.landing`); `summaries_pushed` holds what
    #: `probe summary push` landed. The writer's output validator sends the run
    #: back once for the difference (`agent.SUMMARY_OWED`).
    summaries_owed: set[str] = field(default_factory=set)
    summaries_pushed: set[str] = field(default_factory=set)
    #: A summary command said the team's summaries are the lane's (mode lane, a
    #: 503): nothing is owed.
    summaries_off: bool = False
    #: The run was already sent back once for owed summaries.
    summaries_owed_asked: bool = False
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


def _hold(deps: Deps, *, policy: str, facts: dict, held: dict) -> appr.Request:
    """Ask the researcher (`Board.hold`). A question that did not come back yes
    (waiting, or a no given before) is counted in `Deps.asked`: the write behind
    it did not fail, it is theirs to decide."""
    req = deps.board.hold(policy=policy, session_id=deps.session_id, facts=facts, held=held, bypass=deps.bypass,
                          mode_known=deps.mode_known)
    if req.state != appr.APPROVED:
        deps.asked += 1
    return req


def _writes(argv: list[str]) -> bool:
    """Whether a `probe ...` command writes. One that cannot be parsed counts:
    it did not run, and nothing says it would only have read."""
    try:
        return precheck.parse(argv).owner != precheck.READ
    except precheck.ParseError:
        return True


def _classify(deps: Deps, command: str, cwd: Path, *, piped_input: bool = False) -> Any:
    """`shell.classify` with this session's folders, in `cwd`."""
    from probe.daemon import shell as sh

    return sh.classify(command, workdirs=deps.workdirs, home=deps.home, cwd=cwd, protected=deps.protected,
                       write_dirs=deps.write_dirs, piped_input=piped_input, hidden=_off_check(deps, cwd),
                       off_inside=_off_inside_check(deps))


def _config_checker(deps: Deps, cwd: Path) -> Any:
    """A `probe_config.Checker` as this session sees the `.probe.config` files
    (the ones above its launch folder the researcher set aside do not count)."""
    from probe.sdk import probe_config as pc
    from probe.sdk import session_marker

    _start, skip = pc.session_view(session_marker.sessions_dir(), deps.session_id)
    # `hash` is `off` to the daemon (C9).
    return pc.Checker(cwd=str(cwd), skip=skip, legacy=True, daemon=True)


def _off_check(deps: Deps, cwd: Path) -> Any:
    """For the shell's checks: is a path `off` (Probe never reads it)? When the
    check cannot be built, every path counts as `off` (fail closed)."""
    try:
        checker = _config_checker(deps, cwd)
    except Exception:  # noqa: BLE001
        return lambda path: True
    return lambda path: checker.check(path).hidden


#: `probe_config.off_inside` answers, per (session, folder): (when, answer).
_OFF_INSIDE: dict[tuple[str, str], tuple[float, bool]] = {}
_OFF_INSIDE_TTL_S = 5.0


def _off_inside_check(deps: Deps) -> Any:
    """For the shell's checks: does a folder hold an `off` path somewhere below?
    (A command reading the whole tree is then refused.) Reused for 30 s."""
    from probe.sdk import probe_config as pc
    from probe.sdk import session_marker

    def check(folder: str) -> bool:
        key = (deps.session_id, folder)
        now = time.monotonic()
        hit = _OFF_INSIDE.get(key)
        if hit is not None and now - hit[0] < _OFF_INSIDE_TTL_S:
            return hit[1]
        try:
            _start, skip = pc.session_view(session_marker.sessions_dir(), deps.session_id)
            answer = pc.off_inside(folder, skip=skip, legacy=True)
        except Exception:  # noqa: BLE001
            answer = True
        if len(_OFF_INSIDE) > 4096:
            _OFF_INSIDE.clear()
        _OFF_INSIDE[key] = (now, answer)
        return answer

    return check


def _off_scrubbed(deps: Deps, text: str, cwd: Path) -> str:
    """A shell output minus the lines that show an `off` file (a backstop: a
    command reading a tree that holds one is refused before it runs)."""
    try:
        from probe.daemon import exclusions as ex

        return ex.scrub_listing(text, _config_checker(deps, cwd))[0]
    except Exception:  # noqa: BLE001 - fail closed
        return "[output removed: it could not be checked against .probe.config]"


def _op_id(deps: Deps, argv: list[str], content: str = "", *, family: str | None = None) -> str:
    """The operation id of a write: derived from `Deps.op_seed` when set, else random.

    `content` is the digest of the files the command sends (`_sent_digest`). The
    server answers a key it has seen with a DIFFERENT body with 422, so a second
    `notes push` of one note with new text needs its own key: the digest is part
    of it. So is how often the command changed within its `family` in this bite
    (default: the same words), or sending A, then B, then A again would reuse A's
    key and be answered with A's stored receipt while the server keeps B -- for a
    push of new text, and for `run set --status running`, `finished`, `running`
    alike (`_family`). The same command sent again with nothing between keeps its
    key (a write that landed is replayed, and a duplicate create is not made
    twice), and a retried bite that sends the same things in the same order sends
    the same keys."""
    if deps.op_seed is None:
        return uuid.uuid4().hex
    words = json.dumps(list(argv))
    group = family or words
    fingerprint = f"{words}\0{content}"
    last = deps.sent.get(group)
    changes = 0 if last is None else last[1] + (last[0] != fingerprint)
    deps.sent[group] = (fingerprint, changes)
    material = f"{deps.op_seed}:{words}:{content}:{changes}"
    return hashlib.sha256(material.encode()).hexdigest()[:32]


def _family(parsed: precheck.Parsed) -> str | None:
    """The writes one key-change counter spans (`_op_id`): every write of one
    command path, so A, B, A of `run set` gives the third its own key; a create
    only with itself, so the same create twice is made once."""
    return None if parsed.path.endswith((" create", " add")) else parsed.path


def _file_digest(path: Path) -> str:
    """sha256 of a file's bytes; its size and mtime when it is bigger than the
    pre-check scans (hashing gigabytes would stall the bite); "missing" when it
    cannot be read."""
    try:
        stat = path.stat()
        if not path.is_file():
            return "missing"
        if stat.st_size > precheck.SCAN_BYTES:
            return f"size:{stat.st_size}:mtime:{stat.st_mtime_ns}"
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return "missing"


def _sent_digest(deps: Deps, parsed: precheck.Parsed, cwd: Path) -> str:
    """One digest of every local file the command sends (`precheck.files_sent`,
    and the document `notes push` / `notes sync` upload), for its operation id.
    "" when it sends none."""
    paths = precheck.files_sent(parsed, cwd)
    document = _document_path(deps, parsed)
    if document is not None:
        paths.append(document)
    if not paths:
        return ""
    digest = hashlib.sha256()
    for path in paths:
        digest.update(f"{path}\0{_file_digest(path)}\n".encode())
    return digest.hexdigest()


def _mark_key_refused(deps: Deps) -> None:
    deps.key_refused = True
    deps.stopped = "Probe refused the daemon's key"


@dataclass
class ProbeResult:
    code: int | None  # None: killed at PROBE_TIMEOUT_S
    stdout: str
    stderr: str = ""

    @property
    def output(self) -> str:
        """What the model reads: stdout, then stderr."""
        if not self.stderr:
            return self.stdout
        glue = "\n" if self.stdout and not self.stdout.endswith("\n") else ""
        return f"{self.stdout}{glue}{self.stderr}"


def probe_executable() -> list[str]:
    """The `probe` of THIS environment (the CLI env the daemon runs in)."""
    beside = Path(sys.executable).with_name("probe")
    if beside.exists():
        return [str(beside)]
    return [sys.executable, "-m", "probe.cli"]


async def _run_probe(deps: Deps, argv: list[str], op_id: str) -> tuple[int | None, str, str]:
    """`(exit code, stdout then stderr, stderr)`: the worker's door for a held
    command (stderr alone for `write_status`)."""
    result = await run_probe_process(deps, argv, op_id)
    return result.code, result.output, result.stderr


async def run_probe_process(deps: Deps, argv: list[str], op_id: str, *, cwd: Path | None = None) -> ProbeResult:
    """Run the real CLI with the daemon's key, stdout and stderr kept apart (the
    JSON a command prints is on stdout alone), in `cwd` (default: the session's
    folder; a compound command's `cd` moves it). Retried only after a transport
    failure, and a write only when a retry cannot make it twice (`_may_retry`),
    all within `PROBE_TOTAL_S`.

    Before every attempt, and every `LEASE_POLL_S` while one runs, this process
    must still hold the session (`write_refusal`); when it no longer does, the
    command's process group is killed. A cancelled caller (the session's end
    cut the bite short) kills and reaps it too before the cancellation goes on.
    Probe refusing the key sets `deps.key_refused` and `deps.stopped`."""
    if deps.replay is not None:
        code, output = await deps.replay.run(argv, op_id)
        return ProbeResult(code, output)
    env = {**_base_env(), **deps.probe_env, "PROBE_IDEMPOTENCY_KEY": op_id, "PROBE_ASYNC": "0",
           "NO_COLOR": "1", "COLUMNS": "200"}
    deadline = _clock() + PROBE_TOTAL_S
    result: ProbeResult | None = None
    for attempt in range(PROBE_ATTEMPTS):
        if write_refusal(deps) is not None:
            if result is None:
                return ProbeResult(None, "", f"not run: {deps.stopped}")
            return ProbeResult(result.code, result.stdout,
                               f"{result.stderr.rstrip()}\nnot run again: {deps.stopped}".lstrip("\n"))
        result = await _attempt(deps, argv, env, min(PROBE_TIMEOUT_S, deadline - _clock()), cwd or deps.cwd)
        if _key_refused(result):
            _mark_key_refused(deps)
            break
        wait = 2 * (attempt + 1)
        if (not _may_retry(result, argv) or attempt + 1 == PROBE_ATTEMPTS
                or deadline - _clock() < wait + PROBE_MIN_ATTEMPT_S):
            break
        await asyncio.sleep(wait)
    assert result is not None
    return result


async def _attempt(deps: Deps, argv: list[str], env: dict[str, str], timeout: float, cwd: Path) -> ProbeResult:
    from probe.daemon.shell import stop_group

    proc = await asyncio.create_subprocess_exec(
        *probe_executable(), *argv, cwd=str(cwd), env=env, stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, start_new_session=True)
    reader = asyncio.ensure_future(proc.communicate())
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    try:
        while True:
            left = deadline - loop.time()
            if left <= 0:
                await stop_group(proc, reader)
                return ProbeResult(None, "", f"stopped after {timeout:.0f}s")
            done, _ = await asyncio.wait({reader}, timeout=min(LEASE_POLL_S, left))
            if done:
                out, err = reader.result()
                return ProbeResult(proc.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace"))
            if write_refusal(deps) is not None:
                await stop_group(proc, reader)
                return ProbeResult(None, "", f"stopped while it ran ({deps.stopped}) - it may have written part "
                                             "of its work")
    except BaseException:
        await stop_group(proc, reader)
        raise


async def _probe_process(deps: Deps, argv: list[str], op_id: str, cwd: Path) -> ProbeResult:
    """`run_probe_process` in `cwd`, named only when it is not the session's
    folder (so a stand-in with the plain signature still fits)."""
    if cwd == deps.cwd:
        return await run_probe_process(deps, argv, op_id)
    return await run_probe_process(deps, argv, op_id, cwd=cwd)


def write_status(code: int | None, stderr: str) -> str:
    """The logbook status of a probe write that ran: `failed` (not exit 0),
    `queued` (exit 0, but the CLI said on STDERR that a write is waiting in the
    outbox: Probe did not answer, so it is not on the record yet --
    `sdk/write_outcome.py`), else `ran`. Only `ran` is listed as recorded.
    stderr only: stdout is what the command printed of the record, which can
    quote anything (a note body, a reason)."""
    if code != 0:
        return "failed"
    return "queued" if was_queued(stderr) else "ran"


def _key_refused(result: ProbeResult) -> bool:
    """The CLI's own line for a credential Probe refused (`probe.cli.main`)."""
    return result.code == 1 and KEY_REFUSED_LINE in result.stderr.splitlines()


def _may_retry(result: ProbeResult, argv: list[str]) -> bool:
    """A transport failure (or a command we had to stop) of a read or of an
    `IDEMPOTENT_COMMANDS` write. Never any other write: a failed GET says nothing
    about the writes the command may have made before it."""
    if result.code == 0:
        return False
    failed = _TRANSPORT_FAILURE.findall(result.stderr) if result.code == 1 else []
    if result.code is not None and not failed:
        return False  # the server answered (or the command failed on its own): not a transport failure
    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError:
        return False
    return parsed.owner == precheck.READ or parsed.path in IDEMPOTENT_COMMANDS


NO_LEASE = "not run: this daemon no longer records this session"
#: What the team-note audit is told for a command that would need the researcher's
#: yes: the audit asks nothing (Richard 2026-10-11), so it does not run.
AUDIT_REFUSED = "not run: the team-note audit asks the researcher nothing, so a command that needs their yes does not run"
#: The team-note audit runs only `probe` reads: the daemon pulls the note before the
#: run and publishes the audit's copy after it (`audit.AuditLane`), under the
#: researcher's own credential -- a `notes sync` under the daemon's key would park
#: the researcher's note as another credential's (`team_note_file.paths`).
AUDIT_SYNC_IS_THE_DAEMONS = ("`probe notes sync` is the daemon's: it pulled the note into your copy and "
                             "publishes your copy when you end with final_result")


#: `probe` commands that read the open web, refused to the team-note audit as
#: their MCP tools are (`agent.AUDIT_REFUSED_TOOLS`): `paper find` is
#: `find_papers` from the shell, and text anyone can author must not reach an
#: audit that publishes into every teammate's instructions.
AUDIT_WEB_COMMANDS = frozenset({"paper find"})


def audit_probe_refusal(parsed: "precheck.Parsed") -> str | None:
    """None when the team-note audit may run this `probe` command; else why not."""
    if parsed.path in AUDIT_WEB_COMMANDS:
        from probe.daemon.agent import AUDIT_WEB_REFUSED  # agent imports this module

        return AUDIT_WEB_REFUSED
    if parsed.owner == precheck.READ:
        return None
    if parsed.path == "notes sync":
        return f"not run: {AUDIT_SYNC_IS_THE_DAEMONS}."
    return f"{AUDIT_REFUSED} (`probe {parsed.path}` writes; the audit reads Probe only)."
#: Opens the logbook reason of an `edge remove` run without a question because
#: Probe says this researcher's daemon made the link (`_own_link`, lineage L9).
OWN_LINK_REASON = "own link (L9): "


def write_refusal(deps: Deps) -> str | None:
    """None while this process may act for the session; else the stop message
    every tool returns (A2, R11). Read fresh from disk on each call, never renewed
    here. The replay bench has no lease. Once Probe refused the daemon's key,
    every call stops."""
    if deps.reader:
        return None
    if deps.key_refused:
        reason = deps.stopped or "Probe refused the daemon's key"
    elif deps.replay is not None:
        return None
    else:
        from probe.daemon import lease

        reason = lease.may_write(deps.session_id)
        if reason is None:
            return None
    deps.stopped = reason
    return f"{NO_LEASE} ({reason}). Nothing is lost: whoever records next reads the chat log."


def held_refusal(deps: Deps, req: appr.Request) -> str | None:
    """What the worker checks right before it runs an action the researcher said
    yes to (G7, C1): this process may still act for the session, the held action
    is still the one they were asked about, and for the team note, the change it
    makes is still the one they were shown (the document re-read, G6). None: run it."""
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    if not appr.verify_held(req):
        return f"not run: request {req.id} no longer matches what the researcher was asked - nothing was done."
    if req.policy == "team_note.edit":
        return _team_note_refusal(deps, req)
    if req.policy == "shell.unsafe_command":
        return _script_refusal(deps, req)
    return None


def _script_refusal(deps: Deps, req: appr.Request) -> str | None:
    """A held shell command runs files its words do not show: they must still be
    the files, with the text, the researcher was shown (hashed when asked)."""
    command, cwd = str(req.held.get("command") or ""), Path(req.held.get("cwd") or deps.cwd)
    now = _script_facts(deps, command, cwd)
    if isinstance(now, str):
        return f"{now.rstrip('.')} (request {req.id}); nothing was done"
    shown = [(s.get("path"), s.get("sha256")) for s in (req.facts or {}).get("scripts") or []]
    if [(s["path"], s["sha256"]) for s in now] != shown:
        return (f"not run: a script request {req.id} runs changed after the researcher was asked - nothing was "
                "done.")
    return None


#: A script that is not text, or bigger than this, is never asked about: the
#: question could not show it whole.
SCRIPT_BYTES = 4 * appr.SCRIPT_CHARS
_WRITES_NOTES_TAIL = " The daemon never runs what it can write."


def _script_facts(deps: Deps, command: str, cwd: Path) -> list[dict] | str:
    """What a held shell command runs besides its own words (`shell.held_scripts`):
    `[{"path", "sha256", "text"}]`, `sha256` None for a file that does not exist
    (yet). A refusal, as the tool's answer, when it runs a file in the notes
    folders, cannot be read, or runs a script the question could not show whole."""
    from probe.daemon import shell as sh

    inside = sh.names_writable(command, cwd=cwd, home=deps.home, folders=deps.write_dirs)
    if inside is not None:
        return f"not run: the command names {inside}, in the folders the daemon writes notes into.{_WRITES_NOTES_TAIL}"
    found = sh.held_scripts(command, cwd=cwd, home=deps.home)
    if found is None:
        return "not run: the daemon could not read which files the command runs (its quoting)."
    out: list[dict] = []
    total = 0
    for path in found:
        entry: dict = {"path": path, "sha256": None}
        if os.path.isfile(path):
            try:
                with open(path, "rb") as handle:
                    data = handle.read(SCRIPT_BYTES + 1)
            except OSError:
                return (f"not run: the command runs {path}, which the daemon can't show the researcher whole (it "
                        "can't be read).")
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = "\0"
            total += len(text)
            if len(data) > SCRIPT_BYTES or "\0" in text or total > appr.SCRIPT_CHARS:
                return (f"not run: the command runs {path}, which the daemon can't show the researcher whole (it "
                        f"isn't text, or is longer than the {appr.SCRIPT_CHARS} characters a question shows).")
            if scrub(text) != text:
                return (f"not run: the command runs {path}, which the daemon can't show the researcher whole (it "
                        "looks like it contains a credential).")
            entry.update(sha256=hashlib.sha256(data).hexdigest(), text=text)
        out.append(entry)
    return out


def _team_note_refusal(deps: Deps, req: appr.Request) -> str | None:
    """Recompute what the held team-note change does NOW: the same text, from the
    same document, and still no credential in it. Anything else: refused, so the
    worker voids the yes."""
    changed = f"not run: the team note changed after the researcher was asked (request {req.id}) - nothing was done."
    held, facts = req.held or {}, req.facts or {}
    if held.get("kind") == "shell":
        verdict = _classify(deps, str(held.get("command") or ""), Path(held.get("cwd") or deps.cwd))
        if not (verdict.safe and verdict.note_target and _in_team_note(verdict.note_target)):
            return f"not run: request {req.id} is no longer a team note change - nothing was done."
        now, text = _team_note_write_facts(verdict), verdict.note_body or ""
    elif held.get("kind") == "probe":
        now = _team_note_sync_facts(deps)
        if now is None:
            return changed
        text = _read(_team_note_paths(deps)[0]) or ""
    else:
        return f"not run: request {req.id} is no longer a team note change - nothing was done."
    if any(now.get(k) != facts.get(k) for k in ("path", "text_sha", "before_sha", "diff")):
        return changed
    found = secrets.scan(text)
    if found:
        return (f"not run: the team note change of request {req.id} now looks like it contains a credential "
                f"({found[0].rule}) - nothing was done.")
    return None


def _base_env() -> dict[str, str]:
    keep = ("PATH", "HOME", "LANG", "LC_ALL", "XDG_STATE_HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
            "PROBE_CONFIG_PATH", "PROBE_CONTEXT", "TMPDIR")
    return {k: os.environ[k] for k in keep if k in os.environ}


def _already_no(req: appr.Request) -> str:
    return f"not run: the researcher already said no to this (question {req.id})."


def _cap(text: str, limit: int = 20_000) -> str:
    if len(text) <= limit:
        return text
    half = limit // 2
    return f"{text[:half]}\n[... {len(text) - limit:,} characters cut ...]\n{text[-half:]}"


# ---------------------------------------------------------------------------
# shell
# ---------------------------------------------------------------------------


async def shell(deps: Deps, command: str, why: str = "") -> str:
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    command = command.strip()
    if not command:
        return "empty command"
    verdict = _classify(deps, command, deps.cwd)
    if verdict.probe_argv is not None:
        return await run_probe_command(deps, verdict.probe_argv, why=why)
    if verdict.steps is not None:
        return await _run_steps(deps, verdict.steps, why)
    auto = deps.bypass and deps.mode_known  # bypass mode: nothing is asked, so nothing is hidden
    if verdict.safe and verdict.note_target:
        found = secrets.scan(verdict.note_body or "")
        if found and not auto:
            deps.lost_writes += 1
            return (f"not run: the note text looks like it contains a credential ({found[0].rule}). A note is "
                    "uploaded to Probe.")
        if _in_team_note(verdict.note_target):
            return await _hold_team_note_write(deps, command, verdict, why)
    text, _ = await _shell_command(deps, command, verdict, why, deps.cwd)
    return text


async def _shell_command(deps: Deps, command: str, verdict: Any, why: str, cwd: Path, *,
                         stdin: bytes | None = None) -> tuple[str, int | None]:
    """One shell command that is not a `probe` command, classified (`verdict`)
    for `cwd`: run at once when safe, else refused, asked about, or (bypass mode)
    run. `(what the model reads, its exit code; None when it did not run to an
    end)`. `stdin`: the output of the probe command it is piped from. A write
    (a note file, or anything off the safe list) that failed or was not run, and
    was not asked about, counts in `Deps.lost_writes`."""
    asked = deps.asked
    text, code = await _checked_shell_command(deps, command, verdict, why, cwd, stdin=stdin)
    if (code != 0 and deps.asked == asked and deps.stopped is None and (verdict.note_target or not verdict.safe)
            and not text.endswith(_SKILLS_ARE_READ)):  # a skill read pointed at the read tool wrote nothing
        deps.lost_writes += 1
    return text, code


async def _checked_shell_command(deps: Deps, command: str, verdict: Any, why: str, cwd: Path, *,
                                 stdin: bytes | None = None) -> tuple[str, int | None]:
    from probe.daemon import shell as sh

    if verdict.refused:  # never a question, not even in bypass mode (`shell._Never`)
        deps.store.log_write(bite=deps.bite_id, op_id=_op_id(deps, ["sh", "-c", command]),
                             argv=["sh", "-c", scrub(command)], head="shell", status="not_run",
                             reason=verdict.reason)
        return f"not run: {verdict.reason} This is refused in every mode.", None
    if deps.audit and not verdict.safe:
        return f"{AUDIT_REFUSED} ({scrub(verdict.reason).rstrip('.')}).", None
    auto = deps.bypass and deps.mode_known  # bypass mode: nothing is asked, so nothing is hidden
    if verdict.fixable and not auto:  # one flag from safe (`shell._Fix`): the daemon adds it, nobody is asked
        return f"not run: {verdict.reason}", None
    if verdict.safe:
        result = await sh.run(command, cwd=cwd, watch=lease_watch(deps), stdin=stdin)
        output = _off_scrubbed(deps, result.output, cwd)
        deps.store.log_lookup(bite=deps.bite_id, tool="shell", query=command, result=output[:2000])
        text = scrub(output)
        return f"[{_shell_status(result)}{' · output cut' if result.truncated else ''}]\n{text}", result.exit_code
    if scrub(command) != command and not auto:
        # C1: the question would have to hide part of the command, and a yes runs
        # all of it. A redaction can swallow more than the secret (a chained
        # command after `password=...`), so nothing that needs hiding is asked.
        return "not run: the command contains what looks like a credential.", None
    if len(command) > appr.COMMAND_CHARS and not auto:
        # G3: a question shows the whole command or none of it; a yes runs all of it.
        # The check's own reason comes FIRST: it is what the daemon can change. Said
        # alone, "too long to ask" sent it shortening a note write whose shape was
        # the problem (`... EOF` then `probe notes push` in one command), until the
        # loop detector cut the bite short (2026-10-03: 89 refusals in 30 days).
        hint = ""
        if "<<" not in command and sh.names_writable(command, cwd=cwd, home=deps.home, folders=deps.write_dirs):
            hint = f" {sh.R_HEREDOC}"  # a note write in another shape: name the one that runs
        return (f"not run: {scrub(verdict.reason)}{hint} It can't be asked about either: the command is "
                f"{len(command)} characters, and a question shows the researcher at most {appr.COMMAND_CHARS}."), None
    if stdin is not None and not auto:
        # A yes runs later, from the worker: the probe output it would read is gone by then.
        return (f"not run: `{command}` is not on the safe list ({verdict.reason}), and a question can't carry the "
                "probe command's output to it."), None
    facts = {"command": command, "cwd": str(cwd), "why_asking": verdict.reason, "reason": why}
    if not auto:
        # R3-2: a yes binds the command's words; a script it runs is bound by its text.
        scripts = _script_facts(deps, command, cwd)
        if isinstance(scripts, str):
            if scripts.endswith(_WRITES_NOTES_TAIL):
                # A write into the notes folders in any other shape (`sed -i`, `>`, an
                # unquoted heredoc): say the one shape that runs, not only why this didn't.
                return f"not run: {verdict.reason}" if "<<" in command else f"{scripts} {sh.R_HEREDOC}", None
            return scripts, None
        if scripts:
            facts["scripts"] = scripts
        if _names_a_skill_folder(command):
            # The skills are the daemon's own, a `read` away. Guessed at in the agent's
            # install folders (`cat ~/.pi/agent/git/.../track-work/reference.md`,
            # `ls ~/.agents/skills/track-work`), they were outside the working folders and
            # each guess was a question for the researcher (14 in 14 days). Refused, not
            # asked: the read tool reads them without anyone's yes. After the notes-write
            # checks above, so a note write keeps the hint that names the shape that runs.
            return f"not run: {verdict.reason.rstrip('.')}. {_SKILLS_ARE_READ}", None
    held = {"kind": "shell", "command": command, "cwd": str(cwd), "op_id": _op_id(deps, ["sh", "-c", command])}
    # JEV BEFORE THE RESEARCHER (F8, `command_check`): in every mode but bypass,
    # a command the safe list did not clear is put to Jev first; only its yes
    # runs it unasked. Anything else falls through to the question below.
    if not auto:
        approved = await _jev_approval(deps, command, verdict, cwd, facts, held)
        if approved is not None:
            stop = write_refusal(deps)  # the check took a moment: still this process's session?
            if stop is not None:
                return stop, None
            result = await _run_shell_write(deps, command, held["op_id"], head="shell", request=None, cwd=cwd,
                                            stdin=stdin, reason=approved)
            return (f"[{approved} · {_shell_status(result)}]\n{scrub(_off_scrubbed(deps, result.output, cwd))}",
                    result.exit_code)
    req = _hold(deps, policy="shell.unsafe_command", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        result = await _run_shell_write(deps, command, held["op_id"], head="shell", request=req.id, cwd=cwd,
                                        stdin=stdin)
        return (f"[{appr.AUTO} · {_shell_status(result)}]\n{scrub(_off_scrubbed(deps, result.output, cwd))}",
                result.exit_code)
    deps.store.log_write(bite=deps.bite_id, op_id=held["op_id"], argv=["sh", "-c", command], head="shell",
                         status="held", reason=verdict.reason, request=req.id)
    return (f"held for the researcher (request {req.id}) - {verdict.reason.rstrip('.')}. It runs if they say yes - "
            "the answer shows up in a later bite."), None


#: How a shell guess at the skills' folders is answered (`_names_a_skill_folder`):
#: a read pointed at the read tool, never a write that was lost (`_shell_command`).
_SKILLS_ARE_READ = ("The skills are read with the read tool, by their path in the skills folder: "
                    "`read track-work/reference.md`.")


def _names_a_skill_folder(command: str) -> bool:
    """Whether a path in `command` runs through one of the shared skills' folders
    (`bite.SHARED_SKILLS`): a word with a `/` that has the skill's name as a whole
    part, glob stars aside (`~/.pi/agent/git/x/skills/track-work/reference.md`,
    `'*track-work/reference.md'`, `skills/edit-notes`). Never a bare word (`grep -rn
    track-work`), a `rev:path` or `host:path` word (`git show
    main:agent/skills/track-work/SKILL.md`), `my-track-work.md`, or a heredoc's text."""
    from probe.daemon.bite import SHARED_SKILLS

    if "<<" in command:
        return False
    try:
        words = shlex.split(command)
    except ValueError:
        words = command.split()
    for word in words:
        parts = word.split("/")
        if len(parts) > 1 and ":" not in parts[0] and any(part.strip("*?") in SHARED_SKILLS for part in parts):
            return True
    return False


def _names_policy_path(deps: Deps, command: str, cwd: Path) -> str | None:
    """A word of `command` naming a path a policy question guards, else None:
    the notes folders the daemon writes (`write_dirs`), the team note
    (`team_note.edit`; its folder, as `_in_team_note` reads it), Probe's whole
    state folder (`~/.local/state/probe`: the sessions' mode files, the
    approvals board, the daemon's own state) and Probe's config (`protected`).
    Read as broadly as `shell.names_writable` reads the notes folders."""
    from probe.daemon import shell as sh
    from probe.daemon.folders import _state_base, note_dirs

    guarded = [*deps.write_dirs, note_dirs()[-1], _state_base(), *deps.protected]
    return sh.names_writable(command, cwd=cwd, home=deps.home, folders=guarded)


#: WHAT JEV MAY JUDGE: `python -c CODE`, alone or after plain `cd DIR`s, and
#: nothing else. Four review rounds of a list of "read-only" programs each found
#: a new way a listed program writes, runs a helper through PATH or reads names
#: its words don't show (`file -z` runs a decompressor, `diff -l` runs `pr`,
#: `gzip -Sc` deletes, `unzip --p` cancels `-p`, `xxd a b` writes, `pip show
#: --log` writes, `sha256sum -c` reads a list, `printf %n` sets PATH, `ps e`
#: prints other environments): the safe list's own per-program rules are where
#: those belong, and reads now run there anywhere. Inline Python is the gray
#: zone left: its whole code is in the command's text, which is what Jev reads.

#: The only Python options a judged `python -c` may carry: none turns the
#: daemon shell's PYTHONSAFEPATH or PYTHONDONTWRITEBYTECODE off (`-E`, `-I`
#: and `-X` would; `-m` and a file run code its words don't show).
_PYTHON_FLAGS = frozenset({"-P", "-B", "-s", "-S", "-u", "-q", "-O", "-OO", "-b", "-bb"})
_PYTHON_NAME = re.compile(r"python(3(\.\d+)?)?")
_PYTHON_REAL = re.compile(r"python(\d+)\.(\d+)")


def _parts(command: str) -> list[list[str]] | None:
    """The simple commands of `command` as the checker's own strict reading
    splits them (`shell._split`), their words unquoted; None when that reading
    refuses it: `$`, backticks, globs and braces expand to what the text
    doesn't show (`X=curl; $X`, `head -c 20 *`). Not the lenient reading the
    scans use: it takes a quoted `'>'` for a redirect and merges the command
    after it (`echo '>'; uv run x.py`) into echo's words."""
    from probe.daemon import shell as sh

    try:
        parts = sh._split(sh._tokenize(command))
    except sh._Refuse:
        return None
    if any(part.redirects for part in parts):
        return None  # a redirect writes or reads what the words don't name; a heredoc runs bash on its body
    return [[w.value for w in part.words] for part in parts]


def _never_judged(deps: Deps, command: str, cwd: Path) -> bool:
    """A command Jev is never asked about: anything but `python -c CODE` on a
    Python 3.11+ (`_python_judgeable`: its options from `_PYTHON_FLAGS`, named
    bare, found on the shell's PATH outside the working folders, no `X=1`
    before it), alone or after plain `cd DIR`s, read by the checker's strict
    reading (`_parts`: no `$`, backticks, globs or braces). And never while the
    shell's PATH holds a folder of the session (a repo's `.venv/bin`)."""
    parts = _parts(command)
    if not parts or _path_reaches_the_session(deps, cwd):
        return True
    judged = False
    for words in parts:
        if not words:
            continue
        name = words[0]
        if name == "cd" and len(words) == 2 and not words[1].startswith("-"):
            continue
        if not _PYTHON_NAME.fullmatch(name) or _program(deps, name, cwd) is None:
            return True
        if not _python_judgeable(deps, name, words[1:], cwd):
            return True
        judged = True
    return not judged


def _roots(deps: Deps, cwd: Path) -> list[str]:
    return [os.path.realpath(r) for r in (*deps.workdirs, cwd)]


def _inside_roots(real: str, roots: list[str]) -> bool:
    return any(real == r or real.startswith(r.rstrip(os.sep) + os.sep) for r in roots)


def _path_reaches_the_session(deps: Deps, cwd: Path) -> bool:
    """Does the daemon shell's PATH hold a folder inside a working folder or
    the session's folder (a repo's `.venv/bin`, `node_modules/.bin`)?"""
    from probe.daemon import shell as sh

    roots = _roots(deps, cwd)
    return any(entry and _inside_roots(os.path.realpath(entry), roots)
               for entry in sh.minimal_env()["PATH"].split(os.pathsep))


def _program(deps: Deps, name: str, cwd: Path) -> str | None:
    """The real file `name` runs, found on the daemon shell's PATH; None when
    there is none, or it lies inside a working folder or the session's folder
    (a repo's own `cut`). Nothing is run to find it."""
    import shutil

    from probe.daemon import shell as sh

    found = shutil.which(name, path=sh.minimal_env()["PATH"])
    if not found:
        return None
    real = os.path.realpath(found)
    return None if _inside_roots(real, _roots(deps, cwd)) else real


def _python_judgeable(deps: Deps, name: str, args: list[str], cwd: Path) -> bool:
    """`python -c CODE` only: every option before `-c` from `_PYTHON_FLAGS`, and
    the real interpreter a Python 3.11+ (one that honours PYTHONSAFEPATH, which
    `shell.minimal_env` sets), read from its real file's name
    (`/usr/bin/python3` -> `python3.12`). Nothing is run to find out: a probe
    that ran it would run whatever PATH names. A name without a version (a
    pyenv shim) is no.

    RESIDUAL, not closed: Python runs `site`'s startup hooks (a `.pth` file or
    `sitecustomize`/`usercustomize` in a site-packages folder) before the code.
    Planting one is a write, and the daemon makes none unasked; whoever could
    plant one (the coding agent, the researcher) can run code directly."""
    k = 0
    while k < len(args) and args[k] in _PYTHON_FLAGS:
        k += 1
    if k >= len(args) - 1 or args[k] != "-c":
        return False
    real = _program(deps, name, cwd)
    m = _PYTHON_REAL.fullmatch(os.path.basename(real or ""))
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= (3, 11)


def _programs(deps: Deps, command: str, cwd: Path) -> list[tuple] | None:  # None: not bindable
    """What Jev's yes is bound to (G3): each program the command's parts run,
    as its real file and that file's identity (device, inode, size, change
    time). A link pointed elsewhere, a file replaced by rename, or one written
    in place (its change time moves, which no one can set back) while Jev
    answers is a different command."""
    out: list[tuple] = []
    for words in _parts(command) or []:
        if not words or words[0] == "cd":
            continue
        real = _program(deps, words[0], cwd)
        try:
            st = os.stat(real) if real else None
        except OSError:
            st = None
        if st is None:
            return None  # no identity to bind a yes to: never judged
        out.append((real, (st.st_dev, st.st_ino, st.st_size, st.st_ctime_ns)))
    return out


def _judgeable(deps: Deps, command: str, verdict: Any, cwd: Path) -> bool:
    """May Jev be asked about this held command at all? Not when it names a
    credential-shaped file (`Verdict.credential`), a hidden file or folder or a
    whole tree's contents (`Verdict.private`), a policy path, or runs what
    `_never_judged` names."""
    from probe.daemon import shell as sh

    parts = _parts(command)
    names = sh.strict_names(command, workdirs=deps.workdirs, home=deps.home, cwd=cwd, protected=deps.protected,
                            write_dirs=deps.write_dirs)  # the strict reading too: `x '>'; cd ~ && ... .bashrc`
    return not (parts is None or names is None or any(names) or getattr(verdict, "credential", True)
                or getattr(verdict, "private", True) or any(sh._tree_read(words) for words in parts)
                or _names_policy_path(deps, command, cwd) is not None or _never_judged(deps, command, cwd))


async def _jev_approval(deps: Deps, command: str, verdict: Any, cwd: Path, facts: dict, held: dict) -> str | None:
    """Jev's yes to a held shell command (`command_check`), as the logbook's
    reason (`auto-approved: Jev p=0.97`, the lowest answer); None: ask the
    researcher. Never asked about what `_judgeable` keeps from Jev, a command
    that runs a script file (its text is the file's, which never goes to
    TypeSafe), or one the researcher was already asked about (a question waits,
    or they said no). A yes is checked again before it stands (G3): Jev took up
    to 3 s, and a link can be pointed at a key, or a program at another file, in
    that time: so the same real programs, the same verdict, no credential,
    private or policy path, and still no script."""
    from probe.daemon import command_check

    if facts.get("scripts") or not _judgeable(deps, command, verdict, cwd):
        return None
    pol = appr.POLICIES["shell.unsafe_command"]
    if deps.board.find_same(deps.session_id, pol.name, pol.fingerprint(facts), appr.action_digest(held)):
        return None
    programs = _programs(deps, command, cwd)
    if programs is None:
        return None
    answer = await command_check.ask_probe(command=command, cwd=str(cwd), reason=str(verdict.reason or ""),
                                           working_folders=_working_roots(deps))
    if answer is None or not answer.approve:
        return None
    again_programs = _programs(deps, command, cwd)
    if again_programs is None or again_programs != programs:
        return None
    again = _classify(deps, command, cwd)
    if not again.safe and (again.refused or again.reason != verdict.reason or not _judgeable(deps, command, again, cwd)):
        return None
    if _script_facts(deps, command, cwd):
        return None
    return command_check.jev_reason(answer.lowest)


async def _run_steps(deps: Deps, steps: list, why: str) -> str:
    """A compound command with `probe` commands in it (`shell.Step`), run in
    order by the daemon itself, as bash would: `cd` moves the folder the later
    parts run in; `&&` runs the next part only after a success and `||` only
    after a failure (a part that did not run -- blocked, held, refused -- counts
    as a failure); `;` always. Each probe command goes through the checks every
    probe command gets (`_probe_command`: owner, secret scan, holds, lease,
    logbook, Idempotency-Key), in that folder; every other part is classified on
    its own, and runs, is asked about, or is refused like a command of its own.
    `probe X | F`: F reads X's stdout, and the pipeline fails when either fails."""
    cwd, status, out = deps.cwd, 0, []
    for step in steps:
        stop = write_refusal(deps)
        if stop is not None:
            out.append(stop)
            break
        shown = f"$ {scrub(step.text)}"
        if (step.before == "&&" and status != 0) or (step.before == "||" and status == 0):
            out.append(f"{shown}\n[not run: the part before it {'failed' if status else 'succeeded'}]")
            if status != 0 and _step_writes(deps, step, cwd):
                deps.lost_writes += 1  # a write that waited on a failure never ran
            continue
        if step.cd is not None:
            text, status, cwd = _cd_step(deps, step, cwd)
        elif step.probe_argv is not None:
            text, status = await _probe_step(deps, step, cwd, why)
        else:
            verdict = _classify(deps, step.text, cwd)
            text, code = await _shell_command(deps, step.text, verdict, why, cwd)
            status = 1 if code is None else code
        out.append(f"{shown}\n{text}" if text else shown)
        if deps.stopped:
            break
        _renew_after_step(deps)
    return _cap("\n\n".join(out))


def _step_writes(deps: Deps, step: Any, cwd: Path) -> bool:
    """Whether a part of a compound command writes: a `probe` write, or a
    command off the safe list or into a note file."""
    if step.cd is not None:
        return False
    if step.probe_argv is not None:
        if _writes(step.probe_argv):
            return True
        if step.filter is None:
            return False
        verdict = _classify(deps, step.filter, cwd, piped_input=True)
        return bool(verdict.note_target or not verdict.safe)
    verdict = _classify(deps, step.text, cwd)
    return bool(verdict.note_target or not verdict.safe)


def _renew_after_step(deps: Deps) -> None:
    """A finished part of a compound is progress: extend the lease, as a finished
    tool call does (`agent._renew_after`), so several slow probe commands in one
    call cannot outlive it -- but only a live lease this process holds while the
    writer still records the session (`lease.records`), so a lapsed, released or
    taken one stays lost."""
    from probe.daemon import lease

    if deps.replay is None and lease.held(deps.session_id) and lease.records(deps.session_id):
        lease.renew(deps.session_id)


def _cd_step(deps: Deps, step: Any, cwd: Path) -> tuple[str, int, Path]:
    """A lone `cd FOLDER` of a compound command: the folders the later parts run
    in, as bash's `cd` (the logical path, else the physical one). A folder the
    shell's rules would ask about is not entered outside bypass mode."""
    verdict = _classify(deps, step.text, cwd)
    if verdict.refused or not (verdict.safe or (deps.bypass and deps.mode_known)):
        return (f"not run: {verdict.reason} The parts after it run in {cwd}.", 1, cwd)
    joined = os.path.join(str(cwd), step.cd)
    for folder in (os.path.normpath(joined), os.path.realpath(joined)):
        if os.path.isdir(folder):
            # The check above reads `..` from the physical folder and bash goes up the
            # logical one: where it lands must itself be a working folder.
            if not (deps.bypass and deps.mode_known) and not _in_working_folders(deps, folder):
                return (f"not run: cd {step.cd} goes to {folder}, outside the working folders. The parts after it "
                        f"run in {cwd}.", 1, cwd)
            return "", 0, Path(folder)
    return f"[exit 1]\ncd: {step.cd}: no such folder", 1, cwd


def _working_roots(deps: Deps) -> list[str]:
    """The working folders and the session's own, real paths, never $HOME or
    above (as `shell.classify` counts them)."""
    from probe.daemon import shell as sh

    homes = {os.path.realpath(str(deps.home)), os.path.normpath(str(deps.home))}
    roots: list[str] = []
    for folder in [*deps.workdirs, deps.cwd]:
        real = os.path.realpath(str(folder))
        if not any(sh._inside(h, real) for h in homes) and real not in roots:
            roots.append(real)
    return roots


def _in_working_folders(deps: Deps, folder: str) -> bool:
    """`folder` (logically and physically) inside a working folder or the
    session's own, never $HOME or above (as `shell.classify` counts them)."""
    from probe.daemon import shell as sh

    roots = _working_roots(deps)
    return all(any(sh._inside(place, root) for root in roots)
               for place in (os.path.normpath(folder), os.path.realpath(folder)))


async def _probe_step(deps: Deps, step: Any, cwd: Path, why: str) -> tuple[str, int]:
    """A `probe ...` part of a compound command, in `cwd`; with a filter after
    it, the filter reads its stdout (and its stderr after `2>&1`). The filter is
    run like any shell command, told its input may hold a file's text; outside
    bypass mode one that is not safe is not run (a question could not carry the
    input to a later yes)."""
    verdict = None
    if step.filter is not None:
        # Judged before the probe command runs: a write whose filter is then refused
        # would have landed while the model is told "not run".
        verdict = _classify(deps, step.filter, cwd, piped_input=True)
        if verdict.refused or not (verdict.safe or (deps.bypass and deps.mode_known)):
            if deps.stopped is None and _writes(step.probe_argv):
                deps.lost_writes += 1
            return (f"not run: the filter after `probe {shlex.join(step.probe_argv)}` would not run at once "
                    f"({verdict.reason}), so neither part ran.", 1)
    text, result = await _probe_command(deps, step.probe_argv, why=why, cwd=cwd)
    if result is None or result.code != 0:
        return text, 1 if result is None or result.code is None else result.code
    if step.filter is None or verdict is None:
        return text, 0
    feed = result.stdout + (result.stderr if step.stderr == "merge" else "")
    filtered, code = await _shell_command(deps, step.filter, verdict, why, cwd, stdin=feed.encode())
    if step.stderr == "keep" and result.stderr.strip():
        filtered += f"\n[probe's stderr]\n{_cap(scrub(result.stderr), 4000)}"
    return filtered, 1 if code is None else code


def lease_watch(deps: Deps) -> Callable[[], str | None]:
    """For `shell.run(watch=...)`: why a running command must stop now (this
    process may no longer act for the session), or None. The worker passes it for
    a held shell command it runs on a yes."""
    return lambda: deps.stopped if write_refusal(deps) is not None else None


def _shell_status(result: Any) -> str:
    if result.stopped:
        return f"stopped: {result.stopped}"
    return "timed out" if result.timed_out else f"exit {result.exit_code}"


async def _run_shell_write(deps: Deps, command: str, op_id: str, *, head: str, request: str | None,
                           cwd: Path | None = None, stdin: bytes | None = None, reason: str = appr.AUTO) -> Any:
    """An approved (bypass-mode, or Jev's yes: `reason`) shell write, watched by
    the lease. Logged BEFORE it runs (`running`), then with how it ended: ran,
    not run (stopped before the launch), cut short with the bite, or failed
    while it ran. A worker killed meanwhile leaves the `running` line, so a
    command that ran is never missing from the logbook (`probe approvals`).
    Who approved it stays first in the reason: `store.jev_approved` lists
    Jev's yeses by it."""
    from probe.daemon import shell as sh

    row = deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["sh", "-c", command], head=head,
                               status="running", reason=reason, request=request)
    try:
        result = await sh.run(command, cwd=cwd or deps.cwd, watch=lease_watch(deps), stdin=stdin)
    except asyncio.CancelledError:
        deps.store.update_write(row, status="cancelled", reason=f"{reason}; {CUT_SHORT}")
        raise
    except Exception as exc:
        deps.store.update_write(row, status="failed", reason=f"{reason}; {FAILED_WHILE_RUNNING} ({type(exc).__name__})")
        raise
    if not result.started:
        deps.store.update_write(row, status="not_run", reason=f"{reason}; not started: {result.stopped}")
    else:
        deps.store.update_write(row, status="ran", reason=reason, output=result.output, exit_code=result.exit_code)
    return result


# ---------------------------------------------------------------------------
# The team note (D6): every change to it is shown to the researcher first.
# ---------------------------------------------------------------------------


def _team_note_paths(deps: Deps) -> tuple[Path, Path]:
    """The team note's document and the base copy it was last synced from, for
    the daemon's own credential (the CLI keys the base by backend + credential)."""
    from probe.cli import team_note_file
    from probe.sdk.config import DEFAULT_BASE_URL

    # The same key `probe notes sync` computes from its resolved settings.
    origin = (deps.probe_env.get("PROBE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    paths = team_note_file.paths(origin=origin, identity=deps.probe_env.get("PROBE_TOKEN", ""))
    return paths.document, paths.base


def _in_team_note(target: str) -> bool:
    from probe.daemon.folders import note_dirs

    folder = note_dirs()[-1]
    real = os.path.realpath(str(folder))
    return os.path.realpath(target).startswith(real.rstrip(os.sep) + os.sep)


def _read(path: Path | str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _diff(before: str, after: str, name: str) -> str:
    """The whole change, never cut (G3): a yes publishes all of it, so all of it is
    shown (a long one only in `probe approvals`, `approvals._render_team_note`)."""
    return "\n".join(difflib.unified_diff(before.splitlines(), after.splitlines(), f"{name} (now)",
                                         f"{name} (after)", n=1, lineterm=""))


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _team_note_write_facts(verdict: Any) -> dict:
    """What a heredoc into the team note changes, from the file as it is NOW."""
    current = _read(verdict.note_target) or ""
    new = current + (verdict.note_body or "") if verdict.note_append else (verdict.note_body or "")
    return {"what": "an edit of this machine's copy, which the next sync publishes", "path": verdict.note_target,
            "diff": _diff(current, new, Path(verdict.note_target).name), "text_sha": _sha(new),
            "before_sha": _sha(current)}


def _team_note_sync_facts(deps: Deps) -> dict | None:
    """What `notes sync` would publish, from the document and its base as they are
    NOW; None when there is nothing to publish."""
    document, base = _team_note_paths(deps)
    text = _read(document)
    before = _read(base) or ""
    if text is None or text == before:
        return None
    return {"what": "publishing this machine's copy", "path": os.path.realpath(document),
            "diff": _diff(before, text, document.name), "text_sha": _sha(text), "before_sha": _sha(before)}


async def _hold_team_note_write(deps: Deps, command: str, verdict: Any, why: str) -> str:
    """A heredoc into the team note: the session hooks publish that file on their
    own, so the WRITE is the change, and it waits for the researcher's yes."""
    facts = _team_note_write_facts(verdict)
    facts["reason"] = why
    held = {"kind": "shell", "command": command, "cwd": str(deps.cwd), "op_id": _op_id(deps, ["sh", "-c", command])}
    req = _hold(deps, policy="team_note.edit", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req)
    if req.state == appr.APPROVED:
        result = await _run_shell_write(deps, command, held["op_id"], head="team note", request=req.id)
        if result.exit_code != 0 and deps.stopped is None:
            deps.lost_writes += 1
        return f"[{appr.AUTO} · {_shell_status(result)}]\n{scrub(result.output)}"
    deps.store.log_write(bite=deps.bite_id, op_id=held["op_id"], argv=["sh", "-c", command], head="team note",
                         status="held", reason="a team note change waits for the researcher", request=req.id)
    return (f"held for the researcher (request {req.id}) - the team note reaches every teammate's agent. It is "
            "written if they say yes - then run `probe notes sync`.")


async def _maybe_hold_team_note_sync(deps: Deps, parsed: precheck.Parsed, op_id: str, why: str) -> str | None:
    """`probe notes sync` publishes the local team note. A local change nobody has
    said yes to is held (shown as the diff against what was last synced); a change
    the researcher already approved as a write goes ahead."""
    if parsed.params.get("pull_only"):
        return None
    facts = _team_note_sync_facts(deps)
    if facts is None:
        return None
    facts["reason"] = why
    fingerprint = appr.POLICIES["team_note.edit"].fingerprint(facts)
    if any(r.policy == "team_note.edit" and r.fingerprint == fingerprint
           for r in deps.board.all(session_id=deps.session_id, state=appr.APPROVED)):
        return None
    held = {"kind": "probe", "argv": parsed.argv, "op_id": op_id, "cwd": str(deps.cwd)}
    req = _hold(deps, policy="team_note.edit", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req)
    if req.state == appr.APPROVED:
        return None
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="a team note change waits for the researcher", request=req.id)
    return f"held for the researcher (request {req.id}) - publishing the team note. It runs if they say yes."


#: The commands that send a document their argv never names, with the command
#: whose JSON `path` named it in this session (`_remember_checkout`): a push
#: sends what the checkout wrote, a `visuals set` with no `--file` the draft
#: `visuals options` wrote.
_DOCUMENT_FROM = {"notes push": "notes checkout", "summary push": "summary checkout",
                  "visuals set": "visuals options"}


def _document_path(deps: Deps, parsed: precheck.Parsed) -> Path | None:
    """The document `notes push` / `summary push` / `notes sync` (and `visuals
    set` without `--file`) upload though their argv never names it: the file
    this session checked out with the same flags, the team note. None for any
    other command, for a push with no checkout known, and for a help request
    (it sends nothing)."""
    if parsed.help:
        return None
    if parsed.path == "visuals set" and parsed.params.get("file"):
        return None  # the file it names is checked as a file parameter
    if parsed.path in _DOCUMENT_FROM:
        path = (deps.store.fact("checkouts", {}) or {}).get(_checkout_key(_DOCUMENT_FROM[parsed.path], parsed))
        return Path(path) if path else None
    if parsed.path == "notes sync" and not parsed.params.get("pull_only"):
        return _team_note_paths(deps)[0]
    return None


def _document_block(deps: Deps, parsed: precheck.Parsed) -> precheck.Block | None:
    """D2: `notes push`, `summary push`, `visuals set` without `--file` and
    `notes sync` upload a document their argv never names. Resolve it
    (`_document_path`) and scan it like any file a command sends."""
    path = _document_path(deps, parsed)
    if path is None and parsed.path in _DOCUMENT_FROM and not parsed.help and not (
            parsed.path == "visuals set" and parsed.params.get("file")):
        what = {"notes push": "a note's file", "summary push": "a summary's file",
                "visuals set": "a visuals file"}[parsed.path]
        return precheck.Block(precheck.new_block_id(),
                              f"the daemon only knows {what} from a `probe {_DOCUMENT_FROM[parsed.path]}` with "
                              "the same flags in this session", "document", argv=parsed.argv, overridable=False)
    return precheck.check_document(path, parsed) if path is not None else None


def _config_block(deps: Deps, parsed: precheck.Parsed, here: Path) -> precheck.Block | None:
    """A command naming a path a `.probe.config` keeps out of the record, as this
    session sees the files (`precheck.check_config`). A check that fails refuses
    the command (fail closed)."""
    try:
        from probe.sdk import probe_config as pc
        from probe.sdk import session_marker

        _start, skip = pc.session_view(session_marker.sessions_dir(), deps.session_id)
        checker = pc.Checker(cwd=str(here), skip=skip, legacy=True, daemon=True)
        return precheck.check_config(parsed, cwd=here, checker=checker, document=_document_path(deps, parsed))
    except Exception as exc:  # noqa: BLE001
        return precheck.Block(precheck.new_block_id(),
                              f"the .probe.config check failed ({type(exc).__name__}), so it was not run",
                              "probe_config", argv=parsed.argv, overridable=False)


async def _server_has_trash(deps: Deps) -> bool | None:
    """Does the server declare the trash? None: Probe could not be asked."""
    if deps.replay is not None:
        features = getattr(deps.replay, "server_features", None)
        return callable(features) and "trash" in features()
    from probe.daemon import probe_api

    try:
        return await probe_api.has_trash(deps.probe_env)
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        raise


async def run_probe_command(deps: Deps, argv: list[str], *, why: str = "", cwd: Path | None = None) -> str:
    """A `probe ...` command from the model, through every check (`_probe_command`)."""
    return (await _probe_command(deps, argv, why=why, cwd=cwd))[0]


#: What a probe command came to: the text the model reads, and the CLI's own
#: result when the command ran (None: blocked, held, refused, not run).
Outcome = tuple[str, "ProbeResult | None"]


async def _probe_command(deps: Deps, argv: list[str], *, why: str = "", cwd: Path | None = None) -> Outcome:
    """The pre-checks, then the real CLI with the daemon's key and an
    Idempotency-Key, in `cwd` (default: the session's folder). A write that
    failed or was not run -- not asked about, and not stopped because this
    process may no longer write -- counts in `Deps.lost_writes`."""
    asked = deps.asked
    text, result = await _checked_probe_command(deps, argv, why=why, cwd=cwd)
    if ((result is None or result.code != 0) and deps.asked == asked and deps.stopped is None
            and _writes(argv)):
        deps.lost_writes += 1
    return text, result


async def _checked_probe_command(deps: Deps, argv: list[str], *, why: str = "", cwd: Path | None = None) -> Outcome:
    here = cwd or deps.cwd
    stop = write_refusal(deps)
    if stop is not None:
        return stop, None
    if argv[:2] == ["daemon", "override"]:
        if deps.audit:
            return f"{AUDIT_REFUSED} (an override is a question).", None
        return await _request_override(deps, argv[2:], why=why)
    from probe.daemon import probe_api

    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError as exc:
        return f"not run: {exc}", None
    if deps.audit:
        refusal = audit_probe_refusal(parsed)
        if refusal is not None:
            return refusal, None
    if parsed.path in SUMMARY_COMMANDS and _mode_seen(deps) == "lane":
        return LANE_SKIP, None
    try:
        # A help request deletes nothing: no trash to ask about (`precheck.Parsed.help`).
        trash = await _server_has_trash(deps) if parsed.path in precheck.DELETES and not parsed.help else False
    except probe_api.KeyRefused:
        return write_refusal(deps) or NO_LEASE, None
    block = (precheck.check(parsed, cwd=here, trash=trash) or _document_block(deps, parsed)
             or _config_block(deps, parsed, here))
    # A write's key only once it is going to run: a blocked command reads none of
    # the files it names (a key file among them), and a read keeps no count.
    if block is not None or parsed.owner == precheck.READ:
        op_id = uuid.uuid4().hex if deps.op_seed is None else hashlib.sha256(
            f"{deps.op_seed}:{json.dumps(list(argv))}".encode()).hexdigest()[:32]
    else:
        op_id = _op_id(deps, argv, _sent_digest(deps, parsed, here), family=_family(parsed))
    if block is not None:
        block.cwd = str(here)
        deps.blocks[block.id] = block
        deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=parsed.path,
                             status="not_run", reason=f"block {block.id}: {block.why}")
        return block.message(), None
    if parsed.owner == precheck.READ:
        result = await _probe_process(deps, argv, op_id, here)
        deps.store.log_lookup(bite=deps.bite_id, tool="probe", query=shlex.join(argv), result=result.output[:2000])
        return f"[exit {result.code}]\n{_cap(scrub(result.output))}", result
    if parsed.path == "notes sync":
        held = await _maybe_hold_team_note_sync(deps, parsed, op_id, why)
        if held is not None:
            return held, None
    if parsed.path in precheck.CASCADE_DELETES:
        gated = await _maybe_hold_delete(deps, parsed, op_id, why)
        if gated is not None:
            return gated
    elif parsed.path in precheck.PERMANENT_DELETES:
        own = await _own_link(deps, parsed)
        if isinstance(own, str):
            return own, None
        if not own:
            return await _hold_permanent_delete(deps, parsed, op_id, why)
        # The logbook shows that no question was asked, and why.
        why = f"{OWN_LINK_REASON}{why}"
    try:
        result = await _probe_process(deps, argv, op_id, here)
    except asyncio.CancelledError:
        deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=parsed.path,
                             status="cancelled", reason=f"{CUT_SHORT} - it may have written part of its work")
        raise
    code, output = result.code, result.output
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=parsed.path,
                         status=write_status(code, result.stderr), output=output, exit_code=code,
                         reason=_cap(why, 300) or None)
    fact = None
    if code == 0:
        _remember_note(deps, parsed, result.stdout)
        # After the logbook line: a bite cut short during the lookup must not
        # read as a write cut short. Not for a queued write: nothing landed yet.
        if write_status(code, result.stderr) == "ran":
            await scope.stamp(deps, parsed)
            fact = branch_fact(deps, parsed, result.stdout)
            note_summary_marks(deps, parsed, argv, result.stdout, result.stderr)
    elif parsed.path.startswith(("summary ", "visuals ")):
        note_summary_marks(deps, parsed, argv, result.stdout, result.stderr)
    elif parsed.path not in IDEMPOTENT_COMMANDS:
        output += "\n[not retried: it may have written part of its work]"
    stop = write_refusal(deps) if deps.key_refused else None
    text = f"[exit {code}]\n{_cap(scrub(output))}" + (f"\n{fact}" if fact else "")
    return text + (f"\n{stop}" if stop else ""), result


#: The fact a run move adds when it files a branch of a run outside any
#: experiment, and earlier moves filed its siblings the same way (writer channel
#: PR-2: six SFT arms of one base run went project-direct, one by one).
BRANCH_FACT = "{n} runs branch from {parent}; none is in an experiment"


def _moved_run(text: str | None) -> dict | None:
    """The run a `run move` printed (its first JSON value), or None."""
    try:
        value, _end = json.JSONDecoder().raw_decode((text or "").lstrip())
    except ValueError:
        return None
    return value if isinstance(value, dict) and value.get("id") else None


def branch_fact(deps: Deps, parsed: precheck.Parsed, stdout: str) -> str | None:
    """After a `run move` that left the run in no experiment: when the runs this
    session moved that branch from the same parent number two or more and none is
    in an experiment, one plain fact line (BRANCH_FACT). From the logbook's own
    outputs: no call to Probe."""
    if parsed.path != "run move":
        return None
    run = _moved_run(stdout)
    if run is None or run.get("experiment_id") or not run.get("parent_run_id"):
        return None
    parent = run["parent_run_id"]
    siblings: dict[str, dict] = {}
    names: dict[str, str] = {}
    for row in deps.store.db.execute("SELECT output FROM writes WHERE head = 'run move' AND status = 'ran' "
                                     "ORDER BY id"):
        moved = _moved_run(row["output"])
        if moved is None:
            continue
        names[moved["id"]] = moved.get("slug") or moved["id"]
        if moved.get("parent_run_id") == parent:
            siblings[moved["id"]] = moved  # the newest move of each run wins
    siblings[run["id"]] = run
    if len(siblings) < 2 or any(r.get("experiment_id") for r in siblings.values()):
        return None
    return BRANCH_FACT.format(n=len(siblings), parent=names.get(parent, parent))


#: The flags that name a note's or a summary's document. Sweep groups and files
#: no longer carry notes, so `--group` / `--artifact` name none.
_ANCHORS = ("project", "experiment", "run", "note")


def _anchor_key(parsed: precheck.Parsed) -> str:
    return "|".join(f"{k}={parsed.params.get(k)}" for k in _ANCHORS if parsed.params.get(k))


def _checkout_key(checkout: str, parsed: precheck.Parsed) -> str:
    """Where a checkout's path is kept: a note's under its flags alone (as
    before), a summary's or a visuals draft's under its command too."""
    anchors = _anchor_key(parsed)
    return anchors if checkout == "notes checkout" else f"{checkout}|{anchors}"


#: The last summary the writer loaded (`probe summary checkout`), for the pin
#: (`worker.Worker._summary_pin`): {"kind", "label", "version", "text", "path",
#: "loaded"}; `loaded` is the checkout's version, which the history is searched for.
SUMMARY_PIN = "summary_pin"


def _remember_note(deps: Deps, parsed: precheck.Parsed, stdout: str) -> None:
    """The file a `notes checkout`, `summary checkout` or `visuals options`
    wrote (the `path` of the JSON it prints on stdout), for the push or `visuals
    set` with the same flags (`_document_path`); and a summary's text, for the
    pin."""
    if parsed.path not in _DOCUMENT_FROM.values():
        if parsed.path == "summary push":
            _pin_after_push(deps, parsed, stdout)
        return
    try:
        payload = json.loads(stdout or "")
    except ValueError:
        return
    path = payload.get("path") if isinstance(payload, dict) else None
    if isinstance(path, str) and os.path.isabs(path):
        checkouts = deps.store.fact("checkouts", {}) or {}
        checkouts[_checkout_key(parsed.path, parsed)] = path
        deps.store.set_fact("checkouts", checkouts)
        if parsed.path == "summary checkout" and isinstance(payload.get("markdown"), str):
            version = int(payload.get("version") or 0)
            deps.store.set_fact(SUMMARY_PIN, {
                "kind": str(payload.get("target") or ""), "label": str(payload.get("label") or ""),
                "version": version, "loaded": version, "text": payload["markdown"], "path": path,
                "anchor": _anchor_key(parsed)})


def _pin_after_push(deps: Deps, parsed: precheck.Parsed, stdout: str) -> None:
    """A push that landed on the pinned summary: the pin is now what was pushed
    (the draft, which is the page's text after a landed push)."""
    pin = deps.store.fact(SUMMARY_PIN)
    if not isinstance(pin, dict) or pin.get("anchor") != _anchor_key(parsed):
        return
    try:
        payload = json.loads(stdout or "")
    except ValueError:
        return
    if not (isinstance(payload, dict) and payload.get("pushed")):
        return
    text = _read(pin.get("path") or "")
    if text is None:
        return
    deps.store.set_fact(SUMMARY_PIN, {**pin, "version": int(payload.get("version") or 0), "text": text})


async def _maybe_hold_delete(deps: Deps, parsed: precheck.Parsed, op_id: str, why: str) -> Outcome | None:
    """`delete.others_data`: a delete whose target or anything under it was made by
    another researcher waits for the researcher's yes (D22). Facts from Probe.
    None: it reaches only the daemon's own work, and runs. Anything it cannot
    establish refuses the delete (FAIL CLOSED): it never runs unchecked."""
    from probe.daemon import probe_api

    try:
        facts = await deletion_facts(deps, parsed)
    except probe_api.KeyRefused:
        return write_refusal(deps) or NO_LEASE, None
    except Exception as exc:  # noqa: BLE001 -- a delete nobody could check does not run
        return f"not run: could not read what the delete would reach ({type(exc).__name__}: {exc}).", None
    if facts.get("refused"):
        deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                             status="not_run", reason=str(facts["refused"]))
        return f"not run: {facts['refused']}", None
    if not facts.get("others"):
        return None
    facts["reason"] = why
    held = {"kind": "probe", "argv": parsed.argv, "op_id": op_id, "cwd": str(deps.cwd)}
    req = _hold(deps, policy="delete.others_data", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        return await _run_approved(deps, parsed.argv, op_id, head=parsed.path, request=req.id)
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="reaches another researcher's data", request=req.id)
    return (f"held for the researcher (request {req.id}) - it deletes another researcher's data. It runs if they "
            "say yes."), None


async def deletion_facts(deps: Deps, parsed: precheck.Parsed) -> dict:
    """What the delete would trash, by creator: `DELETE ...?dry_run=true` (S13),
    sent only to a server that declares the trash. Raises `probe_api.Unreachable`
    when Probe could not be asked whether it has one.

    Never None. When the target cannot be read from the command (under the name
    the CLI's parser gives it: `project_id`, `experiment_id`, `run`), when it is
    not a slug or an id, or when the server has no trash, the facts carry
    `refused` and no id: the caller refuses, and a stored yes no longer matches
    them, so it is void."""
    from probe.daemon import probe_api

    kind = precheck.CASCADE_DELETES[parsed.path]
    target = precheck.delete_target(parsed)

    def refused(why: str) -> dict:
        return {"id": None, "name": target, "what": kind, "others": {"unknown owner|items": 1}, "count": None,
                "updated_at": None, "refused": why}

    if not target:
        return refused(f"`probe {parsed.path}` names no target the daemon can read, so it can't check what the "
                       "delete reaches.")
    try:
        probe_api.valid_ref(target)
    except probe_api.BadRef as exc:
        return refused(f"{exc}: a delete takes a slug, a uuid or id:<uuid>")
    trash = await _server_has_trash(deps)
    if trash is None:  # not "no trash": the caller tries again later
        raise probe_api.Unreachable(precheck.TRASH_UNKNOWN)
    if not trash:
        return refused(precheck.NO_TRASH)
    if deps.replay is not None:
        return deps.replay.deletion_facts(kind, target)
    try:
        return await probe_api.deletion_preview(deps.probe_env, kind, target,
                                                recursive=bool(parsed.params.get("recursive")))
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        raise


async def _own_link(deps: Deps, parsed: precheck.Parsed) -> bool | str:
    """Is this `edge remove` of a link THIS researcher's daemon made (lineage
    plan L9, R9)? Then it runs without a question: the daemon revisits its own
    links as the session goes on. True only when Probe says so
    (`probe_api.edge_is_this_daemons`); anything it cannot establish -- a server
    without `GET /v1/edges/{id}`, an unreadable edge, no answer -- is False, and
    the delete asks as every permanent delete does (FAIL CLOSED, like
    `_maybe_hold_delete`). Bypass mode asks nothing anyway, so it reads nothing.
    A str: the stop message, when Probe refused the key."""
    from probe.daemon import probe_api

    if parsed.path != "edge remove" or (deps.bypass and deps.mode_known):
        return False
    edge_id = next((v for v in precheck._strings(parsed.params.get("edge_id")) if v.strip()), None)
    if not edge_id:
        return False
    try:
        if deps.replay is not None:
            check = getattr(deps.replay, "edge_is_this_daemons", None)
            answer = check(edge_id) if callable(check) else False
        else:
            answer = probe_api.edge_is_this_daemons(deps.probe_env, edge_id)
        if inspect.isawaitable(answer):
            answer = await answer
        return answer is True  # only a plain yes exempts it
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        return write_refusal(deps) or NO_LEASE
    except Exception:  # noqa: BLE001 -- an edge nobody could read is asked about
        return False


async def _hold_permanent_delete(deps: Deps, parsed: precheck.Parsed, op_id: str, why: str) -> Outcome:
    """`delete.permanent`: a delete with no trash behind it (an artifact, a note, a
    paper, a view, an edge...) cannot be undone, so it waits for the researcher's
    yes, whoever made what it deletes. Bypass mode runs it at once."""
    auto = deps.bypass and deps.mode_known
    shown = appr.override_command(parsed.argv)
    if len(shown) > appr.COMMAND_CHARS and not auto:
        return (f"not run: the command is {len(shown)} characters - a question shows at most "
                f"{appr.COMMAND_CHARS}."), None
    facts = {"command": shown, "what": precheck.PERMANENT_DELETES[parsed.path], "undo": "cannot be undone",
             "reason": why}
    held = {"kind": "probe", "argv": parsed.argv, "op_id": op_id, "cwd": str(deps.cwd)}
    req = _hold(deps, policy="delete.permanent", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        return await _run_approved(deps, parsed.argv, op_id, head=parsed.path, request=req.id)
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="a delete Probe cannot undo", request=req.id)
    return f"held for the researcher (request {req.id}) - this delete can't be undone. It runs if they say yes.", None


async def _run_approved(deps: Deps, argv: list[str], op_id: str, *, head: str, request: str,
                        cwd: Path | None = None) -> Outcome:
    """A held probe command bypass mode approved at once: run, logged as such."""
    result = await _probe_process(deps, argv, op_id, cwd or deps.cwd)
    code, output = result.code, result.output
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=head,
                         status=write_status(code, result.stderr), reason=appr.AUTO, output=output, exit_code=code,
                         request=request)
    if write_status(code, result.stderr) == "ran":
        await scope.stamp_argv(deps, argv)
    stop = write_refusal(deps) if deps.key_refused else None
    return f"[{appr.AUTO} · exit {code}]\n{_cap(scrub(output))}" + (f"\n{stop}" if stop else ""), result


def _is_delete(argv: list[str]) -> bool:
    try:
        return precheck.parse(argv).path in precheck.DELETES
    except precheck.ParseError:
        return False


async def _request_override(deps: Deps, args: list[str], *, why: str) -> Outcome:
    if not args:
        return "usage: probe daemon override <block> --why \"<one line: why the check is wrong>\"", None
    block_id = args[0]
    reason = why
    if "--why" in args:
        at = args.index("--why")
        reason = " ".join(args[at + 1:at + 2]) or why
    block = deps.blocks.get(block_id)
    if block is None:
        return f"no block {block_id} in this bite - running the command again shows its block id.", None
    if not block.overridable:
        return f"block {block_id} has no override: {block.why}", None
    if _is_delete(block.argv):
        # G5: whatever blocked it, a delete runs only through its own checks (the
        # trash, and the researcher's yes when it reaches others' data).
        return (f"block {block_id} has no override: a delete runs only as a plain command, through the delete "
                "checks."), None
    auto = deps.bypass and deps.mode_known
    here = Path(block.cwd) if block.cwd else deps.cwd
    if here != deps.cwd and not auto:
        # A yes runs from the worker, in the session's folder: a relative path in
        # the command would name another file there than the one that was checked.
        return f"not run: block {block_id} came from a command run in {here}, and a yes runs in {deps.cwd}.", None
    # Each argument scrubbed on its own: a redaction can hide a flagged value, never
    # swallow the arguments after it (C1). The yes is bound to the raw argv.
    shown = appr.override_command(block.argv)
    if len(shown) > appr.COMMAND_CHARS and not auto:
        return (f"not run: the command is {len(shown)} characters - a question shows at most {appr.COMMAND_CHARS}. "
                "A long text can go in a file (`@file`)."), None
    facts = {"command": shown, "blocked_because": block.why, "flagged": block.flagged, "masked": block.flagged,
             "reason": reason}
    try:
        parsed = precheck.parse(block.argv)
        content, family = _sent_digest(deps, parsed, here), _family(parsed)
    except precheck.ParseError:
        content, family = "", None
    held = {"kind": "probe", "argv": block.argv, "op_id": _op_id(deps, block.argv, content, family=family),
            "cwd": str(here),
            "override": block.check}
    req = _hold(deps, policy="check.override", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        return await _run_approved(deps, block.argv, held["op_id"], head="override", request=req.id, cwd=here)
    deps.store.log_write(bite=deps.bite_id, op_id=held["op_id"], argv=["probe", *block.argv], head="override",
                         status="held", reason=f"override of block {block_id}: {reason}", request=req.id)
    return f"held for the researcher: request {req.id}. If they say yes, the command runs as it was.", None


# ---------------------------------------------------------------------------
# read
# ---------------------------------------------------------------------------


async def read_file(deps: Deps, path: str, offset: int | None = None, limit: int | None = None) -> str:
    """Read a file: numbered lines (`offset`: the first line, 1-based; `limit`:
    how many, at most 2000), or with neither, a preview of a CSV/TSV (header,
    first rows, shape), JSON (what it holds, pretty-printed), Parquet or NumPy
    .npy/.npz file (dtype, shape, first values). Never a pickle (loading one runs
    code) or an image. The files a safe `cat` may read (`shell.read_refusal`),
    and the Probe skills folder, read-only (a `cat` of it is not safe-listed);
    in bypass mode any file but Probe's own key and state. Scrubbed and capped.

    For the tool list: a READ tool (not in `WRITE_TOOLS`). Everything it touches
    on the store runs on the event loop; only the file's own reading goes to a
    thread."""
    from probe.daemon import reader
    from probe.daemon import shell as sh
    from probe.daemon.bite import skills_root

    stop = write_refusal(deps)
    if stop is not None:
        return stop
    path = (path or "").strip()
    if not path:
        return "give a path"
    if "\0" in path:
        return "not read: the path holds a NUL byte"
    skills = None if deps.reader else skills_root()
    path = _in_skills(path, deps.cwd, skills)
    refused = sh.read_refusal(path, workdirs=deps.workdirs, home=deps.home, cwd=deps.cwd,
                              protected=deps.protected, write_dirs=deps.write_dirs,
                              read_dirs=[skills] if skills is not None else [],
                              hidden=_off_check(deps, deps.cwd))
    if refused is not None:
        reason, never = refused
        if never:
            return f"not read: {reason} This is refused in every mode."
        if deps.reader:
            return f"not read: {reason} The reader reads only what a safe `cat` may read in the working folders."
        if not (deps.bypass and deps.mode_known):
            # The shell's read programs reach further (`shell.classify`): a plain file outside runs at once there.
            return (f"not read: {reason} The read tool reads only what a safe `cat` may read in the working "
                    "folders. Outside them, `cat` through the shell runs at once for a plain file; a hidden, "
                    "credential-shaped or private one asks the researcher.")
    full = Path(str(deps.home) + path[1:]) if path == "~" or path.startswith("~/") else deps.cwd / path
    text = scrub(await asyncio.to_thread(reader.render, full, offset, limit))
    if not deps.reader:
        deps.store.log_lookup(bite=deps.bite_id, tool="read", query=path, result=text[:2000])
    return text


def _in_skills(path: str, cwd: Path, skills: Path | None) -> str:
    """A path the skills name relative to their folder (`track-work/reference.md`)
    is read there, when it names no file in the session's folder: `path` made
    absolute. Anything else, `path` as given."""
    if skills is None or os.path.isabs(path) or path.startswith("~") or os.path.lexists(cwd / path):
        return path
    inside = os.path.normpath(skills / path)
    if not inside.startswith(str(skills).rstrip(os.sep) + os.sep) or not os.path.isfile(inside):
        return path
    return inside


# ---------------------------------------------------------------------------
# session(op=...): the chat log, the logbook, the state of the record
# ---------------------------------------------------------------------------


class SessionOp(StrEnum):
    OPEN = "open"
    OUTLINE = "outline"
    SEARCH = "search"
    LOGBOOK = "logbook"
    STATUS = "status"


#: The ops as the tool's schema names them: an inline `enum` (a StrEnum would be a `$ref`).
SessionOpName = Literal[tuple(op.value for op in SessionOp)]  # type: ignore[valid-type]
#: `kind` of op=search, the same way: a free string let a guessed kind ("output")
#: answer "no event matches" for text that IS in the session.
KindName = Literal[tuple(k.value for k in Kind)]  # type: ignore[valid-type]


#: The arguments each op of `session` takes. The tool's schema is the union of
#: them all, so an argument that belongs to another op is REFUSED before
#: anything runs, never dropped: dropped, it answers a question nobody asked
#: (the lesson of #735; the old `session_search(logbook=true)` dropped `kind`
#: and the turn range that way).
SESSION_OPTIONS: dict[SessionOp, tuple[str, ...]] = {
    SessionOp.OPEN: ("event_id", "turn", "page"),
    SessionOp.OUTLINE: ("page",),
    SessionOp.SEARCH: ("query", "kind", "turn_from", "turn_to"),
    SessionOp.LOGBOOK: ("query",),
    SessionOp.STATUS: (),
}


#: The reader's ops: the session itself, and the writer's logbook (read only: so the
#: reader can say what the writer filed). `status` is the writer's own.
READER_SESSION_OPS: frozenset[SessionOp] = frozenset({SessionOp.OPEN, SessionOp.OUTLINE, SessionOp.SEARCH,
                                                      SessionOp.LOGBOOK})
ReaderSessionOpName = Literal[tuple(op.value for op in SessionOp if op in READER_SESSION_OPS)]  # type: ignore[valid-type]


def session(deps: Deps, op: str, *, status: Callable[[], str] | None = None, event_id: str | None = None,
            turn: int | None = None, page: int | None = None, query: str | None = None, kind: str | None = None,
            turn_from: int | None = None, turn_to: int | None = None) -> str:
    """The `session` tool: `op` picks what it reads, and only that op's
    arguments (`SESSION_OPTIONS`) may be given -- None or "" is not given.
    `status`: plain code's state of the record (`Worker.state_of_record`)."""
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    allowed = READER_SESSION_OPS if deps.reader else frozenset(SessionOp)
    raw = op
    try:
        op = SessionOp(op)
    except ValueError:
        op = None
    if op is None or op not in allowed:
        return f"not run: op {raw!r} is not one of: {', '.join(o.value for o in SessionOp if o in allowed)}"
    given = {"event_id": event_id, "turn": turn, "page": page, "query": query, "kind": kind,
             "turn_from": turn_from, "turn_to": turn_to}
    foreign = [name for name, value in given.items() if value not in (None, "") and name not in SESSION_OPTIONS[op]]
    if foreign:
        named = ", ".join(f"`{name}`" for name in foreign)
        options = ", ".join(SESSION_OPTIONS[op]) or "none"
        return (f"not run: {named} {'is not an option' if len(foreign) == 1 else 'are not options'} of op={op}; "
                f"its options are: {options}")
    if op in (SessionOp.SEARCH, SessionOp.LOGBOOK) and not (query or "").strip():
        return f"not run: op={op} needs `query`"
    if kind and kind not in {k.value for k in Kind}:
        return f"not run: kind {kind!r} is not one of: {', '.join(k.value for k in Kind)}"
    if op == SessionOp.OPEN:
        return session_open(deps, event_id, turn, False, page or 0)
    if op == SessionOp.OUTLINE:
        text = _outline(deps.store)
        # One line per turn has no end of its own: past a page it pages like `open`
        # (it was left to the harness's spill to a file, which is gone).
        return text if len(text) <= OPEN_PAGE_CHARS else _page(text, page or 0, "outline")
    if op == SessionOp.SEARCH:
        return session_search(deps, query or "", kind, turn_from, turn_to)
    if op == SessionOp.LOGBOOK:
        return session_search(deps, query or "", logbook=True)
    if status is None:
        return "not run: the state of the record is not available here"
    return _cap(status())


def session_search(deps: Deps, query: str, kind: str | None = None, turn_from: int | None = None,
                   turn_to: int | None = None, logbook: bool = False) -> str:
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    if logbook:
        rows = deps.store.search_logbook(query, limit=SEARCH_LIMIT, writes_only=deps.reader)
        if not rows:
            whose = "the writer's" if deps.reader else "your"
            return f"nothing in {whose} logbook matches {query!r}"
        return "\n".join(f"- {r['what']} #{r['id']}: {r['body'][:300]} {r['status'] or ''} {(r['reason'] or '')[:200]}"
                         for r in rows)
    kinds = [kind] if kind else None
    # The writer never sees what arrived in `read only (daemon)`; the reader does.
    hits = deps.store.search(query, kinds=kinds, turn_from=turn_from, turn_to=turn_to, limit=SEARCH_LIMIT,
                             recorded=not deps.reader)
    if not deps.reader:  # the logbook is the writer's
        deps.store.log_lookup(bite=deps.bite_id, tool="session.search", query=query, result=f"{len(hits)} hits")
    if not hits:
        return f"no event matches {query!r}" + (f" (kind {kind})" if kind else "")
    out = []
    for ev in hits:
        text = ev.command or ev.text
        at = text.lower().find(query.split()[0].lower()) if query.split() else 0
        start = max(0, at - 200)
        snippet = text[start:start + 500].replace("\n", " ⏎ ")
        tag = f" ({ev.note})" if ev.note else ""
        out.append(f"- {ev.event_id} · turn {ev.turn} · {ev.kind.value}{' · ' + ev.tool if ev.tool else ''}: "
                   f"{snippet}{tag}")
    return "\n".join(out)


def session_open(deps: Deps, event_id: str | None = None, turn: int | None = None, outline: bool = False,
                 page: int = 0) -> str:
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    recorded = not deps.reader  # the writer never sees `read only (daemon)`
    if outline:
        return _outline(deps.store, recorded=recorded)
    if turn is not None:
        from probe.daemon.bite import render

        rows = deps.store.db.execute("SELECT seq FROM events WHERE turn = ? ORDER BY seq", (turn,)).fetchall()
        if not rows:
            return f"no turn {turn}"
        events = deps.store.events_between(rows[0]["seq"], rows[-1]["seq"], recorded=recorded)
        text = "\n\n".join(render(ev) for ev in events if ev.turn == turn)
        return _page(text, page, f"turn {turn}")
    if not event_id:
        return "give an event_id or a turn (op=outline: one line per turn)"
    ev = deps.store.get(event_id, recorded=recorded)
    if ev is None:
        return f"no event {event_id}"
    text = ev.text
    if ev.side_file:
        side = _read_side(deps, ev.side_file)
        if side is not None:  # the full text: scrubbed as the preview was at intake
            text = _off_scrubbed(deps, side, Path(ev.cwd or deps.cwd))
    if ev.note:
        text = f"({ev.note})\n{text}"
    if ev.kind == Kind.TOOL_OUTPUT:
        call = deps.store.call_for(ev.call_id, recorded=recorded)
        head = f"output of: {call.command or ' '.join(filter(None, (call.tool, call.text)))}\n" if call else ""
        text = head + text
    elif ev.command:
        text = ev.command
    return _page(scrub(text), page, event_id)


def _read_side(deps: Deps, path: str) -> str | None:
    """A persisted output's full text: only from THIS session's side folder
    (`<session id>/tool-results/`; the adapter checked the path against the
    session's own folder when it read the line, and this checks again)."""
    try:
        resolved = Path(path).resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if resolved.parent.name != "tool-results" or resolved.parent.parent.name != deps.session_id:
        return None
    if not resolved.is_file() or resolved.stat().st_size > MAX_SIDE_FILE_BYTES:
        return None
    try:
        return resolved.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _page(text: str, page: int, label: str) -> str:
    pages = max(1, -(-len(text) // OPEN_PAGE_CHARS))
    page = max(0, min(page, pages - 1))
    chunk = text[page * OPEN_PAGE_CHARS:(page + 1) * OPEN_PAGE_CHARS]
    more = f"\n[page {page + 1} of {pages}; page={page + 1} for more]" if page + 1 < pages else ""
    return f"[{label} · page {page + 1} of {pages}]\n{chunk}{more}"


def _outline(store: Store, *, recorded: bool = False) -> str:
    only = f" WHERE (e.bite IS NULL OR e.bite != {UNRECORDED_BITE})" if recorded else ""
    p_only = f" AND (p.bite IS NULL OR p.bite != {UNRECORDED_BITE})" if recorded else ""
    rows = store.db.execute(
        "SELECT turn, min(ts) AS ts, count(*) AS n, "
        f"(SELECT text FROM events p WHERE p.turn = e.turn AND p.kind = 'prompt'{p_only} ORDER BY seq LIMIT 1) "
        "AS prompt, "
        f"sum(CASE WHEN kind = 'tool_call' THEN 1 ELSE 0 END) AS calls FROM events e{only} GROUP BY turn ORDER BY turn")
    lines = [f"turn {r['turn']} · {r['n']} events · {r['calls']} commands · {(r['prompt'] or '(no prompt)')[:160]!r}"
             for r in rows]
    return "\n".join(lines) or "empty session"



#: Commands whose landing makes a summary owed (plan 3.5): the entity is new, or
#: an experiment's question got its answer.
_OWES_SUMMARY = frozenset({"project create", "experiment create"})
#: The run's summary and visuals tally (`Deps.summaries_owed` and friends), kept
#: in the store until the run's end stands (`tally_settled`): a run paused after
#: ROUNDS_BEFORE_YIELD carries on in the next bite with new Deps, and still owes.
SUMMARY_TALLY = "summary_tally"
_TALLY_SETS = ("summaries_owed", "summaries_pushed", "concluded", "visuals_landed")
_TALLY_FLAGS = ("summaries_off", "summaries_owed_asked", "visuals_owed_asked")


def _tally(deps: Deps) -> None:
    """Read the stored tally into `deps`, once per Deps."""
    if deps.tally_loaded:
        return
    deps.tally_loaded = True
    saved = deps.store.fact(SUMMARY_TALLY)
    if not isinstance(saved, dict):
        return
    for name in _TALLY_SETS:
        getattr(deps, name).update(str(x) for x in saved.get(name) or [] if isinstance(x, str))
    for name in _TALLY_FLAGS:
        setattr(deps, name, getattr(deps, name) or bool(saved.get(name)))
    state = saved.get("visuals_state")
    if isinstance(state, dict):
        deps.visuals_state.update({k: v for k, v in state.items() if isinstance(v, dict) and k not in deps.visuals_state})


#: The team's summaries mode as last seen (`{"mode", "at"}`): a checkout's JSON,
#: a refused push or set (lane), a landed push (recorder), or
#: `summaries_mode`'s read. The writer is sent back for a summary only in
#: recorder mode: in lane mode the push is refused, and asking costs rounds.
SUMMARIES_MODE = "summaries_mode"
#: How long a seen mode stands: the global flip moves it once, and a stale
#: `lane` only skips a nudge.
SUMMARIES_MODE_TTL_S = 1800


#: The commands that keep a summary and its tables: in lane mode the server
#: refuses the writes, and the bench's lane replays spent a quarter more on them
#: (12 checkouts, 3 pushes, 12 visuals calls a session). Once a checkout or a
#: refusal said lane, they are not run until the seen mode expires.
SUMMARY_COMMANDS = frozenset({"summary checkout", "summary push", "visuals options", "visuals set"})
LANE_SKIP = ("not run: Probe's overview lane still writes this team's summaries and tables (mode lane), so "
             "`probe summary` and `probe visuals` wait until it hands them over. Record everything else as usual.")


def _mode_seen(deps: Deps) -> str | None:
    """The stored mode while fresh (`SUMMARIES_MODE`), else None; asks nobody."""
    saved = deps.store.fact(SUMMARIES_MODE)
    if isinstance(saved, dict) and time.time() - float(saved.get("at") or 0) < SUMMARIES_MODE_TTL_S:
        return saved.get("mode")
    return None


def _note_mode(deps: Deps, mode: str) -> None:
    deps.store.set_fact(SUMMARIES_MODE, {"mode": mode, "at": time.time()})


async def summaries_mode(deps: Deps, owed: str) -> str | None:
    """`lane` | `recorder` | None (unknown: the server could not say). The
    stored mode while fresh, else one summary read of `owed` (`kind ref`)."""
    from probe.daemon import probe_api

    seen = _mode_seen(deps)
    if seen in probe_api.SUMMARIES_MODES:
        return seen
    kind, _, ref = owed.partition(" ")
    try:
        mode = await asyncio.wait_for(probe_api.summaries_mode(deps.probe_env, kind, ref), probe_api.SCOPE_TIMEOUT_S)
    except probe_api.KeyRefused:
        _mark_key_refused(deps)  # the worker hands recording back, as for any refused key
        return None
    except Exception:  # noqa: BLE001 -- unknown: no nudge
        return None
    if mode:
        _note_mode(deps, mode)
    return mode


def tally_save(deps: Deps) -> None:
    deps.store.set_fact(SUMMARY_TALLY, {
        **{name: sorted(getattr(deps, name)) for name in _TALLY_SETS},
        **{name: bool(getattr(deps, name)) for name in _TALLY_FLAGS},
        "visuals_state": deps.visuals_state,
    })


def tally_settled(deps: Deps) -> None:
    """The run's end stands: the next run starts owing nothing. What the last
    checkouts said about tables (`visuals_state`) stays for the session."""
    deps.store.set_fact(SUMMARY_TALLY, {"visuals_state": deps.visuals_state})


def _flag_key(parsed: Any) -> str | None:
    """`kind:ref` from a summary or visuals command's own `--experiment` /
    `--project` flags."""
    from probe.cli import summary_cli

    experiment = next(iter(precheck._strings(parsed.params.get("experiment"))), None)
    if experiment:
        return f"{summary_cli.EXPERIMENT}:{experiment}"
    project = next(iter(precheck._strings(parsed.params.get("project"))), None)
    return f"{summary_cli.PROJECT}:{project}" if project else None


def _json(stdout: str) -> dict | None:
    try:
        payload = json.loads(stdout or "")
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


def _lane_said(parsed: Any, stdout: str, stderr: str) -> bool:
    """Did this summary or visuals command say the team's summaries are the
    lane's? A checkout's JSON `mode`; a refused push's JSON `detail`, or a
    refused `visuals set`'s error line, ending in `summary_cli.LANE_MARK`.
    Never free text: a page, a chart title in a 409's list, any other
    command's output could hold the same words."""
    from probe.cli import summary_cli

    payload = _json(stdout)
    if parsed.path == "summary checkout":
        return bool(payload) and payload.get("mode") == summary_cli.MODE_LANE
    if parsed.path == "summary push":
        detail = payload.get("detail") if payload else None
        return isinstance(detail, str) and detail.endswith(summary_cli.LANE_MARK)
    if parsed.path == "visuals set":
        return any(line.startswith("error: ") and line.rstrip().endswith(summary_cli.LANE_MARK)
                   for line in (stderr or "").splitlines())
    return False


def note_summary_marks(deps: Deps, parsed: Any, argv: list[str], stdout: str = "", stderr: str = "") -> None:
    """Keep the run's summary and visuals tally (`Deps.summaries_owed` and
    friends, saved to the store; plain code, never raises into the write it
    follows). A push settles a summary only when it landed (`pushed` in its
    JSON): a merge that asks for another push, a conflict or a refusal do not."""
    try:
        _tally(deps)
        from probe.cli import summary_cli

        if _lane_said(parsed, stdout, stderr):
            deps.summaries_off = True
            _note_mode(deps, summary_cli.MODE_LANE)
        elif parsed.path == "summary push":
            key = _flag_key(parsed)
            payload = _json(stdout)
            if key and payload and payload.get("pushed"):
                deps.summaries_pushed.add(key)
                _note_mode(deps, "recorder")
        elif parsed.path == "summary checkout":
            key = _flag_key(parsed)
            payload = _json(stdout)
            visuals = payload.get("visuals") if payload else None
            if key and isinstance(visuals, dict):
                deps.visuals_state[key] = visuals
            if payload and payload.get("mode") == "recorder":
                _note_mode(deps, "recorder")
        elif parsed.path == "visuals set":
            key = _flag_key(parsed)
            if key and _json(stdout) and _json(stdout).get("set"):
                deps.visuals_landed.add(key)
        else:
            conclusion = precheck._strings(parsed.params.get("conclusion"))
            concluding = parsed.path == "experiment set" and any(c.strip() for c in conclusion)
            if not (parsed.path in _OWES_SUMMARY or concluding):
                return
            found = summary_cli.landing(list(argv))
            if found is None:
                return
            key = f"{found[0]}:{found[1]}"
            deps.summaries_owed.add(key)
            deps.summaries_pushed.discard(key)  # a push before this write does not cover it
            if concluding:
                deps.concluded.add(key)
        tally_save(deps)
    except Exception:  # noqa: BLE001 -- bookkeeping, never a failed write
        return


def summaries_owed(deps: Deps) -> list[str]:
    """`kind ref` for each summary this run owes and did not push; [] when the
    team's summaries are the lane's."""
    _tally(deps)
    if deps.summaries_off:
        return []
    return [key.replace(":", " ", 1) for key in sorted(deps.summaries_owed - deps.summaries_pushed)]


def visuals_owed(deps: Deps) -> list[str]:
    """`kind ref` for each experiment this run concluded whose checkout said it
    carries Metrics-center tables and charts and has none, with no `visuals set`
    since; [] when the team's summaries are the lane's."""
    _tally(deps)
    if deps.summaries_off:
        return []
    owed = [key for key in deps.concluded
            if (deps.visuals_state.get(key) or {}).get("eligible") and not deps.visuals_state[key].get("count")
            and key not in deps.visuals_landed]
    return [key.replace(":", " ", 1) for key in sorted(owed)]
