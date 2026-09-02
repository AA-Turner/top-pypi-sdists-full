"""Regression test for the ``fast=True`` extraction-rules bug (found 2026-07-23
building the WS-14 public SEO tools — the first real caller of ``fast=True``):
``matrx_scraper.parser.extraction_rules.rules`` is a ``list[dict]``, not a
name-keyed dict, so ``all_rules.items()`` always raised ``AttributeError``,
making the fast path entirely dead code."""

from __future__ import annotations

from matrx_scraper.orchestrator import _parse_html_content

_HTML = """
<html><head><title>Hello</title></head>
<body><h1>Hi</h1><p>Some visible text content for the page.</p></body></html>
"""


def test_fast_mode_extraction_does_not_raise() -> None:
    result = _parse_html_content(_HTML, "https://example.com/", fast=True)
    assert isinstance(result, dict)
    assert "links" in result
    assert "_pipeline" in result


def test_fast_and_slow_mode_both_produce_a_result() -> None:
    fast = _parse_html_content(_HTML, "https://example.com/", fast=True)
    slow = _parse_html_content(_HTML, "https://example.com/", fast=False)
    assert isinstance(fast, dict)
    assert isinstance(slow, dict)
