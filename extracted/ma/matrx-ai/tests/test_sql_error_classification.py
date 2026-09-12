"""An error is classified by SQLSTATE / exception type — never by words in it.

2026-09-11 incident: `sql query table=ai.provider fields=[…, sync_policy]` hit an
unknown column on the deployed (stale) ORM model and was reported to a
super-admin agent as "your access level doesn't permit … requires super_admin",
because the classifier asked `"policy" in str(exc).lower()` and the COLUMN IS
NAMED sync_policy.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools import db_hints
from matrx_ai.tools.implementations import database


class _PgError(Exception):
    """Shape of an asyncpg server error: a SQLSTATE plus a server message."""

    def __init__(self, message: str, sqlstate: str) -> None:
        super().__init__(message)
        self.sqlstate = sqlstate

    def as_dict(self) -> dict[str, Any]:
        return {"message": str(self), "code": self.sqlstate}


async def _empty_schemas() -> list[str]:
    return []


async def _empty_tables() -> dict[str, list[str]]:
    return {}


async def _no_schema_for(name: str) -> list[str]:
    return ["ai"]


async def _columns(schema: str, name: str) -> frozenset[str]:
    return frozenset({"id", "name"})


@pytest.fixture(autouse=True)
def _stub_lookups(monkeypatch):
    monkeypatch.setattr(database, "_app_schemas", _empty_schemas)
    monkeypatch.setattr(database, "_tables_by_schema", _empty_tables)
    monkeypatch.setattr(database, "_schemas_for_table", _no_schema_for)
    monkeypatch.setattr(database, "_get_table_columns", _columns)


@pytest.mark.asyncio
async def test_unknown_column_named_like_a_policy_is_not_a_permissions_error() -> None:
    exc = _PgError('column "sync_policy" of relation "ai.provider" does not exist', "42703")

    message, suggested = await database._agent_db_error(exc)

    assert "access level" not in message
    assert "super_admin" not in message
    assert "sync_policy" in message
    assert "does not exist" in message
    assert "Columns of ai.provider: id, name." in message
    assert database._structured_query_error_type(exc) == "validation"


@pytest.mark.asyncio
async def test_local_unknown_column_error_lists_live_and_build_columns() -> None:
    """The message the live-catalog read path raises stays an unknown-column."""
    from matrx_orm.operations.catalog_select import UnregisteredRelationError

    exc = UnregisteredRelationError(
        'column "sync_polcy" of relation "ai.provider" does not exist\n'
        "Live columns of ai.provider: id, name, sync_policy.\n"
        "The server build's registered model for ai.provider knows: id, name; "
        "the database has: id, name, sync_policy."
    )

    message, _ = await database._agent_db_error(exc)

    assert "access level" not in message
    assert "the database has: id, name, sync_policy" in message


@pytest.mark.asyncio
async def test_genuine_insufficient_privilege_still_reports_permissions() -> None:
    exc = _PgError("permission denied for table provider", "42501")

    message, suggested = await database._agent_db_error(exc)

    assert "access level doesn't permit" in message
    assert "42501" in message
    assert "super_admin" in suggested


@pytest.mark.asyncio
async def test_rls_denial_without_the_word_policy_still_reports_permissions() -> None:
    """A wrapped ORM PermissionDeniedError carries no SQLSTATE of its own."""

    class PermissionDeniedError(Exception):
        pass

    exc = PermissionDeniedError("the statement was refused")
    message, _ = await database._agent_db_error(exc)

    assert "access level doesn't permit" in message


def test_sqlstate_is_read_through_wrappers() -> None:
    inner = _PgError("permission denied for table provider", "42501")
    outer = RuntimeError("query failed")
    outer.__cause__ = inner

    assert db_hints.sqlstate_of(outer) == "42501"
    assert db_hints.is_permission_error(outer) is True
    assert db_hints.is_permission_error(ValueError("a sync_policy column problem")) is False
