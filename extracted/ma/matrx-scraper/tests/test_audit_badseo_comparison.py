"""OpenSEO's public fixture site, audited by OUR crawler and checks — compared on mapped checks.

badseo.dev (https://github.com/every-app/open-seo, ``badseo/``) is a public
site built to be crawled: every page declares the exact OpenSEO issue set it
must raise. We run our real pipeline (the audit fixture harness, with the
network ON and production pacing) and compare ONLY on issue types that map to
one of our checks (``OPENSEO_TO_OURS``, verified by reading each check). Their
thresholds differ from ours on the "≈" rows, so an extra verdict there is a
threshold difference, never a mis-flag.

Network: opt-in (``-m network``). Recorded once for OPENSEO-TOOLS-SPEC §8.2.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from audit_fixture_harness import run_fixture_audit

BADSEO_ORIGIN = "https://badseo.dev"
EXPECTED = json.loads(
    (Path(__file__).parent / "fixtures" / "audit_site" / "badseo-expected.json").read_text()
)

#: OpenSEO issue id -> our check key (None = no check of ours answers it).
OPENSEO_TO_OURS: dict[str, str | None] = {
    "server-error": "server_error_5xx",
    "broken-internal-link": "broken_internal_links",
    "missing-title": "title_presence",
    "broken-page": "broken_page_4xx",
    "duplicate-title": "title_duplication",
    "duplicate-meta-description": "meta_description_duplication",
    "duplicate-content": "duplicate_content_exact",
    "missing-meta-description": "meta_description_presence",
    "missing-h1": "h1_presence",
    "multiple-h1": "h1_presence",
    "redirect-chain": "redirect_chain",
    "noindex-page": "meta_robots_conflicts",
    "redirect-loop": "redirect_loop",
    "canonicalized-page": "canonical_conflicts",
    "canonical-conflict": None,  # HTML vs Link-header canonical disagree; ours judges the target
    "thin-content": "thin_content",
    "images-missing-alt": "image_alt_presence",
    "orphan-page": "orphan_pages",
    "title-too-long": "title_length",
    "title-too-short": "title_length",
    "meta-description-too-long": "meta_description_length",
    "meta-description-too-short": "meta_description_length",
    "heading-order-skip": "heading_hierarchy",
    "slow-response": "ttfb_server_response",
    "deep-page": "crawl_depth",
    "no-outgoing-links": None,
    # Crawl states, not checks (spec §8.1 — Lane H's reason codes).
    "blocked-page": None,
    "rate-limited-page": None,
    "crawl-rate-limited": None,
}
#: Same concern, different threshold — an extra verdict of ours is not a mis-flag.
THRESHOLD_ROWS = frozenset({"thin_content", "title_length", "ttfb_server_response", "crawl_depth"})
MAPPED = frozenset(k for k in OPENSEO_TO_OURS.values() if k)


def compare(expected: dict[str, list[str]], raised: dict[str, set[str]]) -> list[dict[str, object]]:
    rows = []
    # Only THEIR declared fixture pages: a page they never assert (their home,
    # catalog, privacy page) has no truth to compare against.
    for path in sorted(expected):
        theirs = {OPENSEO_TO_OURS.get(i) for i in expected.get(path, [])} - {None}
        ours = raised.get(path, set()) & MAPPED
        for key in sorted(theirs | ours):
            if key in theirs and key in ours:
                verdict = "match"
            elif key in theirs:
                verdict = "MISS" if path in raised else "MISS (no verdict for this URL)"
            else:
                verdict = "threshold" if key in THRESHOLD_ROWS else "EXTRA"
            rows.append({"path": path, "check": key, "verdict": verdict})
    return rows


@pytest.mark.network
@pytest.mark.asyncio
async def test_badseo_mapped_comparison() -> None:
    run = await run_fixture_audit(None, SimpleNamespace(origin=BADSEO_ORIGIN), polite=True)
    expected = {path: entry["expected"] for path, entry in EXPECTED["pages"].items()}
    rows = compare(expected, run.raised_by_page)
    print(f"\nbadseo.dev mapped comparison (OpenSEO {EXPECTED['source_commit']}):")
    for row in rows:
        if row["verdict"] != "match":
            print(f"  {row['verdict']:<32} {row['path']:<40} {row['check']}")
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["verdict"])] = counts.get(str(row["verdict"]), 0) + 1
    print("  totals:", counts)
    print(
        "  crawl:", getattr(run.crawl_completed, "status", None), f"{len(run.raised_by_page)} pages"
    )
    assert run.raised_by_page, "the crawl produced no page verdicts at all"
