from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InvoiceStatsOffering")


@_attrs_define
class InvoiceStatsOffering:
    """
    Attributes:
        offering_name (str):
        aggregated_price (float):
        aggregated_tax (float):
        aggregated_total (float):
        service_category_title (str):
        service_provider_name (str):
        service_provider_uuid (UUID):
    """

    offering_name: str
    aggregated_price: float
    aggregated_tax: float
    aggregated_total: float
    service_category_title: str
    service_provider_name: str
    service_provider_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_name = self.offering_name

        aggregated_price = self.aggregated_price

        aggregated_tax = self.aggregated_tax

        aggregated_total = self.aggregated_total

        service_category_title = self.service_category_title

        service_provider_name = self.service_provider_name

        service_provider_uuid = str(self.service_provider_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_name": offering_name,
                "aggregated_price": aggregated_price,
                "aggregated_tax": aggregated_tax,
                "aggregated_total": aggregated_total,
                "service_category_title": service_category_title,
                "service_provider_name": service_provider_name,
                "service_provider_uuid": service_provider_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_name = d.pop("offering_name")

        aggregated_price = d.pop("aggregated_price")

        aggregated_tax = d.pop("aggregated_tax")

        aggregated_total = d.pop("aggregated_total")

        service_category_title = d.pop("service_category_title")

        service_provider_name = d.pop("service_provider_name")

        service_provider_uuid = UUID(d.pop("service_provider_uuid"))

        invoice_stats_offering = cls(
            offering_name=offering_name,
            aggregated_price=aggregated_price,
            aggregated_tax=aggregated_tax,
            aggregated_total=aggregated_total,
            service_category_title=service_category_title,
            service_provider_name=service_provider_name,
            service_provider_uuid=service_provider_uuid,
        )

        invoice_stats_offering.additional_properties = d
        return invoice_stats_offering

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
