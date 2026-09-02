"""Kinds for the ``kindcomp_*`` kind-component authoring surface, read half
(KIND_TOOL_LEDGER, ``lead-w2e`` batch 2).

Mirrors the ``tool_component_*`` family's structure for the KIND component
authoring tools (``implementations/kind_component.py``). Reuse of the
``tool_component_context`` / ``tool_component_code`` kinds was REJECTED after
reading both implementations: those declare tool-surface keys (tool metadata,
binding info) these tools never emit, and these carry kind-surface keys
(kind summary, canonical example, dual-gate summary) those never emit —
binding either way would declare a shape the producer does not return.

Sub-projections (kind/example/component summaries) are the same
``kind_shared`` dicts the ``kind_get`` detail nests, so the sub-models are
imported from ``kinds/kind_authoring.py`` — one definition per projection.

Placeholder tier: projections of our own registry rows.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind

from matrx_ai.tools.kinds.kind_authoring import (
    KindComponentSummary,
    KindDefinitionSummary,
    KindExampleSummary,
)


class KindComponentIncidentGroup(KindSubModel):
    """Open render incidents collapsed by error signature."""

    id: str = ""
    component_id: str | None = None
    component_key: str | None = None
    platform: str | None = None
    role: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    error_stack_preview: str | None = None
    component_semver: str | None = None
    has_data_snapshot: bool = False
    first_seen: str | None = None
    last_seen: str | None = None
    occurrence_count: int = 0


class KindComponentContextSummary(KindSubModel):
    """The bundle's one-look summary block."""

    kind: str = ""
    kind_definition_id: str = ""
    kind_version: int | None = None
    is_active: bool = False
    title_key: str | None = None
    has_canonical_example: bool = False
    component_count: int = 0
    #: None for viewers (the incident section is editor-only).
    open_incident_types: int | None = None


@kind(
    "kind_component_context",
    label="Kind Component Context",
    family="kind_components",
    example={
        "kind": {
            "id": "aa11aa11-0000-4000-8000-000000000000",
            "kind": "invoice_summary",
            "label": "Invoice Summary",
            "authoring_owner": None,
            "version": 1,
            "is_active": False,
            "visibility": "private",
            "organization_id": None,
            "created_by": None,
            "emitted_fingerprint": "abc123",
            "has_schema": True,
            "metadata": {},
        },
        "json_schema": {"type": "object"},
        "canonical_example": {"__kind": "invoice_summary", "total": 12.5},
        "canonical_example_status": "passed",
        "examples": [],
        "components": [],
        "component_ids": [],
        "open_incidents": [],
        "incidents_visible": True,
        "props_contract": {},
        "platform_components": {},
        "design_doctrine": "",
        "summary": {
            "kind": "invoice_summary",
            "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
            "kind_version": 1,
            "is_active": False,
            "title_key": None,
            "has_canonical_example": True,
            "component_count": 0,
            "open_incident_types": 0,
        },
    },
    maturity="placeholder",
)
class KindComponentContext(KindModel):
    """``kindcomp_get_context`` — the full component-authoring bundle."""

    kind: KindDefinitionSummary
    json_schema: dict[str, JsonValue] | None = None
    canonical_example: JsonValue | None = None
    canonical_example_status: str | None = None
    examples: list[KindExampleSummary] = []
    components: list[KindComponentSummary] = []
    component_ids: list[str] = []
    #: Editor-only: open incidents deduplicated by error signature.
    open_incidents: list[KindComponentIncidentGroup] = []
    incidents_visible: bool = False
    props_contract: dict[str, str] = {}
    platform_components: dict[str, str] = {}
    design_doctrine: str = ""
    summary: KindComponentContextSummary | None = None


@kind(
    "kind_component_code",
    label="Kind Component Code",
    family="kind_components",
    example={
        "component_id": "ff66ff66-0000-4000-8000-000000000000",
        "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
        "platform": "web",
        "role": "output",
        "component_key": "invoice_card",
        "source": "db",
        "semver": "1.0.0",
        "version": 3,
        "is_default": True,
        "is_active": True,
        "config": {},
        "pinned_kind_version": None,
        "sections_returned": ["component_source", "props_transform"],
        "section_lengths": {"component_source": 1450, "props_transform": 0},
        "sections": {"component_source": "export default function...", "props_transform": ""},
    },
    maturity="placeholder",
)
class KindComponentCode(KindModel):
    """``kindcomp_get_code`` — a component's metadata and code sections."""

    component_id: str = ""
    kind_definition_id: str = ""
    platform: str | None = None
    role: str | None = None
    component_key: str | None = None
    source: str | None = None
    semver: str | None = None
    #: DB-managed integer revision.
    version: int | None = None
    is_default: bool = False
    is_active: bool = False
    config: dict[str, JsonValue] | None = None
    pinned_kind_version: int | None = None
    sections_returned: list[str] = []
    section_lengths: dict[str, int] = {}
    sections: dict[str, str] = {}


