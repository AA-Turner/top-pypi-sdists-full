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
import http.client
import logging
import socket
from typing import IO, Callable, Optional

import requests
import urllib3

from . import parts, range_requests
from .download_error import S3DownloadError

LOGGER = logging.getLogger(__name__)

# The same block size the existing single-stream download reads in.
CHUNK_SIZE_BYTES = 1024 * 1024

# What a connection going away looks like while a body is being read from the raw
# urllib3 stream, which does not translate its exceptions the way requests does.
BODY_NETWORK_ERRORS = (
    urllib3.exceptions.HTTPError,
    http.client.IncompleteRead,
    requests.ConnectionError,
    ConnectionError,
    socket.timeout,
    TimeoutError,
)


class StreamInterrupted(Exception):
    """The body stopped arriving. ``written`` says how much of it made it to disk."""

    def __init__(self, written: int, cause: Optional[BaseException]):
        super().__init__("stream interrupted after %d bytes" % written)
        self.written = written
        self.cause = cause


def stream_body_to_file(
    response: requests.Response,
    file: IO[bytes],
    limit: Optional[int],
    on_bytes: Optional[Callable[[int], None]] = None,
) -> int:
    """Writes the body at the file's current position. Returns the bytes written.

    Reads the raw bytes, without undoing any Content-Encoding. A range is a range of
    the stored object, and decoding it would make every length and offset here
    meaningless; it also means the file on disk is byte for byte the object in S3.

    ``limit`` is how much the range should hold. A body longer than that is an
    error rather than something to truncate quietly, because it means S3 answered
    a different question from the one that was asked. A body that ends short is
    StreamInterrupted, like one that is cut off, since both leave the range
    unfinished and the caller resumes both the same way.
    """
    written = 0
    stream = response.raw.stream(CHUNK_SIZE_BYTES, decode_content=False)
    while True:
        try:
            chunk = next(stream)
        except StopIteration:
            break
        except BODY_NETWORK_ERRORS as ex:
            raise StreamInterrupted(written, ex) from ex

        if limit is not None and written + len(chunk) > limit:
            raise S3DownloadError(
                reason="S3 sent more than the %d bytes requested for the range" % limit
            )

        # Outside the network try on purpose: a full disk is an OSError too, and
        # retrying the download will not make room on it.
        file.write(chunk)
        written += len(chunk)
        if on_bytes is not None:
            on_bytes(len(chunk))

    if limit is not None and written < limit:
        raise StreamInterrupted(written, None)

    return written


class RangedPartReceiver:
    """Fetches one range into its place in the file.

    The download counterpart of the upload side's RetryingPartSender.

    Safe to call concurrently from several threads: each call opens its own handle
    on the file, and the ranges never overlap, so no two writers touch the same
    bytes.

    A range cut off part-way resumes from the first byte that did not
    arrive rather than starting over, so an interruption costs the bytes
    in flight, not the whole range. That matters more than it would for upload: a
    5 GiB range restarted from zero on every drop over a flaky link may never finish.
    """

    def __init__(
        self,
        requester: range_requests.RangeRequester,
        file_path: str,
        if_match: Optional[str],
        on_bytes: Optional[Callable[[int], None]] = None,
        max_error_attempts: int = range_requests.MAX_S3_PART_DOWNLOAD_ATTEMPTS,
    ):
        self._requester = requester
        self._file_path = file_path
        self._if_match = if_match
        self._on_bytes = on_bytes
        self._max_error_attempts = max_error_attempts

    def transfer_part(self, part: parts.DownloadPart) -> parts.ReceivedPart:
        budget = range_requests.RetryBudget(self._max_error_attempts)
        response = part.take_response()
        received = 0

        try:
            with open(self._file_path, "r+b") as file:
                while received < part.length:
                    offset = part.start + received
                    if response is None:
                        response = self._requester.open(
                            first=offset,
                            last=part.last,
                            if_match=self._if_match,
                            budget=budget,
                            accepted=(206,),
                        )
                        _check_range(response, offset, part.last)

                    file.seek(offset)
                    try:
                        received += stream_body_to_file(
                            response,
                            file,
                            limit=part.length - received,
                            on_bytes=self._on_bytes,
                        )
                        continue
                    except StreamInterrupted as ex:
                        received += ex.written
                        if ex.written > 0:
                            budget.progress_made()
                        cause = ex.cause
                    finally:
                        response.close()
                        response = None

                    self._requester.after_error(
                        budget,
                        reason="S3 file part #%d was cut off after %d of %d bytes%s"
                        % (
                            part.part_number,
                            received,
                            part.length,
                            "" if cause is None else " (%s)" % cause,
                        ),
                        due_connection_error=True,
                    )
        finally:
            if response is not None:
                response.close()

        return parts.ReceivedPart(part_number=part.part_number, size=received)


def _check_range(response: requests.Response, first: int, last: int) -> None:
    content_range = range_requests.parse_content_range(
        response.headers.get("Content-Range")
    )
    if (
        content_range is None
        or content_range.first != first
        or content_range.last != last
    ):
        response.close()
        raise S3DownloadError(
            reason="S3 answered range %d-%d with Content-Range %r"
            % (first, last, response.headers.get("Content-Range")),
            status_code=response.status_code,
        )
