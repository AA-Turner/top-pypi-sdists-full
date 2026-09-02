"""The SEO-audit parity fixture must stay current with `audit_html`.

matrx-extend's `src/lib/seo/audit.ts` is a declared LIVE-DOM mirror of
`seo_audit.audit_html`, and `matrx-extend/tests/unit/seo-audit-fixture-parity.test.ts`
proves it against a fixture generated from THIS side. That only works if the
fixture is regenerated whenever the Python's counting rules change — otherwise
the extension is pinned to a stale answer and the drift the whole exercise
exists to catch reappears on the server side instead.

So: this test regenerates the fixture in memory and compares. A failure means
you changed `audit_html` without regenerating. Regenerate AND make the matching
change in matrx-extend in the same unit of work:

    .venv/bin/python packages/matrx-scraper/scripts/generate_seo_audit_parity_fixture.py
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATOR = REPO_ROOT / "packages/matrx-scraper/scripts/generate_seo_audit_parity_fixture.py"
FIXTURE = REPO_ROOT / "packages/matrx-scraper/tests/__fixtures__/seo-audit-parity.json"


def _load_generator():
    spec = importlib.util.spec_from_file_location("_seo_parity_gen", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixture_matches_current_auditor() -> None:
    generator = _load_generator()
    assert json.loads(FIXTURE.read_text(encoding="utf-8")) == generator.build(), (
        "seo-audit-parity.json is stale. audit_html changed without regenerating "
        "the fixture, so matrx-extend is still asserting the OLD answers. Run:\n"
        "  .venv/bin/python packages/matrx-scraper/scripts/"
        "generate_seo_audit_parity_fixture.py\n"
        "and make the matching change in matrx-extend's src/lib/seo/audit.ts."
    )


def test_fixture_still_covers_the_rules_that_drifted() -> None:
    """A shrinking fixture is silent coverage loss — pin the four real bugs."""
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    names = {case["name"] for case in fixture["cases"]}
    for required in (
        "sentences_no_trailing_whitespace",
        "headings_empty_and_duplicate",
        "headings_cap_200_after_empty_skip",
        "links_non_http_schemes",
        "flesch_clamp_single_sentence",
    ):
        assert required in names, f"fixture lost coverage for {required}"
