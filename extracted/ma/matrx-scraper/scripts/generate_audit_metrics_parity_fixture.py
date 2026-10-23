#!/usr/bin/env python
"""Generate the page-audit METRICS parity fixture (Python -> TS mirrors).

`matrx_scraper/audit_metrics.py` owns four deterministic evaluators — social
card, heading structure, URL quality and indexability. Two TypeScript copies
mirror them byte-for-byte:

    matrx-frontend  features/marketing/seo/audit/{social,headings,url-quality,indexability,stored}.ts
                    (proved by audit.parity.test.ts)
    matrx-extend    src/lib/seo/evaluators/*.ts
                    (proved by tests/unit/seo-evaluator-parity.test.ts)

This script runs every input below through the Python and writes what it
answered. Before 2026-10-22 the fixture had no generator: it was hand-copied,
so when `evaluate_indexability` learned to resolve relative canonicals and to
accept the requested URL or a redirect hop as "self", both TS copies lagged
with every test green.

Run from the aidream repo root:
    .venv/bin/python packages/matrx-scraper/scripts/generate_audit_metrics_parity_fixture.py

Writes (all committed, byte-identical):
    packages/matrx-scraper/tests/__fixtures__/audit-parity.json   <- THE home
    ../matrx-frontend/features/marketing/seo/audit/__fixtures__/audit-parity.json
    ../matrx-extend/tests/unit/__fixtures__/audit-parity.json

`tests/test_audit_metrics_parity_fixture.py` regenerates in memory and fails
when the home is stale. Each mirror's parity test reads the aidream home when
the sibling checkout exists and fails when its vendored copy differs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "packages" / "matrx-scraper"))

from matrx_scraper.audit_metrics import (  # noqa: E402
    evaluate_heading_structure,
    evaluate_indexability,
    evaluate_social_card,
    evaluate_url_quality,
)

# fmt: off
SOCIAL_CASES: list[dict[str, Any]] = [{'og': {}, 'twitter': {}},
     {'og': {'og:title': 'AI Matrx - Enterprise AI Platform',
             'og:description': 'Build AI apps without code.',
             'og:image': 'https://aimatrx.com/og.png',
             'og:site_name': 'AI Matrx',
             'og:url': 'https://aimatrx.com/',
             'og:type': 'website'},
      'twitter': {'twitter:card': 'summary_large_image',
                  'twitter:title': 'AI Matrx',
                  'twitter:description': 'x desc',
                  'twitter:image': 'https://aimatrx.com/tw.png'}},
     {'og': {'og:title': '  Trimmed  ', 'og:image': 'http://insecure.com/img.jpg'},
      'twitter': {'twitter:card': 'gallery'}},
     {'og': {'og:description': 'Only a description here'},
      'twitter': {'twitter:title': 'Twitter-only title',
                  'twitter:image': 'https://x.com/i.png'}},
     {'og': {'og:title': 'This is an extremely long social sharing title that goes well past '
                         'the seventy character truncation threshold used by platforms',
             'og:type': 'article',
             'og:url': 'https://ex.com/a',
             'og:image': 'https://ex.com/i.jpg',
             'og:description': 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'},
      'twitter': {'twitter:card': 'summary'}},
     {'og': {'og:title': 42, 'og:image': None}, 'twitter': {'twitter:card': '   '}}]

HEADINGS_CASES: list[Any] = [[],
     [{'text': 'Welcome', 'level': 1},
      {'text': 'About', 'level': 2},
      {'text': 'Team', 'level': 3}],
     [{'text': 'Intro', 'level': 2}, {'text': 'Deep', 'level': 5}],
     [{'text': 'One', 'level': 1},
      {'text': 'Two', 'level': 1},
      {'text': '', 'level': 2},
      {'text': '  ', 'level': 3}],
     [{'text': 'A really long heading that keeps going and going far past the seventy '
               'character threshold for headings',
       'level': 1},
      {'text': 'ok', 'level': 2},
      {'text': 'skip', 'level': 4}],
     [{'text': 'bad level', 'level': 9},
      {'text': 'no level'},
      'not a dict',
      {'text': 'Real', 'level': 1}]]

URL_QUALITY_CASES: list[str] = ['https://example.com/',
     'https://example.com/blog/my-post',
     'https://EXAMPLE.com/Blog/My_Post?utm_source=x#section',
     'https://example.com/a/b/c/d/e/f/deep-page',
     'https://example.com/caf%C3%A9/menu',
     'https://example.com//double//slash',
     'https://example.com/very-long-segment-very-long-segment-very-long-segment-very-long-segment-very-long-segment-very-long-segment-very-long-segment-very-long-segment-end',
     'not a url at all']

INDEXABILITY_CASES: list[dict[str, Any]] = [{'http_status': 200,
      'meta_robots': None,
      'canonical_url': None,
      'redirect_chain': [],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': 'index, follow',
      'canonical_url': 'https://ex.com/page/',
      'redirect_chain': [],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': 'NOINDEX, nofollow',
      'canonical_url': 'https://ex.com/other',
      'redirect_chain': [{'url': 'http://ex.com/page', 'status': 301},
                         {'url': 'https://ex.com/page', 'status': 200}],
      'final_url': 'https://ex.com/page'},
     {'http_status': 404,
      'meta_robots': None,
      'canonical_url': None,
      'redirect_chain': [],
      'final_url': 'https://ex.com/missing'},
     {'http_status': None,
      'meta_robots': 'none',
      'canonical_url': 'HTTPS://EX.COM:443/Page',
      'redirect_chain': [{'url': 'a', 'status': None}],
      'final_url': 'https://ex.com/Page'},
     {'http_status': 200,
      'meta_robots': ' index ,  NOFOLLOW ',
      'canonical_url': 'not a url',
      'redirect_chain': [{'url': '1', 'status': 301},
                         {'url': '2', 'status': 302},
                         {'url': '3', 'status': 200}],
      'final_url': 'https://ex.com/x?b=2'}]

CANONICAL_RESOLUTION_CASES: list[dict[str, Any]] = [{'http_status': 200,
      'meta_robots': None,
      'canonical_url': '/page',
      'redirect_chain': [],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': '//ex.com/page',
      'redirect_chain': [],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': 'https://other.com/page',
      'redirect_chain': [],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': '/other',
      'redirect_chain': [],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': 'https://ex.com/old-page',
      'redirect_chain': [],
      'final_url': 'https://ex.com/page',
      'requested_url': 'https://ex.com/old-page'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': 'http://ex.com/start',
      'redirect_chain': [{'url': 'http://ex.com/start', 'status': 301},
                         {'url': 'https://ex.com/page', 'status': 200}],
      'final_url': 'https://ex.com/page'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': 'https://ex.com/start',
      'redirect_chain': [{'url': 'https://ex.com/start', 'status': 301},
                         {'url': 'https://ex.com/middle', 'status': 301},
                         {'url': 'https://ex.com/page', 'status': 200}],
      'final_url': 'https://ex.com/page',
      'requested_url': 'https://ex.com/start'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': '/middle',
      'redirect_chain': [{'url': 'https://ex.com/start', 'status': 301},
                         {'url': 'https://ex.com/middle', 'status': 301},
                         {'url': 'https://ex.com/page', 'status': 200}],
      'final_url': 'https://ex.com/page',
      'requested_url': 'https://ex.com/start'},
     {'http_status': 200,
      'meta_robots': None,
      'canonical_url': 'https://ex.com/page',
      'redirect_chain': [{'url': 'https://ex.com/start', 'status': 301},
                         {'url': 'https://ex.com/middle', 'status': 301},
                         {'url': 'https://ex.com/page', 'status': 200}],
      'final_url': 'https://ex.com/page',
      'requested_url': 'https://ex.com/start'}]
# fmt: on
# CANONICAL_RESOLUTION_CASES, in order: relative self, protocol-relative self,
# cross-domain, relative elsewhere, canonical = the requested URL (no redirect),
# canonical = the redirecting start URL (2 hops), then a 3-hop chain with the
# canonical naming its start, its middle, and its final URL. Only the final URL
# (or the requested URL when nothing redirected) is self. `resolve_canonical_url` / `canonical_is_self` decide each.


def _indexability(case: dict[str, Any]) -> dict[str, Any]:
    return evaluate_indexability(
        case["http_status"],
        case["meta_robots"],
        case["canonical_url"],
        case["redirect_chain"],
        case["final_url"],
        case.get("requested_url"),
    )


def build() -> dict[str, Any]:
    return {
        "_readme": (
            "GENERATED — do not hand-edit. Source of truth: "
            "matrx_scraper/audit_metrics.py. Regenerate with .venv/bin/python "
            "packages/matrx-scraper/scripts/generate_audit_metrics_parity_fixture.py "
            "from the aidream repo root."
        ),
        "social": [
            {"input": c, "output": evaluate_social_card(c["og"], c["twitter"])}
            for c in SOCIAL_CASES
        ],
        "headings": [
            {"input": c, "output": evaluate_heading_structure(c)} for c in HEADINGS_CASES
        ],
        "indexability": [
            {"input": c, "output": _indexability(c)}
            for c in [*INDEXABILITY_CASES, *CANONICAL_RESOLUTION_CASES]
        ],
        "url_quality": [{"input": c, "output": evaluate_url_quality(c)} for c in URL_QUALITY_CASES],
    }


HOME = REPO_ROOT / "packages/matrx-scraper/tests/__fixtures__/audit-parity.json"
VENDORED = (
    REPO_ROOT.parent / "matrx-frontend/features/marketing/seo/audit/__fixtures__/audit-parity.json",
    REPO_ROOT.parent / "matrx-extend/tests/unit/__fixtures__/audit-parity.json",
)


def render() -> str:
    return json.dumps(build(), indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def main() -> int:
    body = render()
    for target in (HOME, *VENDORED):
        if not target.parent.parent.exists():
            print(f"SKIP vendored copy (repo not present): {target}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        print(f"wrote -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
