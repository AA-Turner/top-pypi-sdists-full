"""``text.similarity`` — how close a text is to each of a list, run through the real scheduler.

Words come from ``matrx_graph.text_match.words``. The expected scores are the matrx_seo AI-visibility reference values (T7 ``similarity_pairs``
token Jaccard + char-3 cosine, ``keep_observed_wording``'s max(Jaccard, containment)),
reproduced here as numbers, never imported. Jaccard / containment are hand-countable:

- "how do I file a tax return online" vs "file my tax return online": 8 and 5 words, 4
  shared, 9 in the union -> Jaccard 4/9 = 0.4444, containment 4/5 = 0.8.
- "plumber near me open now" vs "emergency plumber near me": 5 and 4, 3 shared, 6 in the
  union -> 0.5, containment 3/4 = 0.75.
- "best running shoes" vs "best running shoe": 3 and 3, 2 shared, 4 in the union -> 0.5,
  containment 2/3 = 0.6667.

Rule 3 users exercised below: question wording vs observed buyer wording (max of both),
near-duplicate quiz questions (pairs), and a headline against the stories already filed.
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
                    "type": "text.similarity",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config or {}, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-similarity", inputs=inputs)
    if ok:
        assert result.status is RunStatus.COMPLETED, result.error
        return result.last_outputs["n"]
    assert result.status is not RunStatus.COMPLETED
    return result


_EXAMPLES = [
    ("how do I file a tax return online", "file my tax return online", 0.4444, 0.8, 0.7063),
    ("plumber near me open now", "emergency plumber near me", 0.5, 0.75, 0.5883),
    ("best running shoes", "best running shoe", 0.5, 0.6667, 0.9193),
]


def test_similarity_is_registered_as_pure():
    spec = _registry().get("text.similarity").spec
    assert spec.determinism.value == "pure"
    assert spec.display_name == "Compare Wording"


@pytest.mark.parametrize(("text", "candidate", "jaccard", "containment", "char3"), _EXAMPLES)
async def test_similarity_scores_match_the_reference(text, candidate, jaccard, containment, char3):
    async def score(method: str) -> float:
        out = await _run({"text": text, "candidates": [candidate]}, {"method": method})
        return out["best"]["score"]

    assert await score("jaccard") == jaccard
    assert await score("containment") == containment
    assert await score("max_jaccard_containment") == max(jaccard, containment)
    assert await score("char3_cosine") == char3


async def test_similarity_folds_case_and_width_before_comparing():
    out = await _run({"text": "Café Olé menu", "candidates": ["CAFÉ OLÉ"]}, {"method": "char3_cosine"})
    assert out["best"]["score"] == 0.8018


async def test_similarity_best_and_threshold_matches_sorted_by_score():
    candidates = ["emergency plumber near me", "pizza delivery", {"q": "plumber near me open now"}]
    out = await _run(
        {"text": "plumber near me open now", "candidates": candidates},
        {"method": "jaccard", "threshold": 0.4, "candidate_path": "q"},
    )
    # A plain-string candidate is its own text even when candidate_path is set for objects.
    assert out["best"] == {"index": 2, "score": 1.0, "candidate": {"q": "plumber near me open now"}}
    assert [(m["index"], m["score"]) for m in out["matches"]] == [(2, 1.0), (0, 0.5)]


async def test_similarity_no_threshold_ranks_every_candidate():
    out = await _run({"text": "best running shoes", "candidates": ["pizza", "best running shoe"]})
    assert [m["index"] for m in out["matches"]] == [1, 0]


async def test_similarity_empty_candidates_has_no_best():
    out = await _run({"text": "anything", "candidates": []})
    assert out["best"] is None and out["matches"] == []


async def test_similarity_items_mode_and_pairs_nominate_near_duplicates():
    questions = [
        {"id": "a", "q": "What is the capital of France?"},
        {"id": "b", "q": "What is the capital city of France?"},
        {"id": "c", "q": "Name a primary color."},
    ]
    out = await _run(
        {"items": questions, "candidates": ["capital of France"]},
        {"text_path": "q", "method": "containment", "threshold": 0.9, "pairs": True},
    )
    assert [r["best"] and r["best"]["score"] for r in out["results"]] == [1.0, 1.0, None]
    assert [r["matches"] != [] for r in out["results"]] == [True, True, False]
    # a vs b: 6 and 7 words, 6 shared -> containment (larger direction) 6/6 = 1.0.
    assert out["pairs"] == [
        {"a": 0, "b": 1, "score": 1.0, "scores": {"containment": 1.0}, "nominated_by": ["containment"]}
    ]
    # Pairs never remove anything: the items are untouched and all three are reported.
    assert len(out["results"]) == 3


async def test_similarity_pairs_needs_items_and_threshold():
    result = await _run({"text": "x", "candidates": []}, {"pairs": True, "threshold": 0.5}, ok=False)
    assert "pairs" in (result.error or "")
    result = await _run({"items": ["x", "y"]}, {"pairs": True}, ok=False)
    assert "threshold" in (result.error or "")
