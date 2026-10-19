"""The `probe` commands the daemon answers in its own process (the `bash` tool set).

Every `probe ...` the daemon's shell is given goes to `tools._checked_probe_command`
first; these few never reach a CLI process (like `probe daemon override`):

    probe daemon session <op> ...   the session store this worker holds open
                                    (`tools.session`: open, outline, search,
                                    logbook, status; the reader's four)
    probe file preview <path>       a data file's preview (`reader.render`), by
                                    the read tool's rules (`tools.read_check`)
    probe draft edit <path>         a draft changed in place (`probe.drafts`),
                                    its change on stdin from a quoted heredoc
    probe mcp tools [tool ...]      the Probe MCP, over the daemon's own key and
    probe mcp call <tool> '<json>'  the connection its agents loaded natively
                                    before (the reader names its session; the
                                    audit refuses the open web)
    probe feedback send "<text>"    the READER's: held for the researcher as the
                                    reader's feedback (`probe.feedback.hold`); the
                                    writer's goes to the CLI as before
    probe daemon task "<text>"      a child agent for one long read, in a context
    probe daemon task <<'EOF'       of its own (`agent.run_task`); the text on
                                    stdin from a quoted heredoc

Each answers like a probe read: `[exit N]` then the text, scrubbed and capped,
so a pipe after it (`probe mcp call ... | jq ...`) reads its stdout.
"""

from __future__ import annotations

import logging
import shlex
from pathlib import Path
from typing import Any

from probe.daemon import toolset
from probe.daemon.store import scrub

log = logging.getLogger("probe.daemon.tools")

#: How `probe daemon session` is used (NEW wording,
#: tests/fixtures/daemon_prompts/tools/bash-replies.NEW.md).
SESSION_USAGE = ("usage: probe daemon session open <event_id> [--page N] | open --turn N [--page N] | outline "
                 "[--page N] | search \"<words>\" [--kind K] [--turn-from N] [--turn-to N] | logbook \"<words>\" | "
                 "status")
READER_SESSION_USAGE = ("usage: probe daemon session open <event_id> [--page N] | open --turn N [--page N] | "
                        "outline [--page N] | search \"<words>\" [--kind K] [--turn-from N] [--turn-to N] | logbook "
                        "\"<words>\"")
#: Its options, as the `session` tool's arguments (`tools.SESSION_OPTIONS`).
_SESSION_FLAGS = {"--page": "page", "--turn": "turn", "--kind": "kind", "--turn-from": "turn_from",
                  "--turn-to": "turn_to"}
_INTS = frozenset({"page", "turn", "turn_from", "turn_to"})
#: `probe file preview`'s refusal outside what it may read (NEW wording, same file).
PREVIEW_REFUSED = "not read: {reason} `probe file preview` reads only what a safe `cat` may read."


#: How `probe daemon task` is used, and what it answers when it cannot run
#: (NEW wording, tests/fixtures/daemon_prompts/tools/task-replies.NEW.md).
TASK_USAGE = "usage: probe daemon task \"<question>\" | probe daemon task <<'EOF', the task, then a line reading EOF"
TASK_OFF = "not run: tasks are off; do the reads yourself."
TASK_NESTED = "not run: a task can't start a task; do the reads yourself."
TASK_BOTH = "not run: give the task as words or a heredoc, not both. {usage}"


#: The most an answer here shows: the read tool's (`reader.MAX_CHARS`).
ANSWER_CHARS = 30_000


def _ok(text: str, code: int = 0):
    """`[exit N]` and the text capped for the model; the command's stdout -- what a
    filter after it in a pipe reads (`probe mcp call ... | jq`) -- is the whole
    scrubbed text, never the capped one (a cut in the middle is not JSON)."""
    from probe.daemon.tools import ProbeResult, _cap

    whole = scrub(text)
    shown = _cap(whole, ANSWER_CHARS)
    return f"[exit {code}]\n{shown}", ProbeResult(code, whole + ("\n" if whole and not whole.endswith("\n") else ""))


