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
                               unless the session runs in bypass mode

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
from probe.daemon.events import Kind
from probe.daemon.store import UNRECORDED_BITE, Store, scrub
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
#: (project create), POST /v1/projects/{id}/groups, PATCH
#: /v1/projects|runs|groups|artifacts|papers|views/{id}, POST
#: /v1/artifacts/{id}/move, POST /v1/projects/{id}/papers|references, POST
#: /v1/edges, POST /v1/runs/{id}/views, sub-notes. NOT here, on purpose:
#: `artifact add` (presign / PUT / confirm), `notes push` and `notes sync` (their
#: merge answers are not replayed), every delete, `artifact version-add`,
#: `experiment freeze`, `version create`, `project code *`, `experiment create`,
#: `experiment set` and `experiment move` (since light experiments R4 they write
#: through `/v1/projects/{P}/experiments[/{E}]`, which the server's allowlist does
#: not name yet: a replayed create would answer 409 for a write that landed),
#: `run end` (it may send
#: more than the one allowlisted PATCH), and `notes append` / `notes edit`: their
#: entity routes are allowlisted, but each READS the note and sends a document
#: built on what it read, so a retry after a write that landed builds a different
#: body -- refused as a reused key, or, after a stale-version 409 shifted the key
#: count, appended twice. Their `--team` routes (`/v1/team-note/apply/*`) are not
#: on the allowlist at all, and the daemon may not pass `--team` anyway
#: (`precheck`). A write that failed mid-way is reported,
#: and the model checks what landed before it tries again. Any other write is
#: never retried: the CLI cannot say that nothing was written.
IDEMPOTENT_COMMANDS = frozenset({
    "project create", "group create",
    "project set", "project tag", "project move",
    "run set", "run tag", "run move", "group set",
    "artifact set", "artifact move", "paper add", "paper update", "paper tag",
    "project reference add", "edge add", "views create", "views rename", "views update",
    "notes create", "notes rename",
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


def _classify(deps: Deps, command: str, cwd: Path, *, piped_input: bool = False) -> Any:
    """`shell.classify` with this session's folders, in `cwd`."""
    from probe.daemon import shell as sh

    return sh.classify(command, workdirs=deps.workdirs, home=deps.home, cwd=cwd, protected=deps.protected,
                       write_dirs=deps.write_dirs, piped_input=piped_input)


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
    """sha256 of a file's bytes; its size and mtime when it is over the upload
    limit (the pre-check refuses it anyway, and hashing it would stall the bite);
    "missing" when it cannot be read."""
    try:
        stat = path.stat()
        if not path.is_file():
            return "missing"
        if stat.st_size > precheck.MAX_UPLOAD_BYTES:
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
    end)`. `stdin`: the output of the probe command it is piped from."""
    from probe.daemon import shell as sh

    if verdict.refused:  # never a question, not even in bypass mode (`shell._Never`)
        deps.store.log_write(bite=deps.bite_id, op_id=_op_id(deps, ["sh", "-c", command]),
                             argv=["sh", "-c", scrub(command)], head="shell", status="not_run",
                             reason=verdict.reason)
        return f"not run: {verdict.reason} This is refused in every mode.", None
    auto = deps.bypass and deps.mode_known  # bypass mode: nothing is asked, so nothing is hidden
    if verdict.fixable and not auto:  # one flag from safe (`shell._Fix`): the daemon adds it, nobody is asked
        return f"not run: {verdict.reason}", None
    if verdict.safe:
        result = await sh.run(command, cwd=cwd, watch=lease_watch(deps), stdin=stdin)
        deps.store.log_lookup(bite=deps.bite_id, tool="shell", query=command, result=result.output[:2000])
        text = scrub(result.output)
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
    held = {"kind": "shell", "command": command, "cwd": str(cwd), "op_id": _op_id(deps, ["sh", "-c", command])}
    req = deps.board.hold(policy="shell.unsafe_command", session_id=deps.session_id, facts=facts, held=held,
                          bypass=deps.bypass, mode_known=deps.mode_known)
    if req.state == appr.DENIED:
        return _already_no(req), None
    if req.state == appr.APPROVED:
        result = await _run_shell_write(deps, command, held["op_id"], head="shell", request=req.id, cwd=cwd,
                                        stdin=stdin)
        return f"[{appr.AUTO} · {_shell_status(result)}]\n{scrub(result.output)}", result.exit_code
    deps.store.log_write(bite=deps.bite_id, op_id=held["op_id"], argv=["sh", "-c", command], head="shell",
                         status="held", reason=verdict.reason, request=req.id)
    return (f"held for the researcher (request {req.id}) - {verdict.reason.rstrip('.')}. It runs if they say yes - "
            "the answer shows up in a later bite."), None


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


def _renew_after_step(deps: Deps) -> None:
    """A finished part of a compound is progress: extend the lease, as a finished
    tool call does (`agent._renew_after`), so several slow probe commands in one
    call cannot outlive it -- but only a live lease this process holds, for a
    switch still at `daemon`, so a lapsed, released or taken one stays lost."""
    from probe.daemon import lease

    if deps.replay is None and lease.held(deps.session_id) and lease.session_state(deps.session_id) == "daemon":
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


def _in_working_folders(deps: Deps, folder: str) -> bool:
    """`folder` (logically and physically) inside a working folder or the
    session's own, never $HOME or above (as `shell.classify` counts them)."""
    from probe.daemon import shell as sh

    homes = {os.path.realpath(str(deps.home)), os.path.normpath(str(deps.home))}
    roots = [os.path.realpath(str(f)) for f in [*deps.workdirs, deps.cwd]]
    roots = [r for r in roots if not any(sh._inside(h, r) for h in homes)]
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


async def _run_shell_write(deps: Deps, command: str, op_id: str, *, head: str, request: str,
                           cwd: Path | None = None, stdin: bytes | None = None) -> Any:
    """An approved (bypass-mode) shell write, watched by the lease; logged, and
    logged as cancelled when the bite is cut short while it runs."""
    from probe.daemon import shell as sh

    try:
        result = await sh.run(command, cwd=cwd or deps.cwd, watch=lease_watch(deps), stdin=stdin)
    except asyncio.CancelledError:
        deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["sh", "-c", command], head=head,
                             status="cancelled", reason="the bite was cut short while it ran", request=request)
        raise
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["sh", "-c", command], head=head,
                         status="ran", reason=appr.AUTO, output=result.output, exit_code=result.exit_code,
                         request=request)
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
    req = deps.board.hold(policy="team_note.edit", session_id=deps.session_id, facts=facts, held=held,
                          bypass=deps.bypass, mode_known=deps.mode_known)
    if req.state == appr.DENIED:
        return _already_no(req)
    if req.state == appr.APPROVED:
        result = await _run_shell_write(deps, command, held["op_id"], head="team note", request=req.id)
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
    req = deps.board.hold(policy="team_note.edit", session_id=deps.session_id, facts=facts, held=held,
                          bypass=deps.bypass, mode_known=deps.mode_known)
    if req.state == appr.DENIED:
        return _already_no(req)
    if req.state == appr.APPROVED:
        return None
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="a team note change waits for the researcher", request=req.id)
    return f"held for the researcher (request {req.id}) - publishing the team note. It runs if they say yes."


def _document_path(deps: Deps, parsed: precheck.Parsed) -> Path | None:
    """The document `notes push` / `notes sync` upload though their argv never
    names it: the file this session checked out with the same flags, the team
    note. None for any other command, and for a push with no checkout known."""
    if parsed.path == "notes push":
        path = (deps.store.fact("checkouts", {}) or {}).get(_anchor_key(parsed))
        return Path(path) if path else None
    if parsed.path == "notes sync" and not parsed.params.get("pull_only"):
        return _team_note_paths(deps)[0]
    return None


def _document_block(deps: Deps, parsed: precheck.Parsed) -> precheck.Block | None:
    """D2: `notes push` and `notes sync` upload a document their argv never names.
    Resolve it (`_document_path`) and scan it like any file a command sends."""
    path = _document_path(deps, parsed)
    if parsed.path == "notes push" and path is None:
        return precheck.Block(precheck.new_block_id(),
                              "the daemon only knows a note's file from a `probe notes checkout` with the same "
                              "flags in this session", "document", argv=parsed.argv, overridable=False)
    return precheck.check_document(path, parsed) if path is not None else None


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
    Idempotency-Key, in `cwd` (default: the session's folder)."""
    here = cwd or deps.cwd
    stop = write_refusal(deps)
    if stop is not None:
        return stop, None
    if argv[:2] == ["daemon", "override"]:
        return await _request_override(deps, argv[2:], why=why)
    from probe.daemon import probe_api

    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError as exc:
        return f"not run: {exc}", None
    try:
        trash = await _server_has_trash(deps) if parsed.path in precheck.DELETES else False
    except probe_api.KeyRefused:
        return write_refusal(deps) or NO_LEASE, None
    block = precheck.check(parsed, cwd=here, trash=trash) or _document_block(deps, parsed)
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
                             status="cancelled", reason="the bite was cut short while it ran - it may have written "
                             "part of its work")
        raise
    code, output = result.code, result.output
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=parsed.path,
                         status=write_status(code, result.stderr), output=output, exit_code=code,
                         reason=_cap(why, 300) or None)
    if code == 0:
        _remember_note(deps, parsed, result.stdout)
    elif parsed.path not in IDEMPOTENT_COMMANDS:
        output += "\n[not retried: it may have written part of its work]"
    stop = write_refusal(deps) if deps.key_refused else None
    return f"[exit {code}]\n{_cap(scrub(output))}" + (f"\n{stop}" if stop else ""), result


_ANCHORS = ("project", "experiment", "run", "group", "artifact", "note")


def _anchor_key(parsed: precheck.Parsed) -> str:
    return "|".join(f"{k}={parsed.params.get(k)}" for k in _ANCHORS if parsed.params.get(k))


def _remember_note(deps: Deps, parsed: precheck.Parsed, stdout: str) -> None:
    """The file a `notes checkout` wrote (the `path` of the JSON it prints on
    stdout), for the `notes push` with the same flags (`_document_path`)."""
    if parsed.path != "notes checkout":
        return
    try:
        payload = json.loads(stdout or "")
    except ValueError:
        return
    path = payload.get("path") if isinstance(payload, dict) else None
    if isinstance(path, str) and os.path.isabs(path):
        checkouts = deps.store.fact("checkouts", {}) or {}
        checkouts[_anchor_key(parsed)] = path
        deps.store.set_fact("checkouts", checkouts)


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
    req = deps.board.hold(policy="delete.others_data", session_id=deps.session_id, facts=facts, held=held,
                          bypass=deps.bypass, mode_known=deps.mode_known)
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
    req = deps.board.hold(policy="delete.permanent", session_id=deps.session_id, facts=facts, held=held,
                          bypass=deps.bypass, mode_known=deps.mode_known)
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
    req = deps.board.hold(policy="check.override", session_id=deps.session_id, facts=facts, held=held,
                          bypass=deps.bypass, mode_known=deps.mode_known)
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
                              read_dirs=[skills] if skills is not None else [])
    if refused is not None:
        reason, never = refused
        if never:
            return f"not read: {reason} This is refused in every mode."
        if deps.reader or not (deps.bypass and deps.mode_known):
            return (f"not read: {reason} The reader reads only what a safe `cat` may read - `cat` through the "
                    "shell asks the researcher.")
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


#: The reader's ops: the session itself. `logbook` and `status` are the writer's record.
READER_SESSION_OPS: frozenset[SessionOp] = frozenset({SessionOp.OPEN, SessionOp.OUTLINE, SessionOp.SEARCH})
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
        rows = deps.store.search_logbook(query, limit=SEARCH_LIMIT)
        if not rows:
            return f"nothing in your logbook matches {query!r}"
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
        out.append(f"- {ev.event_id} · turn {ev.turn} · {ev.kind.value}{' · ' + ev.tool if ev.tool else ''}: {snippet}")
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
        text = _read_side(deps, ev.side_file) or text
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

