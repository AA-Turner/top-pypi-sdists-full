"""Drift gate: a native tool_def row with NO executor binding is OWNED by this
repo (it runs server-side by routing policy), so a missing @tool declaration
for it is ``MISSING_IN_CODE`` — not an "external" row the gate ignores.

Live incident 2026-09-12: ``memory`` (native, unbound) silently never
registered; the gate counted it as external and reported a clean boot while
every request dropped the tool at pre-flight.
"""

from __future__ import annotations

from matrx_ai.tools.validation.engine import FindingKind, validate


def _row(name: str, *, source_kind: str = "native", executors: list[str] | None = None) -> dict:
    return {
        "name": name,
        "source_kind": source_kind,
        "parameters": {},
        "description": "fixture",
        "is_active": True,
        "validation_exempt": False,
        "executors": executors or [],
    }


def test_unbound_native_row_without_code_is_missing_in_code() -> None:
    report = validate({}, [_row("ghost_native")], owner_executors={"matrx-ai-core"})
    kinds = {(f.kind, f.tool_name) for f in report.findings}
    assert (FindingKind.MISSING_IN_CODE, "ghost_native") in kinds
    assert report.db_count == 1 and report.external_count == 0


def test_unbound_non_native_row_stays_external() -> None:
    report = validate(
        {},
        [_row("remote_thing", source_kind="mcp_discovered")],
        owner_executors={"matrx-ai-core"},
    )
    assert not report.findings
    assert report.external_count == 1


def test_row_bound_to_foreign_executor_stays_external() -> None:
    report = validate(
        {}, [_row("client_only", executors=["matrx-user"])], owner_executors={"matrx-ai-core"}
    )
    assert not report.findings
    assert report.external_count == 1
