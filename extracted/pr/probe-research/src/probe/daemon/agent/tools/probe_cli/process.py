"""run the real probe CLI with the daemon's key: operation ids, bounded retries, reads answered in the host."""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from probe.shared.command_rules import command_rules as precheck
from probe.sdk.settings.key_refusal import KEY_REFUSED_LINE
from probe.sdk.values.write_outcome import was_queued

log = logging.getLogger("probe.daemon.tools")

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
#: "<METHOD> <path>: <cause>" (`sdk/delivery/transport/transport.py`) and printed by `cli.main` as
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
#: /v1/edges, POST /v1/runs/{id}/views, POST /v1/runs/{id}/uses (dataset use,
#: checkpoint use; an upsert either way), sub-notes (an experiment's under
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
#: with this key (`probe.shared.feedback.feedback.send_asked`), and anywhere else it only holds a
#: question on the local board, which `probe.shared.feedback.feedback.hold` never doubles.
IDEMPOTENT_COMMANDS = frozenset({
    "project create", "group create",
    "experiment create", "experiment set", "experiment move", "experiment fork",
    "project set", "project tag", "project move",
    "run set", "run tag", "run move", "group set",
    "artifact move", "paper add", "paper update", "paper tag",
    "project reference add", "edge add", "views create", "views rename", "views update",
    "notes create", "notes rename", "feedback send",
    "dataset use", "checkpoint use",
})


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
    Probe refusing the key sets `deps.key_refused` and `deps.stopped`.

    A read in `host_reads.MOVED` starts no process: the daemon host answers it
    with the CLI command's own body, under the same budget, lease watch and
    retries (`_in_host`). Every other read -- and one the host hands back --
    still spawns, and each read is counted by where it ran (`_count_read`)."""
    if deps.replay is not None:
        code, output = await deps.replay.run(argv, op_id)
        return ProbeResult(code, output)
    from probe.daemon.host import reads as host_reads

    env = _command_env(deps, op_id)
    where = host_reads.route(argv)
    deadline = _clock() + PROBE_TOTAL_S
    result: ProbeResult | None = None
    for attempt in range(PROBE_ATTEMPTS):
        if write_refusal(deps) is not None:
            if result is None:
                return ProbeResult(None, "", f"not run: {deps.stopped}")
            return ProbeResult(result.code, result.stdout,
                               f"{result.stderr.rstrip()}\nnot run again: {deps.stopped}".lstrip("\n"))
        budget = min(PROBE_TIMEOUT_S, deadline - _clock())
        result = None
        if where.call is not None:
            result = await _in_host(deps, where.call, env, budget)
            if result is None:  # handed back (`host_reads.start`): the CLI answers it
                where = host_reads.Route(read=where.call.path)
        if result is None:
            result = await _attempt(deps, argv, env, budget, cwd or deps.cwd)
        if attempt == 0:
            _count_read(deps, where)
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


def _command_env(deps: Deps, op_id: str) -> dict[str, str]:
    """What a `probe` command runs with: the session's key, URL and session
    (`deps.probe_env`), never this process's."""
    return {**_base_env(), **deps.probe_env, "PROBE_IDEMPOTENCY_KEY": op_id, "PROBE_ASYNC": "0",
            "NO_COLOR": "1", "COLUMNS": "200"}


async def read_in_host(deps: Deps, argv: list[str], op_id: str, timeout: float) -> ProbeResult | None:
    """A `probe` read plain code makes for the writer (its message's runs,
    `worker._read_runs`, swarm friction T18): answered in the daemon host
    (`host_reads`) within `timeout`, or by the bench's replay -- never a new
    process, never retried, counted apart from the model's (`PREFETCHED`). Probe
    refusing the key sets `deps.key_refused` and `deps.stopped`, as
    `run_probe_process` does. None: a read the host leaves to the CLI, or this
    process no longer holds the session (`deps.stopped`, `write_refusal`)."""
    if deps.replay is not None:
        code, output = await deps.replay.run(argv, op_id)
        return ProbeResult(code, output)
    if write_refusal(deps) is not None:
        return None
    from probe.daemon.host import reads as host_reads

    where = host_reads.route(argv)
    if where.call is None:
        return None
    result = await _in_host(deps, where.call, _command_env(deps, op_id), timeout)
    if result is not None:
        _count_read(deps, where, how=PREFETCHED)
        if _key_refused(result):
            _mark_key_refused(deps)
    return result


async def _attempt(deps: Deps, argv: list[str], env: dict[str, str], timeout: float, cwd: Path) -> ProbeResult:
    from probe.daemon.shell.runner import stop_group

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


async def _in_host(deps: Deps, call: Any, env: dict[str, str], timeout: float) -> ProbeResult | None:
    """`_attempt` for a read the daemon host answers itself (`host_reads`): on a
    thread of its own, waited for until its answer, `timeout`, or this process
    no longer holding the session -- each said as `_attempt` says it. None: the
    host hands it back, and the CLI answers it. A cancelled caller stops waiting
    at once; the read ends by its own (later) deadline."""
    from probe.daemon.host import reads as host_reads

    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout  # before the read's own, which is later (`host_reads.THREAD_GRACE_S`)
    answer = host_reads.start(call, env, timeout)
    if answer is None:
        return None
    while True:
        left = deadline - loop.time()
        if left <= 0:
            return ProbeResult(None, "", f"stopped after {timeout:.0f}s")
        done, _ = await asyncio.wait({answer}, timeout=min(LEASE_POLL_S, left))
        if done:
            got = answer.result()
            return None if got is None else ProbeResult(*got)
        if write_refusal(deps) is not None:
            return ProbeResult(None, "", f"stopped while it ran ({deps.stopped}) - it may have written part "
                                         "of its work")


#: The store fact counting this session's `probe` reads by where they ran:
#: `{"in_host": {"run get": n, ...}, "spawned": {...}, "prefetched": {...}}`. A
#: read not moved into the host yet is the `spawned` part (R38: the remainder
#: stays visible); `prefetched` (PREFETCHED) is plain code's own, in the host
#: (`read_in_host`), never the model's.
PROBE_READS_FACT = "probe_reads"
PREFETCHED = "prefetched"


def _count_read(deps: Deps, where: Any, *, how: str | None = None) -> None:
    """Count a read that ran under where it ran (`PROBE_READS_FACT`), or under
    `how`; a spawned one is also a log line naming the command. A count never
    fails the command."""
    if where.call is None and where.read is None:
        return  # not a read
    ran, path = ("in_host", where.call.path) if where.call is not None else ("spawned", where.read)
    how = how or ran
    if how == "spawned":
        log.info("probe read spawned a CLI process (not answered in the daemon host): probe %s", path)
    try:
        counts = deps.store.fact(PROBE_READS_FACT) or {}
        counts.setdefault(how, {})[path] = int(counts.get(how, {}).get(path, 0)) + 1
        deps.store.set_fact(PROBE_READS_FACT, counts)
    except Exception:  # noqa: BLE001 -- a count, never the command's failure
        log.debug("probe read count not kept", exc_info=True)


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
    `sdk/values/write_outcome.py`), else `ran`. Only `ran` is listed as recorded.
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


def _base_env() -> dict[str, str]:
    keep = ("PATH", "HOME", "LANG", "LC_ALL", "XDG_STATE_HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
            "PROBE_CONFIG_PATH", "PROBE_CONTEXT", "TMPDIR")
    return {k: os.environ[k] for k in keep if k in os.environ}
from probe.daemon.agent.tools.probe_cli.probe_cli import _document_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
