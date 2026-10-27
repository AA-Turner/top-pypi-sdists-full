"""One way to run the `claude` binary, for every module that needs to.

Four modules grew their own copy of this — `setup.py`, `capabilities.py`,
`capture.py` and `updater.py` — each with a module-level `_CLAUDE_TIMEOUT_S`
and a near-identical `subprocess.run` around it. The copies had drifted to
20s / 90s / 180s / 90s, and only ONE of them (updater's) passed
`stdin=subprocess.DEVNULL`.

THE STDIN ARGUMENT IS THE POINT. `capture_output=True` redirects stdout and
stderr but NOT stdin, so a `claude` subcommand that decides to prompt inherits
the user's terminal: its question goes into the captured (invisible) stdout
while it blocks on a TTY nobody knows is being read, until the timeout fires.
A child that puts that TTY in raw mode eats the user's keystrokes meanwhile.
Handing it DEVNULL turns "hang for the full timeout" into "fail immediately on
EOF", which is a diagnosable failure instead of a mystery.

The timeouts stay DIFFERENT and stay at the call site: listing plugins is a
directory read and installing one is a network fetch, so a single shared
constant would be wrong for both. What is shared is the mechanism, not the
number.
"""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field

#: Reading local plugin state. No network, so a slow one is a wedged process.
LIST_TIMEOUT_S = 20.0

#: `marketplace add` + `update`. Claude bounds its own cache refresh at 120s
#: ("Refreshing marketplace cache (timeout: 120s)"), so this sits just above it
#: as a backstop rather than a second, shorter deadline that would cut Claude's
#: own retry off mid-flight.
REFRESH_TIMEOUT_S = 150.0

#: `plugin install`. Measured at well under a second against a warm marketplace;
#: 60s is the allowance for a cold fetch on a bad network.
INSTALL_TIMEOUT_S = 60.0

#: Turning capture off. Kept at the value capture.py used before this module.
CAPTURE_TIMEOUT_S = 90.0


@dataclass(frozen=True)
class Result:
    """The outcome of one `claude` invocation.

    `ok` is "the command did what was asked". `reachable` is the weaker "we got
    to run it at all" — False when the binary is missing or the process never
    produced an exit status. The two differ exactly where it matters: a machine
    with no Claude Code installed must not be reported as one where a plugin
    failed to install.
    """

    ok: bool
    detail: str = ""
    reachable: bool = True
    #: What ran, as a person would type it (`claude plugin update …`). Carried
    #: so an error message names the argv that was actually executed, instead
    #: of a caller re-typing a verb table that lives in plugin_cli.
    command: str = ""

    def __bool__(self) -> bool:
        return self.ok


def available() -> bool:
    """Whether the binary resolves at all. Absent is NORMAL on a GPU pod."""
    return shutil.which("claude") is not None


@dataclass
class _Bound:
    timeout: float
    #: When the block's time runs out (`time.monotonic`): ONE budget for every
    #: call in it, not one per call.
    deadline: float
    #: Binaries that timed out inside the block: not asked again in it.
    hung: set[str] = field(default_factory=set)


_bound: ContextVar[_Bound | None] = ContextVar("probe_agent_cli_bound", default=None)


class StoppedError(OSError):
    """A process the update gave up on was not started (`Processes.stop`)."""


class Processes:
    """The processes one part of an update starts through `capture` (each
    leading a process group of its own), so the update can stop them all when
    that part runs past its deadline (`upgrading.component_deadline`): a hung
    `codex plugin list` must not go on changing plugins after the update has
    moved on. Once stopped, it starts nothing more."""

    def __init__(self) -> None:
        import threading

        self._lock = threading.Lock()
        self._live: set = set()
        self.stopped = False

    def add(self, process: subprocess.Popen) -> bool:
        with self._lock:
            if self.stopped:
                return False
            self._live.add(process)
            return True

    def discard(self, process: subprocess.Popen) -> None:
        with self._lock:
            self._live.discard(process)

    def stop(self) -> int:
        """SIGKILL every live one's process group; start none after. How many."""
        with self._lock:
            self.stopped = True
            live = list(self._live)
        for process in live:
            _kill_group(process)
        return len(live)


_processes: ContextVar[Processes | None] = ContextVar("probe_update_processes", default=None)


@contextmanager
def tracking(processes: Processes) -> Iterator[None]:
    """`capture` calls in this block (this context: a thread started in a copy
    of it too) are `processes`' to stop."""
    token = _processes.set(processes)
    try:
        yield
    finally:
        _processes.reset(token)


@contextmanager
def bounded(timeout: float) -> Iterator[None]:
    """Every agent-CLI call in the block ends within `timeout` seconds of the
    block's start -- one budget shared by all of them -- a binary that timed out
    once is not run again inside it, and a call that times out is killed with
    its whole process group.

    For a read a person waits on (`probe status --refresh`): the call sites keep
    their own, longer allowances for the wizard. A hung binary stays hung for
    the few seconds one status read takes, so asking it a second question
    (`plugin list`, then `--version`) would only cost a second timeout. Covers
    `run` here, Codex's in `plugin_cli.run`, the version probe in
    `backfill.agent_version` and pi's `--help` sniff. A thread started inside
    the block shares its budget only when it runs in a copy of this context
    (`contextvars.copy_context`).

    The group: an agent CLI can be a wrapper that starts the real binary as its
    child (npm's `codex` is node starting the native one), and killing the
    wrapper alone leaves that child running. Inside the block each call starts
    its own process group (POSIX) and a timeout kills the group. Only inside it:
    a wizard's `claude plugin install` stays in the terminal's group, where a
    Ctrl-C reaches it as SIGINT rather than as a kill.
    """
    token = _bound.set(_Bound(timeout, time.monotonic() + timeout))
    try:
        yield
    finally:
        _bound.reset(token)


