"""batched_list_result's left_out matches live kind v14: optional and nullable, absent unless asked.

The model said ``list`` defaulting to ``[]`` while the live kind (v14, 2026-10-27) allows null, so
publish_kind_catalog reported drift."""

from matrx_graph.nodes.data.collections import BatchOutput


def test_left_out_is_absent_unless_asked():
    assert BatchOutput.model_fields["left_out"].default is None
    assert not BatchOutput.model_fields["left_out"].is_required()


def test_left_out_schema_allows_null_and_a_list():
    prop = BatchOutput.model_json_schema()["properties"]["left_out"]
    types = {branch.get("type") for branch in prop.get("anyOf", [prop])}
    assert "null" in types and "array" in types
