from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceUsageByOrgType")


@_attrs_define
class ResourceUsageByOrgType:
    """
    Attributes:
        organization_type (Union[None, str]): SCHAC organization type URN
        component_type (str): Component type (e.g., cpu, gpu)
        usage (str): Total usage for this component
        resource_count (int): Number of resources
    """

    organization_type: Union[None, str]
    component_type: str
    usage: str
    resource_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization_type: Union[None, str]
        organization_type = self.organization_type

        component_type = self.component_type

        usage = self.usage

        resource_count = self.resource_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_type": organization_type,
                "component_type": component_type,
                "usage": usage,
                "resource_count": resource_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_organization_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        organization_type = _parse_organization_type(d.pop("organization_type"))

        component_type = d.pop("component_type")

        usage = d.pop("usage")

        resource_count = d.pop("resource_count")

        resource_usage_by_org_type = cls(
            organization_type=organization_type,
            component_type=component_type,
            usage=usage,
            resource_count=resource_count,
        )

        resource_usage_by_org_type.additional_properties = d
        return resource_usage_by_org_type

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
