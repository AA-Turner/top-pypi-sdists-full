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

    part_types   FilePart, PartMetadata, the values that move between threads
    readers      one part's byte range of a file, as a non-resident body
    sources      reads an asset into parts, streaming from disk where possible
    senders      sends one part, with the existing retry strategy
    collectors   accumulates completed parts, thread safely, in S3's order
    budgets      bounds how much part data may be resident, and hands it back safely
    pools        workers plus the budget shared by every asset
    schedulers   serial or parallel, the one genuine choice made at upload time

Only the scheduler is abstract, because only it has two implementations selected
at runtime. Everything else has exactly one, and the seams that tests substitute
are plain duck typing.

The names below are the package's public surface; inside the package the modules
import each other as modules.
"""
from .budgets import PartsBudget, Reservation, reserve
from .collectors import PartsCollector
from .part_options import PartsUploadOptions
from .part_types import FilePart, PartMetadata
from .pools import PartsUploadPool, create_parts_upload_pool
from .readers import FileRangeReader
from .schedulers import (
    ParallelPartsUploadScheduler,
    PartsUploadScheduler,
    SerialPartsUploadScheduler,
    create_parts_upload_scheduler,
)
from .senders import RetryingPartSender
from .sources import FileRangePartsSource, StreamPartsSource, open_parts_source
from .throttling import ThrottleGate, default_gate

__all__ = [
    "FilePart",
    "ParallelPartsUploadScheduler",
    "PartMetadata",
    "PartsBudget",
    "PartsCollector",
    "FileRangePartsSource",
    "FileRangeReader",
    "PartsUploadOptions",
    "PartsUploadPool",
    "PartsUploadScheduler",
    "Reservation",
    "RetryingPartSender",
    "SerialPartsUploadScheduler",
    "StreamPartsSource",
    "ThrottleGate",
    "default_gate",
    "create_parts_upload_pool",
    "create_parts_upload_scheduler",
    "open_parts_source",
    "reserve",
]
