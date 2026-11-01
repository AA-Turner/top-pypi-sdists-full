"""browse mode=notes: one row of the tenant-wide notes catalog, its ref and identity."""

from __future__ import annotations
from typing import Any
from ....shared.reads.search_contract import (
    EntityType,
    NoteCatalogKind)


class NoteRowsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    @staticmethod
    def _note_row_ref(kind: Any, ident: Any) -> tuple[str, str] | None:
        """`(entity_type, address)` for a notes-catalog row, or None when it
        names no openable document. The catalog's kinds are `entity`'s kinds,
        spelled the same, except the two singletons-in-name below."""
        if kind == NoteCatalogKind.TEAM_NOTE:
            return EntityType.TEAM_NOTE.value, EntityType.TEAM_NOTE.value
        if not ident:
            return None
        if kind == NoteCatalogKind.SUB_NOTE:
            return EntityType.SUB_NOTE.value, f"{EntityType.SUB_NOTE.value}:{ident}"
        try:
            catalog = NoteCatalogKind(kind)
        except ValueError:
            return None
        return catalog.value, f"{catalog.value}:{ident}"

    @staticmethod
    def _note_identity(row: dict) -> str:
        """A catalog row's identity for resuming after it: `kind:id`, with the
        team note's absent id spelled empty (it is the one row with none)."""
        return f"{row.get('kind')}:{row.get('id') or ''}"

    def _note_row(self, row: dict) -> dict:
        resolved = self._note_row_ref(row.get("kind"), row.get("id"))
        out: dict = {}
        if resolved is not None:
            out["entity_type"], out["uuid"] = resolved
        out.update(
            {
                key: row[key]
                # Tokens against the token cap; `tokens` is null (so left off)
                # for a document the server has not counted yet.
                for key in ("title", "excerpt", "tokens", "limit_tokens", "updated_at")
                if row.get(key) is not None
            }
        )
        # WHERE the note lives, as addresses a reader can open: the ancestry is
        # what tells "the scorer caveat on run X" from the same title elsewhere.
        ancestors = [
            {"uuid": f"{a.get('kind')}:{a.get('id')}", "title": a.get("title")}
            for a in row.get("ancestors") or []
            if isinstance(a, dict) and a.get("id")
        ]
        if ancestors:
            out["ancestors"] = ancestors
        return out

    @staticmethod
    def _note_names_hidden(row: dict, hidden: frozenset[str]) -> bool:
        ancestors = row.get("ancestors") or []
        ids = [row.get("id"), *[a.get("id") for a in ancestors if isinstance(a, dict)]]
        return any(isinstance(i, str) and i.lower() in hidden for i in ids)
