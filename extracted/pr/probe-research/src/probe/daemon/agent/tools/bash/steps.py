"""run a compound command with probe steps in order, as bash would (cd, &&, ||, pipes into filters)."""

from __future__ import annotations
import os
import shlex
from pathlib import Path
from typing import Any
from probe.daemon.store.events import scrub


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
    from probe.daemon.host import lease

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
from probe.daemon.agent.tools.bash.bash import _shell_command  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.bash.read_only import _writes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.config import _classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.probe_cli import _probe_command  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, _cap  # noqa: E402 -- pieces need each other; the front door loads this one first
