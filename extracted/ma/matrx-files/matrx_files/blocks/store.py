# File: matrx_files/blocks/store.py
"""The reader/writer seam of this package's half of the Block Ledger.

Nothing here decides anything — dedupe and the lawful route live in
`record.py`, so they can be exercised without a database. Same shape as
`matrx_scraper.blocks.store.BlockStore` (duck-typed, not imported — a
package cannot depend on matrx-scraper) and `aidream/services/block_ledger/store.py`;
all three satisfy the same protocol and write the same row in the same ONE
database.

No raw SQL: the model is the only writer.
"""

from __future__ import annotations

from typing import Any, Protocol

__all__ = ["BlockStore", "OrmBlockStore"]


class BlockStore(Protocol):
    async def find_open(
        self,
        *,
        organization_id: str,
        input_ref: str,
        source_type: str,
        error_class: str,
    ) -> Any | None: ...

    async def create(self, **fields: Any) -> Any: ...

    async def update(self, block_id: str, **fields: Any) -> Any: ...


class OrmBlockStore:
    """`platform.acquisition_block` through this package's own model, and nothing else."""

    @staticmethod
    def _model() -> Any:
        """Imported on first use so importing this module never needs a bound database."""
        from matrx_files.blocks.model import AcquisitionBlock

        return AcquisitionBlock

    async def find_open(
        self,
        *,
        organization_id: str,
        input_ref: str,
        source_type: str,
        error_class: str,
    ) -> Any | None:
        rows = await self._model().filter_items(
            organization_id=organization_id,
            input_ref=input_ref,
            source_type=source_type,
            error_class=error_class,
            deleted_at__isnull=True,
        )
        return rows[0] if rows else None

    async def create(self, **fields: Any) -> Any:
        return await self._model().create_item(**fields)

    async def update(self, block_id: str, **fields: Any) -> Any:
        return await self._model().update_item(block_id, **fields)

    async def hard_delete(self, block_id: str) -> int:
        """Remove a row outright. ONLY the boot self-test's own probe row uses this."""
        return await self._model().delete_where(id=block_id)
