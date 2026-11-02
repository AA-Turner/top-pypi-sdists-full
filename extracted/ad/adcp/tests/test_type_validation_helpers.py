"""Public union aliases can reuse adapters without changing validation."""

from __future__ import annotations

from typing import Annotated, Any, Literal

import pytest
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from adcp.types import VendorPricingOption, VendorPricingOptionUnion, validate_union, validation
from adcp.types.domains.core.vendor_pricing_option import (
    VendorPricingOption as GeneratedVendorPricingOption,
)


class _First(BaseModel):
    kind: Literal["first"]
    value: int


class _Second(BaseModel):
    kind: Literal["second"]
    value: str


_Tagged = Annotated[_First | _Second, Field(discriminator="kind")]


def test_vendor_pricing_aliases_bind_the_same_generated_union() -> None:
    assert VendorPricingOption is VendorPricingOptionUnion
    assert VendorPricingOption is GeneratedVendorPricingOption
    assert validate_union is validation.validate_union


@pytest.mark.parametrize(
    "fields",
    [
        {"model": "cpm", "cpm": 2.5, "currency": "USD"},
        {"model": "percent_of_media", "percent": 10.0, "currency": "USD"},
        {"model": "flat_fee", "amount": 20.0, "period": "campaign", "currency": "USD"},
        {"model": "per_unit", "unit": "render", "unit_price": 0.1, "currency": "USD"},
        {"model": "custom", "description": "Usage tier", "metadata": {}},
    ],
)
def test_every_vendor_pricing_arm_validates(fields: dict[str, Any]) -> None:
    payload = {"pricing_option_id": "price-1", **fields}
    result = validate_union(VendorPricingOption, payload)
    assert result.pricing_option_id == "price-1"
    assert result.model == fields["model"]
    assert result.model_dump(mode="json") == TypeAdapter(VendorPricingOption).validate_python(
        payload
    ).model_dump(mode="json")


def test_union_discriminator_is_preserved() -> None:
    first = validate_union(_Tagged, {"kind": "first", "value": 1})
    second = validate_union(_Tagged, {"kind": "second", "value": "x"})
    assert isinstance(first, _First)
    assert isinstance(second, _Second)
    with pytest.raises(ValidationError) as exc:
        validate_union(_Tagged, {"kind": "unknown", "value": 1})
    assert exc.value.errors()[0]["type"] == "union_tag_invalid"


def test_warm_validation_reuses_the_adapter_but_returns_independent_models(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validation._union_adapter.cache_clear()
    constructed: list[Any] = []

    def make_adapter(union: Any) -> TypeAdapter[Any]:
        constructed.append(union)
        return TypeAdapter(union)

    monkeypatch.setattr(validation, "TypeAdapter", make_adapter)
    first = validate_union(_Tagged, {"kind": "first", "value": 1})
    second = validate_union(_Tagged, {"kind": "first", "value": 2})
    assert constructed == [_Tagged]
    assert first is not second
    first.value = 99
    assert second.value == 2
    validation._union_adapter.cache_clear()


def test_cache_keeps_different_union_annotations_separate() -> None:
    with pytest.raises(ValidationError) as tagged:
        validate_union(_Tagged, {"kind": "unknown", "value": 1})
    with pytest.raises(ValidationError) as untagged:
        validate_union(_First | _Second, {"kind": "unknown", "value": 1})
    assert tagged.value.errors()[0]["type"] == "union_tag_invalid"
    assert untagged.value.errors()[0]["type"] == "literal_error"


def test_validation_errors_are_not_swallowed() -> None:
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        validate_union(
            VendorPricingOption,
            {"pricing_option_id": "price-1", "model": "cpm", "cpm": -1.0, "currency": "USD"},
        )


def test_equal_unions_with_different_arm_order_keep_their_coercion() -> None:
    integer_first = int | bool
    boolean_first = bool | int
    assert integer_first == boolean_first
    assert type(validate_union(integer_first, "1")) is int
    assert type(validate_union(boolean_first, "1")) is bool
    assert type(validate_union(integer_first, "1")) is int


def test_unhashable_annotation_metadata_can_still_be_validated() -> None:
    union = Annotated[int | str, {"description": "Caller metadata"}]
    with pytest.raises(TypeError):
        hash(union)
    assert validate_union(union, 1) == 1
    assert validate_union(union, "x") == "x"


def test_model_class_inputs_return_the_model_directly() -> None:
    result = validate_union(_First, {"kind": "first", "value": 3})
    assert isinstance(result, _First)
    assert result.value == 3
