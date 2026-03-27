"""Mission plan compiler — deterministic and LLM-assisted plan compilation.

Transforms spec artifacts or natural-language prompts into structured mission
plans (``CompiledPlan``), and structured edits into ``CompiledPatch`` operations.
Persistence helpers (``apply_plan``, ``apply_patch``) write results to the
mission storage layer.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from . import artifact_storage, mission_storage
from .spec_schema import SpecPhaseStatus, get_phase_status, parse_spec_content

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Output dataclasses
# ---------------------------------------------------------------------------

_VALID_PATCH_OPS = frozenset(
    {
        "add_item",
        "drop_item",
        "change_priority",
        "change_dependencies",
        "change_adapter_binding",
    }
)

_ACTIVE_STATUSES = frozenset({"active", "running"})


# ---------------------------------------------------------------------------
# Graph validation
# ---------------------------------------------------------------------------


def _validate_dag(nodes: dict[str, list[str]]) -> None:
    """Validate that a dependency graph is a DAG (no cycles, no unknown refs)."""
    all_ids = set(nodes)
    for node_id, deps in nodes.items():
        for dep in deps:
            if dep == node_id:
                raise ValueError(f"Item {node_id!r} has a self-dependency")
            if dep not in all_ids:
                raise ValueError(f"Item {node_id!r} depends on unknown item {dep!r}")

    visited: set[str] = set()
    in_stack: set[str] = set()

    def dfs(node: str) -> None:
        if node in in_stack:
            raise ValueError(f"Circular dependency detected involving item {node!r}")
        if node in visited:
            return
        in_stack.add(node)
        for dep in nodes.get(node, []):
            dfs(dep)
        in_stack.discard(node)
        visited.add(node)

    for node in nodes:
        dfs(node)


@dataclass(frozen=True)
class CompiledItem:
    summary: str
    temp_id: str
    description: str = ""
    priority: int = 50
    item_type: str = "task"
    adapter_type: str = "noop"
    adapter_config: dict[str, Any] = field(default_factory=dict)
    concurrency_group: str | None = None
    lane: str | None = None
    depends_on: list[str] = field(default_factory=list)
    binding_reason: str = ""


@dataclass(frozen=True)
class AdapterDefaults:
    adapter_type: str = "noop"
    adapter_config: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CompiledPlan:
    items: list[CompiledItem]
    title: str = ""
    description: str = ""
    referenced_artifacts: list[dict[str, Any]] = field(default_factory=list)
    execution_profile: str | None = None


@dataclass(frozen=True)
class PatchOperation:
    op: str
    target_item_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    restricted: bool = False


@dataclass(frozen=True)
class CompiledPatch:
    operations: list[PatchOperation]
    referenced_artifacts: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Deterministic: spec → plan
# ---------------------------------------------------------------------------


def compile_from_spec(
    db: ThreadSafeConnection,
    spec_fqn: str,
    *,
    adapter_defaults: AdapterDefaults | None = None,
    execution_profile: Any | None = None,
) -> CompiledPlan:
    art = artifact_storage.get_artifact_by_fqn(db, spec_fqn)
    if art is None:
        raise ValueError(f"Spec artifact not found: {spec_fqn!r}")

    tasks_status = get_phase_status(art.get("metadata", {}), "tasks")
    if tasks_status != SpecPhaseStatus.APPROVED:
        raise ValueError(f"Spec {spec_fqn!r} tasks phase is {tasks_status.value!r}, must be approved")

    spec = parse_spec_content(art["content"])

    if not spec.tasks:
        raise ValueError(f"Spec {spec_fqn!r} has no tasks")

    items: list[CompiledItem] = []
    for task in spec.tasks:
        adapter_type = "noop"
        adapter_config: dict[str, Any] = {}

        if adapter_defaults is not None:
            adapter_type = adapter_defaults.adapter_type
            adapter_config = {
                **adapter_defaults.adapter_config,
                "spec_fqn": spec_fqn,
                "task_id": task.id,
            }

        items.append(
            CompiledItem(
                summary=task.summary,
                temp_id=task.id,
                depends_on=list(task.depends_on),
                adapter_type=adapter_type,
                adapter_config=adapter_config,
            )
        )

    version = art.get("version", 1)
    ref_artifacts = [{"fqn": spec_fqn, "version": version}]

    plan = CompiledPlan(
        items=items,
        title=art.get("name", spec_fqn),
        referenced_artifacts=ref_artifacts,
    )

    if execution_profile is not None:
        from .mission_profiles import apply_execution_profile, discover_workflows

        workflows = discover_workflows()
        plan, _lane_limits = apply_execution_profile(plan, execution_profile, workflows)

    return plan


# ---------------------------------------------------------------------------
# Post-compile: apply adapter defaults
# ---------------------------------------------------------------------------


def apply_adapter_defaults(plan: CompiledPlan, defaults: AdapterDefaults) -> CompiledPlan:
    new_items: list[CompiledItem] = []
    for item in plan.items:
        if item.adapter_type == "noop":
            new_items.append(
                CompiledItem(
                    summary=item.summary,
                    temp_id=item.temp_id,
                    description=item.description,
                    priority=item.priority,
                    item_type=item.item_type,
                    adapter_type=defaults.adapter_type,
                    adapter_config={**defaults.adapter_config, **item.adapter_config},
                    concurrency_group=item.concurrency_group,
                    lane=item.lane,
                    depends_on=list(item.depends_on),
                )
            )
        else:
            new_items.append(item)
    return CompiledPlan(
        items=new_items,
        title=plan.title,
        description=plan.description,
        referenced_artifacts=list(plan.referenced_artifacts),
        execution_profile=plan.execution_profile,
    )


# ---------------------------------------------------------------------------
# LLM-assisted: prompt → plan
# ---------------------------------------------------------------------------

_PLAN_SYSTEM_PROMPT = """\
You are a mission planner. Given a user request, output a JSON object matching this schema:

