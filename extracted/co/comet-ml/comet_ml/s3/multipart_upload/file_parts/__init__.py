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
"""Uploading the parts of a single S3 multipart asset.

    part_types    FilePart, PartMetadata, the values that move between threads
    readers       one part's byte range of a file, as a non-resident body
    sources       reads an asset into parts, streaming from disk where possible
    senders       sends one part, with the existing retry strategy
    collectors    accumulates completed parts, thread safely, in S3's order
    part_options  the upload concurrency settings

What is not specific to upload - the budgets, the pool, the schedulers, the
throttle gate and the retry policy - lives in multipart_transfer, shared with
ranged download.

The names below are the package's public surface; inside the package the modules
import each other as modules.
"""
from .collectors import PartsCollector
from .part_options import PartsUploadOptions
from .part_types import FilePart, PartMetadata
from .readers import FileRangeReader
from .senders import RetryingPartSender
from .sources import FileRangePartsSource, StreamPartsSource, open_parts_source

__all__ = [
    "FilePart",
    "FileRangePartsSource",
    "FileRangeReader",
    "PartMetadata",
    "PartsCollector",
    "PartsUploadOptions",
    "RetryingPartSender",
    "StreamPartsSource",
    "open_parts_source",
]
