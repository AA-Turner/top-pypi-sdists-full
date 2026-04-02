from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourcesLimits")


@_attrs_define
class ResourcesLimits:
    """
    Attributes:
        offering_uuid (UUID): UUID of the offering
        name (str): Name of the limit
        value (int): Limit value
        offering_country (str): Country of the offering
        organization_group_name (str): Name of the organization group
        organization_group_uuid (str): UUID of the organization group
    """

    offering_uuid: UUID
    name: str
    value: int
    offering_country: str
    organization_group_name: str
    organization_group_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        name = self.name

        value = self.value

        offering_country = self.offering_country

        organization_group_name = self.organization_group_name

        organization_group_uuid = self.organization_group_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "name": name,
                "value": value,
                "offering_country": offering_country,
                "organization_group_name": organization_group_name,
                "organization_group_uuid": organization_group_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        name = d.pop("name")

        value = d.pop("value")

        offering_country = d.pop("offering_country")

        organization_group_name = d.pop("organization_group_name")

        organization_group_uuid = d.pop("organization_group_uuid")

        resources_limits = cls(
            offering_uuid=offering_uuid,
            name=name,
            value=value,
            offering_country=offering_country,
            organization_group_name=organization_group_name,
            organization_group_uuid=organization_group_uuid,
        )

        resources_limits.additional_properties = d
        return resources_limits

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
