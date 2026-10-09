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
"""Downloading a single direct-S3 object in parallel byte ranges.

    download_options  the part size and the per-asset and total concurrency
    range_requests    one ranged GET on the presigned URL, with the upload retry policy
    parts             the ranges, and the source that divides an object into them
    receivers         fetches one range into its place in the file, resuming on a drop
    collectors        what has been written, thread safely, for progress and checking
    downloader        probe, schedule, verify, move into place

The parts pool, its budgets, the schedulers, the throttle gate and the retry
policy come from multipart_transfer, shared with upload. The pool is created by
the caller that downloads whole assets, so that several assets share it.
"""
from .download_error import S3DownloadError
from .download_options import MultipartDownloadOptions, PartsDownloadOptions
from .downloader import S3MultipartDownloader

__all__ = [
    "MultipartDownloadOptions",
    "PartsDownloadOptions",
    "S3DownloadError",
    "S3MultipartDownloader",
]
