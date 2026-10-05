"""SDK HTTP transport over the Probe Research v3 contract.

One thin wrapper around httpx that knows the two auth surfaces:
  * ``/v1/*``    -> ``Authorization: Bearer probe_pat_...`` (user API token)
  * ``/ingest/*`` -> ``Authorization: Bearer ros_ing_...`` (+ optional X-Signature HMAC)

It maps HTTP status to the typed exceptions in ``errors`` and retries idempotent
calls on 5xx / network blips with capped backoff. Reads that paginate expose the
``X-Next-Cursor`` response header via :class:`Page`.
"""

from __future__ import annotations

from .secret_gate import InspectionResult, freeze_stream, freeze_upload, warn_if_incomplete

import hashlib
import hmac
import json
import os
import random
import re
import sys
import time
from contextlib import contextmanager
from contextvars import ContextVar
from probe._compat import StrEnum
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any

import httpx

from ..client_headers import (
    CLIENT_KIND_HEADER,
    device_headers,
    CLIENT_VERSION_HEADER,
    client_version_headers,
    current_client_headers,
)
import functools
from urllib.parse import urlsplit

from . import client_status
from . import diagnostics as _diagnostics
from . import durable
from . import errors
from . import safe_warn
from . import session_marker
from . import unstorable
from .config import DAEMON_SHELL_CONFIG, Settings
from .agent_session import AGENT_SESSION_HEADER, agent_session_headers
from .surface import SURFACE_HEADER, TOOL_HEADER, Surface, current_tool
from .tls import ssl_context

#: SDK reliability 2.8: every request from this client says it speaks per-writer
#: leases. The server flips a `leases` run to the legacy rules on the first
#: heartbeat, status write or logged batch WITHOUT it (an older client that will
#: never register a lease), so a lease-capable writer must never be mistaken
#: for one -- its CLI `probe log` and its attached ranks included.
LEASES_HEADER = "X-Probe-Leases"

#: 429 rides along: sixteen PUTs in flight make throttling ordinary, and a
#: throttled upload is a retry, not a verdict.
_RETRYABLE = {429, 502, 503, 504}

#: How far this machine's clock may be off the server's before the SDK says so.
#: HTTP `Date` has 1 s resolution and a response takes time to arrive, so the
#: threshold is generous on purpose.
CLOCK_SKEW_WARN_SECONDS = 60.0
#: Whether this process has compared its clock with a server `Date` yet.
_clock_checked = False


def _check_clock_skew(resp: httpx.Response) -> None:
    """Warn ONCE per process when this machine's clock is off the server's.

    ``Run.log`` dates every point with this machine's clock (plan 1.4) and
    findings bin by that date, so a wrong clock would shift a run's times with
    nothing saying why. Uses the first response that carries an HTTP ``Date``
    header. Never raises, and never corrects anything: a warning, not a clamp
    (PR #2002 review)."""
    global _clock_checked
    if _clock_checked:
        return
    date = resp.headers.get("date")
    if not date:
        return
    _clock_checked = True
    try:
        from datetime import datetime, timezone
        from email.utils import parsedate_to_datetime

        server = parsedate_to_datetime(date)
        if server.tzinfo is None:
            return
        skew = (datetime.now(timezone.utc) - server).total_seconds()
    except Exception:  # noqa: BLE001 -- a malformed header is not the caller's problem
        return
    if abs(skew) > CLOCK_SKEW_WARN_SECONDS:
        side = "ahead of" if skew > 0 else "behind"
        safe_warn.warn(
            f"probe: this machine's clock is {abs(skew):.0f} s {side} the server's "
            f"(HTTP Date: {date}). Metric points are dated with this clock, so their "
            "times will be shifted by that much. Fix the clock on this host (NTP)."
        )


def _warn_upload_inspection(response: httpx.Response) -> None:
    if 200 <= response.status_code < 300 and response.headers.get("x-probe-inspection-warning"):
        # A storage endpoint controls its response headers. Report the signal
        # using fixed text, never echo arbitrary remote content or credentials.
        warn_if_incomplete(
            InspectionResult(warnings=("server could not fully inspect artifact contents",))
        )


#: Route families whose create/change requests ARE recording research — the
#: writes the tracking auto-mark mirrors (see `_auto_mark_tracking`). Nested
#: routes (artifacts, notes, uploads) live under these prefixes, so they are
#: covered without being named. Kept conceptually in step with the CLI-command
#: vocabulary in plugins/probe-research/hooks/tracking_guard.py::WRITE_GROUPS —
#: that list names probe COMMANDS for the warn layer, this one names URL
#: families for the auto-mark, and both lean the same way: a miss costs
#: silence (no mark), never a false mark. Machine plumbing (/v1/tokens, auth,
#: capabilities, workspaces) is deliberately absent.
_RESEARCH_PATH_PREFIXES = (
    "/v1/projects",
    "/v1/experiments",
    "/v1/runs",
    "/v1/artifacts",
    "/ingest/",
)

#: Methods that only read. Everything else on a research path is a write.
_READ_METHODS = ("GET", "HEAD", "OPTIONS")

#: Cap on remembered sessions, so a long-lived transport (the hosted MCP serves
#: many callers through one) cannot grow a set forever. Forgetting is cheap and
#: safe: the session is re-checked on its next write, which costs one stat and
#: still cannot overwrite a decision.
_TRACKING_MEMO_CAP = 512


def _is_research_path(path: str) -> bool:
    """Whether this path is a research route, matched on SEGMENT boundaries.

    A bare prefix test would read `/v1/projects-search` as `/v1/projects`, so a
    future search-shaped POST under a look-alike name would flip tracking. The
    prefix must be the whole path or be followed by `/` or `?`.
    """
    for prefix in _RESEARCH_PATH_PREFIXES:
        if not path.startswith(prefix):
            continue
        rest = path[len(prefix) :]
        if not rest or rest[0] in "/?" or prefix.endswith("/"):
            return True
    return False


def _iter_file(fh, chunk_size: int, limit: int | None = None):
    """Yield an open binary file in fixed-size chunks -- a streaming upload body.

    With ``limit`` the body stops at that many bytes even if the file has grown
    since it was measured (a log appended to mid-upload): the declared
    Content-Length and the verified bytes stay the same thing. A file that
    SHRANK sends short and fails cleanly under Content-Length."""
    remaining = limit
    # Inside a `deadline_scope`, checked per chunk: httpx's timeouts bound each
    # socket operation, so an upload that keeps making slow progress would
    # otherwise never be cut. An unfinished body cannot have been applied.
    deadline = _request_deadline.get()
    while remaining is None or remaining > 0:
        if deadline is not None and time.monotonic() >= deadline:
            raise errors.DeadlineExceeded("upload: deadline passed mid-body")
        chunk = fh.read(chunk_size if remaining is None else min(chunk_size, remaining))
        if not chunk:
            break
        if remaining is not None:
            remaining -= len(chunk)
        yield chunk


_DEFAULT_TIMEOUT = 30.0
_MAX_RETRIES = 3

