"""Typed, appliable edits to a workflow Definition.

The platform primitive behind "an agent suggests a workflow fix and the
system applies it" (the recovery advisor's ``edit_workflow`` proposal,
studio one-click repairs). An agent returns a ``DefinitionPatch`` — a flat
list of typed operations — and ``apply_patch`` materializes a NEW
``Definition`` from it, pure and deterministic: no LLM, no DB, no engine.

Gate stack (mirrors matrx-ai's agent-plans loop — every gate runs before
any row is written):

1. ``DefinitionPatch.model_validate`` — the ops are structurally typed.
2. ``apply_patch`` — target nodes/edges/variables must exist; all issues
   are collected and raised together as ``DefinitionPatchError``.
3. The resulting ``Definition`` re-validates through Pydantic (duplicate
   id checks fire here).
4. The CALLER then runs ``validate_definition`` + ``compile_graph`` and
   only persists (``DefinitionStore.save_draft``) when both pass.

Merge semantics for ``update_node_data``: dicts merge recursively, an
explicit ``None`` value DELETES that key, any other value replaces. This
lets an agent both set and unset config without shipping the whole blob.
"""

from __future__ import annotations

import copy
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.placement import place_added_node
from matrx_graph.types.definition import Definition, EdgeDef, NodeDef, Position
from matrx_graph.types.primitives import EdgeKind
from matrx_graph.types.variables import VariableSpec

# The Studio's presentation vocabulary (apps/workflow-studio/src/lib/node-kinds.ts,
# features/canvas/groups.ts): sticky notes and group frames are stored under
# definition.metadata.annotations / metadata.groups, never as engine steps.
ANNOTATION_NODE_TYPE = "annotation"
GROUP_NODE_TYPE = "group"
GROUP_COLORS = ("slate", "blue", "violet", "emerald", "amber")
GROUP_PADDING = 28
GROUP_HEADER_HEIGHT = 36
EDGE_NOTE_MAX_LINES = 3
EDGE_NOTE_MAX_LENGTH = 160


class DefinitionPatchError(ValueError):
    """A patch could not be applied. ``issues`` lists every problem found."""

    def __init__(self, issues: list[str]) -> None:
        self.issues = issues
        super().__init__("; ".join(issues) or "definition patch failed")


class UpdateNodeDataOp(BaseModel):
    """Deep-merge ``data`` into an existing node's ``data`` payload.

    Nested dicts merge recursively; an explicit ``None`` deletes the key;
    scalars/lists replace. ``data.config`` is where node config lives, so
    ``{"config": {"timeout_s": 60}}`` tweaks one config key in place.
    """

    model_config = ConfigDict(extra="forbid")

    op: Literal["update_node_data"] = "update_node_data"
    node_id: str = Field(min_length=1)
    data: dict[str, Any]  # api-any-ok: per-node data whose shape is the node type's own contract


class UpdateNodeTypeOp(BaseModel):
    """Replace an existing node's top-level React Flow renderer type.

    The executable spec remains ``data.spec_type``. Callers changing a node's
    concrete identity generally pair this operation with
    :class:`UpdateNodeDataOp` in the same :class:`DefinitionPatch` so the
    renderer category and executable spec persist atomically.
    """

    model_config = ConfigDict(extra="forbid")

    op: Literal["update_node_type"] = "update_node_type"
    node_id: str = Field(min_length=1)
    type: str = Field(min_length=1, max_length=120)


class AddNodeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_node"] = "add_node"
    node: NodeDef


class RemoveNodeOp(BaseModel):
    """Remove a node. Edges touching it are removed too (a dangling edge
    would fail definition validation anyway — removing them is the only
    coherent outcome)."""

    model_config = ConfigDict(extra="forbid")

    op: Literal["remove_node"] = "remove_node"
    node_id: str = Field(min_length=1)


class AddEdgeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add_edge"] = "add_edge"
    edge: EdgeDef


class ReplaceNodeOp(BaseModel):
    """Replace an existing node WHOLE — type, position and data all become
    what this op carries. The counterpart to ``update_node_data``'s merge:
    use this when the author is restating the node as it should now be, and
    ``update_node_data`` when they are tweaking one key in place.

    The node id must already exist (``add_node`` creates a new one). Edges
    are untouched — replacing a node never re-wires the graph around it.
    """

    model_config = ConfigDict(extra="forbid")

    op: Literal["replace_node"] = "replace_node"
    node: NodeDef


