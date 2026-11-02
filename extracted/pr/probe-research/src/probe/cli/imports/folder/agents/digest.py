"""one headless digest run (pi today): launch through the process registry, feed the prompt on stdin, wait with a deadline, report the tail."""

from __future__ import annotations
import subprocess
import threading
import time
from pathlib import Path

#: The default bound for a pi launch (`_run_pi`): far tighter than the
#: import's deadlines (`backfill_run.UNIT_TIMEOUT_S` 45 min,
#: `CLASSIFY_TIMEOUT_S` 90 min), which bound an open-ended traversal of
#: somebody's drive. Sized for the retired claims draft, one bounded file in
#: and one small file out.
DIGEST_TIMEOUT_S = 300.0

#: How much of pi's output is kept. This string is the entire record of a failed
#: digest, and an unbounded one puts a runaway run's megabytes into a lane report
#: somebody reads.
_PI_TAIL_CHARS = 2000


def _pi_tail(*chunks) -> str:
    """The last `_PI_TAIL_CHARS` of pi's output, decoded defensively.

    BYTES ARE A REAL CASE here, not paranoia. `TimeoutExpired.stdout` carries
    the raw chunks read before the deadline -- the process decoder never saw
    them -- so it is `bytes` even on a `Popen` opened with an `encoding`.
    Formatting that into a message gives `b'...'` with the escapes visible;
    calling `.decode` unconditionally raises on the normal path, where it is
    already `str`. Both, or this helper is a crash in the error path.
    """
    text = ""
    for chunk in chunks:
        if not chunk:
            continue
        text += chunk.decode("utf-8", "replace") if isinstance(chunk, bytes) else chunk
    return text[-_PI_TAIL_CHARS:]


def _run_pi(
    binary: str,
    folder: Path,
    prompt: str,
    *,
    workdir: Path | None,
    tools: str | None,
    model: str | None,
    timeout: float | None,
    label: str,
    out,
    paint_to,
    cancel_event: threading.Event | None = None,
) -> tuple[bool, str]:
    """One headless pi digest: launch it, feed the prompt, wait, report.

    THIS SHORT-CIRCUITS THE STREAMING MACHINERY, NOT THE TEARDOWN CONTRACT, and
    the distinction is the whole reason this is not the four-line
    `subprocess.run` it looks like it wants to be. pi runs `--mode text`, which
    is not our stream-json: no event to fold, no file counter to advance, and a
    digest runs `progress=False` anyway, so `fold_event` and the spinner have
    nothing to do. Everything ELSE `launch_agent` documents still holds. An
    agent is not one process -- it starts servers and shells of its own -- so it
    needs its OWN PROCESS GROUP and a row in `_LIVE`, or Ctrl-C leaves it
    reading with the wizard gone. `subprocess.run` gives neither, and that exact
    bug has already shipped once (see `stop_all`).

    `communicate` is what makes the prompt safe on stdin: it writes and reads
    concurrently, so the pipe-buffer deadlock the streaming path stages a temp
    file to avoid cannot happen. The prompt is never an argv element -- a
    rendered view is far past `MAX_ARG_STRLEN`.
    """
    from ... import jobs as import_jobs

    if cancel_event is not None and cancel_event.is_set():
        return False, "agent cancelled"
    tag = f"{label} " if label else ""

    def note(text: str) -> None:
        # The two destinations the streaming path writes its status line to,
        # and no third one. TWO LINES is the entire budget: a pi digest prints
        # nothing at all until it exits, and this module's own history is that
        # a silent agent is indistinguishable from a hang -- for up to
        # DIGEST_TIMEOUT_S here. There is no event stream to drive more than
        # "started" and "finished", and inventing a spinner for one bounded
        # call would be the machinery this branch exists to skip.
        if paint_to is not None:
            paint_to(text)
            return
        out.write(f"  {text}\n")
        out.flush()

    # `is None`, not `or`: an explicit `timeout=0` is a caller asking for
    # something specific, and `or` would silently substitute five minutes.
    bound = DIGEST_TIMEOUT_S if timeout is None else timeout
    try:
        argv = agent_argv(Agent.PI, binary, folder, workdir=workdir, tools=tools, model=model)
    except ArgvTooLargeError as exc:
        return False, str(exc)

    if cancel_event is not None and cancel_event.is_set():
        return False, "agent cancelled"

    # Same copy shape as the claude/codex quiet-run notes: the label prefix
    # already names the session and the agent, so the note is just the verb.
    note(f"{tag}reading the view")
    started = time.monotonic()
    try:
        proc = import_jobs.spawn_child(
            argv,
            cwd=str(workdir if workdir is not None else folder),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # one ordered stream, like the streaming path
            # NOT `text=True`, which encodes AND decodes with the LOCALE codec
            # in strict mode. Under `LC_ALL=C` that is ASCII, and a rendered
            # transcript view is routinely not ASCII -- so writing the prompt
            # raises `UnicodeEncodeError`, which is a `ValueError`, not a
            # `SubprocessError`, and takes the wizard down instead of failing
            # one digest. Pinned to utf-8 with replacement in both directions.
            encoding="utf-8",
            errors="replace",
            # The tail is read by people and stored in lane reports, and nothing
            # downstream strips ANSI. Ask pi not to emit it -- and pin
            # FORCE_COLOR too: an inherited FORCE_COLOR=1 overrides NO_COLOR
            # in node, bringing the escapes back PLUS a node warning line
            # about the conflict, merged into the tail. Verified on a real
            # machine carrying FORCE_COLOR=1 ambiently.
            env={**_backfill_agent_env(), "NO_COLOR": "1", "FORCE_COLOR": "0"},
            # ITS OWN PROCESS GROUP, for the reason `launch_agent` gives at
            # length: only a group can be killed as one.
            start_new_session=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, str(exc)
    if not _register_agent(proc, cancel_event):
        return False, "agent cancelled"

    try:
        stdout, _stderr = proc.communicate(input=prompt, timeout=bound)
    except subprocess.TimeoutExpired as exc:
        _kill_tree(proc)
        # NAME THE BOUND AND SHOW THE OUTPUT. "pi timed out" is unactionable:
        # the reader cannot tell a wedged binary from a deadline set too tight,
        # and whatever pi managed to say is usually the answer.
        partial = _pi_tail(exc.stdout, exc.stderr)
        return False, (
            f"pi did not finish within {bound:g}s"
            + (f" — last output: {partial}" if partial else ", and printed nothing")
        )
    except KeyboardInterrupt:
        # Same rule as the streaming path: the thread taking the interrupt must
        # not leave its siblings running.
        stop_all()
        raise
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        # `ValueError` is deliberate belt-and-braces on top of the pinned
        # encoding above: a codec failure out of `communicate` must fail ONE
        # digest, never the lane.
        _kill_tree(proc)
        return False, str(exc)
    finally:
        _release_agent(proc)

    ok = proc.returncode == 0
    note(f"{tag}{'finished' if ok else 'failed'} in {time.monotonic() - started:.1f}s")
    return ok, _pi_tail(stdout)
from probe.cli.imports.folder.agents.agents import Agent  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.argv import ArgvTooLargeError, agent_argv  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.process import _kill_tree, _register_agent, _release_agent, stop_all  # noqa: E402 -- an import cycle: bound once this module's names exist
from probe.cli.imports.folder.agents.shell_tools import _backfill_agent_env  # noqa: E402 -- an import cycle: bound once this module's names exist
