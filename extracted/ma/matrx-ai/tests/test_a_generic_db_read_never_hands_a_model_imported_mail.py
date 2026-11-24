"""Generic agent database reads refuse relations that can hold imported Gmail (Limited Use)."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import database


@pytest.mark.parametrize("table", ["crm.interaction", "crm.sending_event", "interaction", "sending_event"])
def test_restricted_relations_are_named(table: str) -> None:
    assert database._model_restricted_read_reason(table)


@pytest.mark.parametrize("table", ["crm.party", "crm.contact_medium", "platform.interaction_log", "party"])
def test_other_relations_stay_open(table: str) -> None:
    assert database._model_restricted_read_reason(table) is None


@pytest.mark.parametrize("table", ["crm.interaction", "crm.sending_event"])
def test_every_read_path_refuses(table: str, monkeypatch: pytest.MonkeyPatch) -> None:
    async def must_not_query(*_a: object, **_k: object) -> None:
        raise AssertionError("the database was asked")

    monkeypatch.setattr(database, "_schemas_for_table", must_not_query)
    monkeypatch.setattr("matrx_orm.operations.dynamic_crud.dynamic_select", must_not_query)
    ctx = SimpleNamespace(call_id="call-1", user_id="user-1", organization_id="org-1")

    direct = asyncio.run(database.db_query({"table": table}, ctx))
    as_person = asyncio.run(database.read_as_person({"table": table}, ctx))
    target, reason = asyncio.run(database._resolve_read_target(table))

    assert not direct.success and "mailbox" in direct.error.message
    assert not as_person.success and "mailbox" in as_person.error.message
    assert target is None and reason and "mailbox" in reason
