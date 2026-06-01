"""KSI-CNA-RVP: AWS WAFv2 Web ACL geo-blocking detector.

Reads Terraform source for `aws_wafv2_web_acl` resources and emits one
Evidence record per Web ACL describing whether at least one rule
references a `statement.geo_match_statement`. Geo-match rules block
traffic from a list of country codes (ISO 3166-1 alpha-2), giving
the boundary an explicit perimeter-side access-enforcement primitive
distinct from the bulk OWASP coverage managed groups provide. For
US-federal workloads the canonical posture is to block embargoed
countries (KP, IR, CU, SY, plus geographic subsets of RU under
sanctions); other workloads with global customer bases legitimately
omit geo-blocking entirely.

Per DECISIONS 2026-05-10 "Tier 3 #4 design: aws.waf_geo_blocking
(single-detector batch)": this is detector beta of the Tier 3 #4
batch. Per-Web-ACL emission. Two states (binary, no `unverifiable`,
matching the family's clean-state pattern):
- `geo_blocking_present` -- at least one rule has a
  `geo_match_statement`. Detail field lists the deduplicated set
  of country codes covered across all geo rules so the Gap Agent
  can reason about whether the country list matches the
  workload's declared customer geography.
- `geo_blocking_absent` -- zero geo-match references across all
  rules. The gap message explicitly names "may be intentional for
  global-customer workloads" -- the Gap Agent reasons about
  whether absence is appropriate, not the detector.

Coverage classified `partial`: presence of a geo_match_statement
does not prove the country_codes list is appropriate (an empty list
provides no protection; a list missing sanctioned regions provides
only token coverage), or that the rule action enforces (a
geo_match_statement with override_action.count is observability
without enforcement -- aws.waf_action_types orthogonally covers
that dimension).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.waf_geo_blocking",
    ksis=["KSI-CNA-RVP"],
    controls=["SC-7", "AC-3"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit geo-blocking Evidence per aws_wafv2_web_acl.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL geo_match_statement
                         presence. 8th detector evidencing
                         KSI-CNA-RVP after Tier 3 #1/#3.
    Evidences (800-53):  SC-7 (Boundary Protection) -- first WAF-
                         family detector to evidence boundary
                         protection at the IaC layer; geo-blocking
                         IS the canonical perimeter-side boundary
                         control. AC-3 (Access Enforcement) --
                         generalizing the IP-layer mapping that
                         aws.waf_ip_set_blocking earned in Tier
                         3 #3, up to the geographic layer.
    Does NOT prove:      the country_codes list is appropriate
                         (empty list provides no protection;
                         list missing sanctioned regions provides
                         only token coverage); the rule action
                         enforces (geo_match with override_action.
                         count logs without blocking --
                         aws.waf_action_types covers that).
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type != "aws_wafv2_web_acl":
            continue
        out.append(_emit_web_acl_evidence(r, now))

    return out


def _emit_web_acl_evidence(r: TerraformResource, now: datetime) -> Evidence:
    web_acl_name = _as_str(r.body.get("name")) or r.name
    country_codes = _collect_country_codes(r.body.get("rule"))

    if country_codes:
        joined = ", ".join(country_codes)
        return Evidence.create(
            detector_id="aws.waf_geo_blocking",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SC-7", "AC-3"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "web_acl_name": web_acl_name,
                "rule_state": "geo_blocking_present",
                "pattern": "wafv2_web_acl_geo_blocking",
                "country_code_count": len(country_codes),
                "country_codes": country_codes,
                "detail": (
                    f"web_acl_name={web_acl_name}; "
                    f"country_code_count={len(country_codes)}; "
                    f"country_codes={joined}"
                ),
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.waf_geo_blocking",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-7", "AC-3"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "web_acl_name": web_acl_name,
            "rule_state": "geo_blocking_absent",
            "pattern": "wafv2_web_acl_geo_blocking",
            "country_code_count": 0,
            "country_codes": [],
            "gap": (
                f"aws_wafv2_web_acl '{web_acl_name}' references zero "
                f"geo_match_statement rules. For US-federal workloads, "
                f"the canonical posture blocks embargoed countries "
                f"(KP, IR, CU, SY, sanctioned subsets of RU); for "
                f"global-customer workloads, geo-blocking absence may "
                f"be intentional. The Gap Agent should reason about "
                f"whether absence is appropriate given the workload's "
                f"declared customer geography. Consider adding an "
                f"aws_wafv2_web_acl rule with statement.geo_match_statement "
                f"and the country_codes list appropriate to the boundary."
            ),
        },
        timestamp=now,
    )


def _collect_country_codes(rule_value: Any) -> list[str]:
    """Walk every rule block and return the deduplicated set of
    country codes from geo_match_statement blocks. python-hcl2
    returns the country_codes list as a Python list of strings;
    aggregate across all rules and dedupe (sorted for stable
    output the M3 fixture-author labels can match against).
    """
    rules = _as_block_list(rule_value)
    seen: set[str] = set()
    for rule in rules:
        statement = rule.get("statement")
        if statement is None:
            continue
        for stmt in _as_block_list(statement):
            for geo in _as_block_list(stmt.get("geo_match_statement")):
                for code in _as_str_list(geo.get("country_codes")):
                    seen.add(code)
    return sorted(seen)


def _as_block_list(value: Any) -> list[dict[str, Any]]:
    """Normalize python-hcl2's "single dict OR list of dicts" block
    representation into a list of dicts."""
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None


def _as_str_list(value: Any) -> list[str]:
    """python-hcl2 returns HCL list literals as Python lists. Filter to
    strings only; defensively handle the single-list-wrapped case
    (rare but observed for some attribute values)."""
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], list):
        value = value[0]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []
