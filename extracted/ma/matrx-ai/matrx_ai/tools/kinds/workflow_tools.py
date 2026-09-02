"""Kinds for the workflow-tool family results (KIND_TOOL_LEDGER, ``lead-w2f``).

Ledger rows: ``workflow_catalog`` · ``workflow_author`` · ``workflow_run`` ·
``workflow_node`` · ``workflow_plan``. Implementations live in aidream
(``aidream/tools/workflow_tool.py``, ``aidream/services/workflow_node_agent/
tools.py``, ``aidream/services/workflow_plans/tools.py``); the models live HERE
because ``TOOL_RESULT_KINDS`` may never import aidream.

WHY NOT ``workflow_run_result``
-------------------------------
The ledger-adjacent registered slug ``workflow_run_result`` is the workflow-io
node family's ``SubgraphCallOutput`` — ``{run_id, last_outputs,
channel_values}``, a child run's terminal payload. The ``workflow_run`` TOOL
returns a queue/status/cancel RECEIPT (``run_id``/``job_id``/``status``/
``steps_executed``/…) and never that shape — binding it would declare a shape
it never returns (the trace batch's finding). So this family mints
``workflow_run_status`` instead of reusing.

TWO DOCUMENTED RESHAPES (the ``scope_system`` precedent — a top-level payload
that is some OTHER model's dump cannot join an ``additionalProperties:false``
union):

* ``workflow_catalog``: ``get_node_type`` now wraps the palette entry as
  ``{"node_type": …}`` and ``get_workflow`` wraps the definition row as
  ``{"workflow": …}``.
* ``workflow_node``: ``get_context`` wraps the context bundle as
  ``{"context": …}`` and ``get_agent`` wraps the agent detail as
  ``{"agent": …}``.

All placeholder tier. Union rule (the trace batch's cap-keys finding): every
key any success branch can emit is declared, action-specific keys optional.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "workflow_catalog_result",
    label="Workflow Catalog Result",
    family="workflow_tools",
    example={
        "node_types": [
            {
                "type": "text.template",
                "display_name": "Template",
                "category": "text",
                "description": "Render a template.",
            }
        ],
        "total": 1,
        "hint": "Call get_node_type with a `type` to see its schemas.",
    },
    # PLACEHOLDER — the union of list_node_types / get_node_type /
    # definition_shape / list_workflows / get_workflow.
    maturity="placeholder",
)
class WorkflowCatalogResult(KindModel):
    #: ``list_node_types``.
    node_types: list[dict] | None = None
    total: int | None = None
    #: ``get_node_type`` — the full palette entry (schemas included), wrapped.
    node_type: dict | None = None
    #: ``definition_shape`` — the worked example + its notes.
    example: dict | None = None
    notes: dict | None = None
    example_is_valid: bool | None = None
    #: ``list_workflows``.
    workflows: list[dict] | None = None
    #: ``get_workflow`` — the full definition row, wrapped.
    workflow: dict | None = None
    hint: str | None = None


@kind(
    "workflow_author_result",
    label="Workflow Author Result",
    family="workflow_tools",
    example={"saved": True, "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "My Flow", "version": 1},
    # PLACEHOLDER — validation reports and create/update save receipts.
    maturity="placeholder",
)
class WorkflowAuthorResult(KindModel):
    #: ``validate`` (and the refused-save branch, which returns the report).
    valid: bool | None = None
    issues: list[dict] | None = None
    #: create/update receipt.
    saved: bool | None = None
    id: str | None = None
    name: str | None = None
    version: int | None = None
    #: Plan rows minted for persisted ``plan.step`` anchors.
    plans: list[dict] | None = None
    #: Rulebook provenance-stamp notes (what the platform normalized).
    provenance: list[str] | None = None
    hint: str | None = None


@kind(
    "workflow_run_status",
    label="Workflow Run Status",
    family="workflow_tools",
    example={"run_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "status": "queued", "job_id": "1"},
    # PLACEHOLDER — the run/status/cancel receipt of the queued-lane tool.
    # NOT `workflow_run_result` (SubgraphCallOutput) — see the module docstring.
    maturity="placeholder",
)
class WorkflowRunStatus(KindModel):
    run_id: str = ""
    #: pending/queued/running/completed/failed/cancelling/…
    status: str | None = None
    #: ``run`` receipt only.
    job_id: str | None = None
    steps_executed: int | None = None
    #: The settled run's terminal output / error, when waited for.
    output: JsonValue | None = None
    error: JsonValue | None = None
    hint: str | None = None


@kind(
    "workflow_node_result",
    label="Workflow Node Result",
    family="workflow_tools",
    example={"applied": True, "workflow_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "node_id": "draft"},
    # PLACEHOLDER — the Node Agent's union: context bundle (wrapped), patch
    # receipts, backing-agent read (wrapped) and update receipt.
    maturity="placeholder",
)
class WorkflowNodeResult(KindModel):
    #: ``get_context`` — the node-scoped context bundle, wrapped.
    context: dict | None = None
    #: ``update_node`` / ``patch`` receipt (loud-open: applied=False + issues).
    applied: bool | None = None
    issues: list[str] | None = None
    summary: str | None = None
    workflow_id: str | None = None
    node_id: str | None = None
    updated_at: str | None = None
    #: ``get_agent`` — the backing agent's detail, wrapped.
    agent: dict | None = None
    #: ``update_agent`` receipt.
    updated: bool | None = None
    agent_id: str | None = None
    version: int | None = None
    hint: str | None = None


class PlanView(KindSubModel):
    """One plan as the Steward sees it (``_plan_view``), plus the joint fields
    the ``list`` branch adds. Not registered — tool-local repeated structure."""

    plan_id: str = ""
    definition_id: str = ""
    node_id: str | None = None
    #: Only present when the caller had the definition at hand.
    has_step: bool | None = None
    name: str | None = None
    intent: str | None = None
    notes: str | None = None
    phase: str | None = None
    input_shape: dict | None = None
    output_shape: dict | None = None
    has_internal_graph: bool | None = None
    promoted_definition_id: str | None = None
    allow_stand_in_in_production: bool | None = None
    status: str | None = None
    resolution: dict | None = None
    #: ``list`` branch only. Upstream/downstream are step LABELS (strings) —
    #: measured live 2026-08-26; the first publish guessed dicts and the
    #: executor's catalog check caught it on a real dispatch.
    position_in_workflow: int | None = None
    upstream: list[str] | None = None
    downstream: list[str] | None = None


@kind(
    "workflow_plan_result",
    label="Workflow Plan Result",
    family="workflow_tools",
    example={
        "action": "read",
        "plan": {
            "plan_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "definition_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "node_id": "open_step",
            "name": "The part we cannot do yet",
            "status": "open",
        },
        "samples": [],
    },
    # PLACEHOLDER — one union across the Steward's 15 actions; every branch
    # echoes `action`, everything else is action-specific.
    maturity="placeholder",
)
class WorkflowPlanResult(KindModel):
    action: str = ""
    #: read / update / set_shape / merge / decompose / resolve / dissolve.
    plan: PlanView | None = None
    #: list / split.
    plans: list[PlanView] | None = None
    samples: list[dict] | None = None
    #: ``list`` — the REAL execution order shipped beside the rows.
    reads_as: str | None = None
    workflow_steps: list[dict] | None = None
    #: ``check`` / ``promote``.
    definition_id: str | None = None
    issues: list[dict] | None = None
    compile_error: str | None = None
    #: ``set_sample``.
    scenario: str | None = None
    is_stand_in: bool | None = None
    sample_saved: bool | None = None
    anchor_warning: str | None = None
    #: ``emit``.
    emitted_node_id: str | None = None
    spec_type: str | None = None
    plan_id: str | None = None
    plan_still_active: bool | None = None
    emitted_so_far: int | None = None
    wired: dict | None = None
    wired_note: str | None = None
    handshake_warnings: list[str] | None = None
    #: ``settle``.
    settled: bool | None = None
    node_ids: list[str] | None = None
    emitted_count: int | None = None
    detached_edges: int | None = None
    needs_wiring: list[str] | None = None
    #: ``build_agent``.
    agent_id: str | None = None
    version_id: str | None = None
    next: str | None = None
    #: ``recommend`` (items pass through the specialist's artifact unshaped).
    recommendations: list[JsonValue] | None = None
    gap_description: JsonValue | None = None
    note: str | None = None


__all__ = [
    "WorkflowCatalogResult",
    "WorkflowAuthorResult",
    "WorkflowRunStatus",
    "WorkflowNodeResult",
    "PlanView",
    "WorkflowPlanResult",
]