#: The transport's own in-request retries, on the one backoff ladder every
#: durable retry loop draws from (`durable.backoff_delays`): 0.2 s doubling to a
#: 2 s ceiling -- a blip's scale, since someone is usually waiting on the call.
_TRANSPORT_BACKOFF = (0.2, 2.0)

#: The longest server ``Retry-After`` one request waits out before retrying.
#: Longer asks go back to the caller at once, as the error's ``retry_after``,
#: for its own (longer-lived, deadline-aware) loop to honour.
_INLINE_RETRY_AFTER_MAX = 10.0


class Attribution(StrEnum):
    AMBIENT = "ambient"
    BACKFILL = "backfill"


_attribution_override: ContextVar[Attribution | None] = ContextVar(
    "probe_request_attribution", default=None
)


def resolve_attribution(value: str | None = None) -> Attribution:
    """An explicit client choice, also inherited by wizard subprocesses."""
    return Attribution(
        value if value is not None else os.environ.get("PROBE_ATTRIBUTION", Attribution.AMBIENT)
    )


@contextmanager
def attribution_scope(value: str):
    """Persisted outbox attribution, isolated between concurrent transports."""
    token = _attribution_override.set(Attribution(value))
    try:
        yield
    finally:
        _attribution_override.reset(token)


#: A monotonic deadline every request on THIS thread must respect, or None.
#: Set only through :func:`deadline_scope`.
_request_deadline: ContextVar[float | None] = ContextVar("probe_request_deadline", default=None)


@contextmanager
def deadline_scope(deadline: float | None):
    """Bound every request this thread makes to ``deadline`` (``time.monotonic()``).

    `Run.finish()` has ONE budget (plan 0.6). It used to be checked only after a
    whole flush returned, so a single stalled request -- or a slow backlog of
    successful ones -- could hold a close far past it (live: 170 s for
    ``flush_timeout=10``). Inside this scope each attempt's timeout is
    ``min(remaining, the transport's own timeout)``, a retry pause never
    outlives the deadline, and a request that would START after it raises
    :class:`errors.DeadlineExceeded` without being sent.

    A ContextVar, so it follows the call down through the outbox drain, the
    upload path and any client the drain builds for another context -- and
    stops at the thread: the heartbeat and every other thread keep their own
    timeouts. Nested scopes keep the EARLIER deadline.
    """
    if deadline is None:
        yield
        return
    outer = _request_deadline.get()
    token = _request_deadline.set(deadline if outer is None else min(outer, deadline))
    try:
        yield
    finally:
        _request_deadline.reset(token)


@contextmanager
def fresh_deadline_scope(deadline: float):
    """Bound this block by ``deadline`` ALONE, replacing any enclosing
    `deadline_scope` instead of keeping the earlier one. Only for a small,
    bounded, best-effort request that must still go out after the enclosing
    budget is spent -- the draining lease beat a deferred close sends
    precisely because its own budget ran out (`Run._draining_beat`)."""
    token = _request_deadline.set(deadline)
    try:
        yield
    finally:
        _request_deadline.reset(token)


#: Set by :func:`patience` to the deadline that was in force OUTSIDE it (often
#: None); `_NOT_PATIENT` everywhere else. Its presence is what turns the
#: deadline into a retry budget, and its value is what :func:`without_patience`
#: restores.
_NOT_PATIENT: Any = object()
_patience_outer: ContextVar[Any] = ContextVar("probe_transport_patience", default=_NOT_PATIENT)

#: The open patience scope's own record -- its budget and whether it has said
#: on stderr that it is retrying -- or None outside one.
_patience_state: ContextVar[dict | None] = ContextVar("probe_transport_patience_state", default=None)

#: A patient retry's wait: 0.5 s doubling to 10 s on the one ladder
#: (`durable.backoff_delays`), each jittered down to as little as half so ranks
#: retrying one outage fall out of step instead of arriving together.
_PATIENCE_BACKOFF = (0.5, 10.0)
#: The least time worth a last patient attempt.
_PATIENCE_LAST_ATTEMPT = 1.0

#: The jitter's own generator: drawing from `random`'s shared one would shift a
#: training script's seeded stream. Seeded from the OS, and again in every
#: forked child, so ranks forked from one parent do not back off in lockstep.
_JITTER = random.Random()
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_JITTER.seed)


def _patient() -> bool:
    return _patience_outer.get() is not _NOT_PATIENT


@contextmanager
def patience(seconds: float | None):
    """Retry for up to ``seconds`` of wall clock instead of ``max_retries`` quick tries.

    For the moment a process cannot go on without an answer -- ``probe.init()``
    opening its run (plan 2.5) -- where one refused connection raised into the
    training script after 1.9 s and a blackholed API after 122 s (measured).

    Built on :func:`deadline_scope`, so everything that holds there holds here:
    each attempt's timeout is capped at the time left, and nothing is sent once
    it is spent. What patience adds, for :meth:`Transport.request` only:

    * retries are bounded by the deadline, not by ``max_retries``;
    * the waits come from `_PATIENCE_BACKOFF`, jittered, and a ``Retry-After``
      is waited out whenever the budget still has room for it;
    * WHAT is retried does not change: connect-class failures always, anything
      else only when the request is idempotent, and never an answer outside
      `_RETRYABLE` (401/403/404/409/422 come back on the first try). A write
      that may already have landed is never re-sent blind.

    ``seconds`` None or <= 0 is today's behaviour (no scope at all). Best-effort
    work inside the scope opts out with :func:`without_patience`.
    """
    if seconds is None or seconds <= 0:
        yield
        return
    token = _patience_outer.set(_request_deadline.get())
    state_token = _patience_state.set({"seconds": float(seconds), "announced": False})
    try:
        with deadline_scope(time.monotonic() + float(seconds)):
            yield
    finally:
        _patience_state.reset(state_token)
        _patience_outer.reset(token)


@contextmanager
def without_patience():
    """Suspend an enclosing :func:`patience` scope -- `probe.init()`'s budget --
    for a block. Requests inside get the transport's own timeouts and quick
    retries again, and the deadline that was in force OUTSIDE patience (if any,
    e.g. a close's) comes back; no init deadline cuts them off.

    The door for any step inside `probe.init()` that may legitimately outlast
    the init budget, or must not spend it:

    * best-effort capture after the run is open (the code snapshot, the
      hardware rail, output capture -- `Client.run`);
    * threads started during init (the heartbeat): a thread that inherits its
      creator's context (free-threaded 3.14) would otherwise carry the init
      deadline for the life of the run;
    * a deliberate long wait, such as a requeue takeover that waits for a dead
      incumbent (plan 2.3), which has its own bound (`PROBE_TAKEOVER_WAIT_SEC`).

    A no-op outside a patience scope. ``tests/test_init_resilience.py`` pins
    that a step wrapped in it survives a wait longer than the whole budget."""
    outer = _patience_outer.get()
    if outer is _NOT_PATIENT:
        yield
        return
    deadline_token = _request_deadline.set(outer)
    patience_token = _patience_outer.set(_NOT_PATIENT)
    state_token = _patience_state.set(None)
    try:
        yield
    finally:
        _patience_state.reset(state_token)
        _patience_outer.reset(patience_token)
        _request_deadline.reset(deadline_token)


