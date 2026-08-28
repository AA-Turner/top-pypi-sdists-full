# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import datetime
import email.utils
import logging
import math
import random
import time
from typing import Any, Dict, List, NamedTuple, Optional

import requests
from requests import Response, Session

from ...config import UPLOAD_FILE_MAX_RETRIES, UPLOAD_FILE_RETRY_BACKOFF_FACTOR
from ...connection.connection_helpers import calculate_backoff_time
from .upload_error import S3UploadError

MAX_UPLOAD_START_ATTEMPTS = UPLOAD_FILE_MAX_RETRIES
MAX_S3_PART_UPLOAD_ATTEMPTS = UPLOAD_FILE_MAX_RETRIES
MAX_UPLOAD_COMPLETE_ATTEMPTS = UPLOAD_FILE_MAX_RETRIES

# Something broke at the far end, or at a gateway in front of it. Retryable, but with
# no promise that retrying will help, so these keep the modest attempt count.
SERVER_ERROR_STATUS_CODES = [500, 502, 504]

# The statuses that mean "you are going too fast" rather than "something broke". The
# distinction matters for how hard we try: a throttled request is one the server has
# promised to accept later, so giving up on it early is throwing away an upload that
# was going to succeed. 429 is here for completeness; S3 itself uses 503 SlowDown.
THROTTLING_STATUS_CODES = [429, 503]

# Derived rather than written out, because the two sets got out of step once already:
# 429 was treated as a rate limit by the retry loop while being absent from the
# retryable list, so it failed on its first attempt without ever reaching the
# throttling path.
RETRYABLE_PART_UPLOAD_STATUS_CODES = SERVER_ERROR_STATUS_CODES + THROTTLING_STATUS_CODES

# The start and complete calls get a much narrower set than the parts do. A part
# upload is a plain PUT of immutable bytes to its own URL, so repeating it is always
# safe. These two are calls into Comet's own API, and their idempotency is not
# established: repeating a completion that the handler already committed could
# complete an upload twice, and repeating a start could leave a second session
# holding a different set of presigned URLs.
#
# So only the statuses that say the request was refused *without being processed*
# qualify. A rate limit is exactly that - the server declined to handle it and asked
# for a slower rate - which is what makes it safe as well as worth retrying. 502 and
# 504 are deliberately excluded even though a 502 on upload-complete was observed
# failing a fully uploaded asset during testing: a gateway that could not return a
# response cannot tell us whether the handler ran, and guessing wrong duplicates the
# completion. Widening this needs an idempotency key on both endpoints, or a
# confirmation from the backend that repeating them is safe.
RETRYABLE_CONTROL_PLANE_STATUS_CODES = list(THROTTLING_STATUS_CODES)

# Throttling gets its own budget, and it is a budget of *time*, not of attempts. Four
# attempts is right for an error that is probably not going to clear; it is the wrong
# shape entirely for a rate limit, where the whole point is to wait the endpoint out.
#
# Time has to be the binding constraint because attempts are consumed at a rate we do
# not control: while some parts are getting through, the shared brake keeps releasing,
# so a heavily throttled part can burn attempts quickly without much time passing. A
# 64 MiB asset against an endpoint rejecting 94% of requests exhausted a 24-attempt
# budget in 55 seconds of a 600 second allowance, and failed while nearly the whole
# allowance was unspent.
MAX_THROTTLE_RETRY_SECONDS = 600.0

# A loose backstop against a pathological endpoint that rejects instantly and forever,
# where the time budget alone would mean a very large number of requests. Deliberately
# high enough that the time budget is what normally decides.
MAX_THROTTLE_ATTEMPTS = 100

# Parts of one asset are thrown at S3 together, so they also get throttled together,
# and an unjittered backoff would march them all back in step - a thundering herd
# aimed at an endpoint that just asked for less traffic. Each sleep is spread over
# the interval it would otherwise be, up to half again as long, which decorrelates
# the attempts without ever retrying sooner than the configured backoff: when the
# server has asked for a slower request rate, erring short is the wrong direction.
# Only the part path needs this; the single-request operations around it have
# nothing to collide with.
PART_UPLOAD_RETRY_JITTER = 0.5

