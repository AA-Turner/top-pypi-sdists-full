"""``data_table`` — rows and columns, once, for every producer (the shared primitive).

The one tabular shape: a SQL result, a data-table lookup, a parsed CSV and a table lifted out
of a PDF all answer it. It lives HERE, in the workflow engine's own package, because a producer
inside this package (``data.parse_csv``) must be able to build it, and a package never imports
its host. aidream keeps only the registration (``aidream/services/table_kinds/models.py``,
``kind("data_table", …)(DataTable)``) and the host-side adapters that need the ORM
(``aidream/services/table_kinds/table_adapter.py``).

Distillation ledger: ``common-docs/operations/table-kinds-run.md``. Moved here from aidream by
KINDS-GLUE wave 5 slice 5.3 (manager ruling 2026-10-03: primitives first, one model per kind).

THE TYPE QUESTION, ANSWERED BY MEASUREMENT: ``DataColumn.type`` is OPTIONAL. Only a read through
a registered model knows its column types; a parsed CSV cell is text whatever it looks like, a
PDF cell is ``str | None``, a JSONB row has no declared column list. The producer that knows
declares it; the ones that do not leave it null; no consumer guesses.

THREE MEASURED DEFECTS THIS SHAPE CLOSES: zero rows still declare their columns; every
truncation says so (``truncated`` / ``truncated_at``); ``row_count`` always counts DATA rows.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel

#: Declared column types. Deliberately a small, portable vocabulary rather than
#: Postgres type names: a consumer wants to know "can I right-align this and sum
#: it", not that the source called it `int8`. The source's own spelling survives
#: in `DataColumn.source_type` when it has one.
COLUMN_TYPES = (
    "string",
    "number",
    "integer",
    "boolean",
    "datetime",
    "date",
    "time",
    "json",
    "array",
    "uuid",
    "binary",
    "unknown",
)


class DataColumn(KindSubModel):
    """One column: what it is called, and — when anyone knows — what it holds."""

    name: str = Field(description="Column name as the source presents it.")
    type: str | None = Field(
        default=None,
        description=(
            f"Portable type, one of: {', '.join(COLUMN_TYPES)}. NULL means the producer "
            "genuinely does not know — a parsed CSV cell is a string whatever it looks like. "
            "NULL is never a synonym for 'string'."
        ),
    )
    nullable: bool | None = Field(
        default=None, description="Whether the source permits a null in this column."
    )
    source_type: str | None = Field(
        default=None, description="The source's own type name, verbatim ('NUMERIC', 'TEXT[]')."
    )
    description: str | None = None


class TableSource(KindSubModel):
    """Where the table came from — enough to go back and get it again.

    A table with no provenance cannot be refreshed, audited or explained, and
    every one of the four producers had a different amount of this (the SQL one
    had NONE: not the table queried, not the filters, not the columns asked for).
    """

    origin: str | None = Field(
        default=None, description="What produced it: sql | data_table | csv | pdf | office | api."
    )
    schema_name: str | None = None
    table_name: str | None = None
    table_id: str | None = Field(default=None, description="Our id for a user-owned data table.")
    query: str | None = Field(
        default=None, description="A human-readable description of what was asked for."
    )
    file_id: str | None = Field(default=None, description="The document a table was lifted from.")
    page_number: int | None = Field(default=None, description="1-based page, for extracted tables.")
    table_index: int | None = Field(
        default=None, description="0-based index of this table within its page or document."
    )
    detector: str | None = Field(
        default=None, description="What found the table, e.g. 'pymupdf.find_tables'."
    )
    detector_version: str | None = None


class DataTable(KindModel, kind="data_table"):
    """Rows and columns, from wherever they came.

    ROWS ARE POSITIONAL, aligned to `columns`. That is the one representation
    every producer can supply honestly: a parsed CSV with no header has cells
    but no names, and forcing it into objects would mean inventing `col_1`,
    `col_2` — names no source ever gave. Object-keyed rows are trivially derived
    from `columns` when the names exist; invented names are not recoverable.

    A ragged row is a real thing (PDF extraction produces them), so rows are not
    forced to the column count. A renderer pads; it must never silently drop a
    cell it cannot place.
    """

    columns: list[DataColumn] = Field(
        default_factory=list,
        description="Declared columns. Present even when there are zero rows.",
    )
    rows: list[list[JsonValue]] = Field(
        default_factory=list, description="Data rows, positional, aligned to `columns`."
    )
    row_count: int = Field(
        default=0,
        description="How many DATA rows this table carries. The header is never one of them.",
    )
    total_row_count: int | None = Field(
        default=None,
        description=(
            "How many rows EXIST at the source, when known and different from `row_count`. "
            "This is what makes '500 of 40,000' sayable."
        ),
    )
    truncated: bool = Field(
        default=False, description="Whether rows were cut off. Never left to be inferred."
    )
    truncated_at: int | None = Field(
        default=None, description="The limit that did the cutting, when there was one."
    )
    title: str | None = Field(default=None, description="A human name for the table.")
    source: TableSource | None = Field(default=None, description="Where it came from.")
    notes: list[str] = Field(
        default_factory=list,
        description=(
            "Honest caveats a reader needs: a heuristic header, ragged rows, a lossy "
            "numeric coercion. Empty is a claim that there are none."
        ),
    )


def columns_from_rows(rows: list[dict[str, Any]]) -> list[DataColumn]:
    """Untyped columns, as the UNION of the keys present, in first-seen order.

    For JSONB-backed rows there is no declared column list at all and rows may
    genuinely disagree about their keys. A union keeps every column that exists
    in any row; taking the first row's keys would silently hide the rest.
    """
    seen: dict[str, None] = {}
    for row in rows:
        if isinstance(row, dict):
            for key in row:
                seen.setdefault(key, None)
    return [DataColumn(name=name) for name in seen]


def from_parsed_csv(
    rows: list[Any], columns: list[str] | None, *, title: str | None = None
) -> DataTable:
    """A parsed CSV → `data_table`.

    Every cell is a string, whatever it looks like — `"689.00"` and `"true"` are
    text, and an empty cell is `""`, not null. So no column is typed. Guessing
    here is how a ZIP code becomes an integer and loses its leading zero.
    """
    names = [c for c in (columns or []) if isinstance(c, str)]
    declared = [DataColumn(name=name, type="string") for name in names]

    positional: list[list[Any]] = []
    for row in rows:
        if isinstance(row, dict):
            if not declared:
                declared = columns_from_rows([row])
                for column in declared:
                    column.type = "string"
            positional.append([row.get(c.name) for c in declared])
        elif isinstance(row, list):
            positional.append(list(row))

    notes = ["every cell is text: a parsed CSV declares no types"]
    if not declared and positional:
        notes.append("no header row: the columns are unnamed and rows are positional only")
    return DataTable(
        columns=declared,
        rows=positional,
        row_count=len(positional),
        title=title,
        source=TableSource(origin="csv"),
        notes=notes,
    )


__all__ = [
    "COLUMN_TYPES",
    "DataColumn",
    "DataTable",
    "TableSource",
    "columns_from_rows",
    "from_parsed_csv",
]
