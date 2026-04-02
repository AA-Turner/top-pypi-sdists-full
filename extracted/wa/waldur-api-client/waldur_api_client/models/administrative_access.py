from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_user import AdminUser


T = TypeVar("T", bound="AdministrativeAccess")


@_attrs_define
class AdministrativeAccess:
    """
    Attributes:
        description (str):
        staff_count (Union[Unset, int]):
        support_count (Union[Unset, int]):
        users (Union[Unset, list['AdminUser']]):
    """

    description: str
    staff_count: Union[Unset, int] = UNSET
    support_count: Union[Unset, int] = UNSET
    users: Union[Unset, list["AdminUser"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        staff_count = self.staff_count

        support_count = self.support_count

        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
            }
        )
        if staff_count is not UNSET:
            field_dict["staff_count"] = staff_count
        if support_count is not UNSET:
            field_dict["support_count"] = support_count
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_user import AdminUser

        d = dict(src_dict)
        description = d.pop("description")

        staff_count = d.pop("staff_count", UNSET)

        support_count = d.pop("support_count", UNSET)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = AdminUser.from_dict(users_item_data)

            users.append(users_item)

        administrative_access = cls(
            description=description,
            staff_count=staff_count,
            support_count=support_count,
            users=users,
        )

        administrative_access.additional_properties = d
        return administrative_access

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
