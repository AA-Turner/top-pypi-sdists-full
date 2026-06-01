"""Flat step registry — exposes phase steps as a unified DAG.

All step IDs are flat: {phase}.{step_name}
Dependencies are derived from:
- Explicit: step.after list (new in v0.83)
- Implicit (fallback): intra-phase order + inter-phase chain
Topological sort ensures correct execution order.
"""
from __future__ import annotations
from kanban_framework.domain.steps_types import StepDef
from kanban_framework.domain.steps_full import FULL_STEPS
from kanban_framework.domain.steps_lightweight import LIGHTWEIGHT_STEPS
from kanban_framework.domain.steps_quick import QUICK_STEPS
from kanban_framework.infra.scheduler import Scheduler


def _topo_sort(steps: list[dict]) -> list[dict]:
    """Sort steps by topological order (Kahn's algorithm).

    Steps with no dependencies come first. Steps with circular or
    unresolvable dependencies are appended at the end.
    """
    if not steps:
        return []
    ids = {s["id"] for s in steps}
    in_degree: dict[str, int] = {s["id"]: 0 for s in steps}
    adj: dict[str, list[str]] = {s["id"]: [] for s in steps}
    for s in steps:
        for dep in s["dependencies"]:
            if dep in ids:
                in_degree[s["id"]] += 1
                adj[dep].append(s["id"])
    queue = [sid for sid, deg in in_degree.items() if deg == 0]
    result: list[dict] = []
    while queue:
        sid = queue.pop(0)
        s = next(x for x in steps if x["id"] == sid)
        result.append(s)
        for nxt in adj[sid]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    # Append stragglers (circular deps) at the end
    seen = {r["id"] for r in result}
    for s in steps:
        if s["id"] not in seen:
            result.append(s)
    return result


def build_step_dag(lightweight: bool = False, quick: bool = False,
                   custom_order: list[str] | None = None,
                   custom_steps: dict[str, list[StepDef]] | None = None) -> dict:
    """Build a flat step DAG from phase step definitions.

    Returns:
        {"steps": [{"id": "plan.plan_A", "dependencies": [], "description": "...",
                    "agent_type": None, "parallel": False, "user_action": True,
                    "interactive": True, "skippable": True, "phase": "plan"}, ...]}
    """
    if custom_steps is not None and custom_order is not None:
        steps_map = custom_steps
        phase_order = custom_order
    elif quick:
        steps_map = QUICK_STEPS
        phase_order = Scheduler.QUICK_PHASE_ORDER
    elif lightweight:
        steps_map = LIGHTWEIGHT_STEPS
        phase_order = Scheduler.LIGHTWEIGHT_PHASE_ORDER
    else:
        steps_map = FULL_STEPS
        phase_order = Scheduler.PHASE_ORDER

    has_explicit_after = any(
        getattr(s, "after", None) for phase_steps in steps_map.values()
        for s in phase_steps
    )

    # When DAG-driven, use steps_map keys as phase_order fallback
    if has_explicit_after and (not phase_order or len(phase_order) == 0):
        phase_order = list(steps_map.keys())

    steps: list[dict] = []
    prev_step_id: str | None = None

    # Collect all steps into flat list if DAG-driven
    if has_explicit_after:
        seen_ids: set[str] = set()
        for phase in phase_order:
            phase_str = phase.value if hasattr(phase, "value") else str(phase)
            for step in steps_map.get(phase_str, []):
                if step.id in seen_ids:
                    continue
                seen_ids.add(step.id)
                deps = list(step.after) if step.after else []
                steps.append({
                    "id": step.id,
                    "phase": phase_str,
                    "description": step.description,
                    "dependencies": deps,
                    "agent_type": step.agent_type,
                    "parallel": step.parallel,
                    "user_action": step.user_action,
                    "interactive": step.interactive,
                    "spawn_prompt": step.spawn_prompt,
                    "skippable": step.user_action,
                    "type": getattr(step, "type", "action"),
                    "guard": getattr(step, "guard", None),
                    "gateway": getattr(step, "gateway", None),
                    "knowledge": getattr(step, "knowledge", None),
                })
                prev_step_id = step.id
        steps = _topo_sort(steps)
    else:
        for phase in phase_order:
            phase_str = phase.value if hasattr(phase, "value") else str(phase)
            phase_steps = steps_map.get(phase_str, [])
            for i, step in enumerate(phase_steps):
                if i == 0 and prev_step_id:
                    deps = [prev_step_id]
                elif i > 0:
                    deps = [phase_steps[i - 1].id]
                else:
                    deps = []

                steps.append({
                    "id": step.id,
                    "phase": phase_str,
                    "description": step.description,
                    "dependencies": deps,
                    "agent_type": step.agent_type,
                    "parallel": step.parallel,
                    "user_action": step.user_action,
                    "interactive": step.interactive,
                    "spawn_prompt": step.spawn_prompt,
                    "skippable": step.user_action,
                    "type": getattr(step, "type", "action"),
                    "guard": getattr(step, "guard", None),
                    "gateway": getattr(step, "gateway", None),
                    "knowledge": getattr(step, "knowledge", None),
                })
                prev_step_id = step.id

    if has_explicit_after:
        steps = _topo_sort(steps)

    return {"steps": steps, "lightweight": lightweight, "quick": quick}


def get_available_steps(dag: dict, completed: set[str],
                        skipped: set[str] | None = None) -> list[dict]:
    """Return steps whose dependencies are all satisfied and not completed/skipped.

    A dependency is satisfied if it's completed OR skipped.
    """
    skipped = skipped or set()
    satisfied = completed | skipped
    available = []
    for step in dag["steps"]:
        if step["id"] in completed or step["id"] in skipped:
            continue
        if all(dep in satisfied for dep in step["dependencies"]):
            available.append(step)
    return available


def get_all_steps(dag: dict) -> list[dict]:
    """Return a shallow copy of all steps in the DAG."""
    return list(dag["steps"])


def resolve_step(step_id: str) -> tuple[str, str]:
    """Split flat step ID into (phase, step_name)."""
    parts = step_id.split(".", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], ""


def find_step_def(step_id: str, lightweight: bool = False,
                  quick: bool = False, mode: str | None = None) -> StepDef | None:
    """Find the StepDef for a given flat step ID.

    Searches: workflow.json loaded steps → hardcoded builtins.
    """
    if mode and mode not in ("full", "lightweight", "quick"):
        mode = mode
    else:
        mode = "quick" if quick else ("lightweight" if lightweight else "full")
    # Priority 1: workflow.json loaded steps (includes extensions + per-mode)
    from kanban_framework.domain.steps import _get_steps
    try:
        steps_map = _get_steps(mode)
        for phase_steps in steps_map.values():
            for step in phase_steps:
                if step.id == step_id:
                    return step
    except Exception:
        pass
    # Priority 2: hardcoded defaults
    if quick:
        steps_map = QUICK_STEPS
    elif lightweight:
        steps_map = LIGHTWEIGHT_STEPS
    else:
        steps_map = FULL_STEPS
    for phase_steps in steps_map.values():
        for step in phase_steps:
            if step.id == step_id:
                return step
    return None
