"""Validation for AgentPlan — two phases, all issues collected.

``validate_plan`` — structural, pure, synchronous: grammar, dependency
graph, reference placement, $inputs resolution.

``validate_plan_agents`` — agent-aware, async, hits the DB through the
host-injected agx managers: agents exist, caller can use them, input keys
match declared variables, structured_output references require an
output_schema.

``compile_graph(compile_plan(plan))`` is the third, engine-level gate —
run it before creating any row.
"""

from __future__ import annotations

import ast
import re
from typing import Any

from matrx_ai.plans.errors import PlanIssue
from matrx_ai.plans.types import (
    AGENT_PAYLOAD_KEYS,
    FAN_OUT_PAYLOAD_KEYS,
    SCALAR_PAYLOAD_KEYS,
    WHEN_REF_RE,
    AgentPlan,
    ParsedRef,
    PlanStep,
    is_ref,
    iter_ref_strings,
    parse_ref,
)

# Mirror of the matrx-graph sandbox surface (nodes/_sandbox.py) used for
# COMPILE-TIME parse validation of `when` predicates. Deliberately a copy,
# not an import of the private tuple: if the engine sandbox ever tightens,
# the worst case here is a loud runtime EdgeRoutingError instead of a
# compile error — never the reverse (accepting something we then execute).
_SANDBOX_ALLOWED: tuple[type[ast.AST], ...] = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Subscript,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Is,
    ast.IsNot,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.Invert,
)


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def sandbox_expression_error(expr: str) -> str | None:
    """Parse-only mirror of matrx_graph's safe_eval checks. None = OK."""
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        return f"invalid expression syntax: {e.msg}"
    for node in ast.walk(parsed):
        if not isinstance(node, _SANDBOX_ALLOWED):
            return (
                f"disallowed expression element {type(node).__name__!r} — "
                f"only comparisons, boolean/arithmetic operators, literals "
                f"and $steps references are permitted"
            )
        if isinstance(node, ast.Name) and node.id != "inputs":
            return f"unknown name {node.id!r} in condition"
    return None


def rewrite_when_predicate(when: str) -> str:
    """Rewrite ``$steps.M.output.<path>`` tokens to sandbox subscripts.

    The predicate is evaluated by the engine against the SOURCE node's
    output payload, so the step prefix disappears: the path becomes
    ``inputs['a'][0]['b']`` subscripts.
    """

    def _sub(match: Any) -> str:
        raw_path = match.group(2)
        segments = [s for s in raw_path.split(".") if s] if raw_path else []
        expr = "inputs"
        for seg in segments:
            expr += f"[{int(seg)}]" if seg.isdigit() else f"[{seg!r}]"
        return expr

    return WHEN_REF_RE.sub(_sub, when)


def effective_deps(step: PlanStep) -> set[int]:
    """depends_on ∪ every step referenced by inputs / for_each / when."""
    deps = set(step.depends_on)
    for _path, raw in iter_ref_strings(step.inputs):
        ref = parse_ref(raw)
        if ref is not None and ref.kind == "steps" and ref.step is not None:
            deps.add(ref.step)
    if step.for_each and is_ref(step.for_each):
        ref = parse_ref(step.for_each)
        if ref is not None and ref.kind == "steps" and ref.step is not None:
            deps.add(ref.step)
    if step.when:
        for match in WHEN_REF_RE.finditer(step.when):
            deps.add(int(match.group(1)))
    return deps


def topological_order(plan: AgentPlan) -> list[int] | None:
    """Kahn topo sort over effective deps. None when the graph has a cycle."""
    by_num = {s.step: s for s in plan.steps}
    deps = {n: {d for d in effective_deps(s) if d in by_num} for n, s in by_num.items()}
    ordered: list[int] = []
    remaining = dict(deps)
    while remaining:
        ready = sorted(n for n, d in remaining.items() if not d)
        if not ready:
            return None
        for n in ready:
            ordered.append(n)
            del remaining[n]
        for d in remaining.values():
            d.difference_update(ready)
    return ordered


def resolve_inputs_path(inputs: dict[str, Any], path: tuple[str, ...]) -> tuple[Any, bool]:
    """Walk a $inputs path. Returns (value, found)."""
    value: Any = inputs
    for seg in path:
        if isinstance(value, dict) and seg in value:
            value = value[seg]
        elif isinstance(value, list) and seg.isdigit() and int(seg) < len(value):
            value = value[int(seg)]
        else:
            return None, False
    return value, True


