"""``data.join`` (2026-10-27): match the items of one list to another by key.

The break this catches: answers come back about short ids and must land on the
right candidate — a position zip or a wrong key puts one candidate's decision on
another, and an answer about an id never sent must be reported, not lost.
Users: Smart Add "Is this a match?", news monitor (triage rows → stories),
CRM enrichment rows → contacts.
"""

from __future__ import annotations

from matrx_graph import RunStatus

from tests.test_data_collections import _out, _run

CANDIDATES = [
    {"id": "c1", "type": "account", "value": "instagram:harborwatch"},
    {"id": "c2", "type": "website", "value": "harborwatch.org"},
    {"id": "c3", "type": "account", "value": "x:harbor_watch"},
]
# answers out of order, one unknown id, one id answered twice
ANSWERS = [
    {"id": "c3", "choice": "not_a_match"},
    {"id": "c9", "choice": "match"},
    {"id": "c1", "choice": "match"},
    {"id": "c1", "choice": "unsure"},
]


async def test_join_nests_each_items_match_by_key_and_reports_unmatched_on_both_sides():
    out = await _out("data.join", {"items": CANDIDATES, "other": ANSWERS}, {"key": "id", "as": "answer"})
    assert [(i["id"], (i["answer"] or {}).get("choice")) for i in out["items"]] == [
        ("c1", "match"),  # first answer for c1 wins by default
        ("c2", None),  # kept, no answer
        ("c3", "not_a_match"),
    ]
    assert out["matched"] == 2
    assert out["unmatched"] == 1
    assert out["unmatched_indexes"] == [1]
    assert out["other_unmatched"] == [{"id": "c9", "choice": "match"}]


async def test_join_merge_mode_many_last_and_dropping_unmatched():
    out = await _out(
        "data.join",
        {"items": CANDIDATES, "other": ANSWERS},
        {"key": "id", "mode": "merge", "many": "last", "keep_unmatched": False},
    )
    assert out["items"] == [
        {"id": "c1", "type": "account", "value": "instagram:harborwatch", "choice": "unsure"},
        {"id": "c3", "type": "account", "value": "x:harbor_watch", "choice": "not_a_match"},
    ]


async def test_join_many_all_other_key_and_case_space_normalize():
    photos = [{"found_on": "Instagram:HarborWatch ", "url": "https://img.example.com/a.png"}, {"url": "https://img.example.com/b.png"}]
    decisions = [
        {"account": {"key": "instagram:harborwatch"}, "label": "match"},
        {"account": {"key": "INSTAGRAM:harborwatch"}, "label": "related"},
    ]
    out = await _out(
        "data.join",
        {"items": photos, "other": decisions},
        {"key": "found_on", "other_key": "account.key", "normalize": "case_space", "many": "all", "as": "decisions"},
    )
    assert [d["label"] for d in out["items"][0]["decisions"]] == ["match", "related"]
    # a photo with no key never matches (a hole is not equal to another hole)
    assert out["items"][1]["decisions"] == []
    assert out["other_unmatched"] == []


async def test_join_empty_lists():
    out = await _out("data.join", {"items": [], "other": ANSWERS}, {"key": "id"})
    assert out["items"] == [] and out["matched"] == 0 and len(out["other_unmatched"]) == 4
    out = await _out("data.join", {"items": CANDIDATES, "other": []}, {"key": "id"})
    assert out["unmatched"] == 3 and all(i["match"] is None for i in out["items"])


async def test_join_merge_refuses_plain_values():
    result = await _run("data.join", {"items": ["c1"], "other": [{"id": "c1"}]}, {"mode": "merge", "other_key": "id"})
    assert result.status is not RunStatus.COMPLETED
    assert "mode merge needs objects" in str(result.error)
