"""A ONE-word term written as exactly two adjacent words hits — in THE shared matcher, so
``text.term_scan``, ``data.check_items`` and the request firewall agree (V6 review, 2026-10-27:
the firewall had a private copy of this rule, so the scanner passed a quote the firewall then
refused the whole writing pass for). Only an exact join counts."""

from __future__ import annotations

import pytest

from matrx_graph.text_match import TermMatcher


def _hit(term: str, text: str) -> bool:
    return bool(TermMatcher([(term, "brand")], strip_accents=True).scan(text)[0])


@pytest.mark.parametrize("text", ["Try Brew lio today.", "Brew-lio is new.", "the brew_lio app", "Ac me"])
def test_a_one_word_term_split_once_hits(text: str) -> None:
    term = "Acme" if text == "Ac me" else "Brewlio"
    assert _hit(term, text)


@pytest.mark.parametrize(
    ("term", "text"),
    [
        ("Brewlio", "a brew list for Friday"),  # joins to "brewlist", not the term
        ("Brewlio", "brew li o"),  # three pieces that are not single letters
        ("Acme", "the academy"),
        ("AI Matrx", "we aim at rx"),  # a two-word term keeps its own rule
    ],
)
def test_only_an_exact_two_word_join_hits(term: str, text: str) -> None:
    assert not _hit(term, text)
