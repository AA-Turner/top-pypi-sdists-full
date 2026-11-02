"""Reasons («motivos de consulta», `motivos`): the port every reason store implements.

A reason is its own aggregate. Its mirror tag (`Motivo.tag_id`) belongs to the tag aggregate and is written by the tag
use cases, never by this port. The entity is `letschatty.models.company.assets.motivo.Motivo`, unchanged. A read by id
is NOT scoped to a company: the use case checks it where `main` did (ADR-007 of api-chatty; ENG-10 where it does not).
A deleted reason is still returned by id.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol

from ...models.company.assets.motivo import Motivo
from ...models.utils.types import StrObjectId


class ReasonRepository(Protocol):
    """Raises `NotFoundError` when no reason has that id."""

    async def get(self, reason_id: StrObjectId) -> Motivo:
        """By id, through the cache."""
        ...

    async def get_fresh(self, reason_id: StrObjectId) -> Motivo:
        """By id from the store now (whoever reads it is about to write), leaving it in the cache."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """The company's live reasons as JSON-ready preview dicts, through the cache."""
        ...

    async def list_fallbacks(self, company_id: StrObjectId) -> List[Motivo]:
        """The company's live «Consulta general» (`is_fallback`), read from the store now."""
        ...

    async def add(self, reason: Motivo) -> Motivo: ...

    async def update(self, reason_id: StrObjectId, changes: Motivo) -> Motivo:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def delete(self, reason_id: StrObjectId) -> Motivo:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...
