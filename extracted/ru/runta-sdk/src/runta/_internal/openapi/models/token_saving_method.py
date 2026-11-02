from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.token_saving_method_method import TokenSavingMethodMethod

T = TypeVar("T", bound="TokenSavingMethod")


@_attrs_define
class TokenSavingMethod:
    """
    Attributes:
        method (TokenSavingMethodMethod):
        blocks (int):
        input_units (int):
        output_units (int):
    """

    method: TokenSavingMethodMethod
    blocks: int
    input_units: int
    output_units: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method = self.method.value

        blocks = self.blocks

        input_units = self.input_units

        output_units = self.output_units

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method": method,
                "blocks": blocks,
                "input_units": input_units,
                "output_units": output_units,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method = TokenSavingMethodMethod(d.pop("method"))

        blocks = d.pop("blocks")

        input_units = d.pop("input_units")

        output_units = d.pop("output_units")

        token_saving_method = cls(
            method=method,
            blocks=blocks,
            input_units=input_units,
            output_units=output_units,
        )

        token_saving_method.additional_properties = d
        return token_saving_method

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
