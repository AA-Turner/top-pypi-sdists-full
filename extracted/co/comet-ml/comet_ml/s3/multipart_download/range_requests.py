# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
import time
from typing import Callable, Collection, Dict, NamedTuple, Optional

import requests

from ...config import UPLOAD_FILE_MAX_RETRIES, UPLOAD_FILE_RETRY_BACKOFF_FACTOR
from ...connection import http_session
from ..multipart_transfer import cancellation, retry_policy, throttling
from .download_error import S3DownloadError

LOGGER = logging.getLogger(__name__)

MAX_S3_PART_DOWNLOAD_ATTEMPTS: int = UPLOAD_FILE_MAX_RETRIES

# How often a part held by the throttle gate checks whether it was canceled. The
# gate can hold for minutes, and a canceled download should not wait them out.
CANCELLATION_POLL_SECONDS = 0.25

# What a failed connection looks like from requests, both when the request is sent
# and when the body of a streamed response is being read.
REQUEST_NETWORK_ERRORS = (
    requests.ConnectionError,
    requests.Timeout,
    ConnectionError,
)

SessionProvider = Callable[[], requests.Session]


def session_provider_for(verify_tls: bool) -> SessionProvider:
    """The session used for ranged GETs straight to S3.

    Like the upload path's: no Comet headers, because this goes to S3, and no
    transport-level retries, because retrying is owned here. Cached per thread, so
    every worker of the parts pool keeps its own connection across the ranges it
    fetches.
    """

    def provider() -> requests.Session:
        return http_session.get_cached_http_session(
            retry=False, verify_tls=verify_tls, tcp_keep_alive=False
        )

    return provider


class RetryBudget:
    """What one part may still spend on retries. Not shared between parts.

    The same two budgets the upload path uses, for the same reasons: server errors
    and dropped connections get a small count of attempts, rate limiting gets a
    budget of time. The error count is given back whenever an attempt made
    progress, because a long range over a flaky link can be interrupted more times
    than the budget allows while still getting closer to done every time.
    """

    __slots__ = [
        "max_error_attempts",
        "error_attempts",
        "throttle_attempts",
        "_started",
    ]

    def __init__(self, max_error_attempts: int):
        self.max_error_attempts = max_error_attempts
        self.error_attempts = 0
        self.throttle_attempts = 0
        self._started = time.monotonic()

    @property
    def elapsed(self) -> float:
        return time.monotonic() - self._started

    @property
    def throttle_time_left(self) -> float:
        return max(0.0, retry_policy.MAX_THROTTLE_RETRY_SECONDS - self.elapsed)

    def progress_made(self) -> None:
        self.error_attempts = 0


class ContentRange(NamedTuple):
    first: int
    last: int
    total: Optional[int]


def parse_content_range(value: Optional[str]) -> Optional[ContentRange]:
    """Parses ``bytes first-last/total``, where total may be ``*``. None if malformed."""
    if not value:
        return None

    try:
        unit, _, spec = value.strip().partition(" ")
        if unit.lower() != "bytes":
            return None

        byte_range, _, total = spec.partition("/")
        first, _, last = byte_range.partition("-")
        return ContentRange(
            first=int(first),
            last=int(last),
            total=None if total.strip() == "*" else int(total),
        )
    except (TypeError, ValueError):
        return None


