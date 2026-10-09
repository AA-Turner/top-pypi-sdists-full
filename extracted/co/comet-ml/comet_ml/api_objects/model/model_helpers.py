# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import io
import logging
import os
from typing import Any, Dict, Optional

from comet_ml import logging_messages, parallel_utils
from comet_ml.assets import data_writers
from comet_ml.assets.data_writers import AssetDataWriterFromResponse
from comet_ml.exceptions import RemoteModelDownloadException
from comet_ml.file_downloader import FileDownloadSizeMonitor
from comet_ml.logging_messages import REMOTE_MODEL_DOWNLOAD_FILE_OVERWRITTEN
from comet_ml.s3.multipart_download import (
    MultipartDownloadOptions,
    S3MultipartDownloader,
)
from comet_ml.s3.multipart_transfer import PartsTransferPool, create_parts_transfer_pool

LOGGER = logging.getLogger(__name__)


def has_direct_s3_download_enabled(download_instructions: Dict[str, Any]) -> bool:
    return download_instructions.get("s3DownloadEnabled", False)


class LazyPartsPool:
    """The pool that fetches byte ranges for every direct-S3 asset of one download.

    Created on the first asset that actually goes direct, because the executor
    pre-spawns every worker it is sized for, and a model with no S3 assets should
    not pay for a poolful of idle threads. Must be a different executor from the
    one downloading whole assets: those tasks block waiting on their ranges, so
    sharing one bounded executor deadlocks once every worker holds an asset.

    Only get() and shutdown() are called, both from the thread driving the
    download, so no locking is needed.
    """

    def __init__(self, options: MultipartDownloadOptions, asset_pool_size: int):
        self._options = options
        self._asset_pool_size = asset_pool_size
        self._pool: Optional[PartsTransferPool] = None

    def get(self) -> PartsTransferPool:
        if self._pool is None:
            self._pool = create_parts_transfer_pool(
                options=self._options.parts_download_options,
                asset_pool_size=self._asset_pool_size,
            )
        return self._pool

    def shutdown(self) -> None:
        """Releases the workers and waits for them.

        Call only after every asset task has finished, so none is left waiting on a range.
        """
        if self._pool is None:
            return

        self._pool.close()
        self._pool.join()
        self._pool = None


def _prepare_asset_path(asset_id: str, asset_path: str) -> None:
    if os.path.exists(asset_path):
        LOGGER.warning(REMOTE_MODEL_DOWNLOAD_FILE_OVERWRITTEN, asset_path, asset_id)
    else:
        try:
            parent_dir = os.path.dirname(asset_path)
            parallel_utils.makedirs_synchronized(parent_dir, exist_ok=True)
        except Exception:
            LOGGER.debug(
                "Error creating parent directories for the asset file", exc_info=True
            )
            raise RemoteModelDownloadException(
                logging_messages.ASSET_WRITE_ERROR
                % (
                    asset_id,
                    asset_path,
                )
            )


def _write_asset_data_to_disk(
    asset_id: str,
    asset_path: str,
    writer: data_writers.AssetDataWriter,
) -> None:
    _prepare_asset_path(asset_id=asset_id, asset_path=asset_path)

    try:
        with io.open(asset_path, "wb") as f:
            writer.write(file=f)
    except Exception:
        LOGGER.debug("Error writing file on path", exc_info=True)
        raise RemoteModelDownloadException(
            logging_messages.ASSET_WRITE_ERROR
            % (
                asset_id,
                asset_path,
            )
        )


def download_cloud_storage_remote_model_asset(
    data_writer: data_writers.AssetDataWriter,
    asset_id: str,
    remote_model_repr: str,
    asset_path: str,
    _monitor: Optional[FileDownloadSizeMonitor] = None,
) -> None:
    try:
        data_writer.monitor = _monitor
        _write_asset_data_to_disk(
            asset_id=asset_id,
            asset_path=asset_path,
            writer=data_writer,
        )
    except Exception as ex:
        LOGGER.debug(
            "Error writing S3/GCS remote model asset with ID: %d as file on path: %r",
            asset_id,
            asset_path,
        )
        raise RemoteModelDownloadException(
            logging_messages.REMOTE_MODEL_ASSET_DOWNLOAD_FAILED_REPR
            % (asset_id, remote_model_repr)
        ) from ex
    return None


def download_model_asset(
    experiment_key: str,
    asset_id: str,
    remote_model_repr: str,
    asset_path: str,
    rest_api_client,
    _monitor: Optional[FileDownloadSizeMonitor] = None,
) -> None:
    try:
        response = rest_api_client.get_experiment_asset(
            asset_id=asset_id,
            experiment_key=experiment_key,
            return_type="response",
            stream=True,
        )
    except Exception as ex:
        LOGGER.debug(
            "Failed to directly download asset into file: %r, asset ID: %r, experiment key: %r",
            asset_path,
            asset_id,
            experiment_key,
        )
        raise RemoteModelDownloadException(
            logging_messages.REMOTE_MODEL_ASSET_DOWNLOAD_FAILED_REPR
            % (asset_id, remote_model_repr)
        ) from ex

    try:
        _write_asset_data_to_disk(
            asset_id=asset_id,
            asset_path=asset_path,
            writer=AssetDataWriterFromResponse(response=response, monitor=_monitor),
        )
    finally:
        try:
            response.close()
        except Exception:
            LOGGER.debug("Error closing model asset download response", exc_info=True)
            pass


def download_s3_model_asset(
    url: str,
    asset_id: str,
    remote_model_repr: str,
    asset_path: str,
    verify_tls: bool = True,
    *,
    download_options: Optional[MultipartDownloadOptions] = None,
    parts_pool: Optional[PartsTransferPool] = None,
    _monitor: Optional[FileDownloadSizeMonitor] = None,
) -> None:
    """Downloads a model asset straight from its presigned S3 URL.

    In parallel byte ranges when a parts pool is given and the object is larger than
    one part, and as a single stream otherwise. See S3MultipartDownloader.
    """
    if download_options is None:
        download_options = MultipartDownloadOptions.defaults()

    _prepare_asset_path(asset_id=asset_id, asset_path=asset_path)

    # this is direct S3 download - no need for Comet specific http session
    downloader = S3MultipartDownloader.create(
        url=url,
        file_path=asset_path,
        options=download_options,
        parts_pool=parts_pool,
        verify_tls=verify_tls,
    )
    try:
        downloader.download(monitor=_monitor)
    except Exception as ex:
        LOGGER.debug(
            "Failed to directly download asset from S3. Asset path: %r, asset ID: %r",
            asset_path,
            asset_id,
            exc_info=True,
        )
        raise RemoteModelDownloadException(
            logging_messages.REMOTE_MODEL_ASSET_DOWNLOAD_FAILED_REPR
            % (asset_id, remote_model_repr)
        ) from ex
