from __future__ import annotations

import pytest
from matrx_graph import (
    ActionTier,
    EdgeKind,
    HandleDirection,
    HandleSpec,
    NodeCategory,
    NodeSpec,
    RetryPolicy,
    field_extras,
)
from pydantic import BaseModel, Field


class _BranchConfig(BaseModel):
    predicate: str = Field(
        description="A boolean expression over the incoming payload",
        json_schema_extra=field_extras(widget="code", help="Jinja expression"),
    )


class _BranchInput(BaseModel):
    value: dict[str, object]


class _BranchOutput(BaseModel):
    direction: str


def test_node_spec_minimal():
    spec = NodeSpec(
        type="control.branch",
        category=NodeCategory.CONTROL,
        display_name="Branch",
        input_schema=_BranchInput,
        output_schema=_BranchOutput,
        config_schema=_BranchConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(
                id="true",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL,),
            ),
            HandleSpec(
                id="false",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL,),
            ),
        ),
        determinism=ActionTier.PURE,
    )
    assert spec.node_type == "control.branch"
    assert spec.determinism is ActionTier.PURE
    assert spec.retry == RetryPolicy.default()
    assert len(spec.handles) == 3


def test_node_spec_accepts_type_alias_for_construction():
    # Both alias "type" and python-field "node_type" work thanks to populate_by_name.
    a = NodeSpec(type="control.branch", category=NodeCategory.CONTROL, display_name="A")
    b = NodeSpec(node_type="control.branch", category=NodeCategory.CONTROL, display_name="A")
    assert a.node_type == b.node_type == "control.branch"


def test_node_spec_type_format_validated():
    with pytest.raises(Exception):
        NodeSpec(
            type="ControlBranch",  # must be snake_case dotted
            category=NodeCategory.CONTROL,
            display_name="Bad",
        )
    with pytest.raises(Exception):
        NodeSpec(
            type="control",  # needs at least one dot
            category=NodeCategory.CONTROL,
            display_name="Bad",
        )


def test_node_spec_palette_descriptor_shape():
    spec = NodeSpec(
        type="control.branch",
        category=NodeCategory.CONTROL,
        display_name="Branch",
        config_schema=_BranchConfig,
    )
    d = spec.to_palette_descriptor()
    # External palette key is still "type" — the rename is internal only.
    assert d["type"] == "control.branch"
    assert d["category"] == "control"
    assert "config_schema" in d
    assert d["config_schema"]["type"] == "object"
    # USL hints survive round-trip into JSON Schema
    props = d["config_schema"]["properties"]
    assert props["predicate"]["ui:widget"] == "code"


def test_handle_spec_frozen():
    h = HandleSpec(id="in", direction=HandleDirection.INPUT)
    with pytest.raises(Exception):
        h.id = "changed"  # type: ignore[misc]
