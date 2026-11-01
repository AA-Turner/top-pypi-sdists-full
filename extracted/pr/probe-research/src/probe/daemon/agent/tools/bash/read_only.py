"""decide whether a bash call only reads (the reader's and a task's limit)."""

from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.store.events import scrub


def _writes(argv: list[str]) -> bool:
    """Whether a `probe ...` command writes. One that cannot be parsed counts:
    it did not run, and nothing says it would only have read."""
    try:
        return precheck.parse(argv).owner != precheck.READ
    except precheck.ParseError:
        return True


#: The `probe` commands the daemon answers in its own process that only read
#: (`local_commands.answer`): run beside other reads. `probe daemon task` is one:
#: its child agent runs only reads (`agent.build_task_agent`).
LOCAL_READS = frozenset({("daemon", "session"), ("file", "preview"), ("mcp", "tools"), ("mcp", "call"),
                         ("daemon", "task")})


#: What a task's `bash` answers to anything that is not a read (NEW wording,
#: tests/fixtures/daemon_prompts/tools/task-replies.NEW.md; `agent.build_task_agent`
#: refuses it before it runs, and the shell and probe paths refuse it again).
TASK_READS_ONLY = "not run: a task only reads - {why}."
#: Why `reads_only` says a call does more than read, in its own words (NEW
#: wording, tests/fixtures/daemon_prompts/tools/task-replies.NEW.md); a command
#: the checker would not run at once says the checker's own reason.
NOT_A_READ = {"unparsed": "it can't be read as a probe command", "writes": "`probe {path}` writes",
              "unlisted": "`probe {path}` is not on the list of reads that only print",
              "file": "it writes a file"}


def _probe_reads(argv: list[str]) -> str | None:
    """None when a `probe ...` command only reads and prints (a local read, a help
    request, or one of READER_PROBE_READS); else why not. A READ-owned command
    off that list may still write a local file (`metrics plot`, `run reproduce
    --export`), so it does not count."""
    if tuple(argv[:2]) in LOCAL_READS:
        return None
    try:
        parsed = precheck.parse(argv)
    except precheck.ParseError:
        return NOT_A_READ["unparsed"]
    if parsed.help:
        return None
    if parsed.owner != precheck.READ:
        return NOT_A_READ["writes"].format(path=parsed.path)
    if parsed.path not in READER_PROBE_READS:
        return NOT_A_READ["unlisted"].format(path=parsed.path)
    return None


def _part_reads(verdict: Any) -> str | None:
    """None when a classified shell command (not a probe command) only reads."""
    if verdict.refused or not verdict.safe:
        return scrub(verdict.reason).rstrip(".")
    if verdict.note_target:
        return NOT_A_READ["file"]
    return None


def reads_only(deps: Deps, command: str) -> str | None:
    """None when a `bash` call only reads: nothing it runs writes a file or
    Probe, asks the researcher or holds a question -- what may run beside other
    calls (`agent.CallOrder`) and all a task may run (`agent.build_task_agent`).
    Else why not, in a few words. Proven from the same checks the call then
    runs through (`shell.classify`, `precheck`); a call it cannot read counts as
    a write. A compound's parts are read in the folder its `cd` parts lead to
    (a refused `cd` leaves later parts where they were: a read stays a read)."""
    command = command.strip()
    if not command:
        return None
    verdict = _classify(deps, command, deps.cwd)
    if verdict.probe_argv is not None:
        return _probe_reads(verdict.probe_argv)
    if verdict.steps is None:
        return _part_reads(verdict)
    cwd = deps.cwd
    for step in verdict.steps:
        if step.cd is not None:
            folder = os.path.normpath(os.path.join(str(cwd), step.cd))
            cwd = Path(folder) if os.path.isdir(folder) else cwd
            continue
        if step.probe_argv is not None:
            why = _probe_reads(step.probe_argv)
            if why is None and step.filter is not None:
                why = _part_reads(_classify(deps, step.filter, cwd, piped_input=True))
        else:
            why = _part_reads(_classify(deps, step.text, cwd))
        if why is not None:
            return why
    return None
from probe.daemon.agent.tools.bash.bash import READER_PROBE_READS  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.config import _classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
