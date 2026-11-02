"""Reminder categories of a company («categorías de recordatorios»): the port and the rules about a name.

The entity is `letschatty.models.company.assets.recordatorio_categoria.RecordatorioCategoria`, unchanged. A category
is deleted logically: it stops being offered, but the reminders that have it keep showing it.
"""
from __future__ import annotations

import re
from typing import List, Protocol

from ...models.company.assets.recordatorio_categoria import RecordatorioCategoria
from ...models.utils.types import StrObjectId

_SPACES = re.compile(r"\s+")


def normalize_name(name: str) -> str:
    """Trimmed, inner spaces collapsed: "  Cobranza   urgente " -> "Cobranza urgente"."""
    return _SPACES.sub(" ", (name or "").strip())


def same_name(a: str, b: str) -> bool:
    """Two names are the same category when they only differ in case."""
    return a.casefold() == b.casefold()


class ReminderCategoryRepository(Protocol):
    async def get(self, category_id: StrObjectId) -> RecordatorioCategoria:
        """Of any company, also a deleted one. Raises `NotFoundError` (and `InvalidId` for a malformed id)."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[RecordatorioCategoria]: ...

    async def list_deleted(self, company_id: StrObjectId) -> List[RecordatorioCategoria]: ...

    async def add(self, category: RecordatorioCategoria) -> RecordatorioCategoria: ...

    async def rename(self, category: RecordatorioCategoria, name: str) -> None:
        """Writes only `name` (and `updated_at`)."""
        ...

    async def delete(self, category: RecordatorioCategoria) -> None:
        """Marks it deleted; the document stays."""
        ...

    async def restore(self, category_id: StrObjectId) -> RecordatorioCategoria: ...
