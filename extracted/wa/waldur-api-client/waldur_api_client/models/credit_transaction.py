import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
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
        customer_uuid (Union[None, UUID]):
        customer_name (Union[None, str]):
        comment (Union[Unset, str]):
        project_uuid (Union[Unset, str]):
        project_name (Union[Unset, str]):
        billing_period (Union[None, Unset, datetime.date]):
    """

    uuid: UUID
    created: datetime.datetime
    amount: str
    transaction_type: TransactionTypeEnum
    transaction_type_display: str
    customer_uuid: Union[None, UUID]
    customer_name: Union[None, str]
    comment: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, str] = UNSET
    project_name: Union[Unset, str] = UNSET
    billing_period: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        amount = self.amount

        transaction_type = self.transaction_type.value

        transaction_type_display = self.transaction_type_display

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        comment = self.comment

        project_uuid = self.project_uuid

        project_name = self.project_name

        billing_period: Union[None, Unset, str]
        if isinstance(self.billing_period, Unset):
            billing_period = UNSET
        elif isinstance(self.billing_period, datetime.date):
            billing_period = self.billing_period.isoformat()
        else:
            billing_period = self.billing_period

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
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        amount = d.pop("amount")

        transaction_type = TransactionTypeEnum(d.pop("transaction_type"))

        transaction_type_display = d.pop("transaction_type_display")

        def _parse_customer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        comment = d.pop("comment", UNSET)

        project_uuid = d.pop("project_uuid", UNSET)

        project_name = d.pop("project_name", UNSET)

        def _parse_billing_period(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                billing_period_type_0 = isoparse(data).date()

                return billing_period_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        billing_period = _parse_billing_period(d.pop("billing_period", UNSET))

        credit_transaction = cls(
            uuid=uuid,
            created=created,
            amount=amount,
            transaction_type=transaction_type,
            transaction_type_display=transaction_type_display,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            comment=comment,
            project_uuid=project_uuid,
            project_name=project_name,
            billing_period=billing_period,
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
