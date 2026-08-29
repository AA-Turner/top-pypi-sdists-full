"""Pydantic models for the Atlas wire format v3.

These models define the schema for the flat-array wire format emitted by the
graph builder over SSE. Both ``build_graph`` (runtime) and ``analyze_file``
(static analysis) produce ``AtlasWireFormat`` instances.

The markdown specification at ``tools/atlas/atlas-server/docs/wire-format-v3.md``
is generated from these models -- run ``python -m mistralai.workflows.core.wire_format``
to regenerate it.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceRange(BaseModel):
    """Byte-offset range ``[begin, end)`` within a source file."""

    model_config = ConfigDict(populate_by_name=True)

    begin: int = Field(description="Start byte offset")
    end: int = Field(description="End byte offset (exclusive)")
    line: int = Field(default=0, description="Line number in source")


class FileRange(BaseModel):
    """Byte-offset range ``[begin, end)`` for a file within the concatenated source blob."""

    model_config = ConfigDict(populate_by_name=True)

    begin: int = Field(description="Start byte offset in concatenated source")
    end: int = Field(description="End byte offset (exclusive)")


class EntrypointInfo(BaseModel):
    """Entry method name and source byte range."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(description="Entry method name")
    begin: int = Field(description="Start byte offset")
    end: int = Field(description="End byte offset (exclusive)")


class HandlerInfo(BaseModel):
    """Metadata about a signal, update, or query handler on a workflow class."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(description="Handler method name")
    param_type: str | None = Field(default=None, description="Annotation of first non-self parameter")
    return_type: str | None = Field(default=None, description="Return type annotation")
    source_range: SourceRange | None = Field(default=None, description="Byte offsets into source")


class FlatNode(BaseModel):
    """A flat node in the v3 wire format.

    All nodes share the core fields (``id``, ``type``, ``name``, ``line``,
    ``source_range``).  Optional fields are present only on specific node types.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Unique node identifier")
    type: str = Field(description="Node type (activity, conditional, loop, ...)")
    name: str = Field(description="Display name")
    line: int = Field(description="Line number in source")
    source_range: SourceRange = Field(description="Byte offsets into source")

    callees: list[str] | None = Field(default=None, description="Called function names (dispatch nodes)")
    dispatch_label: str | None = Field(default=None, description="Protocol dispatch label (dispatch nodes)")
    tools: list[str] | None = Field(default=None, description="Tool names (agent nodes)")
    handoffs: list[str] | None = Field(default=None, description="Handoff agent names (agent nodes)")
    connectors: list[str] | None = Field(
        default=None,
        description="Connector names this node uses (activity nodes via Depends, agent nodes via connectors=)",
    )
    children: list[str] | None = Field(default=None, description="Child node IDs (loop, try_except)")
    branches: list[list[str]] | None = Field(default=None, description="Per-lane node IDs (parallel)")
    is_error: bool | None = Field(default=None, description="True for error/raise output nodes")
    branchTrue: list[str] | None = Field(  # noqa: N815
        default=None,
        description="Node IDs in a container-child conditional's true branch (drives branch layout)",
    )
    branchFalse: list[str] | None = Field(  # noqa: N815
        default=None,
        description="Node IDs in a container-child conditional's false branch (drives branch layout)",
    )
    branchDescendants: list[str] | None = Field(  # noqa: N815
        default=None,
        description="IDs of non-terminal nodes in conditional branches",
    )
    child_workflow_id: str | None = Field(
        default=None,
        description=(
            "Routing identifier of the child workflow (child_workflow nodes): its registered "
            "workflow name (the class name when unresolvable). Set only when the child is in "
            "the scanned set."
        ),
    )
    child_workflow_file: str | None = Field(
        default=None,
        description="Source file of the child workflow, when in the scanned set (child_workflow nodes)",
    )
    is_async: bool | None = Field(
        default=None,
        alias="async",
        description="True for fire-and-forget child workflows (child_workflow nodes)",
    )
    param_type: str | None = Field(default=None, description="Type annotation of the first non-self parameter")
    param_fields: list[dict[str, str]] | None = Field(
        default=None, description="Structured parameter list: [{name, type, description?}]"
    )


