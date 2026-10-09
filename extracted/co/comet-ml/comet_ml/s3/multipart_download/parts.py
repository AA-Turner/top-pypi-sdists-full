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
"""The values that move between threads during a ranged download.

Shaped to fit the upload side's schedulers, which are reused unchanged: they need a
part with ``part_number`` and ``close()``, a source with ``parts()``, a sender with
``send(part)`` and a collector with ``on_part_complete(result)``. Nothing in the
scheduling cares which way the bytes go.
"""
import threading
from typing import Iterator, Optional

import requests


class DownloadPart:
    """One byte range of the object, and where it goes in the file.

    The first part may arrive already open: the request that discovered the
    object's size was itself a ranged GET for this part, so its body is read rather
    than thrown away. Ownership of that response passes to whoever calls
    take_response(), and close() releases it if nobody did - which is what the
    scheduler relies on for a part that is cancelled before it runs.
    """

    __slots__ = ["part_number", "start", "length", "_response", "_lock"]

    def __init__(
        self,
        part_number: int,
        start: int,
        length: int,
        response: Optional[requests.Response] = None,
    ):
        self.part_number = part_number
        self.start = start
        self.length = length
        self._response = response
        self._lock = threading.Lock()

    @property
    def last(self) -> int:
        """The last byte of the range, inclusive, as a Range header wants it."""
        return self.start + self.length - 1

    def take_response(self) -> Optional[requests.Response]:
        with self._lock:
            response, self._response = self._response, None
        return response

    def close(self) -> None:
        response = self.take_response()
        if response is not None:
            response.close()

    def __repr__(self) -> str:
        return "DownloadPart(part_number=%d, start=%d, length=%d)" % (
            self.part_number,
            self.start,
            self.length,
        )


class ReceivedPart:
    """A range that has been written to the file in full."""

    __slots__ = ["part_number", "size"]

    def __init__(self, part_number: int, size: int):
        self.part_number = part_number
        self.size = size

    def __repr__(self) -> str:
        return "ReceivedPart(part_number=%d, size=%d)" % (self.part_number, self.size)


class RangePartsSource:
    """Divides an object of known size into consecutive ranges of at most part_size."""

    def __init__(
        self,
        total_size: int,
        part_size: int,
        first_response: Optional[requests.Response] = None,
    ):
        self.total_size = total_size
        self.part_size = part_size
        self._first_response = first_response

    @property
    def parts_number(self) -> int:
        return -(-self.total_size // self.part_size)

    def parts(self) -> Iterator[DownloadPart]:
        start = 0
        part_number = 1
        while start < self.total_size:
            length = min(self.part_size, self.total_size - start)
            response = self._first_response if part_number == 1 else None
            yield DownloadPart(
                part_number=part_number, start=start, length=length, response=response
            )
            start += length
            part_number += 1
