from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_state_counter import OfferingStateCounter


T = TypeVar("T", bound="OfferingStateCounters")


@_attrs_define
class OfferingStateCounters:
    """
    Attributes:
        resources (list['OfferingStateCounter']):
        users (list['OfferingStateCounter']):
    """

    resources: list["OfferingStateCounter"]
    users: list["OfferingStateCounter"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()
            resources.append(resources_item)

        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()
            users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resources": resources,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_state_counter import OfferingStateCounter

        d = dict(src_dict)
        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = OfferingStateCounter.from_dict(resources_item_data)

            resources.append(resources_item)

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = OfferingStateCounter.from_dict(users_item_data)

            users.append(users_item)

        offering_state_counters = cls(
            resources=resources,
            users=users,
        )

        offering_state_counters.additional_properties = d
        return offering_state_counters

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
