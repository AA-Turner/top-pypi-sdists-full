"""Adversarial review of f83b7d49 (2026-10-27): the term scan leaked names past a blind wall.

Every case here was a miss (or a false "clean") in the first ``text.term_scan``; the shared
matcher (``matrx_graph.text_match``) closes them for ``text.term_scan`` and ``data.check_items``
``not_contains`` alike. The compact-match false-positive guards are here too, both directions.
"""

from __future__ import annotations

import time
import unicodedata

import pytest

from matrx_graph.nodes.text.similarity import SimilarityConfig, SimilarityExecutor, SimilarityInput
from matrx_graph.nodes.text.term_scan import TermScanConfig, TermScanExecutor, TermScanInput
from matrx_graph.types.result import Failure


async def _scan(text=None, items=None, terms=(), **cfg):
    return await TermScanExecutor().execute(
        None, TermScanInput(text=text, items=items, terms=list(terms)), TermScanConfig(**cfg)
    )


async def scan(text=None, items=None, terms=(), **cfg):
    out = await _scan(text, items, terms, **cfg)
    assert not isinstance(out, Failure), out.error.message
    return out.result


LEAKS = [
    ("Try AIMatrx today", "AI Matrx"),
    ("Try A.I. Matrx", "AI Matrx"),
    ("Try AI Matrx", "AIMatrx"),
    ("drink CocaCola", "Coca-Cola"),
    ("OReilly books", "O'Reilly"),
    ("O'Reilly books", "OReilly"),
    ("A c m e", "Acme"),
    ("Ac​me rocks", "Acme"),
    ("Ac­me rocks", "Acme"),
    ("Ac‍me rocks", "Acme"),
    ("İSTANBUL tours", "istanbul"),
    (unicodedata.normalize("NFD", "visit Café Olé"), "Café Olé"),
    ("visit Café Olé", unicodedata.normalize("NFD", "Café Olé")),
    (unicodedata.normalize("NFD", "Zoë"), "Zoë"),
    ("visit example.com today", "https://www.example.com/"),
    ("visit example.com today", "www.example.com"),
    ("see https://www.example.com/pricing now", "example.com"),
]


@pytest.mark.parametrize(("text", "term"), LEAKS)
async def test_text_match_no_leaks(text, term):
    out = await scan(text=text, terms=[term])
    assert not out.clean, (text, term)
    hit = out.hits[0]
    # Positions still index the ORIGINAL text, whatever the folding did.
    assert text[hit.start : hit.end] == hit.matched_text


@pytest.mark.parametrize(
    ("text", "term"),
    [
        ("the academy opens", "Acme"),
        ("we aim at rx savings", "AI Matrx"),
        ("we aim at rx savings", "AIMatrx"),
        ("a party for all", "art"),
    ],
)
async def test_text_match_compact_never_invents_a_name(text, term):
    out = await scan(text=text, terms=[term])
    assert out.clean, (text, term, out.hits)


async def test_text_match_bad_text_path_fails_with_a_sentence():
    out = await _scan(items=[{"brief": {"text": "We love Acme"}}], terms=["Acme"], text_path="brief.txt")
    assert isinstance(out, Failure)
    assert "brief.txt" in out.error.message


async def test_text_match_zero_usable_terms_fails_with_a_sentence():
    out = await _scan(text="Acme", terms=["Acme"], classes=["brands"])
    assert isinstance(out, Failure)
    assert "brands" in out.error.message


async def test_text_match_punctuation_distinct_terms_kept():
    out = await scan(text="I use C# daily", terms=["C++", "C#"])
    assert out.term_count == 2
    assert [h.term for h in out.hits] == ["C#"]
    # The symbols are required: folded "C++" never hits a lone "C".
    out = await scan(text="grade C work", terms=["C++"])
    assert out.clean


async def test_text_match_exact_mode_strips_outer_whitespace():
    out = await scan(text="Ask Acme now", terms=["  Acme "], match="exact")
    assert [h.matched_text for h in out.hits] == ["Acme"]


async def test_text_match_accents_kept_unless_asked():
    out = await scan(text="Cafe Ole", terms=["Café Olé"])
    assert out.clean
    out = await scan(text="Cafe Ole", terms=["Café Olé"], strip_accents=True)
    assert not out.clean


async def test_text_match_curly_apostrophe_similarity():
    out = await SimilarityExecutor().execute(
        None,
        SimilarityInput(text="don't buy cheap shoes", candidates=["don’t buy cheap shoes"]),
        SimilarityConfig(method="jaccard"),
    )
    assert out.result.best.score == 1.0


