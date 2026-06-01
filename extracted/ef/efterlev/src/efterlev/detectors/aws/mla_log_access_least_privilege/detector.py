"""KSI-MLA-ALA: Authorizing Log Access — least-privilege detector.

Reads Terraform for the IaC-declared least-privilege boundaries on log
data:

- `aws_cloudwatch_log_resource_policy` — explicit resource policies on
  log groups. Their existence is positive signal.
- IAM policy resources containing `logs:` actions. Classified as
  `scoped` (specific Resource ARN) or `overly_permissive` (wildcard
  Resource).

Per DECISIONS 2026-05-07 "Tier 1 #4 design": this is detector #2 of 6
closing the gap analysis. KSI-MLA-ALA classified `evidenceable-via-iac`.

NOTE: this detector duplicates the IAM-policy-document parsing pattern
from `aws.mfa_required_on_iam_policies` (literal JSON via `json.loads`,
plus `${data.aws_iam_policy_document.NAME.json}` reference resolution
through the data-source registry). When a third IAM-policy-content
detector lands from the Tier 1 #4 backlog (`svc_at_rest_encryption_coverage`
won't need it; `cna_dos_protection` won't need it; so this duplication
ends here in v1), refactor the parser into a shared `efterlev.iam`
helper module.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_IAM_POLICY_TYPES: set[str] = {
    "aws_iam_policy",
    "aws_iam_role_policy",
    "aws_iam_user_policy",
    "aws_iam_group_policy",
}

# Match `${data.aws_iam_policy_document.NAME.json}` references the
# python-hcl2 parser leaves as strings starting with `${`. Mirrors the
# regex in `aws.mfa_required_on_iam_policies` — same data-source
# resolution shape.
_DATA_DOC_REF_RE = re.compile(
    r"\$\{\s*data\.aws_iam_policy_document\.([A-Za-z0-9_-]+)\.(?:minified_)?json\s*\}"
)


@detector(
    id="aws.mla_log_access_least_privilege",
    ksis=["KSI-MLA-ALA"],
    controls=["AC-3", "AC-6"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit log-access-state Evidence per relevant resource.

    Evidences (KSI):     KSI-MLA-ALA — IaC-declared least-privilege
                         boundary on log access (positive: explicit
                         resource policy or scoped IAM policy; negative:
                         wildcard `logs:*` on `Resource: "*"`).
    Evidences (800-53):  AC-3 (Access Enforcement),
                         AC-6 (Least Privilege).
    Does NOT prove:      runtime authorization decisions, just-in-time
                         cadence, ABAC tag resolution at runtime, or
                         whether the log destination itself is
                         appropriately scoped.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    # Index data-source `aws_iam_policy_document` blocks by name so the
    # `${data.aws_iam_policy_document.X.json}` reference shape can be
    # resolved when an IAM policy uses that pattern.
    policy_docs_by_name: dict[str, TerraformResource] = {
        r.name: r for r in resources if r.kind == "data" and r.type == "aws_iam_policy_document"
    }

    for r in resources:
        if r.kind != "resource":
            continue
        if r.type == "aws_cloudwatch_log_resource_policy":
            out.append(_emit_resource_policy_evidence(r, now))
        elif r.type in _IAM_POLICY_TYPES:
            ev = _emit_iam_policy_evidence(r, now, policy_docs_by_name)
            if ev is not None:
                out.append(ev)

    return out


def _emit_resource_policy_evidence(r: TerraformResource, now: datetime) -> Evidence:
    """`aws_cloudwatch_log_resource_policy` — its presence is the
    positive signal regardless of policy contents (an admin has
    explicitly declared who can write to the log group)."""
    return Evidence.create(
        detector_id="aws.mla_log_access_least_privilege",
        ksis_evidenced=["KSI-MLA-ALA"],
        controls_evidenced=["AC-3", "AC-6"],
        source_ref=r.source_ref,
        content={
            "resource_type": r.type,
            "resource_name": r.name,
            "log_access_state": "configured",
            "pattern": "explicit_resource_policy",
            "detail": _coerce_str(r.body.get("policy_name")) or "",
        },
        timestamp=now,
    )


def _emit_iam_policy_evidence(
    r: TerraformResource,
    now: datetime,
    policy_docs_by_name: dict[str, TerraformResource],
) -> Evidence | None:
    policy_attr = r.body.get("policy")
    if isinstance(policy_attr, list) and len(policy_attr) == 1:
        policy_attr = policy_attr[0]

    # Path 1: literal JSON policy document.
    policy_doc = _try_parse_policy(policy_attr)
    if policy_doc is not None:
        return _classify_from_json_doc(r, now, policy_doc)

    # Path 2: `${data.aws_iam_policy_document.NAME.json}` reference —
    # resolve the data source and walk its HCL `statement` blocks.
    if isinstance(policy_attr, str):
        ref = _DATA_DOC_REF_RE.search(policy_attr)
        if ref is not None:
            doc = policy_docs_by_name.get(ref.group(1))
            if doc is None:
                return _emit(
                    r,
                    now,
                    "unparseable",
                    gap=(
                        f"policy references `data.aws_iam_policy_document.{ref.group(1)}.json` "
                        f"but no matching data source was found in scope"
                    ),
                )
            return _classify_from_data_source(r, now, doc)

    # Path 3: jsonencode(...) or other non-resolvable shape — we can't
    # see the contents. Skip silently rather than emit noise; the
    # `mfa_required_on_iam_policies` detector already flags this exact
    # unparseable pattern at the IAM-policy hygiene layer.
    return None


def _try_parse_policy(policy_attr: Any) -> dict[str, Any] | None:
    if not isinstance(policy_attr, str):
        return None
    s = policy_attr.strip()
    if not s.startswith("{"):
        return None
    try:
        loaded = json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def _classify_from_json_doc(
    r: TerraformResource, now: datetime, policy_doc: dict[str, Any]
) -> Evidence | None:
    """Walk a JSON-shaped IAM policy doc; emit Evidence iff any
    statement touches `logs:` actions."""
    statements = policy_doc.get("Statement") or []
    if isinstance(statements, dict):
        statements = [statements]
    if not isinstance(statements, list):
        return None

    log_statements = [s for s in statements if _statement_touches_logs(s)]
    if not log_statements:
        return None  # IAM policy with no logs:* actions — not relevant

    overly_permissive = any(_is_overly_permissive(s) for s in log_statements)
    if overly_permissive:
        return _emit(
            r,
            now,
            "overly_permissive",
            gap=(
                "policy grants `logs:*` on Resource: '*' "
                "(no scoping by log group ARN; KSI-MLA-ALA wants least-privilege)"
            ),
        )
    return _emit(r, now, "scoped", detail=f"log_statements={len(log_statements)}")


def _classify_from_data_source(
    r: TerraformResource,
    now: datetime,
    data_source: TerraformResource,
) -> Evidence | None:
    """Walk a `data "aws_iam_policy_document" "NAME"` block; emit
    Evidence iff any `statement` touches `logs:` actions.

    HCL form differs from JSON: `effect` lowercase, `actions` is a
    list, `resources` is a list, `condition` is nested blocks.
    """
    stmt_blocks = data_source.body.get("statement") or []
    if isinstance(stmt_blocks, dict):
        stmt_blocks = [stmt_blocks]
    if not isinstance(stmt_blocks, list):
        return None

    log_blocks: list[dict[str, Any]] = []
    overly: bool = False
    for stmt in stmt_blocks:
        if not isinstance(stmt, dict):
            continue
        actions = _normalize_to_list(stmt.get("actions"))
        if not _actions_touch_logs(actions):
            continue
        log_blocks.append(stmt)
        resources = _normalize_to_list(stmt.get("resources"))
        if _is_overly_permissive_hcl(actions, resources):
            overly = True

    if not log_blocks:
        return None
    if overly:
        return _emit(
            r,
            now,
            "overly_permissive",
            gap=(
                "policy (via data.aws_iam_policy_document) grants `logs:*` "
                'on `resources = ["*"]` (no scoping by log group ARN)'
            ),
        )
    return _emit(r, now, "scoped", detail=f"log_statements={len(log_blocks)}")


def _statement_touches_logs(stmt: Any) -> bool:
    if not isinstance(stmt, dict):
        return False
    actions = stmt.get("Action")
    return _actions_touch_logs(_normalize_to_list(actions))


def _actions_touch_logs(actions: list[Any]) -> bool:
    return any(isinstance(a, str) and a.lower().startswith("logs:") for a in actions)


def _is_overly_permissive(stmt: dict[str, Any]) -> bool:
    """JSON-shape statement: `Resource: "*"` AND any action is `logs:*`."""
    if stmt.get("Effect") != "Allow":
        return False
    actions = _normalize_to_list(stmt.get("Action"))
    has_log_wildcard = any(isinstance(a, str) and a == "logs:*" for a in actions)
    if not has_log_wildcard:
        return False
    resources = _normalize_to_list(stmt.get("Resource"))
    return any(r == "*" for r in resources)


def _is_overly_permissive_hcl(actions: list[Any], resources: list[Any]) -> bool:
    """HCL-shape statement: `actions` contains `logs:*` AND `resources`
    contains `*`."""
    has_log_wildcard = any(isinstance(a, str) and a == "logs:*" for a in actions)
    if not has_log_wildcard:
        return False
    return any(r == "*" for r in resources)


def _normalize_to_list(v: Any) -> list[Any]:
    """IAM policy `Action`/`Resource` can be a single string or a list.
    Same for `aws_iam_policy_document` HCL `actions`/`resources`."""
    if v is None:
        return []
    if isinstance(v, list):
        # python-hcl2 sometimes wraps single-element lists; flatten one
        # level if every entry is itself a list.
        if all(isinstance(item, list) for item in v):
            flat: list[Any] = []
            for item in v:
                flat.extend(item)
            return flat
        return v
    return [v]


def _emit(
    r: TerraformResource,
    now: datetime,
    log_access_state: str,
    *,
    detail: str | None = None,
    gap: str | None = None,
) -> Evidence:
    content: dict[str, Any] = {
        "resource_type": r.type,
        "resource_name": r.name,
        "log_access_state": log_access_state,
        "pattern": "iam_policy_with_logs_actions",
    }
    if detail:
        content["detail"] = detail
    if gap:
        content["gap"] = gap
    return Evidence.create(
        detector_id="aws.mla_log_access_least_privilege",
        ksis_evidenced=["KSI-MLA-ALA"],
        controls_evidenced=["AC-3", "AC-6"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _coerce_str(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    return None
