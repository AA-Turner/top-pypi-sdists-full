from __future__ import annotations

import hashlib
import json
import logging
from collections import defaultdict
from typing import Any

from pydantic import BaseModel, ValidationError

from matrx_graph.diagnostics.compile_validation import scream_node_config_rejected
from matrx_graph.content_ir.edge_routing import (
    EdgeRoutingDeclarationError,
    parse_edge_routing,
)
from matrx_graph.content_ir.triggers import TriggerDeclarationError, parse_node_trigger
from matrx_graph.errors import CompilationError
from matrx_graph.kinds import declared_output_kind
from matrx_graph.executor.schema_validation import schema_validity_errors
from matrx_graph.executor.registry import NodeRegistry, default_registry
from matrx_graph.types.channel import ChannelSpec
from matrx_graph.types.compiled import CompiledEdge, CompiledGraph, CompiledNode, StepClock
from matrx_graph.types.input_surface import InputSpec, compiled_kind_and_variant, hint_values
from matrx_graph.types.definition import Definition
from matrx_graph.types.primitives import EdgeKind, RetryPolicy
from matrx_graph.validation import declared_input_defaults, split_setting_refs, validate_definition

logger = logging.getLogger(__name__)


# ``Definition.metadata[START_WHEN_READY_KEY] = True`` opts a workflow into START WHEN READY
# scheduling (executor/FEATURE.md).
START_WHEN_READY_KEY = "start_when_ready"


def _hash_definition(definition: Definition) -> str:
    payload = definition.model_dump(mode="json")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]


def _resolve_config(
    config_schema: type[BaseModel],
    raw_config: dict[str, Any],
    *,
    node_id: str | None = None,
    spec_type: str | None = None,
    node_data: dict[str, Any] | None = None,
) -> BaseModel:
    try:
        return config_schema.model_validate(raw_config)
    except ValidationError as e:
        if node_id is not None and spec_type is not None and node_data is not None:
            scream_node_config_rejected(
                node_id=node_id,
                spec_type=spec_type,
                config_schema=config_schema,
                raw_config=raw_config,
                node_data=node_data,
                validation_error=e,
            )
        raise CompilationError(
            f"Invalid config for node (schema: {config_schema.__name__}): {e}"
        ) from e
    except Exception as e:
        raise CompilationError(
            f"Invalid config for node (schema: {config_schema.__name__}): {e}"
        ) from e


# Edge kinds that route at run time and therefore matter for cycle
# classification (mirrors Scheduler._JOINABLE_KINDS). ERROR edges route as of
# the Node Result System (they deliver the structured NodeError on a routable
# node failure, prune on success) so they participate in back-edge
# classification like any other routable kind; STREAM edges neither
# join-count nor route.
_ROUTABLE_KINDS = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL, EdgeKind.ERROR)


