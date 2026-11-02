"""Cloud-only wall-clock containment for pre-push checks."""

import codecs
import os
import selectors
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import ExitStack, contextmanager, suppress
from pathlib import Path
from threading import Thread
from typing import Any, cast

DEFAULT_BUDGET_SECONDS = 600
TERM_GRACE_SECONDS = 10
KILL_GRACE_SECONDS = 1
OUTPUT_DRAIN_SECONDS = 1
MAX_PENDING_STDOUT_BYTES = 65536


def _restore_signal_handlers(installed: list[tuple[int, object]], primary_error: BaseException | None) -> None:
    restoration_errors = []
    for signum, previous_handler in reversed(installed):
        try:
            signal.signal(signum, cast(Any, previous_handler))
        except BaseException as exc:
            restoration_errors.append((signum, exc))
    if primary_error is not None:
        for signum, error in restoration_errors:
            primary_error.add_note(f"Signal restoration failed for {signum}: {error!r}")
    elif restoration_errors:
        raise restoration_errors[0][1]


def _eligible_signal_handlers(
    is_posix: Callable[[], bool],
    is_main_thread: Callable[[], bool],
    get_handler: Callable[[int], object],
) -> list[tuple[int, object]]:
    candidates: tuple[str, ...] = ("SIGTERM", "SIGHUP")
    if not is_posix() or not is_main_thread():
        candidates = ()
    return [
        (signum, previous_handler)
        for name in candidates
        if (signum := getattr(signal, name, None)) is not None
        if (previous_handler := get_handler(signum)) is not None
    ]


@contextmanager
def _temporary_signal_handlers(
    *,
    is_posix: Callable[[], bool] = lambda: os.name == "posix",
    is_main_thread: Callable[[], bool] = lambda: threading.current_thread() is threading.main_thread(),
    get_handler: Callable[[int], object] = signal.getsignal,
) -> Iterator[Any]:
    """Yield lifecycle state; callers catch Interrupted through begin_cleanup().

    Call begin_cleanup() before cleanup work. first_signum remains inspectable
    after exit; signals are no longer intercepted once handlers are restored.
    Reentrant handler calls are ignored while capture is active. CPython
    dispatches pending signal handlers in signum order, so first_signum reflects
    handler invocation order, not kernel arrival order.
    """
    eligible = _eligible_signal_handlers(is_posix, is_main_thread, get_handler)

    class Lifecycle:
        class Interrupted(BaseException):
            """First body signal; catch only inside the with body."""

        phase = "installing"
        first_signum: int | None = None
        restoration_started = False
        interrupted = False
        _handling_lock = threading.Lock()

        def handle(self, signum: int, frame: object) -> None:
            if not self._handling_lock.acquire(blocking=False):
                return
            try:
                if self.first_signum is None:
                    self.first_signum = signum
                if all((self.phase == "body", not self.restoration_started, not self.interrupted)):
                    self.interrupted = True
                    raise self.Interrupted()
            finally:
                self._handling_lock.release()

        def begin_body(self) -> None:
            self.phase = "body"
            if self.first_signum is not None:
                self.handle(self.first_signum, None)

        def begin_cleanup(self) -> None:
            self.phase = "cleanup"

    lifecycle = Lifecycle()
    installed: list[tuple[int, object]] = []
    primary_error = None
    try:
        for signum, previous_handler in eligible:
            signal.signal(signum, lifecycle.handle)
            installed.append((signum, previous_handler))
        try:
            yield lifecycle
        finally:
            lifecycle.restoration_started, lifecycle.phase = True, "restoring"
    except BaseException as exc:
        primary_error = exc
        raise
    finally:
        lifecycle.restoration_started, lifecycle.phase = True, "restoring"
        _restore_signal_handlers(installed, primary_error)


def resolve_budget_seconds(environ: Mapping[str, str]) -> int:
    """Resolve a positive override, warning once when falling back."""
    raw = environ.get("AGDT_PRE_PUSH_BUDGET_SECONDS")
    if raw is None:
        return DEFAULT_BUDGET_SECONDS
    try:
        value = int(raw)
        if value > 0:
            return value
    except ValueError:
        pass  # Invalid integer input intentionally falls through to the warning/default.
    print(
        "AGDT pre-push: invalid AGDT_PRE_PUSH_BUDGET_SECONDS; using 600s",
        file=sys.stderr,
    )
    return DEFAULT_BUDGET_SECONDS


def _stop_group(process: subprocess.Popen, status: list[int] | None = None) -> bool:
    """Reap the leader and confirm its entire group is gone before allowing a push."""
    completed_status = process.poll()
    if status is not None and completed_status is not None:
        status.append(completed_status)
    try:
        os.killpg(process.pid, 0)
    except ProcessLookupError:
        return True
    for sig, grace in ((signal.SIGTERM, TERM_GRACE_SECONDS), (signal.SIGKILL, KILL_GRACE_SECONDS)):
        with suppress(ProcessLookupError):
            os.killpg(process.pid, sig)
        cleanup_deadline = time.monotonic() + grace
        while time.monotonic() < cleanup_deadline:
            process.poll()  # Reap the group leader before probing the group.
            try:
                os.killpg(process.pid, 0)
            except ProcessLookupError:
                return True
            time.sleep(0.05)
    return False


