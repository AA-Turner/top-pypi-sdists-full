"""GRAPH_OP stream event: the one wire vocabulary for edits to any graph.

One vocabulary for every graph kind (workflow, orchestra, org chart, topical
map, map, agent graph, board). A person's save, an agent's tool call and
another tab's change are all the same ``GraphOpEvent`` with a ``phase``
(proposed -> applied -> committed, or rejected).

Where the pieces live (the dependency direction forces it): ``matrx-graph``
depends on this package, so the wire models live here and ``matrx-graph``
imports them. The generic ops below cover the graph shape shared by every
kind (nodes with a ``parentId``, edges with a kind). The workflow-only ops
(variables, result, entry nodes, edge kind/note/data) are declared here at
wire level only; their APPLY semantics are ``matrx_graph.patch`` classes, and
``matrx-graph``'s tests prove every workflow patch op name is in this union.

Types only; the emitter method is ``Emitter.send_graph_op`` (every emitter implements it).
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_serializer

GraphKind = Literal["workflow", "orchestra", "org_chart", "hr_org_chart", "records_org", "topical_map", "map", "agent_graph", "board"]
GraphOpPhase = Literal["proposed", "applied", "committed", "rejected"]
GraphActorKind = Literal["agent", "person"]
GraphEdgeKind = Literal["data", "control", "conditional", "error", "stream", "relation"]
GraphRelationKind = Literal["contains", "relates", "reports_to", "hands_off", "dotted", "origin"]


class GraphPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: float
    y: float


class GraphNodeData(BaseModel):
    """Node payload. ``spec_type`` names the node type (``info.note``, ``agent.run``...) when the
    node's ``type`` is a visual category; absent, the node's ``type`` IS the spec type. That is the
    engine's own rule (matrx-graph ``NodeDef.spec_type``) and both shapes are real stored nodes, so
    the wire carries both exactly as stored, never a filled-in copy that could later shadow ``type``."""

    model_config = ConfigDict(extra="allow")

    spec_type: str | None = Field(default=None, min_length=1)

    @model_serializer(mode="wrap")
    def _omit_absent_spec_type(self, handler: Any) -> dict[str, Any]:
        out = handler(self)
        if out.get("spec_type") is None:
            out.pop("spec_type", None)
        return out


class GraphNode(BaseModel):
    """A node in the shared graph document shape (CONTRACTS section 1)."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1)
    type: str = Field(min_length=1)
    position: GraphPoint
    parentId: str | None = Field(default=None, description="Frame that contains this node.")  # noqa: N815 - wire name
    width: float | None = None
    height: float | None = None
    style: dict[str, Any] | None = None  # api-any-ok: renderer style bag, shape is the canvas's own
    data: GraphNodeData


class GraphEdgeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    kind: GraphEdgeKind
    relation: GraphRelationKind | None = None
    condition: Any | None = None  # api-any-ok: predicate shape is the edge kind's own contract
    mappings: Any | None = None  # api-any-ok: mapping shape is the edge kind's own contract
    note: str | None = None


class GraphEdge(BaseModel):
    """An edge in the shared graph document shape (CONTRACTS section 1)."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    sourceHandle: str | None = None  # noqa: N815 - wire name
    targetHandle: str | None = None  # noqa: N815 - wire name
    type: str | None = None
    data: GraphEdgeData


# --- generic ops (every graph kind) ---------------------------------------------------------


class GraphAddNodeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["add_node"]
    node: GraphNode


class GraphRemoveNodeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["remove_node"]
    node_id: str = Field(min_length=1)


class GraphReplaceNodeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["replace_node"]
    node: GraphNode


class GraphUpdateNodeDataOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["update_node_data"]
    node_id: str = Field(min_length=1)
    data: dict[str, Any]  # api-any-ok: merged into the node type's own data contract


class GraphUpdateNodeTypeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["update_node_type"]
    node_id: str = Field(min_length=1)
    type: str = Field(min_length=1)


class GraphMoveNodeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["move_node"]
    node_id: str = Field(min_length=1)
    position: GraphPoint


class GraphSetParentOp(BaseModel):
    """Put a node inside a frame (``parent_id``) or take it out (``None``)."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["set_parent"]
    node_id: str = Field(min_length=1)
    parent_id: str | None = None


class GraphAddEdgeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["add_edge"]
    edge: GraphEdge


class GraphRemoveEdgeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["remove_edge"]
    edge_id: str = Field(min_length=1)


class GraphReplaceEdgeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["replace_edge"]
    edge: GraphEdge


class GraphSetEdgeKindOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["set_edge_kind"]
    edge_id: str = Field(min_length=1)
    kind: GraphEdgeKind


class GraphSetEdgeNoteOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["set_edge_note"]
    edge_id: str = Field(min_length=1)
    note: str = ""


class GraphUpdateEdgeDataOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["update_edge_data"]
    edge_id: str = Field(min_length=1)
    data: dict[str, Any]  # api-any-ok: merged into the edge kind's own data contract


# --- workflow-only ops (wire level; apply semantics live in matrx_graph.patch) ----------------


class GraphSetVariableOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["set_variable"]
    variable: dict[str, Any]  # api-any-ok: the declared-input shape is matrx_graph's VariableDefinition


class GraphRemoveVariableOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["remove_variable"]
    name: str = Field(min_length=1)


class GraphSetResultOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["set_result"]
    node_id: str | None = None
    output_kind: str | None = None
    input_kind: str | None = None


class GraphSetEntryNodesOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["set_entry_nodes"]
    node_ids: list[str]


class GraphSetWorkflowSettingOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["set_workflow_setting"]
    key: str = Field(min_length=1)
    value: str | None = None


class GraphDescribeWorkflowOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["describe_workflow"]
    name: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=4000)


GraphOp = Annotated[
    GraphAddNodeOp
    | GraphRemoveNodeOp
    | GraphReplaceNodeOp
    | GraphUpdateNodeDataOp
    | GraphUpdateNodeTypeOp
    | GraphMoveNodeOp
    | GraphSetParentOp
    | GraphAddEdgeOp
    | GraphRemoveEdgeOp
    | GraphReplaceEdgeOp
    | GraphSetEdgeKindOp
    | GraphSetEdgeNoteOp
    | GraphUpdateEdgeDataOp
    | GraphSetVariableOp
    | GraphRemoveVariableOp
    | GraphSetResultOp
    | GraphSetEntryNodesOp
    | GraphSetWorkflowSettingOp
    | GraphDescribeWorkflowOp,
    Field(discriminator="op"),
]
"""Every op a GRAPH_OP event can carry, discriminated by ``op``."""


# --- the event payload ------------------------------------------------------------------------


class GraphRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: GraphKind
    id: str = Field(min_length=1)


class GraphOpActor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: GraphActorKind
    id: str = Field(min_length=1)
    label: str
    conversation_id: str | None = None


class GraphOpEvent(BaseModel):
    """Payload of the ``graph_op`` stream event (CONTRACTS section 3).

    Per ``graph.id`` ``seq`` is monotonic. ``proposed`` renders as a pending change,
    ``applied`` as solid, ``committed`` reconciles to ``version``, ``rejected`` rolls
    the batch back (``reason`` ``"abandoned"`` = the turn ended without a commit).
    """

    model_config = ConfigDict(extra="forbid")

    graph: GraphRef
    op_id: str = Field(min_length=1)
    seq: int = Field(ge=0)
    batch_id: str = Field(min_length=1, description="One tool call or one person action.")
    phase: GraphOpPhase
    base_version: int | None = None
    version: int | None = Field(default=None, description="Committed carries the new version.")
    op: GraphOp | None = Field(default=None, description="Present on proposed and applied.")
    reason: str | None = Field(default=None, description="Why a batch was rejected.")
    actor: GraphOpActor
    label: str = Field(max_length=60, description='e.g. "Add step 3 · Summarize".')
    intent_id: str | None = Field(default=None, description="The plan step this op belongs to.")
