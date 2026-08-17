"""Deterministic JSON structure sketch used in the Layer 1 offload preview."""

import json

from xpander_sdk.core.context_optimizer.structure_sketch import (
    _MAX_PARSE_CHARS,
    sketch_structure,
)


def test_homogeneous_object_array_reports_count_and_keys():
    payload = json.dumps(
        [{"id": f"u{i}", "name": "x", "tags": ["a", "b"]} for i in range(1240)]
    )
    sketch = sketch_structure(payload)
    assert sketch is not None
    assert "array of 1,240 objects" in sketch
    assert "id: str" in sketch
    assert "name: str" in sketch
    assert "tags: array of 2 str" in sketch


def test_keys_missing_from_some_items_are_marked_optional():
    payload = json.dumps([{"id": "a", "archived": True}, {"id": "b"}, {"id": "c"}])
    sketch = sketch_structure(payload)
    assert "id: bool" not in sketch
    assert "id: str" in sketch
    assert "archived?: bool" in sketch


def test_object_with_nested_arrays():
    payload = json.dumps(
        {
            "items": [{"sku": "s", "qty": 3} for _ in range(500)],
            "next_cursor": "abc",
            "has_more": True,
        }
    )
    sketch = sketch_structure(payload)
    assert sketch.startswith("JSON object {")
    assert "items: array of 500 objects {sku: str, qty: int}" in sketch
    assert "next_cursor: str" in sketch
    assert "has_more: bool" in sketch


def test_heterogeneous_list_reports_a_type_histogram():
    payload = json.dumps([{"a": 1}] * 8 + ["text"] * 2)
    sketch = sketch_structure(payload)
    assert "array of 10 items (mixed:" in sketch
    assert "8 object" in sketch
    assert "2 str" in sketch


def test_tail_difference_is_caught_by_the_last_item_sample():
    payload = json.dumps([{"a": 1}] * 200 + ["surprise"])
    sketch = sketch_structure(payload)
    assert "mixed" in sketch


def test_many_keys_of_differing_shape_are_capped_with_a_remainder_note():
    payload = json.dumps([{f"k{i}": ("s" if i % 2 else i) for i in range(30)}])
    sketch = sketch_structure(payload)
    assert "+18 more keys" in sketch


def test_a_map_keyed_by_identifiers_is_described_by_entry_shape():
    payload = json.dumps(
        {f"user_{i}@example.com": {"seen": 1, "plan": "pro"} for i in range(40)}
    )
    sketch = sketch_structure(payload)
    assert "map of 40 entries, each {seen: int, plan: str}" in sketch
    assert "example.com" not in sketch


def test_stringified_json_inside_a_wrapper_is_described():
    inner = json.dumps([{"id": i, "name": "n"} for i in range(40)])
    payload = json.dumps({"status": "ok", "body": inner})
    sketch = sketch_structure(payload)
    assert "body: str holding array of 40 objects" in sketch


def test_non_json_content_returns_none():
    assert sketch_structure("just some log output\nline two") is None
    assert sketch_structure("") is None
    assert sketch_structure('"a bare json string"') is None
    assert sketch_structure("{not valid json") is None


def test_payload_above_the_parse_cap_returns_none():
    payload = "[" + ("1," * (_MAX_PARSE_CHARS // 2)) + "1]"
    assert len(payload) > _MAX_PARSE_CHARS
    assert sketch_structure(payload) is None


def test_output_is_clipped_and_single_line():
    payload = json.dumps([{f"key_with_a_long_name_{i}": "v" for i in range(12)}])
    sketch = sketch_structure(payload, max_chars=80)
    assert len(sketch) <= 80
    assert sketch.endswith("...")
    assert "\n" not in sketch


def test_sketch_is_deterministic():
    payload = json.dumps([{"b": 1, "a": "x"} for _ in range(50)])
    assert sketch_structure(payload) == sketch_structure(payload)


def test_values_never_appear_in_the_sketch():
    payload = json.dumps(
        [{"token": "REDACT-ME-PLACEHOLDER", "count": 5} for _ in range(3)]
    )
    sketch = sketch_structure(payload)
    assert "REDACT-ME-PLACEHOLDER" not in sketch
    assert "token: str" in sketch
    assert "count: int" in sketch


def test_deeply_nested_values_collapse_at_the_depth_cap():
    payload = json.dumps({"a": {"b": {"c": {"d": {"e": 1}}}}})
    sketch = sketch_structure(payload)
    assert "{...}" in sketch


def test_empty_containers():
    assert sketch_structure("[]") == "JSON empty array"
    assert sketch_structure("{}") == "JSON object {}"
