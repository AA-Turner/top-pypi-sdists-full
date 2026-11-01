"""the shell tool: classify a command, run it at once, or hold it as a question (bypass mode and Jev aside)."""

from __future__ import annotations

import asyncio
import shlex
from pathlib import Path
from typing import Any, Callable

from probe.shared.mailbox import approvals as appr
from probe.daemon.store.jev import CUT_SHORT, FAILED_WHILE_RUNNING
from probe.daemon.store.events import scrub
from probe.tap_core import secrets


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
    if deps.task:
        # A task only reads: refused here, before any route a write could take (a
        # team-note heredoc is held before the shell checks run), whatever its own
        # `bash` decided. The shell and probe paths refuse it again where it would run.
        not_read = reads_only(deps, command)
        if not_read is not None:
            return TASK_READS_ONLY.format(why=not_read)
    verdict = _classify(deps, command, deps.cwd)
    if verdict.probe_argv is not None:
        return await run_probe_command(deps, verdict.probe_argv, why=why, stdin=verdict.probe_stdin)
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
            and not text.endswith(skills_are_read())):  # a skill read pointed at the skills wrote nothing
        deps.lost_writes += 1
    return text, code


async def _checked_shell_command(deps: Deps, command: str, verdict: Any, why: str, cwd: Path, *,
                                 stdin: bytes | None = None) -> tuple[str, int | None]:
    from probe.daemon import shell as sh

    if deps.task and (verdict.refused or verdict.note_target or not verdict.safe):
        # A task only reads, checked again where the command would run (its own
        # `bash` refused it already): refused, never asked, never run in bypass mode.
        return TASK_READS_ONLY.format(why=_part_reads(verdict)), None
    if deps.reader and not verdict.refused and (verdict.note_target or not verdict.safe):
        # The reader only reads: what is not a safe read is refused, never asked
        # (nobody answers the reader) and never run in bypass mode.
        return READER_READS_ONLY.format(why=scrub(verdict.reason or "it writes a file").rstrip(".")), None
    if verdict.refused:  # never a question, not even in bypass mode (`shell._Never`)
        if not deps.reader:
            deps.store.log_write(bite=deps.bite_id, op_id=_op_id(deps, shell_argv(command)),
                                 argv=shell_argv(scrub(command)), head="shell", status="not_run",
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
        if _logs_lookups(deps):  # the logbook is the writer's
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
            return f"not run: {verdict.reason.rstrip('.')}. {skills_are_read()}", None
    held = {"kind": "shell", "command": command, "cwd": str(cwd), "op_id": _op_id(deps, shell_argv(command))}
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
    deps.store.log_write(bite=deps.bite_id, op_id=held["op_id"], argv=shell_argv(command), head="shell",
                         status="held", reason=verdict.reason, request=req.id)
    return (f"held for the researcher (request {req.id}) - {verdict.reason.rstrip('.')}. It runs if they say yes - "
            "the answer shows up in a later bite."), None


#: How a shell guess at the skills' folders is answered (`_names_a_skill_folder`):
#: a read pointed at the read tool, never a write that was lost (`_shell_command`).
_SKILLS_ARE_READ = ("The skills are read with the read tool, by their path in the skills folder: "
                    "`read track-work/reference.md`.")
#: The same with the `bash` tool set: the skills folder, named (NEW wording,
#: tests/fixtures/daemon_prompts/tools/bash-replies.NEW.md).
SKILLS_ARE_CAT = "The skills are in the skills folder: `cat {skills}/track-work/reference.md`."
#: What the reader's `bash` answers to anything but a read (NEW wording, same file).
READER_READS_ONLY = "not run: the reader only reads - {why}."
#: The `probe` reads the reader's `bash` runs (besides the ones the daemon answers
#: itself: `probe daemon session`, `file preview`, `mcp call|tools`, `feedback
#: send`): a list, not "every read", so a read that grows an option that writes
#: (`run reproduce --export`) never reaches it unreviewed. Each prints only.
READER_PROBE_READS = frozenset({
    "project get", "project list", "project lineage", "project branches",
    "experiment get", "experiment list", "experiment lineage", "experiment edges", "experiment branch",
    "run get", "run list", "run metrics", "run series", "run inputs", "run upstream",
    "group get", "group list",
    "notes show", "notes find", "notes list", "notes team",
    "paper list", "paper find", "paper citations", "paper edges", "paper graph",
    "dataset list", "dataset show", "checkpoint list", "source list", "source show", "provenance",
    "artifact list", "artifact tree", "artifact versions",
    "metrics grouped", "metrics wide", "series latest", "span get", "span list", "trial get", "trial list",
    "views list", "views show", "session status",
})


def skills_are_read() -> str:
    from probe.daemon.agent import toolset

    if not toolset.bash_only():
        return _SKILLS_ARE_READ
    from probe.daemon.worker.bite.bite import skills_root

    return SKILLS_ARE_CAT.format(skills=skills_root() or "<skills folder>")


def _names_a_skill_folder(command: str) -> bool:
    """Whether a path in `command` runs through one of the shared skills' folders
    (`bite.SHARED_SKILLS`): a word with a `/` that has the skill's name as a whole
    part, glob stars aside (`~/.pi/agent/git/x/skills/track-work/reference.md`,
    `'*track-work/reference.md'`, `skills/edit-notes`). Never a bare word (`grep -rn
    track-work`), a `rev:path` or `host:path` word (`git show
    main:agent/skills/track-work/SKILL.md`), `my-track-work.md`, or a heredoc's text."""
    from probe.daemon.worker.bite.bite import SHARED_SKILLS

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
    from probe.daemon.session.session import _state_base, note_dirs

    guarded = [*deps.write_dirs, note_dirs()[-1], _state_base(), *deps.protected]
    return sh.names_writable(command, cwd=cwd, home=deps.home, folders=guarded)


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

    row = deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=shell_argv(command), head=head,
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
from probe.daemon.agent.tools.bash.jev import _jev_approval  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.bash.read_only import TASK_READS_ONLY, _part_reads, reads_only  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.bash.steps import _run_steps  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.config import _classify, _off_scrubbed  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.probe_cli import run_probe_command  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.process import _op_id  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.refusals import AUDIT_REFUSED, _WRITES_NOTES_TAIL, _script_facts, write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.team_note import _hold_team_note_write, _in_team_note  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, _already_no, _hold, _logs_lookups, shell_argv  # noqa: E402 -- pieces need each other; the front door loads this one first
