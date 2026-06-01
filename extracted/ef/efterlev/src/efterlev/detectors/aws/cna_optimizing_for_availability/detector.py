"""KSI-CNA-OFA: Optimizing for Availability detector.

Reads Terraform source for the common availability primitives that
contribute to the KSI's "high availability and rapid recovery" outcome:
multi-AZ databases, multi-AZ autoscaling groups, read replicas, S3
cross-region replication, ECS service spreading. Emits one Evidence
record per matching resource (positive) or per missing-config resource
(negative — most often `aws_db_instance` without `multi_az = true`).

Per DECISIONS 2026-05-07 "Tier 1 #4 design: detector gap analysis +
prioritized adds": this is detector #1 of 6 closing the gap analysis.
KSI-CNA-OFA classified `evidenceable-via-iac` — full detector candidate,
no manifest needed for the configuration half.

Coverage is reported as `partial` in mapping.yaml: the IaC layer covers
configured availability primitives; runtime failover behavior, RTO/RPO
measurement, and DR exercise cadence are out of scope (procedural,
covered by separate KSIs / Evidence Manifests).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="aws.cna_optimizing_for_availability",
    ksis=["KSI-CNA-OFA"],
    controls=[],  # KSI-CNA-OFA has no mapped 800-53 controls in FRMR 0.9.43-beta
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit availability-state Evidence for every matching resource.

    Evidences (KSI):     KSI-CNA-OFA — IaC-declared availability primitives
                         (multi-AZ DBs, multi-AZ ASGs, read replicas,
                         S3 cross-region replication, ECS service spread).
    Evidences (800-53):  None — KSI-CNA-OFA has no mapped controls.
    Does NOT prove:      runtime failover behavior, RTO/RPO measurement,
                         DR exercise cadence, full multi-region SaaS
                         posture (those are adjacent KSIs / Evidence
                         Manifest territory per CLAUDE.md "Per-fix
                         regression test discipline" `partial` framing).
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type == "aws_db_instance":
            ev = _emit_db_instance_evidence(r, now)
            if ev is not None:
                out.append(ev)
        elif r.type == "aws_rds_cluster":
            ev = _emit_rds_cluster_evidence(r, now)
            if ev is not None:
                out.append(ev)
        elif r.type == "aws_autoscaling_group":
            ev = _emit_asg_evidence(r, now)
            if ev is not None:
                out.append(ev)
        elif r.type == "aws_s3_bucket_replication_configuration":
            ev = _emit_s3_replication_evidence(r, now)
            if ev is not None:
                out.append(ev)
        elif r.type == "aws_ecs_service":
            ev = _emit_ecs_spread_evidence(r, now)
            if ev is not None:
                out.append(ev)

    return out


def _emit_db_instance_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    body = r.body
    # Read replicas are an availability pattern: presence of replicate_source_db
    # makes the resource a replica of another DB.
    replicate_source = body.get("replicate_source_db")
    if isinstance(replicate_source, str) and replicate_source.strip():
        return Evidence.create(
            detector_id="aws.cna_optimizing_for_availability",
            ksis_evidenced=["KSI-CNA-OFA"],
            controls_evidenced=[],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "availability_state": "configured",
                "pattern": "read_replica",
                "detail": f"replicate_source_db={replicate_source}",
            },
            timestamp=now,
        )

    # Multi-AZ flag is the canonical availability primitive for DB
    # instances. Honor literal `true`, string "true", or string "1"
    # (Terraform sometimes resolves bools to strings via interpolation).
    multi_az = body.get("multi_az")
    if _is_truthy(multi_az):
        return Evidence.create(
            detector_id="aws.cna_optimizing_for_availability",
            ksis_evidenced=["KSI-CNA-OFA"],
            controls_evidenced=[],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "availability_state": "configured",
                "pattern": "multi_az",
            },
            timestamp=now,
        )

    return Evidence.create(
        detector_id="aws.cna_optimizing_for_availability",
        ksis_evidenced=["KSI-CNA-OFA"],
        controls_evidenced=[],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "availability_state": "absent",
            "pattern": "multi_az",
            "gap": "aws_db_instance declared without multi_az=true and not a read replica",
        },
        timestamp=now,
    )


def _emit_rds_cluster_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    body = r.body
    # Aurora-style RDS clusters are inherently multi-AZ when they have
    # ≥2 cluster instances (which Terraform users usually express via
    # a separate aws_rds_cluster_instance count). The cluster resource
    # itself can hint via availability_zones being explicitly listed,
    # OR via global cluster membership. Emit positive when either
    # signal is present; absent otherwise.
    azs = body.get("availability_zones")
    if isinstance(azs, list) and len(azs) >= 2:
        return Evidence.create(
            detector_id="aws.cna_optimizing_for_availability",
            ksis_evidenced=["KSI-CNA-OFA"],
            controls_evidenced=[],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "availability_state": "configured",
                "pattern": "multi_az",
                "detail": f"availability_zones={len(azs)}",
            },
            timestamp=now,
        )
    global_cluster = body.get("global_cluster_identifier")
    if isinstance(global_cluster, str) and global_cluster.strip():
        return Evidence.create(
            detector_id="aws.cna_optimizing_for_availability",
            ksis_evidenced=["KSI-CNA-OFA"],
            controls_evidenced=[],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "availability_state": "configured",
                "pattern": "multi_az",
                "detail": f"global_cluster={global_cluster}",
            },
            timestamp=now,
        )
    # Without explicit AZ enumeration or global-cluster membership, the
    # cluster's multi-AZ status depends on per-instance count which we
    # can't see from a single resource. Emit nothing rather than a noisy
    # negative — `aws_rds_cluster_instance` count is the cross-resource
    # signal, and inferring from it requires Gap-Agent-level reasoning.
    return None


def _emit_asg_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    body = r.body
    # ASGs spread across AZs by referencing multiple subnets via
    # `vpc_zone_identifier`. Terraform commonly passes this as a list
    # of subnet IDs (each subnet is in a single AZ).
    vpc_zone_identifier = body.get("vpc_zone_identifier")
    subnet_count = _count_list_or_set(vpc_zone_identifier)

    if subnet_count >= 2:
        return Evidence.create(
            detector_id="aws.cna_optimizing_for_availability",
            ksis_evidenced=["KSI-CNA-OFA"],
            controls_evidenced=[],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "availability_state": "configured",
                "pattern": "asg_multi_az",
                "detail": f"vpc_zone_identifier={subnet_count} subnets",
            },
            timestamp=now,
        )
    if subnet_count == 1:
        return Evidence.create(
            detector_id="aws.cna_optimizing_for_availability",
            ksis_evidenced=["KSI-CNA-OFA"],
            controls_evidenced=[],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "availability_state": "absent",
                "pattern": "asg_multi_az",
                "gap": "aws_autoscaling_group references only 1 subnet (single-AZ)",
            },
            timestamp=now,
        )
    # Zero subnets or unparseable expression: nothing to claim.
    return None


def _emit_s3_replication_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    # The mere presence of an aws_s3_bucket_replication_configuration is the
    # signal — it requires a destination bucket (often in another region).
    # Emit positive evidence; cross-region-ness is best confirmed at the
    # destination's AZ which we can't always resolve, so we don't gate on it.
    body = r.body
    rule_count = _count_rule_blocks(body)
    return Evidence.create(
        detector_id="aws.cna_optimizing_for_availability",
        ksis_evidenced=["KSI-CNA-OFA"],
        controls_evidenced=[],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "availability_state": "configured",
            "pattern": "s3_replication",
            "detail": f"rules={rule_count}" if rule_count else "rules=present",
        },
        timestamp=now,
    )


def _emit_ecs_spread_evidence(r: TerraformResource, now: datetime) -> Evidence | None:
    body = r.body
    constraints = body.get("placement_constraints")
    if isinstance(constraints, list) and constraints:
        for c in constraints:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "spread" and "availability-zone" in str(c.get("expression", "")):
                return Evidence.create(
                    detector_id="aws.cna_optimizing_for_availability",
                    ksis_evidenced=["KSI-CNA-OFA"],
                    controls_evidenced=[],
                    source_ref=r.source_ref,
                    content={
                        "resource_type": r.type,
                        "resource_name": r.name,
                        "availability_state": "configured",
                        "pattern": "ecs_service_spread",
                    },
                    timestamp=now,
                )
    # No spread constraint: don't emit a negative — many ECS services
    # legitimately use placement_strategies (random / binpack) instead,
    # and we can't classify those without more context. Future
    # enhancement: detect placement_strategies field too.
    return None


def _is_truthy(v: Any) -> bool:
    """Terraform booleans can resolve to literal True, "true", or "1"."""
    if v is True:
        return True
    if isinstance(v, str):
        return v.lower() in ("true", "1")
    return False


def _count_list_or_set(v: Any) -> int:
    """vpc_zone_identifier may be a list of subnet IDs OR an unresolved
    `module.foo.private_subnets` reference. Count list entries; 0 if not
    a resolvable list."""
    if isinstance(v, list):
        return len(v)
    return 0


def _count_rule_blocks(body: dict[str, Any]) -> int:
    rule = body.get("rule")
    if isinstance(rule, list):
        return len(rule)
    if isinstance(rule, dict):
        return 1
    return 0
