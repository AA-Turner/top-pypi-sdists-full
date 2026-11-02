"""Dry-run — ENGINE_SPEC §8: a formally distinct, synchronous, ZERO-side-effect mode.

``dry_run(graph, ...)`` resolves a compiled graph topologically and computes,
WITHOUT executing anything, every node's would-be state:

  * ``ready``      — every required inbound edge resolves against the
                     supplied per-node samples (§7 slot data, passed in by
                     the host) and the node's static inputs / run variables
                     resolve.
  * ``blocked``    — with the exact missing-binding list
                     (``{edge_id, reason: no_source_data |
                     mapping_unresolvable | var_missing}``).
  * ``unknowable`` — readiness cannot be decided statically: the node is
                     only reachable via dynamic dispatch (``Send`` targets —
                     map/loop bodies), sits behind a conditional whose
                     predicate can't be evaluated against available samples,
                     or all of its inbound edges prune (dead branch).

Every edge mapping is validated against the upstream's DECLARED output
schema AND the available sample: a dot-path that misses the sample is a
**warning**; one that provably misses a CLOSED schema is an **error**. Node
inputs (static + routed preview) are additionally validated against the
node's input schema; those findings are per-node diagnostics + report-level
warnings (samples are samples — the real run may differ).

Every author-written PREDICATE is additionally TRIED against the sample it
would actually meet — ``data.filter`` / ``data.assert`` / ``control.branch``
and every conditional edge — and the per-item result table rides the report as
``predicate_preview`` (W57, 2026-09-12). One row per item: the item, the value
the expression returned, kept/dropped (or passed/failed), and the sandbox's own
reason when an item raised. It is ONE evaluation: the warnings this module
raises about inert and constant predicates are DERIVED from that same table, so
a surface showing the rows and a surface showing the warning can never disagree.
Bounded at ``PREDICATE_PREVIEW_ROW_LIMIT`` rows, and it says when it truncated.

ZERO side effects, structurally: the function takes no checkpointer, no
emitter, no store; it never invokes an executor, never dispatches a Send,
never writes a row. Pure computation → a typed ``DryRunReport`` (the
documented exception to stream-everything).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from matrx_graph.executor.introspect import resolve_invocation_inputs
from matrx_graph.knobs import dry_run_knob
from matrx_graph.executor.registry import NodeRegistry, default_registry
from matrx_graph.executor.schema_validation import validate_instance
from matrx_graph.mapping_sources import (
    WHOLE_PAYLOAD,
    unknown_sigil,
    unknown_sigil_message,
)
from matrx_graph.paths import first_segment as path_first_segment, resolve_path
from matrx_graph.types.compiled import CompiledEdge, CompiledGraph, CompiledNode
from matrx_graph.types.primitives import EdgeKind
from matrx_graph.types.variables import VAR_REF_KEY, is_var_ref

_JOINABLE_KINDS = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL)

NodeState = Literal["ready", "blocked", "unknowable"]
EdgeState = Literal["satisfied", "unsatisfied", "pruned", "unknowable"]
MissingReason = Literal["no_source_data", "mapping_unresolvable", "var_missing"]


class DryRunSample(BaseModel):
    """Design-time stand-in for one node's output (§7 data slots).

    The host resolves each node's best slot (live > test > declared) and
    passes ``{value, emissions, slot}``; the engine never reads storage.
    """

    model_config = ConfigDict(frozen=True)

    value: Any = None  # api-any-ok: a captured node output — any JSON shape
    emissions: dict[str, Any] = Field(
        default_factory=dict
    )  # api-any-ok: captured ctx.emit payloads keyed by handle id
    slot: str | None = Field(
        default=None, description="Provenance label (e.g. 'last_live_output')."
    )


class MappingIssue(BaseModel):
    edge_id: str
    target_key: str
    source_key: str
    severity: Literal["error", "warning"]
    message: str


class MissingBinding(BaseModel):
    edge_id: str = Field(description="Unresolved inbound edge id; '' for node-level var_missing.")
    reason: MissingReason
    message: str = ""


#: How many per-item rows a predicate preview carries. A gate can be tried
#: against thousands of items; the AUTHOR only needs enough rows to see the
#: shape of the answer, and an unbounded payload on a report that rides an MCP
#: tool result is its own defect. Truncation is always declared
#: (``truncated`` + the summary line), never silent.
#: KNOB MIRROR of platform.feature_knob "workflow.dry_run" "predicate_preview_row_limit" —
#: the standalone default; the host binds the live row through configure_dry_run_knobs.
PREDICATE_PREVIEW_ROW_LIMIT = 25

#: Longest rendering of one sample item in a preview row.
_ITEM_PREVIEW_CHARS = 160

PredicateKind = Literal["filter", "assert", "branch", "edge"]
PredicateVerdict = Literal["kept", "dropped", "passed", "failed", "error"]


class PredicateRow(BaseModel):
    """One sample item, and what the author's predicate actually answered."""

    model_config = ConfigDict(frozen=True)

    index: int = Field(description="Position in the sample (0-based).")
    item: str = Field(
        description="The payload the predicate saw, rendered for reading (truncated)."
    )
    result: Any = Field(  # api-any-ok: whatever the author's expression returned
        default=None, description="The value the expression returned; null when it raised."
    )
    verdict: PredicateVerdict
    error: str | None = Field(
        default=None, description="The sandbox's own reason when this item raised."
    )