def deadline_remaining(default: float) -> float:
    """Seconds left in this thread's `deadline_scope`, never more than
    ``default``; ``default`` itself outside a scope. For local waits (a scan, a
    lock) that must share a close's one budget without being requests."""
    deadline = _request_deadline.get()
    if deadline is None:
        return default
    return max(0.0, min(default, deadline - time.monotonic()))


def _retry_after_seconds(resp: httpx.Response) -> float | None:
    """The server's ``Retry-After`` in seconds (delta-seconds or an HTTP-date,
    RFC 9110 10.2.3), or None when absent or unreadable. Never negative."""
    raw = (resp.headers.get("Retry-After") or "").strip()
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        from datetime import datetime, timezone
        from email.utils import parsedate_to_datetime

        when = parsedate_to_datetime(raw)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


#: Answers a gateway gives IN PLACE of the app's: the request may have been
#: processed and only its response lost.
_AMBIGUOUS_STATUSES = frozenset({502, 503, 504})


def outcome_unknown(exc: BaseException) -> bool:
    """Whether a failed request may still have been PROCESSED by the server.

    A read timeout, a dropped connection or a protocol error after the request
    left, a deadline that cut only the response, or a 502/503/504 from whatever
    sits in front of the app: the write may have landed and only its answer was
    lost. A connect-class failure is not unknown (the request never left), nor
    is any answer the app itself gave. Only a request that is safe to send twice
    -- a run create carrying its `creation_key` on a server that declares
    `run_creation_key` (plan 2.5) -- may be re-sent after one of these."""
    if isinstance(exc, errors.DeadlineExceeded):
        return exc.sent
    if isinstance(exc, errors.TransportError):
        cause = exc.__cause__
        return isinstance(cause, httpx.HTTPError) and not isinstance(cause, _CONNECT_ERRORS)
    return isinstance(exc, errors.RosError) and exc.status in _AMBIGUOUS_STATUSES


def _announce_patience(status: int | None) -> None:
    """One stderr line when a patience scope first retries, so a job that is
    quietly waiting on the API does not look hung."""
    state = _patience_state.get()
    if state is None or state.get("announced"):
        return
    state["announced"] = True
    why = f"answered {status}" if status else "is not reachable"
    try:
        print(
            f"probe: the Probe API {why}; probe.init() keeps retrying for up to "
            f"{state['seconds']:g}s (PROBE_INIT_TIMEOUT_SEC)",
            file=sys.stderr,
            flush=True,
        )
    except Exception:  # noqa: BLE001 -- a notice may never break the retry
        pass


def wait_out_retry_after(exc: BaseException, *, minimum: float = 0.0) -> bool:
    """Wait the ``Retry-After`` a failure carried (``RosError.retry_after``), at
    least ``minimum``, before the caller sends again. False -- without waiting
    -- when that wait does not fit: the caller then raises the failure it has
    at once, rather than sleeping an hour (a ``Retry-After: 3600``) or sleeping
    out its whole budget only to raise anyway.

    What "fits" is the transport's own rule for the same header
    (`Transport._retry_pause`), so a create and a read answered alike wait
    alike. Inside :func:`patience` (init's budget) the ONE bound is the budget
    left, less room for the attempt after the wait (`_patient_pause`): a
    ``Retry-After: 30`` 10 s into a 90 s budget is waited out. Outside one,
    anything over `_INLINE_RETRY_AFTER_MAX` -- or over this thread's
    deadline -- is not."""
    asked = getattr(exc, "retry_after", None)
    wait = max(float(minimum), float(asked or 0.0))
    deadline = _request_deadline.get()
    if _patient() and deadline is not None:
        if wait > deadline - time.monotonic() - _PATIENCE_LAST_ATTEMPT:
            return False
        _announce_patience(getattr(exc, "status", None))
    else:
        if wait > _INLINE_RETRY_AFTER_MAX:
            return False
        if deadline is not None and deadline - time.monotonic() <= wait:
            return False
    if wait > 0:
        time.sleep(wait)
    return True


def _with_retry_after(error: errors.RosError, resp: httpx.Response) -> errors.RosError:
    """Carry the response's ``Retry-After`` on the error the caller will see, so
    every retry loop above (the outbox worker, the exporter, `finish()`) can
    wait at least as long as the server asked (plan 0.4/0.6)."""
    wait = _retry_after_seconds(resp)
    if wait is not None:
        error.retry_after = wait
    return error


#: Cap on the CONNECT phase, independent of the overall timeout. A dead or
#: black-holing endpoint used to park a caller for the full 30s per request,
#: which in a training loop is long enough to trip a distributed collective
#: while every rank waits on the same stalled POST. Reads keep the full budget:
#: a slow query is worth waiting for, an unreachable host is not.
_DEFAULT_CONNECT_TIMEOUT = 5.0

#: Failures that prove the request never reached the server: the connection was
#: never established, or it never left the pool. Retrying these is safe for ANY
#: method, because there is no chance the server processed a first attempt.
#:
#: Deliberately NOT here: ReadTimeout and RemoteProtocolError. Those mean the
#: request was already on the wire and only the RESPONSE was lost, so a retry of
#: a non-idempotent write can duplicate it -- a metric batch appended twice is
#: silent data corruption, which is worse than the error it would have avoided.
_CONNECT_ERRORS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
)


def _blob_label(url: str) -> str:
    """A presigned URL reduced to host + path.

    The query string carries the signature, so it never enters the buffer. What
    is left is what a reader actually needs: which store, which object.
    """
    try:
        parts = urlsplit(url)
        return f"{parts.netloc}{parts.path}"
    except Exception:
        return "<blob>"


def _presigned_put_error(resp: httpx.Response, url: str) -> errors.RosError:
    """The error for a presigned PUT's failed answer. 401/403 is the upload's
    own capability refused, not the credential (none was sent): `UploadRefused`
    (#2073). Everything else maps as on any request."""
    if resp.status_code in (401, 403):
        detail = resp.text
        try:
            parsed = resp.json()
            if isinstance(parsed, dict) and parsed.get("detail") is not None:
                detail = parsed["detail"]
        except ValueError:
            pass
        message = (
            f"upload to {_blob_label(url)} refused ({resp.status_code}): "
            f"{errors._detail_message(detail)[:300]}. A presigned upload carries no "
            "credential, so this refuses the upload's signed URL, not your login; a "
            "self-hosted server must set public_base_url to its own address"
        )
        return _with_retry_after(
            errors.UploadRefused(message, status=resp.status_code, detail=detail), resp
        )
    return _with_retry_after(errors.error_for(resp.status_code, resp.text), resp)


