"""a probe command from the model through every pre-check, then the CLI; overrides and the post-move branch fact."""

from __future__ import annotations

import asyncio
import hashlib
import json
import shlex
import uuid
from pathlib import Path

from probe.shared.mailbox import approvals as appr
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.session import scope
from probe.daemon.store.jev import CUT_SHORT
from probe.daemon.store.events import scrub


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


async def _server_has_trash(deps: Deps) -> bool | None:
    """Does the server declare the trash? None: Probe could not be asked."""
    if deps.replay is not None:
        features = getattr(deps.replay, "server_features", None)
        return callable(features) and "trash" in features()
    from probe.daemon.session import probe_api

    try:
        return await probe_api.has_trash(deps.probe_env)
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        raise


async def run_probe_command(deps: Deps, argv: list[str], *, why: str = "", cwd: Path | None = None,
                            stdin: str | None = None) -> str:
    """A `probe ...` command from the model, through every check (`_probe_command`).
    `stdin`: what a quoted heredoc fed it (`shell.PROBE_STDIN_COMMANDS`)."""
    return (await _probe_command(deps, argv, why=why, cwd=cwd, stdin=stdin))[0]


#: What a probe command came to: the text the model reads, and the CLI's own
#: result when the command ran (None: blocked, held, refused, not run).
Outcome = tuple[str, "ProbeResult | None"]


async def _probe_command(deps: Deps, argv: list[str], *, why: str = "", cwd: Path | None = None,
                         stdin: str | None = None) -> Outcome:
    """The pre-checks, then the real CLI with the daemon's key and an
    Idempotency-Key, in `cwd` (default: the session's folder). A write that
    failed or was not run -- not asked about, and not stopped because this
    process may no longer write -- counts in `Deps.lost_writes`."""
    asked = deps.asked
    text, result = await _checked_probe_command(deps, argv, why=why, cwd=cwd, stdin=stdin)
    if ((result is None or result.code != 0) and deps.asked == asked and deps.stopped is None
            and _writes(argv)):
        deps.lost_writes += 1
    return text, result


async def _checked_probe_command(deps: Deps, argv: list[str], *, why: str = "", cwd: Path | None = None,
                                 stdin: str | None = None) -> Outcome:
    here = cwd or deps.cwd
    stop = write_refusal(deps)
    if stop is not None:
        return stop, None
    if deps.task:
        # A task only reads, checked again here (its own `bash` refused it already),
        # before the commands the daemon answers itself: `probe draft edit` is one.
        not_read = _probe_reads(argv)
        if not_read is not None:
            return TASK_READS_ONLY.format(why=not_read), None
    from probe.daemon.shell import local_commands

    local = await local_commands.answer(deps, argv, here, stdin)
    if local is not None:
        return local
    if argv[:2] == ["daemon", "override"]:
        if deps.reader:
            return READER_READS_ONLY.format(why="an override runs a write"), None
        if deps.audit:
            return f"{AUDIT_REFUSED} (an override is a question).", None
        return await _request_override(deps, argv[2:], why=why)
    from probe.daemon.session import probe_api

    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError as exc:
        return f"not run: {exc}", None
    if deps.audit:
        refusal = audit_probe_refusal(parsed)
        if refusal is not None:
            return refusal, None
    if deps.reader and not parsed.help and (parsed.owner != precheck.READ or parsed.path not in READER_PROBE_READS):
        why = f"`probe {parsed.path}` writes" if parsed.owner != precheck.READ else \
            f"`probe {parsed.path}` is not one of its reads"
        return READER_READS_ONLY.format(why=why), None
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
        if deps.reader:
            return block.message(), None
        deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *argv], head=parsed.path,
                             status="not_run", reason=f"block {block.id}: {block.why}")
        return block.message(), None
    if parsed.owner == precheck.READ:
        result = await _probe_process(deps, argv, op_id, here)
        if _logs_lookups(deps):  # the logbook is the writer's
            deps.store.log_lookup(bite=deps.bite_id, tool="probe", query=shlex.join(argv),
                                  result=result.output[:2000])
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
from probe.daemon.agent.tools.bash.bash import READER_PROBE_READS, READER_READS_ONLY  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.bash.read_only import TASK_READS_ONLY, _probe_reads, _writes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.drafts import _checkout_key, _remember_note  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.config import _config_block  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.deletes import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _hold_permanent_delete,
    _is_delete,
    _maybe_hold_delete,
    _own_link,
    _run_approved,
)
from probe.daemon.agent.tools.probe_cli.owed import LANE_SKIP, SUMMARY_COMMANDS, _mode_seen, note_summary_marks  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.process import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    IDEMPOTENT_COMMANDS,
    ProbeResult,
    _family,
    _mark_key_refused,
    _op_id,
    _probe_process,
    _sent_digest,
    write_status,
)
from probe.daemon.agent.tools.refusals import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    AUDIT_REFUSED,
    NO_LEASE,
    OWN_LINK_REASON,
    audit_probe_refusal,
    write_refusal,
)
from probe.daemon.agent.tools.team_note import _maybe_hold_team_note_sync, _team_note_paths  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, _already_no, _cap, _hold, _logs_lookups  # noqa: E402 -- pieces need each other; the front door loads this one first
