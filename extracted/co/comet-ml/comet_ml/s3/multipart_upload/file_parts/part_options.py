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
from ....config import config_constants
from ...multipart_transfer.transfer_options import PartsTransferOptions, TransferLimits

CONFIG_KEY_UPLOAD_CONCURRENCY = "comet.s3_multipart.upload_concurrency"
CONFIG_KEY_TOTAL_UPLOAD_CONCURRENCY = "comet.internal.s3_multipart_total_concurrency"

DEFAULT_PARTS_UPLOAD_CONCURRENCY = (
    config_constants.S3_MULTIPART_UPLOAD_CONCURRENCY_DEFAULT
)
MIN_PARTS_UPLOAD_CONCURRENCY = config_constants.S3_MULTIPART_UPLOAD_CONCURRENCY_MIN
MAX_PARTS_UPLOAD_CONCURRENCY = config_constants.S3_MULTIPART_UPLOAD_CONCURRENCY_MAX


UPLOAD_LIMITS = TransferLimits(
    config_key=CONFIG_KEY_UPLOAD_CONCURRENCY,
    total_config_key=CONFIG_KEY_TOTAL_UPLOAD_CONCURRENCY,
    default=DEFAULT_PARTS_UPLOAD_CONCURRENCY,
    minimum=MIN_PARTS_UPLOAD_CONCURRENCY,
    maximum=MAX_PARTS_UPLOAD_CONCURRENCY,
)


class PartsUploadOptions(PartsTransferOptions):
    """How per-part parallelism is bounded for upload.

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

    This is the only type that knows what the upload tunables are, and
    from_config() is the only place that knows how they are read.
    """

    LIMITS = UPLOAD_LIMITS