LOGGER = logging.getLogger(__name__)


class UploadResult(NamedTuple):
    response: Optional[Response]
    retry_attempts: int
    failed: bool
    has_connection_error: bool


class UploadRetryStrategyOp(object):
    """A strategy to perform upload operations with defined retry attempt counts
    for different stages of S3 direct upload.

    Args:
        max_upload_start_attempts: number of attempts for upload-start call.
        max_upload_complete_attempts: number of attempts for S3 AWS part upload
        max_s3_file_part_upload_attempts: number of attempts for S3 AWS part upload
    """

    def __init__(
        self,
        max_upload_start_attempts: int,
        max_upload_complete_attempts: int,
        max_s3_file_part_upload_attempts: int,
        retry_backoff_factor: float,
    ):
        self.max_upload_start_attempts = max_upload_start_attempts
        self.max_upload_complete_attempts = max_upload_complete_attempts
        self.max_s3_file_part_upload_attempts = max_s3_file_part_upload_attempts
        self.retry_backoff_factor = retry_backoff_factor

    @classmethod
    def default_upload_retry_strategy(cls):
        return UploadRetryStrategyOp(
            max_upload_start_attempts=MAX_UPLOAD_START_ATTEMPTS,
            max_upload_complete_attempts=MAX_UPLOAD_COMPLETE_ATTEMPTS,
            max_s3_file_part_upload_attempts=MAX_S3_PART_UPLOAD_ATTEMPTS,
            retry_backoff_factor=UPLOAD_FILE_RETRY_BACKOFF_FACTOR,
        )

    def start_multipart_upload(
        self,
        session: Session,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, Any],
        throttle_gate: Any = None,
    ) -> UploadResult:
        result = _request_with_retries(
            session=session,
            method="POST",
            url=url,
            json_payload=payload,
            data=None,
            headers=headers,
            max_retries=self.max_upload_start_attempts,
            retry_backoff_factor=self.retry_backoff_factor,
            retry_on_bad_response_status=True,
            allowed_retry_status_codes=RETRYABLE_CONTROL_PLANE_STATUS_CODES,
            retry_jitter=PART_UPLOAD_RETRY_JITTER,
            throttle_gate=throttle_gate,
        )
        _raise_for_comet_bad_status_or_failure(
            result=result, operation="start S3 direct upload"
        )

        return result

    def complete_multipart_upload(
        self,
        session: Session,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, Any],
        throttle_gate: Any = None,
    ) -> UploadResult:
        result = _request_with_retries(
            session=session,
            method="POST",
            url=url,
            json_payload=payload,
            data=None,
            headers=headers,
            max_retries=self.max_upload_complete_attempts,
            retry_backoff_factor=self.retry_backoff_factor,
            retry_on_bad_response_status=True,
            allowed_retry_status_codes=RETRYABLE_CONTROL_PLANE_STATUS_CODES,
            retry_jitter=PART_UPLOAD_RETRY_JITTER,
            throttle_gate=throttle_gate,
        )
        _raise_for_comet_bad_status_or_failure(
            result=result, operation="complete S3 direct upload"
        )

        return result

    def upload_s3_file_part(
        self,
        session: Session,
        url: str,
        file_data: Any,
        throttle_gate: Any = None,
    ) -> UploadResult:
        # retrying also on 500 response status (see description: https://comet-ml.atlassian.net/browse/CM-10420)
        result = _request_with_retries(
            session=session,
            method="PUT",
            url=url,
            json_payload=None,
            data=file_data,
            headers=None,
            max_retries=self.max_s3_file_part_upload_attempts,
            retry_backoff_factor=self.retry_backoff_factor,
            retry_on_bad_response_status=True,
            allowed_retry_status_codes=RETRYABLE_PART_UPLOAD_STATUS_CODES,
            retry_jitter=PART_UPLOAD_RETRY_JITTER,
            throttle_gate=throttle_gate,
        )
        return result


