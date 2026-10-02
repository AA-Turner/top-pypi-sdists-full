import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.event_groups_enum import EventGroupsEnum
from ..models.event_types_enum import EventTypesEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailHook")


@_attrs_define
class EmailHook:
    """
    Attributes:
        url (str):
        uuid (UUID):
        author_uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        hook_type (str):
        author_fullname (str):
        author_username (str):
        author_email (str):
        email (str):
        is_active (Union[Unset, bool]):
        event_types (Union[Unset, list[EventTypesEnum]]):
        event_groups (Union[Unset, list[EventGroupsEnum]]):
    """

    url: str
    uuid: UUID
    author_uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    hook_type: str
    author_fullname: str
    author_username: str
    author_email: str
    email: str
    is_active: Union[Unset, bool] = UNSET
    event_types: Union[Unset, list[EventTypesEnum]] = UNSET
    event_groups: Union[Unset, list[EventGroupsEnum]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        author_uuid = str(self.author_uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        hook_type = self.hook_type

        author_fullname = self.author_fullname

        author_username = self.author_username

        author_email = self.author_email

        email = self.email

        is_active = self.is_active

        event_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_types, Unset):
            event_types = []
            for event_types_item_data in self.event_types:
                event_types_item = event_types_item_data.value
                event_types.append(event_types_item)

        event_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_groups, Unset):
            event_groups = []
            for event_groups_item_data in self.event_groups:
                event_groups_item = event_groups_item_data.value
                event_groups.append(event_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "author_uuid": author_uuid,
                "created": created,
                "modified": modified,
                "hook_type": hook_type,
                "author_fullname": author_fullname,
                "author_username": author_username,
                "author_email": author_email,
                "email": email,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if event_types is not UNSET:
            field_dict["event_types"] = event_types
        if event_groups is not UNSET:
            field_dict["event_groups"] = event_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        author_uuid = UUID(d.pop("author_uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        hook_type = d.pop("hook_type")

        author_fullname = d.pop("author_fullname")

        author_username = d.pop("author_username")

        author_email = d.pop("author_email")

        email = d.pop("email")

        is_active = d.pop("is_active", UNSET)

        event_types = []
        _event_types = d.pop("event_types", UNSET)
        for event_types_item_data in _event_types or []:
            event_types_item = EventTypesEnum(event_types_item_data)

            event_types.append(event_types_item)

        event_groups = []
        _event_groups = d.pop("event_groups", UNSET)
        for event_groups_item_data in _event_groups or []:
            event_groups_item = EventGroupsEnum(event_groups_item_data)

            event_groups.append(event_groups_item)

        email_hook = cls(
            url=url,
            uuid=uuid,
            author_uuid=author_uuid,
            created=created,
            modified=modified,
            hook_type=hook_type,
            author_fullname=author_fullname,
            author_username=author_username,
            author_email=author_email,
            email=email,
            is_active=is_active,
            event_types=event_types,
            event_groups=event_groups,
        )

        email_hook.additional_properties = d
        return email_hook

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
