"""``data.dedupe`` similarity/normalize and ``data.limit`` round-robin (2026-10-27).

Breaks these catch:
* dedupe only matched exact keys, so "Fast Delivery " and "fast  delivery", or a
  claim repeated in other words, stayed as separate rows;
* limit only took the head, so one product line / engine / section crowded out
  every other when N was smaller than the list.
Users A: brand claims, testimony re-cuts, news story duplicates, results from two
engines. Users B: offering roles across product lines, news source diversity,
multi-engine results, study-kit questions across sections.
"""

from __future__ import annotations

import pytest

from matrx_graph import RunStatus

from matrx_graph.errors import CompilationError
from tests.test_data_collections import _out, _run


# --------------------------------------------------------------------------- dedupe normalize


async def test_normalize_case_space_makes_one_key():
    items = [{"t": "Fast Delivery ", "n": 1}, {"t": "fast  delivery", "n": 2}, {"t": "Free returns", "n": 3}]
    plain = await _out("data.dedupe", {"items": items}, {"key": "t"})
    assert plain["kept"] == 3
    out = await _out("data.dedupe", {"items": items}, {"key": "t", "normalize": "case_space"})
    assert [i["n"] for i in out["items"]] == [1, 3]


# --------------------------------------------------------------------------- dedupe similar

CLAIMS = [
    {"id": 1, "topic": "ship", "text": "We offer fast free delivery on every order over fifty dollars"},
    {"id": 2, "topic": "ship", "text": "Fast free delivery on every order over fifty dollars, we offer it"},
    {"id": 3, "topic": "pay", "text": "We offer fast free delivery on every order over fifty dollars"},
    {"id": 4, "topic": "ship", "text": "Handmade in Portland by a team of six"},
]


async def test_similar_jaccard_within_topic():
    out = await _out(
        "data.dedupe",
        {"items": CLAIMS},
        {"similar": {"text": "text", "measure": "jaccard", "threshold": 0.85, "within": "topic"}},
    )
    # 2 repeats 1 (same topic); 3 has the same words but another topic -> kept.
    assert [i["id"] for i in out["items"]] == [1, 3, 4]
    assert out["dropped"] == 1


async def test_similar_without_within_compares_everything():
    out = await _out(
        "data.dedupe", {"items": CLAIMS}, {"similar": {"text": "text", "threshold": 0.85}}
    )
    assert [i["id"] for i in out["items"]] == [1, 4]


async def test_containment_catches_a_recut_that_jaccard_misses():
    recut = [
        {"id": "full", "q": "Our guides know the tides so well that every paddler returns relaxed and happy after the long morning tour"},
        {"id": "cut", "q": "every paddler returns relaxed and happy after the long morning tour"},
    ]
    jac = await _out("data.dedupe", {"items": recut}, {"similar": {"text": "q", "measure": "jaccard", "threshold": 0.85}})
    assert jac["kept"] == 2
    con = await _out("data.dedupe", {"items": recut}, {"similar": {"text": "q", "measure": "containment", "threshold": 0.85}})
    assert [i["id"] for i in con["items"]] == ["full"]


async def test_similar_composes_with_merge_keeps_evidence():
    results = [
        {"title": "Best kayak tours in Tampa Bay for families", "engines": ["brave"], "rank": 3},
        {"title": "Best kayak tours Tampa Bay for families", "engines": ["google"], "rank": 1},
        {"title": "Marina slip rental rates", "engines": ["google"], "rank": 2},
    ]
    out = await _out(
        "data.dedupe",
        {"items": results},
        {
            "similar": {"text": "title", "threshold": 0.8},
            "merge": {"combine_lists": ["engines"], "keep_lowest": ["rank"]},
        },
    )
    assert out["items"][0]["engines"] == ["brave", "google"]
    assert out["items"][0]["rank"] == 1
    assert out["kept"] == 2


async def test_short_texts_only_match_when_identical_and_empty_never_match():
    items = [{"t": "Sale"}, {"t": "sale!"}, {"t": "Sale now"}, {"t": ""}, {"t": ""}, {"x": 1}]
    out = await _out("data.dedupe", {"items": items}, {"similar": {"text": "t", "threshold": 0.5}})
    # "Sale" == "sale!" (same words); "Sale now" has < min_words so is not a near match;
    # empty and missing text are never "the same".
    assert out["kept"] == 5


async def test_key_and_similar_together_is_refused():
    with pytest.raises(CompilationError, match="not both"):
        await _run("data.dedupe", {"items": []}, {"key": "a", "similar": {"text": "t"}})
    with pytest.raises(CompilationError, match="offset or from_end"):
        await _run("data.limit", {"items": []}, {"count": 1, "offset": 1, "round_robin": {"by": "g"}})


# --------------------------------------------------------------------------- limit round robin

