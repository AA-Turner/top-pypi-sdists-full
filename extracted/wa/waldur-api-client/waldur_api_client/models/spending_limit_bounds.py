from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SpendingLimitBounds")


@_attrs_define
class SpendingLimitBounds:
    """
    Attributes:
        default (Union[None, Unset, float]): Amount the order form starts from; the customer may change or clear it.
        maximum (Union[None, Unset, float]): Highest limit a customer may set for this period.
    """

    default: Union[None, Unset, float] = UNSET
    maximum: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default: Union[None, Unset, float]
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        maximum: Union[None, Unset, float]
        if isinstance(self.maximum, Unset):
            maximum = UNSET
        else:
            maximum = self.maximum

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default is not UNSET:
            field_dict["default"] = default
        if maximum is not UNSET:
            field_dict["maximum"] = maximum

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_default(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        default = _parse_default(d.pop("default", UNSET))

        def _parse_maximum(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        maximum = _parse_maximum(d.pop("maximum", UNSET))

        spending_limit_bounds = cls(
            default=default,
            maximum=maximum,
        )

        spending_limit_bounds.additional_properties = d
        return spending_limit_bounds

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
