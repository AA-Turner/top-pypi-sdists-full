"""Root golden-vector fixture, run through the comparer this package SHIPS.

Same fixture the playwright and TS packages read (repo-root eval_golden_vectors.json),
so a divergence in the copied evaluator shows up here.

The vectors go through `_mobile_operators.evaluate_sub_checks`, which is what every
assertion in this binding actually calls — not the canonical `_evaluation` entry
point, which would pin the copy rather than the fork that ships.

The canonical entry point is also exercised, but only as the cross-check it is.
"""
import json
from pathlib import Path

import pytest

from testmu_appium._evaluation import evaluate_sub_checks as canonical_evaluate_sub_checks
from testmu_appium._evaluation._mobile_operators import evaluate_sub_checks

_FIXTURE = Path(__file__).resolve().parents[2] / "eval_golden_vectors.json"


def _cases():
    return json.loads(_FIXTURE.read_text())


def test_fixture_present():
    assert len(_cases()) >= 33


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["name"])
def test_golden_vector_through_the_shipping_comparer(case):
    result = evaluate_sub_checks(
        case.get("claim", ""), case["composite_operator"], case["sub_checks"]
    )
    assert result["status"] == case["expected_status"]
    assert result["composite_operator"] == case["composite_operator"]
    assert len(result["sub_results"]) == len(case["sub_checks"])


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["name"])
def test_the_shipping_comparer_agrees_with_the_canonical_one(case):
    """Every root vector uses web operators only, so the fork must answer identically
    — including each sub_result, not just the overall status."""
    assert evaluate_sub_checks(
        case.get("claim", ""), case["composite_operator"], case["sub_checks"]
    ) == canonical_evaluate_sub_checks(
        case.get("claim", ""), case["composite_operator"], case["sub_checks"]
    )


def test_root_vectors_do_not_cover_the_mobile_json_family():
    """Pins the gap that motivates _mobile_operators.

    The shared vectors exercise the web operator set only; the legacy mobile runtime's
    perform_assertion also dispatches json_key_exists / json_keys_count /
    json_array_length / json_array_contains / json_value_equals. Package-local cases
    cover those (test_mobile_operators.py). If this assertion starts failing, the
    shared vectors grew mobile coverage and the local cases can shrink.
    """
    operators = {
        sc["operator"] for case in _cases() for sc in case["sub_checks"]
    }
    assert not (operators & {
        "json_key_exists", "json_keys_count", "json_array_length",
        "json_array_contains", "json_value_equals",
    })