def call_timeout(timeout: float) -> float:
    """`timeout`, or what is left of the enclosing `bounded` block's budget when
    that is shorter (0 once it has run out)."""
    bound = _bound.get()
    if bound is None:
        return timeout
    return min(timeout, max(0.0, bound.deadline - time.monotonic()))


def already_hung(binary: str) -> bool:
    """Whether `binary` timed out earlier in the enclosing `bounded` block."""
    bound = _bound.get()
    return bound is not None and binary in bound.hung


def timed_out(binary: str) -> None:
    """Remember, for the enclosing `bounded` block, that `binary` timed out."""
    bound = _bound.get()
    if bound is not None:
        bound.hung.add(binary)


def seconds(value: float) -> str:
    """A duration as a message says it: `20s`, `1s`, `0.5s` -- never `0s` for
    half a second, as `:.0f` printed it."""
    return f"{max(round(value, 1), 0.1):g}s"


#: `Result.detail` for a call `bounded` skipped.
SKIPPED_HUNG = "not run: it timed out earlier in this check"
#: `Result.detail` for a call the `bounded` block had no time left for.
OUT_OF_TIME = "not run: the check ran out of time"


def capture(argv: list[str], *, timeout: float, env: dict | None = None, cwd: str | None = None
            ) -> subprocess.CompletedProcess:
    """`subprocess.run` with output captured as text and stdin closed: the one
    way every agent-CLI call here starts its process. Inside `bounded`, or
    inside `tracking` (an update's part), the child leads a process group of
    its own and a timeout, or the part's `Processes.stop`, kills the whole
    group. Raises what `subprocess.run` raises (`StoppedError` for a part
    already stopped)."""
    extra = {**({"env": env} if env is not None else {}), **({"cwd": cwd} if cwd is not None else {})}
    processes = _processes.get()
    if processes is not None and processes.stopped:
        raise StoppedError(f"not run, the update stopped this step: {' '.join(argv[:3])}")
    if (_bound.get() is None and processes is None) or os.name == "nt":
        return subprocess.run(  # noqa: S603 - the callers pass a resolved binary, no shell
            argv,
            capture_output=True,
            text=True,
            # See the module docstring: without this the child inherits the
            # user's terminal and an invisible prompt costs the full timeout.
            stdin=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
            **extra,
        )
    with subprocess.Popen(  # noqa: S603 - the callers pass a resolved binary, no shell
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
        **extra,
    ) as process:
        if processes is not None and not processes.add(process):
            _kill_group(process)  # stopped while it started
        try:
            out, err = process.communicate(timeout=timeout)
        except BaseException:  # a timeout, or the caller's own interrupt
            _kill_group(process)
            process.wait()
            raise
        finally:
            if processes is not None:
                processes.discard(process)
    if processes is not None and processes.stopped and process.returncode is not None and process.returncode < 0:
        raise StoppedError(f"stopped: the update gave up on this step ({' '.join(argv[:3])})")
    return subprocess.CompletedProcess(argv, process.returncode, out, err)


def _kill_group(process: subprocess.Popen) -> None:
    """SIGKILL the group `process` leads, and so every child it started."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    except OSError:
        process.kill()


def run(args: list[str], *, timeout: float) -> Result:
    """Run `claude <args>` with output captured and stdin closed."""
    command = " ".join(["claude", *args])
    binary = shutil.which("claude")
    if not binary:
        return Result(
            ok=False, detail="`claude` not found on PATH", reachable=False, command=command
        )
    return run_binary(binary, args, timeout=timeout, command=command)


def run_binary(binary: str, args: list[str], *, timeout: float, command: str) -> Result:
    """`binary <args>` as a `Result`: what `run` here and `plugin_cli.run` share."""
    if already_hung(binary):
        return Result(ok=False, detail=SKIPPED_HUNG, reachable=False, command=command)
    timeout = call_timeout(timeout)
    if timeout <= 0:
        return Result(ok=False, detail=OUT_OF_TIME, reachable=False, command=command)
    try:
        completed = capture([binary, *args], timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out(binary)
        # Distinct from a non-zero exit: nothing ran to completion, so the
        # caller cannot conclude anything about the state on disk.
        return Result(
            ok=False, detail=f"timed out after {seconds(timeout)}", reachable=False, command=command
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return Result(ok=False, detail=str(exc), reachable=False, command=command)
    # `stdout`/`stderr` are None whenever the streams were not captured. That
    # never happens on the path above, but a caller (or a test double) handing
    # back a CompletedProcess built some other way must not turn into an
    # AttributeError inside the one helper every `claude` call goes through.
    out = (completed.stdout or "").strip()
    err = (completed.stderr or "").strip()
    if completed.returncode != 0:
        return Result(ok=False, detail=err or out, command=command)
    return Result(ok=True, detail=out, command=command)
