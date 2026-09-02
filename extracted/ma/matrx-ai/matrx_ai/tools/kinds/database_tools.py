"""Kinds for the database-group tool results.

Ledger rows: `data` `data_action` `db_admin` `db_user` `sql` (KIND_TOOL_LEDGER,
agent ``lead-w2c``). NOT here: `scope_system` (kinds/scope_tools.py) and
`value_store` (kinds/value_store.py) — same batch, different families.

WHY NOT `sql_query_result`
--------------------------
The ledger's reuse candidate for these rows was the registered (distilled)
`sql_query_result` — the workflow ``admin.sql.*`` nodes' rows/row_count/command
shape. Reading the implementations rejected it (the batch-3 finding: claim-time
guesses are candidates, never conclusions): every one of these tools is a
multi-action dispatcher whose union carries catalog listings, schema
descriptions, write receipts and cap keys that shape never declares. Binding
them to it would declare a shape they never return.

TWO TOOLS, ONE SHAPE: `db_admin` and `db_user` run the SAME dispatcher
(``aidream/services/db_grants/tools.py`` — they differ only in engine and RLS
wrapping), so they share ``db_scoped_result``.

All placeholder tier: rows/records stay opaque ``dict``s — the columns are the
caller's, not ours. Union rule (the trace batch's cap-keys finding): every key
any success branch can emit is declared, action-specific keys optional.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "data_tool_result",
    label="Data Tool Result",
    family="database",
    example={"resource_type": "note", "rows": [{"id": "n-1", "title": "Example"}], "count": 1},
    # PLACEHOLDER — the outer union of catalog/query/count/get/create/update/
    # delete over the user's own RLS-scoped resources.
    maturity="placeholder",
)
class DataToolResult(KindModel):
    #: `catalog`.
    resources: list[dict] | None = None
    usage: str | None = None
    #: `query` — one page + self-cap state (`total` is the pre-cap count).
    resource_type: str | None = None
    rows: list[dict] | None = None
    count: int | None = None
    total: int | None = None
    truncated: bool | None = None
    truncation_notice: str | None = None
    #: `get` / `create` / `update`.
    record: dict | None = None
    created: bool | None = None
    updated: bool | None = None
    #: `delete` receipt.
    id: str | None = None
    deleted: bool | None = None


@kind(
    "data_action_result",
    label="Data Action Result",
    family="database",
    example={"operation": "transcript_to_note", "result": {"note_id": "n-1"}},
    # PLACEHOLDER — named multi-table operations; `result` is the operation's
    # own payload and stays open.
    maturity="placeholder",
)
class DataActionResult(KindModel):
    #: `catalog`.
    operations: list[dict] | None = None
    usage: str | None = None
    #: a named operation run.
    operation: str | None = None
    result: JsonValue | None = None


@kind(
    "db_scoped_result",
    label="Scoped DB Result",
    family="database",
    example={"table": "workbench.notes", "rows": [{"id": "n-1"}], "count": 1},
    # PLACEHOLDER — ONE kind for BOTH `db_admin` and `db_user`: the same
    # grant-gated dispatcher (schema/query/get/create/update/delete), differing
    # only in engine, so one shape — not two near-duplicate slugs.
    maturity="placeholder",
)
class DbScopedResult(KindModel):
    table: str | None = None
    #: `schema`.
    primary_keys: list[str] | None = None
    columns: list[dict] | None = None
    references: list[dict] | None = None
    referenced_by: list[dict] | None = None
    #: `query`.
    rows: list[dict] | None = None
    count: int | None = None
    #: `get` / `create` / `update`.
    record: dict | None = None
    created: bool | None = None
    updated: bool | None = None
    #: `delete` receipt.
    id: str | None = None
    deleted: bool | None = None


@kind(
    "sql_tool_result",
    label="SQL Tool Result",
    family="database",
    example={"rows": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}], "count": 1},
    # PLACEHOLDER — the admin `sql` dispatcher's union: query pages, the three
    # schema projections (all-schemas listing / one-table description / the
    # ambiguous-or-missing report), and the insert/update/upsert/delete write
    # receipts (`data` full echo or `ids` minimal echo).
    maturity="placeholder",
)
class SqlToolResult(KindModel):
    #: `query`.
    rows: list[dict] | None = None
    count: int | None = None
    #: `schema` — the all-schemas / one-schema listing.
    schemas: dict | None = None
    schema_count: int | None = None
    total_tables: int | None = None
    note: str | None = None
    #: `schema` — one table's description (the `table` value is
    #: schema-qualified; the old redundant bare `schema` key was dropped with
    #: the reshape, like `text_regex_extract`'s `span`), or the
    #: ambiguous/missing report.
    table: str | None = None
    columns: list[dict] | None = None
    ambiguous: bool | None = None
    candidates: list[str] | None = None
    foreign_keys: list[str] | None = None
    referenced_by: list[str] | None = None
    fk_lookup_error: dict | None = None
    #: write receipts — the verb key carries the affected-row count.
    inserted: int | None = None
    updated: int | None = None
    upserted: int | None = None
    deleted: int | None = None
    data: list[dict] | None = None
    ids: list[str | None] | None = None


#: tool name → model, merged into ``TOOL_RESULT_KINDS`` by the package init.
DATABASE_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "data": DataToolResult,
    "data_action": DataActionResult,
    "db_admin": DbScopedResult,
    "db_user": DbScopedResult,
    "sql": SqlToolResult,
}
