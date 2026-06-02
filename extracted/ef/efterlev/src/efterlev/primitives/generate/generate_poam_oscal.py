"""`generate_poam_oscal` primitive — OSCAL 1.0.4 POA&M JSON assembly.

Companion to `generate_poam_markdown` (v0.1.x). Same input shape, same
data model, different output: OSCAL 1.0.4 plan-of-action-and-milestones
JSON conforming to the GSA fedramp-automation rule set + the upstream
NIST OSCAL JSON schema.

OSCAL background: NIST's Open Security Controls Assessment Language
is the standardized JSON/XML interchange format for compliance
documentation. FedRAMP 20x (RFC-0024 expected Sep 2026) targets OSCAL
as the submission format. 3PAOs increasingly want OSCAL inputs because
their GRC tools ingest it directly.

Why 1.0.4: FedRAMP's current published guidance + GSA's validation
rule set both target OSCAL 1.0.4. OSCAL 1.1.0 has breaking schema
changes; emitting 1.1.0 would not validate against the GSA rule set.
When FedRAMP publishes 1.1.0 guidance, this primitive should emit
both behind a `--oscal-version` flag.

Determinism: this is a deterministic primitive (no LLM). UUIDs are
derived from a fixed namespace + deterministic input via uuid5, so
re-runs produce byte-identical output (modulo the `last-modified`
timestamp which the maintainer must override for true determinism;
see `last_modified` parameter).

Honest scope at v0.1.105: minimal-conformant POA&M with metadata,
system-id, observations, findings, poam-items. No `import-ssp`
reference (system-id-only mode). No risks block. No
local-definitions.components (LLM-narrative implementation
statements are scoped for the component-definition export at v0.1.107).

Spec references:
  - https://pages.nist.gov/OSCAL/concepts/layer/assessment/poam/
  - https://github.com/GSA/fedramp-automation/tree/master/src/validations
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from efterlev.models.indicator import Indicator
from efterlev.primitives.base import primitive
from efterlev.primitives.generate.generate_poam_markdown import PoamClassificationInput

# Fixed UUID namespace for efterlev-emitted OSCAL artifacts. uuid5(NAMESPACE, name)
# produces deterministic UUIDs from input strings, so re-runs of the same
# scan produce the same OSCAL UUIDs — critical for diffing across runs.
# Namespace itself is uuid5(uuid.NAMESPACE_DNS, "efterlev.com/oscal").
_EFTERLEV_OSCAL_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "efterlev.com/oscal")

# OSCAL 1.0.4 is the FedRAMP-current schema version. Pinning here so
# upstream OSCAL bumps don't silently break our emit.
_OSCAL_VERSION = "1.0.4"

# OSCAL namespace-qualifies custom prop names. Without `ns`, OSCAL constrains
# `prop.name` to a small well-known set (marking, accepted, false-positive,
# priority, risk-adjusted). Caught by the v0.1.110 NIST oscal-cli gate.
_EFTERLEV_PROP_NS = "https://efterlev.com/ns/oscal"


def _det_uuid(*parts: str) -> str:
    """Deterministic UUID derived from input parts. Same inputs → same UUID."""
    return str(uuid.uuid5(_EFTERLEV_OSCAL_NAMESPACE, "|".join(parts)))


class GeneratePoamOscalInput(BaseModel):
    """Input to `generate_poam_oscal`.

    Mirrors `GeneratePoamMarkdownInput` for the data shape. The OSCAL-
    specific fields (`system_name`, `system_id`, `last_modified`) are
    OSCAL POA&M required-or-recommended-by-spec.
    """

    model_config = ConfigDict(frozen=True)

    classifications: list[PoamClassificationInput]
    indicators: dict[str, Indicator]
    baseline_id: str
    frmr_version: str
    # System identification. OSCAL POA&M requires either an `import-ssp`
    # ref or a `system-id`; we use system-id-only at v0.1.105 (don't
    # require an SSP to exist yet). `system_name` becomes the POA&M
    # title. Defaults are placeholders the maintainer SHOULD override
    # before submitting to a 3PAO.
    system_name: str = "Unnamed System (efterlev placeholder)"
    system_id: str = "efterlev-system-default"
    # Last-modified timestamp for OSCAL metadata. Defaults to "now"
    # but should be pinned by the caller for deterministic output
    # (e.g., to the scan timestamp so re-emit produces same JSON).
    last_modified: datetime = Field(default_factory=lambda: datetime.now(UTC))


class GeneratePoamOscalOutput(BaseModel):
    """Output: OSCAL POA&M JSON-shape dict + summary counts."""

    model_config = ConfigDict(frozen=True)

    # Full OSCAL POA&M document as a Python dict. Caller serializes to
    # JSON (json.dumps) at the I/O boundary; keeping it as dict here
    # makes downstream validation / structural assertions easy.
    oscal_document: dict[str, Any]
    # Top-level POA&M item count (one per partial/not_implemented KSI).
    item_count: int
    # Same skip-list semantics as the markdown primitive.
    skipped_unknown_ksi: list[str] = Field(default_factory=list)


@primitive(capability="generate", side_effects=False, version="0.4.0", deterministic=True)
def generate_poam_oscal(input: GeneratePoamOscalInput) -> GeneratePoamOscalOutput:
    """Emit an OSCAL 1.0.4 POA&M JSON document from Gap-Agent classifications.

    Deterministic: given the same `classifications` / `indicators` /
    `last_modified`, output is byte-identical (UUIDs derived via
    `uuid5` from deterministic inputs). The dynamic field is
    `last_modified`; pin it explicitly for full reproducibility.
    """
    # Skip implemented / not_applicable / evidence_layer_inapplicable —
    # these don't need POA&M items by definition. Same filter as the
    # markdown primitive.
    open_classifications = [
        c for c in input.classifications if c.status in ("partial", "not_implemented")
    ]

    skipped_unknown: list[str] = []
    observations: list[dict[str, Any]] = []
    risks: list[dict[str, Any]] = []
    poam_items: list[dict[str, Any]] = []

    last_modified_iso = input.last_modified.replace(microsecond=0).isoformat()

    for classification in open_classifications:
        ksi_id = classification.ksi_id
        indicator = input.indicators.get(ksi_id)
        if indicator is None:
            skipped_unknown.append(ksi_id)
            continue

        # Severity heuristic: not_implemented → high, partial → moderate.
        # OSCAL emit uses FedRAMP's lowercase {high, moderate, low}
        # vocabulary (validated by FRMP-OSCAL-001). The markdown POA&M
        # uses HIGH/MEDIUM for human-readable convention; the two
        # vocabularies are intentionally distinct (machine vs human
        # consumer). Both flagged in OSCAL props as "reviewer must
        # confirm against internal risk framework."
        severity = "high" if classification.status == "not_implemented" else "moderate"

        # One observation per cited evidence record. OSCAL semantics:
        # observations are the underlying evidence; findings reference
        # observations; poam-items reference findings. We deduplicate
        # observation UUIDs by evidence_id so multi-finding-on-same-
        # evidence cases share the observation.
        observation_uuids: list[str] = []
        for evidence_id in classification.evidence_ids:
            obs_uuid = _det_uuid("observation", evidence_id)
            observation_uuids.append(obs_uuid)
            # Only append if we haven't already (dedup by uuid).
            if not any(o["uuid"] == obs_uuid for o in observations):
                observations.append(
                    {
                        "uuid": obs_uuid,
                        "title": f"Detector evidence {evidence_id[:12]}",
                        "description": (
                            f"Deterministic detector evidence record cited by "
                            f"the Gap Agent's classification for {ksi_id}. "
                            f"Full record visible via `efterlev provenance show "
                            f"{evidence_id}`."
                        ),
                        "methods": ["EXAMINE"],
                        "types": ["finding"],
                        "collected": last_modified_iso,
                    }
                )

        # One risk per (ksi, control) pair. OSCAL POA&M models per-control
        # deficiencies as risks (NOT findings — findings live in
        # assessment-results, a sibling layer). Emitting one risk per
        # 800-53 control the KSI cites matches how 3PAOs read POA&Ms.
        # Risk status is a free-form pattern-constrained string; "open"
        # is the canonical FedRAMP value for unremediated items.
        risk_uuids: list[str] = []
        for control_id in indicator.controls:
            risk_uuid = _det_uuid("risk", ksi_id, control_id)
            risk_uuids.append(risk_uuid)
            risk_entry: dict[str, Any] = {
                "uuid": risk_uuid,
                "title": f"{ksi_id} → {control_id.upper()} not satisfied",
                "description": classification.rationale,
                "statement": (
                    f"{ksi_id} is classified {classification.status} against "
                    f"control {control_id.upper()} based on detector evidence "
                    f"cited above. Reviewer must confirm the residual risk."
                ),
                "status": "open",
                "props": [
                    {
                        "name": "weakness-source-identifier",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": ksi_id,
                    },
                    {"name": "control-id", "ns": _EFTERLEV_PROP_NS, "value": control_id},
                ],
            }
            # OSCAL schema requires `related-observations` to be non-empty
            # when present. Procedural KSIs with no evidence_ids would
            # otherwise emit `[]` and fail validation.
            if observation_uuids:
                risk_entry["related-observations"] = [
                    {"observation-uuid": obs_uuid} for obs_uuid in observation_uuids
                ]
            risks.append(risk_entry)

        poam_items.append(
            {
                "uuid": _det_uuid("poam-item", ksi_id),
                "title": f"Remediate {ksi_id} ({classification.status})",
                "description": indicator.statement,
                "props": [
                    {
                        "name": "weakness-source-identifier",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": ksi_id,
                    },
                    {
                        "name": "severity",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": severity,
                        "remarks": (
                            "Severity is a starting heuristic (not_implemented "
                            "→ high, partial → moderate). Reviewer must confirm "
                            "against the system's internal risk framework."
                        ),
                    },
                    {
                        "name": "frmr-baseline",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": input.baseline_id,
                    },
                    {
                        "name": "frmr-version",
                        "ns": _EFTERLEV_PROP_NS,
                        "value": input.frmr_version,
                    },
                ],
                "related-risks": [{"risk-uuid": risk_uuid} for risk_uuid in risk_uuids],
            }
        )

    document = {
        "plan-of-action-and-milestones": {
            "uuid": _det_uuid("poam-root", input.system_id, input.baseline_id),
            "metadata": {
                "title": f"Plan of Action and Milestones for {input.system_name}",
                "last-modified": last_modified_iso,
                "version": "1.0.0",
                "oscal-version": _OSCAL_VERSION,
                "remarks": (
                    f"Generated by efterlev from FRMR {input.frmr_version} "
                    f"baseline {input.baseline_id}. POA&M items derive from "
                    f"Gap Agent classifications with status partial or "
                    f"not_implemented; implemented / not_applicable / "
                    f"evidence_layer_inapplicable verdicts produce no items."
                ),
            },
            "system-id": {
                "id": input.system_id,
                "identifier-type": "https://ietf.org/rfc/rfc4122",
            },
            "observations": observations,
            "risks": risks,
            "poam-items": poam_items,
        }
    }

    return GeneratePoamOscalOutput(
        oscal_document=document,
        item_count=len(poam_items),
        skipped_unknown_ksi=skipped_unknown,
    )
