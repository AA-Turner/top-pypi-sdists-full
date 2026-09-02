"""Kinds for the ``toolcomp_*`` tool-component authoring surface.

Ledger rows (KIND_TOOL_LEDGER, agent ``lead-w2d``): the read/create half —
``toolcomp_get_context`` · ``toolcomp_get_code`` · ``toolcomp_get_sample_detail`` ·
``toolcomp_get_incident_detail`` · ``toolcomp_list_tools`` ·
``toolcomp_create_component``. Implementations:
``matrx_ai/tools/implementations/tool_component.py``.

All PLACEHOLDER tier: the payloads are our own registry rows (``tool.definition``,
``tool_ui``, ``tool_ui_incident``, ``tool_test_sample``) — no rich provider data.
Fields that carry STORED JSON authored elsewhere (stream events, snapshots,
arguments, browser info) are ``Any`` by contract, not by neglect: their shape
belongs to the producer, and narrowing them here would fail validation exactly
on the interesting rows (the ``fs_*`` "0 is a claim" trap, type edition).

TWO BRANCH-UNION KINDS (the ``fs_*`` union rule — declare every key any branch
can emit, because the executor enforces ONE declared kind per tool):

- ``tool_component_sample`` — ``toolcomp_get_sample_detail`` returns the
  condensed shape by default and a raw-events shape with ``full_events=true``;
  the same condensed shape also nests inside ``tool_component_context.samples``.
  One kind, both branches, branch-only fields optional.
- ``tool_component_listing`` — ``toolcomp_list_tools`` has a flat paginated
  mode and a grouped mode; one kind, both modes.

``toolcomp_get_code`` keeps its deliberate prompt ergonomics (raw fenced code
blocks, never JSON-escaped strings) via ``ToolResult.provider_content``: the
model still reads the fenced text while ``output`` is the structured kind.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind

_FAMILY = "tool_components"


@kind(
    "tool_component_tool_row",
    label="Tool Listing Row",
    family=_FAMILY,
    example={
        "id": "b2f9…",
        "name": "fs_read",
        "description": "Read a file from the workspace filesystem",
        "category": "core",
        "tags": ["files"],
        "is_active": True,
        "source_kind": "native",
    },
    maturity="placeholder",
)
class ToolComponentToolRow(KindModel):
    """One tool row in a ``toolcomp_list_tools`` result (description capped at 120)."""

    id: str = ""
    name: str = ""
    description: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    is_active: bool | None = None
    source_kind: str | None = None


@kind(
    "tool_component_tool_group",
    label="Tool Listing Group",
    family=_FAMILY,
    example={"count": 1, "tools": []},
    maturity="placeholder",
)
class ToolComponentToolGroup(KindModel):
    """One group of tools in a grouped ``toolcomp_list_tools`` result."""

    count: int = 0
    tools: list[ToolComponentToolRow] = []


@kind(
    "tool_component_listing",
    label="Tool Listing",
    family=_FAMILY,
    example={
        "total_matching": 1,
        "offset": 0,
        "limit": 30,
        "returned": 1,
        "has_more": False,
        "next_offset": None,
        "tools": [
            {
                "__kind": "tool_component_tool_row",
                "id": "b2f9…",
                "name": "fs_read",
                "description": "Read a file",
                "category": "core",
                "tags": None,
                "is_active": True,
                "source_kind": "native",
            }
        ],
        "group_by": None,
        "total_tools": None,
        "group_count": None,
        "groups": None,
    },
    maturity="placeholder",
)
class ToolComponentListing(KindModel):
    """``toolcomp_list_tools`` result — flat paginated mode OR grouped mode."""

    # flat mode
    total_matching: int | None = None
    offset: int | None = None
    limit: int | None = None
    returned: int | None = None
    has_more: bool | None = None
    next_offset: int | None = None
    tools: list[ToolComponentToolRow] | None = None
    # grouped mode
    group_by: str | None = None
    total_tools: int | None = None
    group_count: int | None = None
    groups: dict[str, ToolComponentToolGroup] | None = None


@kind(
    "tool_component_tool_def",
    label="Tool Definition Facts",
    family=_FAMILY,
    example={
        "id": "b2f9…",
        "name": "fs_read",
        "description": "Read a file",
        "parameters": {},
        "output_schema": None,
        "annotations": None,
        "source_kind": "native",
        "managed_by_server_id": None,
        "category": "core",
        "tags": None,
        "icon": None,
        "is_active": True,
        "surface_name": None,
        "is_workflow_component": None,
    },
    maturity="placeholder",
)
class ToolComponentToolDef(KindModel):
    """The tool a component renders — a ``tool.definition`` row projection, or
    the synthesized stub for a workflow emit-to-frontend component (``id=None``,
    ``source_kind='workflow_component'``, stub-only fields set)."""

    id: str | None = None
    name: str = ""
    description: str | None = None
    parameters: Any | None = None
    output_schema: Any | None = None
    annotations: Any | None = None
    source_kind: str | None = None
    managed_by_server_id: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    icon: str | None = None
    is_active: bool | None = None
    # workflow-component stub only
    surface_name: str | None = None
    is_workflow_component: bool | None = None


@kind(
    "tool_component_summary",
    label="Component Summary",
    family=_FAMILY,
    example={
        "id": "c1a2…",
        "tool_name": "fs_read",
        "surface_name": "matrx-default/default",
        "display_name": "File Reader",
        "results_label": None,
        "language": "tsx",
        "semver": "1.0.0",
        "version": 1,
        "is_active": True,
        "keep_expanded_on_stream": False,
        "allowed_imports": ["react"],
        "notes": None,
        "has_inline_code": True,
        "has_overlay_code": False,
        "has_utility_code": False,
        "has_header_extras_code": False,
        "has_header_subtitle_code": False,
        "inline_code_length": 1024,
        "overlay_code_length": 0,
        "created_at": "2026-08-01T00:00:00+00:00",
        "updated_at": None,
    },
    maturity="placeholder",
)
class ToolComponentSummary(KindModel):
    """A ``tool_ui`` row without its code bodies (lengths + presence flags only)."""

    id: str = ""
    tool_name: str | None = None
    surface_name: str | None = None
    display_name: str | None = None
    results_label: str | None = None
    language: str | None = None
    semver: str | None = None
    #: DB-trigger-managed integer revision (snapshots into tool_ui_version).
    version: int | None = None
    is_active: bool | None = None
    keep_expanded_on_stream: bool | None = None
    allowed_imports: list[str] | None = None
    notes: str | None = None
    has_inline_code: bool = False
    has_overlay_code: bool = False
    has_utility_code: bool = False
    has_header_extras_code: bool = False
    has_header_subtitle_code: bool = False
    inline_code_length: int = 0
    overlay_code_length: int = 0
    created_at: str | None = None
    updated_at: str | None = None


@kind(
    "tool_component_sample_event",
    label="Sample Timeline Event",
    family=_FAMILY,
    example={"event": "status_update", "status": "running", "message": "Working…"},
    maturity="placeholder",
)
class ToolComponentSampleEvent(KindModel):
    """One condensed entry in a test sample's event timeline. Value fields are
    ``Any``: they are lifted from stored stream-event JSON the producer owns."""

    event: str = ""
    note: str | None = None
    status: Any | None = None
    message: Any | None = None
    tool_event: Any | None = None
    tool_name: Any | None = None
    inner_event: Any | None = None
    reason: Any | None = None


@kind(
    "tool_component_sample",
    label="Tool Test Sample",
    family=_FAMILY,
    example={
        "id": "s1b2…",
        "is_success": True,
        "use_for_component": True,
        "arguments_used": {"path": "notes.txt"},
        "event_timeline": [
            {"__kind": "tool_component_sample_event", "event": "chunk", "note": "(streaming text)"}
        ],
        "execution_stats": {"duration_ms": 412},
        "output_preview": "hello…",
        "admin_comments": None,
        "sample_id": None,
        "arguments": None,
        "raw_stream_events": None,
        "final_payload": None,
    },
    maturity="placeholder",
)
class ToolComponentSample(KindModel):
    """A ``tool_test_sample`` — the condensed shape (default, and nested in
    ``tool_component_context.samples``) OR the raw ``full_events=true`` shape
    of ``toolcomp_get_sample_detail``. Branch-only fields optional."""

    # condensed branch
    id: str | None = None
    is_success: bool | None = None
    use_for_component: bool | None = None
    arguments_used: Any | None = None
    event_timeline: list[ToolComponentSampleEvent] | None = None
    execution_stats: dict[str, Any] | None = None
    output_preview: str | None = None
    admin_comments: str | None = None
    # full-events branch
    sample_id: str | None = None
    arguments: Any | None = None
    raw_stream_events: Any | None = None
    final_payload: Any | None = None


@kind(
    "tool_component_incident_summary",
    label="Component Incident Summary",
    family=_FAMILY,
    example={
        "id": "i9c8…",
        "component_type": "inline",
        "error_type": "TypeError",
        "error_message": "x is not a function",
        "error_stack_preview": "TypeError: x is not a function\n  at render…",
        "component_version": "1.0.2",
        "resolved": False,
        "resolution_notes": None,
        "tool_update_snapshot_keys": ["output"],
        "first_seen": "2026-08-01T00:00:00+00:00",
        "last_seen": "2026-08-02T00:00:00+00:00",
        "occurrence_count": 3,
    },
    maturity="placeholder",
)
class ToolComponentIncidentSummary(KindModel):
    """One deduped open-incident signature (identical error_type/message/stack
    head collapsed; oldest id kept, occurrences rolled up)."""

    id: str | None = None
    component_type: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    error_stack_preview: str | None = None
    component_version: str | None = None
    resolved: bool | None = None
    resolution_notes: str | None = None
    tool_update_snapshot_keys: list[str] | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    occurrence_count: int = 0


@kind(
    "tool_component_context_summary",
    label="Component Context Summary",
    family=_FAMILY,
    example={
        "tool_id": "b2f9…",
        "tool_name": "fs_read",
        "surface_name": "matrx-default/default",
        "is_workflow_component": False,
        "has_component": True,
        "sample_count": 2,
        "has_reference_sample": True,
        "open_incident_types": 1,
        "open_incident_total_occurrences": 3,
    },
    maturity="placeholder",
)
class ToolComponentContextSummary(KindModel):
    """The at-a-glance facts block of a ``toolcomp_get_context`` result."""

    tool_id: str | None = None
    tool_name: str = ""
    surface_name: str | None = None
    is_workflow_component: bool = False
    has_component: bool = False
    sample_count: int = 0
    has_reference_sample: bool = False
    #: deduped incident signatures (see tool_component_incident_summary)
    open_incident_types: int = 0
    open_incident_total_occurrences: int = 0


@kind(
    "tool_component_context",
    label="Component Context",
    family=_FAMILY,
    example={
        "tool": {"__kind": "tool_component_tool_def", "id": "b2f9…", "name": "fs_read"},
        "components": [],
        "component_ids": [],
        "samples": [],
        "open_incidents": [],
        "summary": {
            "__kind": "tool_component_context_summary",
            "tool_name": "fs_read",
            "has_component": False,
        },
    },
    maturity="placeholder",
)
class ToolComponentContext(KindModel):
    """``toolcomp_get_context`` — the curated everything-bundle for working on
    one tool's UI component: tool facts, component summaries, condensed samples,
    open incidents, and the summary block."""

    tool: ToolComponentToolDef = ToolComponentToolDef()
    components: list[ToolComponentSummary] = []
    component_ids: list[str] = []
    samples: list[ToolComponentSample] = []
    open_incidents: list[ToolComponentIncidentSummary] = []
    summary: ToolComponentContextSummary = ToolComponentContextSummary()


@kind(
    "tool_component_code",
    label="Component Code",
    family=_FAMILY,
    example={
        "component_id": "c1a2…",
        "tool_name": "fs_read",
        "display_name": "File Reader",
        "semver": "1.0.0",
        "version": 1,
        "language": "tsx",
        "allowed_imports": ["react"],
        "sections_returned": ["inline_code"],
        "section_lengths": {"inline_code": 1024},
        "sections": {"inline_code": "export default function …"},
    },
    maturity="placeholder",
)
class ToolComponentCode(KindModel):
    """``toolcomp_get_code`` — the requested code sections plus the metadata
    needed to call patch/update correctly. The prompt still receives the
    labeled fenced-block text via ``provider_content``."""

    component_id: str = ""
    tool_name: str | None = None
    display_name: str | None = None
    semver: str | None = None
    version: int | None = None
    language: str | None = None
    allowed_imports: list[str] | None = None
    sections_returned: list[str] = []
    section_lengths: dict[str, int] = {}
    sections: dict[str, str] = {}


@kind(
    "tool_component_incident_detail",
    label="Component Incident Detail",
    family=_FAMILY,
    example={
        "incident_id": "i9c8…",
        "tool_name": "fs_read",
        "component_id": "c1a2…",
        "component_type": "inline",
        "component_version": "1.0.2",
        "error_type": "TypeError",
        "error_message": "x is not a function",
        "error_stack": "TypeError: x is not a function\n  at render…",
        "browser_info": None,
        "session_id": None,
        "tool_update_snapshot": None,
        "resolved": False,
        "resolution_notes": None,
        "created_at": "2026-08-01T00:00:00+00:00",
    },
    maturity="placeholder",
)
class ToolComponentIncidentDetail(KindModel):
    """``toolcomp_get_incident_detail`` — one full ``tool_ui_incident`` row,
    including the crash-time snapshot the component received."""

    incident_id: str = ""
    tool_name: str | None = None
    component_id: str | None = None
    component_type: str | None = None
    component_version: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    error_stack: str | None = None
    browser_info: Any | None = None
    session_id: str | None = None
    tool_update_snapshot: Any | None = None
    resolved: bool | None = None
    resolution_notes: str | None = None
    created_at: str | None = None


@kind(
    "tool_component_update_result",
    label="Component Updated",
    family=_FAMILY,
    example={
        "component_id": "c1a2…",
        "updated_sections": ["inline_code"],
        "updated_settings": None,
        "semver": "1.0.1",
        "version": 2,
        "updated_at": "2026-08-01T00:00:00+00:00",
        "message": "Successfully updated 1 section(s) on component c1a2….",
    },
    maturity="placeholder",
)
class ToolComponentUpdateResult(KindModel):
    """Receipt for one component update — code sections
    (``toolcomp_update_code``: sections + semver/version/message) or settings
    (``toolcomp_update_settings``: settings + updated_at only). One union kind
    for the two receipts, branch-only fields optional."""

    component_id: str = ""
    #: toolcomp_update_code only
    updated_sections: list[str] | None = None
    #: toolcomp_update_settings only
    updated_settings: list[str] | None = None
    semver: str | None = None
    #: DB-trigger-managed integer revision (auto-bumped on every save).
    version: int | None = None
    updated_at: str | None = None
    message: str | None = None


@kind(
    "tool_component_patch_outcome",
    label="Component Patch Outcome",
    family=_FAMILY,
    example={"index": 0, "description": "patch 1", "status": "applied", "match_round": "exact"},
    maturity="placeholder",
)
class ToolComponentPatchOutcome(KindModel):
    """One applied edit in a ``toolcomp_patch_code`` call."""

    index: int = 0
    description: str = ""
    status: str = ""
    #: which match round landed the old_string (exact / whitespace / quotes).
    match_round: str | None = None


@kind(
    "tool_component_patch_result",
    label="Component Patched",
    family=_FAMILY,
    example={
        "component_id": "c1a2…",
        "section": "inline_code",
        "patches_applied": 1,
        "patch_results": [
            {
                "__kind": "tool_component_patch_outcome",
                "index": 0,
                "description": "patch 1",
                "status": "applied",
                "match_round": "exact",
            }
        ],
        "semver": "1.0.1",
        "version": 2,
        "updated_at": "2026-08-01T00:00:00+00:00",
        "message": "Applied 1 patch(es) to 'inline_code'.",
    },
    maturity="placeholder",
)
class ToolComponentPatchResult(KindModel):
    """``toolcomp_patch_code`` success receipt — every patch applied in order."""

    component_id: str = ""
    section: str = ""
    patches_applied: int = 0
    patch_results: list[ToolComponentPatchOutcome] = []
    semver: str | None = None
    version: int | None = None
    updated_at: str | None = None
    message: str = ""


@kind(
    "tool_component_incident_resolution",
    label="Incident Resolved",
    family=_FAMILY,
    example={
        "incident_id": "i9c8…",
        "resolved": True,
        "resolved_at": "2026-08-01T00:00:00+00:00",
        "resolution_notes": "Fixed the null guard.",
    },
    maturity="placeholder",
)
class ToolComponentIncidentResolution(KindModel):
    """``toolcomp_resolve_incident`` — the receipt for one resolved incident."""

    incident_id: str = ""
    resolved: bool = True
    resolved_at: str = ""
    resolution_notes: str | None = None


@kind(
    "tool_component_create_result",
    label="Component Created",
    family=_FAMILY,
    example={
        "component_id": "c1a2…",
        "tool_id": "b2f9…",
        "tool_name": "fs_read",
        "surface_name": "matrx-default/default",
        "display_name": "File Reader",
        "created_at": "2026-08-01T00:00:00+00:00",
        "message": "Component created for 'fs_read' on surface 'matrx-default/default'.",
    },
    maturity="placeholder",
)
class ToolComponentCreateResult(KindModel):
    """``toolcomp_create_component`` — the receipt for one created component."""

    component_id: str | None = None
    #: NULL for workflow emit-to-frontend components (no backing tool_def row).
    tool_id: str | None = None
    tool_name: str | None = None
    surface_name: str = ""
    display_name: str = ""
    created_at: str | None = None
    message: str = ""
