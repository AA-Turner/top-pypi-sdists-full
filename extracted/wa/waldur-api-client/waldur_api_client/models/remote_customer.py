from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RemoteCustomer")


@_attrs_define
class RemoteCustomer:
    """
    Attributes:
        uuid (UUID):
        name (str):
        abbreviation (str):
        phone_number (str):
        email (str):
    """

    uuid: UUID
    name: str
    abbreviation: str
    phone_number: str
    email: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        abbreviation = self.abbreviation

        phone_number = self.phone_number

        email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "abbreviation": abbreviation,
                "phone_number": phone_number,
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        abbreviation = d.pop("abbreviation")

        phone_number = d.pop("phone_number")

        email = d.pop("email")

        remote_customer = cls(
            uuid=uuid,
            name=name,
            abbreviation=abbreviation,
            phone_number=phone_number,
            email=email,
        )

        remote_customer.additional_properties = d
        return remote_customer

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