class ReplaceEdgeOp(BaseModel):
    """Replace an existing edge WHOLE (source, target, handles, data).

    The edge id must already exist (``add_edge`` creates a new one).
    """

    model_config = ConfigDict(extra="forbid")

    op: Literal["replace_edge"] = "replace_edge"
    edge: EdgeDef


class RemoveEdgeOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["remove_edge"] = "remove_edge"
    edge_id: str = Field(min_length=1)


class SetVariableOp(BaseModel):
    """Upsert a declared run variable by name."""

    model_config = ConfigDict(extra="forbid")

    op: Literal["set_variable"] = "set_variable"
    variable: VariableSpec


class RemoveVariableOp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["remove_variable"] = "remove_variable"
    name: str = Field(min_length=1)


class MoveNodeOp(BaseModel):
    """Move a step, sticky note or group frame on the canvas (absolute position)."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["move_node"] = "move_node"
    node_id: str
    position: Position


class SetEdgeKindOp(BaseModel):
    """Set an edge's kind (data / control / conditional / error / stream) — edge.data.kind."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["set_edge_kind"] = "set_edge_kind"
    edge_id: str
    kind: EdgeKind


class SetEdgeNoteOp(BaseModel):
    """Set the short note shown on an edge; an empty note removes it — edge.data.note."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["set_edge_note"] = "set_edge_note"
    edge_id: str
    note: str = ""


class UpdateEdgeDataOp(BaseModel):
    """Deep-merge into an edge's data (same merge rules as update_node_data)."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["update_edge_data"] = "update_edge_data"
    edge_id: str
    data: dict[str, Any]


# The smallest note the canvas draws (its resizer's floor); a smaller size is raised to it.
NOTE_MIN_WIDTH = 180
NOTE_MIN_HEIGHT = 100


def _size_note(note: dict[str, Any], width: float | None, height: float | None) -> None:
    """Write a note's size where the canvas reads it: the node box and its style, as a save does."""
    if width is None and height is None:
        return
    def px(value: float, floor: int) -> float | int:
        size = max(float(value), floor)
        return int(size) if size.is_integer() else size

    style = dict(note.get("style") or {})
    if width is not None:
        note["width"] = style["width"] = px(width, NOTE_MIN_WIDTH)
    if height is not None:
        note["height"] = style["height"] = px(height, NOTE_MIN_HEIGHT)
    note["style"] = style