def _raise_for_comet_bad_status_or_failure(result: UploadResult, operation: str):
    if result.failed and result.response is not None:
        LOGGER.debug(
            "Bad response for %s, status: %d, text: %r",
            operation,
            result.response.status_code,
            result.response.text,
        )
        result.response.raise_for_status()

    if result.failed:
        if result.response is not None:
            LOGGER.warning(
                "Bad response received when trying to %s, code: %d, text: %r",
                operation,
                result.response.status_code,
                result.response.text,
            )
        raise S3UploadError(
            reason="Failed to %s due to recurrent connection error with Comet backend"
            % operation,
            due_connection_error=result.has_connection_error,
        )


def _request_with_retries(
    session: Session,
    method: str,
    url: str,
    json_payload: Optional[Dict[str, Any]],
    data: Any,
    headers: Optional[Dict[str, Any]],
    max_retries: int,
    retry_backoff_factor: float,
    retry_on_bad_response_status: bool = False,
    allowed_retry_status_codes: Optional[List[int]] = None,
    retry_jitter: float = 0.0,
    throttle_gate: Any = None,
) -> UploadResult:
    # Two budgets, because the two failures deserve different patience. A server
    # error is probably not going to clear, so it keeps the caller's attempt count.
    # A throttling response is a promise to accept the request later, so abandoning
    # it early discards an upload that was going to succeed: it gets its own, much
    # larger budget, bounded by wall clock so that waiting cannot outlive the
    # presigned URL being waited on.
    error_attempts = 0
    throttle_attempts = 0
    started_at = time.monotonic()

    retry_attempt = 0
    response = None
    while True:
        if throttle_gate is not None:
            # Blocks while any part upload in this process is being rate limited,
            # including before the first attempt: a part that starts while the
            # endpoint is complaining should wait rather than add to the pile.
            #
            # Bounded by what is left of this request's own throttling budget, so a
            # brake applied on behalf of other uploads cannot hold this one past the
            # point where it would be allowed to retry anyway.
            budget_left = MAX_THROTTLE_RETRY_SECONDS - (time.monotonic() - started_at)
            if not throttle_gate.wait_until_open(timeout=max(0.0, budget_left)):
                LOGGER.debug(
                    "Giving up on %r for URL %r: still rate limited with no time left "
                    "in the %.0fs budget.",
                    method,
                    url,
                    MAX_THROTTLE_RETRY_SECONDS,
                )
                break

        if retry_attempt > 0:
            # A body that is a stream rather than bytes has already been consumed
            # by the failed attempt, so it has to be put back to its start before
            # it can be sent again. Duck typed on purpose: bytes need nothing, and
            # this module must not depend on the parts package that imports it.
            rewind = getattr(data, "rewind", None)
            if callable(rewind):
                rewind()

        try:
            response = session.request(
                method=method,
                url=url,
                json=json_payload,
                data=data,
                headers=headers,
            )
            failed = False
        except (ConnectionError, requests.ConnectionError):
            failed = True
            response = None
            LOGGER.debug(
                "ConnectionError when do %r for URL %r. Attempt: %d of %d.",
                method,
                url,
                retry_attempt,
                max_retries,
                exc_info=True,
            )

        retry_attempt += 1

        if response is not None and response.status_code != 200:
            failed = True
            if not retry_on_bad_response_status:
                # do not retry on bad status code - fail immediately
                return UploadResult(
                    response=response,
                    retry_attempts=retry_attempt,
                    failed=True,
                    has_connection_error=False,
                )
            elif (
                allowed_retry_status_codes is not None
                and response.status_code not in allowed_retry_status_codes
            ):
                # status_code isn't in allowed retry status codes - fail immediately
                return UploadResult(
                    response=response,
                    retry_attempts=retry_attempt,
                    failed=True,
                    has_connection_error=False,
                )

        if not failed:
            if throttle_gate is not None:
                # Enough of these and the shared brake returns to its floor.
                throttle_gate.report_success()

            return UploadResult(
                response=response,
                retry_attempts=retry_attempt,
                failed=False,
                has_connection_error=False,
            )

        throttled = (
            response is not None and response.status_code in THROTTLING_STATUS_CODES
        )

        if throttled:
            throttle_attempts += 1
            elapsed = time.monotonic() - started_at
            retry_after = _retry_after_seconds(response)

            if throttle_gate is not None:
                # The gate holds every part, and that wait happens at the top of the
                # next iteration, so this attempt must not sleep the backoff as well.
                # It is told what remains of the budget so that a server asking for
                # longer than that cannot park every upload in the process for it.
                hold = throttle_gate.report_throttled(
                    retry_after,
                    max_hold=max(0.0, MAX_THROTTLE_RETRY_SECONDS - elapsed),
                )
                backoff_time = 0.0
            else:
                hold = None
                backoff_time = _backoff_with_jitter(
                    retry_backoff_factor, throttle_attempts, retry_jitter
                )
                if retry_after is not None:
                    backoff_time = max(backoff_time, retry_after)
                # No gate here to bound the wait, so it is bounded against the same
                # budget the gate would have used. Otherwise a server asking for an
                # hour parks this thread for an hour, long after the budget that
                # decides whether to retry at all has run out.
                backoff_time = min(
                    backoff_time, max(0.0, MAX_THROTTLE_RETRY_SECONDS - elapsed)
                )

            if (
                throttle_attempts >= MAX_THROTTLE_ATTEMPTS
                or elapsed >= MAX_THROTTLE_RETRY_SECONDS
            ):
                LOGGER.debug(
                    "Giving up on %r for URL %r after %d rate limited attempts over "
                    "%.1fs.",
                    method,
                    url,
                    throttle_attempts,
                    elapsed,
                )
                break

            LOGGER.debug(
                "Rate limited on %r, URL %r. Throttled attempt %d of %d, %.1fs "
                "elapsed, waiting %.2fs.",
                method,
                url,
                throttle_attempts,
                MAX_THROTTLE_ATTEMPTS,
                elapsed,
                hold if hold is not None else backoff_time,
            )
            if backoff_time > 0:
                time.sleep(backoff_time)

            continue

        error_attempts += 1
        if error_attempts >= max_retries:
            break

        backoff_time = _backoff_with_jitter(
            retry_backoff_factor, error_attempts, retry_jitter
        )
        LOGGER.debug(
            "Failed to do %r, URL %r. Attempt: %d of %d. Retrying after: %r seconds",
            method,
            url,
            error_attempts,
            max_retries,
            backoff_time,
        )
        time.sleep(backoff_time)

    # every retry budget is spent
    return UploadResult(
        response=response,
        retry_attempts=retry_attempt,
        failed=True,
        has_connection_error=response is None,
    )