class FlatEdge(BaseModel):
    """A flat directed edge in the v3 wire format."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Unique edge identifier")
    from_: str = Field(alias="from", description="Source node ID")
    to: str = Field(description="Target node ID")
    kind: str = Field(description="Edge kind (sequential, branch_true, ...)")


class AtlasWireFormat(BaseModel):
    """Top-level v3 wire format emitted by the server over SSE.

    ``sources`` is populated by the builder functions (``build_graph_dynamically``
    / ``build_graph_statically``) and excluded from ``to_dict()`` by default so
    that user source code is not sent over the API.  ``node_summaries`` and
    ``workflow_summary`` are added by the worker after LLM summarisation.
    """

    model_config = ConfigDict(populate_by_name=True)

    version: Literal[3] = Field(default=3, description="Format version discriminant")
    workflow_name: str = Field(
        description="Registered workflow name (@workflow.define(name=...)); the class name when unresolvable"
    )
    sources: dict[str, str] | None = Field(default=None, description="Per-file source text, keyed by path")
    files: dict[str, FileRange] = Field(description="Byte ranges per file path")
    primary_file: str | None = Field(default=None, description="File the user selected in the picker")
    nodes: list[FlatNode] = Field(description="All graph nodes, flat list")
    edges: list[FlatEdge] = Field(description="All graph edges, flat list")
    incomplete: bool = Field(description="True when cross-module refs are unresolved")
    entrypoint: EntrypointInfo | None = Field(default=None, description="Entry method metadata")
    output_type: str | None = Field(default=None, description="Return type annotation of the entry method")
    signals: list[HandlerInfo] = Field(default_factory=list, description="@workflow.signal() handlers")
    updates: list[HandlerInfo] = Field(default_factory=list, description="@workflow.update() handlers")
    queries: list[HandlerInfo] = Field(default_factory=list, description="@workflow.query() handlers")
    connectors: list[str] = Field(default_factory=list, description="@uses_connectors() declared connector names")
    on_behalf_of: bool = Field(default=False, description="@workflow.define(on_behalf_of=...) flag")
    schedule: str | None = Field(default=None, description="Reserved; always null")
    node_summaries: dict[str, dict[str, str]] | None = Field(
        default=None,
        description="LLM-generated summaries keyed by node ID",
    )
    workflow_summary: dict[str, str] | None = Field(
        default=None,
        description="LLM-generated summary of the workflow as a whole",
    )

    def to_dict(self, *, include_sources: bool = False) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict using wire field names."""
        exclude = {"sources"} if not include_sources else None
        return self.model_dump(by_alias=True, exclude_none=True, exclude=exclude)


# ---------------------------------------------------------------------------
# Documentation generator
# ---------------------------------------------------------------------------

_NODE_TYPES_TABLE = """\
| `type` | Shape in UI | Description |
|---|---|---|
| `workflow` | Rectangle (container) | Synthetic root node wrapping all other nodes |
| `entrypoint` | Circle | The workflow entry method |
| `activity` | Rounded rect | A resolved workflow step |
| `output` | Rounded rect | Workflow output terminus |
| `unknown` | Dashed rect | Unrecognised code -- rendered as `...` |
| `conditional` | Diamond (container) | `if/elif/else` branch point |
| `loop` | Rectangle (container) | `for`/`while` body |
| `try_except` | Rectangle (container) | `try/except` body |
| `dispatch` | Stacked rect | Protocol dispatch; carries `callees[]` |
| `agent` | Stacked rect | `Runner.run` agent; carries `tools[]` and `handoffs[]` |
| `human_input` | Rounded rect | `wait_for_input` -- waits for human |
| `wait_condition` | Rounded rect | `wait_condition` -- event wait |
| `parallel` | Wide rect | Parallel fan-out |
| `task` | Rounded rect | Background task |
| `memory_op` | Rounded rect | Memory operation (save/load) |
| `continue_as_new` | Rounded rect | `continue_as_new` -- restarts the workflow with fresh history |\
"""

_EDGE_KINDS_TABLE = """\
| `kind` | Description |
|---|---|
| `sequential` | Normal control flow |
| `branch_true` / `branch_false` | Conditional -> first node in each branch |
| `branch_merge` | Branch rejoins the main flow |
| `branch_true_skip` / `branch_false_skip` | Empty branch bypass |
| `branch_exit_true` / `branch_exit_false` | Branch that returns early |\
"""

_SUMMARIES_EXAMPLE = """\
```json
{
  "file": "workflows/billing.py",
  "status": "ready",
  "workflow_summary": {
    "short": "Customer billing run",
    "long": "Charges a customer's saved card and emails them a receipt."
  },
  "summaries": {
    "charge_card": {
      "short": "charge customer card",
      "long": "Initiates a card charge via the payment gateway."
    },
    "send_receipt": {
      "short": "send receipt email",
      "long": "Sends a receipt to the customer's email address."
    }
  }
}
```\
"""


