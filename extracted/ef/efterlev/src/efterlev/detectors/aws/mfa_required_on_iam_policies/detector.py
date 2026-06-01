"""AWS IAM policy MFA-required detector.

Evidences KSI-IAM-MFA ("Enforcing Phishing-Resistant MFA") and 800-53
IA-2 ("Identification and Authentication") at the infrastructure layer:
we confirm that IAM policy documents include a
`aws:MultiFactorAuthPresent` condition on `Allow` statements that would
otherwise grant sensitive access unconditionally.

Per CLAUDE.md's MVP scope note: this detector proves *MFA-presence*, not
*phishing-resistance*. KSI-IAM-MFA requires FIDO2/WebAuthn-tier MFA,
which lives in IdP configuration (Okta/Entra/Cognito) — procedural
evidence outside Terraform's view. The README names this gap explicitly.

Resource types inspected:
  - `aws_iam_policy`
  - `aws_iam_role_policy`
  - `aws_iam_user_policy`
  - `aws_iam_group_policy`

The `policy` attribute can be:

  1. A literal JSON string — the simplest case. Parsed directly.
  2. A `jsonencode({...})` expression — RESOLVED: python-hcl2 renders the
     inner object as a Python literal, which we static-eval and walk like a
     JSON policy. (A non-literal jsonencode argument is still unparseable.)
  3. A `data.aws_iam_policy_document.NAME.json` reference — RESOLVED in
     v0.1.10 by walking the matching `data "aws_iam_policy_document"`
     block's `statement {}` blocks and translating the HCL `condition {
     test = "Bool" variable = "aws:MultiFactorAuthPresent" values =
     ["true"] }` form to the same MFA-presence check used on JSON
     statements. `aws_iam_policy_document` is the canonical Terraform
     pattern; pre-v0.1.10 we false-flagged every reference as
     unparseable, classifying KSI-IAM-MFA as not_implemented even when
     policies DID enforce MFA.

Evidence emitted per policy resource:
  - `mfa_required = "present"` — at least one `Allow` statement requires
    MFA, OR a `Deny` statement fires when MFA is absent (the AWS-recommended
    deny-without-MFA idiom), in JSON / jsonencode / data-source form.
  - `mfa_required = "absent"`  — the policy has Allow/Deny statements but
    none enforce MFA.
  - `mfa_required = "unparseable"` — the `policy` attribute is a non-literal
    expression we cannot statically resolve (e.g. a non-literal jsonencode
    argument or composed `source_policy_documents`), AND no resolvable
    data-source reference. The Gap Agent treats this as partial rather than
    false-positive implemented.
"""

from __future__ import annotations

import ast
import json
import re
from datetime import UTC, datetime
from typing import Any

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource

_IAM_POLICY_TYPES = {
    "aws_iam_policy",
    "aws_iam_role_policy",
    "aws_iam_user_policy",
    "aws_iam_group_policy",
}

_MFA_CONDITION_KEY = "aws:MultiFactorAuthPresent"

# Match `${data.aws_iam_policy_document.NAME.json}` (and `.minified_json`)
# in the policy attribute. python-hcl2 returns these references as
# strings starting with `${` after parsing.
_DATA_DOC_REF_RE = re.compile(
    r"\$\{\s*data\.aws_iam_policy_document\.([A-Za-z0-9_-]+)\.(?:minified_)?json\s*\}"
)

# Match `${jsonencode(<arg>)}` — python-hcl2 renders `jsonencode({...})` this
# way, with the inner object already parsed into a Python-literal string.
_JSONENCODE_RE = re.compile(r"^\$\{\s*jsonencode\((.*)\)\s*\}$", re.DOTALL)