def validate_plan(plan: AgentPlan) -> list[PlanIssue]:
    """Structural validation. Returns ALL issues (empty = valid)."""
    issues: list[PlanIssue] = []
    seen_steps: set[int] = set()
    for s in plan.steps:
        if s.step in seen_steps:
            issues.append(
                PlanIssue(
                    path="steps",
                    step=s.step,
                    message=f"duplicate step number {s.step} — step numbers must be unique.",
                )
            )
        seen_steps.add(s.step)
    defined = {s.step for s in plan.steps}
    by_num = {s.step: s for s in plan.steps}

    for s in plan.steps:
        prefix = f"steps[{s.step}]"

        for dep in s.depends_on:
            if dep == s.step:
                issues.append(
                    PlanIssue(path=f"{prefix}.depends_on", step=s.step,
                              message="a step cannot depend on itself.")
                )
            elif dep not in defined:
                issues.append(
                    PlanIssue(path=f"{prefix}.depends_on", step=s.step,
                              message=f"depends_on references undefined step {dep}.")
                )

        for key in s.inputs:
            if not _IDENTIFIER_RE.match(key):
                issues.append(
                    PlanIssue(path=f"{prefix}.inputs.{key}", step=s.step,
                              message=f"input key {key!r} is not a valid identifier.")
                )
        for ref_path, raw in iter_ref_strings(s.inputs):
            kpath = f"{prefix}.inputs.{ref_path}"
            ref = parse_ref(raw)
            if ref is None:
                issues.append(
                    PlanIssue(
                        path=kpath, step=s.step,
                        message=(
                            f"{raw!r} looks like a reference but does not match the "
                            f"grammar ($inputs.<path> | $steps.<n>.output[.<path>] | "
                            f"$item[.<path>])."
                        ),
                    )
                )
                continue
            issues.extend(_check_ref(ref, raw, kpath, s, plan, defined))
            issues.extend(_check_payload_path(ref, raw, kpath, s, by_num))

        if s.for_each is not None:
            fpath = f"{prefix}.for_each"
            ref = parse_ref(s.for_each) if is_ref(s.for_each) else None
            if ref is None:
                issues.append(
                    PlanIssue(path=fpath, step=s.step,
                              message="for_each must be a $inputs or $steps reference resolving to a list.")
                )
            elif ref.kind == "item":
                issues.append(
                    PlanIssue(path=fpath, step=s.step,
                              message="for_each cannot reference $item.")
                )
            elif ref.kind == "steps":
                if ref.step == s.step:
                    issues.append(
                        PlanIssue(path=fpath, step=s.step,
                                  message="for_each cannot reference the step itself.")
                    )
                elif ref.step not in defined:
                    issues.append(
                        PlanIssue(path=fpath, step=s.step,
                                  message=f"for_each references undefined step {ref.step}.")
                    )
                else:
                    issues.extend(_check_payload_path(ref, s.for_each, fpath, s, by_num))
            elif ref.kind == "inputs":
                value, found = resolve_inputs_path(plan.inputs, ref.path)
                if not found:
                    issues.append(
                        PlanIssue(path=fpath, step=s.step,
                                  message=f"{s.for_each!r} does not resolve against plan.inputs.")
                    )
                elif not isinstance(value, list):
                    issues.append(
                        PlanIssue(
                            path=fpath, step=s.step,
                            message=(
                                f"{s.for_each!r} resolves to {type(value).__name__}, "
                                f"but for_each requires a list."
                            ),
                        )
                    )

        if s.when is not None:
            wpath = f"{prefix}.when"
            deps = {d for d in effective_deps(s) if d in defined}
            when_steps = {int(m.group(1)) for m in WHEN_REF_RE.finditer(s.when)}
            if len(deps) != 1:
                issues.append(
                    PlanIssue(
                        path=wpath, step=s.step,
                        message=(
                            f"when requires exactly one dependency (this step has "
                            f"{len(deps)}: {sorted(deps)}) — the condition is evaluated "
                            f"against that dependency's output."
                        ),
                    )
                )
            elif when_steps - deps:
                issues.append(
                    PlanIssue(
                        path=wpath, step=s.step,
                        message=(
                            f"when may only reference the step's single dependency "
                            f"{next(iter(deps))}, got {sorted(when_steps)}."
                        ),
                    )
                )
            elif not when_steps:
                issues.append(
                    PlanIssue(path=wpath, step=s.step,
                              message="when must reference $steps.<dep>.output.<path> at least once.")
                )
            else:
                error = sandbox_expression_error(rewrite_when_predicate(s.when))
                if error:
                    issues.append(PlanIssue(path=wpath, step=s.step, message=error))
                for match in WHEN_REF_RE.finditer(s.when):
                    ref = parse_ref(match.group(0))
                    if ref is not None:
                        issues.extend(
                            _check_payload_path(ref, match.group(0), wpath, s, by_num)
                        )

    # Non-finite floats (NaN/Infinity survive json.loads) compile to bare
    # names the sandbox rejects only at EXECUTION time — i.e. after upstream
    # paid calls. Reject them at the gate.
    issues.extend(_nonfinite_issues(plan.inputs, "inputs", None))
    for s in plan.steps:
        issues.extend(_nonfinite_issues(s.inputs, f"steps[{s.step}].inputs", s.step))

    if topological_order(plan) is None:
        issues.append(
            PlanIssue(path="steps", message="the dependency graph contains a cycle.")
        )
    return issues


