"""The raw `sql` tool never writes into platform-internal schemas, for ANY agent.

DATED-CHANGES-ATTACK B2 (2026-09-28): the "AI Model Config Sync" agent holds the
`sql` tool, which wrote to every schema outside the non-app list — including
`platform` (where scheduled database changes live, and whose functions run as
the database owner), `iam` (access), `scheduler` (every schedule needs Arman's
approval by name) and the audit/history machinery. A write there from an agent
skips every guard those systems have. Reads stay allowed.

The deny list is server code the agent cannot influence (the agent supplies only
a table name); `platform.dated_change` is also guarded inside the database itself
(fixed target allowlist + validation trigger), so even a raw writer cannot widen
what a dated change may touch.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.implementations import database

INTERNAL = [
    "platform.dated_change",
    "platform.entity_types",
    "iam.users",
    "iam.permission",
    "admin.admins",
    "audit.summary",
    "history.ai_offering",
    "meta.anything",
    "ops.app_log",
    "partman.part_config",
    "scheduler.sch_task",
    "runtime.global_execution",
]


async def _resolve(monkeypatch, table: str):
    async def fake_resolve_table(raw: str):
        schema, name = database._split_schema_table(raw)
        return schema, name, []

    monkeypatch.setattr(database, "_resolve_table", fake_resolve_table)
    return await database._resolve_write_target(table)


@pytest.mark.parametrize("table", INTERNAL + ['"PLATFORM"."Dated_Change"', " Iam.Users "])
async def test_platform_internal_writes_are_refused(monkeypatch, table):
    schema, name, err_type, err_msg = await _resolve(monkeypatch, table)
    assert (schema, name) == (None, None), f"{table} was writable through the sql tool"
    assert err_type == "permission"
    assert "platform-internal" in (err_msg or "")


async def test_bare_name_resolving_into_platform_is_refused(monkeypatch):
    async def fake_schemas_for_table(name: str):
        return ["platform"]

    monkeypatch.setattr(database, "_schemas_for_table", fake_schemas_for_table)
    schema, name, err_type, _ = await database._resolve_write_target("dated_change")
    assert (schema, name, err_type) == (None, None, "permission")


@pytest.mark.parametrize("table", ["ai.offering", "workspace.tasks", "seo.keyword"])
async def test_app_schemas_stay_writable(monkeypatch, table):
    schema, name, err_type, _ = await _resolve(monkeypatch, table)
    assert err_type is None and schema is not None


def test_internal_schemas_stay_readable():
    for schema in ("platform", "iam", "scheduler"):
        assert schema not in database._NON_APP_SCHEMAS