def _make_stdout_forwarder() -> tuple[Callable[[str], None], Callable[[], None]]:
    try:
        stdout_fd = sys.stdout.fileno()
        was_blocking = os.get_blocking(stdout_fd)
        os.set_blocking(stdout_fd, False)
    except AttributeError, OSError, ValueError:

        def forward_direct(text: str) -> None:
            sys.stdout.write(text)
            sys.stdout.flush()

        return forward_direct, lambda: None

    pending = bytearray()
    forwarding = True

    def forward(text: str) -> None:
        nonlocal forwarding
        if not forwarding:
            return
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        errors = getattr(sys.stdout, "errors", None) or "strict"
        pending.extend(text.encode(encoding, errors=errors))
        if len(pending) > MAX_PENDING_STDOUT_BYTES:
            pending.clear()
            forwarding = False
            return
        try:
            written = os.write(stdout_fd, pending)
        except BlockingIOError:
            return
        del pending[:written]

    def restore() -> None:
        with suppress(OSError):
            os.set_blocking(stdout_fd, was_blocking)

    return forward, restore


def _drain_output(fd: int, decoder: codecs.IncrementalDecoder, emit: Callable[[str], None]) -> None:
    """Drain available shutdown output without waiting for EOF, then finish decoding."""
    os.set_blocking(fd, False)
    drain_deadline = time.monotonic() + OUTPUT_DRAIN_SECONDS
    while time.monotonic() < drain_deadline:
        try:
            chunk = os.read(fd, 4096)
        except BlockingIOError:
            break
        if not chunk:
            break
        emit(decoder.decode(chunk))
    emit(decoder.decode(b"", final=True))


def run_with_budget(command: Sequence[str], budget_seconds: int, log_path: Path) -> int:
    """Stream checks, preserving statuses; permit only confirmed POSIX timeouts."""
    if budget_seconds <= 0 or os.name != "posix":
        raise ValueError("A positive budget and POSIX process-group support are required")
    with log_path.open("w", encoding="utf-8") as log, ExitStack() as cleanup:
        forward_stdout, restore_stdout = _make_stdout_forwarder()
        try:

            def emit(text: str) -> None:
                log.write(text)
                log.flush()
                forward_stdout(text)

            emit(f"AGDT pre-push: cloud-agent budget {budget_seconds}s\n")
            emit(f"GITHUB_ACTIONS={os.environ.get('GITHUB_ACTIONS', '<unset>')}\n")
            deadline = time.monotonic() + budget_seconds
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                shell=False,
                bufsize=0,
            )
            cleanup.callback(_stop_group, process)
            assert process.stdout is not None

            status: list[int] = []

            def observe_exit() -> None:
                try:
                    status.append(process.wait(timeout=max(0, deadline - time.monotonic())))
                except subprocess.TimeoutExpired:
                    pass  # Only a leader still running at the deadline qualifies for timeout allowance.

            with process.stdout as pipe, selectors.DefaultSelector() as selector:
                observer = Thread(target=observe_exit, daemon=True)
                observer.start()
                cleanup.pop_all()
                cleanup.callback(observer.join)
                cleanup.callback(_stop_group, process)
                selector.register(pipe, selectors.EVENT_READ)
                decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
                while time.monotonic() < deadline:
                    forward_stdout("")
                    if not selector.select(timeout=min(0.05, max(0, deadline - time.monotonic()))):
                        if status:
                            break
                        continue
                    chunk = os.read(pipe.fileno(), 4096)
                    emit(decoder.decode(chunk))
                    if not chunk:
                        break
                observer.join()
                cleaned = _stop_group(process, status)
                _drain_output(pipe.fileno(), decoder, emit)
                cleanup.pop_all()
                if status and cleaned:
                    return status[0]
                emit(
                    f"AGDT_PRE_PUSH_BUDGET_EXHAUSTED budget={budget_seconds}s: "
                    "targeted checks did not finish; push allowed, CI is the gate\n"
                    if cleaned
                    else "AGDT pre-push: timeout cleanup unconfirmed; push blocked\n"
                )
                return int(not cleaned)
        finally:
            restore_stdout()


def main(argv: Sequence[str] | None = None) -> int:
    """Run the existing checks command with the cloud budget and repository log."""
    try:
        return run_with_budget(
            [sys.executable, "-u", "-m", "agentic_devtools.cli.checks", "--format-fix"],
            resolve_budget_seconds(os.environ),
            Path(__file__).resolve().parents[3] / ".pre-push-output.log",
        )
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"AGDT pre-push: {exc}; push blocked", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