# ── the write half of the kindcomp_* family (lead-w2e batch 3) ───────────────


@kind(
    "kind_component_create_result",
    label="Kind Component Created",
    family="kind_components",
    example={
        "component_id": "ff66ff66-0000-4000-8000-000000000000",
        "kind": "invoice_summary",
        "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
        "platform": "web",
        "role": "output",
        "component_key": "invoice_card",
        "semver": "1.0.0",
        "compile_checked": True,
        "compile_note": None,
        "message": "Component 'invoice_card' created for kind 'invoice_summary'.",
    },
    maturity="placeholder",
)
class KindComponentCreateResult(KindModel):
    """Receipt of ``kindcomp_create_component``."""

    component_id: str = ""
    kind: str = ""
    kind_definition_id: str = ""
    platform: str | None = None
    role: str | None = None
    component_key: str | None = None
    semver: str | None = None
    #: False when esbuild is missing and the TSX gate was skipped.
    compile_checked: bool = False
    compile_note: str | None = None
    message: str | None = None


@kind(
    "kind_component_update_result",
    label="Kind Component Updated",
    family="kind_components",
    example={
        "component_id": "ff66ff66-0000-4000-8000-000000000000",
        "updated_sections": ["component_source"],
        "semver": "1.0.1",
        "version": 4,
        "compile_checked": True,
        "message": "Updated 1 section(s).",
        "updated_settings": None,
    },
    maturity="placeholder",
)
class KindComponentUpdateResult(KindModel):
    """ONE union receipt for ``kindcomp_update_code`` and
    ``kindcomp_update_settings`` (the ``tool_component_update_result``
    precedent — branch-only fields optional)."""

    component_id: str = ""
    #: update_code branch: which code sections were replaced.
    updated_sections: list[str] | None = None
    semver: str | None = None
    version: int | None = None
    compile_checked: bool | None = None
    message: str | None = None
    #: update_settings branch: which settings keys were written.
    updated_settings: list[str] | None = None


class KindComponentPatchOutcome(KindSubModel):
    """One applied patch inside a ``kindcomp_patch_code`` run."""

    index: int = 0
    description: str | None = None
    status: str | None = None
    #: Which matching round hit: exact / whitespace / quotes+whitespace.
    match_round: str | None = None


@kind(
    "kind_component_patch_result",
    label="Kind Component Patched",
    family="kind_components",
    example={
        "component_id": "ff66ff66-0000-4000-8000-000000000000",
        "section": "component_source",
        "patches_applied": 1,
        "patch_results": [
            {"index": 0, "description": "patch 1", "status": "applied", "match_round": "exact"}
        ],
        "semver": "1.0.1",
        "version": 5,
        "compile_checked": True,
    },
    maturity="placeholder",
)
class KindComponentPatchResult(KindModel):
    """Receipt of ``kindcomp_patch_code`` — all-or-nothing patch application."""

    component_id: str = ""
    section: str | None = None
    patches_applied: int = 0
    patch_results: list[KindComponentPatchOutcome] = []
    semver: str | None = None
    version: int | None = None
    compile_checked: bool = False


@kind(
    "kind_component_incident_resolution",
    label="Kind Component Incident Resolved",
    family="kind_components",
    example={
        "incident_id": "9977aa00-0000-4000-8000-000000000000",
        "resolved": True,
        "resolved_at": "2026-08-27T02:00:00+00:00",
        "resolution_notes": "Fixed the props contract read.",
    },
    maturity="placeholder",
)
class KindComponentIncidentResolution(KindModel):
    """Receipt of ``kindcomp_resolve_incident``."""

    incident_id: str = ""
    resolved: bool = False
    resolved_at: str | None = None
    resolution_notes: str | None = None
