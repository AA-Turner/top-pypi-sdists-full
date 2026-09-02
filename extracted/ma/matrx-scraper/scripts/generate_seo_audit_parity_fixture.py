#!/usr/bin/env python
"""Generate the SEO-audit cross-language parity fixture.

`matrx_scraper/seo_audit.py::audit_html` is the CANONICAL single-page auditor.
matrx-extend's `src/lib/seo/audit.ts::runAudit` is a deliberate second
implementation of it — the live-DOM mirror (see that file's header for why the
server physically cannot produce its result). Four numeric rules had drifted
apart silently before 2026-08-09 and both sides were persisting different
numbers for the same page.

This script feeds a fixed set of HTML fixtures through the Python and writes
the answers it produced. The extension test
(`matrx-extend/tests/unit/seo-audit-fixture-parity.test.ts`) replays the same
HTML through `runAudit` and asserts identical output. If it fails, ONE SIDE
CHANGED WITHOUT THE OTHER — fix both in the same unit of work and regenerate.

Same recipe as matrx-frontend's `features/marketing/seo/audit/__fixtures__/
audit-parity.json` (which mirrors `audit_metrics.py`), whose generator was
never committed — this one is, deliberately.

Run:
    .venv/bin/python packages/matrx-scraper/scripts/generate_seo_audit_parity_fixture.py

Writes (both paths are repo-relative and both are committed):
    packages/matrx-scraper/tests/__fixtures__/seo-audit-parity.json
    ../matrx-extend/tests/fixtures/seo-audit-parity.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "packages" / "matrx-scraper"))

from matrx_scraper.seo_audit import audit_html  # noqa: E402

# Fields the extension can compare. The extension's display shape is nested;
# the 1:1 mapping onto these flat server names is documented in the header of
# matrx-extend `src/lib/seo/audit.ts` and applied in its parity test.
#
# Deliberately EXCLUDED (the extension does not and should not compute them —
# they need a crawl, not a tab): schema_org, h1/h2/h1_count, link_count, links,
# text_hash, content_fingerprint, structured_data, image_inventory, resources,
# page_identity, mixed_content, pagination.
COMPARED_FIELDS = (
    "url",
    "title",
    "title_length",
    "meta_description",
    "meta_description_length",
    "canonical",
    "robots",
    "lang",
    "hreflang",
    "og",
    "twitter",
    "schema_types",
    "headings",
    "internal_links",
    "external_links",
    "images_total",
    "images_missing_alt",
    "word_count",
    "sentence_count",
    "flesch_reading_ease",
)


def _page(head: str = "", body: str = "", *, lang: str = "en") -> str:
    """Wrap fixture fragments in a realistic document.

    NOTE the newlines between block elements. selectolax's
    `body.text(deep=True, separator=" ")` inserts a separator between text
    nodes; the DOM's `textContent` does not. Real HTML has whitespace between
    block tags, so both sides see the same word boundaries — fixtures must too,
    or they test a formatting artifact instead of a rule.
    """
    return (
        f'<!doctype html><html lang="{lang}"><head>\n{head}\n</head>\n'
        f"<body>\n{body}\n</body></html>"
    )


BASE = "https://example.com/page"


CASES: list[dict[str, str]] = [
    {
        "name": "sentences_no_trailing_whitespace",
        "why": (
            "The final sentence has no whitespace after its terminator. Counting "
            "DELIMITERS instead of split-pieces is off by one on every page and "
            "feeds the Flesch denominator directly. This is drift #1."
        ),
        "base_url": BASE,
        "html": _page("<title>Cat</title>", "<p>The cat sat.</p>"),
    },
    {
        "name": "sentences_multiple",
        "why": 're.split(r"[.!?]+\\s+", "One. Two. Three.") -> 3 pieces, not 2.',
        "base_url": BASE,
        "html": _page("<title>Three</title>", "<p>One. Two. Three.</p>"),
    },
    {
        "name": "sentences_abbreviations",
        "why": (
            "Neither side does linguistic sentence detection — 'Dr. ' and 'D.C. ' "
            "each split. Pinned so a well-meaning 'improvement' on one side alone "
            "is caught."
        ),
        "base_url": BASE,
        "html": _page(
            "<title>Abbrev</title>",
            "<p>Dr. Smith went to Washington D.C. yesterday. He left at 5 p.m. today!</p>",
        ),
    },
    {
        "name": "sentences_terminator_runs",
        "why": "[.!?]+ collapses runs: '!!!' and '?!' are one delimiter, not three.",
        "base_url": BASE,
        "html": _page(
            "<title>Runs</title>",
            "<p>Really?! Yes!!! Absolutely... maybe.</p>",
        ),
    },
    {
        "name": "headings_empty_and_duplicate",
        "why": (
            "Empty headings are skipped BEFORE the cap, and duplicates are kept "
            "(dedup is a cross-page job, not this one). Drift #2."
        ),
        "base_url": BASE,
        "html": _page(
            "<title>Headings</title>",
            "\n".join(
                [
                    "<h1>Real</h1>",
                    "<h2></h2>",
                    "<h2>   </h2>",
                    "<h2>Duplicate</h2>",
                    "<h2>Duplicate</h2>",
                    "<h3>Also real</h3>",
                    "<h6>Deep</h6>",
                ]
            ),
        ),
    },
    {
        "name": "headings_cap_200_after_empty_skip",
        "why": (
            "The 200 cap counts KEPT headings. Capping before the empty-skip lets "
            "blank <h_> wrappers (card grids) eat the slots and inflate the count."
        ),
        "base_url": BASE,
        "html": _page(
            "<title>Cap</title>",
            "\n".join(f"<h2></h2>\n<h2>H{i}</h2>" for i in range(205)),
        ),
    },
    {
        "name": "links_non_http_schemes",
        "why": (
            "javascript:/mailto:/tel:/#fragment must be counted as NEITHER. "
            "`new URL('javascript:void(0)')` parses fine with an empty host, so an "
            "exception-only guard counted them as external. Drift #3."
        ),
        "base_url": BASE,
        "html": _page(
            "<title>Links</title>",
            "\n".join(
                [
                    '<a href="/about">internal rel</a>',
                    '<a href="https://example.com/deep">internal abs</a>',
                    '<a href="https://other.test/x">external</a>',
                    '<a href="javascript:void(0)">js</a>',
                    '<a href="mailto:a@b.c">mail</a>',
                    '<a href="tel:+15551234">tel</a>',
                    '<a href="#frag">fragment</a>',
                    '<a href="ftp://files.test/x">ftp</a>',
                    "<a>no href at all</a>",
                ]
            ),
        ),
    },
    {
        "name": "links_subdomain_vs_same_host",
        "why": (
            "A subdomain counts as EXTERNAL on both sides. The Python tags it "
            'link_type="subdomain" for the link graph but still does `external += 1`.'
        ),
        "base_url": BASE,
        "html": _page(
            "<title>Hosts</title>",
            "\n".join(
                [
                    '<a href="https://example.com/same">same host</a>',
                    '<a href="https://blog.example.com/p">subdomain</a>',
                    '<a href="https://www.example.com/p">www is also a subdomain</a>',
                    '<a href="http://example.com/scheme">same host, other scheme</a>',
                    '<a href="https://notexample.com/p">different registrable</a>',
                ]
            ),
        ),
    },
    {
        "name": "zero_text_page",
        "why": (
            "No text -> word_count 0, sentence_count 0, flesch null. A `score ? ...` "
            "null-guard also turns a legitimate 0 into null; only 'no text' may."
        ),
        "base_url": BASE,
        "html": _page("<title>Empty</title>", "<div></div>"),
    },
    {
        "name": "flesch_clamp_single_sentence",
        "why": (
            "400 long words in ONE sentence drives raw Flesch far past the DB "
            "column's range. The ±999.99 clamp is part of the contract on both "
            "write paths. Drift #4."
        ),
        "base_url": BASE,
        "html": _page(
            "<title>Clamp</title>",
            "<p>" + " ".join(["extraordinarily"] * 400) + ".</p>",
        ),
    },
    {
        "name": "flesch_ordinary_prose",
        "why": "A normal score — pins the rounding (round(score*100)/100), not just the clamp.",
        "base_url": BASE,
        "html": _page(
            "<title>Prose</title>",
            "<p>The cat sat on the mat. The dog ran fast. Birds sing in the "
            "morning light. It was a good day for a walk.</p>",
        ),
    },
    {
        "name": "missing_title_description_canonical",
        "why": "Absent != empty. title '' / length 0; description and canonical null.",
        "base_url": BASE,
        "html": _page("", "<p>Body only.</p>", lang=""),
    },
    {
        "name": "title_and_description_whitespace",
        "why": (
            "The Python STRIPS the title before measuring length; the description "
            "content attribute is taken raw. Both lengths are persisted."
        ),
        "base_url": BASE,
        "html": _page(
            '<title>   Padded Title   </title>\n<meta name="description" content="A description.">',
            "<p>Body.</p>",
        ),
    },
    {
        "name": "kitchen_sink_metadata",
        "why": (
            "og/twitter/canonical/robots/hreflang/images/schema all at once. "
            "Absolute hrefs on purpose — see the relative-URL note in the test."
        ),
        "base_url": BASE,
        "html": _page(
            "\n".join(
                [
                    "<title>Kitchen Sink</title>",
                    '<meta name="description" content="Everything, all at once.">',
                    '<meta name="robots" content="index, follow">',
                    '<link rel="canonical" href="https://example.com/page">',
                    '<link rel="alternate" hreflang="es" href="https://example.com/es/page">',
                    '<link rel="alternate" hreflang="fr" href="https://example.com/fr/page">',
                    '<meta property="og:title" content="OG Title">',
                    '<meta property="og:description" content="OG Description">',
                    '<meta property="og:image" content="https://cdn.example.com/i.png">',
                    '<meta name="twitter:card" content="summary_large_image">',
                    '<meta name="twitter:title" content="TW Title">',
                    '<meta name="ignored" content="not og, not twitter">',
                    '<meta property="og:empty" content="">',
                    '<script type="application/ld+json">'
                    '{"@context":"https://schema.org","@type":"Article",'
                    '"author":{"@type":"Person","name":"A"}}'
                    "</script>",
                ]
            ),
            "\n".join(
                [
                    "<h1>Kitchen Sink</h1>",
                    '<img src="https://cdn.example.com/a.png" alt="described">',
                    '<img src="https://cdn.example.com/b.png" alt="">',
                    '<img src="https://cdn.example.com/c.png" alt="   ">',
                    '<img src="https://cdn.example.com/d.png">',
                    "<p>A short article body. It has two sentences.</p>",
                ]
            ),
        ),
    },
]


def build() -> dict:
    cases = []
    for case in CASES:
        result = audit_html(case["html"], case["base_url"]).to_dict()
        cases.append(
            {
                "name": case["name"],
                "why": case["why"],
                "base_url": case["base_url"],
                "html": case["html"],
                "expected": {k: result[k] for k in COMPARED_FIELDS},
            }
        )
    return {
        "_readme": (
            "GENERATED — do not hand-edit. Source of truth: "
            "matrx_scraper/seo_audit.py::audit_html. Regenerate with "
            ".venv/bin/python packages/matrx-scraper/scripts/"
            "generate_seo_audit_parity_fixture.py from the aidream repo root. "
            "If matrx-extend's seo-audit-fixture-parity test fails, one side "
            "changed without the other — fix BOTH in the same unit of work."
        ),
        "source": "packages/matrx-scraper/matrx_scraper/seo_audit.py::audit_html",
        "generator": "packages/matrx-scraper/scripts/generate_seo_audit_parity_fixture.py",
        "compared_fields": list(COMPARED_FIELDS),
        "cases": cases,
    }


def main() -> int:
    payload = build()
    body = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"

    targets = [
        REPO_ROOT / "packages/matrx-scraper/tests/__fixtures__/seo-audit-parity.json",
        REPO_ROOT.parent / "matrx-extend/tests/fixtures/seo-audit-parity.json",
    ]
    for target in targets:
        if not target.parent.parent.exists():
            print(f"SKIP (repo not present): {target}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        print(f"wrote {len(payload['cases'])} cases -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
