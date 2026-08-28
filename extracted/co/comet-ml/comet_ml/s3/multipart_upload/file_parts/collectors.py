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
import threading
from typing import Any, Dict, List, Optional, Union

from . import part_types


class PartsCollector(object):
    """Accumulates completed parts for one asset.

    Parts may complete on any worker thread and in any order, so both the parts
    list and the running byte count are guarded by a single lock. Order is
    restored once, in completed_parts(): S3 requires the parts of a
    CompleteMultipartUpload request to be listed by ascending part number.
    """

    def __init__(self, monitor: Optional[Any] = None):
        self._lock = threading.Lock()
        self._parts: List[part_types.PartMetadata] = []
        self._bytes_read = 0
        # Bytes of parts still being sent, by part number. Kept apart from
        # _bytes_read because that one is authoritative: it is what the complete call
        # reports as the object's size, so it may only ever count parts S3 has
        # accepted. This is for the progress display, which wants to move while a
        # part is in flight rather than only when it lands.
        self._streaming: Dict[int, int] = {}
        self._monitor = monitor

    @property
    def bytes_read(self) -> int:
        """Bytes in parts S3 has accepted. What the complete call reports."""
        with self._lock:
            return self._bytes_read

    @property
    def progress_bytes(self) -> int:
        """Accepted bytes plus what is currently on the wire, for display only."""
        with self._lock:
            return self._bytes_read + sum(self._streaming.values())

    def on_part_progress(self, part_number: int, streamed: int) -> None:
        """Reports how much of one part has been handed to the HTTP layer so far.

        Absolute rather than a delta, so a retry that starts the part again simply
        reports zero and cannot leave a stale amount counted.
        """
        with self._lock:
            self._streaming[part_number] = streamed

        self._notify()

    def on_part_complete(self, part: part_types.PartMetadata) -> None:
        with self._lock:
            self._parts.append(part)
            self._bytes_read += part.size
            # Its streamed count is now covered by _bytes_read; leaving it would
            # count the part twice.
            self._streaming.pop(part.part_number, None)

        self._notify()

    def _notify(self) -> None:
        # Notified outside the lock: the value is read back through a property that
        # takes the same lock. What the monitor sees may already include a part that
        # finished on another thread, which is harmless for a progress display.
        # self._monitor is assigned once and never reassigned.
        monitor = self._monitor
        if monitor is not None:
            monitor.monitor_callback(_Progress(self.progress_bytes))

    def completed_parts(self) -> List[Dict[str, Union[str, int]]]:
        """Returns the completed parts in the ascending part-number order S3 requires."""
        with self._lock:
            ordered = sorted(self._parts, key=lambda part: part.part_number)

        return [
            {"ETag": part.e_tag, "PartNumber": part.part_number} for part in ordered
        ]

    def completed_parts_number(self) -> int:
        with self._lock:
            return len(self._parts)


class _Progress(object):
    """What UploadSizeMonitor.monitor_callback reads: an object with bytes_read.

    A separate carrier so that the collector can report accepted-plus-in-flight for
    display without letting that figure reach the complete call, which must report
    only what S3 has accepted.
    """

    __slots__ = ["bytes_read"]

    def __init__(self, bytes_read: int):
        self.bytes_read = bytes_read