{
  "title": "short plan title",
  "description": "optional longer description",
  "items": [
    {
      "summary": "task summary",
      "temp_id": "unique_id",
      "description": "",
      "priority": 50,
      "item_type": "task",
      "depends_on": []
    }
  ]
}

Rules:
- Each item must have a unique temp_id (short, snake_case).
- depends_on references other items' temp_id values.
- priority is 1-100 (lower = higher priority).
- Output ONLY valid JSON, no markdown fences, no commentary.
"""


async def compile_from_prompt(
    prompt: str,
    ai_service: Any,
    *,
    adapter_defaults: AdapterDefaults | None = None,
    artifact_context: list[dict[str, Any]] | None = None,
    execution_profile: Any | None = None,
) -> CompiledPlan:
    system = _PLAN_SYSTEM_PROMPT
    if artifact_context:
        system += "\n\nRelevant artifacts:\n" + json.dumps(artifact_context, indent=2)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    raw = await ai_service.complete(messages, max_completion_tokens=2000)

    plan = _parse_plan_json(raw, prompt)

    if artifact_context:
        plan = CompiledPlan(
            items=plan.items,
            title=plan.title,
            description=plan.description,
            referenced_artifacts=list(plan.referenced_artifacts) + list(artifact_context),
        )

    if adapter_defaults is not None:
        plan = apply_adapter_defaults(plan, adapter_defaults)

    if execution_profile is not None:
        from .mission_profiles import apply_execution_profile, discover_workflows

        workflows = discover_workflows()
        plan, _lane_limits = apply_execution_profile(plan, execution_profile, workflows)

    return plan


def _parse_plan_json(raw: str | None, fallback_summary: str) -> CompiledPlan:
    if not raw:
        return _fallback_plan(fallback_summary)

    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("LLM returned invalid JSON for plan, using fallback")
        return _fallback_plan(fallback_summary)

    if not isinstance(data, dict) or "items" not in data:
        logger.warning("LLM JSON missing 'items' key, using fallback")
        return _fallback_plan(fallback_summary)

    items: list[CompiledItem] = []
    for raw_item in data["items"]:
        if not isinstance(raw_item, dict):
            continue
        items.append(
            CompiledItem(
                summary=str(raw_item.get("summary", "")),
                temp_id=str(raw_item.get("temp_id", f"item_{len(items)}")),
                description=str(raw_item.get("description", "")),
                priority=int(raw_item.get("priority", 50)),
                item_type=str(raw_item.get("item_type", "task")),
                depends_on=list(raw_item.get("depends_on", [])),
            )
        )

    if not items:
        return _fallback_plan(fallback_summary)

    return CompiledPlan(
        items=items,
        title=str(data.get("title", "")),
        description=str(data.get("description", "")),
    )


def _fallback_plan(summary: str) -> CompiledPlan:
    return CompiledPlan(
        items=[CompiledItem(summary=summary, temp_id="item_0")],
        title="Plan from prompt",
    )


# ---------------------------------------------------------------------------
# LLM-assisted: patch
# ---------------------------------------------------------------------------

_PATCH_SYSTEM_PROMPT = """\
You are a mission plan editor. Given the current plan state and a user edit request,
output a JSON object with patch operations:

