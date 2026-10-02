from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingComponentStat")


@_attrs_define
class OfferingComponentStat:
    """
    Attributes:
        period (str):
        billing_period (str):
        date (str):
        usage (int):
        description (str):
        measured_unit (str):
        type_ (str):
        name (str):
    """

    period: str
    billing_period: str
    date: str
    usage: int
    description: str
    measured_unit: str
    type_: str
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        billing_period = self.billing_period

        date = self.date

        usage = self.usage

        description = self.description

        measured_unit = self.measured_unit

        type_ = self.type_

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "billing_period": billing_period,
                "date": date,
                "usage": usage,
                "description": description,
                "measured_unit": measured_unit,
                "type": type_,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        billing_period = d.pop("billing_period")

        date = d.pop("date")

        usage = d.pop("usage")

        description = d.pop("description")

        measured_unit = d.pop("measured_unit")

        type_ = d.pop("type")

        name = d.pop("name")

        offering_component_stat = cls(
            period=period,
            billing_period=billing_period,
            date=date,
            usage=usage,
            description=description,
            measured_unit=measured_unit,
            type_=type_,
            name=name,
        )

        offering_component_stat.additional_properties = d
        return offering_component_stat

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
