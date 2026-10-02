from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_recipient_customer import NotificationRecipientCustomer
    from ..models.notification_recipient_offering import NotificationRecipientOffering


T = TypeVar("T", bound="NotificationRecipient")


@_attrs_define
class NotificationRecipient:
    """
    Attributes:
        email (str):
        offerings (list['NotificationRecipientOffering']):
        customers (list['NotificationRecipientCustomer']):
        full_name (Union[None, Unset, str]):
    """

    email: str
    offerings: list["NotificationRecipientOffering"]
    customers: list["NotificationRecipientCustomer"]
    full_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        customers = []
        for customers_item_data in self.customers:
            customers_item = customers_item_data.to_dict()
            customers.append(customers_item)

        full_name: Union[None, Unset, str]
        if isinstance(self.full_name, Unset):
            full_name = UNSET
        else:
            full_name = self.full_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "offerings": offerings,
                "customers": customers,
            }
        )
        if full_name is not UNSET:
            field_dict["full_name"] = full_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_recipient_customer import NotificationRecipientCustomer
        from ..models.notification_recipient_offering import NotificationRecipientOffering

        d = dict(src_dict)
        email = d.pop("email")

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = NotificationRecipientOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        customers = []
        _customers = d.pop("customers")
        for customers_item_data in _customers:
            customers_item = NotificationRecipientCustomer.from_dict(customers_item_data)

            customers.append(customers_item)

        def _parse_full_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        full_name = _parse_full_name(d.pop("full_name", UNSET))

        notification_recipient = cls(
            email=email,
            offerings=offerings,
            customers=customers,
            full_name=full_name,
        )

        notification_recipient.additional_properties = d
        return notification_recipient

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
