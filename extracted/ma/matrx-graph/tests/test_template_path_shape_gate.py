"""A ``$item`` TEMPLATE IS CHECKED — statically where the shape is declared,
and named honestly at run time where it is not.

The defect (live 2026-09-12, Newsroom Desk run ``08568b55``): the Conductor
wired ``control.gather`` → ``data.map_template`` with ``{"items": "values"}``
and templated ``{"entries": "$item.entries", ...}``. ``gather_result.values``
holds the RAW per-item results — the fields are ``structured_output`` /
``final_text`` / ``messages`` — so the path could never resolve. Four paid
ledger agents ran, then step 5 died on ``segment 'entries' is missing or not
indexable`` and nothing told the author what WAS there or where ``entries``
actually lived. Edge mappings had been schema-checked since 2026-09-11; the
template inside the node was checked by nothing.

What is locked here:

1. a ``$item.<path>`` over elements of a DESCRIBED, CLOSED list is rejected at
   validate time, naming the node, the path, the element's real fields and the
   upstream field the list came from;
2. a path that IS a declared element field still validates (no false alarm);
3. an UNDESCRIBED element (``list[JsonValue]`` — which is exactly
   ``gather_result.values``) yields NO static finding: an unprovable path is
   not a finding, and guessing would block legitimate authoring;
4. so case 3 is caught at RUN time instead, by an error that names the keys the
   element actually has, the nested path where the wanted field really lives,
   and the gather collections (``structured_outputs`` / ``final_texts``) the
   list should have been mapped from.
"""

from __future__ import annotations

from typing import Any, ClassVar