async def answer(deps: Any, argv: list[str], here: Path, stdin: str | None):
    """The outcome of a command answered here, or None for any other."""
    if argv[:2] == ["daemon", "session"]:
        return _session(deps, argv[2:])
    if argv[:2] == ["file", "preview"]:
        return await _preview(deps, argv[2:], here)
    if argv[:2] == ["draft", "edit"]:
        return await _draft_edit(deps, argv[2:], here, stdin)
    if argv[:2] in (["mcp", "call"], ["mcp", "tools"]) and toolset.bash_only():
        return await _mcp(deps, argv)
    if argv[:2] == ["feedback", "send"] and deps.reader:
        return _reader_feedback(deps, argv[2:])
    if argv[:2] == ["daemon", "task"]:
        return await _task(deps, argv[2:], stdin)
    return None


# -- probe daemon task ---------------------------------------------------------------


async def _task(deps: Any, args: list[str], stdin: str | None):
    """A task (`agent.run_task`, through `Deps.task_runner`): its text is the
    words after `task`, or a quoted heredoc's (then no words). Never from a task,
    and only while tasks are on (`toolset.tasks`)."""
    if deps.task:
        return _ok(TASK_NESTED, 1)
    if not toolset.tasks() or deps.task_runner is None:
        return _ok(TASK_OFF, 1)
    words = [a for a in args if a != "--"]
    if words and words[0] in ("-h", "--help", "help") and len(words) == 1 and stdin is None:
        return _ok(TASK_USAGE)
    if stdin is not None and words:
        return _ok(TASK_BOTH.format(usage=TASK_USAGE), 2)
    text = (stdin if stdin is not None else " ".join(words)).strip()
    if not text:
        return _ok(TASK_USAGE, 2)
    answer, code = await deps.task_runner(text)
    return _ok(answer, code)


# -- probe daemon session ------------------------------------------------------


def _session(deps: Any, args: list[str]):
    from probe.daemon import tools

    usage = READER_SESSION_USAGE if deps.reader else SESSION_USAGE
    if not args or args[0] in ("-h", "--help", "help"):
        return _ok(usage, 0 if args else 2)
    op, rest = args[0], args[1:]
    given: dict[str, Any] = {}
    words: list[str] = []
    k = 0
    while k < len(rest):
        word = rest[k]
        name, eq, value = word.partition("=")
        if name in _SESSION_FLAGS:
            if not eq:
                if k + 1 >= len(rest):
                    return _ok(f"not run: {name} needs a value. {usage}", 2)
                value = rest[k + 1]
                k += 1
            key = _SESSION_FLAGS[name]
            if key in _INTS:
                try:
                    given[key] = int(value)
                except ValueError:
                    return _ok(f"not run: {name} takes a number, not {value!r}. {usage}", 2)
            else:
                given[key] = value
        elif word.startswith("--"):
            return _ok(f"not run: {word} is not an option. {usage}", 2)
        else:
            words.append(word)
        k += 1
    if op == "open":
        if len(words) > 1:
            return _ok(f"not run: open takes one event id. {usage}", 2)
        if words:
            given["event_id"] = words[0]
    elif op in ("search", "logbook"):
        if words:
            given["query"] = " ".join(words)
    elif words:
        return _ok(f"not run: {op} takes no words ({' '.join(words)!r}). {usage}", 2)
    text = tools.session(deps, op, status=deps.record_status, **given)
    refused = text.startswith(("not run", "give an", "no event", "no turn"))
    return _ok(text, 1 if refused else 0)


# -- probe file preview ----------------------------------------------------------


async def _preview(deps: Any, args: list[str], here: Path):
    import asyncio

    from probe.daemon import reader as reader_mod
    from probe.daemon import tools

    paths = [a for a in args if not a.startswith("-")]
    if len(paths) != 1 or len(args) != 1:
        return _ok("usage: probe file preview <path>", 2)
    path = paths[0]
    refused, full = tools.read_check(deps, path, here)
    if refused is not None:
        return _ok(refused, 1)
    text = scrub(await asyncio.to_thread(reader_mod.render, full, None, None))
    if tools._logs_lookups(deps):
        deps.store.log_lookup(bite=deps.bite_id, tool="probe", query=f"file preview {path}", result=text[:2000])
    return _ok(text, 1 if text.startswith("not read:") else 0)