def _instrumented(verb: str):
    """Bracket a blob transfer so the ring buffer can see it.

    These are the longest-running requests the SDK makes -- artifact and weight
    transfers -- and therefore the likeliest to stall, but only `request()` was
    instrumented, so the stall detector was blind to exactly the traffic most
    able to park a training loop.
    """

    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(self, url, *args, **kwargs):
            started = time.monotonic()
            label = _blob_label(url)
            base = self.settings.base_url
            _diagnostics.begin_transport(verb, label, base=base)
            error = None
            try:
                return fn(self, url, *args, **kwargs)
            except BaseException as exc:
                error = repr(exc)
                raise
            finally:
                _diagnostics.end_transport()
                _diagnostics.record_transport(
                    verb, label, seconds=time.monotonic() - started, error=error, base=base
                )

        return wrapper

    return decorate


@dataclass
class Page:
    """A list response plus the opaque keyset cursor for the next page."""

    items: list[Any]
    next_cursor: str | None


#: Surfaces that genuinely run ON the machine they are reporting. The MCP is
#: excluded and that is not an oversight: `_client_for_token` is shared by the
#: local stdio server and the HOSTED one, and the hosted server memoizes a
#: transport per token while serving many people through it -- so a device
#: identity fixed there would report our pod as every caller's machine, the exact
#: bug `client_headers_scope` was introduced to prevent for versions.
#:
#: The cost is that an MCP-only report carries no device. The server closes that
#: gap from its side: `current_client_versions` resolves a device-less report
#: through the token's live device bindings when exactly one device holds it, so
#: the plugin's version still lands on the right machine instead of rendering as
#: a second one.
_DEVICE_REPORTING_SURFACES = frozenset({Surface.CLI.value, Surface.SDK.value})


def _device_headers_for(surface: str) -> dict[str, str]:
    """The machine header for a transport on THIS host, or nothing.

    Fail-quiet. A machine whose identity file cannot be read or written reports
    as a client that predates device identity -- a supported state, not an error
    worth failing a research write over.
    """
    if surface not in _DEVICE_REPORTING_SURFACES:
        return {}
    try:
        from .device_identity import device_instance_id

        return device_headers(device_instance_id())
    except Exception:  # noqa: BLE001 - identity is telemetry, never a hard failure
        return {}


def _is_trash_notice(resp: httpx.Response) -> bool:
    """The server's 410 for a run, group, experiment or project in its TRASH."""
    if resp.status_code != 410:
        return False
    try:
        body = resp.json()
    except (json.JSONDecodeError, ValueError):
        return False
    return isinstance(body, dict) and body.get("detail") == "in_trash"


