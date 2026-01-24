"""Internal library bug definition."""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    NoReturn,
)


@dataclass
class LibraryBug(Exception):
    """If raised then there is a bug in the `fa_purity` library."""

    @dataclass(frozen=True)
    class _Private:
        pass

    _private: LibraryBug._Private = field(repr=False, hash=False, compare=False)
    traceback: Exception

    @staticmethod
    def new(exception: Exception) -> NoReturn:
        """Raise a new `LibraryBug` error."""
        raise LibraryBug(LibraryBug._Private(), exception)
