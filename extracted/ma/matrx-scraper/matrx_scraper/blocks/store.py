"""The reader/writer seam of the Block Ledger, and the package's own implementation of it.

Nothing here decides anything — dedupe, vocabulary and the lawful route live in `record.py`,
so they can be exercised without a database and so the database access has exactly one shape
to get right.

Two implementations exist, deliberately, because there are two hosts and they register the
table differently: aidream writes through its generated manager
(`aidream/services/block_ledger/store.py`), and any standalone entrypoint of THIS package
writes through :class:`OrmBlockStore` below. Both satisfy :class:`BlockStore`, both talk to
the same row in the same ONE database, and neither carries a decision the other could
disagree with.

No raw SQL: the model is the only writer.
"""

from __future__ import annotations

from typing import Any, Protocol

__all__ = ["BlockStore", "OrmBlockStore"]


class BlockStore(Protocol):
    async def get_many(self, *, organization_id: str, block_ids: list[str]) -> list[Any]: ...

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
        from matrx_scraper.blocks.model import AcquisitionBlock

        return AcquisitionBlock

    async def get_many(self, *, organization_id: str, block_ids: list[str]) -> list[Any]:
        if not block_ids:
            return []
        return await self._model().filter_items(
            organization_id=organization_id,
            id__in=list(block_ids),
            deleted_at__isnull=True,
        )

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
        """Remove a row outright. ONLY the boot self-test's own probe row uses this.

        A real block is never deleted — it is resolved, dropped or soft-deleted by a person on
        the ledger screen. The probe row is ours, it is not a finding, and leaving one behind
        on every container start would put litter in front of the operator who reads this
        table to decide what to go and get.
        """
        return await self._model().delete_where(id=block_id)
