"""``text.term_scan`` proper-name terms: an everyday-word name counts only where written as a name.

Break this guards: drop the ``proper_name_only`` filter in ``TermMatcher.scan`` (or the
``everyday_words`` marking) and "Render times got slow …" is flagged as a brand leak again — the
over-match that kills good blind questions. Drop the mid-sentence rule and "Rendering in Render
is slow" leaks a brand. The expected values below are the REFERENCE matcher's answers
(``matrx_seo.name_matching.proper_name_match`` as of origin/main 2026-10-27, run on these exact
sentences), frozen here as literals.

Rule 3 users exercised: blind panel questions (a never-say list, ``everyday_words: auto``),
brand-neutral copywriting (text mode, ``everyday_words`` as a list), unbranded keyword research
(items mode, per-term ``match``).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.text_match import TermMatcher

from tests._fixtures import make_app_context


async def _run(inputs: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "text.term_scan",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config or {}, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-term-scan-names", inputs=inputs)
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["n"]


def _name_hits(term: str, text: str, co_terms: tuple[str, ...] = ()) -> list[str]:
    m = TermMatcher([(term, None, "proper_name_only"), *((c, None, "any") for c in co_terms)])
    return [h.matched_text for h in m.scan(text)[0] if h.term == term]


# (term, sentence, co_terms, reference answer) — the reference's own output on each sentence.
PARITY = [
    ("Render", "Render times got slow, what should a small studio upgrade first?", (), None),
    ("Render", "Rendering in Render is slow", (), "Render"),
    ("Apple", "I baked an apple pie.", (), None),
    ("Apple", "Apple pie is my favourite dessert.", (), None),
    ("Apple", "We switched to Apple last year.", (), "Apple"),
    ("Apple", "Apple vs Samsung: which phone lasts longer?", (), "Apple"),
    ("Render", "Render's free tier sleeps after 15 minutes.", (), "Render"),
    ("Render", "Render.com hosts our API.", (), "Render"),
    ("Render", "Render offers managed Postgres.", (), "Render"),
    ("Monday", "Monday is the best day to post.", (), None),
    ("Render", "Heroku or Render for a side project?", (), "Render"),
    ("Render", "- Render\n- Fly", (), "Render"),
    ("Notion", "Notion: a great place for docs.", (), "Notion"),
    ("Notion", "The notion that prices fall is wrong.", (), None),
    ("Notion", "Notion has a database feature.", (), "Notion"),
    ("Notion", "Notion has crossed my mind.", (), None),
    ("Stream", '"Stream" was the answer they picked.', (), "Stream"),
    ("Render", "Is it worth it? Render — managed hosting.", (), "Render"),
    ("Linear", "Linear is fine for most teams.", (), None),
    ("Square", "We tried Stripe. Square is a payments provider too.", ("Stripe",), "Square"),
    ("Render", "RENDER IS DOWN", (), None),
    ("Render", "Like Render, Fly runs containers.", (), "Render"),
]


@pytest.mark.parametrize(("term", "text", "co_terms", "expected"), PARITY)
def test_text_match_proper_name_parity_with_reference(term, text, co_terms, expected):
    hits = _name_hits(term, text, co_terms)
    assert (hits[0] if hits else None) == expected


def test_text_match_proper_name_counts_every_named_occurrence_and_only_those():
    text = "Render is slow. Render vs Fly? We left Render. render it again."
    assert [h for h in _name_hits("Render", text)] == ["Render", "Render"]
    # The same term with no mode matches all four.
    assert len(TermMatcher([("Render", None)]).scan(text)[0]) == 4


async def test_term_scan_blind_panel_question_everyday_brand_is_not_a_leak():
    """Blind panel questions: the never-say list's brand 'Render' is an everyday word."""
    terms = [{"term": "Render", "class": "brand"}, {"term": "Fly.io", "class": "competitor"}]
    q_ok = "Render times got slow, what should a small studio upgrade first?"
    q_leak = "Rendering in Render is slow — should we move?"
    out = await _run({"items": [q_ok, q_leak], "terms": terms}, {"everyday_words": "auto"})
    assert out["clean_items"] == [q_ok]
    assert out["flagged_items"] == [q_leak]
    assert [(h["term"], h["start"]) for h in out["results"][1]["hits"]] == [("Render", 13)]
    # Without the option the good question is (wrongly) a leak: the default is unchanged.
    out = await _run({"items": [q_ok, q_leak], "terms": terms})
    assert out["clean_items"] == []


async def test_term_scan_auto_marks_only_one_word_dictionary_terms():
    """`auto`: 'Apple' (a dictionary word) becomes proper-name-only; 'Samsung' and the multi-word
    'Apple Music' stay plain, so they match in any case at a sentence start."""
    text = "apple music is on sale. samsung too. Apple pie for dessert."
    out = await _run({"text": text, "terms": ["Apple", "Samsung", "Apple Music"]}, {"everyday_words": "auto"})
    assert sorted(h["term"] for h in out["hits"]) == ["Apple Music", "Samsung"]
    out = await _run({"text": text, "terms": ["Apple", "Samsung", "Apple Music"]}, {"everyday_words": "none"})
    assert sorted(h["term"] for h in out["hits"]) == ["Apple", "Apple", "Apple Music", "Samsung"]


async def test_term_scan_per_term_any_overrides_auto():
    text = "Apple pie for dessert."
    out = await _run({"text": text, "terms": [{"term": "Apple", "match": "any"}]}, {"everyday_words": "auto"})
    assert [h["matched_text"] for h in out["hits"]] == ["Apple"]


async def test_term_scan_brand_neutral_copy_with_everyday_word_list():
    """Brand-neutral copywriting: the client's own list of everyday-word brands, text mode."""
    terms = ["Notion", "Coda"]
    copy = "Notion has crossed my mind, but the notion is simple."
    out = await _run({"text": copy, "terms": terms}, {"everyday_words": ["notion"]})
    assert out["clean"] is True
    named = "We compared Notion and Coda."
    out = await _run({"text": named, "terms": terms}, {"everyday_words": ["notion"]})
    assert [(h["term"], h["start"]) for h in out["hits"]] == [("Notion", 12), ("Coda", 23)]
    # Another listed name in the same text is the second signal a verb cue needs (rule 3d).
    out = await _run({"text": "Notion has crossed my mind. Coda too.", "terms": terms}, {"everyday_words": ["notion"]})
    assert [h["term"] for h in out["hits"]] == ["Notion", "Coda"]


async def test_term_scan_unbranded_keyword_research_per_term_mode():
    """Unbranded keyword research: drop keywords that name a brand; per-term `match`."""
    keywords = ["apple pie recipe", "best Apple laptop", "Apple: is it worth it", "linear algebra help"]
    terms = [{"term": "Apple", "match": "proper_name_only"}, {"term": "Linear", "match": "proper_name_only"}]
    out = await _run({"items": keywords, "terms": terms})
    assert out["clean_items"] == ["apple pie recipe", "linear algebra help"]
    assert out["flagged_items"] == ["best Apple laptop", "Apple: is it worth it"]
