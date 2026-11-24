"""EVERY WORKFLOW SAVE CARRIES ITS AUTHOR.

Definition aa3e6306… ("Verification Desk") was silently broken by a Workflow
Studio save on 2026-09-11 and nobody could be told WHO saved it: the row had
taken ninety draft saves and ``updated_by`` was NULL through every one of
them.

WHY IT WAS NULL — not a missing column, a missing caller. ``workflow.definition``
carries the platform-wide ``_stamp_actor`` trigger::

    uid := COALESCE(NULLIF(current_setting('app.user_id', true), '')::uuid,
                    (SELECT auth.uid()));
    NEW.updated_by := COALESCE(uid, NEW.updated_by);

Both sources are empty on this path. aidream reaches Postgres DIRECTLY through
matrx-orm rather than through PostgREST, so there is no verified JWT for
``auth.uid()`` to read, and nothing in the save path sets the ``app.user_id``
GUC (the only ``set_config('app.user_id', …)`` in the whole repo is in a
provenance test). ``COALESCE(uid, NEW.updated_by)`` therefore preserves
whatever the APPLICATION wrote — and the application wrote nothing.
``DefinitionStore.create`` has always passed ``created_by`` explicitly for
exactly this reason; ``save_draft`` had no twin.

These tests stand on the payload the ORM actually receives, so they fail the
moment a save stops naming its author — and a source check stands on the
callers, so a NEW save path cannot quietly omit it either.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

import pytest

from matrx_graph.db._registry import configure_db
from matrx_graph.db.definition_store import DefinitionStore
from matrx_graph.types.definition import Definition

AUTHOR_ID = "87a6e699-3622-4869-8843-d0867456c0dd"


class _Result:
    def __init__(self, row: dict[str, Any]) -> None:
        self.rows_affected = 1
        self.updated_rows = [row]


class _CapturingModel:
    """Stands in for the matrx-orm ``WfDefinition`` model and records exactly
    what ``save_draft`` asked the database to write."""

    captured: dict[str, Any] = {}

    @classmethod
    def filter(cls, **_: Any) -> Any:
        class _NoRow:
            async def values(self, *_a: str) -> list[dict[str, Any]]:
                return []

        return _NoRow()

    @classmethod
    async def update_where(
        cls,
        _filters: dict[str, Any],
        *,
        expected_version: int | None = None,
        **updates: Any,
    ) -> _Result:
        cls.captured = dict(updates)
        row = {
            "id": uuid4(),
            "name": "Verification Desk",
            "description": None,
            "nodes": [],
            "edges": [],
            "viewport": {"x": 0, "y": 0, "zoom": 1},
            "channels": [],
            "strict_channels": False,
            "entry_nodes": [],
            "variables": [],
            "metadata": {},
            "version": 91,
            "is_active": True,
            "is_archived": False,
            "published_to_web": False,
            "is_favorite": False,
            "tags": [],
            "category": None,
            "created_by": UUID(AUTHOR_ID),
            "organization_id": None,
            "project_id": None,
            "task_id": None,
            "input_kind": None,
            "output_kind": None,
            "created_at": None,
            "updated_at": None,
        }
        return _Result(row)


@pytest.fixture
def store() -> DefinitionStore:
    configure_db(models={"WfDefinition": _CapturingModel})
    _CapturingModel.captured = {}
    return DefinitionStore()


async def _save(store: DefinitionStore, **kwargs: Any) -> None:
    await store.save_draft(
        str(uuid4()),
        definition=Definition(nodes=[], edges=[]),
        **kwargs,
    )


@pytest.mark.asyncio
async def test_a_save_with_an_author_writes_updated_by(store: DefinitionStore) -> None:
    # The whole point. Without this the trigger has nothing to preserve and
    # the column stays NULL for the life of the row.
    await _save(store, user_id=AUTHOR_ID)
    written = _CapturingModel.captured.get("updated_by")
    assert written is not None, (
        "save_draft sent no updated_by. The _stamp_actor trigger cannot "
        "supply one on a direct matrx-orm connection, so the column stays "
        "NULL and the save has no author."
    )
    assert UUID(str(written)) == UUID(AUTHOR_ID)


@pytest.mark.asyncio
async def test_an_unattributed_save_does_not_blank_a_known_author(
    store: DefinitionStore,
) -> None:
    # A headless caller (a seed script, a boot-time repair) has no user. It
    # must leave the column alone rather than overwriting a real author with
    # NULL — the trigger's COALESCE only protects what we do not send.
    await _save(store)
    assert "updated_by" not in _CapturingModel.captured


@pytest.mark.asyncio
async def test_a_blank_author_is_not_written_as_an_author(
    store: DefinitionStore,
) -> None:
    await _save(store, user_id="")
    assert "updated_by" not in _CapturingModel.captured


@pytest.mark.asyncio
async def test_a_non_uuid_principal_never_blanks_a_real_author(
    store: DefinitionStore,
) -> None:
    # Admin-token auth sets user_id to the literal "admin". Coercing that to
    # NULL and writing it would ERASE the last real author — worse than the
    # bug being fixed.
    await _save(store, user_id="admin")
    assert "updated_by" not in _CapturingModel.captured


@pytest.mark.asyncio
async def test_description_omission_preserves_but_explicit_null_clears(store: DefinitionStore) -> None:
    """The store distinguishes an omitted description from an explicit clear."""
    await _save(store)
    assert "description" not in _CapturingModel.captured

    await _save(store, description=None)
    assert _CapturingModel.captured["description"] is None


# The callers (a new save path cannot quietly go unattributed) are host files: that guard is
# tests/package_host_contracts/test_matrx_graph_host.py.
