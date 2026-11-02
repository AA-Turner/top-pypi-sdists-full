"""``data.parse_csv`` + ``data.parse_yaml`` — text-to-structured-data parsers.

Companions to ``data.parse_json``: exports, spreadsheets-as-text, and config
files are the other three shapes text arrives in. Same posture — a parse
failure is a node Failure (route it with an ERROR edge or let it park), never
a silent ok=false payload.

``data.parse_yaml`` produces the canonical ``Value`` archetype (kind
``value``), byte-for-byte the parse_json contract. ``data.parse_csv`` has a
richer honest shape (rows + columns + count) and registers its own kind.
"""

from __future__ import annotations

import csv
import io
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.nodes.data.data_table import DataTable, from_parsed_csv
from matrx_graph.types.canonical_payloads import Value
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

_IO_HANDLES = (
    HandleSpec(id="in", direction=HandleDirection.INPUT),
    HandleSpec(id="out", direction=HandleDirection.OUTPUT),
)

#: Row-count ceiling — a CSV bigger than this belongs in the files/RAG
#: pipeline, not a node payload that gets checkpointed as JSONB.
MAX_CSV_ROWS = 100_000


class ParseCsvInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="CSV text to parse.")


class ParseCsvConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    delimiter: str = Field(
        default=",",
        min_length=1,
        max_length=1,
        description="Column separator — ',' for CSV, '\\t' for TSV, ';' etc.",
    )
    has_header: bool = Field(
        default=True,
        description=(
            "First line names the columns: rows become objects keyed by those "
            "names. Off, rows are plain value lists."
        ),
    )
    trim: bool = Field(default=True, description="Strip surrounding whitespace from every cell.")


class ParseCsvOutput(KindModel, kind="parsed_table"):
    rows: list[JsonValue] = Field(
        description="The parsed rows — objects when a header exists, else value lists."
    )
    columns: list[str] = Field(
        default_factory=list,
        description="Column names from the header row (empty when has_header is off).",
    )
    count: int = Field(description="How many data rows were parsed.")
    #: KINDS-GLUE 5.3 (Stage D, additive): the same rows as one typed ``data_table`` (every
    #: column text). ``rows`` / ``columns`` / ``count`` stay: ``scraped_page`` nests this kind.
    table: DataTable | None = Field(
        default=None, description="The same rows as one data_table (every column text)."
    )


class ParseCsvExecutor:
    """Parse delimited text into typed rows via the stdlib csv reader."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.parse_csv",
        category=NodeCategory.DATA,
        display_name="CSV to Data",
        description="Turn spreadsheet-style text into rows you can work with.",
        input_schema=ParseCsvInput,
        input_kind="text",
        output_schema=ParseCsvOutput,
        config_schema=ParseCsvConfig,
        output_kind="parsed_table",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="table",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ParseCsvInput,
        config: ParseCsvConfig,
    ) -> NodeResult[ParseCsvOutput]:
        _ = ctx
        try:
            reader = csv.reader(io.StringIO(inputs.text), delimiter=config.delimiter)
            raw_rows = list(reader)
        except csv.Error as e:
            return failure("parse_failed", f"csv.Error: {e}")
        if len(raw_rows) > MAX_CSV_ROWS + (1 if config.has_header else 0):
            return failure(
                "too_many_rows",
                f"CSV has more than {MAX_CSV_ROWS} rows — a table this large "
                "belongs in file/RAG ingestion, not a workflow payload.",
            )

        def cell(value: str) -> str:
            return value.strip() if config.trim else value

        columns: list[str] = []
        rows: list[JsonValue] = []
        if config.has_header:
            if raw_rows:
                columns = [cell(c) for c in raw_rows[0]]
            for raw in raw_rows[1:]:
                row: dict[str, JsonValue] = {}
                for i, name in enumerate(columns):
                    row[name or f"column_{i + 1}"] = cell(raw[i]) if i < len(raw) else None
                rows.append(row)
        else:
            rows = [[cell(v) for v in raw] for raw in raw_rows]
        return success(
            ParseCsvOutput(
                rows=rows,
                columns=columns,
                count=len(rows),
                table=from_parsed_csv(rows, columns),
            )
        )


class ParseYamlInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="YAML text to parse.")


class ParseYamlExecutor:
    """Parse YAML text via ``yaml.safe_load`` — never full load."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.parse_yaml",
        category=NodeCategory.DATA,
        display_name="YAML to Data",
        description="Turn YAML text (configs, front-matter) into real data.",
        input_schema=ParseYamlInput,
        input_kind="text",
        output_schema=Value[JsonValue],
        output_kind="value",
        handles=_IO_HANDLES,
        determinism=ActionTier.PURE,
        icon="file-code",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ParseYamlInput,
        config: BaseModel,
    ) -> NodeResult[Value[JsonValue]]:
        _ = ctx, config
        import yaml

        try:
            parsed = yaml.safe_load(inputs.text)
        except yaml.YAMLError as e:
            return failure("parse_failed", f"{type(e).__name__}: {e}")
        return success(Value[JsonValue](value=parsed))
