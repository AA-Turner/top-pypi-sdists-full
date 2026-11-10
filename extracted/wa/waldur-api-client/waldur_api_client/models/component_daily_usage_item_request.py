import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ComponentDailyUsageItemRequest")


@_attrs_define
class ComponentDailyUsageItemRequest:
    """
    Attributes:
        type_ (str): Type of the usage-based component
        date (datetime.date): UTC date the amount was used on
        amount (str): Usage on that date. Replaces the amount reported for it before.
    """

    type_: str
    date: datetime.date
    amount: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        date = self.date.isoformat()

        amount = self.amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "date": date,
                "amount": amount,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        date = isoparse(d.pop("date")).date()

        amount = d.pop("amount")

        component_daily_usage_item_request = cls(
            type_=type_,
            date=date,
            amount=amount,
        )

        component_daily_usage_item_request.additional_properties = d
        return component_daily_usage_item_request

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
