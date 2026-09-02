"""Silence all log output in the hook hot path.

Hook stdout/stderr are a strict protocol surface: AI clients (Cursor, Claude
Code, ...) treat *any* hook stderr output as an error and flag the invocation as
failed. The hook path never calls ``setup_logging``, so structlog's default sink
is stdout; scan helpers such as ``get_or_create_device_id`` emit a device-id
line that would corrupt the hook response or (once redirected to stderr) trip
the client's stderr-is-error heuristic.

Unlike ``setup_logging`` this does **no disk I/O** — it must be safe in the hot,
possibly read-only hook path (``setup_logging`` writes a per-fire log file and
can raise on a read-only fs).
"""

from __future__ import annotations

import logging

import structlog


def silence_hook_logging() -> None:
    """Route structlog + stdlib logging to nowhere.

    Idempotent, process-global, no disk I/O. Call once at each hook entrypoint,
    before any code that might log (e.g. the scan device-id helpers).

    - structlog: a ``CRITICAL``-threshold filtering bound logger drops every
      call below critical (the scan device-id lines are debug/info), and
      ``ReturnLoggerFactory`` means even a stray ``critical`` returns the value
      instead of printing it to stdout. (``make_filtering_bound_logger`` only
      accepts the standard level ints, so ``CRITICAL`` is the ceiling; the
      return-logger factory is what makes it a true no-op.)
    - stdlib ``logging``: ``logging.disable`` gags any ``logging``-based lines
      (e.g. httpx) at or below critical.

    ``cache_logger_on_first_use`` is left ``False`` (structlog's default) so
    already-created module-level loggers (e.g. ``scan.device``) re-bind against
    this config on their next call rather than caching a prior sink, and so a
    later ``structlog.reset_defaults()`` (tests) fully restores default output.
    """
    structlog.configure(
        processors=[],
        wrapper_class=structlog.make_filtering_bound_logger(logging.CRITICAL),
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    logging.disable(logging.CRITICAL)
