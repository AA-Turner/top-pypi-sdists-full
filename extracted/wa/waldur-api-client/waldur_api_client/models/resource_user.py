from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceUser")


@_attrs_define
class ResourceUser:
    """
    Attributes:
        uuid (UUID):
        resource (str):
        role (str):
        user (str):
        resource_uuid (UUID):
        role_uuid (UUID):
        user_uuid (UUID):
        resource_name (str):
        role_name (str):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_full_name (str):
    """

    uuid: UUID
    resource: str
    role: str
    user: str
    resource_uuid: UUID
    role_uuid: UUID
    user_uuid: UUID
    resource_name: str
    role_name: str
    user_username: str
    user_full_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        resource = self.resource

        role = self.role

        user = self.user

        resource_uuid = str(self.resource_uuid)

        role_uuid = str(self.role_uuid)

        user_uuid = str(self.user_uuid)

        resource_name = self.resource_name

        role_name = self.role_name

        user_username = self.user_username

        user_full_name = self.user_full_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource": resource,
                "role": role,
                "user": user,
                "resource_uuid": resource_uuid,
                "role_uuid": role_uuid,
                "user_uuid": user_uuid,
                "resource_name": resource_name,
                "role_name": role_name,
                "user_username": user_username,
                "user_full_name": user_full_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource = d.pop("resource")

        role = d.pop("role")

        user = d.pop("user")

        resource_uuid = UUID(d.pop("resource_uuid"))

        role_uuid = UUID(d.pop("role_uuid"))

        user_uuid = UUID(d.pop("user_uuid"))

        resource_name = d.pop("resource_name")

        role_name = d.pop("role_name")

        user_username = d.pop("user_username")

        user_full_name = d.pop("user_full_name")

        resource_user = cls(
            uuid=uuid,
            resource=resource,
            role=role,
            user=user,
            resource_uuid=resource_uuid,
            role_uuid=role_uuid,
            user_uuid=user_uuid,
            resource_name=resource_name,
            role_name=role_name,
            user_username=user_username,
            user_full_name=user_full_name,
        )

        resource_user.additional_properties = d
        return resource_user

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
