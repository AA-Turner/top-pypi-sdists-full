"""Wiring the Kind Availability Index to a real workflow and the live registry.

``availability`` is pure by design — it takes declarations and a schema
resolver and touches nothing. This module is the impure half: it reads a
``Definition`` (what the designer is editing, possibly unsaved and invalid) or
a ``CompiledGraph`` (what will actually run), turns it into declarations, and
feeds the index from the LIVE kind catalog (``matrx_graph.kinds``).

WHY THE INDEX STAYS SYNC WHEN THE CATALOG IS ASYNC
--------------------------------------------------
``resolve_kind`` is async and cached. The index walk is recursive and
discovers which kinds it needs AS IT GOES — a nested kind is only known once
its parent's schema has been read. Making the walk async would push a database
call into every level of a recursive schema walk, and make the primitive
unusable from the compiler and from any sync caller.

So resolution is a FIXED-POINT PREFETCH instead: build with what we have, read
``unresolved_kinds`` (which the index already reports loudly), fetch exactly
those, rebuild. Each pass discovers at most one more level of nesting, so it
converges in at most ``MAX_NESTING_DEPTH + 1`` passes and normally in two. The
index stays pure, the catalog stays async, and neither has to know about the
other.

WHAT COUNTS AS "CONSUMES"
-------------------------
The used/unused split — the picker's default view — needs to know which kinds
are already spoken for. Three sources, all of them declarations the author
already made:

* a node's declared ``input_kind``;
* a kind-filtered edge's ``kind_filter`` (that edge exists precisely to consume
  that kind);
* a kind-triggered node's ``trigger_kind`` (it consumes it by definition).

A value referenced by ACCESSOR is also consumed — but accessor selections live
in node config, whose shape is node-specific, so they are collected by the
caller and passed in via ``extra_consumed``. The API layer does exactly that.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from matrx_graph.content_ir.availability import (
    MAX_NESTING_DEPTH,
    KindAvailabilityIndex,
    NodeKindDeclaration,
    build_availability_index,
)
from matrx_graph.content_ir.edge_routing import parse_edge_routing
from matrx_graph.content_ir.triggers import parse_node_trigger
from matrx_graph.types.compiled import CompiledGraph
from matrx_graph.types.definition import Definition
from matrx_graph.types.primitives import EdgeKind

__all__ = [
    "declarations_from_definition",
    "declarations_from_compiled",
    "build_index_for_definition",
    "build_index_for_declarations",
]

_FLOW_EDGE_KINDS = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL)


def _spec_kinds(spec_type: str, registry: Any) -> tuple[str | None, str | None]:
    """The registered NodeSpec's declared (input_kind, output_kind).

    A node type the registry does not know is not an error here: the designer
    routinely holds a definition with an unregistered node while editing, and
    the picker must keep working around it. Compilation is where an unknown
    type is fatal.
    """
    if registry is None:
        return None, None
    try:
        executor = registry.get(spec_type)
    except Exception:  # noqa: BLE001 — unknown type is normal at design time
        return None, None
    spec = getattr(executor, "spec", None)
    return getattr(spec, "input_kind", None), getattr(spec, "output_kind", None)


def _step_order(node_ids: list[str], edges: list[tuple[str, str]]) -> dict[str, int]:
    """Kahn layering — the same "which step runs first" answer compilation makes.

    Order is what lets the picker refuse to offer a node a value produced after
    it runs. A node inside a cycle gets NO step (``None``), which the index
    reads as "makes no ordering claim" — never as "runs first".
    """
    in_degree: dict[str, int] = dict.fromkeys(node_ids, 0)
    outgoing: dict[str, list[str]] = defaultdict(list)
    for source, target in edges:
        if source in in_degree and target in in_degree:
            in_degree[target] += 1
            outgoing[source].append(target)

    order: dict[str, int] = {}
    frontier = sorted(nid for nid, degree in in_degree.items() if degree == 0)
    layer = 1
    while frontier:
        for node_id in frontier:
            order[node_id] = layer
        nxt: list[str] = []
        for node_id in frontier:
            for target in outgoing.get(node_id, ()):
                in_degree[target] -= 1
                if in_degree[target] == 0:
                    nxt.append(target)
        frontier = sorted(nxt)
        layer += 1
    return order


def declarations_from_definition(
    definition: Definition, registry: Any = None
) -> list[NodeKindDeclaration]:
    """Turn an authored definition into index declarations."""
    flow_edges = [
        (edge.source, edge.target) for edge in definition.edges if edge.kind in _FLOW_EDGE_KINDS
    ]
    order = _step_order([n.id for n in definition.nodes], flow_edges)

    consumed_by_node: dict[str, set[str]] = defaultdict(set)
    for edge in definition.edges:
        try:
            routing = parse_edge_routing(edge.data)
        except ValueError:
            # A malformed routing declaration is a compile-time error the
            # studio already shows. The picker must not die on a definition
            # that is mid-edit.
            continue
        if routing.kind_filter:
            consumed_by_node[edge.target].add(routing.kind_filter)

    declarations: list[NodeKindDeclaration] = []
    for node in definition.nodes:
        spec_input, spec_output = _spec_kinds(node.spec_type, registry)
        raw_input = node.data.get("input_kind")
        raw_output = node.data.get("output_kind")
        input_kind = (
            raw_input.strip() if isinstance(raw_input, str) and raw_input.strip() else spec_input
        )
        output_kind = (
            raw_output.strip()
            if isinstance(raw_output, str) and raw_output.strip()
            else spec_output
        )

        consumes = set(consumed_by_node.get(node.id, ()))
        if input_kind:
            consumes.add(input_kind)
        trigger = parse_node_trigger(node.data)
        if trigger is not None:
            consumes.add(trigger.kind)

        declarations.append(
            NodeKindDeclaration(
                node_id=node.id,
                label=node.label or node.id,
                output_kind=output_kind,
                consumes=tuple(sorted(consumes)),
                # A trigger node is outside the flow: it makes no ordering
                # claim, so everything in the run is available to it — which is
                # exactly what "fires wherever the kind appears" means.
                step=None if trigger is not None else order.get(node.id),
            )
        )
    return declarations


def declarations_from_compiled(graph: CompiledGraph) -> list[NodeKindDeclaration]:
    """Turn a compiled graph into index declarations (the runtime truth)."""
    step_of: dict[str, int] = {}
    for index, layer in enumerate(graph.topological_layers, start=1):
        for node_id in layer:
            step_of[node_id] = index

    consumed_by_node: dict[str, set[str]] = defaultdict(set)
    for edge in graph.edges.values():
        if edge.kind_filter:
            consumed_by_node[edge.target_node_id].add(edge.kind_filter)

    declarations: list[NodeKindDeclaration] = []
    for node_id, node in graph.nodes.items():
        consumes = set(consumed_by_node.get(node_id, ()))
        if node.input_kind:
            consumes.add(node.input_kind)
        if node.trigger_kind:
            consumes.add(node.trigger_kind)
        declarations.append(
            NodeKindDeclaration(
                node_id=node_id,
                label=node_id,
                output_kind=node.output_kind,
                consumes=tuple(sorted(consumes)),
                step=None if node.trigger_kind else step_of.get(node_id),
            )
        )
    return declarations


async def build_index_for_declarations(
    declarations: list[NodeKindDeclaration],
    *,
    extra_consumed: set[str] | None = None,
    max_depth: int = MAX_NESTING_DEPTH,
) -> KindAvailabilityIndex:
    """Build the index against the LIVE kind catalog (fixed-point prefetch).

    ``extra_consumed`` marks kinds the caller knows are already used but that
    the definition does not declare — today, accessor selections read out of
    node config. They fold into the used/unused split so the picker's default
    view stays honest.
    """
    from matrx_graph.kinds import resolve_kind, resolve_kind_edges

    if extra_consumed:
        declarations = [
            d.model_copy(update={"consumes": tuple(sorted(set(d.consumes) | extra_consumed))})
            for d in declarations
        ]

    schemas: dict[str, dict[str, Any] | None] = {}
    edges: dict[str, tuple[tuple[str, str], ...]] = {}

    async def _fetch(slugs: set[str]) -> set[str]:
        """Resolve a wave of slugs; return every child slug their edges name."""
        children: set[str] = set()
        for slug in sorted(slugs):
            if slug in schemas:
                children.update(child for _field, child in edges.get(slug, ()))
                continue
            entry, _reason = await resolve_kind(slug)
            # A degraded resolution stores None, which the index reports as
            # unresolved — a loud "the world is incomplete", never a silent
            # omission and never a retry storm (the catalog caches its own
            # misses; only ``catalog_unreachable`` stays uncached, which is
            # correct: an outage must recover immediately).
            schemas[slug] = entry.json_schema if entry is not None else None
            declared = await resolve_kind_edges(slug)
            edges[slug] = declared
            children.update(child for _field, child in declared)
        return children

    frontier = {d.output_kind for d in declarations if d.output_kind}
    # Composition edges name children the SCHEMA never mentions, so the
    # prefetch must follow them too — otherwise the index would discover a
    # declared child and have no schema for it, reporting a real kind as
    # unresolved. Bounded by the same depth cap as the walk.
    for _pass in range(max_depth + 1):
        discovered = await _fetch(frontier)
        frontier = {slug for slug in discovered if slug not in schemas}
        if not frontier:
            break

    def _resolve_edges(slug: str) -> tuple[tuple[str, str], ...]:
        return edges.get(slug, ())

    index = build_availability_index(
        declarations, schemas.get, resolve_edges=_resolve_edges, max_depth=max_depth
    )
    for _pass in range(max_depth + 1):
        missing = {slug for slug in index.unresolved_kinds if slug not in schemas}
        if not missing:
            break
        await _fetch(missing)
        index = build_availability_index(
            declarations, schemas.get, resolve_edges=_resolve_edges, max_depth=max_depth
        )
    return index


async def build_index_for_definition(
    definition: Definition,
    *,
    registry: Any = None,
    extra_consumed: set[str] | None = None,
) -> KindAvailabilityIndex:
    """The designer-facing entry point: an authored definition -> the index."""
    return await build_index_for_declarations(
        declarations_from_definition(definition, registry),
        extra_consumed=extra_consumed,
    )
