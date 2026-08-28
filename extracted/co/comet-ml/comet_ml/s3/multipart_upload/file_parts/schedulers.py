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
import abc
import logging
import threading
from concurrent import futures as concurrent_futures
from typing import List, Optional, Tuple

from .... import thread_pool
from .. import upload_error
from . import budgets, collectors, part_options, part_types, pools, senders, sources

LOGGER = logging.getLogger(__name__)


class PartsUploadScheduler(abc.ABC):
    """Decides when the parts produced by a source are handed to a sender.

    The one abstraction here with two real implementations: which of them runs is
    chosen at upload time by create_parts_upload_scheduler().
    """

    @abc.abstractmethod
    def upload(
        self,
        source: sources.PartsSourceType,
        sender: senders.RetryingPartSender,
        collector: collectors.PartsCollector,
    ) -> None:
        """Uploads every part of the source, or raises the first failure seen.

        Returns only once no part upload is still running, so that the caller can
        complete or abort the multipart upload without leaving work behind.
        """


class SerialPartsUploadScheduler(PartsUploadScheduler):
    """Sends one part at a time on the calling thread.

    This is the behaviour the SDK had before per-part parallelism, and it stays
    the default whenever no parts pool has been provided.
    """

    def upload(self, source, sender, collector) -> None:
        for part in source.parts():
            collector.on_part_complete(sender.send(part))


class ParallelPartsUploadScheduler(PartsUploadScheduler):
    """Sends the parts of one asset concurrently through a shared, bounded pool.

    The calling thread stays the only reader. For each part it first reserves
    capacity and only then reads the bytes, so the amount of part data resident at
    any moment is bounded by the reservations, not by how fast this loop can read.

    Capacity comes from two budgets in one all-or-nothing reservation, because they
    answer different questions. The per-asset budget caps how much of the pool a
    single upload may take. The pool budget caps what all uploads together may
    take, which is what keeps N concurrent assets from multiplying resident part
    data by N.

    Acquisition order is per-asset first, then the pool, and it cannot deadlock:
    the per-asset budget is private to this upload, so no other thread ever waits
    on it.
    """

    def __init__(self, pool: pools.PartsUploadPool, asset_budget: budgets.PartsBudget):
        self._pool = pool
        self._asset_budget = asset_budget

    def upload(self, source, sender, collector) -> None:
        failure = _FirstFailure()
        submitted: List[Tuple[thread_pool.Future, part_types.FilePart]] = []
        reservable = (self._asset_budget, self._pool.budget)
        parts = source.parts()

        try:
            while failure.empty():
                # Taken before the bytes are read, so what is resident is bounded
                # by the budgets rather than by how fast this loop can read.
                reservation = budgets.reserve(reservable)

                try:
                    part = next(parts)
                except StopIteration:
                    reservation.release()
                    break
                except BaseException:
                    reservation.release()
                    raise

                try:
                    future = self._pool.submit(
                        self._send_part, part, sender, collector, failure, reservation
                    )
                except BaseException:
                    reservation.release()
                    # The sender closes a part once it owns it. Nothing owns this one,
                    # so its file handle would stay open until the process exited.
                    part.close()
                    raise

                # Belt and braces, and neither can double-release because
                # Reservation.release() is idempotent. The task covers the call
                # running or raising; the callback also covers it being cancelled
                # without ever running, which the task cannot.
                future.add_done_callback(reservation.release_on_done)
                # Paired with its part, because a future that is cancelled never runs
                # and so never hands its part to the sender.
                submitted.append((future, part))
        finally:
            _wait_for_all(submitted, failure)

        failure.reraise()

    def _send_part(
        self,
        part: part_types.FilePart,
        sender: senders.RetryingPartSender,
        collector: collectors.PartsCollector,
        failure: "_FirstFailure",
        reservation: budgets.Reservation,
    ) -> None:
        try:
            # Once one part has failed the whole upload is going to be aborted, so
            # there is nothing to gain from sending the parts already queued.
            if failure.empty():
                collector.on_part_complete(sender.send(part))
        except Exception as exception:
            failure.record(exception)
        finally:
            reservation.release()


class _FirstFailure(object):
    """Keeps the first exception raised by any part, which is the one worth reporting."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._exception: Optional[BaseException] = None

    def record(self, exception: BaseException) -> None:
        with self._lock:
            if self._exception is None:
                self._exception = exception

    def empty(self) -> bool:
        with self._lock:
            return self._exception is None

    def reraise(self) -> None:
        with self._lock:
            exception = self._exception

        if exception is not None:
            raise exception


def _wait_for_all(
    submitted: List[Tuple[thread_pool.Future, part_types.FilePart]],
    failure: "_FirstFailure",
) -> None:
    for future, part in submitted:
        try:
            future.result()
        except concurrent_futures.CancelledError:
            # A cancelled task never ran, so it never sent its part and never
            # recorded a failure of its own. That has to be recorded here, because
            # otherwise this upload returns as though it had succeeded and the
            # caller completes the multipart upload with a partial list of parts:
            # S3 assembles what it was given and the asset is stored truncated,
            # reported as a success. Measured on twenty parts, thirteen landed.
            #
            # The part is closed here for the same reason - nothing else owns it.
            part.close()
            failure.record(
                upload_error.S3UploadError(
                    reason="S3 file part #%d upload was cancelled before it ran"
                    % part.part_number
                )
            )
        except Exception:
            # Part failures are recorded by the task itself; this only guards
            # against the pool reporting a task that never got to run.
            LOGGER.debug("S3 file part upload task ended with an error", exc_info=True)


def create_parts_upload_scheduler(
    pool: Optional[pools.PartsUploadPool], options: part_options.PartsUploadOptions
) -> PartsUploadScheduler:
    """Returns the parallel scheduler when a pool is available, the serial one otherwise.

    The per-asset budget is created here, once per upload, so each asset gets its
    own allowance of the shared pool.
    """
    if pool is None:
        return SerialPartsUploadScheduler()

    return ParallelPartsUploadScheduler(
        pool=pool, asset_budget=budgets.PartsBudget(max_parts=options.concurrency)
    )