def _detect_back_edges(
    entry_ids: tuple[str, ...],
    edges: dict[str, CompiledEdge],
    outgoing: dict[str, list[str]],
    all_node_ids: list[str],
) -> set[str]:
    """Classify cycle back-edges by iterative DFS from the entry nodes
    (ENGINE_SPEC §3.2 / F13 compat).

    Every cycle reachable from an entry node has ≥1 edge classified as a
    back-edge (target currently on the DFS stack); excluding those from the
    join required sets makes the forward subgraph a DAG, so legacy feedback
    edges (self-loops, A→B→A) re-fire per delivery instead of deadlocking
    the §3 join accumulator.

    A cycle UNREACHABLE from the entry nodes is ambiguous (no deterministic
    back-edge orientation, and its nodes could never fire anyway) — that is
    a LOUD CompilationError naming the cycle, never a silent deadlock.
    """
    color: dict[str, int] = {}  # missing=white, 1=on stack, 2=done
    back: set[str] = set()
    for root in entry_ids:
        if color.get(root):
            continue
        color[root] = 1
        stack: list[tuple[str, Any]] = [(root, iter(outgoing.get(root, [])))]
        while stack:
            _node_id, edge_iter = stack[-1]
            descended = False
            for eid in edge_iter:
                edge = edges[eid]
                if edge.kind not in _ROUTABLE_KINDS:
                    continue
                tgt = edge.target_node_id
                state = color.get(tgt, 0)
                if state == 1:
                    back.add(eid)
                elif state == 0:
                    color[tgt] = 1
                    stack.append((tgt, iter(outgoing.get(tgt, []))))
                    descended = True
                    break
            if not descended:
                color[stack[-1][0]] = 2
                stack.pop()

    # Disconnected-cycle guard: peel the unreachable subgraph with Kahn's
    # algorithm (routable edges only); anything left is a cycle no entry
    # node can reach — reject loudly with the cycle members named.
    unreachable = [nid for nid in all_node_ids if nid not in color]
    if unreachable:
        unreachable_set = set(unreachable)
        in_degree = dict.fromkeys(unreachable, 0)
        local_out: dict[str, list[str]] = defaultdict(list)
        for edge in edges.values():
            if edge.kind not in _ROUTABLE_KINDS:
                continue
            if edge.source_node_id in unreachable_set and edge.target_node_id in unreachable_set:
                in_degree[edge.target_node_id] += 1
                local_out[edge.source_node_id].append(edge.target_node_id)
        frontier = [nid for nid in unreachable if in_degree[nid] == 0]
        while frontier:
            nid = frontier.pop()
            unreachable_set.discard(nid)
            for tgt in local_out.get(nid, ()):
                in_degree[tgt] -= 1
                if in_degree[tgt] == 0:
                    frontier.append(tgt)
        if unreachable_set:
            cycle_nodes = sorted(unreachable_set)
            cycle_edges = sorted(
                e.edge_id
                for e in edges.values()
                if e.source_node_id in unreachable_set and e.target_node_id in unreachable_set
            )
            raise CompilationError(
                f"Cycle unreachable from any entry node: nodes "
                f"{cycle_nodes} (edges {cycle_edges}). The engine cannot "
                "orient its feedback edge, so the cycle would deadlock the "
                "join accumulator silently (ENGINE_SPEC §3.4/§12.8). Give "
                "the cycle an entry path (an inbound edge from the entry "
                "subgraph) or declare one of its nodes in entry_nodes."
            )
    return back


def _topological_layers(
    node_ids: list[str],
    edges: list[tuple[str, str]],
) -> tuple[tuple[str, ...], ...]:
    """Kahn's algorithm with layering. Cycles are legal at runtime (Pregel loop
    convergence handles them) but we still produce best-effort layers here for
    static visualization. Unresolved nodes land in a final 'cycle' layer.
    """
    in_degree: dict[str, int] = dict.fromkeys(node_ids, 0)
    outgoing: dict[str, list[str]] = defaultdict(list)
    for src, tgt in edges:
        if tgt in in_degree:
            in_degree[tgt] += 1
        outgoing[src].append(tgt)

    layers: list[tuple[str, ...]] = []
    remaining = set(node_ids)
    while remaining:
        layer = tuple(sorted(n for n in remaining if in_degree[n] == 0))
        if not layer:
            # Cycle — emit remaining as one final layer and stop peeling.
            layers.append(tuple(sorted(remaining)))
            break
        layers.append(layer)
        for n in layer:
            remaining.discard(n)
            for tgt in outgoing[n]:
                in_degree[tgt] = max(0, in_degree[tgt] - 1)

    return tuple(layers)



def _dispatch_target_ids(nodes: dict[str, CompiledNode]) -> set[str]:
    """Every node a dispatcher (``validation.DISPATCHER_NODE_TYPES``) names as its
    ``config.target_node_id`` — reached by dispatch only, never an entry candidate."""
    from matrx_graph.validation import DISPATCHER_NODE_TYPES

    targets: set[str] = set()
    for nid, node in nodes.items():
        if node.spec_type not in DISPATCHER_NODE_TYPES:
            continue
        target = getattr(node.config, "target_node_id", None)
        if isinstance(target, str) and target in nodes and target != nid:
            targets.add(target)
    return targets