# -- probe draft edit --------------------------------------------------------------


async def _draft_edit(deps: Any, args: list[str], here: Path, stdin: str | None):
    import asyncio

    from probe import drafts

    if deps.reader:
        from probe.daemon.tools import READER_READS_ONLY

        return READER_READS_ONLY.format(why="`probe draft edit` writes"), None
    if deps.audit:
        from probe.daemon.tools import AUDIT_REFUSED

        return f"{AUDIT_REFUSED} (the audit edits only its copy of the team note).", None
    paths = [a for a in args if not a.startswith("-")]
    if len(paths) != 1 or len(args) != 1:
        return _ok(f"usage: probe draft edit <path>, the change on stdin:\n{drafts.EDIT_FORMAT}", 2)
    code, text = await asyncio.to_thread(drafts.edit, paths[0], stdin, here)
    deps.store.log_lookup(bite=deps.bite_id, tool="edit", query=paths[0], result=scrub(text)[:2000])
    return _ok(text, code)


# -- probe mcp tools | call ---------------------------------------------------------

#: The Probe MCP's instructions per MCP address and agent (`mcp_guide`):
#: (text, when asked, whether the answer came).
_GUIDE: dict[str, tuple[str, float, bool]] = {}
#: A failed fetch is asked again after this many seconds.
GUIDE_RETRY_S = 600.0


def _clock() -> float:
    import time

    return time.monotonic()


def _stops(exc: BaseException) -> bool:
    """Is `exc` (or any exception an exception group holds) a cancel or an exit,
    which must go on, never be read as the MCP failing?"""
    import asyncio

    if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt, SystemExit, GeneratorExit)):
        return True
    return any(_stops(inner) for inner in getattr(exc, "exceptions", None) or ())
#: The heading over them (the CLI's own, `cli.mcp_bridge.render_tools`).
GUIDE_HEADING = "# How to read Probe (the Probe MCP's instructions)"


def _target(deps: Any):
    """The daemon's MCP connection: its key, and for the reader the watched
    session (as `agent.build_reader_agent`'s native connection named it)."""
    from probe import __version__
    from probe.cli import mcp_bridge
    from probe.client_headers import client_version_headers
    from probe.sdk.config import mcp_url

    key = deps.probe_env.get("PROBE_TOKEN", "")
    url = mcp_url(deps.probe_env.get("PROBE_BASE_URL", ""))
    if not key or not url:
        raise mcp_bridge.BridgeError("the daemon has no Probe MCP here (no key, or no MCP for its Probe)")
    headers = {"Authorization": f"Bearer {key}", **client_version_headers("cli", __version__)}
    if deps.reader:
        from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER, HIDE_SESSION_WORK_HEADER

        headers.update({AGENT_HEADER: deps.harness, AGENT_SESSION_HEADER: deps.session_id,
                        HIDE_SESSION_WORK_HEADER: "1"})
    return mcp_bridge.Target(url=url, headers=headers)


async def mcp_guide(deps: Any) -> str:
    """The Probe MCP's instructions under GUIDE_HEADING, as the native MCP put
    them in the agents' instructions; "" when it cannot be reached (logged)."""
    import anyio

    from probe.cli import mcp_bridge

    try:
        where = _target(deps)
    except Exception as exc:  # noqa: BLE001
        log.warning("no Probe MCP instructions: %s", exc)
        return ""
    cache = f"{where.url} {deps.reader}"
    hit = _GUIDE.get(cache)
    now = _clock()
    if hit is None or (not hit[2] and now - hit[1] >= GUIDE_RETRY_S):
        # Asked once, and again only GUIDE_RETRY_S after a failure: a down MCP costs
        # one wait per retry period (not up to TOTAL_TIMEOUT_S every model round), and
        # the instructions change at most once a period (each change rewrites the
        # cached prompt prefix). While a fetch is under way, others see none.
        _GUIDE[cache] = ("", now, False)
        try:
            with anyio.fail_after(mcp_bridge.TOTAL_TIMEOUT_S):
                async with mcp_bridge._session(where) as (_session, init):
                    _GUIDE[cache] = ((init.instructions or "").strip(), now, True)
        except BaseException as exc:  # noqa: BLE001 -- task groups wrap the cause
            if _stops(exc):
                # The run was cut short (a cancel, also inside a task group's
                # exception group), not the MCP: ask again next time.
                if hit is None:
                    del _GUIDE[cache]
                else:
                    _GUIDE[cache] = hit
                raise
            log.warning("no Probe MCP instructions: %s", mcp_bridge._describe(exc))
            return ""
    text = _GUIDE[cache][0]
    return f"{GUIDE_HEADING}\n\n{text}" if text else ""


