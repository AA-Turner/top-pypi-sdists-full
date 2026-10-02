from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrganizationalUser")


@_attrs_define
class OrganizationalUser:
    """
    Attributes:
        user_uuid (UUID):
        username (str):
        full_name (str):
        role (Union[None, str]):
    """

    user_uuid: UUID
    username: str
    full_name: str
    role: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uuid = str(self.user_uuid)

        username = self.username

        full_name = self.full_name

        role: Union[None, str]
        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_uuid": user_uuid,
                "username": username,
                "full_name": full_name,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_uuid = UUID(d.pop("user_uuid"))

        username = d.pop("username")

        full_name = d.pop("full_name")

        def _parse_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role = _parse_role(d.pop("role"))

        organizational_user = cls(
            user_uuid=user_uuid,
            username=username,
            full_name=full_name,
            role=role,
        )

        organizational_user.additional_properties = d
        return organizational_user

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
