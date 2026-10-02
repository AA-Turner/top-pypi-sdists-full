from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_placement_allocation_resources import InstancePlacementAllocationResources


T = TypeVar("T", bound="InstancePlacementAllocation")


@_attrs_define
class InstancePlacementAllocation:
    """
    Attributes:
        resource_provider_uuid (str):
        resource_provider_name (str):
        resources (InstancePlacementAllocationResources):
    """

    resource_provider_uuid: str
    resource_provider_name: str
    resources: "InstancePlacementAllocationResources"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_provider_uuid = self.resource_provider_uuid

        resource_provider_name = self.resource_provider_name

        resources = self.resources.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_provider_uuid": resource_provider_uuid,
                "resource_provider_name": resource_provider_name,
                "resources": resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_placement_allocation_resources import InstancePlacementAllocationResources

        d = dict(src_dict)
        resource_provider_uuid = d.pop("resource_provider_uuid")

        resource_provider_name = d.pop("resource_provider_name")

        resources = InstancePlacementAllocationResources.from_dict(d.pop("resources"))

        instance_placement_allocation = cls(
            resource_provider_uuid=resource_provider_uuid,
            resource_provider_name=resource_provider_name,
            resources=resources,
        )

        instance_placement_allocation.additional_properties = d
        return instance_placement_allocation

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
