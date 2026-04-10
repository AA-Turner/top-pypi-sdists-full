from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TopServiceProviderByResources")


@_attrs_define
class TopServiceProviderByResources:
    """
    Attributes:
        customer_uuid (UUID): UUID of the service provider
        customer_name (str): Name of the service provider
        resources_count (int): Number of active resources
        projects_count (int): Number of distinct projects
    """

    customer_uuid: UUID
    customer_name: str
    resources_count: int
    projects_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        resources_count = self.resources_count

        projects_count = self.projects_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "resources_count": resources_count,
                "projects_count": projects_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        resources_count = d.pop("resources_count")

        projects_count = d.pop("projects_count")

        top_service_provider_by_resources = cls(
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            resources_count=resources_count,
            projects_count=projects_count,
        )

        top_service_provider_by_resources.additional_properties = d
        return top_service_provider_by_resources

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
