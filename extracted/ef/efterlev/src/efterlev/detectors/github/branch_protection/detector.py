"""KSI-PIY-RSD: GitHub branch_protection rule detector.

Reads Terraform source for `github_branch_protection` resources
(GitHub provider) and emits one Evidence record per resource
describing whether the rule actually enforces meaningful protections.
A `github_branch_protection` resource that exists with NONE of
required_status_checks / required_pull_request_reviews /
enforce_admins set is the canonical "branch protection rule
declared but enforces nothing" gap -- the GitHub API accepts the
resource and the boundary owner can point at it during audit, but
no actual gate is in place.

This is the FIRST detector under detectors/github/ that reads
Terraform source rather than .github/workflows/*.yml. The github
provider's `github_branch_protection` is the canonical
infrastructure-as-code path for branch-protection rules; the
alternative (REST API + UI) leaves no IaC artifact to evidence.

Joins `github.piy_sdlc_security_gates` (which evidences
SDLC security gates in workflow YAML) on the same KSI -- branch
protection complements workflow gates: workflow gates run on PRs;
branch protection enforces that PRs require those gates to pass
before merge. KSI-PIY-RSD's "Reviewing Security in the SDLC"
classification benefits from both layers.

Two emission states (binary, no `unverifiable`):
- `protections_present` -- at least one of required_status_checks,
  required_pull_request_reviews, or enforce_admins is set. The
  detail field lists the protected branch pattern, the required
  review count, and the required status check count.
- `protections_absent` -- none of the above. Gap message names the
  "rule declared but enforces nothing" shape explicitly.

Coverage classified `partial`: presence of these blocks doesn't
prove the values are appropriate (required_approving_review_count=0
is a meaningless review block; an empty contexts list is a
meaningless status check block; required_status_checks{strict=false}
allows merging with stale checks). The Gap Agent reasons about the
specific values from the detail field.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="github.branch_protection",
    ksis=["KSI-PIY-RSD"],
    controls=["SA-15", "CM-2"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit branch-protection Evidence per github_branch_protection.

    Evidences (KSI):     KSI-PIY-RSD (Reviewing Security in the
                         SDLC) -- IaC-layer per-branch_protection-
                         resource posture. Joins
                         github.piy_sdlc_security_gates on this
                         KSI; SDLC security gates + branch
                         protection are complementary halves of
                         "PRs require reviewed, gated changes".
    Evidences (800-53):  SA-15 (Development Process / Standards
                         and Tools), CM-2 (Baseline Configuration).
                         Both new for the github family at the IaC
                         layer.
    Does NOT prove:      review counts are appropriate (count=0 is
                         meaningless); status check contexts cover
                         the relevant CI workflows; the rule's
                         pattern matches the actually-protected
                         branches; whether the GitHub Apps that
                         CAN bypass restrictions are themselves
                         appropriately scoped.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    for r in resources:
        if r.type != "github_branch_protection":
            continue
        out.append(_emit_evidence(r, now))

    return out


def _emit_evidence(r: TerraformResource, now: datetime) -> Evidence:
    pattern = _as_str(r.body.get("pattern")) or "(no pattern declared)"

    status_check_blocks = _as_block_list(r.body.get("required_status_checks"))
    review_blocks = _as_block_list(r.body.get("required_pull_request_reviews"))
    enforce_admins = _as_bool(r.body.get("enforce_admins"))

    has_status_checks = bool(status_check_blocks)
    has_reviews = bool(review_blocks)
    has_enforce_admins = bool(enforce_admins)

    required_review_count = 0
    for block in review_blocks:
        count = _as_int(block.get("required_approving_review_count"))
        if count is not None:
            required_review_count = max(required_review_count, count)

    required_status_check_count = 0
    for block in status_check_blocks:
        contexts = _as_str_list(block.get("contexts"))
        required_status_check_count += len(contexts)

    base_content: dict[str, Any] = {
        "resource_type": r.type,
        "resource_name": r.name,
        "protected_branch_pattern": pattern,
        "pattern": "github_branch_protection",
        "has_required_status_checks": has_status_checks,
        "has_required_pull_request_reviews": has_reviews,
        "enforce_admins": has_enforce_admins,
        "required_review_count": required_review_count,
        "required_status_check_count": required_status_check_count,
    }

    if has_status_checks or has_reviews or has_enforce_admins:
        base_content["rule_state"] = "protections_present"
        base_content["detail"] = (
            f"protected_branch={pattern}; "
            f"required_review_count={required_review_count}; "
            f"required_status_check_count={required_status_check_count}; "
            f"enforce_admins={has_enforce_admins}"
        )
    else:
        base_content["rule_state"] = "protections_absent"
        base_content["gap"] = (
            f"github_branch_protection '{r.name}' (pattern: {pattern}) "
            f"declares no enforcement: no required_status_checks block, "
            f"no required_pull_request_reviews block, and enforce_admins "
            f"is not true. The rule exists in IaC and the boundary owner "
            f"can point at it during audit, but no actual merge-time gate "
            f"is in place. Add a required_pull_request_reviews block with "
            f"required_approving_review_count >= 1 (and ideally a "
            f"required_status_checks block listing the CI workflows that "
            f"must pass before merge)."
        )

    return Evidence.create(
        detector_id="github.branch_protection",
        ksis_evidenced=["KSI-PIY-RSD"],
        controls_evidenced=["SA-15", "CM-2"],
        source_ref=r.source_ref,
        content=base_content,
        timestamp=now,
    )


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
    """Same single-element-list unwrapping for ints."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    if isinstance(value, bool):
        return None  # reject bool-as-int (1 != True semantically here)
    if isinstance(value, int):
        return value
    return None


def _as_bool(value: Any) -> bool:
    """python-hcl2 returns booleans as bool; treat any other shape as
    False (the Terraform default for enforce_admins is false)."""
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    return bool(value) if isinstance(value, bool) else False


def _as_str_list(value: Any) -> list[str]:
    """python-hcl2 returns HCL list literals as Python lists. Filter to
    strings only."""
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], list):
        value = value[0]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []
