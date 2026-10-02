from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Association")


@_attrs_define
class Association:
    """
    Attributes:
        uuid (UUID):
        allocation (str):
        username (Union[None, Unset, str]):
        groupname (Union[None, Unset, str]):
        useridentifier (Union[None, Unset, str]):
    """

    uuid: UUID
    allocation: str
    username: Union[None, Unset, str] = UNSET
    groupname: Union[None, Unset, str] = UNSET
    useridentifier: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        allocation = self.allocation

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        groupname: Union[None, Unset, str]
        if isinstance(self.groupname, Unset):
            groupname = UNSET
        else:
            groupname = self.groupname

        useridentifier: Union[None, Unset, str]
        if isinstance(self.useridentifier, Unset):
            useridentifier = UNSET
        else:
            useridentifier = self.useridentifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "allocation": allocation,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if groupname is not UNSET:
            field_dict["groupname"] = groupname
        if useridentifier is not UNSET:
            field_dict["useridentifier"] = useridentifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        allocation = d.pop("allocation")

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_groupname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        groupname = _parse_groupname(d.pop("groupname", UNSET))

        def _parse_useridentifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        useridentifier = _parse_useridentifier(d.pop("useridentifier", UNSET))

        association = cls(
            uuid=uuid,
            allocation=allocation,
            username=username,
            groupname=groupname,
            useridentifier=useridentifier,
        )

        association.additional_properties = d
        return association

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
