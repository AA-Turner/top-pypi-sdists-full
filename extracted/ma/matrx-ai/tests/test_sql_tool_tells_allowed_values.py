"""The sql tool names the allowed values BEFORE a refusal (schema action) and AFTER it, and a
refusal the model can correct never pushes a tool toward the loop guard's shut-off.

Live: chat d1e4226e (2026-11-12) — six guesses at ``roles <@ ARRAY[...]`` values, an
information_schema refusal that pointed nowhere, and the failures counted toward "tool will be
disabled". SUT: the real parser, the real ``db_schema`` / ``_sql_query_scoped`` with only the catalog
seam stubbed, and the real loop-guard evaluator.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.orchestrator.loop_guard import (
    LoopGuardThresholds,
    build_standoff_provision,
    loop_guard_evidence,
    evaluate_loop_health,
    failing_tool_from_history,
)
from matrx_ai.orchestrator.tracking import ToolCallUsage
from matrx_ai.tools import db_hints
from matrx_ai.tools.implementations import database
from matrx_ai.tools.models import ToolContext

ROLES_CHECK = (
    "CHECK ((roles <@ ARRAY['member'::text, 'manager'::text, 'officer'::text, 'incorporator'::text, "
    "'authorized_signer'::text]))"
)


def test_array_containment_names_allowed_values() -> None:
    assert db_hints.allowed_values_from_check(ROLES_CHECK) == [
        "member", "manager", "officer", "incorporator", "authorized_signer",
    ]
    assert db_hints.allowed_values_from_check("CHECK (NOT (roles <@ ARRAY['a'::text]))") == []


@pytest.mark.asyncio
async def test_schema_action_lists_allowed_values_per_column(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_orm.catalog as catalog

    async def resolve(requested: str) -> tuple[str, str, list[str]]:
        return "company", "legal_entity_person", []

    async def columns(database_name: str, *, schema: str, table: str) -> list[dict[str, Any]]:
        return [{"column_name": "roles"}, {"column_name": "name"}]

    async def checks(database_name: str, *, schema: str, table: str) -> list[dict[str, str]]:
        return [
            {"column_name": "roles", "constraint_def": ROLES_CHECK},
            {"column_name": "name", "constraint_def": "CHECK ((char_length(name) > 0))"},
        ]

    async def fks(database_name: str, *, schema: str, table: str) -> list[dict[str, str]]:
        return [{"direction": "out", "local_col": "org_id", "other_table": "iam.organization", "other_col": "id"}]

    monkeypatch.setattr(database, "_resolve_table", resolve)
    monkeypatch.setattr(database, "_get_database_name", lambda: "x")
    monkeypatch.setattr(catalog, "describe_relation_columns", columns)
    monkeypatch.setattr(catalog, "relation_check_constraints", checks)
    monkeypatch.setattr(catalog, "relation_foreign_key_columns", fks)

    result = await database.db_schema({"table": "company.legal_entity_person"}, ToolContext(call_id="c"))
    assert result.success
    assert result.output["allowed_values"] == {
        "roles": ["member", "manager", "officer", "incorporator", "authorized_signer"]
    }
    assert result.output["foreign_keys"] == ["org_id -> iam.organization.id"]


@pytest.mark.asyncio
async def test_information_schema_refusal_points_to_the_schema_action() -> None:
    result = await database._sql_query_scoped(
        {"table": "information_schema.check_constraints"}, ToolContext(call_id="c"), 1.0, "super_admin"
    )
    assert result.success is False
    assert "not application data" in result.error.message
    assert "'schema'" in result.error.message and "allowed values" in result.error.message


def _detail(error: dict[str, Any] | None) -> dict[str, Any]:
    if error is None:
        return {"name": "sql", "success": True}
    return {"name": "sql", "success": False, "error": error}


def _history(details: list[dict[str, Any]]) -> list[ToolCallUsage]:
    return [ToolCallUsage(iteration=1, tool_calls_count=len(details), tool_calls_details=details)]


def _refused(args: dict[str, Any]) -> dict[str, Any]:
    return {**_detail({"error_type": "constraint_violation", "message": "x"}), "arguments": args}


def test_distinct_corrected_constraint_refusals_do_not_count_toward_the_shutoff() -> None:
    limits = LoopGuardThresholds()
    history = _history([_refused({"roles": [f"v{i}"]}) for i in range(limits.window_size)])
    health = evaluate_loop_health(history, thresholds=limits)
    assert health.failures_in_window == 0
    assert health.verdict == "healthy"
    assert failing_tool_from_history(history, window_size=limits.window_size) is None


def test_repeating_the_identical_refused_call_counts_and_trips_the_guard() -> None:
    limits = LoopGuardThresholds()
    history = _history([_refused({"roles": ["ceo"]})] * limits.window_size)
    health = evaluate_loop_health(history, thresholds=limits)
    assert health.failures_in_window == limits.window_size - 1  # the first try is exempt
    assert health.verdict == "stuck"
    assert failing_tool_from_history(history, window_size=limits.window_size) == "sql"


def test_the_standoff_evidence_agrees_with_the_verdict() -> None:
    limits = LoopGuardThresholds()
    distinct = _history([_refused({"roles": [f"v{i}"]}) for i in range(4)])
    p = build_standoff_provision(distinct, tool_name="sql", health=evaluate_loop_health(distinct, thresholds=limits))
    assert p["failures_this_tool"] == 0 and p["consecutive_failures_this_tool"] == 0 and p["failures_total"] == 0
    repeat = _history([_refused({"roles": ["ceo"]})] * 4)
    p = build_standoff_provision(repeat, tool_name="sql", health=evaluate_loop_health(repeat, thresholds=limits))
    assert p["failures_this_tool"] == 3 and p["consecutive_failures_this_tool"] == 3 and p["failures_total"] == 3
    assert loop_guard_evidence(repeat)["tools"][0]["failures"] == 3


@pytest.mark.parametrize(
    "error",
    [
        {"error_type": "validation", "message": "bad args"},
        {"error_type": "permission", "message": "no", "refusal": True},
    ],
)
def test_repeated_bad_arguments_or_refusals_still_trip_the_guard(error: dict[str, Any]) -> None:
    limits = LoopGuardThresholds()
    history = _history([_detail(error)] * (limits.window_size))
    assert evaluate_loop_health(history, thresholds=limits).verdict == "stuck"


def test_a_broken_tool_still_trips_the_guard() -> None:
    limits = LoopGuardThresholds()
    history = _history([_detail({"error_type": "database", "message": "boom"})] * (limits.window_size))
    health = evaluate_loop_health(history, thresholds=limits)
    assert health.verdict == "stuck"
    assert failing_tool_from_history(history, window_size=limits.window_size) == "sql"
