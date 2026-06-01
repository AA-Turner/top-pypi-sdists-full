"""`validate_oscal_fedramp_rules` primitive — FedRAMP-specific OSCAL POA&M rules.

Layered on top of the v0.1.106 JSON-schema gate (`validate_oscal_poam`).
The schema gate catches structural conformance (required fields, types,
UUID format). This primitive catches FedRAMP-specific shape constraints
the upstream OSCAL schema doesn't enforce — value enumerations, cross-
references, prop conventions.

Rules are ported from a subset of the GSA fedramp-automation rule set
(https://github.com/GSA/fedramp-automation/tree/master/src/validations/constraints).
GSA's rules are XML-Schematron + metaschema-targeting OSCAL XML. This
module re-implements the highest-value subset directly against the JSON
shape — same intent, no Java/Saxon CI dependency.

Why a separate primitive (not extending `validate_oscal_poam`):
- Different rule source (GSA vs NIST)
- Different update cadence (FedRAMP rules evolve; NIST schema is
  versioned slowly)
- Composable: callers can choose schema-only, FedRAMP-only, or both

Why Python-native (not vendored Schematron + Saxon):
- Saxon-HE adds a Java runtime to CI (50+ MB image bloat)
- ISO Schematron in pure Python (lxml.isoschematron) is reliable but
  pulls another transitive dep tree
- The target rule set at v0.1.107 is small (5 rules); a hand-port is
  smaller, more legible, and easier for contributors to extend

Roadmap: rule list grows as customer-facing 3PAO feedback surfaces
specific patterns. v0.1.108 may swap implementation to Saxon if the
rule count crosses ~30 (engine-driven becomes simpler than hand-port).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from efterlev.primitives.base import primitive

# FedRAMP-recognized severity values for POA&M item props. Per FedRAMP
# Rev5 POA&M Template + GSA fedramp-automation rule set. Note "moderate"
# (not "medium") — FedRAMP convention.
_FEDRAMP_SEVERITIES = frozenset({"high", "moderate", "low"})

# FedRAMP-recognized risk status values per OSCAL POA&M conventions +
# GSA rule set. The OSCAL schema permits any pattern-conforming string;
# FedRAMP narrows to this enumeration.
_FEDRAMP_RISK_STATUSES = frozenset(
    {"open", "investigating", "remediation-pending", "closed", "deviation-requested"}
)

# FedRAMP 20x baseline identifiers. The frmr-baseline prop on poam-items
# must reference one of these — otherwise the artifact is not a 20x
# POA&M (or the baseline identifier is malformed).
_FEDRAMP_20X_BASELINES = frozenset({"fedramp-20x-low", "fedramp-20x-moderate", "fedramp-20x-high"})

# OSCAL versions FedRAMP currently accepts. Update when FedRAMP publishes
# guidance for a newer OSCAL minor.
_FEDRAMP_OSCAL_VERSIONS = frozenset({"1.0.4"})


class FedrampRuleViolation(BaseModel):
    """One FedRAMP-specific rule violation."""

    model_config = ConfigDict(frozen=True)

    # Stable rule ID (FRMP-OSCAL-NNN) for documentation + suppression.
    rule_id: str
    # JSON pointer to the offending element.
    path: str
    # Human-readable explanation including the offending value.
    message: str
    # Severity of the rule itself: "error" gates emit; "warning" is
    # informational. v0.1.107 ships errors only.
    severity: str = "error"


class ValidateOscalFedrampRulesInput(BaseModel):
    """Input: an OSCAL POA&M document as a Python dict."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    oscal_document: dict[str, Any]


class ValidateOscalFedrampRulesOutput(BaseModel):
    """Output: pass/fail + the full list of rule violations."""

    model_config = ConfigDict(frozen=True)

    valid: bool
    violations: list[FedrampRuleViolation] = Field(default_factory=list)
    # Number of rules evaluated. Useful for "are we actually checking
    # anything?" sanity assertions in tests.
    rules_evaluated: int


def _get_prop(props: list[dict[str, Any]], name: str) -> str | None:
    """Return the value of the first prop matching `name`, or None."""
    for prop in props:
        if prop.get("name") == name:
            value = prop.get("value")
            return str(value) if value is not None else None
    return None


def _check_severity_enum(
    poam_items: list[dict[str, Any]],
) -> list[FedrampRuleViolation]:
    """FRMP-OSCAL-001: severity prop must be one of {high, moderate, low}."""
    violations: list[FedrampRuleViolation] = []
    for idx, item in enumerate(poam_items):
        severity = _get_prop(item.get("props", []), "severity")
        if severity is None:
            violations.append(
                FedrampRuleViolation(
                    rule_id="FRMP-OSCAL-001",
                    path=f"poam-items.{idx}.props",
                    message="POA&M item missing required `severity` prop",
                )
            )
            continue
        if severity not in _FEDRAMP_SEVERITIES:
            violations.append(
                FedrampRuleViolation(
                    rule_id="FRMP-OSCAL-001",
                    path=f"poam-items.{idx}.props.severity",
                    message=(
                        f"severity={severity!r} not in FedRAMP enumeration "
                        f"{sorted(_FEDRAMP_SEVERITIES)}"
                    ),
                )
            )
    return violations


