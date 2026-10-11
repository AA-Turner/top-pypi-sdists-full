"""A note's home is a scope — the one place the `note` tool reads and moves homes.

``workbench.notes.home_scope_id`` is NOT NULL; a note created without a home lands in its
organization's General by a database trigger. Scopes are rows of the ``custom.context_scopes``
view. Moving a note is ``platform.set_home`` (SECURITY DEFINER, uses ``auth.uid()``), called
inside the caller's RLS session so the database knows who moves it. This module never writes
``organization_id`` or ``home_scope_id`` itself.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

SCOPES_VIEW = "custom.context_scopes"


@dataclass(frozen=True)
class HomeChoice:
    scope_id: str | None
    name: str | None = None
    error: str | None = None


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


async def _select_scopes(*, ids: list[str] | None = None, organization_id: str | None = None) -> list[dict[str, Any]]:
    """Scopes visible to the acting person, by id list or by organization."""
    from matrx_orm.operations.dynamic_crud import DynamicFilter, dynamic_select

    from matrx_ai.tools.implementations.database import _get_database_name

    filters: list[Any] = []
    if ids is not None:
        filters.append(DynamicFilter(field="id", operator="in", value=list(ids)))
    if organization_id is not None:
        filters.append(DynamicFilter(field="organization_id", value=organization_id))
    return await dynamic_select(
        SCOPES_VIEW,
        filters=tuple(filters),
        columns=("id", "organization_id", "name"),
        database=_get_database_name(),
    )


async def home_names(scope_ids: list[str | None]) -> dict[str, str]:
    """scope id -> name for the homes of these notes (unknown ids are absent)."""
    wanted = sorted({str(s) for s in scope_ids if s})
    if not wanted:
        return {}
    rows = await _select_scopes(ids=wanted)
    return {str(r["id"]): str(r.get("name") or "") for r in rows}


async def resolve_home(home: str, organization_id: str | None) -> HomeChoice:
    """A scope id, or a scope NAME inside ``organization_id``, to one scope."""
    text = (home or "").strip()
    if not text:
        return HomeChoice(None, error="home is empty.")
    if _is_uuid(text):
        rows = await _select_scopes(ids=[text])
        if not rows:
            return HomeChoice(None, error=f"No home with id {text} is visible to you.")
        return HomeChoice(str(rows[0]["id"]), str(rows[0].get("name") or ""))
    if not organization_id:
        return HomeChoice(None, error="A home name needs the note's organization to be resolved in; pass the home id instead.")
    rows = await _select_scopes(organization_id=organization_id)
    hits = [r for r in rows if str(r.get("name") or "").strip().casefold() == text.casefold()]
    if len(hits) == 1:
        return HomeChoice(str(hits[0]["id"]), str(hits[0].get("name") or ""))
    if not hits:
        known = sorted({str(r.get("name") or "") for r in rows if r.get("name")})
        return HomeChoice(None, error=f"No home named '{text}' in this organization. Homes: {', '.join(known) or 'none visible'}.")
    return HomeChoice(None, error=f"{len(hits)} homes are named '{text}' in this organization; pass the home id.")


async def set_home(note_id: str, scope_id: str, expected_version: int | None = None) -> dict[str, Any]:
    """Move a note via ``platform.set_home`` under the caller's open RLS session."""
    from matrx_orm import call_function

    from matrx_ai.tools.implementations.database import _get_database_name

    result = await call_function(
        _get_database_name(), "platform", "set_home", "note", note_id, scope_id, expected_version
    )
    if isinstance(result, str):
        import json

        result = json.loads(result)
    return result if isinstance(result, dict) else {"result": result}
