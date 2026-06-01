"""KSI-CNA-MAT: Lambda VPC isolation detector.

Reads Terraform source for `aws_lambda_function` resources and emits
one Evidence record per function describing whether the function
declares a `vpc_config` block (network-isolated execution) or runs in
the AWS-managed default VPC pool (internet-facing).

Per DECISIONS 2026-05-10 "Tier 2 #3 design: VPC isolation, route auth,
WAF attachment": this is detector beta of the Tier 2 #3 batch. The
fundamental design call: the detector emits per-resource posture and
lets the Gap Agent reason about intentionality. Internet-facing
Lambdas are sometimes legitimate (webhook handlers, public health
endpoints); the detector does not try to distinguish them via
heuristics, annotations, or exemption lists. The agent has the
broader prompt context to weigh whether `internet_facing` is a gap
or by design.

Three states per function:
- `vpc_isolated` -- vpc_config block declared with at least one subnet_id
  and security_group_id. These may be literal IDs or Terraform references
  (e.g. `[aws_subnet.app.id]`, `${module.vpc.private_subnets}`) — either way
  the function is attached to a VPC. When values are references, the evidence
  notes `references_interpolated` (counts may be dynamic). Whether the subnet
  is itself private is out of scope (runtime / adjacent-detector concern).
- `internet_facing` -- vpc_config absent. Function executes in the
  AWS-managed default VPC pool with internet egress; reduces
  network-attack-surface controls compliance frameworks ask about.
- `unverifiable` -- vpc_config block present but subnet_ids OR
  security_group_ids are absent/empty (a malformed block).

Coverage classified `partial` per the DECISIONS entry: a vpc_config
declaration doesn't prove the function actually routes through the
VPC under all conditions, that the SGs allow only intended egress,
or that the subnets are themselves private. Those are runtime /
adjacent-detector concerns.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_INTERPOLATION_MARKERS = ("${", "{{")


@detector(
    id="aws.lambda_vpc_isolation",
    ksis=["KSI-CNA-MAT"],
    controls=["SC-7", "SC-7(3)"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit VPC-isolation Evidence per aws_lambda_function.

    Evidences (KSI):     KSI-CNA-MAT (Minimizing Attack Surface) --
                         IaC-layer per-Lambda VPC-isolation posture.
    Evidences (800-53):  SC-7 (Boundary Protection),
                         SC-7(3) (Access Points).
    Does NOT prove:      runtime traffic actually routes through the
                         VPC; security groups allow only intended
                         egress; subnets are themselves private; the
                         intentional-internet-Lambda case (webhook
                         handler, public health endpoint) is not a gap.
                         Per the DECISIONS entry, the Gap Agent
                         reasons about intentionality from broader
                         prompt context.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type != "aws_lambda_function":
            continue
        out.append(_emit_lambda_evidence(r, now))

    return out


def _emit_lambda_evidence(r: TerraformResource, now: datetime) -> Evidence:
    function_name = _as_str(r.body.get("function_name")) or r.name
    vpc_block = _normalize_block(r.body.get("vpc_config"))

    if vpc_block is None:
        return Evidence.create(
            detector_id="aws.lambda_vpc_isolation",
            ksis_evidenced=["KSI-CNA-MAT"],
            controls_evidenced=["SC-7", "SC-7(3)"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "function_name": function_name,
                "isolation_state": "internet_facing",
                "pattern": "lambda_vpc_isolation",
                "gap": (
                    f"aws_lambda_function '{function_name}' has no "
                    f"vpc_config block; the function executes in the "
                    f"AWS-managed default VPC pool with internet egress. "
                    f"Compliance reviewers consistently ask about VPC "
                    f"isolation posture for serverless boundaries. If "
                    f"this Lambda is intentionally internet-facing "
                    f"(webhook handler, public health endpoint), the "
                    f"reviewer should annotate the gap as accepted."
                ),
            },
            timestamp=now,
        )

    subnet_ids = vpc_block.get("subnet_ids")
    sg_ids = vpc_block.get("security_group_ids")

    # A vpc_config block requires both subnet_ids and security_group_ids; if
    # either is absent/empty the block is malformed and isolation can't be
    # confirmed.
    if not (_refs_present(subnet_ids) and _refs_present(sg_ids)):
        return Evidence.create(
            detector_id="aws.lambda_vpc_isolation",
            ksis_evidenced=["KSI-CNA-MAT"],
            controls_evidenced=["SC-7", "SC-7(3)"],
            source_ref=r.source_ref,
            content={
                "resource_type": r.type,
                "resource_name": r.name,
                "function_name": function_name,
                "isolation_state": "unverifiable",
                "pattern": "lambda_vpc_isolation",
                "detail": (
                    "vpc_config block declared but subnet_ids or "
                    "security_group_ids are absent/empty; isolation posture "
                    "cannot be inferred"
                ),
            },
            timestamp=now,
        )

    # subnet_ids / security_group_ids are present. They may be literal lists
    # or Terraform references (e.g. `[aws_subnet.app.id]`) — either way the
    # function is attached to a VPC, so it's vpc_isolated. Whether the subnet
    # is itself private is out of scope (a runtime / adjacent-detector concern,
    # per the DECISIONS entry).
    interpolated = _list_has_interpolation(subnet_ids) or _list_has_interpolation(sg_ids)
    subnet_count = _count_list(subnet_ids)
    sg_count = _count_list(sg_ids)
    detail = (
        f"function_name={function_name}; vpc_config declared with "
        f"{subnet_count} subnet(s) and {sg_count} security group(s)"
    )
    if interpolated:
        detail += " (subnet/SG values are Terraform references; counts may be dynamic)"

    return Evidence.create(
        detector_id="aws.lambda_vpc_isolation",
        ksis_evidenced=["KSI-CNA-MAT"],
        controls_evidenced=["SC-7", "SC-7(3)"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "function_name": function_name,
            "isolation_state": "vpc_isolated",
            "pattern": "lambda_vpc_isolation",
            "subnet_count": subnet_count,
            "security_group_count": sg_count,
            "references_interpolated": interpolated,
            "detail": detail,
        },
        timestamp=now,
    )


def _normalize_block(value: Any) -> dict[str, Any] | None:
    """python-hcl2 represents nested HCL blocks as a single dict OR a
    list-of-dicts (for repeatable blocks). vpc_config is MaxItems=1
    on aws_lambda_function; unwrap a one-element list, otherwise
    expect a dict. None when absent or malformed.
    """
    if isinstance(value, dict):
        return value
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict):
        return value[0]
    return None


def _as_str(value: Any) -> str | None:
    """python-hcl2 occasionally returns strings wrapped in single-element lists."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return value if isinstance(value, str) else None


def _is_interpolated(s: Any) -> bool:
    """True if `s` contains a Terraform interpolation marker."""
    if not isinstance(s, str):
        return False
    return any(marker in s for marker in _INTERPOLATION_MARKERS)


def _list_has_interpolation(value: Any) -> bool:
    """True if `value` is itself a Terraform interpolation expression
    (e.g., `${module.vpc.private_subnets}` returned by hcl2 as a
    string), OR a list whose elements include interpolation strings.
    Returns False for resolved literal lists.
    """
    if _is_interpolated(value):
        return True
    if isinstance(value, list):
        return any(_is_interpolated(item) for item in value)
    return False


def _count_list(value: Any) -> int:
    """Count elements in a list; 0 if not a list."""
    if isinstance(value, list):
        return len(value)
    return 0


def _refs_present(value: Any) -> bool:
    """True if subnet_ids/security_group_ids declares at least one reference.

    Accepts a literal list with >=1 non-empty element, or a non-empty bare
    interpolation string (e.g. `${module.vpc.private_subnets}`).
    """
    if isinstance(value, list):
        return any(v not in (None, "") for v in value)
    if isinstance(value, str):
        return value.strip() != ""
    return False