def _check_risk_status_enum(
    risks: list[dict[str, Any]],
) -> list[FedrampRuleViolation]:
    """FRMP-OSCAL-002: risk status must be a FedRAMP-recognized value."""
    violations: list[FedrampRuleViolation] = []
    for idx, risk in enumerate(risks):
        status = risk.get("status")
        if status is None:
            continue  # Schema gate catches missing required field
        if status not in _FEDRAMP_RISK_STATUSES:
            violations.append(
                FedrampRuleViolation(
                    rule_id="FRMP-OSCAL-002",
                    path=f"risks.{idx}.status",
                    message=(
                        f"risk status={status!r} not in FedRAMP enumeration "
                        f"{sorted(_FEDRAMP_RISK_STATUSES)}"
                    ),
                )
            )
    return violations


def _check_poam_item_has_evidence_link(
    poam_items: list[dict[str, Any]],
) -> list[FedrampRuleViolation]:
    """FRMP-OSCAL-003: every POA&M item must reference at least one risk
    or observation. A POA&M item with no evidence link is unreviewable.
    """
    violations: list[FedrampRuleViolation] = []
    for idx, item in enumerate(poam_items):
        has_risk = bool(item.get("related-risks"))
        has_obs = bool(item.get("related-observations"))
        if not has_risk and not has_obs:
            violations.append(
                FedrampRuleViolation(
                    rule_id="FRMP-OSCAL-003",
                    path=f"poam-items.{idx}",
                    message=(
                        "POA&M item has neither related-risks nor "
                        "related-observations; reviewers have no path "
                        "from the item to the underlying evidence"
                    ),
                )
            )
    return violations


def _check_baseline_enum(
    poam_items: list[dict[str, Any]],
) -> list[FedrampRuleViolation]:
    """FRMP-OSCAL-004: frmr-baseline prop must reference a FedRAMP 20x baseline."""
    violations: list[FedrampRuleViolation] = []
    for idx, item in enumerate(poam_items):
        baseline = _get_prop(item.get("props", []), "frmr-baseline")
        if baseline is None:
            continue  # Optional in OSCAL; FedRAMP context warns elsewhere
        if baseline not in _FEDRAMP_20X_BASELINES:
            violations.append(
                FedrampRuleViolation(
                    rule_id="FRMP-OSCAL-004",
                    path=f"poam-items.{idx}.props.frmr-baseline",
                    message=(
                        f"frmr-baseline={baseline!r} not a recognized FedRAMP "
                        f"20x baseline {sorted(_FEDRAMP_20X_BASELINES)}"
                    ),
                )
            )
    return violations


def _check_oscal_version(metadata: dict[str, Any]) -> list[FedrampRuleViolation]:
    """FRMP-OSCAL-005: oscal-version must be a FedRAMP-current version."""
    version = metadata.get("oscal-version")
    if version is None:
        return [
            FedrampRuleViolation(
                rule_id="FRMP-OSCAL-005",
                path="metadata.oscal-version",
                message="metadata missing required `oscal-version` field",
            )
        ]
    if version not in _FEDRAMP_OSCAL_VERSIONS:
        return [
            FedrampRuleViolation(
                rule_id="FRMP-OSCAL-005",
                path="metadata.oscal-version",
                message=(
                    f"oscal-version={version!r} not in FedRAMP-accepted "
                    f"set {sorted(_FEDRAMP_OSCAL_VERSIONS)}"
                ),
            )
        ]
    return []


@primitive(capability="validate", side_effects=False, version="0.1.0", deterministic=True)
def validate_oscal_fedramp_rules(
    input: ValidateOscalFedrampRulesInput,
) -> ValidateOscalFedrampRulesOutput:
    """Apply FedRAMP-specific OSCAL POA&M rules. Returns pass/fail + violations."""
    poam = input.oscal_document.get("plan-of-action-and-milestones", {})
    poam_items = poam.get("poam-items", []) or []
    risks = poam.get("risks", []) or []
    metadata = poam.get("metadata", {}) or {}

    violations: list[FedrampRuleViolation] = []
    violations.extend(_check_severity_enum(poam_items))
    violations.extend(_check_risk_status_enum(risks))
    violations.extend(_check_poam_item_has_evidence_link(poam_items))
    violations.extend(_check_baseline_enum(poam_items))
    violations.extend(_check_oscal_version(metadata))

    return ValidateOscalFedrampRulesOutput(
        valid=not violations,
        violations=violations,
        rules_evaluated=5,
    )
