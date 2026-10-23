"""The per-page CHECK parity fixture must stay current with `run_page_checks`.

`tests/__fixtures__/page-checks-parity.json` is the ONE home of the expected
verdicts. matrx-frontend `features/marketing/seo/audit/checks.ts` is the browser
mirror of `seo_audit.run_page_checks`; its `checks.parity.test.ts` replays this
file (and fails when its vendored copy differs from it).

This test regenerates the fixture in memory and compares. A failure means a
check, a threshold or a reasoning string changed in Python without the fixture
being regenerated — so the frontend is still asserting the OLD answers. Regenerate
AND make the matching change in checks.ts in the same unit of work:

    .venv/bin/python packages/matrx-scraper/scripts/generate_page_checks_parity_fixture.py
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATOR = REPO_ROOT / "packages/matrx-scraper/scripts/generate_page_checks_parity_fixture.py"
FIXTURE = REPO_ROOT / "packages/matrx-scraper/tests/__fixtures__/page-checks-parity.json"


def _load_generator():
    spec = importlib.util.spec_from_file_location("_page_checks_parity_gen", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixture_matches_current_checks() -> None:
    generator = _load_generator()
    assert FIXTURE.read_text(encoding="utf-8") == generator.render(), (
        "page-checks-parity.json is stale: run_page_checks changed without "
        "regenerating the fixture, so matrx-frontend checks.ts is still asserting "
        "the OLD verdicts. Run:\n"
        "  .venv/bin/python packages/matrx-scraper/scripts/"
        "generate_page_checks_parity_fixture.py\n"
        "and make the matching change in matrx-frontend "
        "features/marketing/seo/audit/checks.ts."
    )


def test_fixture_covers_every_check_and_the_shell_rules() -> None:
    """A shrinking fixture is silent coverage loss."""
    generator = _load_generator()
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert fixture["check_names"] == list(
        generator.run_page_checks(generator.PageEvidence(url=generator.URL)).keys()
    )
    names = {case["name"] for case in fixture["cases"]}
    for required in (
        "healthy_page",
        "all_evidence_missing",
        "js_app_shell",
        "js_shell_unknown",
        "js_shell_root_text_at_limit",
        "js_shell_root_text_real_page",
        "dead_end_page",
        "canonical_names_start_url",
        "canonical_names_middle_hop",
        "kept_soft_404",
        "js_shell_bot_wall",
        "js_shell_non_2xx",
    ):
        assert required in names, f"fixture lost coverage for {required}"
