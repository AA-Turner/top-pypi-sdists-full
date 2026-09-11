"""Cross-CI contract test: the Python constraint evaluator must reproduce the
versioned package fixture exactly. The fixture is the wire contract with matrx-frontend
(features/agents/components/settings-management/validation/constraints.ts is
the spec, and its twin suite
features/agents/.../__tests__/constraint-eval-fixture.test.ts reads THIS SAME
content from common-docs).

The fixture moved from `systems/model-config/` to `systems/agents/ai-models/`
in the common-docs docs rename cascade (6bb0b8aa) and this test kept pointing
at the old path — where it silently SKIPPED, which is why nobody noticed.

🚨 A missing package fixture is never a skip. It means the Python evaluator is
UNMEASURED, so this suite throws `UNMEASURED:` with a remedy. When a sibling
common-docs checkout is present, a second test also requires the two tracked
copies to be byte-identical. CI remains hermetic because it cannot read the
private sibling repository with its repository-scoped GITHUB_TOKEN.

Path resolution follows the repo convention: common-docs is a SIBLING checkout,
overridable with `MATRX_COMMON_DOCS` (whole-bundle root, as in
scripts/check_shared_skills.py) or `MATRX_SHARED_FIXTURES_DIR` (the directory
that directly holds constraint-eval-fixture.json).
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

# tests/ -> matrx-ai/ -> packages/ -> <repo root> -> the checkout dir holding
# both repos as siblings.
_SIBLINGS = Path(__file__).resolve().parents[3].parent
COMMON_DOCS_ROOT = Path(
    os.environ.get("MATRX_COMMON_DOCS", str(_SIBLINGS / "common-docs"))
)
DEFAULT_FIXTURES_DIR = COMMON_DOCS_ROOT / "systems" / "agents" / "ai-models"
PACKAGE_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
FIXTURES_DIR = Path(os.environ.get("MATRX_SHARED_FIXTURES_DIR", str(PACKAGE_FIXTURES_DIR)))
FIXTURE_PATH = FIXTURES_DIR / "constraint-eval-fixture.json"

UNMEASURED = (
    f"UNMEASURED: the package constraint-evaluator contract fixture is missing at "
    f"{FIXTURE_PATH}. This suite is the only thing proving "
    "matrx_ai.catalog.constraint_eval still matches the TypeScript spec "
    "(matrx-frontend features/agents/components/settings-management/validation/"
    "constraints.ts), so a missing fixture is a RED contract, never a pass. "
    "Remedy: restore packages/matrx-ai/tests/fixtures/constraint-eval-fixture.json "
    "or point MATRX_SHARED_FIXTURES_DIR at the directory that holds it."
)

ASSERTED_FIELDS = ("ruleId", "key", "severity", "category", "message")


def _load_cases() -> list[dict[str, Any]]:
    # NEVER downgrade this to a pytest.skip — see the module docstring. The
    # skip is what let this test point at a dead path for the whole life of
    # the rename.
    if not FIXTURE_PATH.exists():
        raise FileNotFoundError(UNMEASURED)
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return data["cases"]


_CASES = _load_cases()


def test_fixture_has_minimum_coverage() -> None:
    assert len(_CASES) >= 25


def test_workspace_common_docs_fixture_matches_package_fixture() -> None:
    shared_fixture = DEFAULT_FIXTURES_DIR / "constraint-eval-fixture.json"
    if not shared_fixture.exists():
        pytest.skip("sibling common-docs checkout is unavailable; package fixture remains measured")
    assert shared_fixture.read_bytes() == FIXTURE_PATH.read_bytes(), (
        "package and common-docs constraint evaluator fixtures diverged; update both "
        "tracked copies in the same integration change"
    )


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
