import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.discount_type_enum import DiscountTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedCampaign")


@_attrs_define
class NestedCampaign:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]): Starting from this date, the campaign is active.
        end_date (Union[Unset, datetime.date]): The last day the campaign is active.
        discount_type (Union[Unset, DiscountTypeEnum]):
        discount (Union[Unset, int]):
        stock (Union[None, Unset, int]):
        description (Union[Unset, str]):
        months (Union[Unset, int]): How many months in a row should the related service (when activated) get special
            deal (0 for indefinitely until active)
        service_provider (Union[Unset, str]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, datetime.date] = UNSET
    discount_type: Union[Unset, DiscountTypeEnum] = UNSET
    discount: Union[Unset, int] = UNSET
    stock: Union[None, Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    months: Union[Unset, int] = UNSET
    service_provider: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        discount_type: Union[Unset, str] = UNSET
        if not isinstance(self.discount_type, Unset):
            discount_type = self.discount_type.value

        discount = self.discount

        stock: Union[None, Unset, int]
        if isinstance(self.stock, Unset):
            stock = UNSET
        else:
            stock = self.stock

        description = self.description

        months = self.months

        service_provider = self.service_provider

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if discount_type is not UNSET:
            field_dict["discount_type"] = discount_type
        if discount is not UNSET:
            field_dict["discount"] = discount
        if stock is not UNSET:
            field_dict["stock"] = stock
        if description is not UNSET:
            field_dict["description"] = description
        if months is not UNSET:
            field_dict["months"] = months
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        _start_date = d.pop("start_date", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        _end_date = d.pop("end_date", UNSET)
        end_date: Union[Unset, datetime.date]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()

        _discount_type = d.pop("discount_type", UNSET)
        discount_type: Union[Unset, DiscountTypeEnum]
        if isinstance(_discount_type, Unset):
            discount_type = UNSET
        else:
            discount_type = DiscountTypeEnum(_discount_type)

        discount = d.pop("discount", UNSET)

        def _parse_stock(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stock = _parse_stock(d.pop("stock", UNSET))

        description = d.pop("description", UNSET)

        months = d.pop("months", UNSET)

        service_provider = d.pop("service_provider", UNSET)

        nested_campaign = cls(
            uuid=uuid,
            name=name,
            start_date=start_date,
            end_date=end_date,
            discount_type=discount_type,
            discount=discount,
            stock=stock,
            description=description,
            months=months,
            service_provider=service_provider,
        )

        nested_campaign.additional_properties = d
        return nested_campaign

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
