from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import database
from matrx_ai.tools.models import ToolContext


@pytest.mark.asyncio
async def test_structured_query_passes_only_typed_parts_to_rls_runner(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    async def runner(**kwargs: Any) -> list[dict[str, Any]]:
        seen.update(kwargs)
        return [
            {
                "id": UUID("c9894a96-4f73-45df-bf90-f7138c51f926"),
                "created_at": datetime(2026, 7, 25, 12, 30, tzinfo=UTC),
                "cost": Decimal("1.25"),
            }
        ]

    monkeypatch.setattr(_ext, "get_scoped_query_runner", lambda: runner)
    result = await database._sql_query_scoped(
        {
            "table": "content.block",
            "match": {"status": "active"},
            "fields": ["id"],
            "order_by": ["-created_at"],
            "limit": 10,
            "offset": 2,
        },
        ToolContext(call_id="call-1"),
        1.0,
        "developer",
    )

    assert result.success is True
    assert result.output == {
        "rows": [
            {
                "id": "c9894a96-4f73-45df-bf90-f7138c51f926",
                "created_at": "2026-07-25T12:30:00Z",
                "cost": "1.25",
            }
        ],
        "count": 1,
    }
    assert seen == {
        "table": "content.block",
        "match": {"status": "active"},
        "fields": ["id"],
        "order_by": ["-created_at"],
        "limit": 10,
        "offset": 2,
    }


@pytest.mark.asyncio
async def test_non_super_query_fails_closed_without_rls_runner(monkeypatch) -> None:
    monkeypatch.setattr(_ext, "get_scoped_query_runner", lambda: None)

    result = await database._sql_query_scoped(
        {"table": "content.block"},
        ToolContext(call_id="call-2"),
        1.0,
        "developer",
    )

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "validation"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        "No model registered for table 'scheduler.schedule' in database "
        "'supabase_automation_matrix'",
        "Unknown field(s) on AgentSchedule: ['title', 'description']",
    ],
)
async def test_sql_schema_misses_are_validation_not_operational_failures(
    monkeypatch, message: str
) -> None:
    """Force the two production failure shapes through the producer boundary."""

    async def reject_schema_shape(*args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        raise ValueError(message)

    monkeypatch.setattr(
        "matrx_orm.operations.dynamic_crud.dynamic_select", reject_schema_shape
    )

    result = await database.db_query(
        {"table": "scheduler.agent_schedule", "fields": ["id", "title"]},
        ToolContext(call_id="call-schema-miss"),
    )

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "validation"


def test_real_database_failure_remains_operational() -> None:
    assert database._structured_query_error_type(ConnectionError("database unavailable")) == (
        "database"
    )


@pytest.mark.asyncio
async def test_reads_outside_an_application_schema_are_refused(monkeypatch) -> None:
    """Reads no longer need a registered model, so the schema guard covers them.

    Without this, the live-catalog read path would make auth/vault/graveyard
    relations selectable through the `sql` tool.
    """

    async def runner(**kwargs: Any) -> list[dict[str, Any]]:  # pragma: no cover
        raise AssertionError("a non-application schema must never reach the runner")

    monkeypatch.setattr(_ext, "get_scoped_query_runner", lambda: runner)

    for table in ("auth.users", "vault.secrets", "graveyard.old_thing"):
        result = await database._sql_query_scoped(
            {"table": table},
            ToolContext(call_id="call-guard"),
            1.0,
            "super_admin",
        )
        assert result.success is False
        assert result.error is not None
        assert result.error.error_type == "permission"
        assert "not application data" in result.error.message


@pytest.mark.asyncio
async def test_bare_table_name_is_qualified_before_the_read(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    async def runner(**kwargs: Any) -> list[dict[str, Any]]:
        seen.update(kwargs)
        return []

    async def schemas_for(name: str) -> list[str]:
        return ["ai"]

    monkeypatch.setattr(_ext, "get_scoped_query_runner", lambda: runner)
    monkeypatch.setattr(database, "_schemas_for_table", schemas_for)

    result = await database._sql_query_scoped(
        {"table": "provider_sync_candidates"},
        ToolContext(call_id="call-bare"),
        1.0,
        "developer",
    )

    assert result.success is True
    assert seen["table"] == "ai.provider_sync_candidates"
