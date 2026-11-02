"""What a managed worker printed before it failed, read back so `agents deploy` can show why.

The deployment status only carries the platform's verdict ("Service is unhealthy."). The reason a worker
did not start - a traceback, a missing dependency, a preflight refusal - only exists in its stdout and
stderr, which the Runtime API serves as the service's runtime logs.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence

import httpx
from pydantic import ValidationError

from . import runtime_logs
from .runtime_logs import LogEntry, terminal_safe

# One call covers several crash cycles of a worker that dies at startup; only the last one is shown.
_LOG_ENTRIES_READ = 100
_READ_DEADLINE_SECONDS = 15.0
_MAX_LINES_SHOWN = 30
_MAX_LINE_LENGTH = 500
_WORKER_STREAMS = frozenset({"stdout", "stderr"})
# The platform logs these on the "koyeb" stream each time it (re)starts an instance; everything the worker
# printed after the newest one belongs to the latest attempt.
_RESTART_MARKERS = ("Instance is starting", "Instance created")


async def fetch_worker_output(
    *,
    service_id: str,
    api_key: str,
    logs_url: str,
    transport: httpx.AsyncBaseTransport | None = None,
) -> list[str] | None:
    """Return the latest start attempt's output, oldest line first, or None if the logs could not be read.

    Never raises: it runs after a deploy has already failed, and must not replace that error with its own.
    """
    try:
        # One deadline for the whole read, retries included: the user is already looking at a failed deploy.
        async with asyncio.timeout(_READ_DEADLINE_SECONDS):
            async with runtime_logs.client(
                logs_url=logs_url, api_key=api_key, timeout_seconds=_READ_DEADLINE_SECONDS, transport=transport
            ) as http:
                page = await runtime_logs.read_page(http, service_id, order="desc", limit=_LOG_ENTRIES_READ, retries=0)
    # InvalidURL is not an HTTPError: a malformed AGENTS_SDK_DEPLOY_RUNTIME_LOGS_URL lands there.
    except (TimeoutError, httpx.HTTPError, httpx.InvalidURL, ValidationError):
        return None
    return latest_attempt_output(page.logs)


def latest_attempt_output(newest_first: Sequence[LogEntry]) -> list[str]:
    lines: list[str] = []
    for entry in newest_first:
        if entry.stream not in _WORKER_STREAMS:
            # A restart after the crash is logged before we read; only a restart preceding output ends it.
            if lines and entry.msg.startswith(_RESTART_MARKERS):
                break
            continue
        line = terminal_safe(entry.msg).rstrip()
        if line.strip():
            lines.append(line if len(line) <= _MAX_LINE_LENGTH else f"{line[: _MAX_LINE_LENGTH - 1]}…")
    return list(reversed(lines))[-_MAX_LINES_SHOWN:]
