# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
from typing import Callable, Optional

import requests

from ....connection import http_session
from .. import retry_strategy as retry_strategy_module, upload_error
from . import part_types, readers, throttling

LOGGER = logging.getLogger(__name__)

SessionProvider = Callable[[], requests.Session]


def default_session_provider() -> requests.Session:
    """Returns the session used for direct calls to S3.

    The session carries no Comet headers because this goes straight to S3, and it
    has no transport level retries because retrying is owned by
    UploadRetryStrategyOp. Sessions are cached per thread, so every worker of a
    parts pool gets its own connection and keeps reusing it across parts.
    """
    return http_session.get_cached_http_session(
        retry=False, verify_tls=True, tcp_keep_alive=False
    )


class RetryingPartSender(object):
    """Sends one part through the existing upload retry strategy.

    Safe to call concurrently from several threads: it keeps no per-part state.
    Anything with a matching send() can stand in for it, which is how the tests
    substitute failures and count concurrency.

    Retry counting, backoff and the set of retryable statuses all stay in
    UploadRetryStrategyOp; this class only translates its result into either a
    PartMetadata or an S3UploadFileError.
    """

    def __init__(
        self,
        retry_strategy: retry_strategy_module.UploadRetryStrategyOp,
        file_name: str,
        session_provider: Optional[SessionProvider] = None,
        throttle_gate: Optional[throttling.ThrottleGate] = None,
    ):
        self._retry_strategy = retry_strategy
        self._file_name = file_name
        # Shared with every other part upload in the process, because a rate limit
        # belongs to the endpoint rather than to any one asset.
        self._throttle_gate = (
            throttle_gate if throttle_gate is not None else throttling.default_gate()
        )
        self._session_provider = (
            session_provider
            if session_provider is not None
            else default_session_provider
        )

    def send(self, part: part_types.FilePart) -> part_types.PartMetadata:
        try:
            result = self._retry_strategy.upload_s3_file_part(
                session=self._session_provider(),
                url=part.url,
                file_data=part.body,
                throttle_gate=self._throttle_gate,
            )
        finally:
            # A streamed part holds a file handle; a bytes part holds nothing.
            part.close()

        response = result.response
        if not result.failed and response is not None and response.status_code == 200:
            return part_types.PartMetadata(
                e_tag=response.headers["ETag"],
                part_number=part.part_number,
                size=part.size,
            )

        if response is not None:
            message = (
                "S3 file part #%d upload failed in %d attempt(s), got response - status: %d, text: %r"
                % (
                    part.part_number,
                    result.retry_attempts,
                    response.status_code,
                    response.text,
                )
            )
        else:
            message = "S3 file part #%d upload failed in %d attempt(s)" % (
                part.part_number,
                result.retry_attempts,
            )

        LOGGER.debug(message)
        raise upload_error.S3UploadFileError(
            file=self._file_name,
            reason=message,
            retry_attempts=result.retry_attempts,
            due_connection_error=result.has_connection_error,
        )