class PredicatePreview(BaseModel):
    """An author-written predicate, TRIED against the sample, per item.

    W57 (2026-09-12): a hand-authored gate had no way to be run against a
    sample before a paid run, so a sign error and an inert expression both
    reached production and refused a correct run. A warning that something
    "looks constant" is not the affordance — SEEING the predicate's answer
    beside each item is. This is that table, carried on the report so every
    surface (the Conductor's check, the Studio inspector) renders the same
    one evaluation rather than each re-deriving its own truth.
    """

    kind: PredicateKind
    expression: str
    binding: str = Field(
        description="Plain language for what `inputs` was bound to, per item."
    )
    total: int = Field(description="Sample items the predicate was tried against.")
    kept: int = 0
    dropped: int = 0
    errors: int = 0
    rows: list[PredicateRow] = Field(default_factory=list)
    truncated: bool = Field(
        default=False, description="True when `rows` shows fewer than `total`."
    )
    row_limit: int = PREDICATE_PREVIEW_ROW_LIMIT
    constant: bool = Field(
        default=False,
        description="The predicate answered the same for every distinct sample item.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="The findings derived from THIS evaluation — never a second pass.",
    )
    summary: str = Field(default="", description="One readable line about the trial.")


class DryRunNodeReport(BaseModel):
    state: NodeState
    missing_required: list[MissingBinding] = Field(default_factory=list)
    mapping_issues: list[MappingIssue] = Field(default_factory=list)
    would_receive: dict[str, Any] | None = (
        None  # api-any-ok: merged static+routed input preview — per-node shape
    )
    diagnostics: list[str] = Field(default_factory=list)
    predicate_preview: PredicatePreview | None = Field(
        default=None,
        description=(
            "For a predicate step (data.filter / data.assert / control.branch): "
            "the author's expression TRIED against the upstream sample, item by "
            "item. None when the step has no predicate or no sample to try it "
            "on (W57)."
        ),
    )


class DryRunEdgeReport(BaseModel):
    state: EdgeState
    slot_used: str | None = None
    predicate_preview: PredicatePreview | None = Field(
        default=None,
        description=(
            "For a conditional connection: its `condition` TRIED against the "
            "payload the source's sample would deliver (W57)."
        ),
    )


class DryRunReport(BaseModel):
    ok: bool = Field(description="True when no error-severity finding exists.")
    nodes: dict[str, DryRunNodeReport]
    edges: dict[str, DryRunEdgeReport]
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    registry_complete: bool = Field(
        default=True,
        description=(
            "False when ≥1 node type is not registered in the supplied "
            "registry — their input contracts were NOT checked, so a green "
            "report is hollow and cannot be fully trusted. A caller running "
            "against the bare default_registry (no builtins) gets ok=True "
            "only because validation was skipped; this flag exposes that."
        ),
    )


