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
from typing import Any, Optional

from ....config import config_constants

LOGGER = logging.getLogger(__name__)

CONFIG_KEY_UPLOAD_CONCURRENCY = "comet.s3_multipart.upload_concurrency"
CONFIG_KEY_TOTAL_UPLOAD_CONCURRENCY = "comet.internal.s3_multipart_total_concurrency"

DEFAULT_PARTS_UPLOAD_CONCURRENCY = (
    config_constants.S3_MULTIPART_UPLOAD_CONCURRENCY_DEFAULT
)
MIN_PARTS_UPLOAD_CONCURRENCY = config_constants.S3_MULTIPART_UPLOAD_CONCURRENCY_MIN
MAX_PARTS_UPLOAD_CONCURRENCY = config_constants.S3_MULTIPART_UPLOAD_CONCURRENCY_MAX


class PartsUploadOptions(object):
    """How per-part parallelism is bounded.

    There is one knob and one ceiling, and only the knob is meant to be tuned.

    ``concurrency`` caps the parts of a *single* asset. This is the new limit
    this feature introduces, it is what makes one large checkpoint fast, and its
    default of 8 is in line with the other transfer libraries (boto3 uses 10,
    the GCS transfer manager 8, rclone 4 with 8 recommended).

    ``total_concurrency`` caps the parts in flight across *every* asset at once,
    and is a ceiling rather than a knob. It is not new behaviour: before parts
    could be uploaded concurrently, each asset uploaded its parts serially on its
    own asset-pool thread, so the process was already limited to one in-flight
    PUT per asset thread. Left unset it resolves to the asset pool size, which
    reproduces that limit exactly, so adding per-part parallelism can neither
    lower the total concurrency an upload already had nor raise peak resident
    part data above what it already was.

    Removing either one has a measured cost. Without the ceiling, N concurrent
    assets hold N x concurrency parts resident, eight times more memory for no
    extra speed. Without the per-asset cap, a single asset takes the whole
    ceiling, which is past the point of diminishing returns and scales badly once
    the sibling ticket makes parts larger.

    This is the only type that knows what the tunables are, and from_config() is
    the only place that knows how they are read.
    """

    def __init__(self, concurrency: int, total_concurrency: Optional[int]):
        """Prefer the factories. Both values are required here so that no layer
        can quietly supply its own idea of a default."""
        self.concurrency = _clamp_concurrency(concurrency)
        self._total_concurrency = total_concurrency

    @classmethod
    def defaults(cls) -> "PartsUploadOptions":
        """The built-in defaults, in one place."""
        return cls(concurrency=DEFAULT_PARTS_UPLOAD_CONCURRENCY, total_concurrency=None)

    @classmethod
    def of(
        cls, concurrency: int, total_concurrency: Optional[int] = None
    ) -> "PartsUploadOptions":
        """Explicit values, for tests and for callers that know what they want."""
        return cls(concurrency=concurrency, total_concurrency=total_concurrency)

    def resolve_total_concurrency(self, asset_pool_size: int) -> int:
        """Total parts in flight allowed across all assets.

        Never lower than the per-asset cap, and never lower than the asset pool
        size, so that adding per-part parallelism can not reduce the concurrency
        an upload already had.

        The asset pool size is used as given rather than clamped. Clamping it would
        break the promise above: an asset pool configured with 128 threads already
        ran 128 uploads at once, each holding one part, so capping the ceiling at 64
        would halve the concurrency this change is supposed to preserve. The bound on
        that number belongs to whoever sizes the asset pool. An explicitly configured
        ceiling is still clamped, because that one is a knob with a documented range.
        """
        if self._total_concurrency is not None:
            return max(_clamp_total(self._total_concurrency), self.concurrency)

        return max(asset_pool_size, self.concurrency)

    @classmethod
    def from_config(cls, config: Any) -> "PartsUploadOptions":
        concurrency = config.get_int(None, CONFIG_KEY_UPLOAD_CONCURRENCY)
        if concurrency is None:
            concurrency = DEFAULT_PARTS_UPLOAD_CONCURRENCY

        return cls(
            concurrency=concurrency,
            total_concurrency=config.get_raw(None, CONFIG_KEY_TOTAL_UPLOAD_CONCURRENCY),
        )

    def __repr__(self) -> str:
        return "PartsUploadOptions(concurrency=%d, total_concurrency=%r)" % (
            self.concurrency,
            self._total_concurrency,
        )


def _clamp_total(total: Any) -> int:
    try:
        value = int(total)
    except (TypeError, ValueError):
        return DEFAULT_PARTS_UPLOAD_CONCURRENCY

    return max(MIN_PARTS_UPLOAD_CONCURRENCY, min(value, MAX_PARTS_UPLOAD_CONCURRENCY))


def _clamp_concurrency(concurrency: Optional[int]) -> int:
    if concurrency is None:
        return DEFAULT_PARTS_UPLOAD_CONCURRENCY

    try:
        concurrency = int(concurrency)
    except (TypeError, ValueError):
        LOGGER.debug(
            "Invalid S3 parts upload concurrency %r, falling back to %d",
            concurrency,
            DEFAULT_PARTS_UPLOAD_CONCURRENCY,
        )
        return DEFAULT_PARTS_UPLOAD_CONCURRENCY

    if concurrency < MIN_PARTS_UPLOAD_CONCURRENCY:
        LOGGER.debug(
            "S3 parts upload concurrency %d is below the minimum, using %d",
            concurrency,
            MIN_PARTS_UPLOAD_CONCURRENCY,
        )
        return MIN_PARTS_UPLOAD_CONCURRENCY

    if concurrency > MAX_PARTS_UPLOAD_CONCURRENCY:
        LOGGER.debug(
            "S3 parts upload concurrency %d is above the maximum, using %d",
            concurrency,
            MAX_PARTS_UPLOAD_CONCURRENCY,
        )
        return MAX_PARTS_UPLOAD_CONCURRENCY

    return concurrency
