"""Regression guard: schemas whose writes belong to a governed service must be
refused by the raw `database` tool — while staying fully readable.

`crm` is the first entry. Every `crm.party` row needs name-key canonicalization,
natural-key dedup, `source` stamping and merge-lineage awareness; a raw INSERT
is a duplicate factory. The guard lifts once the party resolver + `agent_data`
registration exist (CRM Wave 1) — until then reads are free, writes are refused
with an explanation the model can act on.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.implementations import database


async def _resolve(monkeypatch, table: str):
    async def fake_resolve_table(raw: str):
        schema, name = database._split_schema_table(raw)
        return schema, name, []

    monkeypatch.setattr(database, "_resolve_table", fake_resolve_table)
    return await database._resolve_write_target(table)


@pytest.mark.parametrize(
    "table", ["crm.party", "crm.contact_medium", "crm.campaign", "crm.interaction"]
)
async def test_crm_writes_are_refused(monkeypatch, table):
    schema, name, err_type, err_msg = await _resolve(monkeypatch, table)
    assert schema is None and name is None
    assert err_type == "permission"
    assert "governed party path" in (err_msg or "")


async def test_ordinary_schema_still_writable(monkeypatch):
    schema, name, err_type, err_msg = await _resolve(monkeypatch, "workspace.tasks")
    assert (schema, name) == ("workspace", "tasks")
    assert err_type is None and err_msg is None


async def test_crm_stays_readable_and_discoverable():
    """The guard must NOT hide `crm` from schema discovery — agents read it."""
    assert "crm" not in database._NON_APP_SCHEMAS
    assert not database._is_blocked_table("crm.party")


def test_generic_blocklist_is_exact_relation_not_bare_name():
    assert database._is_blocked_table("chat.message")
    assert not database._is_blocked_table("support.message")
    with pytest.raises(ValueError, match="schema.table"):
        database._is_blocked_table("message")
