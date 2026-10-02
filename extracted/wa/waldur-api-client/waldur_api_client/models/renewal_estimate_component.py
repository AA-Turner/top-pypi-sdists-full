from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RenewalEstimateComponent")


@_attrs_define
class RenewalEstimateComponent:
    """
    Attributes:
        component_type (str):
        component_name (str):
        billing_type (str):
        billing_period (Union[None, str]):
        current_limit (int):
        new_limit (int):
        unit_price (str):
        measured_unit (str):
        period_description (str):
        total (str):
    """

    component_type: str
    component_name: str
    billing_type: str
    billing_period: Union[None, str]
    current_limit: int
    new_limit: int
    unit_price: str
    measured_unit: str
    period_description: str
    total: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_type = self.component_type

        component_name = self.component_name

        billing_type = self.billing_type

        billing_period: Union[None, str]
        billing_period = self.billing_period

        current_limit = self.current_limit

        new_limit = self.new_limit

        unit_price = self.unit_price

        measured_unit = self.measured_unit

        period_description = self.period_description

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component_type": component_type,
                "component_name": component_name,
                "billing_type": billing_type,
                "billing_period": billing_period,
                "current_limit": current_limit,
                "new_limit": new_limit,
                "unit_price": unit_price,
                "measured_unit": measured_unit,
                "period_description": period_description,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        component_type = d.pop("component_type")

        component_name = d.pop("component_name")

        billing_type = d.pop("billing_type")

        def _parse_billing_period(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        billing_period = _parse_billing_period(d.pop("billing_period"))

        current_limit = d.pop("current_limit")

        new_limit = d.pop("new_limit")

        unit_price = d.pop("unit_price")

        measured_unit = d.pop("measured_unit")

        period_description = d.pop("period_description")

        total = d.pop("total")

        renewal_estimate_component = cls(
            component_type=component_type,
            component_name=component_name,
            billing_type=billing_type,
            billing_period=billing_period,
            current_limit=current_limit,
            new_limit=new_limit,
            unit_price=unit_price,
            measured_unit=measured_unit,
            period_description=period_description,
            total=total,
        )

        renewal_estimate_component.additional_properties = d
        return renewal_estimate_component

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