{
  "operations": [
    {
      "op": "add_item",
      "payload": {"summary": "new task", "temp_id": "new_1", "priority": 50, "depends_on": []}
    },
    {
      "op": "drop_item",
      "target_item_id": "existing_item_uuid"
    },
    {
      "op": "change_priority",
      "target_item_id": "existing_item_uuid",
      "payload": {"priority": 10}
    },
    {
      "op": "change_dependencies",
      "target_item_id": "existing_item_uuid",
      "payload": {"depends_on": ["other_uuid"]}
    },
    {
      "op": "change_adapter_binding",
      "target_item_id": "existing_item_uuid",
      "payload": {"adapter_type": "agent", "adapter_config": {}}
    }
  ]
}

Valid ops: add_item, drop_item, change_priority, change_dependencies, change_adapter_binding.
Output ONLY valid JSON, no markdown fences, no commentary.
"""


async def compile_patch(
    prompt: str,
    current_items: list[dict[str, Any]],
    ai_service: Any,
    *,
    artifact_context: list[dict[str, Any]] | None = None,
) -> CompiledPatch:
    system = _PATCH_SYSTEM_PROMPT + "\n\nCurrent plan items:\n" + json.dumps(current_items, indent=2)
    if artifact_context:
        system += "\n\nRelevant artifacts:\n" + json.dumps(artifact_context, indent=2)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    raw = await ai_service.complete(messages, max_completion_tokens=2000)

    patch = _parse_patch_json(raw, current_items)

    if artifact_context:
        patch = CompiledPatch(
            operations=patch.operations,
            referenced_artifacts=list(patch.referenced_artifacts) + list(artifact_context),
        )

    return patch


def _parse_patch_json(raw: str | None, current_items: list[dict[str, Any]]) -> CompiledPatch:
    if not raw:
        return CompiledPatch(operations=[])

    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("LLM returned invalid JSON for patch")
        return CompiledPatch(operations=[])

    if not isinstance(data, dict) or "operations" not in data:
        return CompiledPatch(operations=[])

    item_status_map: dict[str, str] = {}
    for item in current_items:
        item_status_map[item["id"]] = item.get("status", "pending")

    ops: list[PatchOperation] = []
    for raw_op in data["operations"]:
        if not isinstance(raw_op, dict):
            continue
        op_name = str(raw_op.get("op", ""))
        if op_name not in _VALID_PATCH_OPS:
            continue

        target_id = raw_op.get("target_item_id")
        payload = raw_op.get("payload", {})
        if not isinstance(payload, dict):
            payload = {}

        restricted = False
        if target_id and item_status_map.get(target_id) in _ACTIVE_STATUSES:
            restricted = True

        ops.append(
            PatchOperation(
                op=op_name,
                target_item_id=target_id,
                payload=payload,
                restricted=restricted,
            )
        )

    return CompiledPatch(operations=ops)


# ---------------------------------------------------------------------------
# Persistence: apply plan
# ---------------------------------------------------------------------------


def apply_plan(
    db: ThreadSafeConnection,
    plan: CompiledPlan,
    *,
    source_type: str = "prompt",
    source_fqn: str | None = None,
    source_version: int | None = None,
    lane_limits: dict[str, int] | None = None,
) -> dict[str, Any]:
    _validate_dag({item.temp_id: list(item.depends_on) for item in plan.items})

    metadata: dict[str, Any] | None = None
    if plan.execution_profile:
        metadata = {"execution_profile": plan.execution_profile}

    session = mission_storage.create_session(
        db,
        title=plan.title,
        description=plan.description,
        source_type=source_type,
        source_fqn=source_fqn,
        source_version=source_version,
        referenced_artifacts=plan.referenced_artifacts or None,
        lane_limits=lane_limits,
        metadata=metadata,
    )

    temp_to_real: dict[str, str] = {}
    for item in plan.items:
        hold = bool((item.adapter_config or {}).get("_hold_on_create"))
        created = mission_storage.create_item(
            db,
            session_id=session["id"],
            summary=item.summary,
            description=item.description or None,
            priority=item.priority,
            item_type=item.item_type,
            adapter_type=item.adapter_type,
            adapter_config=item.adapter_config or None,
            concurrency_group=item.concurrency_group,
            lane=item.lane,
            hold_requested=hold,
        )
        temp_to_real[item.temp_id] = created["id"]

    for item in plan.items:
        real_id = temp_to_real[item.temp_id]
        for dep_temp_id in item.depends_on:
            dep_real_id = temp_to_real.get(dep_temp_id)
            if dep_real_id:
                mission_storage.add_dependency(db, item_id=real_id, depends_on_id=dep_real_id)

    snapshot = mission_storage.build_plan_snapshot(db, session["id"])
    mission_storage.create_revision(
        db,
        session_id=session["id"],
        revision_number=1,
        operations=[{"op": "initial_plan", "source_type": source_type}],
        plan_snapshot_after=snapshot,
        referenced_artifacts=plan.referenced_artifacts or None,
        reason="initial plan",
    )

    return session


# ---------------------------------------------------------------------------
# Persistence: apply patch
# ---------------------------------------------------------------------------


def apply_patch(
    db: ThreadSafeConnection,
    session_id: str,
    patch: CompiledPatch,
    *,
    allow_restricted: bool = False,
) -> dict[str, Any]:
    if not allow_restricted:
        restricted_ops = [op for op in patch.operations if op.restricted]
        if restricted_ops:
            targets = [op.target_item_id for op in restricted_ops]
            raise ValueError(f"Patch contains operations targeting active items: {targets}")

    session = mission_storage.get_session(db, session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id!r}")

    # Prevalidate all references before any mutation
    existing_items = mission_storage.list_items_by_session(db, session_id)
    existing_ids = {item["id"] for item in existing_items}

    # Collect temp_ids that will be created by add_item ops
    add_temp_ids: set[str] = set()
    for op in patch.operations:
        if op.op == "add_item":
            tid = op.payload.get("temp_id")
            if tid:
                add_temp_ids.add(tid)

    # All valid dependency targets: existing items + temp_ids from this patch
    valid_dep_targets = existing_ids | add_temp_ids

    for op in patch.operations:
        # Non-add ops must target existing items
        if op.op != "add_item" and op.target_item_id:
            if op.target_item_id not in existing_ids:
                raise ValueError(f"Patch op {op.op!r} targets nonexistent item: {op.target_item_id!r}")

        # Validate dependency references in add_item and change_dependencies
        if op.op == "add_item":
            for dep_ref in op.payload.get("depends_on", []):
                if dep_ref not in valid_dep_targets:
                    raise ValueError(f"add_item dependency references unknown item: {dep_ref!r}")
        elif op.op == "change_dependencies" and op.target_item_id:
            for dep_ref in op.payload.get("depends_on", []):
                if dep_ref not in valid_dep_targets:
                    raise ValueError(f"change_dependencies references unknown item: {dep_ref!r}")

    # Build projected graph and validate it is acyclic
    # Start with existing deps, apply add/change/drop ops, check for cycles
    graph: dict[str, list[str]] = {}
    for item in existing_items:
        graph[item["id"]] = mission_storage.get_dependencies(db, item["id"])
    for op in patch.operations:
        if op.op == "add_item":
            tid = op.payload.get("temp_id", "")
            graph[tid] = list(op.payload.get("depends_on", []))
        elif op.op == "change_dependencies" and op.target_item_id:
            graph[op.target_item_id] = list(op.payload.get("depends_on", []))
        elif op.op == "drop_item" and op.target_item_id:
            graph.pop(op.target_item_id, None)
            for node_deps in graph.values():
                if op.target_item_id in node_deps:
                    node_deps.remove(op.target_item_id)
    _validate_dag(graph)

    # Pass 1: create all new items (without dependencies)
    temp_to_real: dict[str, str] = {}

    for op in patch.operations:
        if op.op != "add_item":
            continue
        payload = op.payload
        created = mission_storage.create_item(
            db,
            session_id=session_id,
            summary=str(payload.get("summary", "")),
            description=payload.get("description"),
            priority=int(payload.get("priority", 50)),
            item_type=str(payload.get("item_type", "task")),
            adapter_type=str(payload.get("adapter_type", "noop")),
            adapter_config=payload.get("adapter_config"),
            concurrency_group=payload.get("concurrency_group"),
            lane=payload.get("lane"),
        )
        temp_id = payload.get("temp_id")
        if temp_id:
            temp_to_real[temp_id] = created["id"]

    # Pass 2: wire dependencies for newly added items
    for op in patch.operations:
        if op.op != "add_item":
            continue
        dep_refs = op.payload.get("depends_on", [])
        if not dep_refs:
            continue
        temp_id = op.payload.get("temp_id")
        real_id = temp_to_real.get(temp_id, "") if temp_id else ""
        if not real_id:
            continue
        for dep_id in dep_refs:
            resolved = temp_to_real.get(dep_id, dep_id)
            mission_storage.add_dependency(db, item_id=real_id, depends_on_id=resolved)

    # Pass 3: apply mutation ops
    for op in patch.operations:
        if op.op == "add_item":
            continue  # already handled

        if op.op == "drop_item":
            if op.target_item_id:
                mission_storage.update_item(db, op.target_item_id, status="dropped")

        elif op.op == "change_priority":
            if op.target_item_id:
                new_priority = int(op.payload.get("priority", 50))
                mission_storage.update_item(db, op.target_item_id, priority=new_priority)

        elif op.op == "change_dependencies":
            if op.target_item_id:
                current_deps = mission_storage.get_dependencies(db, op.target_item_id)
                new_deps = op.payload.get("depends_on", [])
                new_deps_resolved = [temp_to_real.get(d, d) for d in new_deps]
                for old_dep in current_deps:
                    if old_dep not in new_deps_resolved:
                        mission_storage.remove_dependency(db, item_id=op.target_item_id, depends_on_id=old_dep)
                for new_dep in new_deps_resolved:
                    if new_dep not in current_deps:
                        mission_storage.add_dependency(db, item_id=op.target_item_id, depends_on_id=new_dep)

        elif op.op == "change_adapter_binding":
            if op.target_item_id:
                updates: dict[str, Any] = {}
                if "adapter_type" in op.payload:
                    updates["adapter_type"] = str(op.payload["adapter_type"])
                if "adapter_config" in op.payload:
                    updates["adapter_config_json"] = op.payload["adapter_config"]
                if updates:
                    mission_storage.update_item(db, op.target_item_id, **updates)

    revisions = mission_storage.list_revisions(db, session_id)
    next_rev = len(revisions) + 1

    snapshot = mission_storage.build_plan_snapshot(db, session_id)
    ops_dicts = [asdict(op) for op in patch.operations]
    mission_storage.create_revision(
        db,
        session_id=session_id,
        revision_number=next_rev,
        operations=ops_dicts,
        plan_snapshot_after=snapshot,
        referenced_artifacts=patch.referenced_artifacts or None,
        reason="patch applied",
    )

    return mission_storage.get_session(db, session_id) or session
