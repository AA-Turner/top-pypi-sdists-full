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

    # Content-IR rule 32: a NAMED marker is never destroyed; it round-trips exactly as written.
    assert rule.model_dump(exclude_unset=True) == {
        "__kind": "control_rule",
        "clamp": {"__kind": "clamp", "min": 1.0, "max": 8.0},
        "off": {"__kind": "off_rule", "floor": True},
        "from_number": [{"__kind": "from_number_step", "lte": 4.0, "to": 2}],
    }
    # Rule 31: a sub-structure's schema declares NO ``__kind`` (never a blank ``const ""``).
    assert "__kind" not in ControlRule.model_json_schema().get("properties", {})


def test_a_blank_marker_is_accepted_and_dropped() -> None:
    rule = ControlRule.model_validate({"__kind": "", "clamp": {"__kind": "", "min": 1, "max": 8}})
    assert rule.model_dump(exclude_unset=True) == {"clamp": {"min": 1.0, "max": 8.0}}


def test_open_rule_map_accepts_root_marker_but_keeps_semantic_kind_key() -> None:
    schema = _RuleMap.model_json_schema()
    parsed = _RuleMap.model_validate(
        {"__kind": "value_map", "kind_": "semantic", "some_key": {"__kind": "nested"}}
    )

    assert "__kind" not in schema.get("properties", {})
    assert parsed.model_dump() == {
        "__kind": "value_map",
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
