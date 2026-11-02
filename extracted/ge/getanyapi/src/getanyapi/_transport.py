"""Shared wire and retry engine for the sync and async clients (SPEC 2.2, 2.8).

Both :class:`getanyapi.AnyAPI` and :class:`getanyapi.AsyncAnyAPI` route every SKU run
through here. The wire contract is frozen:

    POST {base_url}/v1/run/{slug}
    Authorization: Bearer <api_key>
    Content-Type: application/json
    Accept: application/json
    Idempotency-Key: <per-call key> (unless the client kill switch is off)
    body = json(input)
    query params (only when set): fields (comma-joined), max_items, summary=true

HTTP 200 parses into ``RunResult[Any]``; any other status maps to the frozen
error hierarchy. Retries cover HTTP 429 and retry-safe transport failures,
never timeouts. Billed POSTs retry only connection-establishment failures that
prove no request was delivered. A ``ReadError`` is ambiguous: it can occur
before the server reads the request, as well as after a body was sent, so it
must not retry. Idempotent or bodyless requests retry any transport failure.
Backoff is jittered exponential and honors ``Retry-After`` on 429.

One 4xx is retryable: a 409 whose code is ``idempotency_in_progress`` means the
gateway is still executing the run this key claims, so the SDK waits the server's
``Retry-After`` in full (past the 8s ordinary ceiling) inside a whole-call wait
budget and collects the replay. Every other 409 is terminal.
"""

from __future__ import annotations

import email.utils
import random
import time
from datetime import datetime, timezone
from typing import Any, cast

import httpx
from pydantic import ValidationError

from ._errors import (
    AnyAPIError,
    ConnectionError,
    RateLimitedError,
    TimeoutError,
    error_for_status,
)
from ._idempotency import (
    generate_idempotency_key,
    validate_idempotency_key,
)
from .types import RequestOptions, RunResult

__all__ = [
    "build_request",
    "parse_raw",
    "request_id_of",
    "validate_run_result",
    "compute_delay",
    "retry_after_seconds",
    "RetryState",
    "error_message",
    "error_details",
    "as_dict",
    "is_retryable_error",
    "is_idempotency_in_progress",
    "sleep",
    "DEFAULT_MAX_IN_PROGRESS_WAIT",
    "IDEMPOTENCY_IN_PROGRESS_CODE",
]

_BASE_DELAY = 0.5  # seconds
_MAX_DELAY = 8.0  # seconds
# Ceiling on the TOTAL seconds one run() call may block waiting out an in-progress
# idempotency claim (SPEC 2.8). The 8s ordinary-backoff ceiling cannot express the
# gateway's own Retry-After: 30, so this separate, much higher budget governs that
# path. 60s covers two full server-directed waits at today's 30s and doubles as
# headroom if the gateway ever raises that value. It is a whole-call budget, not a
# per-wait clamp: a wait longer than the remaining budget is refused outright rather
# than truncated, because a truncated wait is guaranteed to find the same claim still
# running and burn an attempt.
DEFAULT_MAX_IN_PROGRESS_WAIT = 60.0  # seconds
# The only 409 code that means "come back later"; every other 409 is terminal.
IDEMPOTENCY_IN_PROGRESS_CODE = "idempotency_in_progress"
# The gateway emits its support handle as X-Anyapi-Request-Id (it is also the only
# request-id header its CORS layer exposes to a browser). The generic x-request-id is
# kept as a fallback for a proxy that stamps the conventional name in front of us.
_REQUEST_ID_HEADERS = ("x-anyapi-request-id", "x-request-id")
_RNG = random.Random()


def request_id_of(response: httpx.Response) -> str | None:
    """Read the support request id from a response, preferring the gateway's header."""
    for header in _REQUEST_ID_HEADERS:
        # httpx types Headers.get as returning Any; pin it at this seam.
        value: str | None = response.headers.get(header)
        if value:
            return value
    return None


def _query_params(options: RequestOptions | None) -> dict[str, str]:
    """Build the response-shaping query params from options (SPEC 2.2)."""
    params: dict[str, str] = {}
    if not options:
        return params
    fields = options.get("fields")
    if fields:
        params["fields"] = ",".join(fields)
    max_items = options.get("max_items")
    if max_items is not None:
        params["max_items"] = str(max_items)
    if options.get("summary"):
        params["summary"] = "true"
    return params


