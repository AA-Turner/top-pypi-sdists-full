"""Regression: the generic admin db_insert/upsert tool must stamp
organization_id onto rows headed for an org-scoped table.

``_stamp_auto_fields`` in ``tools/implementations/database.py`` is the ONE
identity-stamping seam for every write the generic any-table admin tool
(db_insert / sql upsert) makes — the table is resolved at call time from the
agent's own arguments, so it can only pick up organization_id here, from the
verified request context. Before this fix it stamped ``created_by``/
``user_id`` only; a row destined for an org-scoped table with no
organization_id in its payload would have hit the NOT NULL constraint.
"""
from __future__ import annotations

from uuid import uuid4

import pytest

from matrx_ai.tools.implementations import database as db_tool
from matrx_ai.tools.models import ToolContext


def _make_ctx(*, user_id: str | None, organization_id: str | None) -> ToolContext:
    ctx = ToolContext(call_id=str(uuid4()), tool_name="db_insert")
    # ToolContext.user_id / .organization_id are properties reading the app
    # context; monkeypatch the instance attribute lookup isn't available, so
    # tests patch the app_context module instead (see fixtures below).
    return ctx


@pytest.fixture
def patched_app_context(monkeypatch):
    def _patch(*, user_id, organization_id):
        from types import SimpleNamespace

        fake_ctx = SimpleNamespace(user_id=user_id, organization_id=organization_id)
        monkeypatch.setattr(
            "matrx_ai.context.app_context.try_get_app_context", lambda: fake_ctx
        )
        monkeypatch.setattr(
            "matrx_ai.context.app_context.get_app_context", lambda: fake_ctx
        )

    return _patch


@pytest.mark.asyncio
async def test_stamps_organization_id_when_table_carries_the_column(
    monkeypatch, patched_app_context
):
    org_id = str(uuid4())
    patched_app_context(user_id="user-1", organization_id=org_id)

    monkeypatch.setattr(
        db_tool,
        "_get_table_columns",
        lambda schema, name: _async_return(
            frozenset({"id", "created_by", "organization_id", "title"})
        ),
    )

    row = {"title": "hello"}
    await db_tool._stamp_auto_fields("workspace", "tasks", [row], _make_ctx(user_id=None, organization_id=None))

    assert row.get("organization_id") == org_id
    assert row.get("created_by") == "user-1"


@pytest.mark.asyncio
async def test_never_stamps_organization_id_when_table_has_no_such_column(
    monkeypatch, patched_app_context
):
    org_id = str(uuid4())
    patched_app_context(user_id="user-1", organization_id=org_id)

    monkeypatch.setattr(
        db_tool,
        "_get_table_columns",
        lambda schema, name: _async_return(frozenset({"id", "created_by", "title"})),
    )

    row = {"title": "hello"}
    await db_tool._stamp_auto_fields("some", "table", [row], _make_ctx(user_id=None, organization_id=None))

    assert "organization_id" not in row
    assert row.get("created_by") == "user-1"


async def _async_return(value):
    return value
