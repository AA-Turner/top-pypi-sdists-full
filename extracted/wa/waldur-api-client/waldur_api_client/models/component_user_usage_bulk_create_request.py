from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.component_user_usage_create_request import ComponentUserUsageCreateRequest


T = TypeVar("T", bound="ComponentUserUsageBulkCreateRequest")


@_attrs_define
class ComponentUserUsageBulkCreateRequest:
    """
    Attributes:
        usages (list['ComponentUserUsageCreateRequest']):
    """

    usages: list["ComponentUserUsageCreateRequest"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usages = []
        for usages_item_data in self.usages:
            usages_item = usages_item_data.to_dict()
            usages.append(usages_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usages": usages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.component_user_usage_create_request import ComponentUserUsageCreateRequest

        d = dict(src_dict)
        usages = []
        _usages = d.pop("usages")
        for usages_item_data in _usages:
            usages_item = ComponentUserUsageCreateRequest.from_dict(usages_item_data)

            usages.append(usages_item)

        component_user_usage_bulk_create_request = cls(
            usages=usages,
        )

        component_user_usage_bulk_create_request.additional_properties = d
        return component_user_usage_bulk_create_request

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