class Transport:
    def __init__(
        self,
        settings: Settings,
        *,
        timeout: float = _DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
        max_retries: int = _MAX_RETRIES,
        surface: str = Surface.SDK.value,
        client_headers: Mapping[str, str] | None = None,
        attribution: str | None = None,
    ):
        self.settings = settings
        self.attribution = resolve_attribution(attribution)
        self.max_retries = max_retries
        #: The per-request budget outside a deadline scope; inside one, each
        #: attempt gets ``min(this, what is left)`` (see `deadline_scope`).
        self.timeout = timeout
        # Which product surface these requests came from (cli/sdk/mcp). Every
        # backend request carries it as `X-Probe-Surface` so analytics can
        # attribute events by surface — headers only, never a payload.
        self.surface = surface
        supplied = client_headers or {}
        if not supplied and surface == Surface.SDK.value:
            # A generic SDK transport reports ITSELF. This used to send nothing,
            # deliberately -- the rule was that only a caller who knew what it
            # was could name a kind, and the SDK had no kind of its own to name.
            # The cost was a blind spot exactly where it hurts: `import probe` in
            # a training script is the install that never opens a terminal, never
            # starts an agent session, and therefore never appears in any
            # fleet-shaped view. It reports the version of the one
            # `probe-research` distribution it shares with the CLI.
            #
            # An EXPLICIT `client_headers` still wins, so the CLI and the hosted
            # MCP (which must speak for their caller, not for this process) are
            # untouched. Only the unspecified default changed.
            from .. import __version__

            supplied = client_version_headers(Surface.SDK.value, __version__)
        self._client_headers = client_version_headers(
            supplied.get(CLIENT_KIND_HEADER),
            supplied.get(CLIENT_VERSION_HEADER),
        )
        # WHICH MACHINE this process is running on, resolved once per transport.
        #
        # Fixed at construction ON PURPOSE, unlike the version identity above:
        # the device file describes the host, and a local process cannot be
        # running on two machines. The hosted MCP is the case that must NOT send
        # it, and it does not reach here with one -- see `_device_headers`.
        self._device_headers = _device_headers_for(surface)
        self._client = client or httpx.Client(
            base_url=settings.base_url,
            timeout=httpx.Timeout(timeout, connect=min(timeout, _DEFAULT_CONNECT_TIMEOUT)),
            verify=ssl_context(),
        )
        # Sessions whose tracking signal this transport has already settled —
        # keyed per SESSION, not per transport: the hosted MCP memoizes one
        # transport per token and serves many callers through it, so a single
        # boolean would let the first caller's session answer for everyone.
        self._tracking_marked: set[str] = set()

    # -- lifecycle ----------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Transport":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- auth ---------------------------------------------------------------
    def _auth_headers(self, path: str, raw_body: bytes) -> dict[str, str]:
        headers: dict[str, str] = {}
        is_ingest = path.startswith("/ingest")
        if is_ingest:
            if not self.settings.ingest_token:
                raise errors.AuthError("no ingest token configured (set PROBE_INGEST_TOKEN)")
            headers["Authorization"] = f"Bearer {self.settings.ingest_token}"
            if self.settings.hmac_secret:
                sig = hmac.new(
                    self.settings.hmac_secret.encode(), raw_body, hashlib.sha256
                ).hexdigest()
                headers["X-Signature"] = f"sha256={sig}"
        else:
            # /v1 accepts a user PAT (probe_pat_) OR a read-only service token
            # (probe_svc_); the backend dispatches on the prefix. A Reader carries
            # only the service token.
            bearer = self.settings.token or self.settings.service_token
            if not bearer:
                if os.environ.get("PROBE_CONFIG_PATH") == DAEMON_SHELL_CONFIG:
                    raise errors.AuthError(
                        "no API token here: this is the Probe daemon's shell, which has no Probe key on "
                        "purpose. Run the probe command as a command of its own (`probe ...`, or chained: "
                        "`cd x && probe ...`): the daemon writes to Probe only that way, with its checks."
                    )
                raise errors.AuthError(
                    f"no API token configured ({session_marker.WIZARD_HINT}, or set "
                    "PROBE_SERVICE_TOKEN)"
                )
            headers["Authorization"] = f"Bearer {bearer}"
        return headers

    # -- deadline -------------------------------------------------------------
    def _attempt_timeout(self, requested: float | None, what: str) -> tuple[Any, bool]:
        """``(timeout kwarg value, clamped)`` for one attempt.

        Outside a :func:`deadline_scope` this is ``requested`` untouched (None
        keeps the client-wide budget) and ``clamped`` is False. Inside one it is
        ``min(requested or self.timeout, remaining)``, and ``clamped`` says the
        deadline -- not the transport -- set the bound. Raises
        :class:`errors.DeadlineExceeded` when nothing is left: the request is
        never sent."""
        deadline = _request_deadline.get()
        if deadline is None:
            return requested, False
        left = deadline - time.monotonic()
        if left <= 0:
            raise errors.DeadlineExceeded(f"{what}: deadline passed before it was sent")
        base = float(self.timeout if requested is None else requested)
        bound = min(base, left)
        return httpx.Timeout(bound, connect=min(bound, _DEFAULT_CONNECT_TIMEOUT)), bound < base

    @staticmethod
    def _retry_pause(attempt: int, resp: httpx.Response | None = None) -> bool:
        """Sleep before retry ``attempt + 1``; False, without sleeping, when that
        retry must not happen here -- the caller then raises the failure it has.

        The wait is the transport's step on the one backoff ladder
        (`durable.backoff_delays`, `_TRANSPORT_BACKOFF`: 0.2 s doubling to 2 s),
        LENGTHENED to the server's ``Retry-After`` when ``resp`` carries one
        (plan 0.4/0.6: the server sends a jittered one on a lock timeout, and 5 s
        on `entitlement_unavailable`). It never retries sooner than asked:

        * a ``Retry-After`` longer than `_INLINE_RETRY_AFTER_MAX` is not waited
          out inside one request -- the error goes back at once carrying
          ``retry_after``, and the caller's own loop (the outbox worker, the
          exporter, `finish()`, each with its own ceiling and deadline) waits;
        * inside a `deadline_scope` with no room for the wait AND another
          attempt, it does not retry at all rather than retry early.
        """
        deadline = _request_deadline.get()
        retry_after = _retry_after_seconds(resp) if resp is not None else None
        if _patient() and deadline is not None:
            return Transport._patient_pause(
                attempt, retry_after, deadline, status=resp.status_code if resp is not None else None
            )
        (*_, delay) = durable.backoff_delays(attempt + 1, _TRANSPORT_BACKOFF)
        if retry_after is not None and retry_after > _INLINE_RETRY_AFTER_MAX:
            return False
        pause = durable.honor_retry_after(delay, retry_after, ceiling=_INLINE_RETRY_AFTER_MAX)
        if deadline is not None and deadline - time.monotonic() <= pause:
            return False
        time.sleep(pause)
        return True

    @staticmethod
    def _patient_pause(
        attempt: int, retry_after: float | None, deadline: float, *, status: int | None = None
    ) -> bool:
        """`_retry_pause` inside :func:`patience`: the jittered `_PATIENCE_BACKOFF`
        step, lengthened to any ``Retry-After`` the budget can still hold, and
        shortened so a last attempt fits before the deadline. False when there
        is no room for one. The scope's FIRST retry says so, once, on stderr."""
        room = deadline - time.monotonic() - _PATIENCE_LAST_ATTEMPT
        if room <= 0 or (retry_after is not None and retry_after > room):
            return False
        _announce_patience(status)
        (*_, step) = durable.backoff_delays(attempt + 1, _PATIENCE_BACKOFF)
        jittered = step / 2 + _JITTER.uniform(0, step / 2)
        time.sleep(min(durable.honor_retry_after(jittered, retry_after, ceiling=room), room))
        return True

    def _may_retry(self, attempt: int) -> bool:
        """The COUNT half of the retry decision: ``max_retries`` quick tries, or,
        inside :func:`patience`, as many as the deadline allows."""
        return attempt <= self.max_retries or _patient()

    @staticmethod
    def _deadline_error(what: str, exc: BaseException) -> errors.DeadlineExceeded:
        """The deadline cut an attempt: ``sent`` when only the response was lost
        (a read timeout), so the server may have applied the request."""
        return errors.DeadlineExceeded(f"{what}: {exc}", sent=isinstance(exc, httpx.ReadTimeout))

    def _send_within_deadline(self, deadline: float, method: str, path: str, **kwargs) -> httpx.Response:
        """Send, then read the body chunk by chunk, checking ``deadline`` between
        chunks. httpx's timeouts bound each socket operation, not the request:
        a response that trickles a byte at a time never trips one (live: a
        close with ``flush_timeout=2`` took 9.8 s). Returns an ordinary,
        fully-read response."""
        with self._client.stream(method, path, **kwargs) as resp:
            if resp.is_stream_consumed:  # an in-memory transport already read it
                resp.read()
                return resp
            chunks: list[bytes] = []
            for chunk in resp.iter_raw():
                chunks.append(chunk)
                if time.monotonic() >= deadline:
                    raise errors.DeadlineExceeded(
                        f"{method} {path}: deadline passed while reading the response", sent=True
                    )
        return httpx.Response(
            resp.status_code,
            headers=resp.headers,
            content=b"".join(chunks),
            request=resp.request,
            extensions=resp.extensions,
        )

    @staticmethod
    def _cut_by_deadline(exc: BaseException, clamped: bool) -> bool:
        """A timeout that fired only because the deadline shortened the attempt:
        our clock ran out, not the server's patience."""
        deadline = _request_deadline.get()
        return (
            clamped
            and deadline is not None
            and isinstance(exc, httpx.TimeoutException)
            and time.monotonic() >= deadline
        )

    # -- core request -------------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any | None = None,
        params: dict[str, Any] | None = None,
        idempotent: bool | None = None,
        timeout: float | None = None,
    ) -> httpx.Response:
        # Validate structure before the recursive scrubber. Scan the normalized
        # body again below: sets/opaque reprs may become new JSON strings.
        if unstorable.has_nul(params) or ("\x00" in path):
            raise errors.ValidationError("probe: NUL in request path or query", status=422)
        if json_body is not None:
            json_body = unstorable.normalize_json(json_body)
            unstorable.validate_nuls(json_body, path=path, method=method)
        # Every JSON upload crosses this boundary, including creates and
        # replay paths that bypass Client.write. A scrub failure must happen
        # before serialization/auth/network; never retry with the original.
        # `scrub_body`: `default_scrub`, minus the ISO timestamps `Run.log`
        # stamps on every point (plan 1.4), which cannot hold a credential.
        from .stamp_scrub import scrub_body

        if json_body is not None:
            original = json_body
            json_body = scrub_body(original)
            # These synchronous account endpoints intentionally enroll a W&B
            # credential. Preserve only their declared authentication field;
            # notes/metadata and every adjacent route remain scrubbed. Durable
            # journals never receive an exemption for these paths.
            enrollment = method.upper() == "POST" and re.fullmatch(
                r"/v1/integrations/wandb/accounts(?:/"
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/reconnect)?",
                path,
            )
            if enrollment and isinstance(original, dict):
                credentials = original.get("credentials")
                if isinstance(credentials, dict) and isinstance(credentials.get("api_key"), str):
                    json_body["credentials"] = {"api_key": credentials["api_key"]}
            # A read-only SQL query is sent AS WRITTEN. Scrubbing rewrites a
            # literal, so `WHERE name = 'sk-baseline'` (a plausible run name)
            # became `'<redacted>'` and counted the wrong thing -- a silently
            # wrong answer. The route executes and discards the text; nothing
            # stores it, and the dashboard already sends it unscrubbed.
            if (
                method.upper() == "POST"
                and path == "/v1/sql"
                and isinstance(original, dict)
                and isinstance(original.get("sql"), str)
            ):
                json_body["sql"] = original["sql"]
        # Scrub BEFORE display escaping: a NUL must not become a word character
        # that hides a neighboring credential from the scrubber's boundaries.
        if json_body is not None:
            json_body, escaped = unstorable.escape_nuls(json_body, path=path, method=method)
            if escaped:
                safe_warn.warn(unstorable.describe(escaped), stacklevel=1)
        # Serialize ourselves so the HMAC signs the exact sanitized bytes.
        raw_body = b"" if json_body is None else json.dumps(json_body).encode()
        # Client identity: what this transport was built with, unless the caller
        # bound a per-request override. Read per-request for the same reason
        # `current_tool()` below is: the hosted MCP memoizes one transport per
        # token and serves many callers through it, so an identity fixed at
        # construction would report the SERVER's version as every caller's.
        # An empty override is a real answer ("this caller reported nothing"),
        # so only None falls back.
        override = current_client_headers()
        client_identity = self._client_headers if override is None else override
        # A per-request client-identity override means we are speaking FOR
        # someone else (the hosted MCP serving a remote caller). This process's
        # machine is not theirs, so the device header drops out with it --
        # sending it would attribute every caller's traffic to the server's own
        # pod, which is the precise bug `client_headers_scope` exists to prevent.
        device_identity = self._device_headers if override is None else {}
        headers = {
            **client_identity,
            **device_identity,
            **self._auth_headers(path, raw_body),
        }
        if json_body is not None:
            headers["Content-Type"] = "application/json"
        # Surface attribution: tag every backend request with the originating
        # product surface, and (MCP only) the tool being served. Headers only.
        headers[SURFACE_HEADER] = self.surface
        headers[LEASES_HEADER] = "1"
        tool = current_tool()
        if tool:
            headers[TOOL_HEADER] = tool
        # Coding-agent session attribution. Read per-request rather than cached
        # at construction: a long-lived client outlives any single session, and
        # a stale id would attribute new runs to a finished conversation.
        # Returns {} when there is no capturable session, so absent means NO
        # header rather than an empty one.
        attribution = _attribution_override.get() or self.attribution
        if attribution is Attribution.AMBIENT:
            headers.update(agent_session_headers())
        key = _idempotency_key(method, path)
        if key:
            headers["Idempotency-Key"] = key

        retry = idempotent if idempotent is not None else method.upper() in {"GET", "PUT"}
        # Wall time as the CALLER experiences it, retries included: what parks a
        # training loop is the total, not any single attempt.
        started = time.monotonic()
        # Mark it in flight BEFORE the call. A request that hangs until the
        # process is killed never reaches either recording site below, so
        # without this the evidence for the exact failure the ring buffer exists
        # to catch is the one thing it cannot show.
        _diagnostics.begin_transport(method, path, base=self.settings.base_url)
        attempt = 0
        while True:
            attempt += 1
            try:
                # Per-call override for the rare request whose SERVER-side work
                # legitimately outlasts the default (a large rewind deletes
                # millions of rows in its transaction). None keeps the
                # client-wide budget -- unless a deadline scope bounds it.
                attempt_timeout, clamped = self._attempt_timeout(timeout, f"{method} {path}")
            except errors.DeadlineExceeded:
                _diagnostics.end_transport()
                raise
            send = dict(
                content=raw_body if json_body is not None else None,
                params=params,
                headers=headers,
                **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
            )
            deadline = _request_deadline.get()
            try:
                if deadline is None:
                    resp = self._client.request(method, path, **send)
                else:
                    resp = self._send_within_deadline(deadline, method, path, **send)
            except errors.DeadlineExceeded:
                _diagnostics.end_transport()
                raise
            except RuntimeError as exc:
                # httpx refuses to send on a CLOSED client with a bare
                # RuntimeError. It is a delivery failure like any other: every
                # caller treats a TransportError as "not sent, try later", and
                # a RuntimeError escaped a non-strict finish() (re-review of
                # #2011). Anything else stays a programming error.
                if not self._client.is_closed:
                    raise
                _diagnostics.end_transport()
                raise errors.TransportError(f"{method} {path}: {exc}") from exc
            except httpx.HTTPError as exc:
                # A connect-class failure never reached the server, so it is
                # replayable whatever the method: this is what keeps one blip on
                # a metrics POST from becoming a hard error. Anything else stays
                # gated on `retry`, because the request may already have landed.
                replayable = retry or isinstance(exc, _CONNECT_ERRORS)
                if replayable and self._may_retry(attempt) and self._retry_pause(attempt):
                    continue
                _diagnostics.end_transport()
                _diagnostics.record_transport(
                    method,
                    path,
                    seconds=time.monotonic() - started,
                    error=repr(exc),
                    base=self.settings.base_url,
                )
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"{method} {path}", exc) from exc
                failure = errors.TransportError(f"{method} {path}: {exc}")
                # The server was never reached: nobody's op can land, so the
                # outbox drain ends the pass for every run, not only this one
                # (plan 1.6). A timeout AFTER sending may be this op's own.
                failure.unreachable = isinstance(exc, _CONNECT_ERRORS)
                raise failure from exc

            _check_clock_skew(resp)
            if (
                resp.status_code in _RETRYABLE
                and retry
                and self._may_retry(attempt)
                and self._retry_pause(attempt, resp)
            ):
                continue

            _diagnostics.end_transport()
            _diagnostics.record_transport(
                method,
                path,
                seconds=time.monotonic() - started,
                status=resp.status_code,
                base=self.settings.base_url,
            )
            if override is None:
                # Only for our OWN identity: under an override (the hosted MCP)
                # the status grades someone else's client, not this process.
                client_status.notice(resp.headers, client_identity, self.surface)
            if resp.status_code >= 400:
                if attempt > 1 and method.upper() == "DELETE" and _is_trash_notice(resp):
                    # A RETRIED delete that finds the thing in the trash: the
                    # first attempt landed and its reply was lost. That is the
                    # delete succeeding, not a refusal; the notice is the answer.
                    return resp
                raise self._to_error(resp)
            if 200 <= resp.status_code < 300:
                # 2xx only: a 3xx means the write did not land where we asked.
                self._auto_mark_tracking(method, path, headers.get(AGENT_SESSION_HEADER))
            return resp

    def _auto_mark_tracking(self, method: str, path: str, session_id: str | None) -> None:
        """First research write of a coding-agent session SETTLES its tracking
        signal, at the process cwd's effective default, so the local surfaces
        stop disagreeing with the backend about whether the session is tracked.
        AFTER success on purpose: a write that never landed marks nothing, and
        a server-commit the client never saw heals on the next successful
        write.

        It settles at the DEFAULT, not at `on`. A write is the agent's act, not
        the researcher's declaration, so it may record which value this session
        started at -- it may never change that value. On a default-off machine
        this therefore writes `off`, and the warn layer keeps warning about the
        write that just happened, which is the honest reading of it. Since
        SessionStart already seeds the same value, this is normally a no-op; it
        still covers a session that started before the seed shipped.

        Three things never mark: reads, non-research routes (see
        `_RESEARCH_PATH_PREFIXES`), and a session held down by the
        `PROBE_SESSION_TRACKING` env override — an explicit signal file would
        outlive and defeat a machine-wide forced-off, so while the env holds
        the setting (EITHER direction) this writes nothing. An explicit
        per-session decision is never touched either; that is the helper's own
        contract.

        ONLY A SETTLED SESSION IS REMEMBERED. `set_tracking_if_absent` returns
        False both for "a decision already exists" and for a transient I/O
        failure (read-only state dir, full disk), so caching on False alone
        would turn one bad moment into a permanently unmarked session for the
        life of this transport. A failure is not remembered; it costs one extra
        stat on the next write and then resolves itself.

        Fail-soft: the auto-mark must never break the write it rides on, so any
        surprise is swallowed — and not remembered, for the same reason.
        """
        if not session_id or session_id in self._tracking_marked:
            return
        if method.upper() in _READ_METHODS:
            return
        if not _is_research_path(path):
            return
        try:
            # Normal path: SessionStart already settled the signal. Read it
            # before resolving any default so a later folder edit cannot add
            # ancestor I/O to every successful write in an existing session.
            if session_marker.tracking_signal(session_id) is not None:
                settled = True
            elif session_marker.tracking_env_override() is not None:
                settled = True  # held by the env for this process's lifetime
            elif session_marker.set_tracking_if_absent(
                session_id, session_marker.resolve_tracking_default(None)[0]
            ):
                settled = True  # this call decided it
            else:
                # False is ambiguous: a decision exists, or the write failed.
                settled = session_marker.tracking_signal(session_id) is not None
        except Exception:  # noqa: BLE001 - by the fail-soft contract above
            return
        if not settled:
            return
        if len(self._tracking_marked) >= _TRACKING_MEMO_CAP:
            self._tracking_marked.clear()
        self._tracking_marked.add(session_id)

    def _to_error(self, resp: httpx.Response) -> errors.RosError:
        try:
            body = resp.json()
            detail = body.get("detail")
            if body.get("code") == errors.CLIENT_TOO_OLD:
                min_version = body.get("min_version")
                min_version = min_version if isinstance(min_version, str) else None
                return errors.ClientTooOldError(
                    errors.upgrade_message(errors._detail_message(detail), min_version),
                    status=resp.status_code,
                    detail=detail,
                    min_version=min_version,
                )
            # A run, group, experiment or project in the server's TRASH answers
            # 410 with a fixed token and the notice beside it ("in the trash
            # since ..., Probe can restore it until ..."). The sentence is what a
            # person or an agent needs to read; the token alone says nothing.
            in_trash = detail == "in_trash"
            if in_trash and isinstance(body.get("message"), str):
                detail = body["message"]
        except (json.JSONDecodeError, ValueError, AttributeError):
            detail, in_trash = resp.text, False
        error = errors.error_for(resp.status_code, detail)
        if in_trash:
            error.in_trash = True
        return _with_retry_after(error, resp)

    # -- typed helpers ------------------------------------------------------
    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params, idempotent=True).json()

    def post(self, path: str, json_body: Any | None = None, *, idempotent: bool = False) -> Any:
        resp = self.request("POST", path, json_body=json_body, idempotent=idempotent)
        return resp.json() if resp.content else None

    def patch(self, path: str, json_body: Any) -> Any:
        return self.request("PATCH", path, json_body=json_body).json()

    def put(self, path: str, json_body: Any) -> Any:
        return self.request("PUT", path, json_body=json_body, idempotent=True).json()

    def delete(self, path: str) -> Any:
        """Returns the parsed body when the route sends one (a run, group or
        project delete answers where it went in the trash and until when; a
        retried one that finds it already there answers the trash notice), and
        None on a 204."""
        resp = self.request("DELETE", path, idempotent=True)
        if not resp.content:
            return None
        try:
            return resp.json()
        except (json.JSONDecodeError, ValueError):
            # A 2xx with a non-JSON body (an ingress/CDN HTML interstitial in front of
            # the API) must not escape as a raw JSONDecodeError; the delete succeeded.
            return None

    def get_page(self, path: str, *, params: dict[str, Any] | None = None) -> Page:
        resp = self.request("GET", path, params=params, idempotent=True)
        return Page(items=resp.json(), next_cursor=resp.headers.get("X-Next-Cursor"))

    @_instrumented("PUT")
    def put_url(
        self,
        url: str,
        data: bytes,
        *,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Raw PUT of bytes to a presigned URL (artifact upload, fold #16).

        No Authorization header: the presigned URL carries its own signature. This
        goes to an absolute URL (R2), not the API base; retried on network blips."""
        # No local content scan: these bytes are pinned by the presigned digest,
        # so a scan could only warn, and the server inspects every upload and
        # returns its own warning (`_warn_upload_inspection` below).
        data = bytes(data)
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                resp = self._client.put(
                    url,
                    content=data,
                    headers=request_headers,
                    **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @freeze_upload
    def put_file(
        self,
        url: str,
        path: str,
        *,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
        chunk_size: int = 1 << 20,
    ) -> None:
        """Stream a local file to a presigned URL without buffering it in memory.

        The sibling of :meth:`put_url` for bytes you do NOT want in memory -- an
        anchored artifact can be model weights, and reading the whole file into a
        ``bytes`` before the PUT is what OOMs the training loop.

        Content-Length is measured from the open file on every attempt, never taken
        from a caller-supplied size. A generator body otherwise makes httpx use
        ``Transfer-Encoding: chunked`` (a presigned R2/S3 PUT rejects it, 411), and a
        declared length that disagrees with the bytes actually streamed frames the PUT
        wrong -- a short header truncates the stored object, a long one hangs the
        connection waiting for bytes that never come. Deriving the length from the same
        handle we stream keeps header and body structurally in lockstep, exactly as the
        old buffered ``put_url(len(data))`` path did.

        Re-opens ``path`` on every attempt: httpx does not rewind a consumed body, so a
        retry after a network blip or a retryable status must stream from byte 0 again
        -- passing a spent file handle would send a truncated body that the server then
        stores and confirms as complete. No Authorization header; the presigned URL
        carries its own signature."""
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                with open(path, "rb") as fh:
                    request_headers["Content-Length"] = str(os.fstat(fh.fileno()).st_size)
                    resp = self._client.put(
                        url,
                        content=_iter_file(fh, chunk_size),
                        headers=request_headers,
                        **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                    )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @_instrumented("PUT")
    def put_part(
        self,
        url: str,
        path: str,
        *,
        offset: int,
        length: int,
        chunk_size: int = 1 << 20,
    ) -> str | None:
        """PUT bytes ``[offset, offset + length)`` of ``path`` to a presigned
        multipart PART URL (plan item (g)); returns the store's ETag.

        THE ONE BYTE PATH WITH NO LOCAL CREDENTIAL GATE, on purpose. Every other
        upload goes through `freeze_upload` / `freeze_stream`, which read the
        whole body, refuse anything over the 64 MiB inspection limit and may
        redact it. A part is a slice of an artifact over that limit: redacting
        it would break the sha256 the whole object is verified against, and the
        limit is the reason the file is going this way at all. These bytes
        reach object storage BEFORE anything scans them; the server's verifier
        inspects a bounded prefix afterwards and RECORDS what it finds on the
        artifact, and nothing is blocked. The caller has already refused a
        credential in the PATH (`secret_gate._check_path`).

        Streams (never buffers the part), with Content-Length fixed to
        ``length`` and the body cut at it, re-opening the file on every attempt
        like `put_file`. No Authorization header; the URL carries its own
        signature."""
        headers = {"Content-Length": str(length)}
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            try:
                with open(path, "rb") as fh:
                    fh.seek(offset)
                    resp = self._client.put(
                        url,
                        content=_iter_file(fh, chunk_size, length),
                        headers=headers,
                        **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                    )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                # #2075: a 401/403 refuses this part's signed URL, never the
                # login (none is sent) -- `UploadRefused`, not an auth block.
                raise _presigned_put_error(resp, url)
            return resp.headers.get("etag")

    @_instrumented("PUT")
    @freeze_stream
    def put_fileobj(
        self,
        url: str,
        fh: Any,
        *,
        size: int,
        content_type: str | None = None,
        headers: Mapping[str, str] | None = None,
        chunk_size: int = 1 << 20,
    ) -> None:
        """PUT an already-open, already-verified file handle to a presigned URL.

        The per-file capture path hashes a descriptor before it streams it (so
        the bytes sent are the bytes checked); this is the sibling of
        :meth:`put_file` that takes that descriptor instead of re-opening a path
        it cannot vouch for. Sends exactly ``size`` bytes, rewinding to byte 0
        on every attempt. No Authorization header; the presigned URL carries
        its own signature."""
        request_headers = dict(headers or {})
        if content_type:
            request_headers.setdefault("Content-Type", content_type)
        request_headers["Content-Length"] = str(size)
        attempt = 0
        while True:
            attempt += 1
            attempt_timeout, clamped = self._attempt_timeout(None, f"PUT {_blob_label(url)}")
            fh.seek(0)
            try:
                resp = self._client.put(
                    url,
                    content=_iter_file(fh, chunk_size, size),
                    headers=request_headers,
                    **({"timeout": attempt_timeout} if attempt_timeout is not None else {}),
                )
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                if self._cut_by_deadline(exc, clamped):
                    raise self._deadline_error(f"PUT {_blob_label(url)}", exc) from exc
                raise errors.TransportError(f"PUT {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _presigned_put_error(resp, url)
            _warn_upload_inspection(resp)
            return

    @_instrumented("GET")
    def get_url(self, url: str) -> bytes:
        """Raw GET of a presigned URL (artifact download); returns the bytes.
        No Authorization header - the presigned URL carries its own signature."""
        attempt = 0
        while True:
            attempt += 1
            try:
                resp = self._client.get(url)
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                raise errors.TransportError(f"GET {_blob_label(url)}: {exc}") from exc
            if (
                resp.status_code in _RETRYABLE
                and attempt <= self.max_retries
                and self._retry_pause(attempt, resp)
            ):
                continue
            if resp.status_code >= 400:
                raise _with_retry_after(errors.error_for(resp.status_code, resp.text), resp)
            return resp.content

    @_instrumented("GET")
    def download_to(
        self, url: str, dest: str, *, chunk_size: int = 1 << 20, max_bytes: int | None = None
    ) -> tuple[int, str]:
        """Stream a presigned-URL GET to ``dest``; return ``(size_bytes, sha256_hex)``.

        The sibling of :meth:`get_url` for the bytes you do NOT want in memory: it
        hashes while it writes, so a caller can verify the blob against a known
        ``content_hash`` without a second pass, and never materialises the whole
        object -- an anchored artifact can be model weights. No Authorization header;
        the presigned URL carries its own signature. Idempotent, so a network blip or
        a retryable status restarts the download from byte 0 (the ``open`` truncates
        ``dest``). A partial file can be left behind only when retries are exhausted
        mid-stream -- the caller owns cleanup on error, same as any failed write."""
        if max_bytes is not None and max_bytes < 0:
            raise ValueError("max_bytes must not be negative")
        attempt = 0
        while True:
            attempt += 1
            try:
                with self._client.stream("GET", url) as resp:
                    if (
                        resp.status_code in _RETRYABLE
                        and attempt <= self.max_retries
                        and self._retry_pause(attempt, resp)
                    ):
                        continue
                    if resp.status_code >= 400:
                        resp.read()  # a streamed response has no .text until read
                        raise _with_retry_after(
                            errors.error_for(resp.status_code, resp.text), resp
                        )
                    hasher = hashlib.sha256()
                    size = 0
                    if max_bytes is not None:
                        declared = resp.headers.get("content-length")
                        if declared is not None and int(declared) > max_bytes:
                            raise ValueError("artifact download exceeds its byte budget")
                    with open(dest, "wb") as fh:
                        for chunk in resp.iter_bytes(chunk_size):
                            if max_bytes is not None and size + len(chunk) > max_bytes:
                                raise ValueError("artifact download exceeds its byte budget")
                            fh.write(chunk)
                            hasher.update(chunk)
                            size += len(chunk)
                return size, hasher.hexdigest()
            except httpx.HTTPError as exc:
                if attempt <= self.max_retries and self._retry_pause(attempt):
                    continue
                raise errors.TransportError(f"GET {_blob_label(url)}: {exc}") from exc


#: The Probe daemon runs each `probe` command with an operation id (R12). Every
#: write request the command makes carries `<op id>-<n>`, n counting that
#: command's writes in order, so a retry of the same command (same id, same
#: sequence) replays on the server instead of writing twice, and two different
#: writes of one command never share a key (the server answers 422 to a key
#: reused for a different request).
_IDEMPOTENCY_ENV = "PROBE_IDEMPOTENCY_KEY"
_idempotency_count = 0


def _idempotency_key(method: str, path: str) -> str | None:
    global _idempotency_count
    base = os.environ.get(_IDEMPOTENCY_ENV, "").strip()
    if not base or method.upper() not in {"POST", "PATCH", "PUT", "DELETE"} or not path.startswith("/v1/"):
        return None
    _idempotency_count += 1
    return f"{base[:80]}-{_idempotency_count}"