async def _mcp(deps: Any, argv: list[str]):
    import anyio

    from probe.cli import mcp_bridge

    try:
        where = _target(deps)
    except mcp_bridge.BridgeError as exc:
        return _ok(f"error: {exc}", 1)
    try:
        with anyio.fail_after(mcp_bridge.TOTAL_TIMEOUT_S):
            if argv[1] == "tools":
                names = [a for a in argv[2:] if not a.startswith("-")]
                instructions, listed = await mcp_bridge._list(where)
                try:
                    text = mcp_bridge.render_tools(instructions, listed, names)
                except KeyError as exc:
                    served = ", ".join(t.name for t in listed)
                    return _ok(f"error: the Probe MCP serves no tool {exc.args[0]} (it serves: {served})", 1)
                return _ok(text)
            if len(argv) < 3 or argv[2].startswith("-"):
                return _ok("usage: probe mcp call <tool> '<json arguments>'", 2)
            tool = argv[2]
            if deps.audit:
                from probe.daemon.agent import AUDIT_REFUSED_TOOLS, AUDIT_WEB_REFUSED

                if tool in AUDIT_REFUSED_TOOLS:
                    return AUDIT_WEB_REFUSED, None
            try:
                payload = mcp_bridge.parse_arguments(" ".join(argv[3:]) if len(argv) > 3 else None)
            except ValueError as exc:
                return _ok(f"error: {exc}", 2)
            if deps.reader and tool in ("search", "search_knowledge"):
                # The watched session is never the team's prior work (`agent.ExcludeWatchedSession`).
                payload = {**payload, "exclude_session": deps.session_id}
            result = await mcp_bridge._call(where, tool, payload)
    except BaseException as exc:  # noqa: BLE001 -- task groups wrap the cause
        if isinstance(exc, (KeyboardInterrupt, SystemExit, GeneratorExit)):
            raise
        import asyncio

        if isinstance(exc, asyncio.CancelledError):
            raise
        return _ok(f"error: {mcp_bridge._describe(exc)}", 1)
    text = mcp_bridge.result_text(result)
    from probe.daemon.tools import _logs_lookups

    if _logs_lookups(deps):
        deps.store.log_lookup(bite=deps.bite_id, tool="probe", query=shlex.join(argv)[:500], result=text[:2000])
    if result.isError:
        return _ok(text or f"error: {tool} failed", 1)
    return _ok(text)


# -- probe feedback send (the reader) -------------------------------------------------


def _reader_feedback(deps: Any, args: list[str]):
    from probe import feedback as fb
    from probe.daemon import approvals as appr
    from probe.daemon.agent import READER_FEEDBACK_HELD

    text = " ".join(a for a in args if a != "--")
    try:  # an empty text is refused by the hold itself, in its own words (as the reader's tool was)
        req = fb.hold(text, session_id=deps.session_id, source=fb.Source.DAEMON_READER, harness=deps.harness)
    except fb.Refused as exc:
        return _ok(f"not sent: {exc}", 1)
    if req.state == appr.DENIED:
        return _ok(f"not sent: the researcher already said no to this feedback ({req.question.header}).", 1)
    return _ok(READER_FEEDBACK_HELD.format(header=req.question.header))
