"""``text.term_scan`` — does a text contain any term of a list, run through the real scheduler.

Behavior matches the contamination scan in matrx_seo's AI-visibility design (T4: NFKC +
casefold, whole-word token sequences; fuzzy near misses at min token length 7 / ratio 0.86)
without importing it. Rule 3 users exercised below: a brand never-say list over a blind
brief (items mode + classes), a writing style guide's banned words (text mode, exact), and a
privileged-term screen over documents (folded + fuzzy review).
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run(inputs: dict[str, Any], config: dict[str, Any] | None = None, *, ok: bool = True):
    registry = _registry()
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
    result = await scheduler.run(run_id="t-term-scan", inputs=inputs)
    if ok:
        assert result.status is RunStatus.COMPLETED, result.error
        return result.last_outputs["n"]
    assert result.status is not RunStatus.COMPLETED
    return result


def test_term_scan_is_registered_as_pure():
    spec = _registry().get("text.term_scan").spec
    assert spec.determinism.value == "pure"
    assert spec.display_name == "Find Terms"


async def test_term_scan_folded_matches_cafe_in_any_case_and_width():
    text = "Lunch at CAFÉ Olé, then the café again."
    out = await _run({"text": text, "terms": ["Café Olé", "café"]}, {"match": "folded"})
    found = [(h["term"], text[h["start"] : h["end"]]) for h in out["hits"]]
    assert found == [("Café Olé", "CAFÉ Olé"), ("café", "CAFÉ"), ("café", "café")]
    assert out["clean"] is False
    assert out["hit_count"] == 3
    # Fullwidth letters fold (NFKC) to the plain term.
    out = await _run({"text": "Visit ＣＡＦＥ today", "terms": ["cafe"]})
    assert [h["matched_text"] for h in out["hits"]] == ["ＣＡＦＥ"]


async def test_term_scan_respects_word_boundaries():
    out = await _run({"text": "The party was art-free.", "terms": ["art"]})
    # "art" inside "party" is not a hit; the standalone "art" is.
    assert [(h["start"], h["end"]) for h in out["hits"]] == [(14, 17)]
    out = await _run({"text": "a party for everyone", "terms": ["art"]})
    assert out["hits"] == [] and out["clean"] is True


async def test_term_scan_exact_is_case_sensitive_and_whole_word():
    terms = ["utilize", "Synergy"]
    out = await _run({"text": "We utilize synergy; Synergy utilizes us.", "terms": terms}, {"match": "exact"})
    assert [(h["term"], h["start"]) for h in out["hits"]] == [("utilize", 3), ("Synergy", 20)]


async def test_term_scan_fuzzy_near_misses_are_review_never_hits():
    out = await _run(
        {"text": "The marketplce opens Monday.", "terms": ["Marketplace"]},
        {"fuzzy": {"enabled": True}},
    )
    assert out["hits"] == []
    assert out["clean"] is True
    assert out["needs_review"] is True
    assert [(f["term"], f["matched_text"]) for f in out["fuzzy"]] == [("Marketplace", "marketplce")]
    assert out["fuzzy"][0]["ratio"] == 0.9524
    # Off by default: the same text reports nothing to review.
    out = await _run({"text": "The marketplce opens Monday.", "terms": ["Marketplace"]})
    assert out["fuzzy"] == [] and out["needs_review"] is False
    # Short terms never fuzz (min token length 7): "Acme" vs "Acne".
    out = await _run({"text": "Acne cream", "terms": ["Acme"]}, {"fuzzy": {"enabled": True}})
    assert out["fuzzy"] == []


async def test_term_scan_empty_terms_and_empty_text_are_clean():
    out = await _run({"text": "Anything at all", "terms": []})
    assert out["clean"] is True and out["hits"] == [] and out["term_count"] == 0
    out = await _run({"text": "", "terms": ["Northwind"]})
    assert out["clean"] is True and out["hits"] == []


async def test_term_scan_items_mode_splits_clean_and_flagged_with_classes():
    items = [
        {"id": "q1", "brief": {"text": "Which dental clinic is open late?"}},
        {"id": "q2", "brief": {"text": "Is Riverbend Dental good for kids?"}},
        {"id": "q3", "brief": {"text": "Compare Northwind Smiles prices"}},
    ]
    terms = [
        {"term": "Riverbend Dental", "class": "brands"},
        {"term": "Northwind Smiles", "class": "competitor_terms"},
    ]
    out = await _run({"items": items, "terms": terms}, {"text_path": "brief.text"})
    assert [i["id"] for i in out["clean_items"]] == ["q1"]
    assert [i["id"] for i in out["flagged_items"]] == ["q2", "q3"]
    assert out["results"][1]["hits"][0]["term_class"] == "brands"
    assert out["flagged_count"] == 2 and out["clean"] is False
    # The classes filter keeps only the named term classes.
    out = await _run({"items": items, "terms": terms}, {"text_path": "brief.text", "classes": ["brands"]})
    assert [i["id"] for i in out["flagged_items"]] == ["q2"]


async def test_term_scan_refuses_text_and_items_together():
    result = await _run({"text": "x", "items": ["y"], "terms": ["x"]}, ok=False)
    assert "text" in (result.error or "") and "items" in (result.error or "")
