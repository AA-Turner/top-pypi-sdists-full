"""run one headless agent over the folder and show what it is doing (watchdog, timeout, activity)."""

from __future__ import annotations
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from probe.cli.imports.folder.agents.agents import AGENT_COPY, Agent, which_agent


#: How often the idle-deadline poller checks the gap since the last event. It is
#: the RESOLUTION of `timeout`, not a second deadline: a kill lands up to one
#: tick late, which against bounds measured in minutes (`UNIT_TIMEOUT_S` is 45
#: of them) is noise. Fixed rather than derived from `timeout` so one wedged
#: agent cannot spin a poller at whatever rate a caller's number implies.
_WATCHDOG_TICK_S = 1.0


def _launch_once(
    folder: Path,
    prompt: str,
    *,
    agent: Agent = Agent.CLAUDE,
    workdir: Path | None = None,
    tools: str | None = None,
    model: str | None = None,
    effort: str | None = None,
    heading: str = "",
    label: str = "",
    timeout: float | None = None,
    stream=None,
    raw_stream=None,
    progress: bool = True,
    total: int = 0,
    session_id: str | None = None,
    resume: str | None = None,
    paint_to=None,
    cancel_event: threading.Event | None = None,
    path_prepend: str | None = None,
    state: Activity,
) -> tuple[bool, str]:
    """Run one headless agent over `folder`, showing what it is doing.

    `state` is filled as the run goes (`fold_event`): `started` once the
    process is registered, then its usage, work and any refusal.

    ONE self-updating line, not the transcript. A raw agent transcript is
    thousands of lines nobody reads, and the previous version showed neither --
    a bare `claude -p` emits nothing until it exits, so a long import was
    indistinguishable from a hang. What a watcher actually needs is that it is
    alive, roughly how far along it is, and what it is touching right now.

    `workdir` is the agent's scratch directory and the only place it may write;
    `folder` stays read-only. See CONFINEMENT.

    `tools`, `model` and `effort` override the allowlist, the model and the
    reasoning effort for one launch (`agent_argv`). Absent, the importer's
    launch is byte-for-byte what it always was.

    `timeout` is an IDLE DEADLINE for claude/codex: the longest this may go
    WITHOUT AN EVENT, not the longest it may run. That is what the numbers have
    always meant -- `backfill_run.UNIT_TIMEOUT_S`'s own docstring reads "a unit
    that has not produced an event in this long is wedged" -- and a wall clock
    in its place would kill a 46-minute import that was healthy the whole way.

    What it did NOT used to be is enforceable. It bounded only the `wait` AFTER
    stdout reached EOF, and `for line in proc.stdout` blocks forever on an
    agent that neither speaks nor exits, so `proc.wait(timeout=)` on the next
    line was never reached: the one case the deadline exists for was the one
    case it could not fire in. A single poller thread now compares the clock
    against the last event stamped by the read loop and kills the process group
    when the gap exceeds the bound. A wedged agent is bounded just as tightly
    as a wall clock would bound it -- it emits nothing, so its last event stays
    at launch -- and the caller gets `False` with a message naming the bound.

    pi keeps a true WALL CLOCK (`communicate(timeout=)`) for the reason the
    idle clock cannot apply to it: `--mode text` is not an event stream, so
    there is nothing to stamp. Its whole run is one bounded call.

    `None` still means unbounded, and costs no thread: a caller that wants a
    deadline says so.

    `raw_stream` is where the agent's VERBATIM stream-json goes under
    `progress=False`; it defaults to `stream`, which is what every existing
    caller wants. The digest lane sends it somewhere that keeps nothing: that
    JSON quotes the conversation being summarized, and echoing it to stdout
    made `probe backfill > import.log` a durable second copy of every session
    -- next to a digester that unlinks its rendered view for exactly that
    reason. Digests still print the two liveness lines (start, finish with
    elapsed) to `stream`, because an agent that says nothing for five minutes
    is indistinguishable from a hang.

    `heading` and `paint_to` decide where that line goes. Alone, the agent draws
    its OWN centred page -- title, blank row, live line -- because appended
    under whatever the picker left on screen it reads as a different program's
    output leaking into the wizard. `paint_to` hands the row to a caller running
    several agents at once, which owns the screen instead (see `tui.Board`).

    `cancel_event` closes the gap between cancelling a worker pool and a
    worker registering its child: a late spawn stops before reading stdout.

    `total` is the census, so the counter reads against the denominator the
    reconcile will check. The tail is returned so the caller can pull the
    agent's JSON summary out of it.
    """
    from ... import jobs as import_jobs

    if cancel_event is not None and cancel_event.is_set():
        return False, "agent cancelled"
    binary = which_agent(agent)
    if not binary:
        name = AGENT_COPY[agent][0]
        # "another", not "the other": there are three now, and which alternatives
        # exist depends on which lane is asking.
        return False, f"`{agent.value}` is not on PATH — install {name}, or pick another agent"
    if workdir is not None and agent is Agent.CLAUDE and unruleable(folder):
        # Refusing beats running unconfined. The rule is the only thing keeping
        # the agent out of the folder, and an unparseable one denies nothing
        # while looking exactly like a working configuration.
        return False, (
            f"{folder} has a parenthesis in its path, which cannot be written as a "
            "Claude permission rule — the folder could not be protected from writes. "
            "Re-run with Codex, whose sandbox needs no path pattern."
        )

    out = stream if stream is not None else sys.stdout

    if agent is Agent.PI:
        return _run_pi(
            binary,
            folder,
            prompt,
            workdir=workdir,
            tools=tools,
            model=model,
            timeout=timeout,
            label=label,
            out=out,
            paint_to=paint_to,
            cancel_event=cancel_event,
        )

    # Defaults to `out`, so every caller that predates the split behaves
    # exactly as it did; only the digest lane sends it elsewhere.
    raw_out = raw_stream if raw_stream is not None else out

    live = progress and hasattr(out, "isatty") and out.isatty()
    started = time.monotonic()
    tail: list[str] = []
    tag = f"{label} " if label else ""
    board = None

    def note(text: str) -> None:
        """The quiet run's two lines. Same shape and same destinations as
        `_run_pi`'s, because it is the same problem: with the stream silenced
        there is nothing else to prove the agent is alive."""
        if paint_to is not None:
            paint_to(text)
            return
        out.write(f"  {text}\n")
        out.flush()

    def paint() -> None:
        if not live:
            return
        text = state.line(time.monotonic() - started)
        if paint_to is not None:
            paint_to(text)
        elif board is not None:
            board.update(0, text)

    # One live screen component for both standalone and concurrent agents.
    # A caller-owned painter already has its board; opening another would
    # erase the other agents' rows.
    if live and paint_to is None:
        from probe.cli.wizard import terminal as tui

        board = tui.Board(heading, [""], out=out)
        board.open()

    stop = threading.Event()

    def tick() -> None:
        # The spinner has to advance on its own: an agent can think for a minute
        # between events, and a frozen spinner is the thing we set out to fix.
        while not stop.wait(0.12):
            state.ticks += 1
            paint()

    try:
        # THE PROMPT, as a file the child reads at its own pace. Not
        # `stdin=PIPE` + `proc.communicate()`: we hold stdout as a pipe and do
        # not start reading it until below, so a prompt past the pipe buffer
        # (64KB here, against prompts of 300KB) deadlocks -- we block writing
        # while the child blocks writing its event stream. An unnamed temp file
        # needs no writer, no thread, and no cleanup path: it is unlinked on
        # close, including when the exec fails.
        prompt_file = tempfile.TemporaryFile()
        prompt_file.write(prompt.encode("utf-8", "replace"))
        prompt_file.flush()
        prompt_file.seek(0)
    except OSError as exc:
        if board is not None:
            board.close(erase=True)
        return False, f"could not stage the prompt: {exc}"
    try:
        argv = agent_argv(
            agent,
            binary,
            folder,
            workdir=workdir,
            tools=tools,
            model=model,
            session_id=session_id,
            resume=resume,
            effort=effort,
        )
        if cancel_event is not None and cancel_event.is_set():
            if board is not None:
                board.close(erase=True)
            return False, "agent cancelled"
        proc = import_jobs.spawn_child(
            argv,
            cwd=str(workdir if workdir is not None else folder),
            stdin=prompt_file,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=_backfill_agent_env(path_prepend),
            # ITS OWN PROCESS GROUP, so the whole tree can be killed at once.
            # An agent is not one process: it starts MCP servers, subagents and
            # shells of its own, and `proc.kill()` reaps only the direct child
            # -- leaving the grandchildren running, reading the folder, with no
            # parent left to stop them. That is what survived a Ctrl-C and kept
            # a 106,007-file import going after the wizard had said "Cancelled".
            start_new_session=True,
        )
    except (OSError, subprocess.SubprocessError, ArgvTooLargeError) as exc:
        if board is not None:
            board.close(erase=True)
        return False, str(exc)
    finally:
        # The child has its own dup of the fd from here on, so ours is done.
        # Closing it is also what unlinks the file on the failure path.
        prompt_file.close()
    if not _register_agent(proc, cancel_event):
        if board is not None:
            board.close(erase=True)
        return False, "agent cancelled"
    state.started = True

    ticker = threading.Thread(target=tick, daemon=True)
    if live:
        ticker.start()

    # THE IDLE DEADLINE. See the `timeout` paragraph above: the bound is time
    # WITHOUT AN EVENT, so the read loop stamps `last_event` and this thread
    # only watches the gap. Killing the GROUP closes the pipe, which is what
    # ends a loop that would otherwise block forever.
    #
    # ONE POLLER on a fixed tick, never a timer re-armed per line: an agent
    # emits thousands of events over an import, and a thread per event is a
    # thread pool nobody asked for. The tick is the resolution of the deadline,
    # and a second's slack on a bound measured in minutes costs nothing.
    expired = threading.Event()
    stop_watch = threading.Event()
    watchdog = None
    last_event = time.monotonic()
    if timeout is not None:

        def _watch() -> None:
            while not stop_watch.wait(_WATCHDOG_TICK_S):
                if time.monotonic() - last_event > timeout:
                    expired.set()
                    _kill_tree(proc)
                    return

        watchdog = threading.Thread(target=_watch, daemon=True)
        watchdog.start()

    if not progress:
        # The label already names the work and the session; repeating the agent
        # after it reads as two subjects in one sentence.
        note(f"{tag}reading the view")

    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            # THE STAMP the idle deadline is measured from. Every line counts,
            # not only the ones `fold_event` finds interesting: an agent
            # emitting anything at all is an agent that has not wedged.
            last_event = time.monotonic()
            tail.append(line.rstrip("\n"))
            del tail[:-40]
            changed = fold_event(line, state)
            if not progress:
                # RAW TRANSCRIPT, and this has to be tested FIRST. Underneath
                # the `changed` branch it was unreachable for anything worth
                # reading: `fold_event` returns True for every tool call,
                # command and message, so `progress=False` handed back a
                # mangled hybrid -- counter lines where the interesting events
                # should have been, raw JSON only for the lines nobody wanted.
                #
                # `raw_out`, not `out`: this JSON quotes the conversation, and
                # the digest lane sends it to a sink that keeps nothing while
                # its status line still reaches the reader.
                raw_out.write(line)
                raw_out.flush()
            elif live:
                if changed:
                    paint()
            elif changed:
                # No TTY (a pipe, a CI log): one plain line per step. Rewriting
                # with \r into a log file produces an unreadable single line.
                #
                # `done`, not `uploaded`. The live line was moved onto files
                # READ when the upload counter turned out to be permanently
                # zero, and this branch -- the one a pipe, a CI log or `nohup`
                # takes -- was left behind counting the dead field. So the fix
                # was invisible to exactly the runs nobody is watching, which
                # are the runs that get read later to find out what happened.
                #
                # LABELLED, because there is no board out here. `run_units`
                # only builds one when interactive, so an unattended import
                # writes up to `concurrency` units into ONE stream -- and
                # without a name the only thing telling `3/704` from `5/704`
                # is a denominator two units can easily share.
                count = f"{state.done}/{state.total} · " if state.total else ""
                out.write(f"  {tag}{count}{state.doing}\n")
                out.flush()
        # UNBOUNDED ON PURPOSE, and only safe because of the poller above. EOF
        # is not exit: a process can close stdout and linger. That is silence,
        # which is exactly what the idle deadline measures -- the poller is
        # still armed here and kills the tree, which is what releases this
        # wait. A `timeout=` here as well would be a second deadline with
        # different semantics and its own message for the same condition.
        code = proc.wait()
    except KeyboardInterrupt:
        # Ctrl-C should stop the agent, not orphan it holding the folder.
        # EVERY agent, not just this one: under `run_units` there are several,
        # and one thread taking the interrupt must not leave its siblings
        # running -- see `stop_all`.
        stop_all()
        raise
    finally:
        # Always, and BEFORE anything else in here. An abandoned poller is a
        # live thread holding a reference to a reaped pid, and a lane of 200
        # digests would leave 200 of them; joined rather than merely signalled
        # so "the run is over" also means "nothing is still about to kill
        # something". The join is prompt -- `Event.wait` returns the moment the
        # event is set, it does not sit out the rest of its tick.
        stop_watch.set()
        if watchdog is not None:
            watchdog.join(timeout=5.0)
        _release_agent(proc)
        # Always: an abandoned ticker keeps repainting over whatever the wizard
        # prints next, and the status line must not outlive the run either way.
        stop.set()
        if live:
            ticker.join(timeout=1.0)
        if board is not None:
            board.close(erase=True)

    elapsed = time.monotonic() - started
    if expired.is_set():
        # NAME THE BOUND AND WHICH CLOCK RAN OUT. "did not finish within 300s"
        # would be false of a run that was talking the whole time and is
        # unactionable besides: what happened is SILENCE, and the fix for a
        # deadline set too tight differs from the fix for a wedged binary.
        # Whatever it managed to say before going quiet is usually the answer.
        partial = "\n".join(tail[-5:])
        if not progress:
            note(f"{tag}stopped after {timeout:g}s with no output")
        return False, (
            f"{AGENT_COPY[agent][0]} produced no output for {timeout:g}s and was stopped"
            + (f" — last output: {partial}" if partial else ", having printed nothing")
        )
    ok = code == 0
    if not progress:
        note(f"{tag}{'finished' if ok else 'failed'} in {elapsed:.1f}s")
    return ok, "\n".join(tail)
from probe.cli.imports.folder.agents.activity import Activity, fold_event  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.argv import ArgvTooLargeError, agent_argv  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.digest import _run_pi  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.process import _kill_tree, _register_agent, _release_agent, stop_all  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.shell_tools import _backfill_agent_env  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.shared.harness.harnesses.claude_code.headless import unruleable  # noqa: E402 -- an import cycle: bound once this module's names exist
