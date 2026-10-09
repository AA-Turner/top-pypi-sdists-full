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
"""Downloading one experiment asset to a file, straight from S3 when the backend allows it."""
import io
import logging
import socket
from typing import Optional
from urllib.parse import urljoin

import requests

# Also first on purpose: importing the connection package before s3.multipart_download
# is what keeps the cycle through api_objects.model from failing.
from ..connection.connection_api import RestApiClient
from ..exceptions import ExperimentAssetDownloadException
from ..file_downloader import (
    FileDownloadManager,
    FileDownloadManagerMonitor,
    FileDownloadSizeMonitor,
)
from ..logging_messages import (
    EXPERIMENT_ASSET_DOWNLOAD_FAILED,
    EXPERIMENT_ASSET_DOWNLOAD_TIMEOUT,
)
from ..s3.multipart_download import MultipartDownloadOptions, S3MultipartDownloader
from ..s3.multipart_download.downloader import (
    publish_file,
    remove_quietly,
    temporary_path_for,
)
from ..s3.multipart_transfer import CancellationToken, create_parts_transfer_pool
from ..utils import wait_for_done

LOGGER = logging.getLogger(__name__)

# One asset per call, so both pools are sized for a single asset.
_SINGLE_ASSET_POOL_SIZE = 1

# How often the progress of a download still running is logged, as Model.download does.
PROGRESS_LOG_INTERVAL = 15

# The block size the backend's response is read in, as write_stream_response_to_file does.
_CHUNK_SIZE_BYTES = 1024 * 1024

# OSErrors that are failures of the transfer rather than of the local file:
# requests' exceptions and socket errors all derive from OSError.
_NETWORK_OS_ERRORS = (
    requests.RequestException,
    ConnectionError,
    TimeoutError,
    socket.timeout,
)


def download_experiment_asset(
    rest_api_client: RestApiClient,
    experiment_key: str,
    asset_id: str,
    file_path: str,
    download_options: MultipartDownloadOptions,
    verify_tls: bool,
    timeout: float,
    log_progress: bool = False,
    progress_log_interval: float = PROGRESS_LOG_INTERVAL,
) -> None:
    """Downloads an experiment asset to file_path, optionally logging its progress.

    The download runs on a FileDownloadManager worker, and this thread waits up to
    timeout seconds for it. With log_progress, the remaining bytes, throughput and
    ETA are logged every progress_log_interval seconds meanwhile. Errors of the
    download are raised here.

    A download still running at the timeout is cancelled: once this raises, nothing
    is written to file_path, even by a worker that has not stopped yet.
    """
    cancel_token = CancellationToken()
    download_manager = FileDownloadManager(
        worker_cpu_ratio=_SINGLE_ASSET_POOL_SIZE, worker_count=_SINGLE_ASSET_POOL_SIZE
    )
    result = download_manager.download_file_async(
        download_func=download_experiment_asset_to_file,
        rest_api_client=rest_api_client,
        experiment_key=experiment_key,
        asset_id=asset_id,
        file_path=file_path,
        download_options=download_options,
        verify_tls=verify_tls,
        cancel_token=cancel_token,
    )
    download_manager.close()

    manager_monitor = FileDownloadManagerMonitor(download_manager)

    def log_remaining() -> None:
        # Until the size is known the manager counts nothing as remaining, and
        # would report a download that has barely started as completed.
        if result.monitor.total_size is not None:
            manager_monitor.log_remaining_downloads()

    wait_for_done(
        check_function=manager_monitor.all_done,
        timeout=timeout,
        progress_callback=log_remaining if log_progress else None,
        sleep_time=progress_log_interval,
    )

    timed_out = not result.ready()
    if timed_out:
        cancelled = cancel_token.cancel()
        if cancelled:
            # Not joined: the worker stops on its own at the latest when a read
            # stalled on the network times out, and removes its temporary file.
            raise ExperimentAssetDownloadException(
                EXPERIMENT_ASSET_DOWNLOAD_TIMEOUT % (asset_id, experiment_key, timeout)
            )
        # Too late to cancel: the file was published just after the wait ended,
        # so the download succeeded after all.

    download_manager.join()
    # Raises whatever the download raised.
    result.get()


def download_experiment_asset_to_file(
    rest_api_client: RestApiClient,
    experiment_key: str,
    asset_id: str,
    file_path: str,
    download_options: MultipartDownloadOptions,
    verify_tls: bool,
    cancel_token: Optional[CancellationToken] = None,
    _monitor: Optional[FileDownloadSizeMonitor] = None,
) -> None:
    """Downloads an experiment asset to file_path.

    The asset is asked for with allow301 and the redirect is not followed. A
    redirect carries the asset's presigned URL in the object store, which is
    downloaded in parallel byte ranges, without the Comet API key ever being sent
    there. A 200 means the backend serves the bytes itself, and they are streamed
    over that one response as before.

    Either way the bytes go to a temporary file, moved into place once complete,
    and only if cancel_token, when given, has not been canceled.
    """
    response = rest_api_client.get_experiment_asset_unredirected(
        asset_id=asset_id, experiment_key=experiment_key
    )
    try:
        if not response.is_redirect:
            _download_backend_response(
                response,
                file_path=file_path,
                cancel_token=cancel_token,
                monitor=_monitor,
            )
            return

        # Location may legally be relative to the URL that was asked.
        url = urljoin(response.url, response.headers["Location"])
    finally:
        response.close()

    LOGGER.debug(
        "Downloading experiment asset %r of experiment %r directly from S3 into %r",
        asset_id,
        experiment_key,
        file_path,
    )

    parts_pool = create_parts_transfer_pool(
        options=download_options.parts_download_options,
        asset_pool_size=_SINGLE_ASSET_POOL_SIZE,
    )
    try:
        downloader = S3MultipartDownloader.create(
            url=url,
            file_path=file_path,
            options=download_options,
            parts_pool=parts_pool,
            verify_tls=verify_tls,
            cancel_token=cancel_token,
        )
        try:
            # Sets the monitor's total size from the object's real size.
            downloader.download(monitor=_monitor)
        except Exception as ex:
            if isinstance(ex, OSError) and not isinstance(ex, _NETWORK_OS_ERRORS):
                # The file cannot be written: the OSError the API documents, as is.
                raise

            LOGGER.debug(
                "Failed to directly download experiment asset from S3. File path: %r, "
                "asset ID: %r, experiment key: %r",
                file_path,
                asset_id,
                experiment_key,
                exc_info=True,
            )
            raise ExperimentAssetDownloadException(
                EXPERIMENT_ASSET_DOWNLOAD_FAILED % (asset_id, experiment_key)
            ) from ex
    finally:
        parts_pool.close()
        parts_pool.join()


def _download_backend_response(
    response: requests.Response,
    file_path: str,
    cancel_token: Optional[CancellationToken],
    monitor: Optional[FileDownloadSizeMonitor],
) -> None:
    if monitor is not None:
        monitor.total_size = _content_length(response)

    temporary_path = temporary_path_for(file_path)
    try:
        with io.open(temporary_path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=_CHUNK_SIZE_BYTES):
                output_file.write(chunk)
                if monitor is not None:
                    monitor.monitor_callback(len(chunk))
                if cancel_token is not None:
                    cancel_token.raise_if_cancelled()

        publish_file(temporary_path, file_path, cancel_token)
    except BaseException:
        remove_quietly(temporary_path)
        raise


def _content_length(response: requests.Response) -> Optional[int]:
    try:
        return int(response.headers["Content-Length"])
    except (KeyError, TypeError, ValueError):
        return None
