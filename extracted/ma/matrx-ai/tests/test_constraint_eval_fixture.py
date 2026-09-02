"""Cross-CI contract test: the Python constraint evaluator must reproduce the
shared fixture exactly. The fixture is the wire contract with matrx-frontend
(features/agents/components/settings-management/validation/constraints.ts is
the spec); it lives in the common-docs repo. Override its directory with
MATRX_SHARED_FIXTURES_DIR (the directory containing constraint-eval-fixture.json).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.catalog.constraint_eval import (
    evaluate_all_constraints,
    parse_constraint,
)

DEFAULT_FIXTURES_DIR = "/Users/armanisadeghi/code/common-docs/systems/model-config"

FIXTURE_PATH = (
    Path(os.environ.get("MATRX_SHARED_FIXTURES_DIR", DEFAULT_FIXTURES_DIR))
    / "constraint-eval-fixture.json"
)

ASSERTED_FIELDS = ("ruleId", "key", "severity", "category", "message")


def _load_cases() -> list[dict[str, Any]]:
    if not FIXTURE_PATH.exists():
        pytest.skip(
            f"shared fixture not found at {FIXTURE_PATH} "
            "(set MATRX_SHARED_FIXTURES_DIR to the directory containing it)",
            allow_module_level=True,
        )
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return data["cases"]


_CASES = _load_cases()


def test_fixture_has_minimum_coverage() -> None:
    assert len(_CASES) >= 25


@pytest.mark.parametrize("case", _CASES, ids=[c["name"] for c in _CASES])
def test_constraint_eval_matches_fixture(case: dict[str, Any]) -> None:
    constraints = [parse_constraint(raw) for raw in case["constraints"]]
    issues = evaluate_all_constraints(constraints, case["config"])

    actual = [
        {
            "ruleId": issue.rule_id,
            "key": issue.key,
            "severity": issue.severity,
            "category": issue.category,
            "message": issue.message,
        }
        for issue in issues
    ]
    expected = [
        {field: raw[field] for field in ASSERTED_FIELDS}
        for raw in case["expected_issues"]
    ]

    assert actual == expected, f"case {case['name']!r} diverged from the fixture"