def _collect_var_refs(obj: Any) -> list[dict[str, Any]]:
    """Every ``{"$var": ...}`` reference DICT (not just names — a
    per-reference default suppresses var_missing)."""
    refs: list[dict[str, Any]] = []
    if is_var_ref(obj):
        refs.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            refs.extend(_collect_var_refs(value))
    elif isinstance(obj, list):
        for value in obj:
            refs.extend(_collect_var_refs(value))
    return refs


def _declared_output_keys(
    node: CompiledNode, registry: NodeRegistry
) -> tuple[set[str] | None, bool]:
    """(declared top-level output keys, schema-is-open). ``None`` keys =
    nothing declarable (unregistered type) — never claim an error from it."""
    if node.effective_output_schema is not None:
        props = node.effective_output_schema.get("properties")
        keys = set(props) if isinstance(props, dict) else set()
        open_schema = node.effective_output_schema.get("additionalProperties", True) is not False
        return keys, open_schema
    try:
        spec = registry.get(node.spec_type).spec
    except Exception:  # noqa: BLE001 — unregistered host node: no schema truth
        return None, True
    schema = spec.output_schema
    open_schema = schema.model_config.get("extra") == "allow"
    return set(schema.model_fields), open_schema


def _map_sample_payload(
    edge: CompiledEdge,
    payload: Any,
    *,
    declared_keys: set[str] | None,
    open_schema: bool,
) -> tuple[dict[str, Any], list[MappingIssue], bool]:
    """Mirror ``Scheduler._map_edge_payload`` against a SAMPLE payload.

    Returns ``(fragment, issues, resolvable)`` — ``resolvable=False`` only on
    an error-severity issue (the mapping can never work per the declared
    schema); a sample-only miss is a warning and the key is omitted from the
    preview.
    """
    issues: list[MappingIssue] = []
    if not isinstance(payload, dict):
        return {"value": payload}, issues, True
    if edge.mappings is None:
        return dict(payload), issues, True

    fragment: dict[str, Any] = {}
    resolvable = True
    sample_keys = set(payload)
    for target_key, source_key in edge.mappings.items():
        if "." in target_key:
            # Engine parity: a dotted TARGET key is rejected at run time.
            issues.append(
                MappingIssue(
                    edge_id=edge.edge_id,
                    target_key=target_key,
                    source_key=source_key,
                    severity="error",
                    message=(
                        f"dotted TARGET key {target_key!r} — target keys must be "
                        "plain top-level input field names (dot-notation is "
                        "SOURCE-side only)."
                    ),
                )
            )
            resolvable = False
            continue
        if source_key == WHOLE_PAYLOAD:
            fragment[target_key] = payload
            continue
        # An unsupported '$' token can never resolve, whatever the sample or
        # the schema says — no node emits '$'-prefixed output keys. Without
        # this it fell through to the dot-path miss below and, on a dynamic or
        # open upstream, came out a WARNING: the "no breaks" that let
        # '$payload' reach a paid run (129a4ec1).
        bad_sigil = unknown_sigil(source_key)
        if bad_sigil is not None:
            issues.append(
                MappingIssue(
                    edge_id=edge.edge_id,
                    target_key=target_key,
                    source_key=source_key,
                    severity="error",
                    message=unknown_sigil_message(
                        str(target_key), bad_sigil, edge_id=str(edge.edge_id)
                    ),
                )
            )
            resolvable = False
            continue
        found, resolved = resolve_path(payload, source_key)
        if found:
            fragment[target_key] = resolved
            continue
        first_segment = path_first_segment(source_key)
        known = (declared_keys or set()) | sample_keys
        if declared_keys is not None and not open_schema and first_segment not in known:
            issues.append(
                MappingIssue(
                    edge_id=edge.edge_id,
                    target_key=target_key,
                    source_key=source_key,
                    severity="error",
                    message=(
                        f"'{target_key}' <- '{source_key}': key "
                        f"'{first_segment}' exists in NEITHER the source's "
                        f"declared output schema (closed; declares "
                        f"{sorted(declared_keys)}) NOR its sample — this "
                        "mapping can never resolve (ENGINE_SPEC §8)."
                    ),
                )
            )
            resolvable = False
        else:
            issues.append(
                MappingIssue(
                    edge_id=edge.edge_id,
                    target_key=target_key,
                    source_key=source_key,
                    severity="warning",
                    message=(
                        f"'{target_key}' <- '{source_key}' does not resolve "
                        "against the available sample — verify the dot-path "
                        "against real output (schema does not rule it out)."
                    ),
                )
            )
    return fragment, issues, resolvable


