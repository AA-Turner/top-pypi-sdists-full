"""Extract a linear run of steps into its OWN Definition, and rewire the parent
to call it — the engine half of "a reusable packet of steps is just a small
Workflow" (docs/workflow/NOMENCLATURE.md).

Pure and deterministic, exactly like ``patch.py``: no LLM, no DB, no engine.
Given a parent ``Definition`` and the node ids of a contiguous linear run, it
produces

  * the CHILD ``Definition`` (those nodes, their internal edges, the run
    variables they reference), and
  * a ``DefinitionPatch`` that removes the run from the parent, drops one
    ``subgraph.call`` node in its place, and reattaches every edge that
    crossed the boundary.

The caller creates the child row first (it needs an id), then applies the
patch through the normal gate stack (``apply_workflow_patch``) so validate +
compile run before anything is persisted.

## How the data keeps flowing

**Into the child.** ``subgraph.call``'s input model is open
(``extra="allow"``) and every extra top-level key it receives is seeded into
the child run, which broadcasts them to the child's entry node — the exact
payload the run's first step used to receive. So an inbound edge is
reattached **byte-identical**: its field links already name that step's own
input args.

**Out of the child.** ``subgraph.call`` returns the run summary, so the run's
outputs live under ``last_outputs.<terminal node id>``. Each outbound edge's
field links are rewritten SOURCE-side with that prefix (dot-paths are a
source-side feature of edge mappings; ``$FULL_PAYLOAD`` becomes the plain
prefix). ERROR edges are left alone — they address the ``code``/``message``/
``details`` dump, which ``subgraph.call`` raises in its own right when the
child run fails.

Anything that cannot be reproduced faithfully is REFUSED with a named,
actionable issue (an outbound broadcast edge, a branch handle the call node
does not have, an external edge into the middle of the run). Never a silent
approximation of the user's graph.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.patch import (
    AddEdgeOp,
    AddNodeOp,
    DefinitionPatch,
    PatchOp,
    RemoveNodeOp,
)
from matrx_graph.types.definition import Definition, EdgeDef, NodeDef, Position
from matrx_graph.types.primitives import EdgeKind
from matrx_graph.types.variables import iter_var_refs

SUBGRAPH_CALL_SPEC_TYPE = "subgraph.call"
#: React Flow visual category for the sub-workflow card (studio `nodes/index.ts`).
SUBGRAPH_NODE_TYPE = "subgraph"
#: ``subgraph.call`` drains no emissions, so a reattached edge must carry NO
#: handle — a ``sourceHandle`` the node never emits on PRUNES the edge
#: (ENGINE_SPEC §2) and everything downstream would silently stop firing.
_NO_HANDLE = None
#: Source key meaning "the whole upstream payload" (scheduler `_map_edge_payload`).
_WHOLE_PAYLOAD = "$FULL_PAYLOAD"
#: Where a child run's per-node outputs land on ``SubgraphCallOutput``.
_LAST_OUTPUTS = "last_outputs"

MIN_EXTRACT_NODES = 2


class ExtractionRejected(ValueError):
    """The selected steps cannot be extracted faithfully. ``issues`` lists
    EVERY reason (same posture as ``DefinitionPatchError``) so the user sees
    the whole picture in one round trip instead of one-at-a-time."""

    def __init__(self, issues: list[str]) -> None:
        self.issues = issues
        super().__init__("; ".join(issues) or "extraction rejected")


class ExtractionPlan(BaseModel):
    """A verified, appliable extraction. Produced by :func:`plan_extraction`."""

    model_config = ConfigDict(extra="forbid")

    child: Definition = Field(description="The new sub-workflow's definition.")
    node_ids: list[str] = Field(description="The extracted run, in execution order.")
    entry_node_id: str
    terminal_node_id: str
    variables_copied: list[str] = Field(default_factory=list)
    inbound_edge_ids: list[str] = Field(default_factory=list)
    outbound_edge_ids: list[str] = Field(default_factory=list)
    call_node_id: str = Field(description="Id the sub-workflow step will take in the parent.")
    call_position: Position

    # The parent's boundary edges, captured pre-removal so the patch can put
    # them back on the call node. Stored as raw dicts (EdgeDef round-trips).
    inbound_edges: list[EdgeDef] = Field(default_factory=list)
    outbound_edges: list[EdgeDef] = Field(default_factory=list)

    def parent_patch(
        self,
        child_definition_id: str,
        *,
        label: str,
        summary: str = "",
        child_terminal_node_id: str | None = None,
    ) -> DefinitionPatch:
        """The edit that swaps the run for one call of ``child_definition_id``.

        Node removal takes the boundary edges with it (``RemoveNodeOp``
        semantics), so they are re-added against the call node — same edge
        ids, so nothing downstream loses its identity.

        ``child_terminal_node_id`` addresses the run's result inside the CHILD.
        It defaults to this plan's own terminal step, which is right when the
        child was built from this plan — but when several workflows are
        rewired onto ONE shared sub-workflow, only the first one's plan built
        it, and the others must address the child's step ids, not their own.
        Getting this wrong produces a field link that silently never resolves.
        """
        terminal = child_terminal_node_id or self.terminal_node_id
        ops: list[PatchOp] = [RemoveNodeOp(node_id=nid) for nid in self.node_ids]
        ops.append(
            AddNodeOp(
                node=NodeDef(
                    id=self.call_node_id,
                    type=SUBGRAPH_NODE_TYPE,
                    position=self.call_position,
                    data={
                        "spec_type": SUBGRAPH_CALL_SPEC_TYPE,
                        "label": label,
                        "config": {"definition_id": child_definition_id},
                    },
                )
            )
        )
        for edge in self.inbound_edges:
            reattached = edge.model_copy(deep=True)
            reattached.target = self.call_node_id
            reattached.targetHandle = _NO_HANDLE
            ops.append(AddEdgeOp(edge=reattached))
        for edge in self.outbound_edges:
            reattached = edge.model_copy(deep=True)
            reattached.source = self.call_node_id
            reattached.sourceHandle = _NO_HANDLE
            if edge.kind is not EdgeKind.ERROR:
                _rewrite_source_mappings(reattached, terminal)
            ops.append(AddEdgeOp(edge=reattached))
        return DefinitionPatch(
            version="1",
            summary=summary or f"Extract {len(self.node_ids)} steps into '{label}'",
            ops=ops,
        )


def _rewrite_source_mappings(edge: EdgeDef, terminal_node_id: str) -> None:
    """Re-address an outbound edge's field links at the child run's output.

    ``{"row_id": "result.row_id"}`` becomes
    ``{"row_id": "last_outputs.<terminal>.result.row_id"}``; ``$FULL_PAYLOAD``
    becomes ``last_outputs.<terminal>`` (the whole terminal step's output).
    """
    mappings = edge.mappings
    if mappings is None:
        return
    prefix = f"{_LAST_OUTPUTS}.{terminal_node_id}"
    edge.data["mappings"] = {
        target_key: (prefix if source_key == _WHOLE_PAYLOAD else f"{prefix}.{source_key}")
        for target_key, source_key in mappings.items()
    }


def _order_run(
    node_ids: list[str], internal_edges: list[EdgeDef], issues: list[str]
) -> tuple[str, str, list[str]] | None:
    """Verify the selection is ONE simple path and return (entry, terminal, order).

    A fan-out, a fan-in, a cycle, or two disconnected pieces is not a run —
    naming which node broke it is what makes the refusal actionable.
    """
    selected = set(node_ids)
    out: dict[str, list[str]] = {}
    inc: dict[str, list[str]] = {}
    for edge in internal_edges:
        out.setdefault(edge.source, []).append(edge.target)
        inc.setdefault(edge.target, []).append(edge.source)

    for nid in sorted(selected):
        if len(out.get(nid, [])) > 1:
            issues.append(
                f"step '{nid}' branches to "
                f"{len(out[nid])} other selected steps — a reusable workflow is "
                "extracted from a single straight run of steps, not a branch."
            )
        if len(inc.get(nid, [])) > 1:
            issues.append(
                f"step '{nid}' is joined by {len(inc[nid])} other selected steps — "
                "a reusable workflow is extracted from a single straight run of "
                "steps, not a join."
            )
    if issues:
        return None

    starts = [nid for nid in selected if not inc.get(nid)]
    ends = [nid for nid in selected if not out.get(nid)]
    if len(starts) != 1 or len(ends) != 1:
        issues.append(
            "the selected steps are not one connected run "
            f"({len(starts)} starting step(s), {len(ends)} ending step(s)) — "
            "select steps that follow one another end to end."
        )
        return None

    entry, terminal = starts[0], ends[0]
    order = [entry]
    cursor = entry
    while out.get(cursor):
        nxt = out[cursor][0]
        if nxt in order:
            issues.append(f"the selected steps loop back on themselves at '{nxt}'.")
            return None
        order.append(nxt)
        cursor = nxt
    if len(order) != len(selected):
        missing = sorted(selected - set(order))
        issues.append(
            "the selected steps are not all connected — "
            f"{', '.join(missing)} cannot be reached from '{entry}'."
        )
        return None
    return entry, terminal, order


def plan_extraction(
    definition: Definition,
    *,
    node_ids: list[str],
    call_node_id: str | None = None,
) -> ExtractionPlan:
    """Verify that ``node_ids`` form an extractable run and build the plan.

    Raises :class:`ExtractionRejected` with every problem found. The parent
    definition is never mutated.
    """
    issues: list[str] = []
    selected_ids = list(dict.fromkeys(node_ids))
    if len(selected_ids) != len(node_ids):
        issues.append("the same step was selected more than once.")
    if len(selected_ids) < MIN_EXTRACT_NODES:
        issues.append(
            f"select at least {MIN_EXTRACT_NODES} steps to extract into a reusable workflow."
        )
    by_id = {n.id: n for n in definition.nodes}
    missing = [nid for nid in selected_ids if nid not in by_id]
    if missing:
        issues.append(
            f"step(s) {', '.join(sorted(missing))} are no longer in this "
            "workflow — it changed since this suggestion was made."
        )
    if issues:
        raise ExtractionRejected(issues)

    selected = set(selected_ids)
    entry_pinned = [nid for nid in definition.entry_nodes if nid in selected]
    if entry_pinned:
        issues.append(
            f"this workflow pins its starting step(s) to "
            f"{', '.join(sorted(entry_pinned))}, which the extraction would "
            "remove. Clear the pinned start first."
        )

    internal: list[EdgeDef] = []
    inbound: list[EdgeDef] = []
    outbound: list[EdgeDef] = []
    for edge in definition.edges:
        src_in, tgt_in = edge.source in selected, edge.target in selected
        if src_in and tgt_in:
            internal.append(edge)
        elif tgt_in:
            inbound.append(edge)
        elif src_in:
            outbound.append(edge)

    ordered = _order_run(selected_ids, internal, issues)
    if ordered is None:
        raise ExtractionRejected(issues)
    entry_id, terminal_id, order = ordered

    if "." in terminal_id:
        issues.append(
            f"the last selected step's id ('{terminal_id}') contains a dot, "
            "which cannot be addressed in a field link — rename that step's "
            "id before extracting."
        )

    for edge in inbound:
        if edge.target != entry_id:
            issues.append(
                f"connection '{edge.id}' feeds '{edge.target}' in the MIDDLE of "
                "the selection — only the first selected step may take input "
                "from outside."
            )
    for edge in outbound:
        if edge.source != terminal_id:
            issues.append(
                f"connection '{edge.id}' leaves '{edge.source}' in the MIDDLE of "
                "the selection — only the last selected step may send output "
                "onward."
            )
            continue
        if edge.sourceHandle is not None:
            issues.append(
                f"connection '{edge.id}' leaves '{edge.source}' on the specific "
                f"output '{edge.sourceHandle}' (one branch of that step). A "
                "sub-workflow step has one plain output, so that branch cannot "
                "be reproduced — extract a run that ends on a step without "
                "branching outputs."
            )
        if edge.kind is EdgeKind.CONDITIONAL and edge.condition:
            issues.append(
                f"connection '{edge.id}' only fires when a condition on "
                f"'{edge.source}' holds ({edge.condition!r}). That condition "
                "reads the step's own result, which a sub-workflow step "
                "reports differently — move the condition off the last "
                "selected step before extracting."
            )
        if edge.kind is EdgeKind.STREAM:
            issues.append(
                f"connection '{edge.id}' carries a live stream, which a "
                "sub-workflow step does not emit."
            )
        if edge.kind in (EdgeKind.DATA, EdgeKind.CONDITIONAL) and edge.mappings is None:
            issues.append(
                f"connection '{edge.id}' passes the whole result of "
                f"'{edge.source}' onward with no field links, so the extraction "
                "cannot tell which fields the next step needs. Add field links "
                "on that connection, then extract."
            )
    if issues:
        raise ExtractionRejected(issues)

    child = _build_child(definition, order, internal)
    positions = [by_id[nid].position for nid in order]
    call_position = Position(
        x=sum(p.x for p in positions) / len(positions),
        y=sum(p.y for p in positions) / len(positions),
    )
    return ExtractionPlan(
        child=child,
        node_ids=order,
        entry_node_id=entry_id,
        terminal_node_id=terminal_id,
        variables_copied=[v.name for v in child.variables],
        inbound_edge_ids=[e.id for e in inbound],
        outbound_edge_ids=[e.id for e in outbound],
        call_node_id=call_node_id or _mint_call_node_id(by_id),
        call_position=call_position,
        inbound_edges=[e.model_copy(deep=True) for e in inbound],
        outbound_edges=[e.model_copy(deep=True) for e in outbound],
    )


def _mint_call_node_id(existing: dict[str, NodeDef]) -> str:
    base = "sub_workflow"
    if base not in existing:
        return base
    index = 2
    while f"{base}_{index}" in existing:
        index += 1
    return f"{base}_{index}"


def _build_child(parent: Definition, order: list[str], internal: list[EdgeDef]) -> Definition:
    """The extracted run as a standalone Definition.

    Node ids are PRESERVED — the parent addresses the run's result as
    ``last_outputs.<terminal id>``, and keeping ids stable also keeps any
    recorded sample data recognizable. Positions are translated to the
    canvas origin so the new workflow opens framed rather than off-screen.
    """
    by_id = {n.id: n for n in parent.nodes}
    picked = [by_id[nid] for nid in order]
    min_x = min(n.position.x for n in picked)
    min_y = min(n.position.y for n in picked)

    nodes: list[NodeDef] = []
    for node in picked:
        clone = node.model_copy(deep=True)
        clone.position = Position(x=node.position.x - min_x, y=node.position.y - min_y)
        nodes.append(clone)

    referenced: set[str] = set()
    for node in nodes:
        referenced.update(name for _, name in iter_var_refs(node.data))
    variables = [v.model_copy(deep=True) for v in parent.variables if v.name in referenced]

    return Definition(
        version="1",
        nodes=nodes,
        edges=[e.model_copy(deep=True) for e in internal],
        channels=[c.model_copy(deep=True) for c in parent.channels],
        strict_channels=parent.strict_channels,
        entry_nodes=[order[0]],
        variables=variables,
        metadata={},
    )


__all__ = [
    "SUBGRAPH_CALL_SPEC_TYPE",
    "ExtractionPlan",
    "ExtractionRejected",
    "plan_extraction",
]