LINES = (
    [{"id": f"a{i}", "line": "kayaks", "score": 10 - i} for i in range(5)]
    + [{"id": f"b{i}", "line": "paddles", "score": 5 - i} for i in range(2)]
    + [{"id": "c0", "line": "vests", "score": 1}]
)


async def test_plain_limit_is_crowded_by_the_big_group():
    out = await _out("data.limit", {"items": LINES}, {"count": 4})
    assert {i["line"] for i in out["items"]} == {"kayaks"}


async def test_round_robin_alternates_groups_largest_first_best_first():
    out = await _out(
        "data.limit",
        {"items": LINES},
        {"count": 5, "round_robin": {"by": "line", "order_by": [{"key": "score", "order": "desc"}]}},
    )
    assert [i["id"] for i in out["items"]] == ["a0", "b0", "c0", "a1", "b1"]
    assert out["kept"] == 5 and out["dropped"] == 3


async def test_round_robin_best_first_inside_group_and_original_order_output():
    shuffled = [LINES[3], LINES[0], LINES[5], LINES[7], LINES[1]]  # a3 a0 b0 c0 a1
    out = await _out(
        "data.limit",
        {"items": shuffled},
        {
            "count": 3,
            "round_robin": {
                "by": "line",
                "order_by": [{"key": "score", "order": "desc"}],
                "output_order": "original",
            },
        },
    )
    assert [i["id"] for i in out["items"]] == ["a0", "b0", "c0"]


async def test_round_robin_group_order_listed_and_first_seen():
    out = await _out(
        "data.limit",
        {"items": LINES},
        {"count": 2, "round_robin": {"by": "line", "group_order": "listed", "groups": ["vests", "paddles"]}},
    )
    assert [i["id"] for i in out["items"]] == ["c0", "b0"]
    out = await _out(
        "data.limit",
        {"items": LINES},
        {"count": 2, "round_robin": {"by": "line", "group_order": "first_seen"}},
    )
    assert [i["id"] for i in out["items"]] == ["a0", "b0"]


async def test_round_robin_items_without_the_group_field_share_one_group():
    items = [{"id": 1, "g": "x"}, {"id": 2}, {"id": 3}, {"id": 4, "g": "x"}]
    out = await _out("data.limit", {"items": items}, {"count": 2, "round_robin": {"by": "g"}})
    assert {i["id"] for i in out["items"]} == {1, 2}


async def test_round_robin_under_the_count_keeps_everything():
    out = await _out("data.limit", {"items": LINES}, {"count": 50, "round_robin": {"by": "line"}})
    assert out["kept"] == 8


# --------------------------------------------------------------------------- review fixes


async def test_trailing_punctuation_and_apostrophes_do_not_split_words():
    items = [
        {"t": "Free delivery. Don't pay shipping, ever!"},
        {"t": "free delivery dont... don't pay shipping ever"},
        {"t": "Free delivery and don't pay shipping ever"},
    ]
    out = await _out("data.dedupe", {"items": items}, {"similar": {"text": "t", "threshold": 0.99}})
    # 1 and 3 have identical word sets once punctuation is stripped; 2 has an extra "dont".
    assert [i["t"] for i in out["items"]] == [items[0]["t"], items[1]["t"]]


async def test_round_robin_refuses_a_group_named_twice():
    with pytest.raises(CompilationError, match="more than once"):
        await _run(
            "data.limit",
            {"items": []},
            {"count": 2, "round_robin": {"by": "g", "group_order": "listed", "groups": ["b", "b"]}},
        )


async def test_round_robin_listed_matches_numbers_and_null_joins_the_missing_group():
    items = [{"id": "a", "g": 1}, {"id": "b", "g": 1}, {"id": "c", "g": 2}, {"id": "n", "g": None}, {"id": "m"}]
    out = await _out(
        "data.limit",
        {"items": items},
        {"count": 3, "round_robin": {"by": "g", "group_order": "listed", "groups": ["2", "1"]}},
    )
    assert [i["id"] for i in out["items"]] == ["c", "a", "n"]  # 2, 1, then the unlisted (null+hole) group
    out = await _out("data.limit", {"items": items}, {"count": 5, "round_robin": {"by": "g", "group_order": "first_seen"}})
    assert [i["id"] for i in out["items"]] == ["a", "c", "n", "b", "m"]


async def test_similar_over_the_cap_fails_with_plain_words():
    items = [{"t": f"claim number {i} about kayaks"} for i in range(6)]
    result = await _run("data.dedupe", {"items": items}, {"similar": {"text": "t", "max_items": 5}})
    assert result.status is not RunStatus.COMPLETED
    assert "capped at 5 items" in str(result.error)
    ok = await _out("data.dedupe", {"items": items[:5]}, {"similar": {"text": "t", "max_items": 5}})
    assert ok["kept"] >= 1