def _nonfinite_issues(value: Any, path: str, step: int | None) -> list[PlanIssue]:
    import math

    issues: list[PlanIssue] = []
    if isinstance(value, float) and not math.isfinite(value):
        issues.append(
            PlanIssue(path=path, step=step,
                      message=f"non-finite number ({value}) is not a valid input value.")
        )
    elif isinstance(value, dict):
        for k, v in value.items():
            issues.extend(_nonfinite_issues(v, f"{path}.{k}", step))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            issues.extend(_nonfinite_issues(v, f"{path}[{i}]", step))
    return issues


def _agent_record_path_error(path: tuple[str, ...], source_step: int) -> str | None:
    """Validate a path into an AiExecutionResult payload beyond depth 1.

    Depth-1-only checking let ``$steps.1.output.final_text.foo`` and
    ``$steps.2.output.values.final_text`` through the gate to die at runtime
    AFTER the source's paid call (2026-07-07 review finding)."""
    first = path[0]
    if first not in AGENT_PAYLOAD_KEYS:
        return (
            f"the payload is the agent execution record (final_text, "
            f"structured_output, usage, ...) — there is no {first!r} key. The "
            f"agent's own JSON fields live under structured_output: did you mean "
            f"$steps.{source_step}.output.structured_output.{'.'.join(path)}?"
        )
    if first in SCALAR_PAYLOAD_KEYS and len(path) > 1:
        return (
            f"{first!r} is a scalar — the path cannot continue past it "
            f"('{'.'.join(path)}')."
        )
    if first == "messages" and len(path) > 1 and not path[1].isdigit():
        return "'messages' is a list — index it: messages.<i>.<field>."
    return None


def _check_payload_path(
    ref: ParsedRef,
    raw: str,
    kpath: str,
    step: PlanStep,
    by_num: dict[int, PlanStep],
) -> list[PlanIssue]:
    """A $steps ref's path must exist on the source step's ACTUAL payload.
    This is the rule that catches ``$steps.1.output.cards`` at the gate
    instead of a runtime ``KeyError: 'cards'`` after the source step's
    (paid) LLM call already ran — the 2026-07-07 incident."""
    if ref.kind != "steps" or not ref.path or ref.step is None:
        return []
    source = by_num.get(ref.step)
    if source is None or ref.step == step.step:
        return []  # _check_ref already reports undefined/self refs

    error: str | None
    if source.for_each is not None:
        first = ref.path[0]
        if first not in FAN_OUT_PAYLOAD_KEYS:
            error = (
                f"step {ref.step} is a for_each step — its payload is "
                f"{{values, count}} (values = the list of per-item agent results). "
                f"Use $steps.{ref.step}.output.count or "
                f"$steps.{ref.step}.output.values.<i>.<field>."
            )
        elif first == "count" and len(ref.path) > 1:
            error = "'count' is a scalar — the path cannot continue past it."
        elif first == "values" and len(ref.path) > 1 and not ref.path[1].isdigit():
            error = (
                f"'values' is the per-item list — did you forget the item index? "
                f"Use $steps.{ref.step}.output.values.<i>.{'.'.join(ref.path[1:])}."
            )
        elif first == "values" and len(ref.path) > 2:
            # Each item is itself an agent execution record.
            error = _agent_record_path_error(ref.path[2:], ref.step)
        else:
            error = None
    else:
        error = _agent_record_path_error(ref.path, ref.step)

    if error is None:
        return []
    return [PlanIssue(path=kpath, step=step.step, message=f"{raw!r}: {error}")]


