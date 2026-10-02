from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServiceProviderRevenues")


@_attrs_define
class ServiceProviderRevenues:
    """
    Attributes:
        total (int): Total revenue amount
        year (int): Invoice year
        month (int): Invoice month
    """

    total: int
    year: int
    month: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        year = self.year

        month = self.month

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "year": year,
                "month": month,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total")

        year = d.pop("year")

        month = d.pop("month")

        service_provider_revenues = cls(
            total=total,
            year=year,
            month=month,
        )

        service_provider_revenues.additional_properties = d
        return service_provider_revenues

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
