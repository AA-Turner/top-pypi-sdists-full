"""The compiled topology document.

What :func:`dreadnode.workflows.compile` emits, what travels in the OCI config,
what is stored in ``workflow_definitions.topology_json``, and what the run page
renders. See ``plans/workflows-prd.md`` §11.

Design rules held here:

* **Structure only, no layout.** Positions are a view concern — they must be
  recomputed whenever a viewer expands or collapses a fan-out group.
* **Event types are declared once and referenced by name.** A schema per *edge*
  would duplicate the same schema across every edge carrying that type.
* **Everything an author wrote that a reader would want** — docstrings,
  annotation strings as authored, field descriptions, defaults, source spans.
"""

import typing as t

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "TOPOLOGY_SIZE_CAP_BYTES",
    "TOPOLOGY_VERSION",
    "EdgeKind",
    "EventTypeDoc",
    "FanOutPoint",
    "FieldDoc",
    "JoinPoint",
    "NodeConfig",
    "NodeConsumes",
    "NodeEmit",
    "NodeKind",
    "ParamDoc",
    "SourceSpan",
    "Topology",
    "TopologyEdge",
    "TopologyInput",
    "TopologyNode",
]

TOPOLOGY_VERSION = 1
"""Document schema version. Bump when the shape changes incompatibly."""

TOPOLOGY_SIZE_CAP_BYTES = 256 * 1024
"""Compile fails above this, so the failure lands on the author's machine."""

NodeKind = t.Literal["entry", "plain", "agent", "join", "approval_gate", "terminal"]
EdgeKind = t.Literal["sequential", "fan_out", "fork", "join", "branch", "approval", "loop"]
ParamKind = t.Literal["context", "event", "collect"]
Cardinality = t.Literal["one", "many"]


class SourceSpan(BaseModel):
    """Where an authored object lives, relative to the capability root."""

    model_config = ConfigDict(extra="forbid")

    path: str
    start_line: int
    end_line: int


class FieldDoc(BaseModel):
    """One field of an event or input model, flattened for display.

    The UI renders this rather than walking JSON Schema for the common case.
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    type: str
    required: bool
    default: t.Any = None
    doc: str | None = None


class ParamDoc(BaseModel):
    """One parameter of a step function, with its annotation *as authored*."""

    model_config = ConfigDict(extra="forbid")

    name: str
    annotation: str
    kind: ParamKind


class EventTypeDoc(BaseModel):
    """A declared event type, referenced by name from nodes and edges."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    doc: str | None = None
    schema_: dict[str, t.Any] = Field(default_factory=dict, alias="schema")
    fields: list[FieldDoc] = Field(default_factory=list)
    source: SourceSpan | None = None
    builtin: bool = False


class NodeConsumes(BaseModel):
    """What a step waits for before it runs."""

    model_config = ConfigDict(extra="forbid")

    events: list[str]
    collect: bool = False
    min_success: int | t.Literal["all"] | None = None


class NodeEmit(BaseModel):
    """One event type a step may emit."""

    model_config = ConfigDict(extra="forbid")

    event: str
    cardinality: Cardinality = "one"
    arm: int | None = None
    """Set when the emit is one arm of a returned union (a branch)."""
    fork_index: int | None = None
    """Set when the emit is one element of a returned tuple (a fork)."""


class NodeConfig(BaseModel):
    """Decorator configuration, after policy is applied."""

    model_config = ConfigDict(extra="forbid")

    max_concurrency: int | None = None
    retries: int = 0
    effective_max_attempts: int = 1
    """The truth, not the request — agent nodes are pinned to 1 in Release 1."""
    materialization_cap: int | None = None
    timeout_sec: int | None = None
    max_iterations: int | None = None
    """RESERVED — bounded loops. Always None in v1."""


class TopologyNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    title: str
    kind: NodeKind
    doc: str | None = None
    doc_summary: str | None = None
    consumes: NodeConsumes
    emits: list[NodeEmit] = Field(default_factory=list)
    params: list[ParamDoc] = Field(default_factory=list)
    config: NodeConfig = Field(default_factory=NodeConfig)
    agents: list[str] = Field(default_factory=list)
    """Agents this step names literally. Definite: it calls exactly these."""
    agents_dynamic: bool = False
    agent_candidates: list[str] = Field(default_factory=list)
    """Agents a *dynamic* step might run, resolved from whoever builds its input.

    Deliberately separate from ``agents``. These are inferred by walking a
    fan-out back to the constant it iterates, so they are a best-effort superset
    — the graph could run these; only a run says which it did. Merging them into
    ``agents`` would let an inference masquerade as a fact."""
    reads_results_of: list[str] = Field(default_factory=list)
    source: SourceSpan | None = None
    snippet: str | None = None
    """RESERVED — see PRD §19 D-16. Spans only in Release 1."""


class TopologyEdge(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    from_: str = Field(alias="from")
    to: str
    event: str
    kind: EdgeKind
    label: str
    arm: int | None = None


class FanOutPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node: str
    target: str
    cap: int


class JoinPoint(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    node: str
    collects: list[str]
    from_: list[str] = Field(alias="from")
    min_success: int | t.Literal["all"] | None = None


class TopologyInput(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    type_name: str
    doc: str | None = None
    schema_: dict[str, t.Any] = Field(default_factory=dict, alias="schema")
    fields: list[FieldDoc] = Field(default_factory=list)


class WorkflowConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeout_sec: int | None = None
    title_template: str | None = None
    """``{field}`` template for naming a run, rendered by the platform from the
    run input. Data rather than code, so no capability Python executes."""


class Topology(BaseModel):
    """The complete compiled document for one workflow."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    topology_version: int = TOPOLOGY_VERSION
    name: str
    capability: str | None = None
    doc: str | None = None
    source: SourceSpan | None = None
    source_sha256: str | None = None
    """Digest of the authored workflow module used to compile this topology."""

    input: TopologyInput
    config: WorkflowConfig = Field(default_factory=WorkflowConfig)

    event_types: dict[str, EventTypeDoc] = Field(default_factory=dict)
    nodes: list[TopologyNode] = Field(default_factory=list)
    edges: list[TopologyEdge] = Field(default_factory=list)

    fan_out_points: list[FanOutPoint] = Field(default_factory=list)
    join_points: list[JoinPoint] = Field(default_factory=list)
    entry: str
    terminals: list[str] = Field(default_factory=list)

    def node(self, key: str) -> TopologyNode:
        for n in self.nodes:
            if n.key == key:
                return n
        raise KeyError(f"no node {key!r} in topology {self.name!r}")

    def successors(self, key: str) -> list[TopologyEdge]:
        return [e for e in self.edges if e.from_ == key]

    def predecessors(self, key: str) -> list[TopologyEdge]:
        return [e for e in self.edges if e.to == key]

    def to_json_dict(self) -> dict[str, t.Any]:
        """Serialize for the OCI config, the database, and the golden file."""
        return self.model_dump(mode="json", by_alias=True, exclude_none=False)
