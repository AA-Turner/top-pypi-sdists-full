import logging
import os
import queue
import sys
import threading
from typing import Optional, TextIO, cast

import structlog

from openreward._version import __version__ as _sdk_version


OPENREWARD_USE_STRUCTURED_LOGS = bool(os.getenv("OPENREWARD_USE_STRUCTURED_LOGS", False))


class _NonBlockingStreamWriter:
    """A stdout writer with a bounded in-memory queue drained by a daemon thread.

    The env server logs synchronously from its asyncio event loop. If stdout
    stops draining -- e.g. a node whose containerd has stopped reading the
    container's log FIFO during a restart loop -- a direct ``write()`` blocks
    once the 64KB pipe buffer fills, freezing the event loop and the whole pod
    until the pipe drains (observed: ~11 minutes in a prod incident).

    Routing writes through a bounded queue moves that blocking off the event
    loop and onto the drain thread: a stalled pipe fills the queue instead of
    the loop, and once the queue is full lines are dropped (and counted, then
    surfaced when the pipe recovers) rather than blocking. Correctness of a
    single log line is traded for never freezing the process -- the right
    trade for a keepalive-dominated stream.

    Presents the ``write``/``flush`` interface structlog's PrintLogger and
    stdlib's StreamHandler expect, so it drops in as their target ``file``.
    """

    def __init__(self, stream=sys.stdout, maxsize: int = 20000):
        self._stream = stream
        self._q: "queue.Queue[str]" = queue.Queue(maxsize=maxsize)
        self._dropped = 0
        self._dropped_lock = threading.Lock()
        self._thread = threading.Thread(
            target=self._drain, name="openreward-log-writer", daemon=True
        )
        self._thread.start()

    def write(self, s: str) -> None:
        # Non-blocking: never waits on the queue, so a stalled pipe can't stall
        # the caller (the event loop). Full queue -> count a drop and move on.
        try:
            self._q.put_nowait(s)
        except queue.Full:
            with self._dropped_lock:
                self._dropped += 1

    def flush(self) -> None:
        # No-op: the drain thread owns the real flush. A synchronous flush here
        # would reintroduce exactly the blocking this class exists to avoid.
        pass

    def _drain(self) -> None:
        while True:
            s = self._q.get()
            try:
                with self._dropped_lock:
                    dropped, self._dropped = self._dropped, 0
                if dropped:
                    # Make the gap visible once the pipe drains so dropped lines
                    # aren't silent. Best-effort; same stream, same failure mode.
                    self._stream.write(
                        '{"severity":"WARNING","message":"log writer dropped '
                        f'{dropped} line(s) under backpressure"}}\n'
                    )
                self._stream.write(s)
                self._stream.flush()
            except Exception:
                # Never let a write error kill the drain thread; drop and continue.
                pass


_stdout_sink_singleton: Optional["_NonBlockingStreamWriter"] = None


def _stdout_sink() -> TextIO:
    """Return the log write target.

    Only the managed env-server (``OPENREWARD_USE_STRUCTURED_LOGS`` set by the
    provisioner) gets the non-blocking writer -- that's the single-worker
    asyncio process a stalled stdout pipe can freeze. Training scripts / dev
    keep plain ``sys.stdout`` and spawn no thread, so behaviour there is
    unchanged.
    """
    if not OPENREWARD_USE_STRUCTURED_LOGS:
        return sys.stdout
    global _stdout_sink_singleton
    if _stdout_sink_singleton is None:
        _stdout_sink_singleton = _NonBlockingStreamWriter(sys.stdout)
    # Duck-typed stand-in: PrintLogger and StreamHandler only call .write()/.flush().
    return cast(TextIO, _stdout_sink_singleton)

# Set by the provisioner when running in a managed env-server pod. Tags every
# structured log line so a log can be traced back to the exact build.
_openreward_build_sha = os.getenv("OPENREWARD_BUILD_SHA")


def _add_runtime_metadata(_, __, event_dict):
    event_dict["sdk_version"] = _sdk_version
    if _openreward_build_sha:
        event_dict["build_sha"] = _openreward_build_sha
    return event_dict


_SHARED_PROCESSORS = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]

_STRUCTURED_PROCESSORS = [*_SHARED_PROCESSORS, _add_runtime_metadata]

def _rename_for_gcp(_, method, event_dict):
    event_dict["message"] = event_dict.pop("event")
    event_dict["severity"] = event_dict.pop("level", method).upper()
    return event_dict


def _resolve_log_level() -> int:
    """Resolve log level from env vars: OPENREWARD_LOG_LEVEL -> LOG_LEVEL -> INFO."""
    raw = os.environ.get("OPENREWARD_LOG_LEVEL") or os.environ.get("LOG_LEVEL") or "INFO"
    return getattr(logging, raw.upper(), logging.INFO)


def get_logger(name: str) -> structlog.BoundLogger:
    """Return a structlog logger scoped to openreward with instance-level config.

    This avoids polluting the global ``structlog.configure()`` namespace so that
    training scripts importing the SDK don't see debug spam when the environment
    server's ``setup_logging()`` has not been called.
    """
    if OPENREWARD_USE_STRUCTURED_LOGS:
        processors = [*_STRUCTURED_PROCESSORS, _rename_for_gcp, structlog.processors.JSONRenderer()]
    else:
        processors = [*_SHARED_PROCESSORS, structlog.dev.ConsoleRenderer()]

    return structlog.wrap_logger(
        structlog.PrintLogger(_stdout_sink()),
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(_resolve_log_level()),
    ).bind(logger_name=name)


def setup_logging(level: int = logging.INFO):
    """Configure logging for the current process.

    Uses JSON structured logging when OPENREWARD_USE_STRUCTURED_LOGS is set,
    otherwise uses a human-readable console renderer.
    """
    if OPENREWARD_USE_STRUCTURED_LOGS:
        final_processors = [*_STRUCTURED_PROCESSORS, _rename_for_gcp, structlog.processors.JSONRenderer()]
    else:
        final_processors = [*_SHARED_PROCESSORS, structlog.dev.ConsoleRenderer()]

    structlog.configure(
        processors=final_processors,
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=_stdout_sink()),
        cache_logger_on_first_use=False,
    )

    if OPENREWARD_USE_STRUCTURED_LOGS:
        # Production: also configure stdlib root logger so that third-party
        # library messages (uvicorn, aiohttp, etc.) flow through structlog.
        formatter = structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
            foreign_pre_chain=[*_STRUCTURED_PROCESSORS, structlog.stdlib.ExtraAdder()],
        )

        handler = logging.StreamHandler(_stdout_sink())
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(level)
