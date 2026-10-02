from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.organizational_user import OrganizationalUser


T = TypeVar("T", bound="OrganizationalAccess")


@_attrs_define
class OrganizationalAccess:
    """
    Attributes:
        scope_type (str):
        scope_uuid (UUID):
        scope_name (str):
        users (list['OrganizationalUser']):
    """

    scope_type: str
    scope_uuid: UUID
    scope_name: str
    users: list["OrganizationalUser"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope_type = self.scope_type

        scope_uuid = str(self.scope_uuid)

        scope_name = self.scope_name

        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()
            users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope_type": scope_type,
                "scope_uuid": scope_uuid,
                "scope_name": scope_name,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organizational_user import OrganizationalUser

        d = dict(src_dict)
        scope_type = d.pop("scope_type")

        scope_uuid = UUID(d.pop("scope_uuid"))

        scope_name = d.pop("scope_name")

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = OrganizationalUser.from_dict(users_item_data)

            users.append(users_item)

        organizational_access = cls(
            scope_type=scope_type,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            users=users,
        )

        organizational_access.additional_properties = d
        return organizational_access

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
