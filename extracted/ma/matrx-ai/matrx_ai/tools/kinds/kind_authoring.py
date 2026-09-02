"""Kinds for the ``kind_*`` authoring tool family (KIND_TOOL_LEDGER, ``lead-w2e``).

Batch 1 declares the read half: ``kind_definition_detail`` for ``kind_get``
(the full definition view: summary + examples + components + surfaces +
schema). The write half of the family (``kind_create`` / ``kind_update_schema``
/ ...) lands in a later batch.

Placeholder tier: projections of our own registry rows.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind


class KindDefinitionSummary(KindSubModel):
    """The ``kind_shared.kind_summary`` projection of one registry row."""

    id: str = ""
    kind: str = ""
    label: str | None = None
    authoring_owner: str | None = None
    version: int | None = None
    is_active: bool = False
    visibility: str | None = None
    organization_id: str | None = None
    created_by: str | None = None
    emitted_fingerprint: str | None = None
    has_schema: bool = False
    metadata: dict[str, JsonValue] = {}


class KindExampleSummary(KindSubModel):
    """The ``kind_shared.example_summary`` projection of one kind_example row."""

    id: str = ""
    kind_version: int | None = None
    label: str | None = None
    source: str | None = None
    is_canonical: bool = False
    validation_status: str | None = None
    deleted: bool = False


class KindComponentSummary(KindSubModel):
    """The ``kind_shared.component_summary`` projection of one kind_component row."""

    id: str = ""
    kind_definition_id: str = ""
    platform: str | None = None
    role: str | None = None
    component_key: str | None = None
    source: str | None = None
    semver: str | None = None
    version: int | None = None
    is_default: bool = False
    is_active: bool = False
    sort_order: int | None = None
    pinned_kind_version: int | None = None
    has_component_source: bool = False
    has_props_transform: bool = False
    component_source_length: int | None = None
    props_transform_length: int | None = None
    notes: str | None = None
    deleted: bool = False


class KindSurfaceSummary(KindSubModel):
    """One detection surface (token / parser strategy) of the kind."""

    id: str = ""
    surface_type: str | None = None
    token: str | None = None
    parser_strategy: str | None = None
    is_active: bool = False


@kind(
    "kind_definition_detail",
    label="Kind Definition",
    family="kind_authoring",
    example={
        "kind": {
            "id": "aa11aa11-0000-4000-8000-000000000000",
            "kind": "postal_address",
            "label": "Postal Address",
            "authoring_owner": "platform",
            "version": 3,
            "is_active": True,
            "visibility": "public",
            "organization_id": None,
            "created_by": None,
            "emitted_fingerprint": "abc123",
            "has_schema": True,
            "metadata": {"maturity": "verified"},
        },
        "canonical_example": {"__kind": "postal_address", "street": "1 Main St"},
        "examples": [],
        "components": [],
        "surfaces": [],
        "json_schema": {"type": "object"},
    },
    maturity="placeholder",
)
class KindDefinitionDetail(KindModel):
    """``kind_get`` — one kind's full definition view."""

    kind: KindDefinitionSummary
    #: The canonical example's stored data (markers included); None when the
    #: kind has no canonical example.
    canonical_example: JsonValue | None = None
    examples: list[KindExampleSummary] = []
    components: list[KindComponentSummary] = []
    surfaces: list[KindSurfaceSummary] = []
    #: The emitted JSON Schema; None when include_schema=false or unset.
    json_schema: dict[str, JsonValue] | None = None


# ── the write half of the kind_* family (lead-w2e batch 2) ───────────────────


class KindChildEdge(KindSubModel):
    """One composed child kind wired by ``kind_create`` (a kind_edge row)."""

    edge_id: str = ""
    field: str = ""
    child_kind: str = ""
    child_kind_id: str = ""
    is_list: bool = False
    child_created: bool = False


class ComponentAuthoringBundle(KindSubModel):
    """Everything a component author needs, returned by ``kind_create``."""

    props_contract: dict[str, str] = {}
    platform_components: dict[str, str] = {}
    allowed_imports: list[str] = []
    design_doctrine: str = ""
    compile_gate: str = ""


