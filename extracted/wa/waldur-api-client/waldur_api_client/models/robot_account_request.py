from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RobotAccountRequest")


@_attrs_define
class RobotAccountRequest:
    """
    Attributes:
        resource (str):
        type_ (str): Type of the robot account.
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        users (Union[Unset, list[str]]): Users who have access to this robot account.
        keys (Union[Unset, Any]):
        responsible_user (Union[None, Unset, str]):
    """

    resource: str
    type_: str
    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    users: Union[Unset, list[str]] = UNSET
    keys: Union[Unset, Any] = UNSET
    responsible_user: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = self.resource

        type_ = self.type_

        username = self.username

        description = self.description

        users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users

        keys = self.keys

        responsible_user: Union[None, Unset, str]
        if isinstance(self.responsible_user, Unset):
            responsible_user = UNSET
        else:
            responsible_user = self.responsible_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource": resource,
                "type": type_,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if description is not UNSET:
            field_dict["description"] = description
        if users is not UNSET:
            field_dict["users"] = users
        if keys is not UNSET:
            field_dict["keys"] = keys
        if responsible_user is not UNSET:
            field_dict["responsible_user"] = responsible_user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource = d.pop("resource")

        type_ = d.pop("type")

        username = d.pop("username", UNSET)

        description = d.pop("description", UNSET)

        users = cast(list[str], d.pop("users", UNSET))

        keys = d.pop("keys", UNSET)

        def _parse_responsible_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        responsible_user = _parse_responsible_user(d.pop("responsible_user", UNSET))

        robot_account_request = cls(
            resource=resource,
            type_=type_,
            username=username,
            description=description,
            users=users,
            keys=keys,
            responsible_user=responsible_user,
        )

        robot_account_request.additional_properties = d
        return robot_account_request

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