def compile(  # noqa: A001 — mirrors matplotlib-style top-level compile()
    definition: Definition,
    registry: NodeRegistry | None = None,
) -> CompiledGraph:
    """Turn a Definition into an executable CompiledGraph.

    Performs validation, config resolution, edge indexing, topological
    layering, and channel inference. Cacheable by `definition_hash`.

    Raises CompilationError if the definition is invalid (validation issues).
    """
    registry = registry or default_registry()
    registry.ensure_bootstrapped()
    result = validate_definition(definition, registry=registry)
    if not result.valid:
        # EVERY issue travels with the error, not just the first. A host
        # that can only repeat "the first of six problems"
        # cannot tell the person in front of it what to fix.
        raise CompilationError(
            f"Definition has {len(result.issues)} validation issue(s); "
            f"first: {result.issues[0].message} at {result.issues[0].path}",
            issues=list(result.issues),
        )
    # Built-in step settings become the real steps they stand for (matrx_graph/step_settings.py);
    # validation above already expanded and checked the same graph.
    from matrx_graph.step_settings import expand_step_settings

    definition = expand_step_settings(definition)

    incoming: dict[str, list[str]] = defaultdict(list)
    outgoing: dict[str, list[str]] = defaultdict(list)
    edges: dict[str, CompiledEdge] = {}
    for edge in definition.edges:
        # Kind routing (§7.3/§7.4). A malformed declaration is an AUTHORING
        # error and dies here, at compile, where the studio can show it —
        # never mid-run, where a typo in ``fan_out`` would silently dispatch
        # a paid step the wrong number of times.
        try:
            routing = parse_edge_routing(edge.data)
        except EdgeRoutingDeclarationError as exc:
            raise CompilationError(f"edge '{edge.id}': {exc}") from exc
        compiled = CompiledEdge(
            edge_id=edge.id,
            source_node_id=edge.source,
            target_node_id=edge.target,
            source_handle=edge.sourceHandle,
            target_handle=edge.targetHandle,
            kind=edge.kind,
            condition=edge.condition,
            mappings=edge.mappings,
            kind_filter=routing.kind_filter,
            fan_out=routing.fan_out,
            item_key=routing.item_key,
            review=edge.review,
        )
        edges[edge.id] = compiled
        outgoing[edge.source].append(edge.id)
        incoming[edge.target].append(edge.id)

    declared_channels: dict[str, ChannelSpec] = {c.name: c for c in definition.channels}

    nodes: dict[str, CompiledNode] = {}
    input_defaults = declared_input_defaults(definition)
    for node in definition.nodes:
        executor = registry.get(node.spec_type)
        spec = executor.spec
        raw_config, config_input_refs, setting_problems = split_setting_refs(spec.config_schema, node.config, input_defaults)
        if setting_problems:
            raise CompilationError(f"node '{node.id}': " + "; ".join(setting_problems))
        config = _resolve_config(
            spec.config_schema,
            raw_config,
            node_id=node.id,
            spec_type=spec.node_type,
            node_data=node.data,
        )

        reads = tuple(h.channel for h in spec.handles if h.direction.value == "input" and h.channel)
        writes = tuple(
            h.channel for h in spec.handles if h.direction.value == "output" and h.channel
        )

        # Phase 6.2 — per-node mock_response. Authored on the user's
        # NodeDef as data.mock_response = {enabled: bool, output: {...}}.
        # We surface it on the CompiledNode iff enabled=true; the
        # scheduler then short-circuits the executor.
        raw_mock = node.data.get("mock_response")
        mock_response: dict[str, Any] | None = None
        if isinstance(raw_mock, dict) and raw_mock.get("enabled") is True:
            mock_output = raw_mock.get("output")
            if isinstance(mock_output, dict):
                mock_response = mock_output

        # Phase 6.1 — per-node RetryPolicy override. Authored as
        # data.retry_policy = {max_attempts, backoff, initial_delay_ms,
        # max_delay_ms, retry_on}. Parsed through RetryPolicy so a bad
        # value fails compilation (loud) rather than at run time.
        raw_retry = node.data.get("retry_policy")
        retry_policy: RetryPolicy | None = None
        if isinstance(raw_retry, dict) and raw_retry:
            try:
                retry_policy = RetryPolicy.model_validate(raw_retry)
            except Exception as e:  # noqa: BLE001
                raise CompilationError(f"node '{node.id}' has an invalid retry_policy: {e}") from e

        # Per-node wall clock. Authored as data.step_clock = {seconds, knob?:
        # {feature, key}}; a bad value fails compilation (loud), never a run.
        step_clock = _compile_step_clock(node.id, node.data.get("step_clock"))

        # Run once per key (matrx_graph/once.py). Authored as data.once; a bad value fails
        # compilation (loud), never a run.
        from matrx_graph.once import parse_once

        try:
            once = parse_once(node.data.get("once"))
        except ValueError as e:
            raise CompilationError(f"node '{node.id}' has an invalid once setting: {e}") from e

        # One at a time per key (matrx_graph/one_at_a_time.py). Authored as data.one_at_a_time;
        # a bad value fails compilation (loud), never a run.
        from matrx_graph.one_at_a_time import parse_one_at_a_time

        try:
            one_at_a_time = parse_one_at_a_time(node.data.get("one_at_a_time"))
        except ValueError as e:
            raise CompilationError(
                f"node '{node.id}' has an invalid one_at_a_time setting: {e}"
            ) from e

        # Run in another organization (matrx_graph/in_organization.py). Authored as
        # data.in_organization; a bad value fails compilation (loud), never a run.
        from matrx_graph.in_organization import parse_in_organization

        try:
            in_organization = parse_in_organization(node.data.get("in_organization"))
        except ValueError as e:
            raise CompilationError(
                f"node '{node.id}' has an invalid in_organization setting: {e}"
            ) from e

        # Per-node output-channel binding. Authored as
        # data.output_channel = "<channel name>": the scheduler writes the
        # node's full output dump to that channel after success/mock, so
        # generic nodes can participate in reducer-based fan-in without a
        # custom executor.
        raw_output_channel = node.data.get("output_channel")
        output_channel: str | None = None
        if raw_output_channel is not None:
            if not isinstance(raw_output_channel, str) or not raw_output_channel.strip():
                raise CompilationError(
                    f"node '{node.id}' has an invalid output_channel: expected a "
                    f"non-empty string, got {raw_output_channel!r}"
                )
            output_channel = raw_output_channel
            if output_channel not in writes:
                writes = (*writes, output_channel)

        # Kind trigger (§7.7c) — read BEFORE entry-node derivation below,
        # which must exclude these nodes.
        try:
            trigger = parse_node_trigger(node.data)
        except TriggerDeclarationError as exc:
            raise CompilationError(f"node '{node.id}': {exc}") from exc

        # Platform-kind I/O declarations. The spec's kinds are the node
        # author's defaults; a NodeDef may override per node via
        # ``data.input_kind`` / ``data.output_kind`` — how a workflow author
        # binds a generic node (llm.*, transform) to a named Shape. A bad
        # value fails compilation loudly; kind EXISTENCE is checked at publish
        # (content_ir/authoring_gate.py) and at run admission by the kind
        # catalog (fatal under workflow_io enforcement), since compile is sync.
        input_kind: str | None = spec.input_kind
        for key in ("input_kind", "output_kind"):
            raw_kind = node.data.get(key)
            if raw_kind is None:
                continue
            if not isinstance(raw_kind, str) or not raw_kind.strip():
                raise CompilationError(
                    f"node '{node.id}' has an invalid {key}: expected a "
                    f"non-empty kind slug string, got {raw_kind!r}"
                )
            if key == "input_kind":
                input_kind = raw_kind.strip()
        # The ONE resolver the save gate shares (authored kind, else the step type's own).
        output_kind = declared_output_kind(node.data, spec.output_kind)

        # Dynamic-output nodes (e.g. io.user_input) compute their effective
        # output schema from their config at compile time — used to generate
        # the run form and for downstream type hints. The registered
        # output_schema stays permissive; this is the real shape.
        effective_output_schema: dict[str, Any] | None = None
        if spec.dynamic_output:
            getter = getattr(config, "effective_output_json_schema", None)
            if callable(getter):
                try:
                    effective_output_schema = getter()
                except Exception as e:  # noqa: BLE001
                    raise CompilationError(
                        f"node '{node.id}' ({spec.node_type}) failed to compute "
                        f"its dynamic output schema: {e}"
                    ) from e
            # Compile-time schema validity (the layer validate_instance's
            # runtime fail-open guard always pointed at): the compiled
            # effective_output_schema must itself be a structurally valid
            # Draft 2020-12 JSON Schema. A malformed one would silently skip
            # every input-gate validation at run time (loud-skip posture) —
            # catch it HERE, at the compile seam, loudly. Fatal while the
            # workflow_io enforcement flag is ON (the live posture since
            # 2026-08-26); with it rolled back only the scream remains.
            if effective_output_schema is not None:
                schema_findings = schema_validity_errors(effective_output_schema)
                if schema_findings:
                    from matrx_graph.kinds import kind_enforcement_enabled

                    message = (
                        f"node '{node.id}' ({spec.node_type}) compiled an "
                        f"effective_output_schema that is NOT a valid Draft "
                        f"2020-12 JSON Schema — its run-time input gate would "
                        f"loud-skip (degraded_reason=schema_invalid). Findings: "
                        f"{'; '.join(schema_findings)}"
                    )
                    if kind_enforcement_enabled("workflow_io"):
                        raise CompilationError(message)
                    logger.error("COMPILE GATE (non-fatal, enforcement OFF): %s", message)

        nodes[node.id] = CompiledNode(
            node_id=node.id,
            spec_type=spec.node_type,
            label=node.label,
            config=config,
            config_input_refs=config_input_refs,
            # Node-authored static inputs. The studio inspector persists
            # these under ``data.input`` (singular) — its canonical key for
            # input-only nodes — so that's read first; ``data.inputs``
            # (plural) is accepted as a fallback for any older/programmatic
            # definitions. Without this the inspector's edits to an
            # input-only node silently never reached the executor.
            static_inputs=(
                node.data.get("input")
                if isinstance(node.data.get("input"), dict)
                else node.data.get("inputs", {})
            ),
            incoming_edge_ids=tuple(incoming.get(node.id, [])),
            outgoing_edge_ids=tuple(outgoing.get(node.id, [])),
            reads_channels=reads,
            writes_channels=writes,
            mock_response=mock_response,
            retry_policy=retry_policy,
            step_clock=step_clock,
            once=once,
            one_at_a_time=one_at_a_time,
            in_organization=in_organization,
            effective_output_schema=effective_output_schema,
            output_channel=output_channel,
            input_kind=input_kind,
            output_kind=output_kind,
            trigger_kind=trigger.kind if trigger else None,
            trigger_mode=trigger.mode if trigger else "all",
            trigger_fire_once=trigger.fire_once if trigger else False,
            trigger_debounce_steps=trigger.debounce_steps if trigger else 0,
            trigger_item_key=trigger.item_key if trigger else "value",
            # Join semantics (ENGINE_SPEC §3) — enum-shaped values were
            # already rejected by validate_definition above; the NodeDef
            # accessors normalize types/defaults. An authored join_policy
            # wins; otherwise the NodeSpec's declared type default applies
            # (control.loop = 'any' — §9: the return edge re-fires the loop
            # per delivery; 'all' would deadlock every loop's first firing).
            join_policy=(  # type: ignore[arg-type]
                node.join_policy
                if node.data.get("join_policy") is not None
                else (spec.default_join_policy or node.join_policy)
            ),
            on_skipped_upstream=node.on_skipped_upstream,  # type: ignore[arg-type]
            skip_defaults=node.skip_defaults,
            arg_merge=node.arg_merge,
            on_item_failure=node.on_item_failure,  # type: ignore[arg-type]
            optional=node.optional,
            deliverable=(
                node.data.get("deliverable") if isinstance(node.data.get("deliverable"), bool) else None
            ),
            review=node.review,
            concurrency=node.concurrency,
            concurrency_input_ref=node.concurrency_input_ref,
            ready_when=node.ready_when,
        )

    # Fill in implicit channels for any name a node declared via handle.channel.
    for node in nodes.values():
        for chan in (*node.reads_channels, *node.writes_channels):
            if chan not in declared_channels and not definition.strict_channels:
                declared_channels[chan] = ChannelSpec(name=chan, reducer="replace")

    if definition.entry_nodes:
        entry = tuple(definition.entry_nodes)
    else:
        # A kind-triggered node (§7.7c) has no incoming edges BY DESIGN. Left
        # in the derived entry set it would fire at step 1 on nothing — the
        # exact opposite of "run when this kind is generated". Its firings
        # come from the subscription matcher instead.
        #
        # A dispatcher's target (a For Each / send / loop / work-queue body) has no inbound
        # connection either, BY DESIGN: it is reached only through the dispatch. Left in the
        # derived entry set it started on its own at step 0 with no item (2026-10-27) — every
        # such workflow had to list entry_nodes by hand to avoid it.
        dispatch_targets = _dispatch_target_ids(nodes)
        entry = tuple(
            nid
            for nid, n in nodes.items()
            if not n.incoming_edge_ids and not n.trigger_kind and nid not in dispatch_targets
        )

    # Cycle back-edge classification (ENGINE_SPEC §3.2 / F13 compat): mark
    # every reachable cycle's feedback edge so the scheduler excludes it from
    # join required sets and re-fires the target per delivery. Raises loudly
    # for a cycle no entry node can reach (never a silent join deadlock).
    back_edge_ids = _detect_back_edges(entry, edges, outgoing, list(nodes))
    for eid in back_edge_ids:
        edges[eid] = edges[eid].model_copy(update={"is_back_edge": True})

    edge_pairs = [(e.source_node_id, e.target_node_id) for e in edges.values()]
    layers = _topological_layers(list(nodes), edge_pairs)

    input_surface = _build_input_surface(definition, nodes)

    return CompiledGraph(
        definition_hash=_hash_definition(definition),
        nodes=nodes,
        edges=edges,
        channels=declared_channels,
        entry_node_ids=entry,
        topological_layers=layers,
        strict_channels=definition.strict_channels,
        # A published workflow's media must be born public; the scheduler
        # enters `public_media_scope()` for the whole run.
        public_media=definition.public_media,
        # START WHEN READY is opted into per workflow while it is proven: ``metadata`` is the
        # definition-level bag every save path already stores and the Studio round-trips.
        start_when_ready=definition.metadata.get(START_WHEN_READY_KEY) is True,
        source_metadata={},
        # Declared run variables — validate_definition already rejected any
        # {'$var': name} reference in static inputs that isn't declared here,
        # so at run time every reference resolves against this dict + the
        # run's initial_variables (see executor/introspect.py). LEGACY — the
        # same declarations also fold into input_surface below.
        variables={v.name: v for v in definition.variables},
        input_surface=input_surface,
    )


