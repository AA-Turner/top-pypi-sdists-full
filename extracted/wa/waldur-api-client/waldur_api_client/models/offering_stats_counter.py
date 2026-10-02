from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingStatsCounter")


@_attrs_define
class OfferingStatsCounter:
    """
    Attributes:
        category_uuid (UUID): UUID of the category
        category_title (str): Title of the category
        service_provider_name (str): Name of the service provider
        service_provider_uuid (UUID): UUID of the service provider
        count (int): Number of offerings
    """

    category_uuid: UUID
    category_title: str
    service_provider_name: str
    service_provider_uuid: UUID
    count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category_uuid = str(self.category_uuid)

        category_title = self.category_title

        service_provider_name = self.service_provider_name

        service_provider_uuid = str(self.service_provider_uuid)

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category_uuid": category_uuid,
                "category_title": category_title,
                "service_provider_name": service_provider_name,
                "service_provider_uuid": service_provider_uuid,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category_uuid = UUID(d.pop("category_uuid"))

        category_title = d.pop("category_title")

        service_provider_name = d.pop("service_provider_name")

        service_provider_uuid = UUID(d.pop("service_provider_uuid"))

        count = d.pop("count")

        offering_stats_counter = cls(
            category_uuid=category_uuid,
            category_title=category_title,
            service_provider_name=service_provider_name,
            service_provider_uuid=service_provider_uuid,
            count=count,
        )

        offering_stats_counter.additional_properties = d
        return offering_stats_counter

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
