from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ArrowBillingLine")


@_attrs_define
class ArrowBillingLine:
    """
    Attributes:
        vendor_name (str):
        subscription_reference (str):
        license_reference (str): Arrow license reference. Used to fetch consumption data.
        offer_sku (str):
        classification (str):
        quantity (Union[None, str]):
        sell_price (Union[None, str]):
        buy_price (Union[None, str]):
    """

    vendor_name: str
    subscription_reference: str
    license_reference: str
    offer_sku: str
    classification: str
    quantity: Union[None, str]
    sell_price: Union[None, str]
    buy_price: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vendor_name = self.vendor_name

        subscription_reference = self.subscription_reference

        license_reference = self.license_reference

        offer_sku = self.offer_sku

        classification = self.classification

        quantity: Union[None, str]
        quantity = self.quantity

        sell_price: Union[None, str]
        sell_price = self.sell_price

        buy_price: Union[None, str]
        buy_price = self.buy_price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vendor_name": vendor_name,
                "subscription_reference": subscription_reference,
                "license_reference": license_reference,
                "offer_sku": offer_sku,
                "classification": classification,
                "quantity": quantity,
                "sell_price": sell_price,
                "buy_price": buy_price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vendor_name = d.pop("vendor_name")

        subscription_reference = d.pop("subscription_reference")

        license_reference = d.pop("license_reference")

        offer_sku = d.pop("offer_sku")

        classification = d.pop("classification")

        def _parse_quantity(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        quantity = _parse_quantity(d.pop("quantity"))

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

        arrow_billing_line = cls(
            vendor_name=vendor_name,
            subscription_reference=subscription_reference,
            license_reference=license_reference,
            offer_sku=offer_sku,
            classification=classification,
            quantity=quantity,
            sell_price=sell_price,
            buy_price=buy_price,
        )

        arrow_billing_line.additional_properties = d
        return arrow_billing_line

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
