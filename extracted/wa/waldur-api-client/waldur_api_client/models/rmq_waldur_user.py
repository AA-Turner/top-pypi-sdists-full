from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqWaldurUser")


@_attrs_define
class RmqWaldurUser:
    """
    Attributes:
        full_name (str):
        username (str):
        email (str):
    """

    full_name: str
    username: str
    email: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        username = self.username

        email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "username": username,
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        username = d.pop("username")

        email = d.pop("email")

        rmq_waldur_user = cls(
            full_name=full_name,
            username=username,
            email=email,
        )

        rmq_waldur_user.additional_properties = d
        return rmq_waldur_user

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
