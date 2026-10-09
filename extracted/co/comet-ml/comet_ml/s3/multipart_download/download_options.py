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
from typing import Any, Dict, Optional

from ...config import config_constants
from ..multipart_transfer import transfer_options

LOGGER = logging.getLogger(__name__)

CONFIG_KEY_DOWNLOAD_CONCURRENCY = "comet.s3_multipart.download_concurrency"
CONFIG_KEY_TOTAL_DOWNLOAD_CONCURRENCY = (
    "comet.internal.s3_multipart_download_total_concurrency"
)
CONFIG_KEY_DOWNLOAD_PART_SIZE = "comet.s3_multipart.download_part_size"
CONFIG_KEY_DOWNLOAD_TIMEOUT = "comet.timeout.file_download"

DEFAULT_DOWNLOAD_PART_SIZE = config_constants.S3_MULTIPART_DOWNLOAD_PART_SIZE_DEFAULT
MIN_DOWNLOAD_PART_SIZE = config_constants.S3_MULTIPART_DOWNLOAD_PART_SIZE_MIN
MAX_DOWNLOAD_PART_SIZE = config_constants.S3_MULTIPART_DOWNLOAD_PART_SIZE_MAX


DOWNLOAD_LIMITS = transfer_options.TransferLimits(
    config_key=CONFIG_KEY_DOWNLOAD_CONCURRENCY,
    total_config_key=CONFIG_KEY_TOTAL_DOWNLOAD_CONCURRENCY,
    default=config_constants.S3_MULTIPART_DOWNLOAD_CONCURRENCY_DEFAULT,
    minimum=config_constants.S3_MULTIPART_DOWNLOAD_CONCURRENCY_MIN,
    maximum=config_constants.S3_MULTIPART_DOWNLOAD_CONCURRENCY_MAX,
)


class PartsDownloadOptions(transfer_options.PartsTransferOptions):
    """How per-range parallelism is bounded for download.

    The same shape as the upload side, a per-asset cap plus a process-wide ceiling
    that follows the asset pool, and for the same reasons. Only the cost of a part
    in flight is different: a range is written to disk as it arrives, so what
    concurrency multiplies here is open connections rather than resident memory.
    """

    LIMITS = DOWNLOAD_LIMITS


class MultipartDownloadOptions:
    """Everything a direct-S3 download needs to know, read from config in one place."""

    def __init__(
        self,
        part_size: int,
        parts_download_options: PartsDownloadOptions,
        request_timeout: Optional[float],
    ):
        """Prefer from_config() or defaults()."""
        self.part_size = clamp_part_size(part_size)
        self.parts_download_options = parts_download_options
        # Per request, as requests applies it: to connecting and to each read, not to
        # the whole range. Without one, a socket that stalls without closing parks
        # its worker for good, and the asset with it.
        self.request_timeout = request_timeout

    @classmethod
    def from_config(cls, config: Any) -> "MultipartDownloadOptions":
        return cls(
            part_size=config.get_int(None, CONFIG_KEY_DOWNLOAD_PART_SIZE),
            parts_download_options=PartsDownloadOptions.from_config(config),
            request_timeout=config.get_int(None, CONFIG_KEY_DOWNLOAD_TIMEOUT),
        )

    @classmethod
    def defaults(cls, **overrides: Any) -> "MultipartDownloadOptions":
        values: Dict[str, Any] = {
            "part_size": DEFAULT_DOWNLOAD_PART_SIZE,
            "parts_download_options": PartsDownloadOptions.defaults(),
            "request_timeout": None,
        }
        values.update(overrides)
        return cls(**values)

    def __repr__(self) -> str:
        return (
            "MultipartDownloadOptions(part_size=%d, parts_download_options=%r, "
            "request_timeout=%r)"
            % (self.part_size, self.parts_download_options, self.request_timeout)
        )


def clamp_part_size(part_size: Optional[int]) -> int:
    if part_size is None:
        return DEFAULT_DOWNLOAD_PART_SIZE

    try:
        part_size = int(part_size)
    except (TypeError, ValueError):
        LOGGER.debug(
            "Invalid S3 download part size %r, falling back to %d",
            part_size,
            DEFAULT_DOWNLOAD_PART_SIZE,
        )
        return DEFAULT_DOWNLOAD_PART_SIZE

    clamped = max(MIN_DOWNLOAD_PART_SIZE, min(part_size, MAX_DOWNLOAD_PART_SIZE))
    if clamped != part_size:
        LOGGER.debug(
            "S3 download part size %d is outside [%d, %d], using %d",
            part_size,
            MIN_DOWNLOAD_PART_SIZE,
            MAX_DOWNLOAD_PART_SIZE,
            clamped,
        )

    return clamped
