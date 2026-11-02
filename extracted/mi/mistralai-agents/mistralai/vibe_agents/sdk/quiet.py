from __future__ import annotations

import logging
import sys

from mistralai.agents import _silence

# Runtime half of the local-SDK log quieting. The logger-name lists and presilence() (raise levels
# + structlog config, run before the workflows import) are single-sourced in mistralai.agents._silence;
# this module reuses them and adds the message filter for records structlog writes straight to a
# handler at runtime, which a per-logger level cannot catch. AGENTS_SDK_DEBUG=1 disables all of it.

_filter_applied = False


class _DropNoise(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(drop in message for drop in _silence.DROP_MESSAGES)


def quiet_local_sdk_logs() -> None:
    # Apply levels (via the single-sourced presilence), then install the message filter for records
    # structlog writes straight to a handler at runtime. No-op when AGENTS_SDK_DEBUG is set.
    global _filter_applied
    if _silence.debug_enabled():
        return
    _silence.presilence()
    if _filter_applied:
        return
    _filter_applied = True
    noise_filter = _DropNoise()
    # A filter on the emitting logger runs before any handler, so it still applies when the root
    # has no handler yet (the record then goes to logging's last-resort handler) and after the
    # worker replaces the root handlers when it sets up its logging at startup.
    for name in _silence.NOISY_LOGGERS:
        logging.getLogger(name).addFilter(noise_filter)
    root = logging.getLogger()
    root.addFilter(noise_filter)
    for handler in root.handlers:
        handler.addFilter(noise_filter)


def show_worker_warnings() -> None:
    """Print WARNING and higher log records to stderr in a worker process.

    presilence() configures structlog before the workflows config loads, so the framework skips its
    own logging setup and installs no console handler. Python then prints warnings only through its
    last-resort handler, which stops as soon as the worker adds the OpenTelemetry log handler to the
    root logger. Without this handler, a worker's warnings, such as a failed tool Hook, reach no
    terminal. The format matches the last-resort handler. If a root handler already writes to the
    console, for example under AGENTS_SDK_DEBUG=1, this is a no-op, so no line prints twice.
    """
    root = logging.getLogger()
    consoles = (sys.stderr, sys.stdout)
    if any(getattr(handler, "stream", None) in consoles for handler in root.handlers):
        return
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.addFilter(_DropNoise())
    root.addHandler(handler)
