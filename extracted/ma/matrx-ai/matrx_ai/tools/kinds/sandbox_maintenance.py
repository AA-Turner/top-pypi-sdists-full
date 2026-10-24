"""Kind for the ``sandbox_maintenance`` agent tool (aidream ``tools/sandbox_maintenance_tool.py``):
the bound sandbox's image versus the current one and its health (``status``), an update onto the
current image that keeps the home (``update``), its own logs (``logs``), and the
siblings on its home it may stop (``stop_sibling``), the person's boxes with their homes
(``boxes``) and a reconnect that resumes one onto the conversation (``reconnect``)."""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "sandbox_maintenance_result",
    disposition="record",
    label="Sandbox Maintenance Result",
    family="sandboxes",
    example={
        "action": "status",
        "sandbox_id": "sbx-abc123",
        "tier": "hosted",
        "running_version": "a1b2c3d-20261001T120000Z",
        "current_version": "e4f5a6b-20261022T080000Z",
        "stale": True,
        "healthy": True,
        "update": {"started": False, "outcome": None},
    },
)
class SandboxMaintenanceResult(KindModel):
    action: str = ""
    sandbox_id: str | None = None
    tier: str | None = None
    template: str | None = None
    running_version: str | None = None
    current_version: str | None = None
    stale: bool | None = None
    stale_reason: str | None = None
    healthy: bool | None = None
    health: dict | None = None
    update: dict | None = None
    queued: bool | None = None
    next_step: str | None = None
    source: str | None = None
    logs: str | None = None
    truncated: bool | None = None
    siblings_sharing_home: list[str] | None = None
    stopped: str | None = None
    boxes: list[dict] | None = None
    reconnected: dict | None = None


SANDBOX_MAINTENANCE_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "sandbox_maintenance": SandboxMaintenanceResult
}

__all__ = ["SANDBOX_MAINTENANCE_TOOL_RESULT_KINDS", "SandboxMaintenanceResult"]
