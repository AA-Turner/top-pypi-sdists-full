"""Engineering pings for daemon errors: `daemon.error` -> PostHog -> #eng-alerts.

`daemon-errors.log` tells the researcher on their own machine; nobody at Probe
learned of a daemon that failed 923 bites in a row on a content filter (anthrogen,
2026-10-03 to 10-07) until a cost audit. This module sends one PostHog event for
an error an engineer should look at, and a PostHog destination ("Daemon errors ->
#eng-alerts", project 526001, its body in `scripts/deploy/posthog-daemon-error-
alerts.json`) posts it to Slack, the way the kb search guardian's events do.

WHAT PINGS is `Kind`. Errors the researcher fixes or that pass on their own do
not (`quiet`): a refused key, the team's daemon switched off, the budget, a rate
limit, a timeout, no answer at all (an offline laptop, a sleeping one waking up),
missing AI libraries. The Probe MCP's own failures count the same way: they reach
the daemon as `httpx.HTTPStatusError` (the status on `.response`) or as
`RuntimeError("Client failed to connect: ...")` raised from the connect error.

ONCE per machine per (kind, error type, status) every REPORT_INTERVAL_S: a
failing bite retries with backoff and a crashed worker is started again, each a
fresh process, so the window is a stamp file in the daemon's state folder
(`telemetry.report_due`), not a counter in memory. The PostHog destination also
masks per team, kind and error type for an hour.

The event rides the CLI's telemetry pipe, so `PROBE_TELEMETRY=off` and a
self-hosted server send nothing, and it never raises. It carries `error_text`
(the error's first line, secret-scrubbed, the home folder as `~`, cut to
ERROR_TEXT_CHARS): the one free-text field client telemetry allows, by Richard's
call (2026-10-07), documented in `probe._shared.telemetry`. `PROBE_DIAGNOSTICS=off`
drops it (the ping still goes, with the error's type and status).

Imports nothing from the AI libraries at load time.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from probe._compat import StrEnum
from probe._shared import telemetry

#: What Slack shows of an error: its first line, after scrubbing, cut here.
ERROR_TEXT_CHARS = 300
#: The same error (kind, type, status) pings again from this machine after this long.
REPORT_INTERVAL_S = 6 * 3600.0
#: Model-route and MCP answers that are the researcher's to fix or pass on their
#: own: the key (401, 403), the budget (402), a timeout (408, and the gateway's
#: 504 when the model did not answer in time), the rate (429).
USER_SIDE_STATUSES = frozenset({401, 402, 403, 408, 429, 504})
_CODE = re.compile(r"^[a-z0-9_]{1,64}$")
#: How far down `__cause__` and inside exception groups an error is looked into.
_DEPTH = 6


class Kind(StrEnum):
    #: The worker died on an unexpected exception (EXIT_CRASHED).
    CRASHED = "crashed"
    #: The model's content filter refused the request.
    MODEL_REFUSED = "model_refused"
    #: The model route answered a 4xx that is not the researcher's (USER_SIDE_STATUSES).
    MODEL_REJECTED = "model_rejected"
    #: A bite failed on an exception that is neither the model's nor the network's: a bug.
    BITE_FAILED = "bite_failed"
    #: The model's gateway answered 5xx bites in a row and the agent took recording back.
    GATEWAY_DOWN = "gateway_down"
    #: The reader failed turns in a row (not on the network, not on its key).
    READER_FAILING = "reader_failing"
    #: A range of events was skipped: bites in a row hit their limits or went in circles.
    EVENTS_SKIPPED = "events_skipped"
    #: A chat log was rewritten under the cursor; the daemon stopped reading it.
    CHAT_LOG_REWRITTEN = "chat_log_rewritten"
    #: The session's switch file could not be read; the worker stopped.
    SWITCH_UNREADABLE = "switch_unreadable"


_base_url: str | None = None


def configure(base_url: str | None) -> None:
    """The Probe API the daemon talks to: the hosted gate is checked against it.
    Until this is called nothing is sent (an unknown backend fails closed)."""
    global _base_url
    _base_url = base_url


def _links(exc: BaseException, depth: int = 0):
    """The error and the errors it was raised from (`__cause__`)."""
    yield exc
    if depth >= _DEPTH:
        return
    if exc.__cause__ is not None:
        yield from _links(exc.__cause__, depth + 1)


def _members(exc: BaseException) -> list[BaseException] | None:
    group = getattr(exc, "exceptions", None)  # an ExceptionGroup (the MCP client's task groups)
    if isinstance(group, (list, tuple)) and group and all(isinstance(e, BaseException) for e in group):
        return list(group)
    return None


def network_only(exc: BaseException, depth: int = 0) -> bool:
    """No HTTP answer at all: a refused or dropped connection, a client timeout,
    here or in what it was raised from. On a laptop that is usually the laptop.
    A group is network-only when every error in it is."""
    import httpx
    from pydantic_ai.exceptions import ModelAPIError, ModelHTTPError

    members = _members(exc)
    if members is not None and depth < _DEPTH:
        return all(network_only(m, depth + 1) for m in members)
    for link in _links(exc):
        if isinstance(link, ModelHTTPError) or status_of(link) is not None:
            return False
        if isinstance(link, (ModelAPIError, ConnectionError, TimeoutError, httpx.TransportError)):
            return True
    return False


def status_of(exc: BaseException | None) -> int | None:
    """The HTTP status an error carries: its own `status_code` (the model's
    errors) or its response's (`httpx.HTTPStatusError`, the MCP's), here or in
    what it was raised from."""
    if exc is None:
        return None
    for link in _links(exc):
        for status in (getattr(link, "status_code", None),
                       getattr(getattr(link, "response", None), "status_code", None)):
            if isinstance(status, int) and not isinstance(status, bool):
                return status
    return None


def quiet(exc: BaseException, depth: int = 0) -> bool:
    """Not Probe's to look at: no answer at all, or an answer that is the
    researcher's (USER_SIDE_STATUSES). A group is quiet when every error in it is."""
    members = _members(exc)
    if members is not None and depth < _DEPTH:
        return all(quiet(m, depth + 1) for m in members)
    return network_only(exc) or status_of(exc) in USER_SIDE_STATUSES


