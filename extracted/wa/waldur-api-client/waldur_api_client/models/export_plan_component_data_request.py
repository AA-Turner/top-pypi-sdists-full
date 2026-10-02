from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportPlanComponentDataRequest")


@_attrs_define
class ExportPlanComponentDataRequest:
    """
    Attributes:
        component_type (Union[None, str]):
        amount (int):
        price (float):
        future_price (Union[None, float]):
    """

    component_type: Union[None, str]
    amount: int
    price: float
    future_price: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_type: Union[None, str]
        component_type = self.component_type

        amount = self.amount

        price = self.price

        future_price: Union[None, float]
        future_price = self.future_price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component_type": component_type,
                "amount": amount,
                "price": price,
                "future_price": future_price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_component_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        component_type = _parse_component_type(d.pop("component_type"))

        amount = d.pop("amount")

        price = d.pop("price")

        def _parse_future_price(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        future_price = _parse_future_price(d.pop("future_price"))

        export_plan_component_data_request = cls(
            component_type=component_type,
            amount=amount,
            price=price,
            future_price=future_price,
        )

        export_plan_component_data_request.additional_properties = d
        return export_plan_component_data_request

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
