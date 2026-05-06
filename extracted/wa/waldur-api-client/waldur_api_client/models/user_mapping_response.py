from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserMappingResponse")


@_attrs_define
class UserMappingResponse:
    """
    Attributes:
        uuid (str):
        full_name (str):
        email (str):
        username (str):
    """

    uuid: str
    full_name: str
    email: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        full_name = self.full_name

        email = self.email

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "full_name": full_name,
                "email": email,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        full_name = d.pop("full_name")

        email = d.pop("email")

        username = d.pop("username")

        user_mapping_response = cls(
            uuid=uuid,
            full_name=full_name,
            email=email,
            username=username,
        )

        user_mapping_response.additional_properties = d
        return user_mapping_response

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
