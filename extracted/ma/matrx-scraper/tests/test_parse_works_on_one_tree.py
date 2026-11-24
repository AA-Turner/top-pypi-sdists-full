"""A page parse works on ONE tree, and nothing in it rescans the page per element.

Operation counts, never timings, so none of these flakes:

- no deep copy of the page (there used to be three: the noise pass's marked copy,
  a copy read only for its body-text length, and the content filter's copy) —
  the readers (metadata, links) run first and the writers share the tree;
- the main-content finder makes no whole-tree soupsieve pass and no re-parse on a
  page none of its root selectors can match (it used to run 12 selectors over a
  fresh re-parse of every page), and the transformer makes no carousel pass on a
  page without one;
- the content filter's "text" rule extracts subtree text only for an element
  whose text is the rule's length (it used to extract it for nearly every
  element: elements x subtree);
- SimHash hashes each distinct word once (it used to hash every occurrence).

Output identity for all of this is pinned by tests/test_parse_identity.py.
"""

from __future__ import annotations

import copy

import bs4
import pytest

from matrx_scraper.parser import hashing, noise_remover, scrape_filter
from matrx_scraper.parser.core import _parse_html_sync

@pytest.fixture(autouse=True)
def _no_list_fetch(monkeypatch):
    # These count operations; the ad-block list's one fetch must not reach the network.
    from matrx_scraper.parser import utils

    def fail(url, **_kwargs):
        raise OSError("no network in tests")

    monkeypatch.setattr(utils.httpx, "get", fail)


_PAGE = "<html><head><title>T</title></head><body><nav><a href='/'>home</a></nav>" + "".join(
    f"<div class='item'><h2>H{i}</h2><p>Paragraph {i} with <a href='/p/{i}'>a link</a>.</p></div>" for i in range(30)
) + "<footer>(c) 2026</footer></body></html>"


def _count(monkeypatch, owner, name, predicate=lambda *a, **k: True):
    calls = {"n": 0}
    real = getattr(owner, name)

    def counting(*args, **kwargs):
        if predicate(*args, **kwargs):
            calls["n"] += 1
        return real(*args, **kwargs)

    monkeypatch.setattr(owner, name, counting)
    return calls


def test_no_full_tree_copy_per_parse(monkeypatch):
    copies = 0
    real = copy.deepcopy

    def counting(obj, *args, **kwargs):
        nonlocal copies
        if isinstance(obj, bs4.Tag):
            copies += 1
        return real(obj, *args, **kwargs)

    fake = type("copy_module", (), {"deepcopy": staticmethod(counting)})
    monkeypatch.setattr(noise_remover, "copy", fake)
    monkeypatch.setattr(scrape_filter, "copy", fake)
    _parse_html_sync(_PAGE, "https://example.test/a")
    assert copies == 0, f"a page parse deep-copied the page {copies} times; it works on one tree"


def test_no_selector_pass_or_reparse_for_a_page_without_an_article_root(monkeypatch):
    selects = _count(monkeypatch, bs4.element.Tag, "select")
    builds = _count(monkeypatch, bs4.BeautifulSoup, "__init__")
    _parse_html_sync(_PAGE, "https://example.test/a")
    assert selects["n"] == 0, f"{selects['n']} whole-tree soupsieve passes on a page no selector can match"
    # The page, the transformer's normalising re-parse, the extractor's re-parse of
    # its flattened text — and nothing for the main-content finder.
    assert builds["n"] == 3, f"{builds['n']} BeautifulSoup trees built for one page"


def test_text_rule_reads_subtree_text_only_at_its_length(monkeypatch):
    text_checks = _count(
        monkeypatch,
        scrape_filter.ScrapeFilter,
        "check_element",
        lambda self, element, attribute, values, match_type: attribute == "text",
    )
    _parse_html_sync(_PAGE, "https://example.test/a")
    assert text_checks["n"] == 0, f"the 'text' rule extracted subtree text {text_checks['n']} times"
    text_checks["n"] = 0
    out = _parse_html_sync(_PAGE.replace("<footer>", "<div><span>Advertisement</span></div><footer>"), "https://example.test/a")
    assert text_checks["n"] == 2  # the div and the span: the only elements of that length
    assert "Advertisement" not in str(out)


def test_simhash_hashes_each_distinct_word_once(monkeypatch):
    md5 = _count(monkeypatch, hashing.hashlib, "md5")
    text = " ".join(["alpha", "beta", "gamma"] * 500)
    hashing.compute_simhash(text)
    assert md5["n"] == 3


def test_filter_soup_and_remove_noise_still_copy_by_default():
    soup = bs4.BeautifulSoup("<html><body><p class='ad'>x</p><nav>n</nav></body></html>", "lxml")
    before = str(soup)
    scrape_filter.ScrapeFilter().filter_soup(
        soup, content_filter_config=[{"attribute": "class", "exact": ["ad"], "partial": [], "regex": []}]
    )
    noise_remover.NoiseRemover().remove_noise(soup)
    assert str(soup) == before, "filter_soup / remove_noise must not mutate their input unless copy_input=False"


def test_a_callers_tree_is_never_rewritten():
    from matrx_scraper.parser.core import ParserOrchestrator

    soup = bs4.BeautifulSoup(_PAGE, "lxml")
    before = str(soup)
    ParserOrchestrator().parse_content(soup, "https://example.test/a")
    assert str(soup) == before
