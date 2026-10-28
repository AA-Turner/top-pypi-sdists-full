"""Data-plane HTTP plumbing: settings, retry policy, error classification, sending.

Every presigned PUT/GET goes through :func:`transfer_request`, which owns the
per-attempt timeout, the 403 re-presign dance, exponential backoff and the
per-part retry window. The transport is duck-typed (``request_raw``) so the
engine is stack-neutral and testable against a local stub server.
"""

from __future__ import annotations

import http.client
import io
import logging
import random
import socket
import ssl
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar
from urllib.parse import urljoin

import urllib3
import urllib3.exceptions

from istari_digital_client._transfer.errors import (
    HttpError,
    RetriesExhausted,
    TransferCancelledError,
    TransferError,
    is_retryable_status,
)
from istari_digital_client._transfer.request_options import control_request_scope

logger = logging.getLogger("istari_digital_client.transfer")

T = TypeVar("T")

MIB = 1024 * 1024
_ERROR_BODY_SNIFF = 64 * 1024
_REDIRECT_STATUSES = {301, 302, 307, 308}
_JITTER_FRACTION = 0.25
# Floor on every retry sleep, so retry_min_interval_millis=0 cannot spin without sleeping.
_MIN_BACKOFF = 0.01


class RawTransport(Protocol):
    """The slice of ``RESTClientObject`` the engine uses."""

    def request_raw(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: Any = None,
        timeout: Any = None,
        preload_content: bool = False,
        decode_content: bool = True,
    ) -> urllib3.BaseHTTPResponse: ...


@dataclass(frozen=True)
class RetryPolicy:
    """Exponential backoff with a cap, optional jitter, and a retry-window budget."""

    enabled: bool = True
    min_interval: float = 0.2
    max_interval: float = 10.0
    jitter: bool = True
    deadline: float = 300.0

    def backoff(self, attempt: int) -> float:
        """Sleep before retrying after ``attempt`` (1-based) failed."""
        wait = min(max(self.min_interval, 0.0), self.max_interval)
        # Stop doubling at the cap: even a zero interval must not construct an
        # enormous integer and overflow its conversion to float on long retries.
        for _ in range(max(attempt - 1, 0)):
            if wait <= 0 or wait >= self.max_interval:
                break
            wait = min(wait * 2, self.max_interval)
        if self.jitter:
            wait *= 1 + random.uniform(-_JITTER_FRACTION, _JITTER_FRACTION)
        return max(wait, _MIN_BACKOFF)