@kind(
    "kind_create_result",
    label="Kind Created",
    family="kind_authoring",
    example={
        "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
        "kind": "invoice_summary",
        "label": "Invoice Summary",
        "version": 1,
        "organization_id": "bb22bb22-0000-4000-8000-000000000000",
        "visibility": "private",
        "platform_kind": False,
        "is_active": False,
        "canonical_example_id": "cc33cc33-0000-4000-8000-000000000000",
        "canonical_example_status": "passed",
        "input_component_id": None,
        "input_component_key": "generic_structured",
        "canonical_example": {"__kind": "invoice_summary", "total": 12.5},
        "children": [],
        "fielded_form": True,
        "form_field_count": 2,
        "json_schema": {"type": "object"},
        "component_authoring": {},
        "message": "Kind 'invoice_summary' created (inactive, private).",
    },
    maturity="placeholder",
)
class KindCreateResult(KindModel):
    """Receipt of ``kind_create`` — the authored (inactive) kind and its assets."""

    kind_definition_id: str = ""
    kind: str = ""
    label: str | None = None
    version: int | None = None
    organization_id: str | None = None
    visibility: str | None = None
    platform_kind: bool = False
    is_active: bool = False
    canonical_example_id: str | None = None
    canonical_example_status: str | None = None
    input_component_id: str | None = None
    input_component_key: str | None = None
    #: The stored canonical example IS the render block (markers included).
    canonical_example: JsonValue | None = None
    canonical_example_included: bool = True
    children: list[KindChildEdge] = []
    fielded_form: bool = False
    form_field_count: int = 0
    json_schema: dict[str, JsonValue] | None = None
    json_schema_included: bool = True
    children_total: int = 0
    children_shown: int = 0
    children_truncated: bool = False
    retrieval_instruction: str | None = None
    component_authoring: ComponentAuthoringBundle | None = None
    message: str | None = None


class StrandedExample(KindSubModel):
    """An example left behind by a schema change (``kind_update_schema``)."""

    id: str = ""
    kind_version: int | None = None
    label: str | None = None
    source: str | None = None
    is_canonical: bool = False
    validation_status: str | None = None
    deleted: bool = False
    #: Why it is stranded: failed_validation or pinned_to_old_kind_version.
    reason: str = ""


@kind(
    "kind_schema_update_result",
    label="Kind Schema Updated",
    family="kind_authoring",
    example={
        "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
        "kind": "invoice_summary",
        "new_version": 2,
        "new_fingerprint": "abc123",
        "example_count": 1,
        "stranded_examples": [],
        "warning": None,
    },
    maturity="placeholder",
)
class KindSchemaUpdateResult(KindModel):
    """Receipt of ``kind_update_schema`` — the new version and its casualties."""

    kind_definition_id: str = ""
    kind: str = ""
    new_version: int | None = None
    new_fingerprint: str | None = None
    example_count: int = 0
    stranded_examples: list[StrandedExample] = []
    warning: str | None = None


@kind(
    "kind_example_result",
    label="Kind Example Added",
    family="kind_authoring",
    example={
        "example_id": "cc33cc33-0000-4000-8000-000000000000",
        "kind": "invoice_summary",
        "kind_version": 1,
        "is_canonical": True,
        "validation_status": "passed",
    },
    maturity="placeholder",
)
class KindExampleResult(KindModel):
    """Receipt of ``kind_add_example`` — the DB trigger's verdict read back."""

    example_id: str = ""
    kind: str = ""
    kind_version: int | None = None
    is_canonical: bool = False
    validation_status: str | None = None


@kind(
    "kind_skill_result",
    label="Kind Skill Created",
    family="kind_authoring",
    example={
        "skill_definition_id": "dd44dd44-0000-4000-8000-000000000000",
        "skill_id": "kind_invoice_summary",
        "kind": "invoice_summary",
        "body_chars": 1450,
        "message": "Skill 'kind_invoice_summary' created — agents can now learn to emit this kind.",
    },
    maturity="placeholder",
)
class KindSkillResult(KindModel):
    """Receipt of ``kind_create_skill`` — the teach-agents-to-emit-it skill."""

    skill_definition_id: str = ""
    skill_id: str = ""
    kind: str = ""
    body_chars: int = 0
    message: str | None = None


@kind(
    "kind_content_block_result",
    label="Kind Content Block Created",
    family="kind_authoring",
    example={
        "render_definition_id": "ee55ee55-0000-4000-8000-000000000000",
        "block_id": "kind-invoice-summary",
        "kind": "invoice_summary",
        "template_chars": 640,
        "message": "Render block 'kind-invoice-summary' created — it now appears in the content-block menu.",
    },
    maturity="placeholder",
)
class KindContentBlockResult(KindModel):
    """Receipt of ``kind_create_content_block`` — the palette render block."""

    render_definition_id: str = ""
    block_id: str = ""
    kind: str = ""
    template_chars: int = 0
    message: str | None = None


@kind(
    "kind_activation_result",
    label="Kind Activation",
    family="kind_authoring",
    example={
        "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
        "kind": "invoice_summary",
        "is_active": True,
        "was_active": False,
        "gated": True,
        "verdict": {"activatable": True},
        "auto_assets": None,
        "note": "Kind is live: it renders through its component and can now be bound to an agent's structured output.",
    },
    maturity="placeholder",
)
class KindActivationResult(KindModel):
    """Receipt of ``kind_activate`` — the dual-gate verdict and the flip."""

    kind_definition_id: str = ""
    kind: str = ""
    is_active: bool = False
    was_active: bool = False
    #: True when the activate direction ran the dual gate (deactivate never is).
    gated: bool = False
    #: content_ir.set_kind_activation's own verdict, verbatim.
    verdict: dict[str, JsonValue] | None = None
    #: Auto-created teach-the-platform assets (skill / content_block receipts).
    auto_assets: dict[str, JsonValue] | None = None
    note: str | None = None
