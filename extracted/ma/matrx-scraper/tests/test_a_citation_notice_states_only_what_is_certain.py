"""The citation notice states only mechanical facts (closing pass, 2026-11-17).

The real 2-query run of 2026-11-17 (``tests/fixtures/real_run_report_sourdough.txt``: the first group's report, as the
writer returned it after the citation check) cited every page it read, yet an earlier notice told the reader
"Partly cited: 4 of 39 paragraphs or list items" because it counted list lead-ins and the writer's own
"Sources:" labels as uncited claims. Only two things are certain by machine: how many distinct read pages the report
cites, and how many were read. A report that cites none opens with the uncited notice; nothing else is written.
"""

from __future__ import annotations

from pathlib import Path

from matrx_scraper.features import research_budget
from matrx_scraper.features.research_budget import canonical_url, citation_coverage, citation_notice

REAL_REPORT = (Path(__file__).parent / "fixtures" / "real_run_report_sourdough.txt").read_text()


def _read_keys() -> set[str]:
    return {canonical_url(m.group(0).rstrip(".,;:")) for m in research_budget._URL.finditer(REAL_REPORT)}


def test_the_real_fully_cited_report_gets_no_partly_cited_notice() -> None:
    keys = _read_keys()
    coverage = citation_coverage(REAL_REPORT, keys)
    assert citation_notice(coverage) == ""
    assert coverage == {"read_pages_cited": len(keys), "pages_read": len(keys)}


def test_the_paragraph_counting_is_gone() -> None:
    assert not hasattr(research_budget, "report_units")
    assert "Partly cited" not in Path(research_budget.__file__).read_text()


def test_a_report_citing_none_of_the_read_pages_opens_with_the_uncited_notice() -> None:
    coverage = citation_coverage("Owners review the scorecard every Monday.", {canonical_url("https://a.example/1")})
    assert coverage == {"read_pages_cited": 0, "pages_read": 1}
    assert citation_notice(coverage).startswith("[Uncited report:")


def test_cited_pages_are_counted_once_and_a_page_not_read_does_not_count() -> None:
    keys = {canonical_url("https://a.example/1"), canonical_url("https://a.example/2")}
    text = "A (https://a.example/1). B (https://a.example/1; https://a.example/2). C (https://other.example/x)."
    assert citation_coverage(text, keys) == {"read_pages_cited": 2, "pages_read": 2}