def _build_input_surface(
    definition: Definition,
    nodes: dict[str, CompiledNode],
) -> dict[str, InputSpec]:
    """Compile THE workflow input surface (INPUT-SURFACE.md).

    Union of every ``io.user_input`` node's fields + the declared variables
    (folded in — no separate species), flattened to ONE name-unique map. A
    collision — two input nodes declaring the same field name, or a declared
    variable shadowing a field — is a NAMED compile refusal: the surface is
    what the outside world addresses, so an ambiguous name has no meaning.
    (Live census 2026-08-27: zero collisions across all stored definitions
    and versions, so this refusal only ever bites NEW authoring.)
    """
    from matrx_graph.nodes.io.user_input import UserInputConfig
    from matrx_graph.types.variables import iter_input_refs, iter_var_refs, variable_json_schema

    surface: dict[str, InputSpec] = {}
    declared_by: dict[str, str] = {}  # input name -> "node '<id>'" / "variables"

    # Names any {'$var'}/{'$input'} marker references, anywhere in authored
    # node data — feeds InputSpec.referenced so the park gate never blocks a
    # run over a declared-but-unconsumed variable.
    referenced_names: set[str] = set()
    for node in definition.nodes:
        referenced_names.update(name for _, name in iter_var_refs(node.data))
        referenced_names.update(name for _, name in iter_input_refs(node.data))

    for node in definition.nodes:
        if node.spec_type != "io.user_input":
            continue
        compiled = nodes.get(node.id)
        if compiled is None:
            continue
        config = compiled.config
        if not isinstance(config, UserInputConfig):  # defensive: registry override
            continue
        schema_props = (compiled.effective_output_schema or {}).get("properties", {}) or {}
        for fld in config.fields:
            owner = f"input node '{node.id}'"
            if fld.key in surface:
                raise CompilationError(
                    f"Workflow input name collision: '{fld.key}' is declared by "
                    f"both {declared_by[fld.key]} and {owner}. The input surface "
                    f"is one flat namespace — rename one of them."
                )
            surface[fld.key] = InputSpec(
                name=fld.key,
                kind=fld.effective_kind(),
                sourcing=fld.effective_sourcing(),  # type: ignore[arg-type]
                variant=fld.effective_variant(),
                default=fld.default,
                label=fld.label or fld.key,
                help=fld.help,
                placeholder=fld.placeholder,
                options=list(fld.options),
                origin="field",
                node_id=node.id,
                field_key=fld.key,
                json_schema=dict(schema_props.get(fld.key, {})),
                edge_fed=bool(compiled.incoming_edge_ids),
                **hint_values(fld),
            )
            declared_by[fld.key] = owner

    for var in definition.variables:
        if var.name in surface:
            raise CompilationError(
                f"Workflow input name collision: variable '{var.name}' shadows "
                f"the input declared by {declared_by[var.name]}. Variables fold "
                f"into the one input surface — rename one of them."
            )
        var_type = var.effective_type()
        kind, variant = compiled_kind_and_variant(var_type, multiple=var.multiple, kind=var.kind)
        surface[var.name] = InputSpec(
            name=var.name,
            kind=kind,
            sourcing="require" if var.default is None else "optional",
            variant=variant,
            default=var.default,
            # Empty when undeclared: every client shows the name in words, never snake_case.
            label=var.label,
            help=var.help or var.description,
            placeholder=var.placeholder,
            options=list(var.options),
            origin="variable",
            json_schema=variable_json_schema(var),
            referenced=var.name in referenced_names,
            **hint_values(var),
        )
        declared_by[var.name] = "the workflow's declared variables"

    return surface


