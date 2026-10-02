import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.transaction_type_enum import TransactionTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreditTransaction")


@_attrs_define
class CreditTransaction:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        amount (str):
        transaction_type (TransactionTypeEnum):
        transaction_type_display (str):
        customer_uuid (UUID):
        customer_name (str):
        comment (Union[Unset, str]):
    """

    uuid: UUID
    created: datetime.datetime
    amount: str
    transaction_type: TransactionTypeEnum
    transaction_type_display: str
    customer_uuid: UUID
    customer_name: str
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        amount = self.amount

        transaction_type = self.transaction_type.value

        transaction_type_display = self.transaction_type_display

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "amount": amount,
                "transaction_type": transaction_type,
                "transaction_type_display": transaction_type_display,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        amount = d.pop("amount")

        transaction_type = TransactionTypeEnum(d.pop("transaction_type"))

        transaction_type_display = d.pop("transaction_type_display")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        comment = d.pop("comment", UNSET)

        credit_transaction = cls(
            uuid=uuid,
            created=created,
            amount=amount,
            transaction_type=transaction_type,
            transaction_type_display=transaction_type_display,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            comment=comment,
        )

        credit_transaction.additional_properties = d
        return credit_transaction

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
