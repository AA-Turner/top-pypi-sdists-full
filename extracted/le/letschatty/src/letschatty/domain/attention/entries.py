"""Entries («¿Por dónde entró?», `entradas`): the port every entry store implements.

An entry is its own aggregate. It does NOT hold its sources: which sources are in it lives in `Source.entrada_id`
(the source's aggregate), so the use cases compute `source_ids` on each read. The entity is
`letschatty.models.company.assets.atencion.Entrada`, unchanged. A read by id is NOT scoped to a company: the use case
checks the company (ADR-007 of api-chatty). A deleted entry is still returned by id.
"""
from __future__ import annotations

from typing import Any, List, Optional, Protocol, Tuple

from ...models.company.assets.atencion import Entrada
from ...models.utils.types import StrObjectId


class EntryRepository(Protocol):
    """Raises `NotFoundError` when no entry has that id."""

    async def get(self, entry_id: StrObjectId) -> Entrada:
        """By id, through the cache."""
        ...

    async def get_fresh(self, entry_id: StrObjectId) -> Entrada:
        """By id from the store now (whoever reads it is about to write), leaving it in the cache."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[Entrada]:
        """The company's entries without `deleted_at`, whole, in the store's order."""
        ...

    async def add(self, entrada: Entrada) -> Entrada: ...

    async def update(self, entry_id: StrObjectId, changes: Entrada) -> Entrada:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def stored_updated_at(self, entry_id: StrObjectId) -> Tuple[bool, Any]:
        """Whether it is stored, and its `updated_at` exactly as stored (raw: compare-and-set compares that value)."""
        ...

    async def update_if_unchanged(self, current: Entrada, changes: Entrada, stored_updated_at: Any) -> Optional[Entrada]:
        """Writes only the fields `changes` was built with, merged onto `current`, with a new `updated_at`, and only
        if the stored `updated_at` is still `stored_updated_at`. None when another write got there first."""
        ...

    async def delete(self, entry_id: StrObjectId) -> Entrada:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...
