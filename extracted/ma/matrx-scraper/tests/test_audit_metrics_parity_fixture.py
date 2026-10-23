"""The page-audit METRICS parity fixture must stay current with `audit_metrics.py`.

`tests/__fixtures__/audit-parity.json` is the ONE home of the expected answers of
`evaluate_social_card`, `evaluate_heading_structure`, `evaluate_url_quality` and
`evaluate_indexability`. matrx-frontend (`audit.parity.test.ts`) and matrx-extend
(`seo-evaluator-parity.test.ts`) replay vendored copies of it, and fail when their
copy differs from this one.

This test regenerates the fixture in memory and compares. A failure means
audit_metrics.py changed without regenerating — both TS copies are still asserting
the OLD answers. Regenerate (writes all three files) AND fix both TS copies:

    .venv/bin/python packages/matrx-scraper/scripts/generate_audit_metrics_parity_fixture.py
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATOR = REPO_ROOT / "packages/matrx-scraper/scripts/generate_audit_metrics_parity_fixture.py"
FIXTURE = REPO_ROOT / "packages/matrx-scraper/tests/__fixtures__/audit-parity.json"


def _load_generator():
    spec = importlib.util.spec_from_file_location("_audit_metrics_parity_gen", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixture_matches_current_audit_metrics() -> None:
    generator = _load_generator()
    assert FIXTURE.read_text(encoding="utf-8") == generator.render(), (
        "audit-parity.json is stale: audit_metrics.py changed without regenerating "
        "the fixture, so the matrx-frontend and matrx-extend evaluators are still "
        "asserting the OLD answers. Run:\n"
        "  .venv/bin/python packages/matrx-scraper/scripts/"
        "generate_audit_metrics_parity_fixture.py\n"
        "and make the matching change in both TS copies."
    )


def test_fixture_covers_canonical_resolution() -> None:
    """A shrinking fixture is silent coverage loss — pin the canonical cases."""
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    canonicals = {case["input"]["canonical_url"] for case in fixture["indexability"]}
    for required in ("/page", "//ex.com/page", "https://other.com/page", "/other"):
        assert required in canonicals, f"fixture lost the {required!r} canonical case"
    assert any(case["input"].get("requested_url") for case in fixture["indexability"])
    assert any(
        case["input"]["canonical_url"] in {hop["url"] for hop in case["input"]["redirect_chain"]}
        and case["input"]["canonical_url"] != case["input"]["final_url"]
        for case in fixture["indexability"]
    ), "fixture lost the canonical-names-a-redirect-hop case"
    for section in ("social", "headings", "indexability", "url_quality"):
        assert len(fixture[section]) >= 5, f"{section} shrank below 5 cases"
