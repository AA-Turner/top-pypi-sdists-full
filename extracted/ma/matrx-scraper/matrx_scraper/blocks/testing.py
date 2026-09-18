"""An in-memory `platform.acquisition_block` that enforces the same unique index.

The database's own `acquisition_block_dedupe_uniq` is one row per (organization, source type,
error class, input). A fake that does not enforce it would let a dedupe bug pass, so this one
raises the same way and the guards drive the real service functions through it.

It ships with the package rather than with either suite because there are now two hosts with
two real stores (aidream's generated manager, and this package's model for the standalone
scraper service) and ONE contract between them. Two fakes would be two contracts, and the
second one would be the one nobody kept honest.
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
        #: Set to raise from `create` once, to exercise the race arm.
        self.raise_conflict_once = False

    def _key(self, row: Any) -> tuple[str, str, str, str]:
        return (
            str(getattr(row, "organization_id", "")),
            str(getattr(row, "source_type", "")),
            str(getattr(row, "error_class", "")),
            str(getattr(row, "input_ref", "")),
        )

    async def get_many(
        self, *, organization_id: str, block_ids: list[str]
    ) -> list[Any]:
        wanted = set(block_ids)
        return [
            row
            for row in self.rows.values()
            if str(getattr(row, "id", "")) in wanted
            and str(getattr(row, "organization_id", "")) == organization_id
            and getattr(row, "deleted_at", None) is None
        ]

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