def schema_path_error(
    output_schema: Any, path: tuple[str, ...]
) -> str | None:
    """Walk a ``structured_output.<path>`` suffix through an agent's
    output_schema (the ``{name, schema: {...}}`` envelope as stored on
    agent rows, or a bare JSON Schema). Returns an error string when a
    segment provably doesn't exist; stays permissive when the schema
    fragment is opaque (no properties/items)."""
    if not isinstance(output_schema, dict):
        return None
    node: Any = output_schema.get("schema", output_schema)
    for seg in path:
        if not isinstance(node, dict):
            return None
        if seg.isdigit():
            items = node.get("items")
            if node.get("type") == "array" or isinstance(items, dict):
                node = items if isinstance(items, dict) else None
                continue
            return f"segment {seg!r} indexes into a non-array schema node."
        properties = node.get("properties")
        if isinstance(properties, dict):
            if seg in properties:
                node = properties[seg]
                continue
            known = ", ".join(sorted(properties)) or "(none)"
            return f"no field {seg!r} in the agent's output schema. Available fields: {known}."
        return None  # opaque fragment — permissive
    return None


def resolved_schema_node(output_schema: Any, path: tuple[str, ...]) -> Any:
    """Best-effort: the schema node a structured_output path lands on."""
    if not isinstance(output_schema, dict):
        return None
    node: Any = output_schema.get("schema", output_schema)
    for seg in path:
        if not isinstance(node, dict):
            return None
        if seg.isdigit():
            node = node.get("items")
            continue
        properties = node.get("properties")
        node = properties.get(seg) if isinstance(properties, dict) else None
    return node


def _check_ref(
    ref: ParsedRef,
    raw: str,
    kpath: str,
    step: PlanStep,
    plan: AgentPlan,
    defined: set[int],
) -> list[PlanIssue]:
    issues: list[PlanIssue] = []
    if ref.kind == "item":
        if step.for_each is None:
            issues.append(
                PlanIssue(path=kpath, step=step.step,
                          message="$item is only valid inside a for_each step.")
            )
    elif ref.kind == "steps":
        if step.for_each is not None:
            issues.append(
                PlanIssue(
                    path=kpath, step=step.step,
                    message=(
                        "a for_each step's inputs may only use $item, $inputs and "
                        "literals — cross-step references cannot vary per item. "
                        "Reference the other step's output via for_each itself, or "
                        "split into a separate step."
                    ),
                )
            )
        elif ref.step == step.step:
            issues.append(
                PlanIssue(path=kpath, step=step.step,
                          message="a step cannot reference its own output.")
            )
        elif ref.step not in defined:
            issues.append(
                PlanIssue(path=kpath, step=step.step,
                          message=f"{raw!r} references undefined step {ref.step}.")
            )
    elif ref.kind == "inputs":
        _, found = resolve_inputs_path(plan.inputs, ref.path)
        if not found:
            issues.append(
                PlanIssue(path=kpath, step=step.step,
                          message=f"{raw!r} does not resolve against plan.inputs.")
            )
    return issues


