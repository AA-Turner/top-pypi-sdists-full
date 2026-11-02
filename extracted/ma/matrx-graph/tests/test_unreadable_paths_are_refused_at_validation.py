"""A path the one resolver cannot read is an ERROR at validation, naming the step and field.

Live defect 2026-10-27: an edge mapping ``{"page_ids": "items[].page_id"}`` (meant
``items[*].page_id``) passed apply-patch as "valid"; ``parse_path`` read ``[]`` as a key
named ``""`` and the step silently received nothing. The validator now refuses any
mapping source / resolver config path the grammar cannot read.
"""

from __future__ import annotations

import pytest

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.paths import path_syntax_problem
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _defn(source: str, payload_key: str = "x") -> dict:
    # A dynamic-output source (io.user_input), so no schema check can see the path —
    # exactly where the live one slipped through.
    return {
        "version": "1",
        "nodes": [
            {
                "id": "intake",
                "type": "io.user_input",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"fields": [{"key": "items", "type": "text", "label": "Items"}]}},
            },
            {
                "id": "canon",
                "type": "text.template",
                "position": {"x": 0, "y": 220},
                "data": {"input": {"template": "T"}, "config": {}},
            },
            {
                "id": "show",
                "type": "output.to_frontend",
                "position": {"x": 0, "y": 440},
                "data": {"config": {"payload_key": payload_key}},
            },
        ],
        "edges": [
            {"id": "e1", "source": "intake", "target": "canon",
             "data": {"kind": "data", "mappings": {"variables": source}}},
            {"id": "e2", "source": "canon", "target": "show", "data": {"kind": "data"}},
        ],
    }


def test_the_live_bad_path_is_an_error_naming_the_edge_and_field() -> None:
    result = validate_definition(_defn("items[].page_id"), registry=_registry())
    assert not result.valid, "items[].page_id validated clean"
    errs = [i for i in result.issues if i.severity == "error" and i.edge_id == "e1"]
    assert errs, [i.message for i in result.issues]
    assert errs[0].path == "edges[e1].data.mappings.variables"
    assert "items[].page_id" in errs[0].message and "[*]" in errs[0].message


@pytest.mark.parametrize("bad", ["items[].page_id", "a..b", "a.", "a[0", "a]", "a[0]b"])
def test_every_unreadable_mapping_path_is_refused(bad: str) -> None:
    assert not validate_definition(_defn(bad), registry=_registry()).valid, bad


def test_a_config_path_the_resolver_reads_is_checked_too() -> None:
    result = validate_definition(_defn("items", payload_key="pages[].url"), registry=_registry())
    errs = [i for i in result.issues if i.severity == "error" and i.node_id == "show"]
    assert errs and errs[0].path == "nodes[show].data.config.payload_key", [i.message for i in result.issues]


@pytest.mark.parametrize("good", ["items", "items[*].page_id", "a.*.b", "a[0].b", "a[-1]", "a.0.b", "a\\.b"])
def test_readable_paths_still_pass(good: str) -> None:
    assert path_syntax_problem(good) is None
    result = validate_definition(_defn(good), registry=_registry())
    assert not [i for i in result.issues if i.severity == "error" and "readable path" in i.message], (
        [i.message for i in result.issues]
    )