async def test_text_match_similarity_best_is_null_when_nothing_overlaps():
    out = await SimilarityExecutor().execute(
        None, SimilarityInput(text="red apples", candidates=["blue whales"]), SimilarityConfig(method="jaccard")
    )
    assert out.result.best is None


async def test_text_match_pairs_group_by_and_any_of_several_methods():
    items = [
        {"q": "best running shoes", "locale": "en"},
        {"q": "best running shoe", "locale": "en"},
        {"q": "best running shoes", "locale": "fr"},
    ]
    out = await SimilarityExecutor().execute(
        None,
        SimilarityInput(items=items),
        SimilarityConfig(
            text_path="q",
            pairs=True,
            group_by="locale",
            pair_methods=[{"method": "jaccard", "threshold": 0.6}, {"method": "char3_cosine", "threshold": 0.85}],
        ),
    )
    pairs = out.result.pairs
    # 0-1 fail Jaccard (0.5) but pass char-3 (0.9193); 0-2 is identical but in another group.
    assert [(p.a, p.b, p.nominated_by) for p in pairs] == [(0, 1, ["char3_cosine"])]
    assert pairs[0].scores == {"jaccard": 0.5, "char3_cosine": 0.9193}


def _bench_corpus():
    import random

    rng = random.Random(7)
    letters = "abcdefghijklmnopqrstuvwxyz"
    vocab = ["".join(rng.choice(letters) for _ in range(rng.randint(3, 11))) for _ in range(3000)]
    terms = [
        " ".join(rng.choice(vocab) for _ in range(rng.choice([1, 1, 2, 3]))) + rng.choice(["", "", "Co"])
        for _ in range(1000)
    ]
    items = [" ".join(rng.choice(vocab) for _ in range(150)) for _ in range(300)]
    return terms, items


def _naive_substring_pass(terms, items):
    """The cheapest possible scan of the same corpus: one ``in`` per term per item.

    Measured in the SAME process right beside the matcher, so a loaded machine slows
    both and the ratio holds (a fixed wall-clock budget failed at 2.08s vs 2.0s under
    load, 2026-10-27). Pure CPU, no I/O, no shared state."""
    low = [i.lower() for i in items]
    t0 = time.perf_counter()
    for term in terms:
        needle = term.lower()
        for text in low:
            needle in text
    return time.perf_counter() - t0


# How many times the naive substring pass the matcher may cost. Measured 2026-10-27 on an idle
# machine: ~6x (exact) and ~20x (fuzzy); the factors keep ~3x headroom. A matcher that goes
# quadratic (re-normalising per term x item pair, say) costs hundreds of times the baseline.
_SCAN_COST_FACTOR = {False: 18, True: 60}


@pytest.mark.parametrize("fuzzy", [False, True])
async def test_text_match_scan_speed(fuzzy):
    terms, items = _bench_corpus()
    # Best of three on both sides: a load spike hits one sample, never the minimum of three.
    baseline = min(_naive_substring_pass(terms, items) for _ in range(3))
    elapsed = float("inf")
    for _ in range(3):
        t0 = time.perf_counter()
        out = await scan(items=items, terms=terms, fuzzy={"enabled": fuzzy})
        elapsed = min(elapsed, time.perf_counter() - t0)
        assert len(out.results) == 300
    limit = _SCAN_COST_FACTOR[fuzzy] * baseline
    assert elapsed < limit, (
        f"{elapsed:.2f}s vs {baseline:.3f}s naive baseline (limit {_SCAN_COST_FACTOR[fuzzy]}x = {limit:.2f}s) "
        f"for 1,000 terms x 300 items x 150 words (fuzzy={fuzzy})"
    )


def _ci(items, **spec):
    from matrx_graph.checks import ItemCheckSpec, check_items

    return check_items(items, [ItemCheckSpec(key="never", type="not_contains", path="t", **spec)])


def test_text_match_check_items_not_contains_shares_the_matcher():
    items = [{"t": "Try AIMatrx today"}, {"t": "Ask Mrs. Smith"}, {"t": "The Marketplce opens"}, {"t": "plain text"}]
    out = _ci(items, terms=["AI Matrx", "Marketplace"], fuzzy=0.86)
    # The run-together name drops its item; the near miss is FLAGGED and kept.
    assert [r.index for r in out.rejected] == [0]
    assert [(f.index, f.term, f.matched_text, f.score) for f in out.flagged] == [
        (2, "Marketplace", "marketplce", 0.9524)
    ]
    assert out.flagged_count == 1 and out.kept == 3
    # fuzzy_drops opts into dropping a near miss.
    out = _ci(items, terms=["AI Matrx", "Marketplace"], fuzzy=0.86, fuzzy_drops=True)
    assert [r.index for r in out.rejected] == [0, 2] and out.flagged == []


