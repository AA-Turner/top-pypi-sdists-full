"""KSI-CNA-RVP: AWS WAFv2 Web ACL rate-limiting detector.

Reads Terraform source for `aws_wafv2_web_acl` resources and emits one
Evidence record per Web ACL describing whether at least one rule
declares a rate-based statement via `statement.rate_based_statement`.
A rate-based statement caps the number of requests a single client (or
custom-key bucket) can make in a 5-minute window, providing the
primary L7 DOS defense the Web ACL has independent of upstream
infrastructure (CloudFront, Shield, ALB, etc.).

Per DECISIONS 2026-05-10 "Tier 3 #1 design: aws.waf_* detector family
v0": this is detector delta of the Tier 3 #1 batch. Per-Web-ACL
emission (NOT per-rule) per the family's first design choice. Two
states (binary, no `unverifiable` per the third design choice):
- `rate_limiting_present` -- at least one rule has a
  `rate_based_statement`. The detail field lists the limits and
  aggregate-key types so the Gap Agent can reason about whether the
  caps are tight enough.
- `rate_limiting_absent` -- zero rate-based statements across all
  rules (or zero rules). The Web ACL still relies on managed groups
  and custom byte-match rules but lacks a per-client request cap.

Coverage classified `partial`: presence of a rate-based statement
does not prove the limit is appropriate (a 1M-requests-per-5-min cap
provides observability without enforcement under realistic abuse
patterns), that the aggregate-key type is right (IP can be bypassed
by botnets; FORWARDED_IP is required when traffic flows through a
proxy), or that scope-down statements aren't gated to a narrow
endpoint set.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.waf_rate_limiting",
    ksis=["KSI-CNA-RVP"],
    controls=["SC-5", "SC-5(2)"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit rate-limiting Evidence per aws_wafv2_web_acl.

    Evidences (KSI):     KSI-CNA-RVP (Reviewing Protections) -- IaC-
                         layer per-Web-ACL rate-based-statement
                         presence. Joins aws.waf_rule_count,
                         aws.waf_managed_rule_groups,
                         aws.cna_dos_protection, and
                         aws.api_gateway_waf_attached on this KSI.
    Evidences (800-53):  SC-5 (Denial of Service Protection),
                         SC-5(2) (Capacity, Bandwidth, and Redundancy --
                         rate caps prevent single-client bandwidth
                         exhaustion).
    Does NOT prove:      the limit value is appropriate (a 1M req/5-min
                         cap is observability without enforcement under
                         realistic abuse); the aggregate-key type is
                         right (IP can be bypassed by botnets;
                         FORWARDED_IP is required when traffic flows
                         through a proxy); scope-down statements aren't
                         narrowing the cap to a tiny endpoint set.
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
    rate_limits = _collect_rate_limits(r.body.get("rule"))

    if rate_limits:
        joined = ", ".join(f"limit={limit} key={key}" for limit, key in rate_limits)
        return Evidence.create(
            detector_id="aws.waf_rate_limiting",
            ksis_evidenced=["KSI-CNA-RVP"],
            controls_evidenced=["SC-5", "SC-5(2)"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "web_acl_name": web_acl_name,
                "rule_state": "rate_limiting_present",
                "pattern": "wafv2_web_acl_rate_limiting",
                "rate_limit_count": len(rate_limits),
                "rate_limits": [
                    {"limit": limit, "aggregate_key_type": key} for limit, key in rate_limits
                ],
                "detail": (
                    f"web_acl_name={web_acl_name}; "
                    f"rate_limit_count={len(rate_limits)}; "
                    f"rate_limits={joined}"
                ),
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.waf_rate_limiting",
        ksis_evidenced=["KSI-CNA-RVP"],
        controls_evidenced=["SC-5", "SC-5(2)"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "web_acl_name": web_acl_name,
            "rule_state": "rate_limiting_absent",
            "pattern": "wafv2_web_acl_rate_limiting",
            "rate_limit_count": 0,
            "rate_limits": [],
            "gap": (
                f"aws_wafv2_web_acl '{web_acl_name}' declares zero "
                f"rate-based statements. Without a per-client request "
                f"cap, the Web ACL relies entirely on upstream "
                f"infrastructure (CloudFront, Shield, ALB) for L7 DOS "
                f"defense -- managed groups catch known-bad patterns "
                f"but not novel volumetric abuse. Consider adding a "
                f"rate_based_statement with a limit appropriate to the "
                f"workload (e.g., limit=2000, aggregate_key_type=IP)."
            ),
        },
        timestamp=now,
    )


def _collect_rate_limits(rule_value: Any) -> list[tuple[int, str]]:
    """Walk every rule block and collect (limit, aggregate_key_type)
    tuples from rate_based_statement blocks. python-hcl2 represents
    repeated HCL blocks as either a single dict or a list of dicts at
    every level (rule, statement, rate_based_statement).
    """
    rules = _as_block_list(rule_value)
    limits: list[tuple[int, str]] = []
    for rule in rules:
        statement = rule.get("statement")
        if statement is None:
            continue
        for stmt in _as_block_list(statement):
            for rate in _as_block_list(stmt.get("rate_based_statement")):
                limit = _as_int(rate.get("limit"))
                key_type = _as_str(rate.get("aggregate_key_type")) or "IP"
                if limit is not None:
                    limits.append((limit, key_type))
    return limits


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


def _as_int(value: Any) -> int | None:
    """python-hcl2 sometimes wraps integers in single-element lists too."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    if isinstance(value, bool):  # bool is an int subclass; reject explicitly
        return None
    if isinstance(value, int):
        return value
    return None
