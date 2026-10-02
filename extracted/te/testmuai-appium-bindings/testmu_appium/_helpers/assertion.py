"""assertion() — local sub-check evaluation.

Evaluation is entirely local: unlike the playwright/selenium siblings' deterministic
path (POST /api/v1/evaluate), this binding never makes an HTTP call for an
assertion. ``{{var}}``/``${var}`` tokens in each sub_check's
``extracted_value``/``expected_value`` are resolved locally via ``_vars.var()``,
then the resolved sub_checks are handed to
``_evaluation._mobile_operators.evaluate_sub_checks`` — the mobile-aware comparer
that additionally understands the ``json_*`` operator family the canonical
``testmu_helper.evaluation`` copy has no rows for.

``driver`` is accepted (not used) for interface parity with the other query
verbs (``textual_query``, ``vision_query``, ``network_query``) that do need one;
a local-only assertion has nothing to read from the device.
"""
import logging

from testmu_appium._evaluation._mobile_operators import evaluate_sub_checks
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")


def _resolve(value):
    """Resolve {{var}}/${var} tokens, coerced to str for the comparer (which
    expects string operands — apply_transforms calls .strip() etc. on them)."""
    if not isinstance(value, str):
        return value
    resolved = var(value)
    return "" if resolved is None else str(resolved)


def _resolve_sub_checks(sub_checks: list[dict]) -> list[dict]:
    """Return a copy of sub_checks with extracted_value/expected_value resolved."""
    resolved = []
    for sc in sub_checks:
        entry = dict(sc)
        if "extracted_value" in entry:
            entry["extracted_value"] = _resolve(entry["extracted_value"])
        if "expected_value" in entry:
            entry["expected_value"] = _resolve(entry["expected_value"])
        resolved.append(entry)
    return resolved


def _branch_sub_checks(sub_checks: list) -> list[dict]:
    """The recorded branch sub-checks in the evaluator's shape, references resolved.

    v16 records ``expected``; the tree walker and the web binding record
    ``expected_value``. The extracted side is ``extracted_value`` for an
    assertion sub-check but ``stored_value`` on a branch condition (auteur's
    blob names the branch's variable reference that way), so both are accepted.
    ``operator`` defaults to ``contains`` and ``transforms`` to ``["strip"]``,
    the same defaults the Playwright binding applies.
    """
    resolved = []
    for sc in sub_checks or []:
        if not isinstance(sc, dict):
            continue
        resolved.append({
            "description": _resolve(sc.get("description") or ""),
            "expected_value": _resolve(sc.get("expected_value") or sc.get("expected") or ""),
            "extracted_value": _resolve(
                sc.get("extracted_value") or sc.get("stored_value") or ""
            ),
            "operator": sc.get("operator") or "contains",
            "transforms": sc.get("transforms") or ["strip"],
            "json_path": sc.get("json_path"),
        })
    return resolved


def evaluate_branch(sub_checks: list, composite_operator: str = "and") -> bool:
    """Evaluate an if / elif branch condition locally over its recorded sub-checks.

    Resolves ``{{var}}`` / ``${param}`` in each sub-check, compares with the
    same evaluator ``verify_assertion`` uses, and returns the verdict; no
    sub-check means the branch is not taken. ``composite_operator`` ``"or"``
    passes on any sub-check, anything else on all of them.
    """
    composite = composite_operator or "and"
    checks = _branch_sub_checks(sub_checks)
    _log.info("[if/else] evaluating %s of %d sub-check(s)", composite, len(checks))
    if not checks:
        _log.info("[if/else] result=False (no valid sub-checks) -> taking false branch")
        return False
    result = evaluate_sub_checks(f"Branch condition ({composite})", composite, checks)
    passed = result.get("status") == "passed"
    _log.info("[if/else] result=%s -> taking %s branch", passed, "true" if passed else "false")
    return passed


def _failure_summary(claim: str, result: dict) -> str:
    """Human-readable summary of which sub-checks failed, expected vs actual."""
    header = f"assertion failed: {claim}" if claim else "assertion failed"
    header += f" ({result.get('composite_operator', 'and')})"
    lines = [header]
    for sr in result.get("sub_results", []):
        if sr.get("passed"):
            continue
        label = sr.get("description") or sr.get("operator", "")
        lines.append(
            f"  - {label}: expected {sr.get('expected')!r} "
            f"{sr.get('operator')} actual {sr.get('extracted_value')!r}"
        )
    return "\n".join(lines)


def assertion(
    driver,
    *,
    claim: str = "",
    composite_operator: str = "and",
    sub_checks: list[dict] | None = None,
    description: str = "",
) -> dict:
    """Evaluate an assertion's sub_checks locally and raise on failure.

    Args:
        driver: Accepted for verb-interface parity; unused (evaluation is
            entirely local — nothing is read from the device).
        claim: Human-readable assertion claim, used only in logging/error text.
        composite_operator: "and" (default) or "or" across sub_checks.
        sub_checks: List of dicts with description/extracted_value/
            expected_value/operator/transforms/json_path. extracted_value and
            expected_value may carry {{var}}/${var} tokens, resolved here.
        description: Step description (logging only).

    Returns:
        The evaluator's {"status", "composite_operator", "sub_results"} dict,
        verbatim, when the assertion passes.

    Raises:
        ValueError: When sub_checks is empty or missing — an assertion with
            nothing to check would pass vacuously under "and". verify_assertion
            refuses an empty tree the same way.
        AssertionError: When the evaluated status is "failed" — the message
            lists each failing sub-check's expected vs actual value.
    """
    if not sub_checks:
        raise ValueError(
            "assertion() carries no sub_checks; an assertion with nothing to "
            "check would pass vacuously"
        )

    resolved_sub_checks = _resolve_sub_checks(sub_checks or [])
    result = evaluate_sub_checks(claim, composite_operator, resolved_sub_checks)

    _log.info(
        "[assertion] claim=%r composite_operator=%s status=%s",
        claim, composite_operator, result["status"],
    )
    if result["status"] == "failed":
        raise AssertionError(_failure_summary(claim, result))
    return result