def test_text_match_check_items_flagged_is_present_and_zero_when_nothing_is_near():
    out = _ci([{"t": "plain text"}], terms=["Marketplace"], fuzzy=0.86)
    assert out.flagged == [] and out.flagged_count == 0


@pytest.mark.parametrize(("word", "term"), [("contact", "contract"), ("serviced", "services"), ("raining", "training")])
def test_text_match_check_items_everyday_near_misses_are_flagged_not_dropped(word, term):
    out = _ci([{"t": f"we offer {word} today"}], terms=[term], fuzzy=0.86)
    assert out.kept == 1 and out.dropped == 0
    assert [f.term for f in out.flagged] == [term]


@pytest.mark.parametrize(("term", "text"), [("C++", "I like c"), ("AT&T", "call at t now")])
async def test_text_match_symbols_are_required_in_both_steps(term, text):
    assert _ci([{"t": text}], terms=[term]).kept == 1
    assert (await scan(text=text, terms=[term])).clean
    assert _ci([{"t": f"we use {term} daily"}], terms=[term]).dropped == 1
    assert not (await scan(text=f"we use {term} daily", terms=[term])).clean


async def test_text_match_html_is_read_as_text_only_when_asked():
    html = "Try <b>AI</b> <span>Matrx</span> &amp; more"
    out = await scan(text=html, terms=["AI Matrx", "&"])
    # Off by default: the tags sit between the words.
    assert [h.term for h in out.hits] == []
    out = await scan(text=html, terms=["AI Matrx"], strip_html=True)
    assert [(h.term, h.matched_text) for h in out.hits] == [("AI Matrx", "AI</b> <span>Matrx")]
    # check_items keeps its HTML stripping.
    assert _ci([{"t": html}], terms=["AI Matrx"]).dropped == 1


# --- Second review (firewall reviewer, 2026-10-27): more spellings that slipped past ------------

SECOND_LEAKS = [
    ("Try AI_Matrx now", "AI Matrx"),  # snake_case: the underscore joins words
    ("Ask AcmeCorp today", "Acme"),  # the term starts a run-together word
    ("Two Acmes opened", "Acme"),  # plural
    ("Call I.B.M. support", "IBM"),  # dotted initials of a short term
    ("Ac͏me rocks", "Acme"),  # combining grapheme joiner (default-ignorable)
    ("Acme️ rocks", "Acme"),  # variation selector (default-ignorable)
    ("Ac⁤me rocks", "Acme"),  # invisible plus (default-ignorable, from the property, not a hand list)
    ("Аcme rocks", "Acme"),  # Cyrillic capital A
    ("ΑCME rocks", "Acme"),  # Greek capital Alpha
    ("Acmе rocks", "Acme"),  # Cyrillic small ie
    ("АСМЕ rocks", "Acme"),  # all-Cyrillic lookalike (TR39 whole-script confusable)
    ("Visit Москва now", "Москва"),  # a Cyrillic term still finds itself
    ("我爱北京", "北京"),  # a script without spaces: substring is a match
    ("東京タワーへ", "タワー"),
]


@pytest.mark.parametrize(("text", "term"), SECOND_LEAKS)
async def test_text_match_second_review_no_leaks(text, term):
    out = await scan(text=text, terms=[term])
    assert not out.clean, (text, term)
    hit = out.hits[0]
    assert text[hit.start : hit.end] == hit.matched_text


@pytest.mark.parametrize(
    ("text", "term"),
    [
        ("the academy opens", "Acme"),
        ("we aim at rx savings", "AI Matrx"),
        ("I bought a cab", "IBM"),
        ("a party for all", "art"),
        ("Москва", "Moscow"),  # a Russian word is compared as itself
    ],
)
async def test_text_match_second_review_no_false_hits(text, term):
    out = await scan(text=text, terms=[term])
    assert out.clean, (text, term, out.hits)


async def test_text_match_exact_mode_is_whole_word():
    out = await scan(text="Acmes and Acme", terms=["Acme"], match="exact")
    assert [h.start for h in out.hits] == [10]


def test_text_match_check_items_catches_the_second_review_spellings():
    out = _ci([{"t": "Try AI_Matrx"}, {"t": "Аcme rocks"}, {"t": "plain"}], terms=["AI Matrx", "Acme"])
    assert [r.index for r in out.rejected] == [0, 1]
