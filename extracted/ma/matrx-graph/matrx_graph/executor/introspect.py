"""Input-resolution introspection shared by the scheduler and API callers.

The scheduler validates a node's inputs by merging its authored
``static_inputs`` with the per-invocation payload (edge-routed outputs or a
seeded value) and running the result through ``spec.input_schema``. Anything
that wants to report — BEFORE execution — what a node's inputs WILL be (a
per-node input-status endpoint, a "can this node run yet?" check) must merge
identically, or it will drift from what the scheduler actually validates.

``resolve_invocation_inputs`` is that single merge. Keep it the ONLY place the
merge is spelled, and call it from both the scheduler execute path and the
introspection callers.

Run-variable substitution happens here too — ``{"$var": name}`` references
authored in ``static_inputs`` are resolved against the run's variables
(``initial_variables``) + the graph's declared defaults BEFORE the overlay,
so an edge-routed value for the same key still wins and edge payloads are
never scanned for refs (they are data, not authored references). Strict mode
(the scheduler) raises ``UnresolvedVariableError`` on a reference with no
value and no default; lenient mode (introspection) resolves it to ``None`` so
a status endpoint reports the field unsatisfied instead of erroring.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.types.compiled import CompiledNode
from matrx_graph.types.variables import VariableSpec, resolve_var_refs


def resolve_invocation_inputs(
    node: CompiledNode,
    invocation_inputs: dict[str, Any],
    *,
    run_variables: dict[str, Any] | None = None,
    declared_variables: dict[str, VariableSpec] | None = None,
    strict_variables: bool = True,
    run_inputs: dict[str, Any] | None = None,
    input_surface: dict[str, Any] | None = None,
    run_facts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The exact input dict the scheduler feeds to ``spec.input_schema``.

    Authored ``static_inputs`` first — with ``{"$var": name}`` references
    substituted from ``run_variables`` / declared defaults — overlaid by the
    invocation's inputs (edge-routed payload / seeded values),
    last-writer-wins — identical to the scheduler's own merge at execution
    time.
    """
    static = resolve_var_refs(
        node.static_inputs,
        run_variables=run_variables or {},
        declared=declared_variables or {},
        node_id=node.node_id,
        strict=strict_variables,
        run_inputs=run_inputs,
        input_surface=input_surface,
        run_facts=run_facts,
    )
    merged = dict(static)
    merged.update(invocation_inputs)
    return merged
