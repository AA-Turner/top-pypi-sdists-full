"""High-level deterministic evaluation over resolved sub-checks. Stdlib-only
(the RFC 9535 branch lazily imports python-jsonpath, a declared dependency)."""
from ._core import apply_transforms, _compare


def _apply_rfc_json_path(value, rfc_json_path: str) -> list:
    import json as _json

    import jsonpath as _jsonpath

    def _parse(v):
        if not isinstance(v, str):
            return v
        try:
            return _json.loads(v)
        except (ValueError, TypeError):
            pass
        try:
            import ast as _ast
            parsed = _ast.literal_eval(v)
            return parsed if isinstance(parsed, (dict, list)) else v
        except (ValueError, SyntaxError, MemoryError, RecursionError):
            return v

    value = _parse(value)
    if isinstance(value, dict) and "status" in value and "headers" in value \
            and ("response_body" in value or "body" in value):
        value = _parse(value.get("response_body", value.get("body")))
    env = getattr(_apply_rfc_json_path, "_strict_env", None)
    if env is None:
        env = _apply_rfc_json_path._strict_env = _jsonpath.JSONPathEnvironment(strict=True)
    return env.findall(rfc_json_path, value)


_RFC_OPERATOR_ALIASES = {
    "greater_than": "gt", "greater_than_or_equal": "gte",
    "less_than": "lt", "less_than_or_equal": "lte",
    "equal": "equals", "not_equal": "not_equals",
}


def _rfc_compare(actual: str, expected: str, operator: str) -> bool:
    operator = _RFC_OPERATOR_ALIASES.get(operator, operator)
    if operator == "starts_with":
        return actual.startswith(expected)
    if operator == "ends_with":
        return actual.endswith(expected)
    return _compare(actual, expected, operator)


def _stringify_match(match) -> str:
    import json as _json

    if isinstance(match, str):
        return match
    if match is None:
        return "null"
    if match is True:
        return "true"
    if match is False:
        return "false"
    if isinstance(match, (dict, list)):
        return _json.dumps(match)
    return str(match)


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
        rfc_json_path = sc.get("rfc_json_path") or ""
        if rfc_json_path:
            matches = _apply_rfc_json_path(sc.get("extracted_value", "") or "", rfc_json_path)
            expected_raw = str(sc.get("expected_value", "") or "")
            passed = bool(matches) and all(
                _rfc_compare(_stringify_match(m), expected_raw, operator) for m in matches)
        else:
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
