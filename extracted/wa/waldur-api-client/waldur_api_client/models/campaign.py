import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.discount_type_enum import DiscountTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.campaign_offering import CampaignOffering


T = TypeVar("T", bound="Campaign")


@_attrs_define
class Campaign:
    """
    Attributes:
        uuid (UUID):
        name (str):
        url (str):
        start_date (datetime.date): Starting from this date, the campaign is active.
        end_date (datetime.date): The last day the campaign is active.
        discount_type (DiscountTypeEnum):
        discount (int):
        state (str):
        service_provider (str):
        offerings (list['CampaignOffering']):
        coupon (Union[Unset, str]): If coupon is empty, campaign is available to all users.
        stock (Union[None, Unset, int]):
        description (Union[Unset, str]):
        months (Union[Unset, int]): How many months in a row should the related service (when activated) get special
            deal (0 for indefinitely until active)
        auto_apply (Union[Unset, bool]):
        required_offerings (Union[Unset, list[UUID]]):
    """

    uuid: UUID
    name: str
    url: str
    start_date: datetime.date
    end_date: datetime.date
    discount_type: DiscountTypeEnum
    discount: int
    state: str
    service_provider: str
    offerings: list["CampaignOffering"]
    coupon: Union[Unset, str] = UNSET
    stock: Union[None, Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    months: Union[Unset, int] = UNSET
    auto_apply: Union[Unset, bool] = UNSET
    required_offerings: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        url = self.url

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        discount_type = self.discount_type.value

        discount = self.discount

        state = self.state

        service_provider = self.service_provider

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        coupon = self.coupon

        stock: Union[None, Unset, int]
        if isinstance(self.stock, Unset):
            stock = UNSET
        else:
            stock = self.stock

        description = self.description

        months = self.months

        auto_apply = self.auto_apply

        required_offerings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.required_offerings, Unset):
            required_offerings = []
            for required_offerings_item_data in self.required_offerings:
                required_offerings_item = str(required_offerings_item_data)
                required_offerings.append(required_offerings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "url": url,
                "start_date": start_date,
                "end_date": end_date,
                "discount_type": discount_type,
                "discount": discount,
                "state": state,
                "service_provider": service_provider,
                "offerings": offerings,
            }
        )
        if coupon is not UNSET:
            field_dict["coupon"] = coupon
        if stock is not UNSET:
            field_dict["stock"] = stock
        if description is not UNSET:
            field_dict["description"] = description
        if months is not UNSET:
            field_dict["months"] = months
        if auto_apply is not UNSET:
            field_dict["auto_apply"] = auto_apply
        if required_offerings is not UNSET:
            field_dict["required_offerings"] = required_offerings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.campaign_offering import CampaignOffering

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        url = d.pop("url")

        start_date = isoparse(d.pop("start_date")).date()

        end_date = isoparse(d.pop("end_date")).date()

        discount_type = DiscountTypeEnum(d.pop("discount_type"))

        discount = d.pop("discount")

        state = d.pop("state")

        service_provider = d.pop("service_provider")

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = CampaignOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        coupon = d.pop("coupon", UNSET)

        def _parse_stock(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stock = _parse_stock(d.pop("stock", UNSET))

        description = d.pop("description", UNSET)

        months = d.pop("months", UNSET)

        auto_apply = d.pop("auto_apply", UNSET)

        required_offerings = []
        _required_offerings = d.pop("required_offerings", UNSET)
        for required_offerings_item_data in _required_offerings or []:
            required_offerings_item = UUID(required_offerings_item_data)

            required_offerings.append(required_offerings_item)

        campaign = cls(
            uuid=uuid,
            name=name,
            url=url,
            start_date=start_date,
            end_date=end_date,
            discount_type=discount_type,
            discount=discount,
            state=state,
            service_provider=service_provider,
            offerings=offerings,
            coupon=coupon,
            stock=stock,
            description=description,
            months=months,
            auto_apply=auto_apply,
            required_offerings=required_offerings,
        )

        campaign.additional_properties = d
        return campaign

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
