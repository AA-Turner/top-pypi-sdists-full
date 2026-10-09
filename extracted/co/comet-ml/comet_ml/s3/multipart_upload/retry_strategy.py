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
import logging
import time
from typing import Any, Dict, List, NamedTuple, Optional

import requests
from requests import Response, Session

from ...config import UPLOAD_FILE_MAX_RETRIES, UPLOAD_FILE_RETRY_BACKOFF_FACTOR
from ..multipart_transfer import retry_policy
from ..multipart_transfer.retry_policy import (
    MAX_THROTTLE_ATTEMPTS,
    MAX_THROTTLE_RETRY_SECONDS,
    SERVER_ERROR_STATUS_CODES,
    THROTTLING_STATUS_CODES,
)
from .upload_error import S3UploadError

MAX_UPLOAD_START_ATTEMPTS = UPLOAD_FILE_MAX_RETRIES
MAX_S3_PART_UPLOAD_ATTEMPTS = UPLOAD_FILE_MAX_RETRIES
MAX_UPLOAD_COMPLETE_ATTEMPTS = UPLOAD_FILE_MAX_RETRIES

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

# Kept under its old name for the part upload path, which is what it was tuned on.
PART_UPLOAD_RETRY_JITTER = retry_policy.PART_RETRY_JITTER

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
            retry_after = retry_policy.retry_after_seconds(response)

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
                backoff_time = retry_policy.backoff_with_jitter(
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

        backoff_time = retry_policy.backoff_with_jitter(
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