def _int_or(value: Any, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class TransferSettings:
    """Everything the engine reads from ``Configuration``, with defaults applied.

    Values are read with ``getattr`` defaults because the legacy stack is often
    handed the sdk ``Configuration`` and post-construction assignments skip
    validation; ``concurrency`` is clamped to 1..16 for the same reason.
    """

    concurrency: int = 4
    part_size_floor: int = 128 * MIB
    threshold: int = 2 * 1024 * MIB
    cache_max_size: int = 2 * 1024 * MIB
    connect_timeout: float = 30.0
    read_timeout: float = 120.0
    control_timeout: float | None = None
    retry: RetryPolicy = RetryPolicy()

    @classmethod
    def from_config(cls, config: Any) -> TransferSettings:
        """Build settings from a legacy or sdk ``Configuration`` (or anything duck-typed)."""
        concurrency = max(
            1, min(_int_or(getattr(config, "transfer_concurrency", None), 4), 16)
        )
        control = getattr(config, "http_request_timeout_secs", None)
        # urllib3 rejects a read timeout <= 0, so a post-construction one gets the default.
        read_timeout = _int_or(getattr(config, "transfer_read_timeout_secs", None), 120)
        control_timeout = (
            float(control) if control is not None and control > 0 else None
        )
        retry = RetryPolicy(
            enabled=bool(getattr(config, "retry_enabled", True)),
            min_interval=_int_or(
                getattr(config, "retry_min_interval_millis", None), 200
            )
            / 1000,
            max_interval=_int_or(
                getattr(config, "retry_max_interval_millis", None), 10_000
            )
            / 1000,
            jitter=bool(getattr(config, "retry_jitter_enabled", True)),
            deadline=float(
                _int_or(getattr(config, "transfer_retry_deadline_secs", None), 300)
            ),
        )
        return cls(
            concurrency=concurrency,
            part_size_floor=_int_or(
                getattr(config, "multipart_chunksize", None), 128 * MIB
            ),
            threshold=_int_or(
                getattr(config, "multipart_threshold", None), 2 * 1024 * MIB
            ),
            cache_max_size=_int_or(
                getattr(config, "filesystem_cache_max_size", None), 2 * 1024 * MIB
            ),
            connect_timeout=control_timeout or 30.0,
            read_timeout=float(read_timeout if read_timeout > 0 else 120),
            control_timeout=control_timeout,
            retry=retry,
        )

    def timeout(self) -> urllib3.Timeout:
        """Per-attempt socket timeout: connect from the control plane, read from the data plane."""
        return urllib3.Timeout(connect=self.connect_timeout, read=self.read_timeout)

    @property
    def complete_timeout(self) -> float:
        """Per-call timeout for multipart complete, which can be slow for thousands of parts."""
        return max(self.control_timeout or 0.0, self.read_timeout)


class Deadline:
    """An eager budget, or an explicitly lazy transfer retry window.

    A retry window starts at the first retryable failure, not during healthy
    initial work. Socket timeouts bound silence independently of this window.
    """

    def __init__(
        self,
        budget: float,
        clock: Callable[[], float] = time.monotonic,
        *,
        lazy: bool = False,
    ) -> None:
        """Keep eager behavior unless ``lazy`` is explicitly requested."""
        self._clock = clock
        self._budget = max(budget, 0.0)
        self._end: float | None = None if lazy else clock() + self._budget

    def start(self) -> None:
        """Start an inactive window on its first retryable failure."""
        if self._end is None:
            self._end = self._clock() + self._budget

    def reset(self) -> None:
        """Renew an active window after reaching a genuinely new byte offset."""
        if self._end is not None:
            self._end = self._clock() + self._budget

    def remaining(self) -> float:
        """Seconds left; an inactive retry window retains its full budget."""
        if self._end is None:
            return self._budget
        return max(self._end - self._clock(), 0.0)

    @property
    def expired(self) -> bool:
        """True once an active budget is spent."""
        return self._end is not None and self.remaining() <= 0.0


def exception_causes(exc: BaseException) -> list[BaseException]:
    """Traverse transport wrappers and chained causes safely, including cycles."""
    pending = [exc]
    result: list[BaseException] = []
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        result.append(current)
        for candidate in (
            current.__cause__,
            current.__context__,
            getattr(current, "reason", None),
            getattr(current, "original_error", None),
            getattr(current, "last_exception", None),
            *current.args,
        ):
            if isinstance(candidate, BaseException):
                pending.append(candidate)
    return result


def is_retryable_exception(exc: BaseException) -> bool:
    """Retry recognized transport failures, never terminal local/certificate errors."""
    status = _status_of(exc)
    if status:
        return (
            exc.retryable if isinstance(exc, HttpError) else is_retryable_status(status)
        )
    causes = exception_causes(exc)
    if any(
        isinstance(c, (TransferError, ssl.SSLCertVerificationError)) for c in causes
    ):
        return False
    tls = any(
        isinstance(c, (ssl.SSLError, urllib3.exceptions.SSLError)) for c in causes
    )
    transient_tls = any(
        isinstance(c, ssl.SSLEOFError)
        or (isinstance(c, ssl.SSLError) and c.errno == ssl.SSL_ERROR_EOF)
        for c in causes
    )
    if tls and not transient_tls:
        return False
    return transient_tls or any(
        isinstance(
            c,
            (
                urllib3.exceptions.TimeoutError,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.IncompleteRead,
                http.client.IncompleteRead,
                http.client.RemoteDisconnected,
                ConnectionError,
                socket.timeout,
            ),
        )
        for c in causes
    )


def _status_of(exc: BaseException) -> int | None:
    status = getattr(exc, "status", None)
    return status if isinstance(status, int) else None


def is_retryable_control_error(exc: BaseException) -> bool:
    """Classification for control-plane (registry) calls raised as the stack's ``ApiException``."""
    status = _status_of(exc)
    if status:
        return is_retryable_status(status)
    return is_retryable_exception(exc)


def check_cancel(*events: threading.Event | None) -> None:
    """Raise ``TransferCancelledError`` if any event is set."""
    for event in events:
        if event is not None and event.is_set():
            raise TransferCancelledError("transfer cancelled")


def _wait(seconds: float, cancel: threading.Event | None) -> None:
    if seconds <= 0:
        return
    if cancel is not None:
        if cancel.wait(seconds):
            raise TransferCancelledError("transfer cancelled")
    else:
        time.sleep(seconds)


def finish_response(response: urllib3.BaseHTTPResponse) -> None:
    """Drain and return a successful response's connection to the pool."""
    try:
        response.drain_conn()
    except Exception:  # noqa: BLE001 - dropping the connection is the fallback
        response.close()
    else:
        response.release_conn()


def _rewind(body: Any) -> None:
    if body is not None and hasattr(body, "seek"):
        body.seek(0, io.SEEK_SET)


def send(
    transport: RawTransport,
    method: str,
    url: str,
    *,
    body: Any = None,
    headers: Mapping[str, str] | None = None,
    timeout: Any,
    preload_content: bool = False,
    decode_content: bool = True,
    max_redirects: int = 3,
) -> urllib3.BaseHTTPResponse:
    """One attempt at ``method url``; non-2xx raises ``HttpError``.

    Sets ``Content-Length`` from ``len(body)`` so a reader is never sent chunked.
    Follows up to ``max_redirects`` 3xx responses itself, rewinding the body first,
    because urllib3 would otherwise re-send an already-consumed reader.
    """
    request_headers = dict(headers or {})
    if body is not None and hasattr(body, "read") and not hasattr(body, "__len__"):
        raise TransferError("readable request bodies must expose an exact length")
    if body is not None and hasattr(body, "__len__"):
        request_headers["Content-Length"] = str(len(body))
    redirects = 0
    while True:
        response = transport.request_raw(
            method,
            url,
            headers=request_headers,
            body=body,
            timeout=timeout,
            preload_content=preload_content,
            decode_content=decode_content,
        )
        status = response.status
        location = response.headers.get("Location")
        if status in _REDIRECT_STATUSES and location and redirects < max_redirects:
            response.close()
            redirects += 1
            url = urljoin(url, location)
            _rewind(body)
            continue
        if 200 <= status < 300:
            return response
        try:
            sniff = response.read(_ERROR_BODY_SNIFF, decode_content=True) or b""
        except Exception:  # noqa: BLE001 - the status is what matters
            sniff = b""
        finally:
            response.close()
        raise HttpError(
            method, url, status, response.reason, response.headers, bytes(sniff)
        )


def retrying(
    attempt: Callable[[int], T],
    *,
    policy: RetryPolicy,
    deadline: Deadline,
    retryable: Callable[[BaseException], bool],
    on_retry: Callable[[int, BaseException, float], None] | None = None,
    cancel: threading.Event | None = None,
) -> T:
    """Call ``attempt(n)`` until it returns, a non-retryable error, or the budget is spent.

    ``policy.enabled=False`` makes exactly one attempt. A spent budget raises
    ``RetriesExhausted`` wrapping the last error.
    """
    n = 0
    last: BaseException | None = None
    while True:
        check_cancel(cancel)
        if last is not None and deadline.expired:
            raise RetriesExhausted(last, n) from last
        n += 1
        try:
            return attempt(n)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:
            if not policy.enabled or not retryable(exc):
                raise
            last = exc
            deadline.start()
            wait = policy.backoff(n)
            if deadline.expired or deadline.remaining() < wait:
                raise RetriesExhausted(exc, n) from exc
            if on_retry is not None:
                on_retry(n, exc, wait)
            logger.debug("retrying after %r (attempt %d, sleeping %.2fs)", exc, n, wait)
            _wait(wait, cancel)


def transfer_request(
    transport: RawTransport,
    method: str,
    *,
    url: str | Callable[[], str],
    refresh_url: Callable[[str], str] | None = None,
    body: Any = None,
    headers: Mapping[str, str] | Callable[[], Mapping[str, str]] | None = None,
    settings: TransferSettings,
    deadline: Deadline,
    cancel: threading.Event | None = None,
    on_retry: Callable[[int, float], None] | None = None,
    on_represign: Callable[[int], None] | None = None,
    preload_content: bool = False,
    decode_content: bool = True,
    timeout: Any = None,
    consume: Callable[[urllib3.BaseHTTPResponse], Any] | None = None,
) -> Any:
    """Send one part or range with the full data-plane retry discipline.

    With ``consume``, the response body is processed inside the attempt (and the
    response closed afterwards), so a failure while streaming it is retried like
    a failed send; the return value is then ``consume``'s. Without it the open
    response is returned.

    * Transport failures, 5xx, 429, 408 and the S3 400 ``RequestTimeout`` back off
      exponentially until ``deadline`` (or make one attempt with retries disabled).
    * A 403 asks ``refresh_url(failed_url)`` for a fresh URL and retries at once. A
      403 on that fresh URL is a denial. If the refresh hands back the *same* URL
      (the registry's download-URL cache), the attempt backs off inside the deadline
      so the cache can roll over.
    * The body is rewound before every attempt.
    * ``url`` and ``headers`` may be zero-argument callables, evaluated at the start
      of each attempt (except the immediate retry on a just-refreshed URL), so a
      retry picks up a proactively refreshed URL and a resumed ``Range``.
    """
    state = _RequestState(url=url if isinstance(url, str) else "")

    def attempt(n: int) -> urllib3.BaseHTTPResponse:
        _rewind(body)
        if not state.fresh_403 and callable(url):
            state.url = url()
        try:
            response = send(
                transport,
                method,
                state.url,
                body=body,
                headers=headers() if callable(headers) else headers,
                timeout=settings.timeout() if timeout is None else timeout,
                preload_content=preload_content,
                decode_content=decode_content,
            )
        except HttpError as exc:
            if exc.expired and refresh_url is not None and not state.fresh_403:
                fresh = refresh_url(state.url)
                if fresh != state.url:
                    if on_represign is not None:
                        on_represign(n)
                    state.url = fresh
                    state.fresh_403 = True
                    return attempt(n)
                raise _SameUrlAfterRefresh(exc) from exc
            raise
        state.fresh_403 = False
        if consume is None:
            return response
        try:
            return consume(response)
        finally:
            response.close()

    def retryable(exc: BaseException) -> bool:
        return isinstance(exc, _SameUrlAfterRefresh) or is_retryable_exception(exc)

    def _on_retry(n: int, exc: BaseException, wait: float) -> None:
        state.fresh_403 = False
        if on_retry is not None:
            on_retry(n, wait)

    try:
        return retrying(
            attempt,
            policy=settings.retry,
            deadline=deadline,
            retryable=retryable,
            on_retry=_on_retry,
            cancel=cancel,
        )
    except _SameUrlAfterRefresh as exc:
        raise exc.error from None
    except RetriesExhausted as exc:
        if isinstance(exc.last, _SameUrlAfterRefresh):
            raise RetriesExhausted(exc.last.error, exc.attempts) from exc.last.error
        raise


@dataclass
class _RequestState:
    """Mutable per-request state shared with the retry closure."""

    url: str
    fresh_403: bool = False


class _SameUrlAfterRefresh(Exception):
    """Control-flow marker for ``transfer_request``, never raised to callers.

    A 403 whose re-presign returned the same URL: back off and try again. It lives
    here rather than in ``errors.py`` because it is unwrapped before it leaves this
    module.
    """

    def __init__(self, error: HttpError) -> None:
        """Keep the 403 so it can be surfaced if the budget runs out."""
        super().__init__(str(error))
        self.error = error


def retry_control_call(
    fn: Callable[[], T],
    *,
    settings: TransferSettings,
    invalidate_auth: Callable[[], bool] | None = None,
    cancel: threading.Event | None = None,
) -> T:
    """Run a registry call with the shared, lazy transfer retry window.

    Retries transient statuses and transport failures, and retries **once** on a 401
    after ``invalidate_auth()`` drops the managed token, so a multi-hour session
    survives JWT expiry.
    """
    deadline = Deadline(settings.retry.deadline, lazy=True)
    refreshed = False

    def attempt(n: int) -> T:
        nonlocal refreshed
        with control_request_scope():
            try:
                return fn()
            except BaseException as exc:
                if (
                    _status_of(exc) == 401
                    and invalidate_auth is not None
                    and not refreshed
                ):
                    refreshed = True
                    if invalidate_auth():
                        return fn()
                raise

    return retrying(
        attempt,
        policy=settings.retry,
        deadline=deadline,
        retryable=is_retryable_control_error,
        cancel=cancel,
    )