def _field_row(name: str, field_info: dict[str, object], *, alias: str | None = None) -> str:
    display = f"`{alias or name}`"
    schema_type = field_info.get("type", "")
    anyof: list[dict[str, object]] = field_info.get("anyOf") or []  # type: ignore[assignment]
    items = field_info.get("items")
    desc = field_info.get("description", "")

    if anyof:
        parts = []
        for variant in anyof:
            if variant.get("type") == "null":
                parts.append("null")
            elif variant.get("type"):
                parts.append(f"`{variant['type']}`")
            elif "$ref" in variant:
                ref_name = str(variant["$ref"]).rsplit("/", 1)[-1]
                parts.append(f"`{ref_name}`")
        type_str = " \\| ".join(parts)
    elif schema_type == "array":
        if isinstance(items, dict) and "$ref" in items:
            inner = items["$ref"].rsplit("/", 1)[-1]
            type_str = f"`{inner}[]`"
        elif isinstance(items, dict) and items.get("type") == "array":
            type_str = "`string[][]`"
        else:
            inner = items.get("type", "any") if isinstance(items, dict) else "any"
            type_str = f"`{inner}[]`"
    elif schema_type:
        type_str = f"`{schema_type}`"
    else:
        type_str = ""

    return f"| {display} | {type_str} | {desc} |"


def _model_table(model: type[BaseModel], *, skip: set[str] | None = None) -> str:
    schema = model.model_json_schema(mode="serialization")
    props = schema.get("properties", {})
    rows = ["| Field | Type | Description |", "|---|---|---|"]
    for name, info in props.items():
        if skip and name in skip:
            continue
        rows.append(_field_row(name, info, alias=name))
    return "\n".join(rows)


def generate_wire_format_docs() -> str:
    """Generate the wire-format-v3.md content from the Pydantic models."""
    sections = [
        "# Wire Format V3",
        "",
        "Atlas streams graph data from the server to the browser as SSE. Each `graph` event "
        "carries a JSON payload conforming to this schema. The same format is used for graphs "
        "uploaded by the worker and stored via the API, so the TypeScript frontend has a single "
        "entry point (`flatToTopology`) whatever the source.",
        "",
        "## Encoding",
        "",
        "V3 uses **flat arrays** -- a list of nodes and a list of edges -- rather than a nested "
        "tree. This is an [adjacency-list](https://en.wikipedia.org/wiki/Adjacency_list) encoding: "
        "container nodes reference their children by ID rather than embedding them as nested objects. "
        "The tree structure is preserved through references, not nesting.",
        "",
        "## Top-level fields",
        "",
        _model_table(AtlasWireFormat, skip={"node_summaries", "workflow_summary"}),
        "",
        "## Node types (`WireFlatNode.type`)",
        "",
        _NODE_TYPES_TABLE,
        "",
        "## Edge kinds (`WireFlatEdge.kind`)",
        "",
        _EDGE_KINDS_TABLE,
        "",
        "## `WireFlatNode` fields",
        "",
        _model_table(FlatNode),
        "",
        "## `graph_summaries` SSE event",
        "",
        "After a `graph` event is emitted, the server starts a background task that calls "
        "the Mistral API to generate short and long descriptions for each node. When complete "
        "it emits a `graph_summaries` event:",
        "",
        _SUMMARIES_EXAMPLE,
        "",
        "| Field | Type | Description |",
        "|---|---|---|",
        "| `file` | `string` | Relative path of the selected file (matches the `graph` event) |",
        '| `status` | `"ready" \\| "failed" \\| "disabled"` | `disabled` when no API key is set; '
        "`failed` when all LLM attempts fail; `ready` on success |",
        "| `summaries` | `Record<string, { short: string; long: string }>` | Keyed by node ID; "
        "empty when `status` is not `ready` |",
        "| `workflow_summary` | `{ short: string; long: string } \\| null` | Describes the workflow "
        "as a whole; `null` when the model omitted it or `status` is not `ready` |",
        "",
        "Node IDs with types `workflow`, `entrypoint`, and `output` are excluded from summaries.",
        "",
        "Both fields are also persisted on the graph payload itself, as the top-level "
        "`node_summaries` and `workflow_summary` keys, so a stored graph carries its summaries "
        "without a second event.",
        "",
        "## `WireFlatEdge` fields",
        "",
        _model_table(FlatEdge),
        "",
    ]
    return "\n".join(sections)


if __name__ == "__main__":
    import sys

    sys.stdout.write(generate_wire_format_docs())
