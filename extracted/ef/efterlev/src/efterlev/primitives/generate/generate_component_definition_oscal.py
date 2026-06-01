"""`generate_component_definition_oscal` primitive — OSCAL 1.0.4 Component-Definition emit.

Companion to `generate_poam_oscal` (v0.1.105). The POA&M says "here are
the gaps"; the Component-Definition says "here is what we implement and
how." Both target OSCAL 1.0.4, both are FedRAMP-current submission
artifacts, both run through the same schema + FedRAMP rule layers
(`validate_oscal_poam` v0.1.106, `validate_oscal_fedramp_rules` v0.1.107).

Scope at v0.1.108: one component (the system), one control-implementation
block, one implemented-requirement per cited control. The implemented-
requirement description is built from the KSI's classification + rationale
— purely deterministic.

v0.1.108.5 enhancement: optional `narratives` dict (KSI ID → narrative
text) populates `implemented-requirement.statements[]` with the
Documentation Agent's per-KSI implementation prose. statement-id
follows the NIST 800-53 convention `<control-id>_smt`. When a KSI
has no narrative, no statements[] are emitted (current behavior;
backward compatible).

Spec reference:
  - https://pages.nist.gov/OSCAL/concepts/layer/implementation/component-definition/
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from efterlev.models.indicator import Indicator
from efterlev.primitives.base import primitive
from efterlev.primitives.generate.generate_poam_markdown import PoamClassificationInput

# Same fixed namespace as POA&M emit so cross-artifact UUID derivation
# is consistent (a CD and a POA&M from the same scan share the system-id
# but emit different per-element UUIDs by design — different concept).
_EFTERLEV_OSCAL_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "efterlev.com/oscal")

_OSCAL_VERSION = "1.0.4"

# OSCAL namespace-qualifies custom prop names. See generate_poam_oscal for
# the rationale (caught by the v0.1.110 NIST oscal-cli gate).
_EFTERLEV_PROP_NS = "https://efterlev.com/ns/oscal"

# NIST 800-53 Rev 5 catalog URL — the canonical source for the controls
# our implemented-requirements reference. FedRAMP 20x layers KSIs on top,
# but the controls themselves are 800-53 Rev 5 by spec.
_NIST_800_53_REV5_CATALOG_URL = (
    "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
    "nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json"
)

# OSCAL component types for a SaaS system. "service" matches FedRAMP
# convention for a SaaS / cloud-service component.
_DEFAULT_COMPONENT_TYPE = "service"


def _det_uuid(*parts: str) -> str:
    """Deterministic UUID derived from input parts. Same inputs → same UUID."""
    return str(uuid.uuid5(_EFTERLEV_OSCAL_NAMESPACE, "|".join(parts)))


# Implementation-status values per OSCAL component conventions. Mirror
# the FRMR / Gap Agent vocabulary so 3PAOs see consistent status
# language across markdown POA&M, OSCAL POA&M, and OSCAL component-def.
_STATUS_TO_OSCAL_IMPL = {
    "implemented": "implemented",
    "partial": "partial",
    "not_implemented": "planned",
    "not_applicable": "not-applicable",
    "evidence_layer_inapplicable": "not-applicable",
}


class GenerateComponentDefinitionOscalInput(BaseModel):
    """Input to `generate_component_definition_oscal`.

    Mirrors `GeneratePoamOscalInput` for shared fields. The CD-specific
    fields (`component_type`, `component_purpose`, `catalog_source`)
    are OSCAL component-definition required-or-recommended-by-spec.
    """

    model_config = ConfigDict(frozen=True)

    classifications: list[PoamClassificationInput]
    indicators: dict[str, Indicator]
    baseline_id: str
    frmr_version: str
    # System identification.
    system_name: str = "Unnamed System (efterlev placeholder)"
    system_id: str = "efterlev-system-default"
    # Component metadata. `service` matches FedRAMP SaaS convention;
    # override for hardware / appliance / interconnection components.
    component_type: str = _DEFAULT_COMPONENT_TYPE
    component_purpose: str = (
        "System component documented from infrastructure-as-code by efterlev. "
        "Implementation statements derived from deterministic detector evidence + "
        "Gap Agent classifications. Reviewer must confirm narrative accuracy "
        "against organizational policy before submission."
    )
    # Catalog source URL. Defaults to NIST 800-53 Rev 5 OSCAL catalog;
    # override when targeting a different control catalog (DoD IL, CMMC).
    catalog_source: str = _NIST_800_53_REV5_CATALOG_URL
    # Optional per-KSI implementation narratives — typically the
    # Documentation Agent's `AttestationDraft.narrative` output. When
    # present, populated into the OSCAL implemented-requirement.statements[]
    # array. Backward compatible: empty dict → no statements emitted.
    # Map shape: {ksi_id: narrative_text}.
    narratives: dict[str, str] = Field(default_factory=dict)
    # Last-modified timestamp; pin for deterministic output.
    last_modified: datetime = Field(default_factory=lambda: datetime.now(UTC))


class GenerateComponentDefinitionOscalOutput(BaseModel):
    """Output: full OSCAL CD JSON document + summary counts."""

    model_config = ConfigDict(frozen=True)

    oscal_document: dict[str, Any]
    component_count: int
    implemented_requirement_count: int
    skipped_unknown_ksi: list[str] = Field(default_factory=list)


@primitive(capability="generate", side_effects=False, version="0.3.0", deterministic=True)
def generate_component_definition_oscal(
    input: GenerateComponentDefinitionOscalInput,
) -> GenerateComponentDefinitionOscalOutput:
    """Emit an OSCAL 1.0.4 Component-Definition JSON document.

    Deterministic: given the same inputs + pinned `last_modified`,
    output is byte-identical (UUIDs derived via uuid5).
    """
    last_modified_iso = input.last_modified.replace(microsecond=0).isoformat()

    skipped_unknown: list[str] = []
    implemented_requirements: list[dict[str, Any]] = []

    # Stable iteration order for byte-stable emit.
    for classification in input.classifications:
        ksi_id = classification.ksi_id
        indicator = input.indicators.get(ksi_id)
        if indicator is None:
            skipped_unknown.append(ksi_id)
            continue

        impl_status = _STATUS_TO_OSCAL_IMPL.get(classification.status, "planned")

        narrative = input.narratives.get(ksi_id)

        # One implemented-requirement per cited control. OSCAL's CD
        # layer expects requirements at the control-id granularity
        # (matches how 3PAO assessors review per-control implementation).
        for control_id in indicator.controls:
            ir_uuid = _det_uuid("ir", input.system_id, ksi_id, control_id)
            ir: dict[str, Any] = {
                "uuid": ir_uuid,
                "control-id": control_id,
                "description": (
                    f"Control {control_id.upper()} is implemented in support "
                    f"of {ksi_id} ({indicator.name}). Status: "
                    f"{classification.status}. Rationale: {classification.rationale}"
                ),
                "props": [
                    {
                        "name": "implementation-status",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": impl_status,
                    },
                    {
                        "name": "weakness-source-identifier",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": ksi_id,
                    },
                    {
                        "name": "frmr-baseline",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": input.baseline_id,
                    },
                ],
            }
            # When a Documentation Agent narrative is present, emit the
            # OSCAL statement structure. statement-id follows the NIST
            # 800-53 convention `<control-id>_smt` for the top-level
            # statement; sub-statements (`_smt.a`, `_smt.b`) would
            # require parsing the catalog's part structure (deferred).
            if narrative:
                statement_uuid = _det_uuid("stmt", input.system_id, ksi_id, control_id)
                ir["statements"] = [
                    {
                        "statement-id": f"{control_id}_smt",
                        "uuid": statement_uuid,
                        "description": narrative,
                    }
                ]
            implemented_requirements.append(ir)

    component_uuid = _det_uuid("component", input.system_id)
    control_impl_uuid = _det_uuid("control-impl", input.system_id, input.baseline_id)

    component = {
        "uuid": component_uuid,
        "type": input.component_type,
        "title": input.system_name,
        "description": (
            f"OSCAL component-definition for {input.system_name} "
            f"({input.system_id}), generated from infrastructure-as-code "
            f"scan against the {input.baseline_id} baseline (FRMR "
            f"{input.frmr_version}). Reviewer must confirm narrative "
            f"accuracy before submission to a 3PAO."
        ),
        "purpose": input.component_purpose,
        "control-implementations": [
            {
                "uuid": control_impl_uuid,
                "source": input.catalog_source,
                "description": (
                    f"Implementation of {input.baseline_id} controls by "
                    f"the {input.system_name} system, evidenced by the "
                    f"detector-derived classifications."
                ),
                "implemented-requirements": implemented_requirements,
            }
        ],
    }

    document = {
        "component-definition": {
            "uuid": _det_uuid("cd-root", input.system_id, input.baseline_id),
            "metadata": {
                "title": f"Component Definition for {input.system_name}",
                "last-modified": last_modified_iso,
                "version": "1.0.0",
                "oscal-version": _OSCAL_VERSION,
                "remarks": (
                    f"Generated by efterlev from FRMR {input.frmr_version} "
                    f"baseline {input.baseline_id}. One implemented-requirement "
                    f"per (KSI x cited control). Implementation-status props "
                    f"derive from Gap Agent classifications."
                ),
            },
            "components": [component],
        }
    }

    return GenerateComponentDefinitionOscalOutput(
        oscal_document=document,
        component_count=1,
        implemented_requirement_count=len(implemented_requirements),
        skipped_unknown_ksi=skipped_unknown,
    )
