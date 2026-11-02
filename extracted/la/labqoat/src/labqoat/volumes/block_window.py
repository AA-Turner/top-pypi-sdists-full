"""A bounded view of an open file, so a request body is exactly one block."""

from __future__ import annotations

from typing import BinaryIO


class BlockWindow:
    """Read at most ``length`` bytes from a file positioned at a block's start."""

    def __init__(self, file: BinaryIO, length: int) -> None:
        """Bound reads of an open file."""
        self._file = file
        self._left = length

    def read(self, size: int = -1) -> bytes:
        """Return the next bytes of the window, never past its end."""
        wanted = self._left if size < 0 else min(size, self._left)
        data = self._file.read(wanted)
        self._left -= len(data)
        return data
