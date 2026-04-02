from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CountUniqueUsersConnectedWithActiveResourcesOfServiceProvider")


@_attrs_define
class CountUniqueUsersConnectedWithActiveResourcesOfServiceProvider:
    """
    Attributes:
        customer_uuid (UUID): UUID of the customer
        customer_name (str): Name of the customer
        count_users (int): Number of unique users
    """

    customer_uuid: UUID
    customer_name: str
    count_users: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        count_users = self.count_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "count_users": count_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        count_users = d.pop("count_users")

        count_unique_users_connected_with_active_resources_of_service_provider = cls(
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            count_users=count_users,
        )

        count_unique_users_connected_with_active_resources_of_service_provider.additional_properties = d
        return count_unique_users_connected_with_active_resources_of_service_provider

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
