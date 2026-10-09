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
import os
import uuid
from typing import Any, Optional

import requests

from ..multipart_transfer import (
    CancellationToken,
    PartsTransferPool,
    PartsTransferScheduler,
    ThrottleGate,
    create_parts_transfer_scheduler,
)
from . import collectors, parts, range_requests, receivers
from .download_error import S3DownloadError
from .download_options import MultipartDownloadOptions

LOGGER = logging.getLogger(__name__)


class S3MultipartDownloader:
    """Downloads one object from a presigned S3 URL, in parallel ranges where it can.

    The first request is a ranged GET for the first part. Its answer settles
    everything else, without a separate HEAD - which a presigned GET URL would
    refuse anyway, since the method is part of what is signed:

    * 206 with a known total: ranges are supported. The object's size and ETag come
      from the headers, the body already in flight becomes part one, and the rest of
      the parts are fetched through the scheduler. An object no larger than one part
      is therefore a single request, exactly as before.
    * 200: whatever is serving the URL ignored the Range header, so the body is the
      whole object and is streamed as it is, the way every download worked before.
    * 416: the object is empty, and there are no bytes to ask a range of.

    The scheduler is the upload side's, reused unchanged: it is serial without a
    pool and parallel with one, and in either case bounds the parts of this asset
    and of every asset sharing the pool.

    Bytes go to a temporary file next to the destination, which is renamed into
    place only once every range has been accounted for. A download that fails part
    way through therefore never leaves a file at the destination that looks complete
    and is not.

    With a cancel token, the download stops with TransferCancelled after the chunk
    of each range is written, or before its next request, sleep or wait on the throttle
    gate. Once the token is canceled, the destination is never touched, by this
    thread or by any range still running.
    """

    def __init__(
        self,
        url: str,
        file_path: str,
        options: MultipartDownloadOptions,
        scheduler: PartsTransferScheduler,
        requester: range_requests.RangeRequester,
        cancel_token: Optional[CancellationToken] = None,
    ):
        """Prefer create()."""
        self._url = url
        self._file_path = file_path
        self._options = options
        self._scheduler = scheduler
        self._requester = requester
        self._cancel_token = cancel_token

    @classmethod
    def create(
        cls,
        url: str,
        file_path: str,
        options: MultipartDownloadOptions,
        parts_pool: Optional[PartsTransferPool] = None,
        verify_tls: bool = True,
        session_provider: Optional[range_requests.SessionProvider] = None,
        throttle_gate: Optional[ThrottleGate] = None,
        cancel_token: Optional[CancellationToken] = None,
    ) -> "S3MultipartDownloader":
        """Without a parts pool, parts are fetched one after another on this thread."""
        return cls(
            url=url,
            file_path=file_path,
            options=options,
            scheduler=create_parts_transfer_scheduler(
                pool=parts_pool, options=options.parts_download_options
            ),
            requester=range_requests.RangeRequester(
                url=url,
                session_provider=(
                    session_provider
                    if session_provider is not None
                    else range_requests.session_provider_for(verify_tls)
                ),
                throttle_gate=(
                    throttle_gate
                    if throttle_gate is not None
                    else range_requests.default_download_gate()
                ),
                request_timeout=options.request_timeout,
                cancel_token=cancel_token,
            ),
            cancel_token=cancel_token,
        )

    def download(self, monitor: Optional[Any] = None) -> int:
        """Downloads the object to the destination path. Returns its size in bytes."""
        temporary_path = temporary_path_for(self._file_path)
        collector = collectors.DownloadPartsCollector(
            monitor=monitor, cancel_token=self._cancel_token
        )
        try:
            size = self._download_to(temporary_path, collector, monitor)
            publish_file(temporary_path, self._file_path, self._cancel_token)
        except BaseException:
            remove_quietly(temporary_path)
            raise

        return size

    def _download_to(
        self,
        path: str,
        collector: collectors.DownloadPartsCollector,
        monitor: Optional[Any],
    ) -> int:
        budget = range_requests.RetryBudget(
            range_requests.MAX_S3_PART_DOWNLOAD_ATTEMPTS
        )
        response = self._requester.open(
            first=0,
            last=self._options.part_size - 1,
            if_match=None,
            budget=budget,
            accepted=(200, 206, 416),
        )

        try:
            if response.status_code == 206:
                content_range = range_requests.parse_content_range(
                    response.headers.get("Content-Range")
                )
                if (
                    content_range is not None
                    and content_range.first == 0
                    and content_range.total is not None
                ):
                    return self._download_ranges(
                        path, response, content_range.total, collector, monitor
                    )

                # Partial content we cannot place in the file. Rare enough that the
                # plain GET below is the right answer rather than a failure.
                LOGGER.debug(
                    "Unusable Content-Range %r from S3, downloading as one stream",
                    response.headers.get("Content-Range"),
                )

            if response.status_code != 200:
                # Either the empty object's 416, or the unusable range above.
                response.close()
                response = self._requester.open(
                    first=None, last=None, if_match=None, budget=budget, accepted=(200,)
                )

            return self._download_whole(path, response, collector)
        finally:
            # Harmless when a part already owns it and closed it.
            response.close()

    def _download_ranges(
        self,
        path: str,
        first_response: requests.Response,
        total_size: int,
        collector: collectors.DownloadPartsCollector,
        monitor: Optional[Any],
    ) -> int:
        if monitor is not None:
            # The object's real size; the size the backend lists for the asset may differ.
            monitor.total_size = total_size

        source = parts.RangePartsSource(
            total_size=total_size,
            part_size=self._options.part_size,
            first_response=first_response,
        )
        LOGGER.debug(
            "Downloading %d bytes from S3 in %d range(s) of up to %d bytes",
            total_size,
            source.parts_number,
            self._options.part_size,
        )

        with open(path, "wb") as file:
            # Sized up front, so every worker writes into its own region of a file
            # that already has its final length.
            file.truncate(total_size)

        receiver = receivers.RangedPartReceiver(
            requester=self._requester,
            file_path=path,
            if_match=first_response.headers.get("ETag"),
            on_bytes=collector.on_bytes_received,
        )
        self._scheduler.transfer(
            source=source, transferrer=receiver, collector=collector
        )

        # The scheduler raises the first failure it sees, so reaching here should mean
        # every range landed. Checked anyway: the file was created at full length, so
        # a range that went missing would otherwise be a run of zeros that nothing
        # else would ever notice.
        if (
            collector.completed_parts_number() != source.parts_number
            or collector.completed_bytes != total_size
        ):
            raise S3DownloadError(
                reason="Only %d of %d ranges, %d of %d bytes, were downloaded"
                % (
                    collector.completed_parts_number(),
                    source.parts_number,
                    collector.completed_bytes,
                    total_size,
                )
            )

        return total_size

    def _download_whole(
        self,
        path: str,
        response: requests.Response,
        collector: collectors.DownloadPartsCollector,
    ) -> int:
        expected = _content_length(response)
        with open(path, "wb") as file:
            try:
                written = receivers.stream_body_to_file(
                    response,
                    file,
                    limit=expected,
                    on_bytes=collector.on_bytes_received,
                )
            except receivers.StreamInterrupted as ex:
                # Nothing to resume from: whatever served this does not take ranges.
                raise S3DownloadError(
                    reason="Download from S3 was cut off after %d bytes%s"
                    % (ex.written, "" if ex.cause is None else " (%s)" % ex.cause),
                    due_connection_error=True,
                ) from ex

        return written


def _content_length(response: requests.Response) -> Optional[int]:
    try:
        return int(response.headers["Content-Length"])
    except (KeyError, TypeError, ValueError):
        return None


def temporary_path_for(file_path: str) -> str:
    """A unique path next to file_path, to download into before publishing."""
    directory, name = os.path.split(file_path)
    return os.path.join(directory, ".%s.%s.cometdownload" % (name, uuid.uuid4().hex))


def publish_file(
    temporary_path: str, file_path: str, cancel_token: Optional[CancellationToken]
) -> None:
    """Moves a finished download into place, unless its download was canceled."""
    if cancel_token is None:
        os.replace(temporary_path, file_path)
    else:
        cancel_token.publish(lambda: os.replace(temporary_path, file_path))


def remove_quietly(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    except OSError:
        LOGGER.debug("Failed to remove partial download %r", path, exc_info=True)
