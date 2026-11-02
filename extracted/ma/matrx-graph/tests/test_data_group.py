"""``data.group`` — put a list's items into groups, run through the real scheduler.

Every test compiles a one-step graph, so the config is validated the way a saved
workflow's is and the output is what a downstream edge would receive. Covers each
way of joining (key, shared values, word overlap, decisions by id), joins that
chain (A~C, C~B ⇒ A, B, C), several ways at once, keeping a prior group's key,
the empty list, a single item, and a lead that does not depend on input order.
"""

from __future__ import annotations

import itertools
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


def _graph(config: dict[str, Any], inputs: dict[str, Any]):
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "g",
                    "type": "data.group",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    return registry, compile_graph(defn, registry=registry)


async def _run(inputs: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    registry, graph = _graph(config, inputs)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-group", inputs=inputs)
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["g"]


def _member_ids(out: dict[str, Any]) -> list[list[Any]]:
    return [group["member_ids"] for group in out["groups"]]


async def test_by_key_groups_equal_values_and_a_missing_key_stands_alone():
    items = [
        {"id": "a", "domain": "x.com"},
        {"id": "b", "domain": "y.com"},
        {"id": "c", "domain": "x.com"},
        {"id": "d"},
        {"id": "e"},
    ]
    out = await _run({"items": items}, {"key": "domain"})
    # Groups are ordered by their first member's position; a missing key is a hole,
    # never "equal to every other hole".
    assert _member_ids(out) == [["a", "c"], ["b"], ["d"], ["e"]]
    assert out["group_count"] == 4
    assert out["item_count"] == 5
    assert out["ungrouped"] == 3
    assert out["groups"][0]["matched_by"] == ["key"]
    assert out["groups"][0]["count"] == 2
    assert out["item_keys"] == ["a", "b", "a", "d", "e"]


async def test_shared_values_join_transitively():
    # a and b share nothing; c shares 2 with a and 3 with b, so all three are one group.
    items = [
        {"id": "a", "keys": [1, 2]},
        {"id": "b", "keys": [3]},
        {"id": "c", "keys": [2, 3]},
        {"id": "d", "keys": [9]},
        {"id": "e", "keys": []},
    ]
    out = await _run({"items": items}, {"shared_values": ["keys"], "union": ["keys"]})
    assert _member_ids(out) == [["a", "b", "c"], ["d"], ["e"]]
    assert out["groups"][0]["union"] == {"keys": [1, 2, 3]}
    assert out["groups"][0]["matched_by"] == ["shared_values"]


async def test_shared_values_read_nested_lists_with_the_accessor_grammar():
    items = [
        {"id": "a", "articles": [{"u": "p/1"}, {"u": "p/2"}]},
        {"id": "b", "articles": [{"u": "p/2"}]},
        {"id": "c", "articles": [{"u": "p/3"}]},
    ]
    out = await _run({"items": items}, {"shared_values": ["articles[].u"], "union": ["articles[].u"]})
    assert _member_ids(out) == [["a", "b"], ["c"]]
    assert out["groups"][0]["union"] == {"articles[].u": ["p/1", "p/2"]}


async def test_token_overlap_needs_the_ratio_and_the_minimum_shared_words():
    items = [
        {"id": "a", "title": "Acme Robotics raises $40M Series B"},
        {"id": "b", "title": "ACME ROBOTICS RAISES new funding"},
        # Shares only stop words with a ("the", "of", "and") — never a group.
        {"id": "c", "title": "The end of the road and the start"},
        # Shares one real word with a ("acme") — below min_shared 2.
        {"id": "d", "title": "Acme opens office"},
    ]
    config = {"token_overlap": {"fields": ["title"], "threshold": 0.6, "min_shared": 2}}
    out = await _run({"items": items}, config)
    assert _member_ids(out) == [["a", "b"], ["c"], ["d"]]
    assert out["groups"][0]["matched_by"] == ["token_overlap"]

    # A stricter ratio separates the same pair: 3 shared of b's 5 words = 0.6.
    strict = await _run({"items": items}, {"token_overlap": {"fields": ["title"], "threshold": 0.8}})
    assert _member_ids(strict) == [["a"], ["b"], ["c"], ["d"]]


async def test_token_overlap_first_member_compares_only_with_the_group_seed():
    # b~a and c~b, but c shares under 2 words with a.
    items = [
        {"id": "a", "title": "alpha beta gamma"},
        {"id": "b", "title": "beta gamma delta"},
        {"id": "c", "title": "gamma delta epsilon"},
    ]
    chained = await _run({"items": items}, {"token_overlap": {"fields": ["title"], "threshold": 0.6}})
    assert _member_ids(chained) == [["a", "b", "c"]]
    seeded = await _run(
        {"items": items},
        {"token_overlap": {"fields": ["title"], "threshold": 0.6, "compare": "first_member"}},
    )
    assert _member_ids(seeded) == [["a", "b"], ["c"]]


async def test_ids_from_applies_decisions_by_id_and_counts_unknown_ids():
    items = [{"id": f"c{n}", "text": f"claim {n}"} for n in range(1, 6)]
    decisions = [
        {"lead_id": "c3", "member_ids": ["c1", "zz"]},
        {"lead_id": "c4", "member_ids": ["c5"]},
        {"lead_id": "nope", "member_ids": []},
    ]
    out = await _run({"items": items, "decisions": decisions}, {"ids_from": {}})
    assert _member_ids(out) == [["c1", "c3"], ["c2"], ["c4", "c5"]]
    # The decision's lead leads when no lead_by is set.
    assert [g["lead"]["id"] for g in out["groups"]] == ["c3", "c2", "c4"]
    assert [g["key"] for g in out["groups"]] == ["c3", "c2", "c4"]
    assert out["unknown_ids"] == ["nope", "zz"]
    assert out["groups"][0]["matched_by"] == ["ids_from"]


async def test_modes_combine_as_any_match():
    items = [
        {"id": "a", "domain": "x.com", "keys": ["k1"], "title": "one two three"},
        {"id": "b", "domain": "y.com", "keys": ["k1"], "title": "zzz"},
        {"id": "c", "domain": "z.com", "keys": [], "title": "one two four"},
        {"id": "d", "domain": "x.com", "keys": [], "title": "unrelated"},
        {"id": "e", "domain": "q.com", "keys": [], "title": "alone here"},
    ]
    config = {
        "key": "domain",
        "shared_values": ["keys"],
        "token_overlap": {"fields": ["title"], "threshold": 0.6},
    }
    out = await _run({"items": items}, config)
    assert _member_ids(out) == [["a", "b", "c", "d"], ["e"]]
    assert out["groups"][0]["matched_by"] == ["key", "shared_values", "token_overlap"]
    assert out["groups"][1]["matched_by"] == []


async def test_existing_groups_keep_their_key_across_runs():
    items = [
        {"id": "a", "url_keys": ["u1"], "title": "Mayor resigns after audit"},
        {"id": "b", "url_keys": ["u9"], "title": "Rocket launch delayed by weather again"},
        {"id": "c", "url_keys": ["u5"], "title": "Totally new thing"},
    ]
    existing = [
        {"story_key": "S-old-2", "member_url_keys": ["u2"], "title": "Rocket launch delayed by weather"},
        {"story_key": "S-old-1", "member_url_keys": ["u1", "u3"], "title": "something else"},
    ]
    config = {
        "shared_values": ["url_keys"],
        "token_overlap": {"fields": ["title"], "threshold": 0.6},
        "existing": {"key_path": "story_key", "values_path": "member_url_keys", "text_paths": ["title"]},
    }
    out = await _run({"items": items, "existing": existing}, config)
    assert [g["key"] for g in out["groups"]] == ["S-old-1", "S-old-2", "c"]
    assert [g["matched_existing"] for g in out["groups"]] == ["S-old-1", "S-old-2", None]
    assert out["matched_existing_count"] == 2
    assert out["item_keys"] == ["S-old-1", "S-old-2", "c"]


async def test_two_groups_matching_one_existing_group_become_one():
    items = [
        {"id": "a", "url_keys": ["u1"]},
        {"id": "b", "url_keys": ["u2"]},
    ]
    existing = [{"key": "S", "values": ["u1", "u2"]}]
    out = await _run(
        {"items": items, "existing": existing},
        {"shared_values": ["url_keys"], "existing": {"values_path": "values"}},
    )
    assert _member_ids(out) == [["a", "b"]]
    assert out["groups"][0]["key"] == "S"
    assert "existing" in out["groups"][0]["matched_by"]


async def test_empty_list():
    out = await _run({"items": []}, {"key": "id"})
    assert out["groups"] == []
    assert (out["group_count"], out["item_count"], out["ungrouped"]) == (0, 0, 0)
    assert out["item_keys"] == []


async def test_single_item():
    out = await _run({"items": [{"id": "only", "v": 1}]}, {"key": "v", "union": ["v"]})
    assert out["group_count"] == 1
    group = out["groups"][0]
    assert (group["key"], group["count"], group["lead"]) == ("only", 1, {"id": "only", "v": 1})
    assert group["union"] == {"v": [1]}
    assert out["ungrouped"] == 1


async def test_lead_is_deterministic_whatever_the_input_order():
    base = [
        {"id": "s3", "url_keys": ["k"], "queue_priority": 2, "size": 5},
        {"id": "s1", "url_keys": ["k"], "queue_priority": 2, "size": 5},
        {"id": "s2", "url_keys": ["k"], "queue_priority": 2, "size": 9},
        {"id": "s0", "url_keys": ["k"], "queue_priority": 1, "size": 99},
        {"id": "s4", "url_keys": ["k"]},
    ]
    config = {
        "shared_values": ["url_keys"],
        "lead_by": [
            {"path": "queue_priority", "order": "desc"},
            {"path": "size", "order": "desc"},
            {"path": "id", "order": "asc"},
        ],
    }
    leads = set()
    for order in itertools.permutations(base):
        out = await _run({"items": list(order)}, config)
        assert out["group_count"] == 1
        leads.add((out["groups"][0]["lead"]["id"], out["groups"][0]["key"]))
    assert leads == {("s2", "s2")}

    # Ties beyond every sort path fall to the id path ascending.
    tie = [{"id": "b", "k": 1}, {"id": "a", "k": 1}]
    out = await _run({"items": tie}, {"key": "k", "lead_by": [{"path": "id", "order": "asc"}]})
    assert out["groups"][0]["lead"]["id"] == "a"


async def test_a_config_with_no_way_to_join_is_refused_at_compile():
    with pytest.raises(Exception) as caught:
        _graph({}, {"items": []})
    assert "key" in str(caught.value) and "token_overlap" in str(caught.value)


# ---------------------------------------------------------------------------
# ids_from as a decision applier (brand discovery's "say the same thing" merge)
# ---------------------------------------------------------------------------

_CLAIMS = [
    {"id": "c1", "text": "We build solar roofs for homes"},
    {"id": "c2", "text": "Solar roofs for homes are what we build, with 25 year warranty"},
    {"id": "c3", "text": "Family owned since 1998"},
    {"id": "c4", "text": "Solar roofs built for homes"},
    {"id": "c5", "text": "Free estimates"},
]


async def test_ids_from_paths_are_settable_and_a_lead_absent_from_its_ids_still_joins():
    decisions = [{"lead": "c2", "ids": ["c4"]}]
    out = await _run(
        {"items": _CLAIMS, "decisions": decisions},
        {"ids_from": {"lead_path": "lead", "ids_path": "ids"}},
    )
    assert _member_ids(out) == [["c1"], ["c2", "c4"], ["c3"], ["c5"]]
    assert out["groups"][1]["lead"]["id"] == "c2"
    assert out["dropped"] == {
        "unknown_id": 0, "id_in_two_groups": 0, "group_lead_missing": 0, "group_not_an_object": 0,
        "duplicate_item_id": 0,
    }


async def test_ids_from_is_not_transitive_and_counts_every_drop_by_reason():
    decisions = [
        {"lead_id": "c1", "member_ids": ["c2"]},
        # c2 is already in c1's group: dropped from this one, never chaining the two.
        {"lead_id": "c3", "member_ids": ["c2", "c4", "ghost"]},
        {"member_ids": ["c5"]},  # no lead
        "c5",  # not an object
    ]
    out = await _run({"items": _CLAIMS, "decisions": decisions}, {"ids_from": {}})
    assert _member_ids(out) == [["c1", "c2"], ["c3", "c4"], ["c5"]]
    assert out["dropped"] == {
        "unknown_id": 1, "id_in_two_groups": 1, "group_lead_missing": 1, "group_not_an_object": 1,
        "duplicate_item_id": 0,
    }
    assert out["unknown_ids"] == ["ghost"]


async def test_lead_by_longest_overrides_the_named_lead_and_counts_it():
    decisions = [{"lead_id": "c1", "member_ids": ["c2", "c4"]}, {"lead_id": "c3", "member_ids": []}]
    named = await _run({"items": _CLAIMS, "decisions": decisions}, {"ids_from": {}})
    assert named["groups"][0]["lead"]["id"] == "c1"
    assert named["leads_changed"] == 0

    out = await _run(
        {"items": _CLAIMS, "decisions": decisions},
        {"ids_from": {}, "lead_by": ["longest(text)"]},
    )
    assert out["groups"][0]["lead"]["id"] == "c2"
    assert out["groups"][0]["key"] == "c2"
    assert out["leads_changed"] == 1  # c3's group of one kept its named lead


async def test_min_overlap_splits_a_member_too_unlike_its_lead():
    decisions = [{"lead_id": "c1", "member_ids": ["c4", "c3"]}]
    config = {"ids_from": {}, "min_overlap": {"threshold": 0.3, "fields": ["text"]}}
    out = await _run({"items": _CLAIMS, "decisions": decisions}, config)
    # c4 shares solar/roofs/for/homes with c1 (4 of 7 distinct 3+ letter words); c3 shares none.
    assert _member_ids(out) == [["c1", "c4"], ["c2"], ["c3"], ["c5"]]
    assert out["split_from_groups"] == 1
    assert out["item_keys"][2] == "c3"

    off = await _run({"items": _CLAIMS, "decisions": decisions}, {"ids_from": {}})
    assert _member_ids(off)[0] == ["c1", "c3", "c4"]
    assert off["split_from_groups"] == 0


async def test_evidence_field_puts_the_other_members_on_the_lead():
    decisions = [{"lead_id": "c1", "member_ids": ["c2", "c4"]}]
    out = await _run(
        {"items": _CLAIMS, "decisions": decisions},
        {"ids_from": {}, "evidence_field": "evidence"},
    )
    lead = out["groups"][0]["lead"]
    assert lead["id"] == "c1" and lead["text"] == _CLAIMS[0]["text"]
    assert lead["evidence"] == [_CLAIMS[1], _CLAIMS[3]]
    # Members stay as they came in; only the lead copy carries the evidence.
    assert "evidence" not in out["groups"][0]["members"][0]
    assert out["groups"][1]["lead"]["evidence"] == []


async def test_order_puts_named_groups_first_and_keeps_the_rest_in_input_order():
    decisions = [{"lead_id": "c1", "member_ids": ["c4"]}]
    out = await _run(
        {"items": _CLAIMS, "decisions": decisions, "order": ["c5", "c4", "c1", "nobody"]},
        {"ids_from": {}},
    )
    # c4 stands for its lead's group; c1 repeats it; unnamed c2, c3 follow in input order.
    assert _member_ids(out) == [["c5"], ["c1", "c4"], ["c2"], ["c3"]]
    assert out["unknown_ids"] == ["nobody"]


# ---------------------------------------------------------------------------
# keys are unique, duplicate ids are counted, "" is a hole (review 2026-10-27)
# ---------------------------------------------------------------------------


def _keys(out: dict[str, Any]) -> list[str]:
    return [g["key"] for g in out["groups"]]


async def test_unjoined_duplicate_ids_get_unique_keys():
    items = [{"id": "a", "k": 1}, {"id": "a", "k": 2}, {"id": "b", "k": 3}]
    out = await _run({"items": items}, {"key": "k"})
    assert _keys(out) == ["a", "a~2", "b"]
    assert out["key_collisions"] == 1
    assert out["item_keys"] == ["a", "a~2", "b"]


async def test_an_existing_key_wins_over_a_lead_id_that_collides_with_it():
    items = [{"id": "y", "u": ["u1"]}, {"id": "x", "u": ["u2"]}]
    existing = [{"key": "y", "values": ["u2"]}]
    out = await _run(
        {"items": items, "existing": existing},
        {"shared_values": ["u"], "existing": {"values_path": "values"}},
    )
    # x's group continues earlier group "y"; the item whose own id is y gets a suffix.
    assert _keys(out) == ["y~2", "y"]
    assert [g["matched_existing"] for g in out["groups"]] == [None, "y"]
    assert out["key_collisions"] == 1


async def test_a_lead_without_an_id_never_takes_a_real_id():
    items = [{"k": 1}, {"id": "group-1", "k": 2}]
    out = await _run({"items": items}, {"key": "k"})
    assert _keys(out) == ["group-1~2", "group-1"]
    assert out["key_collisions"] == 1
    assert len(set(_keys(out))) == 2


async def test_duplicate_item_ids_are_counted_and_the_later_items_stand_alone():
    items = [{"id": "c1"}, {"id": "c2"}, {"id": "c1", "note": "later copy"}]
    decisions = [{"lead_id": "c2", "member_ids": ["c1"]}]
    out = await _run({"items": items, "decisions": decisions}, {"ids_from": {}})
    # A decision naming c1 means the FIRST c1; the later copy is its own group, in place.
    assert _member_ids(out) == [["c1", "c2"], ["c1"]]
    assert out["groups"][1]["members"] == [{"id": "c1", "note": "later copy"}]
    assert out["dropped"]["duplicate_item_id"] == 1
    assert _keys(out) == ["c2", "c1"]


async def test_ids_are_compared_as_text_so_1_and_quoted_1_are_one_id():
    items = [{"id": 1}, {"id": "2"}]
    decisions = [{"lead_id": "1", "member_ids": [2]}]
    out = await _run({"items": items, "decisions": decisions}, {"ids_from": {}})
    assert _member_ids(out) == [[1, "2"]]
    assert out["dropped"]["unknown_id"] == 0


async def test_an_empty_string_key_is_a_hole_and_joins_nothing():
    items = [{"id": "a", "k": ""}, {"id": "b", "k": ""}, {"id": "c", "k": "  "}]
    out = await _run({"items": items}, {"key": "k"})
    assert _member_ids(out) == [["a"], ["b"], ["c"]]
    # An empty lead sort value sorts last like a missing one.
    out = await _run(
        {"items": [{"id": "a", "k": 1, "p": ""}, {"id": "b", "k": 1, "p": "z"}]},
        {"key": "k", "lead_by": [{"path": "p", "order": "asc"}]},
    )
    assert out["groups"][0]["lead"]["id"] == "b"
