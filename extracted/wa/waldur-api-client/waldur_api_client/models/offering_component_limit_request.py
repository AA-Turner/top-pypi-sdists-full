from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingComponentLimitRequest")


@_attrs_define
class OfferingComponentLimitRequest:
    """
    Attributes:
        min_ (int): Minimum allowed value
        max_ (int): Maximum allowed value
        max_available_limit (int): Maximum available limit across all resources
    """

    min_: int
    max_: int
    max_available_limit: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_ = self.min_

        max_ = self.max_

        max_available_limit = self.max_available_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min": min_,
                "max": max_,
                "max_available_limit": max_available_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_ = d.pop("min")

        max_ = d.pop("max")

        max_available_limit = d.pop("max_available_limit")

        offering_component_limit_request = cls(
            min_=min_,
            max_=max_,
            max_available_limit=max_available_limit,
        )

        offering_component_limit_request.additional_properties = d
        return offering_component_limit_request

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
