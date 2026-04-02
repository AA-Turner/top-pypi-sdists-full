from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentMultiplierConfig")


@_attrs_define
class ComponentMultiplierConfig:
    """
    Attributes:
        component_type (str):
        factor (int):
        min_limit (Union[Unset, int]):
        max_limit (Union[Unset, int]):
    """

    component_type: str
    factor: int
    min_limit: Union[Unset, int] = UNSET
    max_limit: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_type = self.component_type

        factor = self.factor

        min_limit = self.min_limit

        max_limit = self.max_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component_type": component_type,
                "factor": factor,
            }
        )
        if min_limit is not UNSET:
            field_dict["min_limit"] = min_limit
        if max_limit is not UNSET:
            field_dict["max_limit"] = max_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        component_type = d.pop("component_type")

        factor = d.pop("factor")

        min_limit = d.pop("min_limit", UNSET)

        max_limit = d.pop("max_limit", UNSET)

        component_multiplier_config = cls(
            component_type=component_type,
            factor=factor,
            min_limit=min_limit,
            max_limit=max_limit,
        )

        component_multiplier_config.additional_properties = d
        return component_multiplier_config

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
