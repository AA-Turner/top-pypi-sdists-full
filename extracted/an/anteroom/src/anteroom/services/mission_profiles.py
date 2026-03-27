"""Mission execution profiles — preference-driven binding selection.

Translates user execution preferences (plan-first, parallel lanes, review
gates, runner preferences) into concrete adapter bindings on compiled mission
items.  Discovers available workflow definitions and scores them against the
profile to select the best fit; falls back gracefully when no workflow matches.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, replace
from typing import Any

from .mission_compiler import CompiledItem, CompiledPlan

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ExecutionProfile dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExecutionProfile:
    """Named execution preferences that drive binding selection."""

    name: str
    description: str = ""
    plan_first: bool = False
    parallel_lanes: bool = False
    review_gate: bool = False
    preferred_runners: list[str] = field(default_factory=list)
    required_inputs: list[str] = field(default_factory=list)
    default_adapter: str = "noop"
    default_adapter_config: dict[str, Any] = field(default_factory=dict)
    lane_limits: dict[str, int] | None = None
    escalation_on_failure: str = "hold"


# ---------------------------------------------------------------------------
# Built-in profile registry
# ---------------------------------------------------------------------------

_BUILTIN_PROFILES: dict[str, ExecutionProfile] = {
    "default": ExecutionProfile(
        name="default",
        description="No special preferences; noop adapter, single lane",
    ),
    "plan-then-execute": ExecutionProfile(
        name="plan-then-execute",
        description="Plan all items first, then execute sequentially",
        plan_first=True,
    ),
    "parallel-review": ExecutionProfile(
        name="parallel-review",
        description="Parallel lanes with review gates on each item",
        parallel_lanes=True,
        review_gate=True,
        preferred_runners=["cli_claude"],
        lane_limits={"default": 3},
    ),
    "hands-off": ExecutionProfile(
        name="hands-off",
        description="Parallel execution, hold on failure for operator triage",
        parallel_lanes=True,
        preferred_runners=["cli_claude"],
        escalation_on_failure="hold",
        lane_limits={"default": 3},
    ),
}


def resolve_profile(name: str) -> ExecutionProfile:
    """Look up a named execution profile. Raises ``ValueError`` if unknown."""
    profile = _BUILTIN_PROFILES.get(name)
    if profile is None:
        available = ", ".join(sorted(_BUILTIN_PROFILES))
        raise ValueError(f"Unknown execution profile: {name!r}. Available: {available}")
    return profile


def list_profiles() -> list[ExecutionProfile]:
    """Return all built-in profiles."""
    return list(_BUILTIN_PROFILES.values())


# ---------------------------------------------------------------------------
# Workflow discovery
# ---------------------------------------------------------------------------


def discover_workflows() -> list[Any]:
    """Enumerate and load all available workflow definitions.

    Returns parsed ``WorkflowDefinition`` objects.  Definitions that fail to
    parse are silently skipped (graceful degradation).
    """
    from .workflow_engine import WorkflowDefinition, load_definition
    from .workflow_resolution import builtin_workflow_dirs

    definitions: list[WorkflowDefinition] = []
    seen_ids: set[str] = set()

    for directory in builtin_workflow_dirs():
        if not directory.is_dir():
            continue
        for yaml_path in sorted(directory.glob("*.yaml")):
            try:
                defn = load_definition(yaml_path)
            except Exception:
                logger.debug("Skipping unparseable workflow: %s", yaml_path)
                continue
            if defn.id not in seen_ids:
                seen_ids.add(defn.id)
                definitions.append(defn)

    return definitions


# ---------------------------------------------------------------------------
# Workflow scoring and selection
# ---------------------------------------------------------------------------

# Weights for scoring criteria
_W_RUNNER = 0.4
_W_INPUT = 0.3
_W_TAG = 0.2
_W_STRUCTURE = 0.1


def score_workflow(definition: Any, profile: ExecutionProfile) -> float:
    """Score a workflow definition against a profile (0.0 to 1.0).

    Criteria:
    - Runner match (0.4): fraction of preferred_runners found in steps
    - Input match (0.3): fraction of required_inputs found in definition inputs
    - Tag match (0.2): overlap between profile name/keywords and definition tags
    - Structure match (0.1): gate steps if review_gate, parallel if parallel_lanes
    """
    scores: list[tuple[float, float]] = []  # (weight, score)

    # Runner match
    if profile.preferred_runners:
        step_runners = {s.runner for s in definition.steps if s.runner}
        matched = sum(1 for r in profile.preferred_runners if r in step_runners)
        scores.append((_W_RUNNER, matched / len(profile.preferred_runners)))
    else:
        scores.append((_W_RUNNER, 0.5))  # neutral when no preference

    # Input match
    if profile.required_inputs:
        defn_inputs = set(definition.inputs.keys())
        matched = sum(1 for i in profile.required_inputs if i in defn_inputs)
        scores.append((_W_INPUT, matched / len(profile.required_inputs)))
    else:
        scores.append((_W_INPUT, 0.5))  # neutral

    # Tag match
    if definition.tags:
        profile_keywords = {profile.name.lower().replace("-", " ")}
        tag_set = {t.lower() for t in definition.tags}
        overlap = len(profile_keywords & tag_set)
        scores.append((_W_TAG, min(overlap / max(len(tag_set), 1), 1.0)))
    else:
        scores.append((_W_TAG, 0.0))

    # Structure match
    structure_score = 0.0
    step_types = {s.type for s in definition.steps}
    if profile.review_gate and "gate" in step_types:
        structure_score += 0.5
    if profile.parallel_lanes and "parallel" in step_types:
        structure_score += 0.5
    if not profile.review_gate and not profile.parallel_lanes:
        structure_score = 0.5  # neutral
    scores.append((_W_STRUCTURE, structure_score))

    total_weight = sum(w for w, _ in scores)
    if total_weight == 0:
        return 0.0
    return sum(w * s for w, s in scores) / total_weight


def select_workflow(
    definitions: list[Any],
    profile: ExecutionProfile,
    *,
    threshold: float = 0.3,
) -> tuple[Any | None, str]:
    """Select the best-fit workflow definition for a profile.

    Returns ``(definition, reason)`` — definition is ``None`` when no workflow
    scores above the threshold.
    """
    if not definitions:
        return None, "no workflow definitions available; using fallback adapter"

    best_defn = None
    best_score = 0.0

    for defn in definitions:
        s = score_workflow(defn, profile)
        if s > best_score:
            best_score = s
            best_defn = defn

    if best_defn is None or best_score < threshold:
        return None, "no workflow matched preferences; using fallback adapter"

    parts = [f"matched workflow '{best_defn.id}'"]
    step_runners = {s.runner for s in best_defn.steps if s.runner}
    runner_overlap = [r for r in profile.preferred_runners if r in step_runners]
    if runner_overlap:
        parts.append(f"runner {', '.join(runner_overlap)} present")
    input_overlap = [i for i in profile.required_inputs if i in best_defn.inputs]
    if input_overlap:
        parts.append(f"input {', '.join(input_overlap)} present")
    parts.append(f"score {best_score:.2f}")

    return best_defn, " — ".join(parts)


# ---------------------------------------------------------------------------
# Apply execution profile to compiled plan
# ---------------------------------------------------------------------------


def apply_execution_profile(
    plan: CompiledPlan,
    profile: ExecutionProfile,
    workflows: list[Any] | None = None,
) -> tuple[CompiledPlan, dict[str, int] | None]:
    """Translate an execution profile into concrete item bindings.

    Returns ``(updated_plan, lane_limits)`` where lane_limits should be set on
    the session.

    Translation rules:
    - Discover and select best-fit workflow; bind noop items to it if matched
    - plan_first: add planning lane, make execution items depend on planning
    - parallel_lanes: assign items to lanes
    - review_gate: insert review gate items after each execution item
    - Does NOT override items with explicitly-set (non-noop) adapter types
    """
    if workflows is None:
        workflows = []

    # --- Binding selection ---
    matched_workflow, binding_reason = select_workflow(workflows, profile)
    lane_limits = dict(profile.lane_limits) if profile.lane_limits else None

    # Resolve workflow ID to a filesystem path for WorkflowAdapter.create(),
    # which passes workflow_path straight to load_definition().
    resolved_workflow_path: str | None = None
    if matched_workflow is not None:
        from .workflow_resolution import resolve_workflow_path

        path = resolve_workflow_path(matched_workflow.id)
        if path is not None:
            resolved_workflow_path = str(path)
        else:
            resolved_workflow_path = matched_workflow.id

    items = list(plan.items)
    new_items: list[CompiledItem] = []

    # --- plan_first: split into planning + execution ---
    planning_ids: list[str] = []
    if profile.plan_first and len(items) > 1:
        planning_item = CompiledItem(
            summary="Plan and prioritize work items",
            temp_id="_planning",
            description="Review and plan all items before execution begins",
            priority=1,
            item_type="planning",
            adapter_type=profile.default_adapter,
            adapter_config={**profile.default_adapter_config, "_binding_reason": "planning phase from profile"},
            lane="planning",
        )
        new_items.append(planning_item)
        planning_ids.append("_planning")

    # --- Process each item ---
    for idx, item in enumerate(items):
        # Determine adapter binding
        if item.adapter_type != "noop":
            # Explicitly set — preserve it
            reason = "explicitly set; not overridden by profile"
            updated = replace(
                item,
                adapter_config={**item.adapter_config, "_binding_reason": reason},
            )
        elif matched_workflow is not None and resolved_workflow_path is not None:
            # Bind to matched workflow using the resolved filesystem path
            config = {
                **profile.default_adapter_config,
                "workflow_path": resolved_workflow_path,
                **item.adapter_config,
                "_binding_reason": binding_reason,
            }
            updated = replace(
                item,
                adapter_type="workflow",
                adapter_config=config,
            )
        else:
            # Fallback to profile default adapter
            config = {
                **profile.default_adapter_config,
                **item.adapter_config,
                "_binding_reason": binding_reason,
            }
            updated = replace(
                item,
                adapter_type=profile.default_adapter,
                adapter_config=config,
            )

        # Assign lane for parallel execution.
        # Use "default" as the lane name so it matches lane_limits keys
        # (the scheduler enforces limits by exact lane name match).
        if profile.parallel_lanes and updated.lane is None:
            updated = replace(updated, lane="default")

        # Add planning dependency
        if planning_ids and updated.temp_id not in planning_ids:
            deps = list(updated.depends_on)
            for pid in planning_ids:
                if pid not in deps:
                    deps.append(pid)
            updated = replace(updated, depends_on=deps)

        new_items.append(updated)

        # Insert review gate after execution item.
        # Gates use hold_requested=True so they block until an operator
        # explicitly resumes them via mission_resume — noop alone would
        # complete instantly and provide no actual gating.
        if profile.review_gate:
            gate_id = f"_review_{updated.temp_id}"
            gate = CompiledItem(
                summary=f"Review: {updated.summary}",
                temp_id=gate_id,
                description=f"Review gate for '{updated.summary}'",
                priority=updated.priority,
                item_type="review",
                adapter_type=profile.default_adapter,
                adapter_config={
                    **profile.default_adapter_config,
                    "_binding_reason": "review gate from profile",
                    "_hold_on_create": True,
                },
                concurrency_group=updated.concurrency_group or f"cg_{updated.temp_id}",
                lane=updated.lane,
                depends_on=[updated.temp_id],
            )
            new_items.append(gate)

    updated_plan = CompiledPlan(
        items=new_items,
        title=plan.title,
        description=plan.description,
        referenced_artifacts=list(plan.referenced_artifacts),
        execution_profile=profile.name,
    )

    return updated_plan, lane_limits
