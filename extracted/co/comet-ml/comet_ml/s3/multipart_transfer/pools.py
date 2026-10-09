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
from typing import Any, Callable

from ... import thread_pool
from . import budgets, transfer_options

LOGGER = logging.getLogger(__name__)


class PartsTransferPool:
    """Workers plus a budget, shared by every asset of one upload or download manager.

    Sharing matters: a pool per asset would multiply both worker threads and
    resident part data by the number of assets transferring at the same time.
    Here both stay fixed no matter how many transfers are in flight.

    This must never be the same executor that runs the asset level tasks.
    Those tasks block waiting for their parts, so sharing one bounded executor
    between the two levels deadlocks as soon as every worker holds an asset task.

    The budget is exposed rather than wrapped so that a caller can reserve it
    together with its own per-asset budget in one all-or-nothing step.
    """

    def __init__(
        self, executor: thread_pool.ThreadPoolExecutor, budget: budgets.PartsBudget
    ):
        self._executor = executor
        self.budget = budget

    def submit(
        self, fn: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> thread_pool.Future:
        return self._executor.submit(fn, *args, **kwargs)

    def close(self) -> None:
        self._executor.close()

    def join(self) -> None:
        self._executor.join()


def create_parts_transfer_pool(
    options: transfer_options.PartsTransferOptions, asset_pool_size: int
) -> PartsTransferPool:
    """Builds the shared parts pool described by the given options.

    Sized by the *total* concurrency rather than the per-asset one. The per-asset
    limit is applied by each transfer's scheduler, so that one asset cannot take the
    whole pool while several assets together still can.
    """
    total = options.resolve_total_concurrency(asset_pool_size)

    LOGGER.debug(
        "Parts transfer pool created with %d workers and %d in-flight slots, "
        "at most %d of them used by a single asset",
        total,
        total,
        options.concurrency,
    )

    return PartsTransferPool(
        executor=thread_pool.ConcurrentThreadPoolExecutor(max_workers=total),
        budget=budgets.PartsBudget(max_parts=total),
    )
