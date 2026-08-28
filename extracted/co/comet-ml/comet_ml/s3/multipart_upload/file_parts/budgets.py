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
import threading
from typing import Sequence

LOGGER = logging.getLogger(__name__)


class PartsBudget(object):
    """Allows a fixed number of parts to be resident in memory at once.

    This is not redundant with the size of the parts pool. A pool's worker count
    bounds how many parts are being *sent*; it does nothing about how many are
    waiting to be sent, because a ThreadPoolExecutor's work queue is unbounded and
    every queued task holds its bytes. Measured on a 200 MiB asset with 4 workers:
    with no budget the producer materialised all 40 parts and peak memory grew by
    201 MiB, the whole asset; with a 4 part budget it materialised 4 and grew by
    20 MiB.

    Peak resident part data is therefore ``max_parts * part_size``, which is the
    figure to size against.

    The semaphore is bounded rather than plain: releasing more than was acquired
    would silently raise the ceiling and undo the memory bound, so it is made a
    loud error at the point of the fault instead.
    """

    def __init__(self, max_parts: int):
        if max_parts < 1:
            raise ValueError("max_parts must be at least 1, got %d" % max_parts)

        self.max_parts = max_parts
        self._semaphore = threading.BoundedSemaphore(max_parts)

    @property
    def available(self) -> int:
        """Reservations currently free. For assertions and debugging, not control flow."""
        acquired = 0
        while self._semaphore.acquire(blocking=False):
            acquired += 1
        for _ in range(acquired):
            self._semaphore.release()
        return acquired

    def acquire(self) -> None:
        self._semaphore.acquire()

    def release(self) -> None:
        self._semaphore.release()


class Reservation(object):
    """Capacity held in one or more budgets, given back exactly once.

    Ownership of a reservation moves between threads: the producer takes it, and
    a pool worker gives it back once the part has been sent. That handover is
    where capacity gets stranded, and a stranded reservation is not a slow path
    but a permanent one, because acquire() has no timeout and nothing sweeps up
    afterwards.

    So release() is idempotent and thread safe rather than something callers have
    to invoke exactly once. Every plausible owner can call it unconditionally, the
    first call gives the capacity back and the rest do nothing. The scheduler
    relies on that: a submitted part is released both by the task that sends it
    and by the future's completion callback, which between them cover the task
    running, raising, and being cancelled without ever running.
    """

    __slots__ = ["_budgets", "_lock", "_released"]

    def __init__(self, budgets: Sequence[PartsBudget]):
        self._budgets = tuple(budgets)
        self._lock = threading.Lock()
        self._released = False

    @property
    def released(self) -> bool:
        with self._lock:
            return self._released

    def release(self) -> None:
        """Gives the capacity back. Safe to call any number of times, from any thread."""
        with self._lock:
            if self._released:
                return
            self._released = True

        # Released in reverse order, and every budget is attempted even if an
        # earlier one fails: a failure here would otherwise strand the rest.
        for budget in reversed(self._budgets):
            try:
                budget.release()
            except Exception:
                LOGGER.debug("Failed to give back in-flight capacity", exc_info=True)

    def release_on_done(self, _future: object = None) -> None:
        """Signature for Future.add_done_callback."""
        self.release()


def reserve(budgets: Sequence[PartsBudget]) -> Reservation:
    """Takes capacity from every budget, or from none of them.

    Acquiring several budgets is the other place capacity can be stranded: if the
    second acquire fails, or is interrupted, the first is already held. Anything
    taken before the failure is given straight back.
    """
    acquired = []
    try:
        for budget in budgets:
            budget.acquire()
            acquired.append(budget)
    except BaseException:
        for budget in reversed(acquired):
            try:
                budget.release()
            except Exception:
                LOGGER.debug("Failed to roll back a partial reservation", exc_info=True)
        raise

    return Reservation(budgets=acquired)
