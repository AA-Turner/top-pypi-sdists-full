"""Mission adapter protocol and registry (#1044).

Adapters bridge mission work items to external execution systems.
V1 ships with NoopAdapter for testing and development.
WorkflowAdapter bridges to the workflow engine (#1046).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AdapterStatus:
    state: str
    summary: str = ""
    artifacts: dict[str, Any] = field(default_factory=dict)
    adapter_ref: str | None = None


class MissionAdapter(Protocol):
    async def create(self, *, item: dict[str, Any], context: dict[str, Any]) -> AdapterStatus: ...

    async def status(self, *, adapter_ref: str) -> AdapterStatus: ...

    async def cancel(self, *, adapter_ref: str) -> AdapterStatus: ...


class NoopAdapter:
    async def create(self, *, item: dict[str, Any], context: dict[str, Any]) -> AdapterStatus:
        try:
            return AdapterStatus(state="completed", summary="No-op execution", adapter_ref=str(uuid4()))
        except Exception as exc:
            return AdapterStatus(state="failed", summary=str(exc))

    async def status(self, *, adapter_ref: str) -> AdapterStatus:
        try:
            return AdapterStatus(state="completed")
        except Exception as exc:
            return AdapterStatus(state="failed", summary=str(exc))

    async def cancel(self, *, adapter_ref: str) -> AdapterStatus:
        try:
            return AdapterStatus(state="cancelled")
        except Exception as exc:
            return AdapterStatus(state="failed", summary=str(exc))


# ---------------------------------------------------------------------------
# Workflow status mapping
# ---------------------------------------------------------------------------

_WORKFLOW_STATUS_MAP: dict[str, str] = {
    "pending": "pending",
    "claimed": "pending",
    "running": "running",
    "paused": "running",
    "completed": "completed",
    "failed": "failed",
    "cancelled": "cancelled",
    "blocked": "running",
    "waiting_for_approval": "running",
    "waiting_for_input": "running",
}

_CANCELLABLE_STATES: frozenset[str] = frozenset({"pending", "paused", "waiting_for_approval", "waiting_for_input"})


class WorkflowAdapter:
    """Bridges mission work items to the workflow engine (#1046)."""

    def __init__(self, *, db: Any, engine: Any) -> None:
        self._db = db
        self._engine = engine

    async def create(self, *, item: dict[str, Any], context: dict[str, Any]) -> AdapterStatus:
        try:
            from .workflow_engine import load_definition

            adapter_config: dict[str, Any] = item.get("adapter_config") or {}
            workflow_path: str | None = adapter_config.get("workflow_path")
            if not workflow_path:
                return AdapterStatus(state="failed", summary="Missing workflow_path in adapter_config")

            definition = load_definition(workflow_path)

            inputs: dict[str, Any] = {}
            if context.get("spec_fqn"):
                inputs["spec_fqn"] = context["spec_fqn"]
            if context.get("task_id"):
                inputs["task_id"] = context["task_id"]
            if context.get("task_summary"):
                inputs["task_summary"] = context["task_summary"]
            if context.get("artifact_refs"):
                inputs["artifact_refs"] = context["artifact_refs"]
            extra_inputs: dict[str, Any] = adapter_config.get("extra_inputs") or {}
            inputs.update(extra_inputs)

            run = await self._engine.enqueue_run(
                definition,
                target_kind="mission",
                target_ref=item["id"],
                inputs=inputs,
            )
            return AdapterStatus(state="pending", adapter_ref=run["id"])
        except Exception as exc:
            return AdapterStatus(state="failed", summary=str(exc))

    async def status(self, *, adapter_ref: str) -> AdapterStatus:
        try:
            from . import workflow_storage

            run = workflow_storage.get_workflow_run(self._db, adapter_ref)
            if not run:
                return AdapterStatus(state="failed", summary="Workflow run not found")

            mapped = _WORKFLOW_STATUS_MAP.get(run["status"], "running")
            return AdapterStatus(
                state=mapped,
                summary=run.get("stop_reason") or "",
                adapter_ref=adapter_ref,
            )
        except Exception as exc:
            return AdapterStatus(state="failed", summary=str(exc))

    async def cancel(self, *, adapter_ref: str) -> AdapterStatus:
        try:
            from . import workflow_storage

            run = workflow_storage.get_workflow_run(self._db, adapter_ref)
            if not run:
                return AdapterStatus(state="failed", summary="Workflow run not found")

            current = run["status"]
            if current not in _CANCELLABLE_STATES:
                mapped = _WORKFLOW_STATUS_MAP.get(current, "running")
                return AdapterStatus(
                    state=mapped,
                    summary=f"Cannot cancel workflow in '{current}' state",
                    adapter_ref=adapter_ref,
                )

            workflow_storage.update_workflow_run(self._db, adapter_ref, status="cancelled")
            workflow_storage.release_lock(self._db, run_id=adapter_ref)
            workflow_storage.create_workflow_event(
                self._db,
                run_id=adapter_ref,
                event_type="run_cancelled",
                payload={"source": "mission_adapter"},
            )
            return AdapterStatus(state="cancelled", adapter_ref=adapter_ref)
        except Exception as exc:
            return AdapterStatus(state="failed", summary=str(exc))


class MissionAdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, MissionAdapter] = {}

    def register(self, adapter_type: str, adapter: MissionAdapter) -> None:
        self._adapters[adapter_type] = adapter

    def get(self, adapter_type: str) -> MissionAdapter | None:
        return self._adapters.get(adapter_type)

    def list_types(self) -> list[str]:
        return sorted(self._adapters.keys())


def create_default_adapter_registry(
    *,
    db: Any | None = None,
    engine: Any | None = None,
) -> MissionAdapterRegistry:
    registry = MissionAdapterRegistry()
    registry.register("noop", NoopAdapter())
    if db is not None and engine is not None:
        registry.register("workflow", WorkflowAdapter(db=db, engine=engine))
    return registry