class RangeRequester:
    """Opens a streamed GET on one presigned URL, retrying the way part uploads do.

    Returns only a response whose status the caller said it can handle, and raises
    S3DownloadError for anything else once the retry budgets are spent. What counts
    as retryable is taken from the upload side unchanged: 500, 502 and 504 get the
    small attempt budget, 429 and 503 the time budget and the shared brake, and
    everything else - an expired URL, a missing object, an object that changed under
    If-Match - fails at once, because repeating it fails the same way.

    Retrying is safe for every request made here: a GET of a byte range has no side
    effects, which is the property the control-plane calls on the upload side lack.

    Safe to use from several threads at once; it keeps no per-request state. The
    per-part state is the RetryBudget that each caller brings.
    """

    def __init__(
        self,
        url: str,
        session_provider: SessionProvider,
        throttle_gate: Optional[throttling.ThrottleGate],
        request_timeout: Optional[float] = None,
        retry_backoff_factor: float = UPLOAD_FILE_RETRY_BACKOFF_FACTOR,
        sleep: Optional[Callable[[float], None]] = None,
        cancel_token: Optional[cancellation.CancellationToken] = None,
    ):
        """With a cancel_token, every attempt, backoff and wait on the gate stops
        with TransferCancelled once it is cancelled."""
        self.url = url
        self._session_provider = session_provider
        self._throttle_gate = throttle_gate
        self._request_timeout = request_timeout
        self._retry_backoff_factor = retry_backoff_factor
        self._cancel_token = cancel_token
        if sleep is None:
            sleep = time.sleep if cancel_token is None else cancel_token.sleep
        self._sleep = sleep

    def open(
        self,
        first: Optional[int],
        last: Optional[int],
        if_match: Optional[str],
        budget: RetryBudget,
        accepted: Collection[int],
    ) -> requests.Response:
        """Sends ``Range: bytes=first-last``, or a plain GET when first is None."""
        headers: Dict[str, str] = {}
        if first is not None:
            headers["Range"] = "bytes=%d-%s" % (first, "" if last is None else last)
        if if_match is not None:
            # Every range after the first is pinned to the object the first one came
            # from. Without it, an object overwritten mid-download is stitched
            # together from two versions and stored as a success.
            headers["If-Match"] = if_match

        while True:
            self._raise_if_cancelled()
            self._wait_for_gate(budget)
            # Again: the gate may have opened just after a cancellation it did not see.
            self._raise_if_cancelled()

            try:
                response = self._session_provider().get(
                    self.url,
                    headers=headers,
                    stream=True,
                    timeout=self._request_timeout,
                )
            except REQUEST_NETWORK_ERRORS:
                LOGGER.debug(
                    "Connection error on S3 ranged GET %r", headers, exc_info=True
                )
                self.after_error(
                    budget,
                    reason="Failed to connect to S3 for range %r"
                    % headers.get("Range"),
                    due_connection_error=True,
                )
                continue

            status = response.status_code
            if status in accepted:
                if self._throttle_gate is not None:
                    self._throttle_gate.report_success()
                return response

            text = _read_error_text(response)
            retry_after = retry_policy.retry_after_seconds(response)
            response.close()

            if status in retry_policy.THROTTLING_STATUS_CODES:
                self._after_throttled(budget, status, retry_after)
                continue

            reason = "S3 answered %d to range %r: %r" % (
                status,
                headers.get("Range"),
                text,
            )
            if status in retry_policy.SERVER_ERROR_STATUS_CODES:
                self.after_error(budget, reason=reason, status_code=status)
                continue

            LOGGER.debug(reason)
            raise S3DownloadError(reason=reason, status_code=status)

    def after_error(
        self,
        budget: RetryBudget,
        reason: str,
        due_connection_error: bool = False,
        status_code: Optional[int] = None,
    ) -> None:
        """Spends one error attempt and backs off, or raises if none are left.

        Public because a body that stops arriving part way through is the same kind
        of failure as a request that could not connect, and is counted against the
        same budget by whoever was reading it.
        """
        budget.error_attempts += 1
        if budget.error_attempts >= budget.max_error_attempts:
            raise S3DownloadError(
                reason="%s (gave up after %d attempts)"
                % (reason, budget.error_attempts),
                due_connection_error=due_connection_error,
                status_code=status_code,
            )

        backoff = retry_policy.backoff_with_jitter(
            self._retry_backoff_factor,
            budget.error_attempts,
            retry_policy.PART_RETRY_JITTER,
        )
        LOGGER.debug(
            "%s. Attempt %d of %d, retrying after %.2fs",
            reason,
            budget.error_attempts,
            budget.max_error_attempts,
            backoff,
        )
        self._sleep(backoff)

    def _after_throttled(
        self, budget: RetryBudget, status: int, retry_after: Optional[float]
    ) -> None:
        budget.throttle_attempts += 1
        if (
            budget.throttle_attempts >= retry_policy.MAX_THROTTLE_ATTEMPTS
            or budget.throttle_time_left <= 0
        ):
            raise S3DownloadError(
                reason="S3 kept rate limiting the download: %d throttled attempts "
                "over %.1fs" % (budget.throttle_attempts, budget.elapsed),
                status_code=status,
            )

        if self._throttle_gate is not None:
            # The wait happens on the gate at the top of the next attempt, for every
            # part at once, so this one must not sleep on top of it.
            self._throttle_gate.report_throttled(
                retry_after, max_hold=budget.throttle_time_left
            )
            return

        backoff = retry_policy.backoff_with_jitter(
            self._retry_backoff_factor,
            budget.throttle_attempts,
            retry_policy.PART_RETRY_JITTER,
        )
        if retry_after is not None:
            backoff = max(backoff, retry_after)
        self._sleep(min(backoff, budget.throttle_time_left))

    def _raise_if_cancelled(self) -> None:
        if self._cancel_token is not None:
            self._cancel_token.raise_if_cancelled()

    def _wait_for_gate(self, budget: RetryBudget) -> None:
        if self._throttle_gate is None:
            return

        if not self._wait_until_open(
            self._throttle_gate, timeout=budget.throttle_time_left
        ):
            raise S3DownloadError(
                reason="Still rate limited by S3 with no time left in the %.0fs "
                "budget" % retry_policy.MAX_THROTTLE_RETRY_SECONDS
            )

    def _wait_until_open(self, gate: throttling.ThrottleGate, timeout: float) -> bool:
        if self._cancel_token is None:
            return gate.wait_until_open(timeout=timeout)

        # In slices, to notice a cancellation while the gate holds.
        deadline = time.monotonic() + timeout
        while True:
            left = deadline - time.monotonic()
            if gate.wait_until_open(
                timeout=max(0.0, min(left, CANCELLATION_POLL_SECONDS))
            ):
                return True
            self._cancel_token.raise_if_cancelled()
            if left <= CANCELLATION_POLL_SECONDS:
                return False


def _read_error_text(response: requests.Response) -> str:
    # An error body from S3 is a short XML document. Anything else that answers with
    # an error status could send an arbitrarily large one, so only the start is kept.
    try:
        return response.raw.read(1024, decode_content=True).decode(
            "utf-8", errors="replace"
        )
    except Exception:
        return ""


_default_download_gate = throttling.ThrottleGate()


def default_download_gate() -> throttling.ThrottleGate:
    """The process-wide brake for downloads.

    Separate from the upload brake rather than shared with it. S3 rate limits reads
    and writes independently, GETs at a higher rate than PUTs, so a download told to
    slow down says nothing about whether an upload in the same process should.
    """
    return _default_download_gate
