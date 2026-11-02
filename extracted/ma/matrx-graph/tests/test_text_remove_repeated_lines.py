"""text.remove_repeated_lines: footer on 3 of 4 pages, threshold edge, empty text, ids kept."""

from __future__ import annotations

from tests.test_text_nodes import _run_single_node

NODE = "text.remove_repeated_lines"
NAV = "Home | Pricing | Contact"
FOOT = "(c) 2026 Acme Inc"


def _pages() -> list[dict]:
    return [
        {"id": "a", "text": f"{NAV}\nAbout us\nWe build things.\n{FOOT}"},
        {"id": "b", "text": f"{NAV}\nPricing\nFrom $5.\n  {FOOT}  "},
        {"id": "c", "text": f"{NAV}\nBlog post\nHello.\n(c)  2026   Acme Inc"},
        {"id": "d", "text": "Standalone page\nNo footer here."},
    ]


async def test_footer_on_three_of_four_pages_is_removed_and_listed_once() -> None:
    out = await _run_single_node(NODE, {"texts": _pages()}, {"min_texts": 3})
    assert out["repeated_lines"] == [NAV, FOOT]
    by_id = {i["id"]: i for i in out["items"]}
    assert by_id["a"]["text"] == "About us\nWe build things."
    assert by_id["c"]["text"] == "Blog post\nHello."
    assert by_id["d"]["text"] == "Standalone page\nNo footer here."
    assert by_id["a"]["removed"] == 2 and by_id["d"]["removed"] == 0
    assert out["__kind"] == "repeated_lines_result"


async def test_threshold_edge_two_of_four_is_kept_at_three_removed_at_two() -> None:
    texts = ["x\nonly two", "x\nsecond", "y\nthird", "z\nfourth"]
    kept = await _run_single_node(NODE, {"texts": texts}, {"min_texts": 3})
    assert kept["repeated_lines"] == [] and kept["items"][0]["text"] == "x\nonly two"
    gone = await _run_single_node(NODE, {"texts": texts}, {"min_texts": 2})
    assert gone["repeated_lines"] == ["x"] and gone["items"][0]["text"] == "only two"


async def test_a_line_repeated_inside_one_text_counts_once() -> None:
    out = await _run_single_node(NODE, {"texts": ["x\nx\nx\nuniq", "other"]}, {"min_texts": 2})
    assert out["repeated_lines"] == []


async def test_emptied_and_empty_texts_are_flagged_not_dropped_and_ids_kept() -> None:
    texts = [{"id": 7, "text": NAV}, {"id": 8, "text": NAV}, {"id": 9, "text": ""}, "plain"]
    out = await _run_single_node(NODE, {"texts": texts}, {"min_texts": 2})
    assert [i["id"] for i in out["items"]] == [7, 8, 9, 3]
    assert out["emptied_ids"] == [7, 8, 9]
    assert out["text_count"] == 4
    assert out["items"][3] == {**out["items"][3], "text": "plain", "emptied": False}


async def test_object_items_use_configured_fields_and_plain_strings_get_positions() -> None:
    out = await _run_single_node(
        NODE,
        {"texts": [{"url": "u1", "body": "k\nA"}, {"url": "u2", "body": "k\nB"}]},
        {"min_texts": 2, "text_field": "body", "id_field": "url"},
    )
    assert [(i["id"], i["text"]) for i in out["items"]] == [("u1", "A"), ("u2", "B")]


def test_step_is_registered_with_plain_schema() -> None:
    from matrx_graph import NodeRegistry, register_builtin_nodes

    reg = NodeRegistry()
    register_builtin_nodes(reg)
    spec = reg.get(NODE).spec
    assert spec.output_kind == "repeated_lines_result"
    assert "min_texts" in spec.config_schema.model_json_schema()["properties"]


async def test_none_item_counts_as_empty_text_and_is_flagged() -> None:
    out = await _run_single_node(NODE, {"texts": [None, {"id": "z", "text": None}, "a"]}, {})
    assert [i["emptied"] for i in out["items"]] == [True, True, False]
    assert out["emptied_ids"] == [0, "z"]


async def test_same_folding_as_the_platform_and_blank_lines_kept() -> None:
    texts = [
        "**Menu**\nfirst\n\nbody one",
        "# Menu\nsecond\n\nbody two",
        "Menu\nthird\n\nbody three",
    ]
    out = await _run_single_node(NODE, {"texts": texts}, {"min_texts": 3})
    assert out["repeated_lines"] == ["**Menu**"]  # first-seen original wording
    assert out["items"][0]["text"] == "first\n\nbody one"
    assert out["items"][1]["text"] == "second\n\nbody two"
