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
from typing import Any, Dict, Optional

from ..multipart_transfer import CancellationToken
from . import parts


class DownloadPartsCollector:
    """Accounts for what has been written, from every worker writing one asset.

    Two counts, kept apart for the same reason as on the upload side. Bytes
    received move with every chunk and feed the progress display. Completed
    parts only move when a range has been written in full, and are what decides
    whether the file is whole.

    The monitor is called under the lock. FileDownloadSizeMonitor adds to a plain
    attribute, which is not atomic across threads, so concurrent chunks reported
    without the lock lose updates and the progress display under-counts.

    Every chunk written by any range is reported here, which makes it where a
    cancel token is checked: the writer gets TransferCancelled right after the
    chunk is counted, and stops.
    """

    def __init__(
        self,
        monitor: Optional[Any] = None,
        cancel_token: Optional[CancellationToken] = None,
    ):
        self._lock = threading.Lock()
        self._bytes_received = 0
        self._parts: Dict[int, int] = {}
        self._monitor = monitor
        self._cancel_token = cancel_token

    @property
    def bytes_received(self) -> int:
        with self._lock:
            return self._bytes_received

    @property
    def completed_bytes(self) -> int:
        with self._lock:
            return sum(self._parts.values())

    def completed_parts_number(self) -> int:
        with self._lock:
            return len(self._parts)

    def on_bytes_received(self, count: int) -> None:
        with self._lock:
            self._bytes_received += count
            if self._monitor is not None:
                self._monitor.monitor_callback(count)

        if self._cancel_token is not None:
            self._cancel_token.raise_if_cancelled()

    def on_part_complete(self, part: parts.ReceivedPart) -> None:
        with self._lock:
            self._parts[part.part_number] = part.size
