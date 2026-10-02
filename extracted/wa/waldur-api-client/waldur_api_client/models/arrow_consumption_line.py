from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowConsumptionLine")


@_attrs_define
class ArrowConsumptionLine:
    """
    Attributes:
        license_reference (str): Arrow license reference (same as resource backend_id).
        resource_name (Union[None, str]):
        resource_uuid (Union[None, str]): UUID of the Waldur resource.
        period (str):
        sell_price (Union[None, str]):
        buy_price (Union[None, str]):
        error (Union[None, Unset, str]): Error message if fetch failed.
    """

    license_reference: str
    resource_name: Union[None, str]
    resource_uuid: Union[None, str]
    period: str
    sell_price: Union[None, str]
    buy_price: Union[None, str]
    error: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        license_reference = self.license_reference

        resource_name: Union[None, str]
        resource_name = self.resource_name

        resource_uuid: Union[None, str]
        resource_uuid = self.resource_uuid

        period = self.period

        sell_price: Union[None, str]
        sell_price = self.sell_price

        buy_price: Union[None, str]
        buy_price = self.buy_price

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "license_reference": license_reference,
                "resource_name": resource_name,
                "resource_uuid": resource_uuid,
                "period": period,
                "sell_price": sell_price,
                "buy_price": buy_price,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        license_reference = d.pop("license_reference")

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        def _parse_resource_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid"))

        period = d.pop("period")

        def _parse_sell_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sell_price = _parse_sell_price(d.pop("sell_price"))

        def _parse_buy_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        buy_price = _parse_buy_price(d.pop("buy_price"))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        arrow_consumption_line = cls(
            license_reference=license_reference,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            period=period,
            sell_price=sell_price,
            buy_price=buy_price,
            error=error,
        )

        arrow_consumption_line.additional_properties = d
        return arrow_consumption_line

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