@detector(
    id="aws.mfa_required_on_iam_policies",
    ksis=["KSI-IAM-MFA"],
    controls=["IA-2"],
    source="terraform",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """Emit MFA-state Evidence for every inspectable IAM policy resource.

    Evidences (KSI):     KSI-IAM-MFA (Enforcing Phishing-Resistant MFA) —
                         partial. Proves MFA presence, not phishing
                         resistance.
    Evidences (800-53):  IA-2 (Identification and Authentication).
    Does NOT prove:      (1) phishing resistance — that's an IdP-layer
                         concern (FIDO2/WebAuthn, hardware keys); (2)
                         policies produced via `jsonencode(...)` or
                         composed via `source_policy_documents` (those
                         remain unparseable in v0.1.10); (3) whether the
                         policy is actually attached to users/roles.
    """
    out: list[Evidence] = []
    now = datetime.now(UTC)

    # v0.1.10: index data-source `aws_iam_policy_document` blocks by
    # name so we can resolve `${data.aws_iam_policy_document.X.json}`
    # references on the resources we iterate over.
    policy_docs_by_name: dict[str, TerraformResource] = {
        r.name: r for r in resources if r.kind == "data" and r.type == "aws_iam_policy_document"
    }

    for r in resources:
        if r.kind != "resource" or r.type not in _IAM_POLICY_TYPES:
            continue
        out.append(_emit_policy_evidence(r, now, policy_docs_by_name))

    return out


def _emit_policy_evidence(
    r: TerraformResource,
    now: datetime,
    policy_docs_by_name: dict[str, TerraformResource],
) -> Evidence:
    policy_attr = r.body.get("policy")
    if isinstance(policy_attr, list) and len(policy_attr) == 1:
        policy_attr = policy_attr[0]

    # Literal-JSON string, then `jsonencode({...})` (python-hcl2 renders the
    # latter as `${jsonencode(<python-literal>)}` — the inner object is already
    # parsed, so we can static-eval it).
    policy_doc = _try_parse_policy(policy_attr)
    if policy_doc is None:
        policy_doc = _try_parse_jsonencode(policy_attr)
    if policy_doc is not None:
        return _classify_from_json_doc(r, now, policy_doc)

    # v0.1.10: when the policy is a data-source reference, resolve to
    # the corresponding `data "aws_iam_policy_document" "NAME"` block
    # and walk its HCL `statement {}` blocks. The HCL form is
    # structurally different from JSON IAM policies (camelCase `Effect`
    # vs lowercase `effect`, `condition` blocks vs nested `Condition`
    # dict) so it has its own walker.
    ref_match = _DATA_DOC_REF_RE.search(policy_attr) if isinstance(policy_attr, str) else None
    if ref_match is not None:
        doc_name = ref_match.group(1)
        data_source = policy_docs_by_name.get(doc_name)
        if data_source is None:
            return _evidence(
                r,
                now,
                mfa_required="unparseable",
                gap=(
                    f"policy references `data.aws_iam_policy_document.{doc_name}.json` "
                    f"but no matching data source was found in scope"
                ),
            )
        return _classify_from_data_source(r, now, data_source)

    return _evidence(
        r,
        now,
        mfa_required="unparseable",
        gap=(
            "policy attribute is not a literal JSON string and not a "
            "resolvable `data.aws_iam_policy_document.*.json` reference "
            "(likely jsonencode or composed source_policy_documents); "
            "static analysis cannot determine MFA enforcement"
        ),
    )


def _classify_from_json_doc(
    r: TerraformResource, now: datetime, policy_doc: dict[str, Any]
) -> Evidence:
    """Walk a JSON-shaped IAM policy doc; emit Evidence.

    MFA is enforced two ways: an `Allow` statement gated on
    `aws:MultiFactorAuthPresent = true`, OR a `Deny` statement that fires when
    `aws:MultiFactorAuthPresent` is false (the AWS-recommended
    deny-without-MFA idiom — e.g. `Effect: Deny` + `NotAction` + a
    `BoolIfExists` condition).
    """
    statements = [s for s in _statements(policy_doc) if isinstance(s, dict)]
    allow = [s for s in statements if s.get("Effect") == "Allow"]
    deny = [s for s in statements if s.get("Effect") == "Deny"]
    has_mfa = any(_statement_requires_mfa(s) for s in allow) or any(
        _deny_enforces_mfa(s) for s in deny
    )
    if has_mfa:
        return _evidence(r, now, mfa_required="present", allow_count=len(allow))
    if not allow and not deny:
        return _evidence(
            r,
            now,
            mfa_required="unparseable",
            gap="policy has no Allow/Deny statements; nothing for MFA to gate",
        )
    return _evidence(
        r,
        now,
        mfa_required="absent",
        allow_count=len(allow),
        gap="policy grants/denies access without an aws:MultiFactorAuthPresent condition",
    )


def _classify_from_data_source(
    r: TerraformResource, now: datetime, data_source: TerraformResource
) -> Evidence:
    """Walk an `aws_iam_policy_document` HCL data source; emit Evidence.

    HCL form (each `statement {}` is a list-of-dict in python-hcl2):

        data "aws_iam_policy_document" "x" {
          statement {
            effect    = "Allow"
            actions   = [...]
            resources = [...]
            condition {
              test     = "Bool"
              variable = "aws:MultiFactorAuthPresent"
              values   = ["true"]
            }
          }
        }
    """
    statements = data_source.body.get("statement", [])
    if isinstance(statements, dict):
        statements = [statements]
    if not isinstance(statements, list):
        return _evidence(
            r,
            now,
            mfa_required="unparseable",
            gap=(f"data source `{data_source.name}` has no statement blocks in its parsed body"),
        )

    allow_statements: list[dict[str, Any]] = []
    for stmt in statements:
        if not isinstance(stmt, dict):
            continue
        # `effect` defaults to "Allow" in aws_iam_policy_document if omitted.
        effect = stmt.get("effect", "Allow")
        if isinstance(effect, list) and effect:
            effect = effect[0]
        if effect != "Allow":
            continue
        allow_statements.append(stmt)

    if not allow_statements:
        return _evidence(
            r,
            now,
            mfa_required="unparseable",
            gap=(
                f"data source `{data_source.name}` has no Allow statements; nothing for MFA to gate"
            ),
        )

    has_mfa = any(_data_statement_requires_mfa(stmt) for stmt in allow_statements)
    return _evidence(
        r,
        now,
        mfa_required="present" if has_mfa else "absent",
        allow_count=len(allow_statements),
        gap=None
        if has_mfa
        else (
            f"data source `{data_source.name}` grants Allow without an "
            "aws:MultiFactorAuthPresent condition on any statement"
        ),
        resolved_via_data_source=data_source.name,
    )


def _data_statement_requires_mfa(statement: dict[str, Any]) -> bool:
    """True iff an HCL statement's condition block is on `aws:MultiFactorAuthPresent=true`.

    HCL `condition` blocks are list-of-dict; each carries `test`,
    `variable`, and `values` (always-list). Match on `variable` (case-
    insensitive) and `values` containing a true-literal.
    """
    conditions = statement.get("condition", [])
    if isinstance(conditions, dict):
        conditions = [conditions]
    if not isinstance(conditions, list):
        return False
    for cond in conditions:
        if not isinstance(cond, dict):
            continue
        variable = cond.get("variable")
        if isinstance(variable, list) and variable:
            variable = variable[0]
        if not isinstance(variable, str) or variable.lower() != _MFA_CONDITION_KEY.lower():
            continue
        values = cond.get("values", [])
        if isinstance(values, str):
            values = [values]
        if not isinstance(values, list):
            continue
        if any(_is_true_literal(v) for v in values):
            return True
    return False


def _evidence(
    r: TerraformResource,
    now: datetime,
    *,
    mfa_required: str,
    allow_count: int | None = None,
    gap: str | None = None,
    resolved_via_data_source: str | None = None,
) -> Evidence:
    content: dict[str, Any] = {
        "resource_type": r.type,
        "resource_name": r.name,
        "mfa_required": mfa_required,
    }
    if allow_count is not None:
        content["allow_statement_count"] = allow_count
    if gap is not None:
        content["gap"] = gap
    if resolved_via_data_source is not None:
        # v0.1.10: surface the data source that supplied the rendered
        # policy so reviewers can navigate from the evidence record
        # back to the actual statement/condition source.
        content["resolved_via_data_source"] = resolved_via_data_source
    return Evidence.create(
        detector_id="aws.mfa_required_on_iam_policies",
        ksis_evidenced=["KSI-IAM-MFA"],
        controls_evidenced=["IA-2"],
        source_ref=r.source_ref,
        content=content,
        timestamp=now,
    )


def _try_parse_policy(value: Any) -> dict[str, Any] | None:
    """Parse a `policy` attribute as JSON; return None if not a literal string."""
    if not isinstance(value, str):
        return None
    # python-hcl2 represents `jsonencode(...)` and interpolation references
    # as strings starting with "${" — those aren't parseable JSON.
    if value.strip().startswith("${"):
        return None
    try:
        parsed = json.loads(value)
    except (json.JSONDecodeError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _try_parse_jsonencode(value: Any) -> dict[str, Any] | None:
    """Parse a `policy = jsonencode({...})` attribute into a policy dict.

    python-hcl2 renders `jsonencode(<obj>)` as `${jsonencode(<py-literal>)}`
    (the inner object is already parsed to Python-dict syntax), so the
    argument is a Python literal we can `ast.literal_eval`. Returns None if the
    value isn't a jsonencode call or the argument isn't a static literal.
    """
    if not isinstance(value, str):
        return None
    m = _JSONENCODE_RE.match(value.strip())
    if m is None:
        return None
    try:
        parsed = ast.literal_eval(m.group(1))
    except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _statements(policy_doc: dict[str, Any]) -> list[Any]:
    """Return the policy's Statement entries, normalized to a list."""
    raw = policy_doc.get("Statement", [])
    if isinstance(raw, dict):
        raw = [raw]
    return raw if isinstance(raw, list) else []


def _allow_statements(policy_doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every Allow statement dict in the policy, normalized to a list."""
    return [
        s for s in _statements(policy_doc) if isinstance(s, dict) and s.get("Effect") == "Allow"
    ]


def _deny_enforces_mfa(statement: dict[str, Any]) -> bool:
    """True iff a Deny statement fires when `aws:MultiFactorAuthPresent` is false.

    The deny-without-MFA idiom: `Effect: Deny` + a condition (e.g.
    `BoolIfExists`/`Bool`) where `aws:MultiFactorAuthPresent` equals false —
    i.e. deny everything unless MFA is present.
    """
    if statement.get("Effect") != "Deny":
        return False
    condition = statement.get("Condition")
    if not isinstance(condition, dict):
        return False
    for operator_block in condition.values():
        if not isinstance(operator_block, dict):
            continue
        for key, value in operator_block.items():
            if key.lower() == _MFA_CONDITION_KEY.lower() and _is_false_literal(value):
                return True
    return False


def _is_false_literal(value: Any) -> bool:
    if isinstance(value, bool):
        return value is False
    if isinstance(value, str):
        return value.strip().lower() == "false"
    if isinstance(value, list):
        return any(_is_false_literal(v) for v in value)
    return False


def _statement_requires_mfa(statement: dict[str, Any]) -> bool:
    """True iff `statement.Condition` references aws:MultiFactorAuthPresent=true."""
    condition = statement.get("Condition")
    if not isinstance(condition, dict):
        return False
    # Condition format: { "<operator>": { "<key>": <value> } }
    for operator_block in condition.values():
        if not isinstance(operator_block, dict):
            continue
        for key, value in operator_block.items():
            if key.lower() != _MFA_CONDITION_KEY.lower():
                continue
            # The value can be "true", True, or ["true"]. Accept any truthy
            # literal string that says so.
            if _is_true_literal(value):
                return True
    return False


def _is_true_literal(value: Any) -> bool:
    if isinstance(value, bool):
        return value is True
    if isinstance(value, str):
        return value.strip().lower() == "true"
    if isinstance(value, list):
        return any(_is_true_literal(v) for v in value)
    return False
