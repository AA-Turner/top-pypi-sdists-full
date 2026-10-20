"""Three-way merge of one context value: non-overlapping edits both land, overlapping edits
never silently pick a winner (context passthrough's simultaneous-edit rule)."""

from __future__ import annotations

from matrx_ai.tools.merge3 import merge_json, merge_text, merge_value, what_changed

CHECKLIST = "# Launch\n- [ ] copy\n- [ ] images\n- [ ] links\n"


def test_two_writers_ticking_different_items_both_land():
    mine = CHECKLIST.replace("- [ ] copy", "- [x] copy")
    theirs = CHECKLIST.replace("- [ ] links", "- [x] links")
    assert merge_text(CHECKLIST, mine, theirs) == "# Launch\n- [x] copy\n- [ ] images\n- [x] links\n"


def test_two_writers_editing_the_same_item_overlap():
    mine = CHECKLIST.replace("- [ ] copy", "- [x] copy")
    theirs = CHECKLIST.replace("- [ ] copy", "- [ ] copy (blocked)")
    assert merge_text(CHECKLIST, mine, theirs) is None


def test_two_inserts_at_the_same_place_overlap():
    assert merge_text(CHECKLIST, CHECKLIST + "- [ ] a\n", CHECKLIST + "- [ ] b\n") is None


def test_an_overwrite_of_a_changed_record_overlaps():
    theirs = CHECKLIST.replace("images", "photos")
    assert merge_text(CHECKLIST, "brand new text\n", theirs) is None


def test_nothing_changed_on_one_side_takes_the_other():
    mine = CHECKLIST.replace("copy", "COPY")
    assert merge_text(CHECKLIST, mine, CHECKLIST) == mine
    assert merge_text(CHECKLIST, CHECKLIST, mine) == mine


def test_json_different_keys_merge_same_key_overlaps():
    base = {"status": "draft", "owner": {"name": "A"}, "tags": ["x"]}
    ok, merged = merge_json(base, {**base, "status": "ready"}, {**base, "owner": {"name": "B"}})
    assert ok and merged == {"status": "ready", "owner": {"name": "B"}, "tags": ["x"]}
    ok, _ = merge_json(base, {**base, "status": "ready"}, {**base, "status": "sent"})
    assert ok is False
    # A list is one value: two different list edits overlap.
    ok, _ = merge_json(base, {**base, "tags": ["x", "y"]}, {**base, "tags": ["x", "z"]})
    assert ok is False
    # A parent and its child overlap.
    ok, _ = merge_json(base, {**base, "owner": None}, {**base, "owner": {"name": "C"}})
    assert ok is False


def test_merge_value_routes_by_shape_and_what_changed_says_what_moved():
    ok, merged = merge_value("a\nb\n", "A\nb\n", "a\nB\n")
    assert ok and merged == "A\nB\n"
    assert "+- [x] links" in what_changed(CHECKLIST, CHECKLIST.replace("- [ ] links", "- [x] links"))
