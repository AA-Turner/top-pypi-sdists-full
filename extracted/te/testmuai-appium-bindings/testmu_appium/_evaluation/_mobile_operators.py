"""The json_* operator family the mobile runtime dispatches, layered over the
canonical comparer.

The canonical ``testmu_helper.evaluation`` operator set covers the web assertion
vocabulary (equals / contains / gt / has_key / ...). The legacy mobile runtime's
perform_assertion additionally dispatches json_key_exists, json_keys_count,
json_array_length, json_array_contains and json_value_equals. The canonical copies
must stay byte-identical to their source, so those rows live here.

``compare`` handles the json_* rows and delegates everything else to the canonical
``_compare``; ``evaluate_sub_checks`` mirrors the canonical composite/transform
pipeline with ``compare`` swapped in.

Two rules govern the json_* rows:

1. COMPARE PARSED VALUES, NEVER THEIR PYTHON REPR. ``str()`` renders a JSON
   document in Python's spelling, not JSON's: ``True`` for ``true``, ``None`` for
   ``null``, single quotes for object and array literals. Both sides are parsed and
   compared structurally instead.

2. FAIL CLOSED ON MALFORMED JSON. A document that does not parse is not evidence
   about its contents, so every json_* row returns False for one.

Booleans and numbers are never conflated: ``[1]`` does not contain ``true``, and
``a=1`` does not match ``a: true``. Python's ``True == 1`` would say otherwise.

This module is stdlib-only, like the copy it extends.
"""
import json

from ._core import _compare, apply_transforms

#: Operators this module owns; everything else falls through to the canonical set.
JSON_OPERATORS = frozenset({
    "json_key_exists",
    "json_keys_count",
    "json_array_length",
    "json_array_contains",
    "json_value_equals",
})

#: "this text is not a JSON document" — distinct from a document that IS ``null``.
_UNPARSEABLE = object()


def _load(value: str):
    """Parse a JSON document, returning _UNPARSEABLE when the text is not JSON."""
    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError, TypeError):
        return _UNPARSEABLE


def _candidates(expected: str) -> list:
    """The values an expected-value string may legitimately stand for.

    A recorded expected value is plain text: ``true`` may mean the boolean or the
    four-character string, and ``2`` may mean the number or its rendering. Both
    readings are offered, JSON literal first, so ``["true"]`` contains ``true`` and
    ``[1, 2, 3]`` contains ``2`` — while ``[1]`` still does not contain ``true``,
    because neither the boolean True nor the string "true" equals the number 1.
    """
    text = "" if expected is None else str(expected)
    parsed = _load(text)
    if parsed is _UNPARSEABLE or parsed == text:
        return [text]
    return [parsed, text]


def _same(value, wanted) -> bool:
    """Structural equality with booleans held apart from numbers."""
    if isinstance(value, bool) != isinstance(wanted, bool):
        return False
    return value == wanted


def _matches(value, expected: str) -> bool:
    """Whether a parsed document value equals what the recorded expectation asked for."""
    return any(_same(value, candidate) for candidate in _candidates(expected))


def _count_matches(count: int, expected: str) -> bool:
    """Compare a container size against a recorded count.

    A count is a number; ``"3"``, ``" 3 "`` and ``3`` all name the same one, but
    ``"three"`` names none.
    """
    try:
        return count == int(str(expected).strip())
    except (TypeError, ValueError):
        return False


def _walk(document, path: str):
    """Follow a dotted path through nested dicts/lists. Returns the sentinel-free
    (found, value) pair so a legitimately-None value is distinguishable from a miss."""
    current = document
    for segment in path.split("."):
        if isinstance(current, dict):
            if segment not in current:
                return False, None
            current = current[segment]
        elif isinstance(current, list):
            try:
                current = current[int(segment)]
            except (ValueError, IndexError):
                return False, None
        else:
            return False, None
    return True, current


#: The canonical comparer's full vocabulary. Its trailing branch returns False for
#: anything else — a silent wrong-answer for a typo'd or unmapped operator, so the
#: mobile layer validates membership and raises instead of guessing.
_CANONICAL_OPERATORS = frozenset({
    "equals", "not_equals", "contains", "not_contains",
    "gt", "gte", "lt", "lte", "has_key", "true", "false",
})

#: Legacy mobile symbol vocabulary (appium_uiActions perform_assertion) mapped onto
#: canonical names where the semantics are exact. is_null / not_null have no
#: canonical counterpart and are deliberately unmapped (they raise) until a real
#: recorded producer defines their null-vs-empty semantics.
_OPERATOR_ALIASES = {
    "==": "equals",
    "!=": "not_equals",
    ">": "gt",
    ">=": "gte",
    "<": "lt",
    "<=": "lte",
}


def compare(actual: str, expected: str, operator: str) -> bool:
    """Deterministic comparison covering the json_* family plus the canonical set.

    Unknown operators raise: the canonical comparer's fall-through returns False,
    which reads as "assertion failed" when the truth is "operator not understood".
    """
    operator = _OPERATOR_ALIASES.get(operator, operator)
    if operator not in JSON_OPERATORS:
        if operator not in _CANONICAL_OPERATORS:
            raise ValueError(
                f"unknown assertion operator {operator!r}; known: "
                f"{sorted(_CANONICAL_OPERATORS | JSON_OPERATORS | set(_OPERATOR_ALIASES))}"
            )
        return _compare(actual, expected, operator)

    document = _load((actual or "").strip())
    if document is _UNPARSEABLE:
        # Fail closed: text that is not a JSON document says nothing about what it
        # would have contained.
        return False

    if operator == "json_key_exists":
        return isinstance(document, dict) and expected in document

    if operator == "json_keys_count":
        return isinstance(document, dict) and _count_matches(len(document), expected)

    if operator == "json_array_length":
        return isinstance(document, list) and _count_matches(len(document), expected)

    if operator == "json_array_contains":
        if not isinstance(document, list):
            return False
        return any(_matches(item, expected) for item in document)

    # json_value_equals — the expected value carries "<dotted.path>=<value>"; a bare
    # value with no "=" compares against the whole document.
    if "=" not in expected:
        return _matches(document, expected)
    path, _, wanted = expected.partition("=")
    found, value = _walk(document, path)
    if not found:
        return False
    return _matches(value, wanted)


def evaluate_sub_checks(claim: str, composite_operator: str, sub_checks: list[dict]) -> dict:
    """Canonical evaluate_sub_checks with the json_*-aware comparer.

    Returns the same {"status", "composite_operator", "sub_results"} shape.
    """
    sub_results: list[dict] = []
    for sc in sub_checks:
        transforms = sc.get("transforms") or []
        json_path = sc.get("json_path")
        operator = sc.get("operator") or "contains"
        actual = apply_transforms(sc.get("extracted_value", "") or "", transforms, json_path)
        expected = apply_transforms(sc.get("expected_value", "") or "", transforms, json_path)
        passed = compare(actual, expected, operator)
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