def _compile_step_clock(node_id: str, raw: Any) -> StepClock | None:
    """``data.step_clock`` → :class:`StepClock`, or a CompilationError naming the node."""
    if raw is None:
        return None
    from matrx_graph.knobs import MAX_STEP_SECONDS, MIN_STEP_SECONDS

    if not isinstance(raw, dict):
        raise CompilationError(f"node '{node_id}' has an invalid step_clock: expected an object, got {raw!r}")
    seconds = raw.get("seconds")
    if isinstance(seconds, bool) or not isinstance(seconds, int) or not (
        MIN_STEP_SECONDS <= seconds <= MAX_STEP_SECONDS
    ):
        raise CompilationError(
            f"node '{node_id}' has an invalid step_clock.seconds {seconds!r}: a whole number "
            f"from {MIN_STEP_SECONDS} to {MAX_STEP_SECONDS}"
        )
    knob = raw.get("knob")
    unknown = set(raw) - {"seconds", "knob"}
    if unknown:
        raise CompilationError(f"node '{node_id}' step_clock has unknown keys {sorted(unknown)}")
    if knob is None:
        return StepClock(seconds=seconds)
    if not (
        isinstance(knob, dict)
        and isinstance(knob.get("feature"), str)
        and knob["feature"].strip()
        and isinstance(knob.get("key"), str)
        and knob["key"].strip()
        and set(knob) <= {"feature", "key"}
    ):
        raise CompilationError(
            f"node '{node_id}' has an invalid step_clock.knob {knob!r}: expected {{feature, key}}"
        )
    return StepClock(seconds=seconds, knob_feature=knob["feature"], knob_key=knob["key"])
