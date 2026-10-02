import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Payment")


@_attrs_define
class Payment:
    """
    Attributes:
        uuid (UUID):
        url (str):
        profile (str):
        date_of_payment (datetime.date):
        invoice (str):
        invoice_uuid (UUID):
        invoice_period (Union[None, str]):
        customer_uuid (UUID):
        sum_ (Union[Unset, str]):
        proof (Union[None, Unset, str]):
    """

    uuid: UUID
    url: str
    profile: str
    date_of_payment: datetime.date
    invoice: str
    invoice_uuid: UUID
    invoice_period: Union[None, str]
    customer_uuid: UUID
    sum_: Union[Unset, str] = UNSET
    proof: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        profile = self.profile

        date_of_payment = self.date_of_payment.isoformat()

        invoice = self.invoice

        invoice_uuid = str(self.invoice_uuid)

        invoice_period: Union[None, str]
        invoice_period = self.invoice_period

        customer_uuid = str(self.customer_uuid)

        sum_ = self.sum_

        proof: Union[None, Unset, str]
        if isinstance(self.proof, Unset):
            proof = UNSET
        else:
            proof = self.proof

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "profile": profile,
                "date_of_payment": date_of_payment,
                "invoice": invoice,
                "invoice_uuid": invoice_uuid,
                "invoice_period": invoice_period,
                "customer_uuid": customer_uuid,
            }
        )
        if sum_ is not UNSET:
            field_dict["sum"] = sum_
        if proof is not UNSET:
            field_dict["proof"] = proof

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        profile = d.pop("profile")

        date_of_payment = isoparse(d.pop("date_of_payment")).date()

        invoice = d.pop("invoice")

        invoice_uuid = UUID(d.pop("invoice_uuid"))

        def _parse_invoice_period(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        invoice_period = _parse_invoice_period(d.pop("invoice_period"))

        customer_uuid = UUID(d.pop("customer_uuid"))

        sum_ = d.pop("sum", UNSET)

        def _parse_proof(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        proof = _parse_proof(d.pop("proof", UNSET))

        payment = cls(
            uuid=uuid,
            url=url,
            profile=profile,
            date_of_payment=date_of_payment,
            invoice=invoice,
            invoice_uuid=invoice_uuid,
            invoice_period=invoice_period,
            customer_uuid=customer_uuid,
            sum_=sum_,
            proof=proof,
        )

        payment.additional_properties = d
        return payment

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
