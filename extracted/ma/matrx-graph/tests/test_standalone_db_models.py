from __future__ import annotations

import re
from pathlib import Path

from matrx_graph.db.standalone import build_standalone_models

BASELINE = (
    Path(__file__).parents[1] / "matrx_graph" / "db" / "migrations" / "0100_baseline_post_reorg.sql"
)

MODEL_TABLES = {
    "WfDefinition": "definition",
    "WfDefinitionVersion": "definition_version",
    "WfRun": "run",
    "WfCheckpoint": "checkpoint",
    "WfNodeOutcome": "node_outcome",
    "WfNodeEvents": "node_events",
    "WfJob": "job",
    "WfTrigger": "trigger",
    "WfNodeDataSlot": "node_data_slot",
    "WfWorkItem": "work_item",
    "WfCheckpointValue": "checkpoint_value",
}


def _baseline_table_body(table: str) -> str:
    sql = BASELINE.read_text(encoding="utf-8")
    match = re.search(
        rf"CREATE TABLE workflow\.{table} \(\n(?P<body>.*?)\n    \);",
        sql,
        flags=re.DOTALL,
    )
    assert match is not None, f"workflow.{table} missing from standalone baseline"
    return match.group("body")


def _baseline_columns(table: str) -> set[str]:
    columns: set[str] = set()
    for line in _baseline_table_body(table).splitlines():
        column_match = re.match(r"^ {8}([a-z][a-z0-9_]*)\s+", line)
        if column_match is not None:
            columns.add(column_match.group(1))
    return columns


def test_standalone_models_match_fresh_install_baseline_column_for_column() -> None:
    models = build_standalone_models("standalone_contract_test")
    assert set(models) == set(MODEL_TABLES)
    for model_key, table in MODEL_TABLES.items():
        assert set(models[model_key]._fields) == _baseline_columns(table)


def test_node_outcome_standalone_model_keeps_full_kind_verdict() -> None:
    fields = set(build_standalone_models("standalone_kind_test")["WfNodeOutcome"]._fields)
    assert {
        "output_kind",
        "output_kind_ok",
        "output_kind_errors",
        "output_kind_version",
        "output_kind_degraded",
    } <= fields


def test_definition_version_variables_are_non_null_with_empty_list_default() -> None:
    field = build_standalone_models("standalone_variables_test")["WfDefinitionVersion"]._fields[
        "variables"
    ]
    assert field.null is False
    assert field.get_default() == []


def test_node_data_slot_uses_canonical_created_by_owner() -> None:
    fields = build_standalone_models("standalone_mandate_owner_test")["WfNodeDataSlot"]._fields
    assert "created_by" in fields
    assert fields["created_by"].null is False
    assert "user_id" not in fields


def test_work_item_standalone_schema_requires_organization_context() -> None:
    fields = build_standalone_models("standalone_work_item_organization_test")["WfWorkItem"]._fields
    assert fields["organization_id"].null is False
    assert re.search(
        r"^        organization_id\s+UUID NOT NULL,",
        _baseline_table_body("work_item"),
        flags=re.MULTILINE,
    )
