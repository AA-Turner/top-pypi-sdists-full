# File: matrx_files/blocks/testing.py
"""An in-memory `platform.acquisition_block` for this package's tests.

Mirrors `matrx_scraper.blocks.testing.FakeBlockStore` — enforces the same
`acquisition_block_dedupe_uniq` shape so a dedupe bug in `record.py` fails a
test the same way it would fail against the real database. A second, drifted
copy of this fake would be the risk `matrx_scraper`'s own module docstring
warns about, so keep the two in sync by hand if either one's contract moves.
"""

from __future__ import annotations

import uuid
from typing import Any

__all__ = ["FakeBlockStore", "FakeRow"]


class FakeRow:
    def __init__(self, **fields: Any) -> None:
        self.__dict__.update(fields)


class FakeBlockStore:
    def __init__(self) -> None:
        self.rows: dict[str, FakeRow] = {}
        self.raise_conflict_once = False

    def _key(self, row: Any) -> tuple[str, str, str, str]:
        return (
            str(getattr(row, "organization_id", "")),
            str(getattr(row, "source_type", "")),
            str(getattr(row, "error_class", "")),
            str(getattr(row, "input_ref", "")),
        )

    async def find_open(
        self,
        *,
        organization_id: str,
        input_ref: str,
        source_type: str,
        error_class: str,
    ) -> Any | None:
        wanted = (organization_id, source_type, error_class, input_ref)
        for row in self.rows.values():
            if self._key(row) == wanted and getattr(row, "deleted_at", None) is None:
                return row
        return None

    async def create(self, **fields: Any) -> Any:
        row = FakeRow(id=str(uuid.uuid4()), deleted_at=None, **fields)
        if self.raise_conflict_once:
            self.raise_conflict_once = False
            raise RuntimeError(
                'duplicate key value violates unique constraint "acquisition_block_dedupe_uniq"'
            )
        for existing in self.rows.values():
            if self._key(existing) == self._key(row):
                raise RuntimeError(
                    "duplicate key value violates unique constraint "
                    '"acquisition_block_dedupe_uniq"'
                )
        self.rows[row.id] = row
        return row

    async def update(self, block_id: str, **fields: Any) -> Any:
        row = self.rows[block_id]
        row.__dict__.update(fields)
        return row

    async def hard_delete(self, block_id: str) -> int:
        return 1 if self.rows.pop(block_id, None) is not None else 0
