# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Injectable writer for the per-fragment data-file write.

``write_fragment_file`` (in :mod:`geneva.runners.ray.writer`) serializes a fragment's
rows into a lance data file inside the writer actor. Routing it through a
``FragmentFileWriter`` lets a test fault it (a short write, or an error the driver turns
into a dropped fragment); production calls the real function. The call site passes
``write_fragment_file`` in as the first argument to avoid a circular import.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


class FragmentFileWriter(Protocol):
    """Writes one fragment's data file. ``fn`` is the real ``write_fragment_file``;
    the rest are its args, forwarded verbatim."""

    def write(self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any: ...


class RealFragmentFileWriter:
    """Production writer: call the real ``write_fragment_file`` unchanged."""

    def write(self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)


# Process-global fragment-file writer. Default is the real one; tests swap it.
_WRITER: FragmentFileWriter = RealFragmentFileWriter()


def get_fragment_file_writer() -> FragmentFileWriter:
    """The writer every fragment-data-file write goes through."""
    return _WRITER


def set_fragment_file_writer(writer: FragmentFileWriter) -> None:
    """Install ``writer`` process-wide (test-only)."""
    global _WRITER
    _WRITER = writer


@contextlib.contextmanager
def using_fragment_file_writer(
    writer: FragmentFileWriter,
) -> Iterator[FragmentFileWriter]:
    """Install ``writer`` for the duration of the block, restoring the prior one."""
    prev = _WRITER
    set_fragment_file_writer(writer)
    try:
        yield writer
    finally:
        set_fragment_file_writer(prev)
