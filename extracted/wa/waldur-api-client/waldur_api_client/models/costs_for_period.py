import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CostsForPeriod")


@_attrs_define
class CostsForPeriod:
    """
    Attributes:
        total_price (str):
        start_date (datetime.date):
        end_date (datetime.date):
    """

    total_price: str
    start_date: datetime.date
    end_date: datetime.date
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_price = self.total_price

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_price": total_price,
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_price = d.pop("total_price")

        start_date = isoparse(d.pop("start_date")).date()

        end_date = isoparse(d.pop("end_date")).date()

        costs_for_period = cls(
            total_price=total_price,
            start_date=start_date,
            end_date=end_date,
        )

        costs_for_period.additional_properties = d
        return costs_for_period

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
