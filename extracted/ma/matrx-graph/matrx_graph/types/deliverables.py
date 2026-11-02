"""THE deliverable rule — ONE implementation, every consumer.

SPEC-workflow-ui-contract §2.2/§2.3. Which nodes of a workflow are its
DELIVERABLES is asked in two places that must never be allowed to disagree:

* ``GET /workflows/{id}/result-schema`` — what a run PROMISES to produce,
  served before any run exists so result surfaces reserve their kind slots.
* ``DefinitionStore.publish`` — the validator that refuses a publish whose
  declared ``output_kind`` is not one of them.

A second copy of this rule is a defect by construction: the endpoint would
advertise a contract the validator does not enforce. Both call
:func:`compute_deliverables`; the publish gate additionally calls
:func:`resolve_io_declaration`.

The rule itself, in order:

1. If the graph holds ≥1 ``output.*`` node, that set IS the declaration —
   terminality is irrelevant, a mid-run showcase is still a deliverable.
2. Otherwise: every terminal node (no outgoing edges) declaring a non-null
   ``CompiledNode.output_kind`` — never a dispatcher (``DISPATCHER_NODE_TYPES``),
   whose work continues at its Send target and whose output is a receipt.
3. ``node.data.deliverable: true|false`` overrides membership either way.

With exactly ONE deliverable, its kind is the workflow's ``output_kind``
(the same inference ``run_result`` applies). With several and no author
declaration, the workflow's ``output_kind`` stays NULL — meaning "the run's
shape IS the collection, read ``run_result.outputs``". We never mint a
wrapper kind to fill that hole.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from matrx_graph.types.compiled import CompiledGraph
from matrx_graph.types.definition import Definition

__all__ = [
    "Deliverable",
    "IoDeclarationVerdict",
    "claim_kind_value",
    "compute_deliverables",
    "declared_result",
    "deliverable_node_ids",
    "resolve_io_declaration",
]


class Deliverable(BaseModel):
    """One declared deliverable of a workflow (SPEC §2.2/§2.4): an
    ``output.*`` node, or a terminal node declaring an output kind, with
    ``node.data.deliverable: true|false`` overriding membership either way."""

    model_config = {"extra": "allow"}

    node_id: str
    title: str
    output_kind: str | None = None
    json_schema: dict[str, Any] = Field(  # api-any-ok: the node's declared output schema
        default_factory=dict
    )
    presentation: str = "panel"
    is_primary: bool = False


def deliverable_node_ids(graph: CompiledGraph, overrides: dict[str, bool] | None = None) -> list[str]:
    """THE membership half of the rule (module docstring), from the compiled graph alone.

    :func:`compute_deliverables` calls it with the definition's ``data.deliverable`` flags; the
    scheduler calls it with none and reads the same flags off ``CompiledNode.deliverable``
    (the compiler copies them), so the run-end check and the publish gate never disagree.
    """
    if overrides is None:
        overrides = {
            nid: node.deliverable
            for nid, node in graph.nodes.items()
            if isinstance(node.deliverable, bool)
        }
    output_ids = [nid for nid, n in graph.nodes.items() if n.spec_type.startswith("output.")]
    if output_ids:
        member_ids = output_ids
    else:
        # A dispatcher (map / send / loop / work queue) hands its work to its
        # target by Send, not by an edge, so it can look terminal — but its own
        # output is only a dispatch receipt, never the workflow's answer
        # (2026-10-27: a fan-out's `map_result` was backfilled as a unit's
        # result and every caller received `{"dispatched": 3}`).
        member_ids = [
            node_id
            for node_id, compiled in graph.nodes.items()
            if not compiled.outgoing_edge_ids
            and compiled.output_kind
            and not _is_dispatcher(compiled.spec_type)
        ]
    members = [nid for nid in member_ids if overrides.get(nid, True)]
    members += [
        nid for nid, flag in overrides.items() if flag and nid not in members and nid in graph.nodes
    ]
    return members


def compute_deliverables(graph: CompiledGraph, definition: Definition) -> list[Deliverable]:
    """THE deliverable set of a workflow — the one rule, see module docstring.

    ``is_primary`` is set here ONLY for the unambiguous single-deliverable
    case; the declaration-aware primary (a declared ``output_kind`` picking
    one of several) is applied by :func:`resolve_io_declaration`, so the
    membership rule stays free of the declaration it is used to validate.
    """
    overrides: dict[str, bool] = {}
    for node in definition.nodes:
        flag = node.data.get("deliverable")
        if isinstance(flag, bool):
            overrides[node.id] = flag
    members = deliverable_node_ids(graph, overrides)

    deliverables: list[Deliverable] = []
    for nid in members:
        compiled = graph.nodes.get(nid)
        if compiled is None:
            continue
        node = next((n for n in definition.nodes if n.id == nid), None)
        cfg = node.config if node is not None else {}
        title = (
            (cfg.get("title") if isinstance(cfg.get("title"), str) else None)
            or compiled.label
            or nid
        )
        presentation = cfg.get("presentation") if isinstance(cfg.get("presentation"), str) else None
        schema: dict[str, Any] = dict(compiled.effective_output_schema or {})
        if not schema:
            schema = _spec_output_schema(compiled.spec_type)
        deliverables.append(
            Deliverable(
                node_id=nid,
                title=str(title),
                output_kind=compiled.output_kind,
                json_schema=schema,
                presentation=presentation or "panel",
                is_primary=bool(node.data.get("is_primary")) if node is not None else False,
            )
        )
    if len(deliverables) == 1 and not deliverables[0].is_primary:
        deliverables[0].is_primary = True
    return deliverables


def _titles(deliverables: list[Deliverable]) -> str:
    """The results named the way the AUTHOR named them, never by node id.

    🚨 FIX-Q5. Every sentence in this module is read by a workflow author — on
    the publish gate, on a Mandate's Holder screen, and in a run's refusal. A
    node id is an internal address: `emit_quiz` is not what the person typed
    into the step's title, and `data.is_primary=true` is a JSON field nobody
    has a control for. Titles fall back to the id only when a step has no
    title at all, which is the one case where the id IS what the screen shows.
    """
    return ", ".join(f"'{d.title}'" for d in deliverables) or "none"


def _spec_output_schema(spec_type: str) -> dict[str, Any]:
    """The node spec's declared output schema, or ``{}``. A registry miss
    never breaks a served schema or a publish — the deliverable is still a
    deliverable, it just has no shape to advertise."""
    try:
        from matrx_graph.executor.registry import default_registry

        from matrx_graph.shape_probe import model_json_schema

        return dict(model_json_schema(default_registry().get(spec_type).spec.output_schema))
    except Exception:  # noqa: BLE001 — a schema miss is never fatal here
        return {}


class IoDeclarationVerdict(BaseModel):
    """The publish gate's answer (SPEC §2.3), and the endpoint's precedence
    answer (§2.4). ``error`` non-None means the publish is REFUSED."""

    model_config = {"extra": "allow"}

    #: The kind to store / serve after the rule ran. May differ from the
    #: author's declaration ONLY by backfill (declaration was None).
    output_kind: str | None = None
    input_kind: str | None = None
    #: True when ``output_kind`` was derived rather than author-declared —
    #: the server BACKFILLS the column in that case (§2.3).
    output_kind_backfilled: bool = False
    #: True when ``input_kind`` was DERIVED from the entry nodes because the
    #: author declared none. Derivation is a serving fallback only: unlike
    #: ``output_kind`` it is never written back, because a NULL input_kind
    #: carries its own meaning — "collected via the run form" (§2.3).
    input_kind_derived: bool = False
    #: Set when the declaration contradicts the graph. Names the mismatch.
    error: str | None = None
    deliverables: list[Deliverable] = Field(default_factory=list)


def resolve_io_declaration(
    graph: CompiledGraph,
    definition: Definition,
    *,
    declared_output_kind: str | None = None,
    declared_input_kind: str | None = None,
) -> IoDeclarationVerdict:
    """SPEC §2.3 — validate an author's IO declaration against the graph.

    ``output_kind``: must be a member of ``{deliverable.output_kind}`` or the
    publish is refused naming the mismatch. No declaration + exactly one
    deliverable → BACKFILL from it. No declaration + multiple deliverables →
    stays NULL (the collection answer, never a wrapper kind).

    ``input_kind``: validated against the entry nodes' ``input_kind``. NULL
    means "collected via the run form" — the normal case, and a meaning of
    its own, so it is never backfilled; with exactly one entry kind and no
    declaration the verdict carries the DERIVED value for serving only
    (``input_kind_derived``).

    A declaration + multiple deliverables → the matching deliverable becomes
    ``is_primary`` (which is how a multi-deliverable workflow becomes
    eligible to hold a kind-contract Mandate).
    """
    deliverables = compute_deliverables(graph, definition)
    kinds = [d.output_kind for d in deliverables if d.output_kind]

    output_kind = declared_output_kind
    output_backfilled = False
    error: str | None = None

    explicit_primaries = [d for d in deliverables if d.is_primary]
    if len(explicit_primaries) > 1:
        error = (
            f"This workflow marks {len(explicit_primaries)} of its results as the main "
            f"answer ({_titles(explicit_primaries)}). A workflow has exactly one main "
            "answer — open it in the workflow editor and leave that mark on one result."
        )
    elif declared_output_kind:
        if explicit_primaries:
            primary = explicit_primaries[0]
            if primary.output_kind not in (None, declared_output_kind):
                error = (
                    f"This workflow's main answer ('{primary.title}') produces "
                    f"'{primary.output_kind}', but the workflow says it answers with "
                    f"'{declared_output_kind}'. Open it in the workflow editor and make "
                    "the two agree."
                )
        else:
            matches = [d for d in deliverables if d.output_kind == declared_output_kind]
            dynamic = [d for d in deliverables if d.output_kind is None]
            if len(matches) == 1:
                matches[0].is_primary = True
            elif len(matches) > 1:
                error = (
                    f"This workflow shows {len(deliverables)} results on screen, and "
                    f"{len(matches)} of them produce '{declared_output_kind}' "
                    f"({_titles(matches)}) — so nothing says which one is the answer. "
                    "Open it in the workflow editor and leave exactly one Show on Screen "
                    f"step producing '{declared_output_kind}'."
                )
            elif len(dynamic) == 1:
                dynamic[0].is_primary = True
            elif dynamic:
                error = (
                    f"This workflow shows {len(deliverables)} results on screen "
                    f"({_titles(dynamic)}) and none of them says what it produces, so "
                    f"nothing can tell which one is the '{declared_output_kind}' answer. "
                    "Open it in the workflow editor and leave exactly one Show on Screen "
                    "step — a step whose result is not the answer can pass it along "
                    "without showing it."
                )
            else:
                offered = ", ".join(sorted(set(kinds))) or "nothing"
                error = (
                    f"No result this workflow shows on screen produces "
                    f"'{declared_output_kind}': its {len(deliverables)} result(s) "
                    f"({_titles(deliverables)}) produce [{offered}]. Open it in the "
                    "workflow editor and either add a step that produces "
                    f"'{declared_output_kind}', or change what this workflow says it "
                    "answers with."
                )
    elif len(deliverables) == 1:
        output_kind = deliverables[0].output_kind
        output_backfilled = output_kind is not None
    # else: multiple (or zero) deliverables, no declaration → NULL. §2.3.

    entry_kinds = [
        graph.nodes[nid].input_kind
        for nid in graph.entry_node_ids
        if nid in graph.nodes and graph.nodes[nid].input_kind
    ]
    input_kind = declared_input_kind
    input_derived = False
    if declared_input_kind:
        if entry_kinds and declared_input_kind not in entry_kinds:
            offered = ", ".join(sorted(set(entry_kinds)))
            declaration_error = (
                f"declared input_kind '{declared_input_kind}' is not accepted by this "
                f"workflow's entry nodes, which declare [{offered}]."
            )
            error = f"{error} {declaration_error}" if error else declaration_error
    elif len(set(entry_kinds)) == 1:
        input_kind = entry_kinds[0]
        input_derived = True

    return IoDeclarationVerdict(
        output_kind=output_kind,
        input_kind=input_kind,
        output_kind_backfilled=output_backfilled,
        input_kind_derived=input_derived,
        error=error,
        deliverables=deliverables,
    )


def declared_result(
    graph: CompiledGraph,
    definition: Definition,
    *,
    declared_output_kind: str | None,
) -> Deliverable | None:
    """THE ONE RESULT a workflow declares — what a caller (``subgraph.call``)
    reads instead of reaching into the child's step ids.

    A workflow declares its result by its ``output_kind`` (the definition
    column) plus, when several steps could answer, the step marked
    ``data.is_primary`` (the ``set_result`` patch op writes both). With no
    ``output_kind``, the ONE step marked ``is_primary`` is still the result (kind
    null). ``None`` means the workflow declares no result — the caller keeps the
    undeclared answer. A declaration the graph contradicts
    RAISES ``ValueError`` with the author-facing sentence of
    :func:`resolve_io_declaration`; it is never guessed around.
    """
    if not declared_output_kind:
        return _marked_result(graph, definition)
    verdict = resolve_io_declaration(graph, definition, declared_output_kind=declared_output_kind)
    if verdict.error:
        raise ValueError(verdict.error)
    primaries = [d for d in verdict.deliverables if d.is_primary]
    if len(primaries) != 1:
        raise ValueError(
            f"This workflow says it answers with '{declared_output_kind}' but no single "
            "step is marked as its result. Open it in the workflow editor and mark the "
            "step whose output is the answer."
        )
    primary = primaries[0]
    compiled = graph.nodes.get(primary.node_id)
    if compiled is not None and _is_dispatcher(compiled.spec_type):
        raise ValueError(
            f"This workflow's result is '{primary.title}', a step that hands each item to "
            "another step — its own output only counts what it sent, never the answer. "
            "Open it in the workflow editor and mark the step after the items are "
            "collected as the result."
        )
    return primary


def _marked_result(graph: CompiledGraph, definition: Definition) -> Deliverable | None:
    """A workflow with no ``output_kind`` that still marks ONE step as its result
    (``set_result`` with only ``node_id``): that step's output is the answer, with
    no kind. None when no single non-dispatcher step is marked."""
    marked = [n for n in definition.nodes if n.data.get("is_primary") is True and n.id in graph.nodes]
    if len(marked) != 1:
        return None
    node = marked[0]
    compiled = graph.nodes[node.id]
    if _is_dispatcher(compiled.spec_type):
        return None
    title = node.config.get("title") if isinstance(node.config.get("title"), str) else None
    return Deliverable(
        node_id=node.id,
        title=str(title or compiled.label or node.id),
        output_kind=None,
        is_primary=True,
    )


def _is_dispatcher(spec_type: str) -> bool:
    from matrx_graph.validation import DISPATCHER_NODE_TYPES

    return spec_type in DISPATCHER_NODE_TYPES


def claim_kind_value(payload: Any, output_kind: str | None) -> Any:
    """The value of ``output_kind`` inside a settled deliverable payload.

    A step that declares the kind answers with its payload as-is. A dynamic
    step (``output.to_frontend`` declares no kind) passes its incoming payload
    through, so the kind-marked value sits ONE level inside it: when exactly one
    child dict carries ``__kind == output_kind`` that child is the answer.
    Anything else returns the payload unchanged — the caller's kind check
    then says whether it fits.
    """
    if not output_kind or not isinstance(payload, dict):
        return payload
    if payload.get("__kind") == output_kind:
        return payload
    nested = [v for v in payload.values() if isinstance(v, dict) and v.get("__kind") == output_kind]
    return nested[0] if len(nested) == 1 else payload
