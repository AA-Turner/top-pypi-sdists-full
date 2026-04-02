from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRobotAccountRequest")


@_attrs_define
class PatchedRobotAccountRequest:
    """
    Attributes:
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        resource (Union[Unset, str]):
        type_ (Union[Unset, str]): Type of the robot account.
        users (Union[Unset, list[str]]): Users who have access to this robot account.
        keys (Union[Unset, Any]):
        responsible_user (Union[None, Unset, str]):
    """

    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    resource: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    users: Union[Unset, list[str]] = UNSET
    keys: Union[Unset, Any] = UNSET
    responsible_user: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        description = self.description

        resource = self.resource

        type_ = self.type_

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
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if description is not UNSET:
            field_dict["description"] = description
        if resource is not UNSET:
            field_dict["resource"] = resource
        if type_ is not UNSET:
            field_dict["type"] = type_
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
        username = d.pop("username", UNSET)

        description = d.pop("description", UNSET)

        resource = d.pop("resource", UNSET)

        type_ = d.pop("type", UNSET)

        users = cast(list[str], d.pop("users", UNSET))

        keys = d.pop("keys", UNSET)

        def _parse_responsible_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        responsible_user = _parse_responsible_user(d.pop("responsible_user", UNSET))

        patched_robot_account_request = cls(
            username=username,
            description=description,
            resource=resource,
            type_=type_,
            users=users,
            keys=keys,
            responsible_user=responsible_user,
        )

        patched_robot_account_request.additional_properties = d
        return patched_robot_account_request

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
