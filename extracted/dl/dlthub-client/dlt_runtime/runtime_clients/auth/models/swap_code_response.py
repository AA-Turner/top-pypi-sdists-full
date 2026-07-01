from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SwapCodeResponse")


@_attrs_define
class SwapCodeResponse:
    """
    Attributes:
        expires_in (int):
        swap_code (str):
    """

    expires_in: int
    swap_code: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expires_in = self.expires_in

        swap_code = self.swap_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_in": expires_in,
                "swap_code": swap_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expires_in = d.pop("expires_in")

        swap_code = d.pop("swap_code")

        swap_code_response = cls(
            expires_in=expires_in,
            swap_code=swap_code,
        )

        swap_code_response.additional_properties = d
        return swap_code_response

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