_PREDICATE_NODE_TYPES: dict[str, str] = {
    "data.filter": "predicate",
    "data.assert": "predicate",
    "control.branch": "predicate",
}


def _config_value(config: Any, key: str) -> Any:
    """Read one config field off EITHER shape a node carries.

    ``CompiledNode.config`` is the VALIDATED pydantic model (compiled.py), while
    an uncompiled ``NodeDef.data.config`` is a plain dict. The W58 check read
    only the dict shape, so against a real compiled graph — every caller that
    matters — it silently found nothing and the constant-predicate warning never
    fired once in production. Found 2026-09-12 building the W57 affordance: the
    per-item table was empty for exactly the same reason the warning was.
    """
    if isinstance(config, dict):
        return config.get(key)
    return getattr(config, key, None)


def _render_item(item: Any) -> str:
    """One sample item, rendered short enough to read in a table cell."""
    try:
        text = repr(item)
    except Exception:  # noqa: BLE001 — a __repr__ that raises is not the author's problem
        text = f"<{type(item).__name__} that cannot be displayed>"
    if len(text) > _ITEM_PREVIEW_CHARS:
        return text[: _ITEM_PREVIEW_CHARS - 1] + "…"
    return text


def _binding_line(kind: PredicateKind, items: list[Any]) -> str:
    """Plain language for WHAT `inputs` is, per item — the one fact W58 proved
    an author cannot find anywhere before writing the expression."""
    if kind == "filter":
        if items and all(isinstance(i, dict) for i in items):
            return "`inputs` is each item itself (the items are objects)."
        if items and not any(isinstance(i, dict) for i in items):
            kinds = sorted({type(i).__name__ for i in items})
            return (
                f"`inputs` is {{'value': <the item>}} — the items are "
                f"{', '.join(kinds)}, not objects, so the item itself is "
                "`inputs['value']`."
            )
        return (
            "`inputs` is each item when the item is an object, and "
            "{'value': <the item>} when it is not."
        )
    if kind == "edge":
        return "`inputs` is the payload this connection delivers."
    return "`inputs` is the whole set of values this step receives."


