from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.catalog.models import ControlRule, _RuleMap


def test_rule_submodels_accept_markers_and_omit_them_when_serialized() -> None:
    rule = ControlRule.model_validate(
        {
            "__kind": "control_rule",
            "clamp": {"__kind": "clamp", "min": 1, "max": 8},
            "off": {"__kind": "off_rule", "floor": True},
            "from_number": [{"__kind": "from_number_step", "lte": 4, "to": 2}],
        }
    )

    assert rule.model_dump(exclude_unset=True) == {
        "clamp": {"min": 1.0, "max": 8.0},
        "off": {"floor": True},
        "from_number": [{"lte": 4.0, "to": 2}],
    }
    assert "__kind" in ControlRule.model_json_schema()["properties"]


def test_open_rule_map_accepts_root_marker_but_keeps_semantic_kind_key() -> None:
    schema = _RuleMap.model_json_schema()
    parsed = _RuleMap.model_validate(
        {"__kind": "value_map", "kind_": "semantic", "some_key": {"__kind": "nested"}}
    )

    assert "__kind" in schema["properties"]
    assert parsed.model_dump() == {
        "kind_": "semantic",
        "some_key": {"__kind": "nested"},
    }


def test_rule_markers_do_not_weaken_existing_value_validation() -> None:
    with pytest.raises(ValidationError):
        ControlRule.model_validate({"to_number": {"x": "not-an-int"}})
    with pytest.raises(ValidationError, match="processor_config requires processor"):
        ControlRule.model_validate({"processor_config": {"order": 5}})
    with pytest.raises(ValidationError, match="exclusive with"):
        ControlRule.model_validate({"processor": "example", "value_map": {"a": "b"}})
    with pytest.raises(ValidationError, match="exclusive with"):
        ControlRule.model_validate({"processor": "example", "const": 1})
