# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Injectable writer for lancedb-native table writes.

``Table.add`` / ``Table.update`` / ``Table.delete`` delegate to the underlying lancedb
table (``self._ltbl``) and commit through lancedb's own binding, not through
``lance.LanceDataset.commit`` (the committer). The MV refresh lands its new rows here,
so faulting the committer alone cannot reach them.

Routing the three ``self._ltbl.{add,update,delete}`` calls through a ``TableWriter``
lets a test fault them. Production uses ``LanceTableWriter``, a pass-through to the
lancedb table.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Iterator


class TableWriter(Protocol):
    """The lancedb-native table mutations geneva issues; each takes ``ltbl`` first and
    forwards the rest verbatim."""

    def add(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any: ...
    def update(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any: ...
    def delete(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any: ...


class LanceTableWriter:
    """Production table writer: a verbatim pass-through to the lancedb table."""

    def add(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        return ltbl.add(*args, **kwargs)

    def update(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        return ltbl.update(*args, **kwargs)

    def delete(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        return ltbl.delete(*args, **kwargs)


# Process-global table writer. Default is the real one; tests swap it.
_WRITER: TableWriter = LanceTableWriter()


def get_table_writer() -> TableWriter:
    """The table writer every lancedb-native mutation goes through."""
    return _WRITER


def set_table_writer(writer: TableWriter) -> None:
    """Install ``writer`` process-wide (test-only)."""
    global _WRITER
    _WRITER = writer


@contextlib.contextmanager
def using_table_writer(writer: TableWriter) -> Iterator[TableWriter]:
    """Install ``writer`` for the duration of the block, restoring the prior one."""
    prev = _WRITER
    set_table_writer(writer)
    try:
        yield writer
    finally:
        set_table_writer(prev)