def build_request(
    *,
    base_url: str,
    slug: str,
    input: dict[str, Any],
    api_key: str,
    options: RequestOptions | None,
    timeout: float,
    idempotency: str,
) -> httpx.Request:
    """Assemble the httpx.Request for a SKU run (no client bound).

    The per-request timeout is carried on the request's ``extensions`` so it
    applies on ``client.send(request)`` without depending on the client default.
    """
    url = f"{base_url.rstrip('/')}/v1/run/{slug}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if idempotency == "auto":
        key = (
            options["idempotency_key"]
            if options is not None and "idempotency_key" in options
            else generate_idempotency_key()
        )
        validate_idempotency_key(key)
        headers["Idempotency-Key"] = key
    if options is not None and options.get("respond_async"):
        headers["Prefer"] = "respond-async"
    # This request is built once before the retry loop. httpx serializes ``json``
    # here, so every send reuses the exact raw body bytes used for fingerprinting.
    return httpx.Request(
        "POST",
        url,
        params=_query_params(options),
        headers=headers,
        json=input,
        extensions={"timeout": httpx.Timeout(timeout).as_dict()},
    )


def _fallback_message(status: int) -> str:
    return f"request failed with status {status}"


def as_dict(value: object) -> dict[str, object]:
    """Narrow an arbitrary JSON value to a str-keyed dict (empty if not one)."""
    if isinstance(value, dict):
        return cast("dict[str, object]", value)
    return {}


def error_message(body: object, status: int) -> str:
    """Extract the ``{error, code}`` details and return the message."""
    return error_details(body, status)[0]


def error_details(body: object, status: int) -> tuple[str, str | None]:
    """Extract the error message and stable code from a JSON body."""
    body_dict = as_dict(body)
    err = body_dict.get("error")
    code = body_dict.get("code")
    parsed_code = code if isinstance(code, str) and code else None
    if isinstance(err, str):
        return err, parsed_code
    return _fallback_message(status), parsed_code


def parse_raw(response: httpx.Response) -> dict[str, Any]:
    """Return the parsed JSON dict on 200, or raise the mapped error otherwise.

    The raw-dict seam (SPEC N2): generated methods validate this dict directly
    into their concrete ``RunResult[XData]`` / ``BareRunResult[XData]`` model, so
    there is no model_validate(model_dump(...)) double-parse. The bare-vs-found
    envelope choice is the caller's (the generated code knows its SKU's shape).
    """
    request_id = request_id_of(response)
    if response.status_code in (200, 202):
        try:
            body = response.json()
        except ValueError as exc:
            raise AnyAPIError(
                f"could not parse run response: {exc}",
                status=200,
                request_id=request_id,
            ) from exc
        if not isinstance(body, dict):
            raise AnyAPIError(
                "run response was not a JSON object",
                status=200,
                request_id=request_id,
            )
        return cast("dict[str, Any]", body)

    err_body: object = None
    try:
        err_body = response.json()
    except ValueError:
        err_body = None
    message, code = error_details(err_body, response.status_code)
    raise error_for_status(
        response.status_code, message, request_id=request_id, code=code
    )


def validate_run_result(raw: dict[str, Any]) -> RunResult[Any]:
    """Validate a raw run dict into a generic ``RunResult[Any]`` (found-data).

    Used by the generic ``client.run(slug, ...)`` helper. Bare SKUs are best
    reached through their typed namespace method (which validates into a
    ``BareRunResult``); the generic path assumes the found-data envelope.
    """
    try:
        return RunResult[Any].model_validate(raw)
    except ValidationError as exc:
        raise AnyAPIError(f"could not parse run response: {exc}", status=200) from exc


def retry_after_seconds(response: httpx.Response) -> float | None:
    """Parse a Retry-After header (seconds or HTTP-date) into non-negative seconds.

    The value is NOT capped here: each caller applies its own ceiling. Ordinary
    backoff clamps to ``_MAX_DELAY``; the in-progress path measures the raw value
    against its wait budget.
    """
    raw = response.headers.get("retry-after")
    if not raw:
        return None
    raw = raw.strip()
    try:
        secs = float(raw)
    except ValueError:
        secs = None
    if secs is not None:
        return max(secs, 0.0)
    try:
        parsed = email.utils.parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    delta = (parsed - datetime.now(timezone.utc)).total_seconds()
    return max(delta, 0.0)


