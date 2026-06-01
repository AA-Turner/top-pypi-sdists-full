"""KSI-CNA-RVP: DoS protection detector.

Reads Terraform for the IaC-declared DoS-protection primitives:
WAFv2 web ACLs (with rate-based-rule counting), classic WAF web ACLs,
WAF attachments to ALB/CloudFront/API Gateway, and AWS Shield Advanced
subscriptions on specific resources.

Per DECISIONS 2026-05-07 "Tier 1 #4 design: detector gap analysis":
this is detector #3 of 6. KSI-CNA-RVP classified `partial` — the
detector covers the configured-state half; the procedural review
cadence ("persistently review the effectiveness") is manifest
territory.

No negative evidence emitted. The absence of WAF/Shield isn't a gap
per se (many workspaces serve no public traffic, or use third-party
edge protection). The Gap Agent reasons about exposure-justified
gaps; the detector emits facts.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.cna_dos_protection",
    ksis=["KSI-CNA-RVP"],
    controls=["SC-5", "SI-8"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit DoS-protection Evidence for every WAF/Shield resource.

    Evidences (KSI):     KSI-CNA-RVP — IaC-declared DoS protections
                         (WAFv2 ACLs, classic WAF, WAF attachments,
                         Shield Advanced subscriptions).
    Evidences (800-53):  SC-5 (Denial of Service Protection),
                         SI-8 (Spam Protection — WAF managed rule
                         groups contribute).
    Does NOT prove:      the procedural review cadence (manifest
                         territory); rule-content correctness
                         (thresholds, scope-down statements);
                         Shield Standard always-on free tier.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.kind != "resource":
            continue
        if r.type == "aws_wafv2_web_acl":
            out.append(_emit_waf_acl(r, now))
        elif r.type == "aws_wafv2_web_acl_association":
            out.append(_emit_waf_attached(r, now))
        elif r.type == "aws_waf_web_acl":
            out.append(_emit_waf_classic(r, now))
        elif r.type == "aws_shield_protection":
            out.append(_emit_shield(r, now))

    return out


def _emit_waf_acl(r: TerraformResource, now: datetime) -> Evidence:
    rate_based = _count_rate_based_rules(r.body)
    return Evidence.create(
        detector_id="aws.cna_dos_protection",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-5", "SI-8"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "protection_state": "configured",
            "pattern": "waf_acl",
            "detail": f"rate_based_rules={rate_based}",
        },
        timestamp=now,
    )


def _emit_waf_attached(r: TerraformResource, now: datetime) -> Evidence:
    body = r.body
    target = _coerce_str(body.get("resource_arn")) or "<unresolved>"
    return Evidence.create(
        detector_id="aws.cna_dos_protection",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-5", "SI-8"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "protection_state": "configured",
            "pattern": "waf_attached",
            "detail": f"target_arn={target}",
        },
        timestamp=now,
    )


def _emit_waf_classic(r: TerraformResource, now: datetime) -> Evidence:
    return Evidence.create(
        detector_id="aws.cna_dos_protection",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-5", "SI-8"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "protection_state": "configured",
            "pattern": "waf_classic_acl",
        },
        timestamp=now,
    )


def _emit_shield(r: TerraformResource, now: datetime) -> Evidence:
    body = r.body
    target = (
        _coerce_str(body.get("resource_arn")) or _coerce_str(body.get("name")) or "<unresolved>"
    )
    return Evidence.create(
        detector_id="aws.cna_dos_protection",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-5", "SI-8"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "protection_state": "configured",
            "pattern": "shield_protection",
            "detail": f"target={target}",
        },
        timestamp=now,
    )


def _count_rate_based_rules(body: dict[str, Any]) -> int:
    """Count `rate_based_statement` blocks across all `rule` blocks
    in an aws_wafv2_web_acl. Rate-based rules are the canonical DoS-
    mitigation primitive in WAFv2 (per-IP request-rate limit)."""
    rules = body.get("rule")
    if rules is None:
        return 0
    if isinstance(rules, dict):
        rules = [rules]
    if not isinstance(rules, list):
        return 0

    count = 0
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if _statement_has_rate_based(rule.get("statement")):
            count += 1
    return count


def _statement_has_rate_based(stmt: Any) -> bool:
    """Recursively check if a `statement {}` block contains a
    `rate_based_statement` — directly or nested inside `and_statement`,
    `or_statement`, `not_statement`."""
    if isinstance(stmt, list):
        return any(_statement_has_rate_based(s) for s in stmt)
    if not isinstance(stmt, dict):
        return False
    if "rate_based_statement" in stmt:
        return True
    # Recurse into composite statement types.
    for key in ("and_statement", "or_statement", "not_statement"):
        nested = stmt.get(key)
        if nested is not None and _statement_has_rate_based(_nested_statements(nested)):
            return True
    return False


def _nested_statements(block: Any) -> Any:
    """`and_statement`/`or_statement` blocks have a `statement` field
    holding their sub-statements; `not_statement` has a single
    `statement`. Normalize to a flat structure."""
    if isinstance(block, list) and len(block) == 1:
        block = block[0]
    if isinstance(block, dict):
        return block.get("statement", [])
    return []


def _coerce_str(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    return None