def _evaluate_predicate(
    expr: str,
    *,
    kind: PredicateKind,
    items: list[Any] | None,
    payload: Any,
    where: str,
) -> PredicatePreview:
    """THE one evaluation. Run the author's predicate over the sample it would
    actually meet and return the per-item result table.

    Both the warnings dry_run already raised (W58) and the new per-item display
    (W57) are derived from THIS — there is no second pass and no second
    evaluator: ``bind_item`` + ``safe_eval`` are the engine's own, the same
    ones ``data.filter`` and the scheduler's conditional edges call at run
    time.

    What the table makes visible, which no warning could:

    1. The verdict PER ITEM — a filter's kept/dropped, an assert's or a
       branch's pass/fail — so a sign error (W57's `kept == 0` written as if
       the filter kept the bad ones) is read off the screen, not guessed.
    2. An item that RAISED, carrying the sandbox's own reason (the inert
       bare-`inputs` refusal, a missing key, a type error) instead of a
       swallowed default.
    3. A predicate that answers the SAME thing for every distinct item — the
       inert-gate signature (W58): it kept 14 of 14 ids its own list contained.
    """
    from matrx_graph.nodes._sandbox import bind_item, safe_eval

    sample: list[Any] = list(items) if items is not None else [payload]
    row_limit = int(dry_run_knob("predicate_preview_row_limit", PREDICATE_PREVIEW_ROW_LIMIT))
    preview = PredicatePreview(
        kind=kind,
        expression=expr,
        binding=_binding_line(kind, sample if items is not None else []),
        total=len(sample),
        row_limit=row_limit,
    )
    rows: list[PredicateRow] = []
    results: list[bool] = []
    first_error: tuple[int, str] | None = None
    for index, item in enumerate(sample):
        try:
            bound = (
                bind_item(expr, item, where=where)
                if items is not None
                else (item if isinstance(item, dict) else bind_item(expr, item, where=where))
            )
            raw = safe_eval(expr, bound)
        except Exception as e:  # noqa: BLE001 — the sandbox's reason IS the message
            preview.errors += 1
            if first_error is None:
                first_error = (index, str(e))
            if len(rows) < row_limit:
                rows.append(
                    PredicateRow(
                        index=index, item=_render_item(item), verdict="error", error=str(e)
                    )
                )
            continue
        passed = bool(raw)
        results.append(passed)
        if passed:
            preview.kept += 1
        else:
            preview.dropped += 1
        if len(rows) < row_limit:
            rows.append(
                PredicateRow(
                    index=index,
                    item=_render_item(item),
                    result=raw if isinstance(raw, (bool, int, float, str)) or raw is None else repr(raw),
                    verdict=(
                        ("kept" if passed else "dropped")
                        if kind == "filter"
                        else ("passed" if passed else "failed")
                    ),
                )
            )
    preview.rows = rows
    preview.truncated = len(rows) < preview.total

    distinct_items = len({_render_item(i) for i in sample})
    preview.constant = (
        len(results) >= 2 and distinct_items >= 2 and len(set(results)) == 1
    )

    # --- findings, derived from the table above (never a re-evaluation) ----
    warnings: list[str] = []
    if first_error is not None:
        index, reason = first_error
        if items is None:
            warnings.append(f"predicate {expr!r} is not evaluable against the sample: {reason}")
        else:
            warnings.append(
                f"predicate {expr!r} is not evaluable against sample item "
                f"{index} of {preview.total}: {reason}"
            )
    elif preview.constant:
        verdict = "kept" if results[0] else "dropped"
        warnings.append(
            f"predicate {expr!r} returned the same value for every one of the "
            f"{preview.total} sample items ({distinct_items} of them distinct) — it "
            f"{verdict} all of them. A gate that answers the same way regardless "
            f"of the item is not testing anything. Check that the predicate reads "
            f"the item (`inputs['value']` for a scalar list) and compares it to "
            f"what you meant."
        )
    preview.warnings = warnings
    preview.summary = _preview_summary(preview)
    return preview


def _preview_summary(preview: PredicatePreview) -> str:
    """One line an agent or an author reads without a legend."""
    if preview.total == 0:
        return "Nothing to try the test on."
    shown = (
        f" (showing the first {len(preview.rows)} of {preview.total})"
        if preview.truncated
        else ""
    )
    if preview.kind == "filter":
        head = (
            f"Tried against {preview.total} sample item(s){shown}: "
            f"kept {preview.kept}, dropped {preview.dropped}"
        )
    else:
        head = (
            f"Tried against {preview.total} sample payload(s){shown}: "
            f"passed {preview.kept}, failed {preview.dropped}"
        )
    if preview.errors:
        head += f", {preview.errors} could not be evaluated at all"
    return head + "."


def _check_predicate_against_sample(
    node: Any,
    preview: dict[str, Any],
    config_key: str,
) -> list[str]:
    """The WARNINGS leg of the one evaluation — kept for callers that only want
    the findings. ``_predicate_preview_for_node`` returns the whole table; both
    come from ``_evaluate_predicate`` so they can never disagree."""
    result = _predicate_preview_for_node(node, preview, config_key)
    return list(result.warnings) if result is not None else []


def _predicate_preview_for_node(
    node: Any,
    preview: dict[str, Any],
    config_key: str,
) -> PredicatePreview | None:
    """Try this predicate step's expression against the inputs it would
    receive. ``None`` when there is no expression at all, or nothing to try it
    on — the caller says THAT out loud rather than rendering an empty table."""
    expr = _config_value(node.config, config_key)
    if not isinstance(expr, str) or not expr.strip():
        return None
    items = preview.get("items")
    if node.spec_type == "data.filter" and isinstance(items, list):
        if not items:
            return None
        return _evaluate_predicate(
            expr, kind="filter", items=items, payload=None, where="data.filter"
        )
    kind: PredicateKind = "branch" if node.spec_type == "control.branch" else "assert"
    return _evaluate_predicate(
        expr, kind=kind, items=None, payload=preview, where=node.spec_type
    )


def dry_run(
    graph: CompiledGraph,
    *,
    inputs: dict[str, Any] | None = None,
    node_inputs: dict[str, dict[str, Any]] | None = None,
    variables: dict[str, Any] | None = None,
    samples: dict[str, DryRunSample] | None = None,
    registry: NodeRegistry | None = None,
) -> DryRunReport:
    """Compute the graph's would-be run state — pure, sync, zero side effects.

    ``inputs``/``node_inputs`` mirror ``Scheduler.run`` seeding (broadcast +
    per-entry-node). ``variables`` are the run's initial_variables.
    ``samples`` is the host-supplied per-node §7 slot data.
    """
    registry = registry or default_registry()
    samples = samples or {}
    run_vars = dict(variables or {})
    node_reports: dict[str, DryRunNodeReport] = {}
    edge_reports: dict[str, DryRunEdgeReport] = {}
    errors: list[str] = []
    warnings: list[str] = []
    registry_complete = True

    # --- edge resolution against samples (source-side, order-free) --------
    # (fragment, issues, state) per joinable non-back edge.
    edge_fragments: dict[str, dict[str, Any] | None] = {}
    edge_issues: dict[str, list[MappingIssue]] = {}
    for edge_id, edge in graph.edges.items():
        if edge.kind not in _JOINABLE_KINDS:
            edge_reports[edge_id] = DryRunEdgeReport(state="unknowable")
            continue
        if edge.is_back_edge:
            # Fires dynamically, once per upstream delivery (F13) — not
            # statically decidable.
            edge_reports[edge_id] = DryRunEdgeReport(state="unknowable")
            continue
        source = graph.nodes[edge.source_node_id]
        sample = samples.get(edge.source_node_id)
        if sample is None:
            edge_reports[edge_id] = DryRunEdgeReport(state="unsatisfied")
            continue
        if edge.kind is EdgeKind.CONTROL:
            # Gates the join, binds no payload (§3.2) — source data exists.
            edge_reports[edge_id] = DryRunEdgeReport(state="satisfied", slot_used=sample.slot)
            edge_fragments[edge_id] = {}
            continue
        if edge.source_handle is not None:
            if edge.source_handle not in sample.emissions:
                # The captured firing didn't take this branch — availability
                # here is genuinely unknowable at design time (§7 emissions
                # give Satisfied only when the handle WAS emitted).
                edge_reports[edge_id] = DryRunEdgeReport(state="unknowable", slot_used=sample.slot)
                continue
            payload: Any = sample.emissions[edge.source_handle]
        else:
            payload = sample.value
        edge_preview: PredicatePreview | None = None
        if edge.kind is EdgeKind.CONDITIONAL and edge.condition:
            # Same one evaluation as a predicate NODE — bind_item still refuses
            # a bare-`inputs` condition over a wrapped scalar payload (W58) and
            # the per-item table now rides the edge report (W57).
            edge_preview = _evaluate_predicate(
                edge.condition,
                kind="edge",
                items=None,
                payload=payload,
                where=f"conditional edge '{edge_id}'",
            )
            if edge_preview.errors:
                reason = next(
                    (r.error for r in edge_preview.rows if r.error), "not evaluable"
                )
                warnings.append(
                    f"edge '{edge_id}': predicate {edge.condition!r} not "
                    f"evaluable against the sample ({reason})"
                )
                edge_reports[edge_id] = DryRunEdgeReport(
                    state="unknowable", slot_used=sample.slot, predicate_preview=edge_preview
                )
                continue
            if edge_preview.dropped:
                edge_reports[edge_id] = DryRunEdgeReport(
                    state="pruned", slot_used=sample.slot, predicate_preview=edge_preview
                )
                continue
        declared_keys, open_schema = _declared_output_keys(source, registry)
        fragment, issues, resolvable = _map_sample_payload(
            edge, payload, declared_keys=declared_keys, open_schema=open_schema
        )
        edge_issues[edge_id] = issues
        if resolvable:
            edge_reports[edge_id] = DryRunEdgeReport(
                state="satisfied", slot_used=sample.slot, predicate_preview=edge_preview
            )
            edge_fragments[edge_id] = fragment
        else:
            edge_reports[edge_id] = DryRunEdgeReport(
                state="unsatisfied", slot_used=sample.slot, predicate_preview=edge_preview
            )

    # --- per-node state, walked topologically for a deterministic report --
    seen: set[str] = set()
    ordered_ids = [nid for layer in graph.topological_layers for nid in layer]
    ordered_ids += [nid for nid in graph.nodes if nid not in set(ordered_ids)]
    for node_id in ordered_ids:
        if node_id in seen:
            continue
        seen.add(node_id)
        node = graph.nodes[node_id]
        report = DryRunNodeReport(state="ready")
        node_reports[node_id] = report

        # Node-level var check (any node may reference run variables).
        for ref in _collect_var_refs(node.static_inputs):
            name = str(ref[VAR_REF_KEY])
            if name in run_vars or "default" in ref:
                continue
            declared = graph.variables.get(name)
            if declared is not None and declared.default is not None:
                continue
            # A folded input-surface entry with a default also satisfies the
            # legacy reference (INPUT-SURFACE.md compat — resolve_var_refs
            # applies the same fallback at run time).
            surface_spec = graph.input_surface.get(name)
            if surface_spec is not None and surface_spec.default is not None:
                continue
            report.missing_required.append(
                MissingBinding(
                    edge_id="",
                    reason="var_missing",
                    message=(
                        f"run variable '{name}' has no value and no default — "
                        "the run would park on this node "
                        "(UnresolvedVariableError)."
                    ),
                )
            )
            errors.append(f"node '{node_id}': run variable '{name}' unresolved")

        is_entry = node_id in graph.entry_node_ids
        required = [
            eid
            for eid in node.incoming_edge_ids
            if graph.edges[eid].kind in _JOINABLE_KINDS and not graph.edges[eid].is_back_edge
        ]

        routed: dict[str, Any] | None = None
        if is_entry:
            routed = {**(inputs or {}), **(node_inputs or {}).get(node_id, {})}
        elif not required:
            report.state = "unknowable"
            report.diagnostics.append(
                "no inbound connections and not an entry node — reachable "
                "only via dynamic dispatch (Send: a map/loop body); "
                "readiness is not statically decidable."
            )
        else:
            satisfied: list[str] = []
            any_unknowable = False
            for eid in required:
                report.mapping_issues.extend(edge_issues.get(eid, []))
                state = edge_reports[eid].state
                if state == "satisfied":
                    satisfied.append(eid)
                elif state == "pruned":
                    continue
                elif state == "unknowable":
                    any_unknowable = True
                else:  # unsatisfied
                    reason: MissingReason = (
                        "mapping_unresolvable"
                        if any(i.severity == "error" for i in edge_issues.get(eid, []))
                        else "no_source_data"
                    )
                    report.missing_required.append(
                        MissingBinding(
                            edge_id=eid,
                            reason=reason,
                            message=(
                                "mapping can never resolve (see mapping_issues)"
                                if reason == "mapping_unresolvable"
                                else (
                                    f"no sample data on source "
                                    f"'{graph.edges[eid].source_node_id}' — run "
                                    "the node once (test) or declare a sample "
                                    "(§7 data slots)."
                                )
                            ),
                        )
                    )
            unresolved = [m for m in report.missing_required if m.edge_id]
            if node.join_policy == "any":
                fire = bool(satisfied)
            else:
                fire = not unresolved and not any_unknowable and bool(satisfied)
            if unresolved or (report.missing_required and not fire):
                report.state = "blocked"
            elif not fire:
                report.state = "unknowable"
                if any_unknowable:
                    report.diagnostics.append(
                        "an inbound connection's availability is not "
                        "statically decidable (unemitted branch handle / "
                        "unevaluable predicate / dynamic re-fire)."
                    )
                else:
                    report.diagnostics.append(
                        "every inbound connection prunes against the samples "
                        "— dead branch for this data."
                    )
            else:
                # Merge satisfied fragments — §3.7 multi-writer parity.
                merged: dict[str, Any] = {}
                merge_pool: dict[str, list[Any]] = {}
                first_writer: dict[str, str] = {}
                for eid in sorted(satisfied):
                    fragment = edge_fragments.get(eid) or {}
                    for key, value in fragment.items():
                        if key in node.arg_merge:
                            merge_pool.setdefault(key, []).append(value)
                            continue
                        if key in first_writer:
                            report.mapping_issues.append(
                                MappingIssue(
                                    edge_id=eid,
                                    target_key=key,
                                    source_key="",
                                    severity="error",
                                    message=(
                                        f"input key '{key}' is written by TWO "
                                        f"edges ('{first_writer[key]}' and "
                                        f"'{eid}') — multi-writer same-arg "
                                        "parks the run (§3.7); declare "
                                        f"data.arg_merge['{key}'] or remap."
                                    ),
                                )
                            )
                            errors.append(f"node '{node_id}': multi-writer input key '{key}'")
                            continue
                        first_writer[key] = eid
                        merged[key] = value
                for key, values in merge_pool.items():
                    merged[key] = values  # preview only; reducer applies at run time
                routed = merged

        if report.missing_required and report.state == "ready":
            report.state = "blocked"

        if routed is not None and report.state == "ready":
            preview = resolve_invocation_inputs(
                node,
                routed,
                run_variables=run_vars,
                declared_variables=graph.variables,
                strict_variables=False,
            )
            report.would_receive = preview
            if node.spec_type in _PREDICATE_NODE_TYPES:
                # ONE evaluation (W57/W58): the per-item table rides the report
                # so a surface can SHOW the author what the predicate answered,
                # and the warnings below are derived from that same table —
                # never a second pass with its own opinion.
                trial = _predicate_preview_for_node(
                    node, preview, _PREDICATE_NODE_TYPES[node.spec_type]
                )
                report.predicate_preview = trial
                for msg in trial.warnings if trial is not None else []:
                    report.diagnostics.append(msg)
                    warnings.append(f"node '{node_id}': {msg}")
            # Input contract check — mirrors the scheduler's pre-execute
            # gates (dynamic-source JSON Schema, else pydantic input_schema).
            try:
                spec = registry.get(node.spec_type).spec
            except Exception:  # noqa: BLE001
                report.diagnostics.append(
                    f"node type '{node.spec_type}' is not registered here — "
                    "input contract not checked."
                )
                registry_complete = False
                spec = None
            if spec is not None:
                if spec.is_source and node.effective_output_schema is not None:
                    field_errors = validate_instance(node.effective_output_schema, preview)
                    if field_errors and is_entry:
                        # Runtime parity (scheduler is_source gate): a source
                        # ENTRY node validates its ACTUAL provided values
                        # (node_inputs — real input, NOT an advisory sample)
                        # against its output schema BEFORE it runs and raises
                        # NodeInputValidationError → ERRORED on any violation.
                        # So the violation is FATAL in dry-run too: block the
                        # node and drop ok — never a green light for a graph
                        # that deterministically errors.
                        report.state = "blocked"
                        for err in field_errors:
                            report.diagnostics.append(f"input mismatch: {err}")
                            errors.append(f"node '{node_id}': input mismatch: {err}")
                    else:
                        # A non-entry source validates against a SAMPLE (§7),
                        # which is advisory — keep the warning posture.
                        for err in field_errors:
                            report.diagnostics.append(f"input mismatch: {err}")
                            warnings.append(f"node '{node_id}': input mismatch: {err}")
                else:
                    try:
                        spec.input_schema.model_validate(preview)
                    except ValidationError as ve:
                        for err in ve.errors():
                            loc = ".".join(str(p) for p in err["loc"])
                            msg = f"input mismatch at '{loc}': {err['msg']}"
                            report.diagnostics.append(msg)
                            warnings.append(f"node '{node_id}': {msg}")

        for issue in report.mapping_issues:
            if issue.severity == "error":
                errors.append(f"node '{node_id}' edge '{issue.edge_id}': {issue.message}")
            else:
                warnings.append(f"node '{node_id}' edge '{issue.edge_id}': {issue.message}")

    # De-duplicate while preserving order (an edge's issues can surface on
    # several targets only via distinct messages, but var/nodes may repeat).
    errors = list(dict.fromkeys(errors))
    warnings = list(dict.fromkeys(warnings))
    return DryRunReport(
        ok=not errors,
        nodes=node_reports,
        edges=edge_reports,
        errors=errors,
        warnings=warnings,
        registry_complete=registry_complete,
    )
