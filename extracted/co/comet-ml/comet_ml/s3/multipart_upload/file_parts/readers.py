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
from typing import Callable, Optional


class FileRangeReader(object):
    """One part's byte range of a file, as a body that never holds the part in memory.

    This is what makes a large part size survivable. A part sent as ``bytes`` is
    fully resident, so a 5 GiB part, which S3 permits and this SDK's clamp allows,
    would be a 5 GiB allocation per part in flight. Read as a range instead, the
    resident cost is whatever the HTTP layer buffers, tens of kilobytes, no matter
    how large the part is.

    Three details make it usable as a requests body:

    * ``__len__`` is what makes requests set Content-Length. Without it, a
      file-like body falls back to chunked transfer encoding, which S3 rejects on
      a presigned PUT.
    * ``read`` never returns bytes beyond this part's range, so one handle per part
      cannot bleed into the next part.
    * ``rewind`` puts the cursor back so a retried attempt resends identical bytes.
      A body that has already been partially consumed cannot simply be re-sent,
      and the retry strategy calls this before every attempt after the first.

    Each reader owns its own file handle, so several can be read concurrently
    without seeking a shared one. That also means they must be closed, which the
    sender does once the part has been sent.
    """

    __slots__ = [
        "_path",
        "_offset",
        "_length",
        "_remaining",
        "_handle",
        "_on_progress",
    ]

    # The HTTP layer pulls a file-like body in small blocks, so the default 8 KiB
    # file buffer turns one part into thousands of syscalls. A megabyte of read
    # buffering costs a megabyte per part in flight and keeps the sender fed.
    READ_BUFFER_BYTES = 1024 * 1024

    def __init__(
        self,
        path: str,
        offset: int,
        length: int,
        on_progress: Optional[Callable[[int], None]] = None,
    ):
        self._path = path
        self._offset = offset
        self._length = length
        self._remaining = length
        # Called with the number of this part's bytes handed to the HTTP layer so
        # far. Without it a part reports nothing until it completes, and with several
        # large parts in flight that is a long silence: 20 parts of 16 MiB on a
        # 6 MB/s link means no progress at all for the first 45 seconds.
        self._on_progress = on_progress
        self._handle = open(path, "rb", buffering=self.READ_BUFFER_BYTES)
        self._handle.seek(offset)

    def __len__(self) -> int:
        return self._length

    def rewind(self) -> None:
        """Restarts the range, so the next read resends the same bytes."""
        self._handle.seek(self._offset)
        self._remaining = self._length
        # A retry resends from the start, so the bytes reported for this part have to
        # go back with it. Progress can therefore dip on a retry, which is honest.
        self._report()

    def read(self, amount: int = -1) -> bytes:
        if self._remaining <= 0:
            return b""

        if amount is None or amount < 0:
            amount = self._remaining

        chunk = self._handle.read(min(amount, self._remaining))
        self._remaining -= len(chunk)
        self._report()

        return chunk

    def _report(self) -> None:
        if self._on_progress is not None:
            self._on_progress(self._length - self._remaining)

    def close(self) -> None:
        self._handle.close()

    def __enter__(self) -> "FileRangeReader":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
