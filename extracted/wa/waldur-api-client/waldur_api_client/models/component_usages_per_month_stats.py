from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ComponentUsagesPerMonthStats")


@_attrs_define
class ComponentUsagesPerMonthStats:
    """
    Attributes:
        usage (str): Total usage amount
        offering_uuid (UUID): UUID of the offering
        component_type (str): Type of the component
        offering_country (str): Country of the offering
        organization_group_name (str): Name of the organization group
        organization_group_uuid (str): UUID of the organization group
        month (int): Month of the billing period
        year (int): Year of the billing period
    """

    usage: str
    offering_uuid: UUID
    component_type: str
    offering_country: str
    organization_group_name: str
    organization_group_uuid: str
    month: int
    year: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usage = self.usage

        offering_uuid = str(self.offering_uuid)

        component_type = self.component_type

        offering_country = self.offering_country

        organization_group_name = self.organization_group_name

        organization_group_uuid = self.organization_group_uuid

        month = self.month

        year = self.year

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usage": usage,
                "offering_uuid": offering_uuid,
                "component_type": component_type,
                "offering_country": offering_country,
                "organization_group_name": organization_group_name,
                "organization_group_uuid": organization_group_uuid,
                "month": month,
                "year": year,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        usage = d.pop("usage")

        offering_uuid = UUID(d.pop("offering_uuid"))

        component_type = d.pop("component_type")

        offering_country = d.pop("offering_country")

        organization_group_name = d.pop("organization_group_name")

        organization_group_uuid = d.pop("organization_group_uuid")

        month = d.pop("month")

        year = d.pop("year")

        component_usages_per_month_stats = cls(
            usage=usage,
            offering_uuid=offering_uuid,
            component_type=component_type,
            offering_country=offering_country,
            organization_group_name=organization_group_name,
            organization_group_uuid=organization_group_uuid,
            month=month,
            year=year,
        )

        component_usages_per_month_stats.additional_properties = d
        return component_usages_per_month_stats

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
