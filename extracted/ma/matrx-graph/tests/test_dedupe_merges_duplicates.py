"""``data.dedupe`` merge option (2026-10-26): keep one row per key, lose nothing.

The break this catches: duplicates are dropped with their values, so a result
found by three engines keeps only the first engine and the first engine's rank.
Users: merging web results across engines/queries, contacts found on several
pages, social accounts found by several sources.
"""

from __future__ import annotations

from matrx_graph import RunStatus

from tests.test_data_collections import _out, _run

MERGE = {"combine_lists": ["engines", "queries"], "keep_lowest": ["rank"]}


async def test_dedupe_merge_combines_lists_and_keeps_lowest_rank():
    results = [
        {"url": "https://tidewaterkayak.com/tours", "engines": ["brave"], "queries": ["kayak tours"], "rank": 4},
        {"url": "https://bayshoremarina.com/slips", "engines": ["brave"], "queries": ["boat slips"], "rank": 1},
        {"url": "https://tidewaterkayak.com/tours", "engines": ["google"], "queries": ["sea kayaking"], "rank": 2},
        {"url": "https://tidewaterkayak.com/tours", "engines": ["google", "bing"], "queries": ["kayak tours"], "rank": 7},
    ]
    out = await _out("data.dedupe", {"items": results}, {"key": "url", "merge": MERGE})
    assert out["items"] == [
        {
            "url": "https://tidewaterkayak.com/tours",
            "engines": ["brave", "google", "bing"],
            "queries": ["kayak tours", "sea kayaking"],
            "rank": 2,
        },
        {"url": "https://bayshoremarina.com/slips", "engines": ["brave"], "queries": ["boat slips"], "rank": 1},
    ]
    assert out["kept"] == 2
    assert out["dropped"] == 2


async def test_dedupe_merge_treats_single_values_as_lists_and_skips_empties():
    contacts = [
        {"email": "dana.ortiz@harborclinic.org", "found_on": "https://harborclinic.org/team", "phone": "(949) 555-0142"},
        {"email": "dana.ortiz@harborclinic.org", "found_on": None, "phone": "(949) 555-0199"},
        {"email": "dana.ortiz@harborclinic.org", "found_on": "https://harborclinic.org/contact"},
    ]
    out = await _out(
        "data.dedupe",
        {"items": contacts},
        {"key": "email", "merge": {"combine_lists": ["found_on"]}},
    )
    assert out["items"] == [
        {
            "email": "dana.ortiz@harborclinic.org",
            "found_on": ["https://harborclinic.org/team", "https://harborclinic.org/contact"],
            # Not a merge field: the first copy's value is kept.
            "phone": "(949) 555-0142",
        }
    ]


async def test_dedupe_without_merge_still_drops_duplicate_values():
    results = [
        {"url": "https://tidewaterkayak.com/tours", "engines": ["brave"], "rank": 4},
        {"url": "https://tidewaterkayak.com/tours", "engines": ["google"], "rank": 2},
    ]
    out = await _out("data.dedupe", {"items": results}, {"key": "url"})
    assert out["items"] == [results[0]]


async def test_dedupe_merge_refuses_a_list_of_plain_values():
    result = await _run(
        "data.dedupe",
        {"items": ["@harborwatch", "@harborwatch"]},
        {"merge": {"combine_lists": ["sources"]}},
    )
    assert result.status is not RunStatus.COMPLETED
    assert "merge needs each item to be an object" in str(result.error)


# ---------------------------------------------------------------------------
# fill_empty (2026-10-27): a blank on the surviving copy takes the first
# non-empty value across the copies. The break this catches: one engine has the
# description, another the thumbnail, and the survivor keeps only its own blanks.
# Users: web results merged by address, social accounts found by several
# sources, CRM duplicate contacts, news stories merged across feeds.
# ---------------------------------------------------------------------------


async def test_dedupe_fill_empty_takes_the_first_non_empty_value_across_copies():
    accounts = [
        {"key": "instagram:harborwatch", "display_name": "", "bio": None, "followers": 1200, "found_where": ["search"]},
        {"key": "instagram:harborwatch", "display_name": "Harbor Watch", "found_where": ["site footer"]},
        {"key": "instagram:harborwatch", "display_name": "HW", "bio": "Tide tables daily", "followers": 9, "found_where": []},
    ]
    out = await _out(
        "data.dedupe",
        {"items": accounts},
        {"key": "key", "merge": {"combine_lists": ["found_where"], "fill_empty": ["display_name", "bio", "followers"]}},
    )
    assert out["items"] == [
        {
            "key": "instagram:harborwatch",
            # blank '' filled from the second copy, missing/None bio from the third
            "display_name": "Harbor Watch",
            "bio": "Tide tables daily",
            # the survivor's own value is never replaced
            "followers": 1200,
            "found_where": ["search", "site footer"],
        }
    ]


async def test_dedupe_fill_empty_star_fills_every_unnamed_field_and_adds_missing_ones():
    results = [
        {"url": "https://tidewaterkayak.com/tours", "title": "Tours", "description": "  ", "engines": ["brave"]},
        {"url": "https://tidewaterkayak.com/tours", "description": "Guided sea kayak tours", "thumbnail": "https://img.example.com/t.png", "engines": ["google"]},
    ]
    out = await _out(
        "data.dedupe",
        {"items": results},
        {"key": "url", "merge": {"combine_lists": ["engines"], "fill_empty": ["*"]}},
    )
    assert out["items"] == [
        {
            "url": "https://tidewaterkayak.com/tours",
            "title": "Tours",
            "description": "Guided sea kayak tours",
            "engines": ["brave", "google"],
            "thumbnail": "https://img.example.com/t.png",
        }
    ]


async def test_dedupe_fill_empty_leaves_a_field_empty_when_every_copy_is_empty():
    items = [{"id": "a", "note": ""}, {"id": "a", "note": None}]
    out = await _out("data.dedupe", {"items": items}, {"key": "id", "merge": {"fill_empty": ["note"]}})
    assert out["items"] == [{"id": "a", "note": ""}]