def _backoff_with_jitter(backoff_factor: float, attempt: int, jitter: float) -> float:
    backoff_time = calculate_backoff_time(
        backoff_factor=backoff_factor, retry_attempt=attempt
    )
    if jitter > 0:
        backoff_time *= 1.0 + jitter * random.random()

    return backoff_time


def _retry_after_seconds(response: Optional[Response]) -> Optional[float]:
    """The server's own instruction on how long to wait, when it sent one.

    A server that says how long to back off knows better than any doubling
    heuristic, so this wins wherever it is present. Both forms the header permits
    are accepted, and anything unparseable is ignored rather than trusted.
    """
    if response is None:
        return None

    raw = response.headers.get("Retry-After")
    if raw is None:
        return None

    try:
        return _finite_seconds(float(raw))
    except (TypeError, ValueError):
        pass

    try:
        retry_at = email.utils.parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        LOGGER.debug("Could not parse Retry-After header %r", raw)
        return None

    now = datetime.datetime.now(tz=retry_at.tzinfo)

    return _finite_seconds((retry_at - now).total_seconds())


def _finite_seconds(value: float) -> Optional[float]:
    """A delay we are willing to act on, or None.

    "Retry-After: inf" parses as a float perfectly well, and on the path with no
    shared gate to bound it that reached time.sleep() directly - a worker thread
    parked forever on a header. Anything not finite is treated as absent rather than
    trusted; the caller then falls back to its own backoff.
    """
    if not math.isfinite(value):
        LOGGER.debug("Ignoring a non-finite Retry-After value: %r", value)
        return None

    return max(0.0, value)
