"""Bounded helpers for cleaning up Windows subprocess resources."""

from __future__ import annotations

import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProcessCleanupDiagnostic:
    stage: str
    message: str


class ProcessCleanupError(RuntimeError):
    def __init__(
        self,
        completed_process: subprocess.CompletedProcess[str],
        cleanup_errors: tuple[ProcessCleanupDiagnostic, ...],
    ) -> None:
        self.completed_process = completed_process
        self.cleanup_errors = cleanup_errors
        details = "; ".join(f"{item.stage}: {item.message}" for item in cleanup_errors)
        super().__init__(f"Process cleanup failed after command completion: {details}")


def _attempt_process_cleanup(
    stage: str,
    action: Callable[..., Any],
    args: tuple[Any, ...],
    errors: list[ProcessCleanupDiagnostic],
    cancellation: BaseException | None,
) -> tuple[Any, BaseException | None, bool]:
    attempt_errors: list[ProcessCleanupDiagnostic] = []
    previous_cancellation = cancellation
    result = None
    try:
        result = action(*args)
    except Exception as error:
        attempt_errors.append(ProcessCleanupDiagnostic(stage, str(error)))
        attempt_errors.extend(
            ProcessCleanupDiagnostic(stage, str(message)) for message in getattr(error, "_agdt_cleanup_errors", ())
        )
    except (KeyboardInterrupt, SystemExit, GeneratorExit) as error:
        if cancellation is None:
            cancellation = error
        else:
            attempt_errors.append(ProcessCleanupDiagnostic(stage, str(error)))
        attempt_errors.extend(
            ProcessCleanupDiagnostic(stage, str(message)) for message in getattr(error, "_agdt_cleanup_errors", ())
        )
    errors.extend(attempt_errors)
    return result, cancellation, bool(attempt_errors) or cancellation is not previous_cancellation


def _drain_and_reap_process(
    process: Any,
    timeout: float,
    drain: Callable[[Any, float], tuple[str | None, str | None]],
    reap: Callable[[Any, float], None],
    as_text: Callable[[str | bytes | None], str | None],
    prefer_output: Callable[[str | None, str | bytes | None], str | None],
    errors: list[ProcessCleanupDiagnostic],
    cancellation: BaseException | None,
) -> tuple[str | None, str | None, subprocess.TimeoutExpired | None, BaseException | None]:
    stdout = stderr = None
    drain_timeout: subprocess.TimeoutExpired | None = None
    if process is None:
        return stdout, stderr, drain_timeout, cancellation
    try:
        stdout, stderr = drain(process, timeout)
    except subprocess.TimeoutExpired as error:
        drain_timeout = error
        stdout = as_text(error.output)
        stderr = as_text(error.stderr)
        errors.append(ProcessCleanupDiagnostic("drain", str(error)))
    except Exception as error:
        errors.append(ProcessCleanupDiagnostic("drain", str(error)))
        stdout = prefer_output(stdout, getattr(error, "output", None))
        stderr = prefer_output(stderr, getattr(error, "stderr", None))
    except (KeyboardInterrupt, SystemExit, GeneratorExit) as error:
        errors.append(ProcessCleanupDiagnostic("drain", str(error)))
        if cancellation is None:
            cancellation = error
        stdout = prefer_output(stdout, getattr(error, "output", None))
        stderr = prefer_output(stderr, getattr(error, "stderr", None))
    previous_cancellation = cancellation
    _, cancellation, _ = _attempt_process_cleanup("reap", reap, (process, timeout), errors, cancellation)
    if cancellation is not previous_cancellation:
        errors.append(ProcessCleanupDiagnostic("reap", str(cancellation)))
    return stdout, stderr, drain_timeout, cancellation


def _attempt_cleanup(
    action: Callable[..., None],
    args: tuple[Any, ...],
    errors: list[str],
    cancellation: BaseException | None,
) -> BaseException | None:
    # Finish all releases before re-raising caller cancellation.
    try:
        action(*args)
    except BaseException as error:
        if isinstance(error, Exception):
            errors.append(str(error))
        elif cancellation is None:
            cancellation = error
        else:
            errors.append(str(error))
    return cancellation


def _close_stream_bounded(stream: Any, timeout: float) -> None:
    errors: list[BaseException] = []

    def close_stream() -> None:
        # Report worker BaseException to the joining thread instead of excepthook.
        try:
            stream.close()
        except BaseException as exc:
            errors.append(exc)

    closer = threading.Thread(target=close_stream, daemon=True)
    closer.start()
    closer.join(timeout)
    if closer.is_alive():
        raise TimeoutError("Stream close exceeded its cleanup deadline")
    if errors:
        error = errors[0]
        if isinstance(error, Exception):
            raise error
        raise RuntimeError(f"Stream close failed in worker: {error}") from error


def _close_process_resources(
    process: Any,
    job_handle: int | None,
    timeout: float,
    close_job: Callable[[int], None],
) -> tuple[str, ...]:
    errors: list[str] = []
    cancellation: BaseException | None = None
    if job_handle:
        cancellation = _attempt_cleanup(close_job, (job_handle,), errors, cancellation)
    if process is not None:
        close_deadline = time.monotonic() + timeout
        for stream in (process.stdout, process.stderr, process.stdin):
            if stream is not None:
                cancellation = _attempt_cleanup(
                    _close_stream_bounded,
                    (stream, max(0, close_deadline - time.monotonic())),
                    errors,
                    cancellation,
                )
        process_handle = getattr(process, "_handle", None)
        close_process_handle = getattr(process_handle, "Close", None)
        if callable(close_process_handle):
            cancellation = _attempt_cleanup(close_process_handle, (), errors, cancellation)
    if cancellation is not None:
        setattr(cancellation, "_agdt_cleanup_complete", True)
        setattr(cancellation, "_agdt_cleanup_errors", tuple(errors))
        raise cancellation
    return tuple(errors)
