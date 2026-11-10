import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="EarlierInvoicePayment")


@_attrs_define
class EarlierInvoicePayment:
    """
    Attributes:
        period (datetime.date): The month the compensation pays.
        invoice_period (datetime.date): The month of the invoice the compensation is written on.
        invoice_uuid (Union[None, UUID]): That invoice; null in a dry run while the current month has no invoice yet.
        resource_name (Union[None, str]):
        resource_uuid (Union[None, UUID]):
        item_name (str): The cost item the compensation pays.
        amount (str):
    """

    period: datetime.date
    invoice_period: datetime.date
    invoice_uuid: Union[None, UUID]
    resource_name: Union[None, str]
    resource_uuid: Union[None, UUID]
    item_name: str
    amount: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period.isoformat()

        invoice_period = self.invoice_period.isoformat()

        invoice_uuid: Union[None, str]
        if isinstance(self.invoice_uuid, UUID):
            invoice_uuid = str(self.invoice_uuid)
        else:
            invoice_uuid = self.invoice_uuid

        resource_name: Union[None, str]
        resource_name = self.resource_name

        resource_uuid: Union[None, str]
        if isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        item_name = self.item_name

        amount = self.amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period": period,
                "invoice_period": invoice_period,
                "invoice_uuid": invoice_uuid,
                "resource_name": resource_name,
                "resource_uuid": resource_uuid,
                "item_name": item_name,
                "amount": amount,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = isoparse(d.pop("period")).date()

        invoice_period = isoparse(d.pop("invoice_period")).date()

        def _parse_invoice_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                invoice_uuid_type_0 = UUID(data)

                return invoice_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        invoice_uuid = _parse_invoice_uuid(d.pop("invoice_uuid"))

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        def _parse_resource_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid"))

        item_name = d.pop("item_name")

        amount = d.pop("amount")

        earlier_invoice_payment = cls(
            period=period,
            invoice_period=invoice_period,
            invoice_uuid=invoice_uuid,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            item_name=item_name,
            amount=amount,
        )

        earlier_invoice_payment.additional_properties = d
        return earlier_invoice_payment

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
