import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatSession")


@_attrs_define
class ChatSession:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        user (Union[Unset, UUID]):
        user_username (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
    """

    uuid: Union[Unset, UUID] = UNSET
    user: Union[Unset, UUID] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_full_name: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        user: Union[Unset, str] = UNSET
        if not isinstance(self.user, Unset):
            user = str(self.user)

        user_username = self.user_username

        user_full_name = self.user_full_name

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if user is not UNSET:
            field_dict["user"] = user
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_full_name is not UNSET:
            field_dict["user_full_name"] = user_full_name
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _user = d.pop("user", UNSET)
        user: Union[Unset, UUID]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UUID(_user)

        user_username = d.pop("user_username", UNSET)

        user_full_name = d.pop("user_full_name", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        chat_session = cls(
            uuid=uuid,
            user=user,
            user_username=user_username,
            user_full_name=user_full_name,
            created=created,
            modified=modified,
        )

        chat_session.additional_properties = d
        return chat_session

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
