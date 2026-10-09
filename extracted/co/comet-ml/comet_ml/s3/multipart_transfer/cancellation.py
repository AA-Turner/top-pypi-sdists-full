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
import threading
from typing import Callable

from .errors import S3PartsTransferError


class TransferCancelled(S3PartsTransferError):
    """Raised inside a transfer whose CancellationToken was cancelled."""

    def __init__(self) -> None:
        super().__init__(reason="The transfer was cancelled")


class CancellationToken:
    """Lets one thread stop a transfer that others are running, and keeps its result unpublished.

    Cancellation is cooperative: the transfer checks the token between chunks,
    before each request, and while it sleeps or waits on the throttle gate, and
    unwinds through TransferCancelled from there, like from any other failure. A
    read already blocked on a stalled socket only returns at its own timeout.

    What is not left to cooperation is the result. publish() and cancel() take the
    same lock, so once cancel() has returned True, nothing is ever published, even
    by a worker that has not noticed the cancellation yet. That is what makes it
    safe for whoever gave up waiting to retry, or to use the destination for
    something else.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cancelled = threading.Event()
        self._published = False

    @property
    def cancelled(self) -> bool:
        return self._cancelled.is_set()

    def cancel(self) -> bool:
        """Cancels the transfer. False if it is too late: the result was published."""
        with self._lock:
            if self._published:
                return False

            self._cancelled.set()
            return True

    def raise_if_cancelled(self) -> None:
        if self._cancelled.is_set():
            raise TransferCancelled()

    def sleep(self, seconds: float) -> None:
        """Sleeps like time.sleep(), but raises TransferCancelled as soon as cancelled."""
        if self._cancelled.wait(timeout=seconds):
            raise TransferCancelled()

    def publish(self, publish_result: Callable[[], None]) -> None:
        """Calls publish_result unless cancelled, in which case raises TransferCancelled."""
        with self._lock:
            self.raise_if_cancelled()
            publish_result()
            self._published = True
