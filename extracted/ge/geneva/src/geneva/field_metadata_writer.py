# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Injectable writer for per-field (column) metadata writes.

The MV refresh writes its ``last_refreshed`` watermark into the ``__source_row_id``
column's field metadata via lancedb's ``update_field_metadata`` (see
``_set_last_refreshed_version`` in :mod:`geneva.table`). This write goes through neither
the committer nor the table writer, so routing it through a ``FieldMetadataWriter`` lets
a test fault it independently, e.g. advance the watermark while the data commit is
dropped. Production uses ``LanceFieldMetadataWriter``, a pass-through to the lancedb
table.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Iterator


class FieldMetadataWriter(Protocol):
    """Updates field metadata on ``ltbl``, forwarding ``*updates`` verbatim."""

    def update(self, ltbl: Any, *updates: Any) -> Any: ...


class LanceFieldMetadataWriter:
    """Production writer: a verbatim pass-through to the lancedb table."""

    def update(self, ltbl: Any, *updates: Any) -> Any:
        return ltbl.update_field_metadata(*updates)


# Process-global field-metadata writer. Default is the real one; tests swap it.
_WRITER: FieldMetadataWriter = LanceFieldMetadataWriter()


def get_field_metadata_writer() -> FieldMetadataWriter:
    """The writer every field-metadata (watermark) mutation goes through."""
    return _WRITER


def set_field_metadata_writer(writer: FieldMetadataWriter) -> None:
    """Install ``writer`` process-wide (test-only)."""
    global _WRITER
    _WRITER = writer


@contextlib.contextmanager
def using_field_metadata_writer(
    writer: FieldMetadataWriter,
) -> Iterator[FieldMetadataWriter]:
    """Install ``writer`` for the duration of the block, restoring the prior one."""
    prev = _WRITER
    set_field_metadata_writer(writer)
    try:
        yield writer
    finally:
        set_field_metadata_writer(prev)