async def validate_plan_agents(plan: AgentPlan, app_ctx: Any) -> list[PlanIssue]:
    """Agent-aware validation. Requires host-injected DB models (agx managers)."""
    from matrx_ai.db.agx_manager import agx_agent_manager_instance

    issues: list[PlanIssue] = []
    rows: dict[str, Any] = {}
    for s in plan.steps:
        agent_id = str(s.agent_id)
        if agent_id in rows:
            continue
        try:
            rows[agent_id] = await agx_agent_manager_instance.load_by_id(agent_id)
        except Exception as e:  # noqa: BLE001 — manager raises on missing/DB error
            rows[agent_id] = None
            issues.append(
                PlanIssue(
                    path=f"steps[{s.step}].agent_id", step=s.step,
                    message=f"agent {agent_id} could not be loaded: {type(e).__name__}: {e}",
                )
            )

    # Every $steps ref that reaches into structured_output, with where it
    # came from — nested input values, for_each and when included. The
    # for_each origin is an EXPLICIT flag: matching on the kpath string
    # misfired on nested input keys literally named "for_each".
    structured_refs: list[tuple[PlanStep, str, str, ParsedRef, bool]] = []
    for s in plan.steps:
        candidates: list[tuple[str, str, bool]] = [
            (f"steps[{s.step}].inputs.{p}", raw, False)
            for p, raw in iter_ref_strings(s.inputs)
        ]
        if s.for_each and is_ref(s.for_each):
            candidates.append((f"steps[{s.step}].for_each", s.for_each, True))
        if s.when:
            candidates.extend(
                (f"steps[{s.step}].when", m.group(0), False)
                for m in WHEN_REF_RE.finditer(s.when)
            )
        for kpath, raw, is_for_each in candidates:
            ref = parse_ref(raw)
            if (
                ref is not None
                and ref.kind == "steps"
                and ref.step is not None
                and "structured_output" in ref.path
            ):
                structured_refs.append((s, kpath, raw, ref, is_for_each))

    by_num = {s.step: s for s in plan.steps}
    for s in plan.steps:
        prefix = f"steps[{s.step}]"
        row = rows.get(str(s.agent_id))
        if row is None:
            continue

        # Access: admin / owner / canonical viewer-level access — same policy as
        # agent_call._can_access (viewer access = may run, per the 2026-08-12
        # is_public-cut ruling; iam.has_access_for owns the ladder).
        is_admin = bool(getattr(app_ctx, "is_admin", False))
        user_id = getattr(app_ctx, "user_id", None)
        is_owner = bool(user_id) and str(getattr(row, "created_by", "") or "") == str(user_id)
        has_viewer = False
        if not (is_admin or is_owner) and user_id:
            from matrx_ai.db.agx_manager import agent_viewer_access

            has_viewer = await agent_viewer_access(str(s.agent_id), str(user_id))
        if not (is_admin or is_owner or has_viewer):
            issues.append(
                PlanIssue(path=f"{prefix}.agent_id", step=s.step,
                          message=f"you do not have access to agent {s.agent_id}.")
            )
            continue
        if getattr(row, "is_active", True) is False or getattr(row, "is_archived", False):
            issues.append(
                PlanIssue(path=f"{prefix}.agent_id", step=s.step,
                          message=f"agent {s.agent_id} is inactive or archived.")
            )
            continue

        declared: dict[str, dict[str, Any]] = {}
        for entry in getattr(row, "variable_definitions", None) or []:
            if isinstance(entry, dict) and entry.get("name"):
                declared[str(entry["name"])] = entry
        for key in s.inputs:
            if key == "user_input":
                continue
            if key not in declared:
                known = ", ".join(sorted(declared)) or "(none)"
                issues.append(
                    PlanIssue(
                        path=f"{prefix}.inputs.{key}", step=s.step,
                        message=(
                            f"agent {getattr(row, 'name', s.agent_id)} has no variable "
                            f"{key!r}. Declared variables: {known}. Free text goes in "
                            f"'user_input'."
                        ),
                    )
                )
        for name, entry in declared.items():
            if entry.get("required") and name not in s.inputs:
                issues.append(
                    PlanIssue(
                        path=f"{prefix}.inputs", step=s.step,
                        message=(
                            f"agent {getattr(row, 'name', s.agent_id)} requires variable "
                            f"{name!r} but this step does not supply it."
                        ),
                    )
                )

    for consumer, kpath, raw, ref, is_for_each in structured_refs:
        source = by_num.get(ref.step or -1)
        if source is None:
            continue
        row = rows.get(str(source.agent_id))
        if row is None:
            continue
        schema = getattr(row, "output_schema", None)
        if not isinstance(schema, dict) or not schema:
            issues.append(
                PlanIssue(
                    path=kpath, step=consumer.step,
                    message=(
                        f"{raw!r}: agent {getattr(row, 'name', source.agent_id)} "
                        f"(step {ref.step}) has no output_schema — structured_output "
                        f"is always null for it. Use final_text, or pick an agent "
                        f"with structured output."
                    ),
                )
            )
            continue
        # Validate the path INSIDE structured_output against the agent's
        # declared schema — the second layer of the KeyError-at-runtime
        # extinction (the first is _check_payload_path).
        so_index = ref.path.index("structured_output")
        inner = ref.path[so_index + 1 :]
        if inner:
            error = schema_path_error(schema, inner)
            if error:
                issues.append(
                    PlanIssue(
                        path=kpath, step=consumer.step,
                        message=(
                            f"{raw!r}: {error} (agent "
                            f"{getattr(row, 'name', source.agent_id)}, step {ref.step})"
                        ),
                    )
                )
                continue
        # for_each over a structured_output path must land on an array.
        if is_for_each:
            node = resolved_schema_node(schema, inner)
            node_type = node.get("type") if isinstance(node, dict) else None
            if isinstance(node_type, str) and node_type != "array":
                issues.append(
                    PlanIssue(
                        path=kpath, step=consumer.step,
                        message=(
                            f"{raw!r} resolves to type {node_type!r} in the agent's "
                            f"output schema, but for_each requires a list."
                        ),
                    )
                )
    return issues
