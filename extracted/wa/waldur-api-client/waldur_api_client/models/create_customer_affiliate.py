import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCustomerAffiliate")


@_attrs_define
class CreateCustomerAffiliate:
    """
    Attributes:
        uuid (UUID):
        url (str):
        customer (str):
        customer_name (str):
        customer_uuid (UUID):
        affiliate (str):
        affiliate_name (str):
        affiliate_uuid (UUID):
        total_earned (float):
        created (datetime.datetime):
        fee_percent (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
    """

    uuid: UUID
    url: str
    customer: str
    customer_name: str
    customer_uuid: UUID
    affiliate: str
    affiliate_name: str
    affiliate_uuid: UUID
    total_earned: float
    created: datetime.datetime
    fee_percent: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    start_date: Union[None, Unset, datetime.date] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        customer = self.customer

        customer_name = self.customer_name

        customer_uuid = str(self.customer_uuid)

        affiliate = self.affiliate

        affiliate_name = self.affiliate_name

        affiliate_uuid = str(self.affiliate_uuid)

        total_earned = self.total_earned

        created = self.created.isoformat()

        fee_percent = self.fee_percent

        is_active = self.is_active

        start_date: Union[None, Unset, str]
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "customer": customer,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "affiliate": affiliate,
                "affiliate_name": affiliate_name,
                "affiliate_uuid": affiliate_uuid,
                "total_earned": total_earned,
                "created": created,
            }
        )
        if fee_percent is not UNSET:
            field_dict["fee_percent"] = fee_percent
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        customer = d.pop("customer")

        customer_name = d.pop("customer_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        affiliate = d.pop("affiliate")

        affiliate_name = d.pop("affiliate_name")

        affiliate_uuid = UUID(d.pop("affiliate_uuid"))

        total_earned = d.pop("total_earned")

        created = isoparse(d.pop("created"))

        fee_percent = d.pop("fee_percent", UNSET)

        is_active = d.pop("is_active", UNSET)

        def _parse_start_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        create_customer_affiliate = cls(
            uuid=uuid,
            url=url,
            customer=customer,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            affiliate=affiliate,
            affiliate_name=affiliate_name,
            affiliate_uuid=affiliate_uuid,
            total_earned=total_earned,
            created=created,
            fee_percent=fee_percent,
            is_active=is_active,
            start_date=start_date,
            end_date=end_date,
        )

        create_customer_affiliate.additional_properties = d
        return create_customer_affiliate

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
