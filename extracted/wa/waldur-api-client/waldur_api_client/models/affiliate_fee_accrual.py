import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AffiliateFeeAccrual")


@_attrs_define
class AffiliateFeeAccrual:
    """
    Attributes:
        uuid (UUID):
        amount (str):
        customer_name (str):
        affiliate_uuid (UUID):
        invoice_year (int):
        invoice_month (int):
        created (datetime.datetime):
    """

    uuid: UUID
    amount: str
    customer_name: str
    affiliate_uuid: UUID
    invoice_year: int
    invoice_month: int
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        amount = self.amount

        customer_name = self.customer_name

        affiliate_uuid = str(self.affiliate_uuid)

        invoice_year = self.invoice_year

        invoice_month = self.invoice_month

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "amount": amount,
                "customer_name": customer_name,
                "affiliate_uuid": affiliate_uuid,
                "invoice_year": invoice_year,
                "invoice_month": invoice_month,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        amount = d.pop("amount")

        customer_name = d.pop("customer_name")

        affiliate_uuid = UUID(d.pop("affiliate_uuid"))

        invoice_year = d.pop("invoice_year")

        invoice_month = d.pop("invoice_month")

        created = isoparse(d.pop("created"))

        affiliate_fee_accrual = cls(
            uuid=uuid,
            amount=amount,
            customer_name=customer_name,
            affiliate_uuid=affiliate_uuid,
            invoice_year=invoice_year,
            invoice_month=invoice_month,
            created=created,
        )

        affiliate_fee_accrual.additional_properties = d
        return affiliate_fee_accrual

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