def bite_kind(exc: BaseException) -> Kind | None:
    """The kind a failed bite pings as, or None. A model 5xx is None here: it
    pings as GATEWAY_DOWN only when the worker gives the lease back over it."""
    from pydantic_ai.exceptions import ContentFilterError, ModelHTTPError, UsageLimitExceeded

    if isinstance(exc, ContentFilterError):
        return Kind.MODEL_REFUSED
    if isinstance(exc, UsageLimitExceeded) or quiet(exc):
        return None
    if isinstance(exc, ModelHTTPError):
        return Kind.MODEL_REJECTED if 400 <= int(exc.status_code) < 500 else None
    return Kind.BITE_FAILED


def error_text(source: BaseException | str) -> str:
    """The first non-empty line of an error (`Type: message`) or of a text, the
    home folder as `~`, secrets redacted, cut to ERROR_TEXT_CHARS."""
    from probe.tap_core import secrets

    raw = source if isinstance(source, str) else f"{type(source).__name__}: {source}"
    line = next((part.strip() for part in raw.splitlines() if part.strip()), "")
    if len(line) > secrets.MAX_SCAN_CHARS:
        # Cut, then drop the word the cut split: a token cut short no longer
        # matches its rule, and a large redaction before it could pull it in.
        line = re.sub(r"\S+$", "", line[:secrets.MAX_SCAN_CHARS])
    # A repr's escaped newline (`'x\nprobe_pat_...'`) sits against the token, so
    # the rules' word boundary would miss it.
    line = line.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
    for home in {str(Path.home()), os.path.realpath(Path.home())}:
        if len(home) > 1:
            line = re.sub(re.escape(home) + r"(?=$|[\\/\s'\":,)\]])", "~", line)
    clean, _ = secrets.redact(line)
    return clean[:ERROR_TEXT_CHARS]


def _code(exc: BaseException | None) -> str | None:
    """The server's refusal `code` on a model-route error, when it is a plain code."""
    if exc is None:
        return None
    from probe.daemon import worker as worker_mod

    code = worker_mod._refusal_code(exc)
    return code if code and _CODE.match(code) else None


def report(kind: Kind, *, session_id: str, lane: str, exc: BaseException | None = None,
           text: str | None = None, count: int | None = None) -> bool:
    """Send one `daemon.error`, once per machine per (kind, error type, status)
    every REPORT_INTERVAL_S. `text` stands in for the exception's when the error
    is the daemon's own finding (events skipped, a rewritten chat log). True
    when it was sent."""
    try:
        error_type = type(exc).__name__ if exc is not None else None
        status = status_of(exc)
        ctx = telemetry.detached_context(_base_url, via=telemetry.Via.DAEMON)
        if not ctx.enabled:  # the opt-out or self-host: send nothing, stamp nothing
            return False
        from probe.daemon.store import state_dir
        from probe.sdk import diagnostics

        key = f"daemon-error-{kind}-{error_type or 'none'}-{status or 0}"
        state_dir().mkdir(parents=True, exist_ok=True)
        if not telemetry.report_due(str(state_dir()), key, interval_s=REPORT_INTERVAL_S):
            return False
        source = text if text is not None else exc
        ctx.emit(
            telemetry.EVENT_DAEMON_ERROR,
            kind=str(kind),
            lane=lane,
            daemon_session=session_id,
            error_type=error_type if error_type and error_type.isidentifier() else None,
            status=status,
            code=_code(exc),
            count=count,
            error_text=None if source is None or diagnostics.disabled() else error_text(source),
        )
        return True
    except Exception:  # noqa: BLE001 -- a ping never costs the daemon anything
        return False


def report_bite_failure(exc: BaseException, *, session_id: str, lane: str) -> bool:
    """A failed bite's ping, if its error is one (`bite_kind`). Never raises."""
    try:
        kind = bite_kind(exc)
    except Exception:  # noqa: BLE001
        return False
    return kind is not None and report(kind, session_id=session_id, lane=lane, exc=exc)


def report_reader_failure(exc: BaseException, *, session_id: str, lane: str, count: int) -> bool:
    """The reader failing `count` turns in a row, unless its error is `quiet`. Never raises."""
    try:
        if quiet(exc):
            return False
    except Exception:  # noqa: BLE001
        return False
    return report(Kind.READER_FAILING, session_id=session_id, lane=lane, exc=exc, count=count)