def compute_delay(attempt: int, rng: random.Random | None = None) -> float:
    """Jittered exponential backoff for retry ``attempt`` (0-based) (SPEC 2.8)."""
    r: random.Random = rng or _RNG
    base = min(_BASE_DELAY * float(2**attempt), _MAX_DELAY)
    jitter = 0.5 + r.random()
    return base * jitter


class RetryState:
    """Tracks retry budget and computes the next delay across attempts.

    Shared by the sync and async run loops so the retry policy lives in one
    place. The caller drives the loop; this object only decides whether another
    attempt is allowed and how long to wait.
    """

    def __init__(
        self,
        max_retries: int,
        max_in_progress_wait: float = DEFAULT_MAX_IN_PROGRESS_WAIT,
    ) -> None:
        self.max_retries = max(0, max_retries)
        self.attempt = 0
        self.max_in_progress_wait = max(0.0, max_in_progress_wait)
        self.in_progress_waited = 0.0

    @property
    def can_retry(self) -> bool:
        return self.attempt < self.max_retries

    def next_delay(self, response: httpx.Response | None) -> float:
        """Delay before the next retry; honors Retry-After on a 429 response.

        A server-sent Retry-After is clamped to the ordinary backoff ceiling
        (8s), which is what every retryable path except the in-progress 409
        wants; that path uses :meth:`in_progress_delay` instead.
        """
        delay = compute_delay(self.attempt)
        if response is not None:
            retry_after = retry_after_seconds(response)
            if retry_after is not None:
                delay = min(retry_after, _MAX_DELAY)
        self.attempt += 1
        return delay

    def in_progress_delay(self, response: httpx.Response) -> float | None:
        """Delay before re-issuing a call whose idempotency claim is still running.

        Honors the server's ``Retry-After`` in full (the gateway sends 30s, well
        past the 8s ordinary ceiling) and falls back to ordinary backoff when the
        header is absent. Returns None when the wait does not fit the remaining
        whole-call budget: the wait is refused, not truncated, because a short
        wait against a long-running claim just spends an attempt on the same 409.
        Consumes budget and an attempt only when it returns a delay.
        """
        retry_after = retry_after_seconds(response)
        delay = retry_after if retry_after is not None else compute_delay(self.attempt)
        if self.in_progress_waited + delay > self.max_in_progress_wait:
            return None
        self.in_progress_waited += delay
        self.attempt += 1
        return delay


def is_retryable_error(
    exc: AnyAPIError | httpx.HTTPError,
    *,
    request_may_be_billed: bool = False,
) -> bool:
    """Retry 429s and transport failures that are safe for this request shape.

    Idempotent or bodyless requests retry any non-timeout transport failure.
    A billed request retries only ``httpx.ConnectError``, the reliable pre-send
    signal. ``httpx.ReadError`` does not establish that bytes were delivered:
    an accept-then-close race or a stale keepalive connection can raise it
    before the server reads the request. It is still unsafe to retry because
    the same type can also represent a failure after delivery. The default
    preserves the one-argument behavior for callers passing an ``AnyAPIError``.
    """
    # ConnectTimeout is a TimeoutException, not a ConnectError. The billed POST
    # loops catch all TimeoutException instances before calling this predicate,
    # so the httpx term is unreachable there. Retain it so direct callers stay
    # timeout-safe and the predicate does not depend on caller catch ordering.
    if isinstance(exc, (TimeoutError, httpx.TimeoutException)):
        return False
    if isinstance(exc, RateLimitedError):
        return True
    if isinstance(exc, ConnectionError):
        return not request_may_be_billed
    if isinstance(exc, httpx.HTTPError):
        return not request_may_be_billed or isinstance(exc, httpx.ConnectError)
    return False


def is_idempotency_in_progress(exc: AnyAPIError) -> bool:
    """True for the one 409 that means "the run this key claims is still executing".

    Because settlement is detached from the caller's connection, that is the
    likely server state after an ambiguous transport failure, so waiting it out
    and collecting the replay is what makes the automatic key useful. No other
    409 qualifies: ``idempotency_conflict`` and ``idempotency_needs_review`` are
    caller-side problems that a retry can never resolve. Matched on the stable
    ``code``, never on prose. See SPEC 2.8.
    """
    return exc.status == 409 and exc.code == IDEMPOTENCY_IN_PROGRESS_CODE


def sleep(seconds: float) -> None:
    """Blocking sleep seam (monkeypatched in tests)."""
    time.sleep(seconds)