class AddAnnotationOp(BaseModel):
    """Add a sticky note to the canvas (stored in metadata.annotations); size is optional."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["add_annotation"] = "add_annotation"
    annotation_id: str
    position: Position
    text: str
    color: str | None = None
    width: float | None = None
    height: float | None = None


class UpdateAnnotationOp(BaseModel):
    """Change a sticky note's text, color, size or position — any of them, in one op.

    A note with no size grows with its text and can run over what sits below it; giving it a
    size is how an author keeps it clear (2026-10-30: only a whole-draft save could size one).
    """

    model_config = ConfigDict(extra="forbid")
    op: Literal["update_annotation"] = "update_annotation"
    annotation_id: str
    text: str | None = None
    color: str | None = None
    width: float | None = None
    height: float | None = None
    position: Position | None = None


class RemoveAnnotationOp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    op: Literal["remove_annotation"] = "remove_annotation"
    annotation_id: str


class GroupNodesOp(BaseModel):
    """Frame steps in a titled group (stored in metadata.groups, like the Studio's Group)."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["group_nodes"] = "group_nodes"
    group_id: str
    title: str
    node_ids: list[str] = Field(min_length=1)
    color: Literal["slate", "blue", "violet", "emerald", "amber"] = "slate"
    description: str | None = None


class UngroupOp(BaseModel):
    """Remove a group frame; its steps stay where they are."""

    model_config = ConfigDict(extra="forbid")
    op: Literal["ungroup"] = "ungroup"
    group_id: str


class SetResultOp(BaseModel):
    """Declare this workflow's ONE result and what it takes — what a caller
    (``subgraph.call``) reads instead of reaching into its step ids.

    ``node_id`` names the step whose output IS the result: it becomes a
    deliverable marked ``is_primary`` and every other step loses that mark;
    ``None`` clears the mark everywhere. ``output_kind`` / ``input_kind`` are
    the workflow's declaration COLUMNS — the definition carries no copy, so
    the save service writes them from :func:`io_declaration_columns`. Omit a
    field to leave it as it is; send ``None`` to clear it.
    """

    model_config = ConfigDict(extra="forbid")
    op: Literal["set_result"] = "set_result"
    node_id: str | None = None
    output_kind: str | None = None
    input_kind: str | None = None


class SetEntryNodesOp(BaseModel):
    """Set the workflow's starting steps (``Definition.entry_nodes``).

    Every id must name a step in the definition. An empty list clears the
    setting, so the engine derives the starting steps itself (steps with no
    incoming connection).
    """

    model_config = ConfigDict(extra="forbid")
    op: Literal["set_entry_nodes"] = "set_entry_nodes"
    node_ids: list[str]


PatchOp = Annotated[
    SetResultOp
    | SetEntryNodesOp
    | UpdateNodeDataOp
    | UpdateNodeTypeOp
    | AddNodeOp
    | ReplaceNodeOp
    | RemoveNodeOp
    | AddEdgeOp
    | ReplaceEdgeOp
    | RemoveEdgeOp
    | SetVariableOp
    | RemoveVariableOp
    | MoveNodeOp
    | SetEdgeKindOp
    | SetEdgeNoteOp
    | UpdateEdgeDataOp
    | AddAnnotationOp
    | UpdateAnnotationOp
    | RemoveAnnotationOp
    | GroupNodesOp
    | UngroupOp,
    Field(discriminator="op"),
]


class DefinitionPatch(BaseModel):
    """A flat, ordered list of typed edits to one Definition."""

    model_config = ConfigDict(extra="forbid")

    version: Literal["1"] = "1"
    summary: str = Field(
        default="",
        description="One-line human-readable description of what the patch does.",
    )
    ops: list[PatchOp] = Field(min_length=1)


def _deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in patch.items():
        if value is None:
            merged.pop(key, None)
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def apply_patch(definition: Definition, patch: DefinitionPatch) -> Definition:
    """Apply ``patch`` to ``definition``, returning a NEW Definition.

    Pure: the input definition is never mutated. Raises
    ``DefinitionPatchError`` with EVERY problem found (missing targets,
    duplicate additions) rather than stopping at the first — the caller
    surfaces the full list to the user/agent in one round trip.
    """
    raw = definition.model_dump(mode="python")
    nodes: list[dict[str, Any]] = raw.get("nodes", [])
    edges: list[dict[str, Any]] = raw.get("edges", [])
    variables: list[dict[str, Any]] = raw.get("variables", [])
    metadata: dict[str, Any] = dict(raw.get("metadata") or {})
    annotations: list[dict[str, Any]] = list(metadata.get("annotations") or [])
    groups: list[dict[str, Any]] = list(metadata.get("groups") or [])
    issues: list[str] = []

    for i, op in enumerate(patch.ops):
        where = f"ops[{i}] ({op.op})"
        if isinstance(op, SetResultOp):
            if "node_id" not in op.model_fields_set:
                continue
            if op.node_id is not None and not any(n.get("id") == op.node_id for n in nodes):
                issues.append(f"{where}: node '{op.node_id}' not found")
                continue
            for n in nodes:
                data = dict(n.get("data") or {})
                if n.get("id") == op.node_id:
                    data["is_primary"] = True
                    data["deliverable"] = True
                elif data.get("is_primary"):
                    data.pop("is_primary", None)
                n["data"] = data
        elif isinstance(op, SetEntryNodesOp):
            step_ids = {n.get("id") for n in nodes}
            missing = [nid for nid in op.node_ids if nid not in step_ids]
            if missing:
                issues.append(f"{where}: steps not found: {missing}")
                continue
            raw["entry_nodes"] = list(dict.fromkeys(op.node_ids))
        elif isinstance(op, UpdateNodeDataOp):
            target = next((n for n in nodes if n.get("id") == op.node_id), None)
            if target is None:
                issues.append(f"{where}: node '{op.node_id}' not found")
                continue
            target["data"] = _deep_merge(target.get("data") or {}, op.data)
        elif isinstance(op, UpdateNodeTypeOp):
            target = next((n for n in nodes if n.get("id") == op.node_id), None)
            if target is None:
                issues.append(f"{where}: node '{op.node_id}' not found")
                continue
            target["type"] = op.type
        elif isinstance(op, AddNodeOp):
            if any(n.get("id") == op.node.id for n in nodes):
                issues.append(f"{where}: node id '{op.node.id}' already exists")
                continue
            # Never on top of another step: the Studio found every overlap
            # an author's add_node left and flagged the graph stacked on open.
            nodes.append(place_added_node(op.node.model_dump(mode="python"), nodes))
        elif isinstance(op, ReplaceNodeOp):
            index = next((i for i, n in enumerate(nodes) if n.get("id") == op.node.id), None)
            if index is None:
                issues.append(f"{where}: node '{op.node.id}' not found — use add_node to create it")
                continue
            # In place: the author's node order is theirs, not the patch's.
            replaced = op.node.model_dump(mode="python")
            # The workflow's declared result (set_result) is a mark ON the step; restating
            # the step under the same id keeps it unless the restatement says otherwise
            # (dropping it silently made the next publish refuse — 2026-10-27).
            previous = nodes[index].get("data") or {}
            if previous.get("is_primary"):
                data = dict(replaced.get("data") or {})
                data.setdefault("is_primary", True)
                if data["is_primary"] is True:
                    data.setdefault("deliverable", previous.get("deliverable", True))
                replaced["data"] = data
            nodes[index] = replaced
        elif isinstance(op, RemoveNodeOp):
            if not any(n.get("id") == op.node_id for n in nodes):
                issues.append(f"{where}: node '{op.node_id}' not found")
                continue
            nodes[:] = [n for n in nodes if n.get("id") != op.node_id]
            edges[:] = [
                e for e in edges if e.get("source") != op.node_id and e.get("target") != op.node_id
            ]
            # A removed step leaves every group frame that listed it.
            for group in groups:
                data = group.get("data") or {}
                members = data.get("memberIds")
                if isinstance(members, list) and op.node_id in members:
                    group["data"] = {**data, "memberIds": [m for m in members if m != op.node_id]}
        elif isinstance(op, AddEdgeOp):
            if any(e.get("id") == op.edge.id for e in edges):
                issues.append(f"{where}: edge id '{op.edge.id}' already exists")
                continue
            edges.append(op.edge.model_dump(mode="python"))
        elif isinstance(op, ReplaceEdgeOp):
            index = next((i for i, e in enumerate(edges) if e.get("id") == op.edge.id), None)
            if index is None:
                issues.append(f"{where}: edge '{op.edge.id}' not found — use add_edge to create it")
                continue
            edges[index] = op.edge.model_dump(mode="python")
        elif isinstance(op, RemoveEdgeOp):
            if not any(e.get("id") == op.edge_id for e in edges):
                issues.append(f"{where}: edge '{op.edge_id}' not found")
                continue
            edges[:] = [e for e in edges if e.get("id") != op.edge_id]
        elif isinstance(op, SetVariableOp):
            dumped = op.variable.model_dump(mode="python")
            existing = next((v for v in variables if v.get("name") == op.variable.name), None)
            if existing is None:
                variables.append(dumped)
            else:
                existing.update(dumped)
        elif isinstance(op, RemoveVariableOp):
            if not any(v.get("name") == op.name for v in variables):
                issues.append(f"{where}: variable '{op.name}' not found")
                continue
            variables[:] = [v for v in variables if v.get("name") != op.name]
        elif isinstance(op, MoveNodeOp):
            target = next((n for n in [*nodes, *annotations, *groups] if n.get("id") == op.node_id), None)
            if target is None:
                issues.append(f"{where}: node, note or group '{op.node_id}' not found")
                continue
            target["position"] = op.position.model_dump(mode="python")
        elif isinstance(op, SetEdgeKindOp | SetEdgeNoteOp | UpdateEdgeDataOp):
            edge = next((e for e in edges if e.get("id") == op.edge_id), None)
            if edge is None:
                issues.append(f"{where}: edge '{op.edge_id}' not found")
                continue
            data = dict(edge.get("data") or {})
            if isinstance(op, SetEdgeKindOp):
                data["kind"] = op.kind.value
            elif isinstance(op, SetEdgeNoteOp):
                note = "\n".join(op.note.replace("\r\n", "\n").split("\n")[:EDGE_NOTE_MAX_LINES])
                note = note[:EDGE_NOTE_MAX_LENGTH]
                if note.strip():
                    data["note"] = note
                else:
                    data.pop("note", None)
            else:
                data = _deep_merge(data, op.data)
            edge["data"] = data
        elif isinstance(op, AddAnnotationOp):
            if any(x.get("id") == op.annotation_id for x in [*nodes, *annotations, *groups]):
                issues.append(f"{where}: id '{op.annotation_id}' already exists")
                continue
            note_data: dict[str, Any] = {"text": op.text}
            if op.color:
                note_data["color"] = op.color
            added: dict[str, Any] = {
                "id": op.annotation_id,
                "type": ANNOTATION_NODE_TYPE,
                "position": op.position.model_dump(mode="python"),
                "data": note_data,
            }
            _size_note(added, op.width, op.height)
            annotations.append(added)
        elif isinstance(op, UpdateAnnotationOp):
            note = next((a for a in annotations if a.get("id") == op.annotation_id), None)
            if note is None:
                issues.append(f"{where}: note '{op.annotation_id}' not found")
                continue
            note_data = dict(note.get("data") or {})
            if op.text is not None:
                note_data["text"] = op.text
            if op.color is not None:
                note_data["color"] = op.color
            note["data"] = note_data
            _size_note(note, op.width, op.height)
            if op.position is not None:
                note["position"] = op.position.model_dump(mode="python")
        elif isinstance(op, RemoveAnnotationOp):
            if not any(a.get("id") == op.annotation_id for a in annotations):
                issues.append(f"{where}: note '{op.annotation_id}' not found")
                continue
            annotations[:] = [a for a in annotations if a.get("id") != op.annotation_id]
        elif isinstance(op, GroupNodesOp):
            if any(x.get("id") == op.group_id for x in [*nodes, *annotations, *groups]):
                issues.append(f"{where}: id '{op.group_id}' already exists")
                continue
            members = [n for n in nodes if n.get("id") in set(op.node_ids)]
            missing = sorted(set(op.node_ids) - {n.get("id") for n in members})
            if missing:
                issues.append(f"{where}: steps not found: {missing}")
                continue
            claimed = sorted(
                nid for g in groups for nid in ((g.get("data") or {}).get("memberIds") or []) if nid in op.node_ids
            )
            if claimed:
                issues.append(f"{where}: steps already in another group: {claimed} — ungroup them first")
                continue
            xs = [float((n.get("position") or {}).get("x", 0)) for n in members]
            ys = [float((n.get("position") or {}).get("y", 0)) for n in members]
            group_data: dict[str, Any] = {"title": op.title, "color": op.color, "memberIds": list(op.node_ids)}
            if op.description:
                group_data["description"] = op.description
            groups.append(
                {
                    "id": op.group_id,
                    "type": GROUP_NODE_TYPE,
                    # The Studio refits the frame around its members on load.
                    "position": {"x": min(xs) - GROUP_PADDING, "y": min(ys) - GROUP_PADDING - GROUP_HEADER_HEIGHT},
                    "data": group_data,
                }
            )
        elif isinstance(op, UngroupOp):
            if not any(g.get("id") == op.group_id for g in groups):
                issues.append(f"{where}: group '{op.group_id}' not found")
                continue
            groups[:] = [g for g in groups if g.get("id") != op.group_id]

    if issues:
        raise DefinitionPatchError(issues)

    raw["nodes"] = nodes
    raw["edges"] = edges
    raw["variables"] = variables
    if annotations or "annotations" in metadata:
        metadata["annotations"] = annotations
    if groups or "groups" in metadata:
        metadata["groups"] = groups
    if metadata or raw.get("metadata") is not None:
        raw["metadata"] = metadata
    # Entry nodes referencing a removed node would fail compile with a
    # confusing message — prune them here, loudly coherent with RemoveNodeOp.
    node_ids = {n.get("id") for n in nodes}
    if raw.get("entry_nodes"):
        raw["entry_nodes"] = [nid for nid in raw["entry_nodes"] if nid in node_ids]

    try:
        return Definition.model_validate(raw)
    except Exception as exc:  # noqa: BLE001 — re-raise as the one patch error type
        raise DefinitionPatchError([f"patched definition invalid: {exc}"]) from exc


def io_declaration_columns(patch: DefinitionPatch) -> dict[str, str | None]:
    """The workflow-level declaration columns a patch sets (``set_result``'s
    ``output_kind`` / ``input_kind``), last op wins; a field the op omitted is
    absent, so the save leaves that column untouched."""
    columns: dict[str, str | None] = {}
    for op in patch.ops:
        if isinstance(op, SetResultOp):
            for name in ("output_kind", "input_kind"):
                if name in op.model_fields_set:
                    value = getattr(op, name)
                    columns[name] = (value or "").strip() or None
    return columns
