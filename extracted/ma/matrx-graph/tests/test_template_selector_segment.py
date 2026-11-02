"""``[field=value]`` — a template path segment that picks a list element by a field (a join by id)."""

from __future__ import annotations

import pytest

from matrx_graph.nodes._template import TemplatePathMissing, substitute_template

CHUNKS = [{"chunk_id": "c1", "content": "one"}, {"chunk_id": "c2", "content": "two"}]


def test_select_by_the_element_itself() -> None:
    out = substitute_template("$in.chunks.[chunk_id={$item}].content", "c2", index=0, extra={"chunks": CHUNKS})
    assert out == "two"


def test_select_by_a_path_into_the_element_and_by_a_literal() -> None:
    assert substitute_template("$in.chunks.[chunk_id={$item.cid}].content", {"cid": "c1"}, index=0, extra={"chunks": CHUNKS}) == "one"
    assert substitute_template("$in.chunks.[chunk_id=c2].content", None, extra={"chunks": CHUNKS}) == "two"


def test_no_match_is_a_missing_path_that_optional_absorbs() -> None:
    with pytest.raises(TemplatePathMissing):
        substitute_template("$in.chunks.[chunk_id={$item}].content", "zz", index=0, extra={"chunks": CHUNKS})
    out = substitute_template({"$optional": "$in.chunks.[chunk_id={$item}].content", "default": ""}, "zz", index=0, extra={"chunks": CHUNKS})
    assert out == ""
