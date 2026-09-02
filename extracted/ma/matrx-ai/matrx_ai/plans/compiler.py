"""compile_plan — AgentPlan → matrx_graph.Definition.

Deterministic, pure, no LLM, no DB. Once compiled, the workflow is
IDENTICAL to any other definition — the engine doesn't know or care that
an agent designed it.

Synthesis rules (why each node exists):

Plain step N::

    [deps...] → step_N_args (data.transform) → step_N (ai.agent.start)

  The assembler builds the complete ``{user_input, variables}`` payload in
  one sandboxed expression, because the scheduler's static-input merge is
  top-level shallow — one dict-valued field can't be split between static
  authoring and edge routing. Each dependency edge carries the source's
  whole payload under a namespaced key (``mappings={"src_step_M":
  "$FULL_PAYLOAD"}``) so same-step merges can't collide.

for_each step N::

    [deps...] → step_N_args → step_N_map (control.map, payload_template)
        ├─ sends → step_N (worker, output_channel=step_N_results)
        │            └─ edge → step_N_gather (control.gather)
        └─ conditional (dispatched == 0) → step_N_empty → step_N_gather

  Workers aggregate through an append channel — the only path that
  survives send-driven parallelism (edge routing merges per-target
  last-writer-wins). Gather is triggered by an edge FROM the worker so it
  runs one super-step after the workers, when their channel commits are
  visible. The empty-list pad keeps gather firing (and layer math static)
  when the map dispatches zero items. Both paths deliver gather at exactly
  fire(map)+2. Gather runs join_policy='any': with the default 'all', an
  empty fan-out deadlocks — the worker→gather edge is never resolved
  (zero workers means nothing fires and nothing prunes it), so §12.8
  parks the run ERRORED. 'any' lets whichever branch delivers satisfy
  the join; the other branch is either pruned (pad, non-empty case) or
  simply absent (worker edge, empty case), and gather still fires once.

Layer padding (the correctness-critical piece)::

  Pregel fires a node when ANY incoming edge fires, so a multi-dependency
  join whose sources complete in different super-steps would fire early
  with a partial payload — and our assembler subscripts would then park
  the run on a missing key. The compiler computes a static firing step for
  every node and pads shorter dependency paths with pass-through
  data.transform nodes so every join's sources arrive in the same wave.

when-conditionals ride the FIRST edge of the dependency chain as a
CONDITIONAL edge; a false predicate means the assembler never fires and
the step (plus everything downstream of it) is skipped while the run
completes normally.

Result contract: ``definition.metadata["agent_plan"]["result_map"]`` maps
each plan step to its terminal node id and kind (``single`` → the
AiExecutionResult dump in ``last_outputs``; ``list`` → the gather node's
``values``). The run's raw output stays engine-native; hosts assemble
per-step results from the map.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition

from matrx_ai.plans.errors import PlanIssue, raise_if_issues
from matrx_ai.plans.types import (
    FOR_EACH_MAX_ITEMS,
    AgentPlan,
    PlanStep,
    is_ref,
    parse_ref,
)
from matrx_ai.plans.validate import (
    effective_deps,
    resolve_inputs_path,
    rewrite_when_predicate,
    topological_order,
    validate_plan,
)

AGENT_PLAN_METADATA_KEY = "agent_plan"
AGENT_PLAN_METADATA_VERSION = 1

_X_SPACING = 340.0
_Y_SPACING = 220.0


def compile_plan(plan: AgentPlan) -> Definition:
    """Convert a plan into a standard Definition. Runs the structural gate
    first — an invalid plan raises ``AgentPlanValidationError``."""
    raise_if_issues(validate_plan(plan))

    order = topological_order(plan)
    if order is None:  # pragma: no cover — validate_plan already rejects cycles
        raise_if_issues([PlanIssue(path="steps", message="dependency cycle.")])
        raise AssertionError("unreachable")

    by_num = {s.step: s for s in plan.steps}
    deps_by_step = {n: sorted(d for d in effective_deps(by_num[n]) if d in by_num) for n in order}

    # Static firing layers (see module docstring).
    fire_args: dict[int, int] = {}
    fire_out: dict[int, int] = {}
    for n in order:
        step = by_num[n]
        deps = deps_by_step[n]
        fire_args[n] = 0 if not deps else 1 + max(fire_out[m] for m in deps)
        fire_out[n] = fire_args[n] + (3 if step.for_each is not None else 1)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    channels: list[dict[str, Any]] = []
    entry_nodes: list[str] = []
    result_map: dict[str, dict[str, str]] = {}
    _rows: dict[int, int] = {}

    def _position(fire: int) -> dict[str, float]:
        row = _rows.get(fire, 0)
        _rows[fire] = row + 1
        return {"x": _X_SPACING * fire, "y": _Y_SPACING * row}

    def _add_node(node_id: str, node_type: str, fire: int, data: dict[str, Any]) -> None:
        nodes.append({"id": node_id, "type": node_type, "position": _position(fire), "data": data})

    def _add_edge(
        source: str,
        target: str,
        *,
        mappings: dict[str, str] | None = None,
        condition: str | None = None,
    ) -> None:
        data: dict[str, Any] = {}
        if mappings is not None:
            data["mappings"] = mappings
        if condition is not None:
            data["kind"] = "conditional"
            data["condition"] = condition
        edges.append(
            {"id": f"e__{source}__{target}", "source": source, "target": target, "data": data}
        )

    for n in sorted(by_num):
        step = by_num[n]
        args_id = f"step_{n}_args"
        agent_id = f"step_{n}"
        is_fan_out = step.for_each is not None

        # --- the args assembler ---
        if is_fan_out:
            expression = "{'items': " + _value_expression(step.for_each, plan) + "}"
        else:
            expression = _payload_expression(step, plan)
        _add_node(
            args_id,
            "data.transform",
            fire_args[n],
            {"config": {"expression": expression}, "label": f"Step {n} inputs"},
        )

        # --- dependency edges, padded to equalize arrival ---
        deps = deps_by_step[n]
        if not deps:
            entry_nodes.append(args_id)
        condition = rewrite_when_predicate(step.when) if step.when is not None else None
        for m in deps:
            source = f"step_{m}_gather" if by_num[m].for_each is not None else f"step_{m}"
            gap = fire_args[n] - 1 - fire_out[m]
            first_hop_mappings = {f"src_step_{m}": "$FULL_PAYLOAD"}
            prev = source
            for k in range(1, gap + 1):
                pad_id = f"pad_{m}_to_{n}_{k}"
                _add_node(
                    pad_id,
                    "data.transform",
                    fire_out[m] + k,
                    {"config": {"expression": "inputs"}, "label": f"Sync {m}→{n}"},
                )
                _add_edge(
                    prev,
                    pad_id,
                    mappings=first_hop_mappings if prev == source else None,
                    condition=condition if prev == source else None,
                )
                prev = pad_id
            _add_edge(
                prev,
                args_id,
                mappings=first_hop_mappings if prev == source else None,
                condition=condition if prev == source else None,
            )

        # --- the agent step itself ---
        if is_fan_out:
            map_id = f"step_{n}_map"
            empty_id = f"step_{n}_empty"
            gather_id = f"step_{n}_gather"
            channel = f"step_{n}_results"
            _add_node(
                map_id,
                "control.map",
                fire_args[n] + 1,
                {
                    "config": {
                        "target_node_id": agent_id,
                        "payload_template": _payload_template(step, plan),
                        "max_dispatches": FOR_EACH_MAX_ITEMS,
                    },
                    "label": f"For each — {step.purpose}",
                },
            )
            _add_node(
                agent_id,
                "ai.agent.start",
                fire_args[n] + 2,
                {
                    "input": {"agent_id": str(step.agent_id)},
                    "output_channel": channel,
                    "label": step.purpose,
                },
            )
            _add_node(
                empty_id,
                "data.transform",
                fire_args[n] + 2,
                {"config": {"expression": "{'empty': True}"}, "label": f"Step {n} empty"},
            )
            _add_node(
                gather_id,
                "control.gather",
                fire_args[n] + 3,
                {
                    "config": {"channel": channel, "only_successful": False},
                    "label": f"Step {n} results",
                    # join_policy 'any': gather fires on whichever branch
                    # actually delivers. With the default 'all' policy an
                    # EMPTY fan-out deadlocks — the worker edge
                    # (step_N → gather) is never resolved because zero
                    # workers were dispatched (nothing fires, nothing
                    # prunes; ENGINE_SPEC §12.8 parks the run). 'any' lets
                    # the empty pad's delivery satisfy the join alone; in
                    # the non-empty case the pad's conditional edge is
                    # pruned at the map boundary (no delivery), and gather
                    # fires exactly once when the worker group completes
                    # (§4.4 group resolution still requires ALL items).
                    "join_policy": "any",
                },
            )
            channels.append({"name": channel, "reducer": "append"})
            _add_edge(args_id, map_id)
            _add_edge(agent_id, gather_id)
            _add_edge(map_id, empty_id, condition="inputs['dispatched'] == 0")
            _add_edge(empty_id, gather_id)
            result_map[str(n)] = {"node_id": gather_id, "kind": "list"}
        else:
            _add_node(
                agent_id,
                "ai.agent.start",
                fire_args[n] + 1,
                {"input": {"agent_id": str(step.agent_id)}, "label": step.purpose},
            )
            _add_edge(args_id, agent_id)
            result_map[str(n)] = {"node_id": agent_id, "kind": "single"}

    total_layers = max(fire_out.values()) + 1
    return Definition.model_validate(
        {
            "nodes": nodes,
            "edges": edges,
            "channels": channels,
            "entry_nodes": entry_nodes,
            "metadata": {
                "source": "agent_plan",
                AGENT_PLAN_METADATA_KEY: {
                    "version": AGENT_PLAN_METADATA_VERSION,
                    "plan": plan.model_dump(mode="json"),
                    "result_map": result_map,
                    "layers": total_layers,
                    "max_steps_hint": total_layers + 5,
                },
            },
        }
    )


def _value_expression(value: Any, plan: AgentPlan) -> str:
    """An input value as a sandbox expression. Recurses into nested
    lists/dicts so a ref anywhere in a literal structure still resolves."""
    if is_ref(value):
        ref = parse_ref(value)
        if ref is None:  # pragma: no cover — validate_plan already rejected it
            raise_if_issues([PlanIssue(path="inputs", message=f"unparseable reference {value!r}.")])
            raise AssertionError("unreachable")
        if ref.kind == "inputs":
            resolved, found = resolve_inputs_path(plan.inputs, ref.path)
            if not found:  # pragma: no cover — validate_plan already rejected it
                raise_if_issues([PlanIssue(path="inputs", message=f"{value!r} does not resolve.")])
            return repr(resolved)
        if ref.kind == "steps":
            expr = f"inputs['src_step_{ref.step}']"
            for seg in ref.path:
                expr += f"[{int(seg)}]" if seg.isdigit() else f"[{seg!r}]"
            return expr
    if isinstance(value, dict):
        entries = ", ".join(f"{k!r}: {_value_expression(v, plan)}" for k, v in value.items())
        return "{" + entries + "}"
    if isinstance(value, list):
        return "[" + ", ".join(_value_expression(v, plan) for v in value) + "]"
    return repr(value)


def _payload_expression(step: PlanStep, plan: AgentPlan) -> str:
    """The plain-step assembler expression building {user_input?, variables?}."""
    parts: list[str] = []
    if "user_input" in step.inputs:
        parts.append(f"'user_input': {_value_expression(step.inputs['user_input'], plan)}")
    variables = {k: v for k, v in step.inputs.items() if k != "user_input"}
    if variables:
        entries = ", ".join(
            f"{k!r}: {_value_expression(v, plan)}" for k, v in sorted(variables.items())
        )
        parts.append(f"'variables': {{{entries}}}")
    return "{" + ", ".join(parts) + "}"


def _payload_template(step: PlanStep, plan: AgentPlan) -> dict[str, Any]:
    """The control.map payload_template for a for_each step.

    ``$item`` references pass through as template strings (substituted per
    item by the map executor); ``$inputs`` references are inlined as
    resolved literals; everything else is a literal.
    """

    def _template_value(value: Any) -> Any:
        if is_ref(value):
            ref = parse_ref(value)
            if ref is not None and ref.kind == "item":
                return value  # substituted per item by control.map (G2)
            if ref is not None and ref.kind == "inputs":
                resolved, _found = resolve_inputs_path(plan.inputs, ref.path)
                return resolved
        if isinstance(value, dict):
            return {k: _template_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_template_value(v) for v in value]
        return value

    template: dict[str, Any] = {}
    if "user_input" in step.inputs:
        template["user_input"] = _template_value(step.inputs["user_input"])
    variables = {k: _template_value(v) for k, v in sorted(step.inputs.items()) if k != "user_input"}
    if variables:
        template["variables"] = variables
    return template
