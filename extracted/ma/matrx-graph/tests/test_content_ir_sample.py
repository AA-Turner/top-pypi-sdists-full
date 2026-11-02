from datetime import date, datetime
from decimal import Decimal
from typing import Literal

import pytest
from pydantic import BaseModel, ConfigDict, JsonValue, ValidationError, create_model

from matrx_graph.content_ir.sample import contract_drift, synthesize_payload


class EmittedItem(BaseModel):
    value: int
    newly_emitted: str


class ConsumedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: int


@pytest.mark.parametrize(
    ("emitted", "consumed", "location"),
    [
        (list[EmittedItem], list[ConsumedItem], "items.0.newly_emitted"),
        (tuple[EmittedItem, ...], tuple[ConsumedItem, ...], "items.0.newly_emitted"),
        (tuple[int, EmittedItem], tuple[int, ConsumedItem], "items.1.newly_emitted"),
        (dict[str, EmittedItem], dict[str, ConsumedItem], "items..newly_emitted"),
        (list[list[EmittedItem]], list[list[ConsumedItem]], "items.0.0.newly_emitted"),
    ],
)
def test_nested_container_contracts_are_exercised(emitted, consumed, location):
    source = create_model("Source", items=(emitted, ...))
    target = create_model("Target", items=(consumed, ...))
    payload = synthesize_payload(source)
    source.model_validate(payload)
    with pytest.raises(ValidationError):
        target.model_validate(payload)
    assert (location, "extra_forbidden") in contract_drift(source, target)
    assert contract_drift(source, source) == []


def test_matching_nested_models_do_not_report_drift():
    class Consumer(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: int
        newly_emitted: str

    source = create_model("Source", items=(list[EmittedItem], ...))
    target = create_model("Target", items=(list[Consumer], ...))
    assert contract_drift(source, target) == []


def test_populated_mapping_preserves_typed_keys():
    class Source(BaseModel):
        items: dict[Literal["row"], EmittedItem]

    payload = synthesize_payload(Source)
    assert "row" in payload["items"]
    Source.model_validate(payload)


def test_dynamic_json_inside_containers_is_synthesizable():
    class Source(BaseModel):
        items: list[dict[str, JsonValue]]

    payload = synthesize_payload(Source)
    assert payload["items"]
    Source.model_validate(payload)
    assert contract_drift(Source, Source) == []


@pytest.mark.parametrize(
    ("emitted_type", "consumed_type", "error"),
    [
        (float, int, "int_from_float"),
        (int, bool, "bool_parsing"),
        (Decimal, int, "int_parsing"),
        (datetime, date, "date_from_datetime_inexact"),
    ],
)
@pytest.mark.parametrize("container", ["model", "list", "map"])
def test_coercible_placeholders_do_not_hide_type_drift(
    emitted_type, consumed_type, error, container
):
    emitted = create_model("Emitted", value=(emitted_type, ...))
    consumed = create_model("Consumed", value=(consumed_type, ...))
    wrap = {"model": lambda t: t, "list": lambda t: list[t], "map": lambda t: dict[str, t]}[
        container
    ]
    source = create_model("Source", items=(wrap(emitted), ...))
    target = create_model("Target", items=(wrap(consumed), ...))
    payload = synthesize_payload(source)
    source.model_validate(payload)
    with pytest.raises(ValidationError):
        target.model_validate(payload)
    assert any(code == error for _, code in contract_drift(source, target))
    assert contract_drift(source, source) == []
