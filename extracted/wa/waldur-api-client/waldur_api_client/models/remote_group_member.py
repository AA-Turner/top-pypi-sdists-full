from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RemoteGroupMember")


@_attrs_define
class RemoteGroupMember:
    """
    Attributes:
        id (str):
        username (str):
        email (str):
        first_name (str):
        last_name (str):
    """

    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        username = self.username

        email = self.email

        first_name = self.first_name

        last_name = self.last_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        username = d.pop("username")

        email = d.pop("email")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        remote_group_member = cls(
            id=id,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        remote_group_member.additional_properties = d
        return remote_group_member

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