import pytest
from matrx_graph import Definition, NodeRegistry, register_builtin_nodes
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.control.gather import GatherOutput
from matrx_graph.nodes.data.map_template import (
    MapTemplateConfig,
    MapTemplateExecutor,
    MapTemplateInput,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from pydantic import BaseModel, ConfigDict, Field


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Row(BaseModel):
    """A described, CLOSED element — the case a static check can settle."""

    model_config = ConfigDict(extra="forbid")

    url: str = ""
    title: str = ""


class _DescribedList(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rows: list[_Row] = Field(default_factory=list)


class _OpaqueList(BaseModel):
    """The gather case: a list whose elements the schema does not describe."""

    model_config = ConfigDict(extra="forbid")

    values: list[Any] = Field(default_factory=list)


def _source_node(node_type: str, output_schema: type[BaseModel]) -> Any:
    class _Node:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type=node_type,
            category=NodeCategory.DATA,
            display_name=node_type,
            description="emits a list",
            input_schema=_In,
            output_schema=output_schema,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.PURE,
        )

        async def execute(
            self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
        ) -> NodeResult[Any]:
            return success(output_schema())

    return _Node()


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _defn(source_type: str, source_key: str, template: dict[str, Any]) -> dict:
    return {
        "version": "1",
        "nodes": [
            {"id": "src", "type": source_type, "position": {"x": 0, "y": 0}, "data": {}},
            {
                "id": "n_reduce",
                "type": "data.map_template",
                "position": {"x": 240, "y": 0},
                "data": {"label": "Keep only the ledger entries", "config": {"template": template}},
            },
        ],
        "edges": [
            {
                "id": "e_src_reduce",
                "source": "src",
                "target": "n_reduce",
                "data": {"kind": "data", "mappings": {"items": source_key}},
            }
        ],
    }


def _template_issues(result: Any) -> list[Any]:
    return [i for i in result.issues if i.node_id == "n_reduce" and "template" in i.path]


# ---------------------------------------------------------------------------
# 1 + 2. Validate time, where the element schema settles it
# ---------------------------------------------------------------------------


def test_item_path_absent_from_a_described_element_is_a_compile_error():
    registry = _registry(_source_node("test.described", _DescribedList))
    result = validate_definition(
        Definition.model_validate(_defn("test.described", "rows", {"u": "$item.entries"})),
        registry=registry,
    )

    assert not result.valid
    issue = next(i for i in _template_issues(result) if i.severity == "error")
    assert "$item.entries" in issue.message
    assert "segment 'entries'" in issue.message
    assert "'rows'" in issue.message  # the upstream field the list came from
    assert "'src'" in issue.message  # the node that emits it
    assert "['title', 'url']" in issue.message  # what an element DOES offer
    assert issue.edge_id == "e_src_reduce"


def test_item_path_that_is_a_declared_element_field_validates():
    registry = _registry(_source_node("test.described", _DescribedList))
    result = validate_definition(
        Definition.model_validate(
            _defn("test.described", "rows", {"u": "$item.url", "t": "$item.title"})
        ),
        registry=registry,
    )

    assert _template_issues(result) == []


# ---------------------------------------------------------------------------
# 3. Validate time stays SILENT on an undescribed element
# ---------------------------------------------------------------------------


def test_undescribed_element_yields_no_static_finding():
    registry = _registry(_source_node("test.opaque", _OpaqueList))
    result = validate_definition(
        Definition.model_validate(_defn("test.opaque", "values", {"e": "$item.entries"})),
        registry=registry,
    )

    assert _template_issues(result) == []


def test_gather_values_elements_are_genuinely_undescribed():
    """The honest limit, read off the real kind: this is WHY case 4 exists."""
    from matrx_graph.shape_probe import is_described, item_schema_of, schema_at_path

    root = GatherOutput.model_json_schema()
    values = schema_at_path(root, "values")
    assert values is not None
    assert not is_described(item_schema_of(values, root))
    # …while a sibling collection with a real element model IS described.
    holes = schema_at_path(root, "holes")
    assert holes is not None
    assert is_described(item_schema_of(holes, root))


# ---------------------------------------------------------------------------
# 4. Run time names what is there and where the field really lives
# ---------------------------------------------------------------------------


#: The real per-item shape gather put in `values` on run 08568b55.
_RAW_AGENT_RESULT: dict[str, Any] = {
    "usage": {"input_tokens": 12},
    "messages": [{"role": "user", "content": "…"}],
    "model": "a-model",
    "final_text": "the ledger, at length",
    "structured_output": {
        "entries": [{"claim": "one"}],
        "document": "the write-up",
        "accusations": [],
        "named_parties": [],
        "open_questions": [],
    },
}


async def test_runtime_miss_names_keys_nested_path_and_gather_collections():
    with pytest.raises(ExecutionError) as exc:
        await MapTemplateExecutor().execute(
            None,  # type: ignore[arg-type] — this node's execute never touches ctx
            MapTemplateInput(items=[_RAW_AGENT_RESULT]),
            MapTemplateConfig(template={"entries": "$item.entries"}),
        )

    message = str(exc.value)
    # The finding itself, unchanged.
    assert "template path '$item.entries' does not resolve for item 0" in message
    # The remedy — all three halves the old message lacked.
    assert "'usage', 'messages', 'model', 'final_text', 'structured_output'" in message.replace(
        '"', "'"
    )
    assert "'$item.structured_output.entries'" in message
    assert "structured_outputs" in message and "final_texts" in message


async def test_runtime_remedy_keeps_the_walked_prefix():
    with pytest.raises(ExecutionError) as exc:
        await MapTemplateExecutor().execute(
            None,  # type: ignore[arg-type]
            MapTemplateInput(items=[{"payload": _RAW_AGENT_RESULT}]),
            MapTemplateConfig(template={"d": "$item.payload.document"}),
        )

    assert "'$item.payload.structured_output.document'" in str(exc.value)


# ---------------------------------------------------------------------------
# 5. The authoring digest: the shape an author was never shown
# ---------------------------------------------------------------------------


def test_upstream_shape_notes_show_the_gather_choice_in_its_own_words():
    """The exact Newsroom Desk wiring, and what an author now gets back."""
    from matrx_graph.shape_probe import upstream_shape_notes

    registry = _registry()
    defn = {
        "version": "1",
        "nodes": [
            {"id": "n_gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {}},
            {
                "id": "n_reduce",
                "type": "data.map_template",
                "position": {"x": 240, "y": 0},
                "data": {"config": {"template": {"entries": "$item.entries"}}},
            },
        ],
        "edges": [
            {
                "id": "e_gather_reduce",
                "source": "n_gather",
                "target": "n_reduce",
                "data": {"kind": "data", "mappings": {"items": "values"}},
            }
        ],
    }
    notes = upstream_shape_notes(defn, registry)

    source = next(n for n in notes if n.get("node_id") == "n_gather")
    assert source["output_kind"] == "gather_result"
    # The decision `values` vs `structured_outputs` is settled by the emitting
    # step's OWN words — so those words travel.
    assert "RAW per-item results" in source["emits"]["values"]
    assert "structured_output" in source["emits"]["structured_outputs"]
    assert source["read_by"] == [{"node_id": "n_reduce", "reads": {"items": "values"}}]

    host = next(n for n in notes if n.get("node_id") == "n_reduce")
    assert host["template_paths"] == ["$item.entries"]
    assert host["items_come_from"] == {"node_id": "n_gather", "path": "values"}
    # Honest about its own limit, with the remedy — never a silent null.
    assert host["element_fields"] is None
    assert "one level down" in host["element_is_undeclared"]


def test_upstream_shape_notes_describe_a_declared_element():
    from matrx_graph.shape_probe import upstream_shape_notes

    registry = _registry(_source_node("test.described", _DescribedList))
    notes = upstream_shape_notes(_defn("test.described", "rows", {"u": "$item.url"}), registry)
    host = next(n for n in notes if n.get("node_id") == "n_reduce")
    assert sorted(host["element_fields"]) == ["title", "url"]
    assert "element_is_undeclared" not in host
