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
"""Moving the parts of a single S3 object concurrently, in either direction.

    budgets           bounds how many parts may be in flight, and hands capacity back safely
    cancellation      stops a transfer from another thread, and keeps its result unpublished
    pools             workers plus the budget shared by every asset
    schedulers        serial or parallel, and the contract of what they schedule
    throttling        the brake that holds every part while S3 is rate limiting
    retry_policy      which statuses are retried, and for how long
    transfer_options  the per-asset cap and process-wide ceiling on concurrency
    errors            the failure both directions raise

Nothing here knows which way the bytes go. multipart_upload supplies parts that
are sent and multipart_download parts that are fetched; both are scheduled,
bounded and throttled by what is in this package.

Only the scheduler is abstract, because only it has two implementations selected
at runtime. What it schedules is described by Protocols in schedulers, which is
all either direction has to satisfy.
"""
from .budgets import PartsBudget, Reservation, reserve
from .cancellation import CancellationToken, TransferCancelled
from .errors import S3PartsTransferError
from .pools import PartsTransferPool, create_parts_transfer_pool
from .schedulers import (
    ParallelPartsTransferScheduler,
    PartsTransferScheduler,
    PartTransferrer,
    SerialPartsTransferScheduler,
    create_parts_transfer_scheduler,
)
from .throttling import ThrottleGate, default_gate
from .transfer_options import PartsTransferOptions, TransferLimits

__all__ = [
    "CancellationToken",
    "ParallelPartsTransferScheduler",
    "PartTransferrer",
    "PartsBudget",
    "PartsTransferOptions",
    "PartsTransferPool",
    "PartsTransferScheduler",
    "Reservation",
    "S3PartsTransferError",
    "SerialPartsTransferScheduler",
    "ThrottleGate",
    "TransferCancelled",
    "TransferLimits",
    "create_parts_transfer_pool",
    "create_parts_transfer_scheduler",
    "default_gate",
    "reserve",
]
