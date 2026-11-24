"""A single-page condense gets the same budget as research_web: the head kept, the cap marked in the text."""

from matrx_scraper.features.read_page import fit_for_condenser
from matrx_scraper.features.research_budget import CONDENSE_MAX_CHARS


def test_a_short_page_is_untouched():
    assert fit_for_condenser("hello") == "hello"


def test_a_long_page_is_capped_to_the_research_budget_and_says_so():
    page = "word " * CONDENSE_MAX_CHARS
    out = fit_for_condenser(page)
    assert len(out) < CONDENSE_MAX_CHARS + 100
    assert f"[Page capped: {CONDENSE_MAX_CHARS:,} of" in out
