"""High-level deterministic evaluation over resolved sub-checks. Stdlib-only."""
from ._core import apply_transforms, _compare


def evaluate_sub_checks(claim: str, composite_operator: str, sub_checks: list[dict]) -> dict:
    """Evaluate resolved sub_checks deterministically.

    Returns {"status", "composite_operator", "sub_results"} — the same shape the
    /api/v1/evaluate endpoint returned.
    """
    sub_results: list[dict] = []
    for sc in sub_checks:
        transforms = sc.get("transforms") or []
        json_path = sc.get("json_path")
        operator = sc.get("operator") or "contains"
        actual = apply_transforms(sc.get("extracted_value", "") or "", transforms, json_path)
        expected = apply_transforms(sc.get("expected_value", "") or "", transforms, json_path)
        passed = _compare(actual, expected, operator)
        sub_results.append({
            "description": sc.get("description", ""),
            "passed": passed,
            "operator": operator,
            "transforms": transforms,
            "expected": sc.get("expected_value", ""),
            "extracted_value": sc.get("extracted_value", ""),
        })

    if composite_operator == "or":
        overall = any(sr["passed"] for sr in sub_results)
    else:
        overall = all(sr["passed"] for sr in sub_results)

    return {
        "status": "passed" if overall else "failed",
        "composite_operator": composite_operator,
        "sub_results": sub_results,
    }
