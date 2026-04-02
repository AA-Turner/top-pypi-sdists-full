from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerContactUpdate")


@_attrs_define
class CustomerContactUpdate:
    """
    Attributes:
        contact_details (Union[Unset, str]):
        email (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        homepage (Union[Unset, str]):
        notification_emails (Union[Unset, str]): Comma-separated list of notification email addresses
    """

    contact_details: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    homepage: Union[Unset, str] = UNSET
    notification_emails: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        contact_details = self.contact_details

        email = self.email

        phone_number = self.phone_number

        homepage = self.homepage

        notification_emails = self.notification_emails

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if contact_details is not UNSET:
            field_dict["contact_details"] = contact_details
        if email is not UNSET:
            field_dict["email"] = email
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if homepage is not UNSET:
            field_dict["homepage"] = homepage
        if notification_emails is not UNSET:
            field_dict["notification_emails"] = notification_emails

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        contact_details = d.pop("contact_details", UNSET)

        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        homepage = d.pop("homepage", UNSET)

        notification_emails = d.pop("notification_emails", UNSET)

        customer_contact_update = cls(
            contact_details=contact_details,
            email=email,
            phone_number=phone_number,
            homepage=homepage,
            notification_emails=notification_emails,
        )

        customer_contact_update.additional_properties = d
        return customer_contact_update

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
