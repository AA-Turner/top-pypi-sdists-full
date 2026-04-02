from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CountUsersOfServiceProviders")


@_attrs_define
class CountUsersOfServiceProviders:
    """
    Attributes:
        service_provider_uuid (UUID): UUID of the service provider
        customer_uuid (UUID): UUID of the customer
        customer_name (str): Name of the customer
        customer_organization_group_uuid (str): UUID of the customer's organization group
        customer_organization_group_name (str): Name of the customer's organization group
        count (int): Count value
    """

    service_provider_uuid: UUID
    customer_uuid: UUID
    customer_name: str
    customer_organization_group_uuid: str
    customer_organization_group_name: str
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_provider_uuid = str(self.service_provider_uuid)

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_organization_group_uuid = self.customer_organization_group_uuid

        customer_organization_group_name = self.customer_organization_group_name

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_provider_uuid": service_provider_uuid,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "customer_organization_group_uuid": customer_organization_group_uuid,
                "customer_organization_group_name": customer_organization_group_name,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_provider_uuid = UUID(d.pop("service_provider_uuid"))

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        customer_organization_group_uuid = d.pop("customer_organization_group_uuid")

        customer_organization_group_name = d.pop("customer_organization_group_name")

        count = d.pop("count")

        count_users_of_service_providers = cls(
            service_provider_uuid=service_provider_uuid,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_organization_group_uuid=customer_organization_group_uuid,
            customer_organization_group_name=customer_organization_group_name,
            count=count,
        )

        count_users_of_service_providers.additional_properties = d
        return count_users_of_service_providers

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
