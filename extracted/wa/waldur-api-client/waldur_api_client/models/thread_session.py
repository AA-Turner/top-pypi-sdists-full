import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.injection_severity_enum import InjectionSeverityEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreadSession")


@_attrs_define
class ThreadSession:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        chat_session (Union[Unset, UUID]):
        flags (Union[Unset, Any]):
        is_archived (Union[Unset, bool]):
        message_count (Union[Unset, int]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        user_username (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    chat_session: Union[Unset, UUID] = UNSET
    flags: Union[Unset, Any] = UNSET
    is_archived: Union[Unset, bool] = UNSET
    message_count: Union[Unset, int] = UNSET
    is_flagged: Union[Unset, bool] = UNSET
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_full_name: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        chat_session: Union[Unset, str] = UNSET
        if not isinstance(self.chat_session, Unset):
            chat_session = str(self.chat_session)

        flags = self.flags

        is_archived = self.is_archived

        message_count = self.message_count

        is_flagged = self.is_flagged

        max_severity: Union[Unset, str] = UNSET
        if not isinstance(self.max_severity, Unset):
            max_severity = self.max_severity.value

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
        if name is not UNSET:
            field_dict["name"] = name
        if chat_session is not UNSET:
            field_dict["chat_session"] = chat_session
        if flags is not UNSET:
            field_dict["flags"] = flags
        if is_archived is not UNSET:
            field_dict["is_archived"] = is_archived
        if message_count is not UNSET:
            field_dict["message_count"] = message_count
        if is_flagged is not UNSET:
            field_dict["is_flagged"] = is_flagged
        if max_severity is not UNSET:
            field_dict["max_severity"] = max_severity
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

        name = d.pop("name", UNSET)

        _chat_session = d.pop("chat_session", UNSET)
        chat_session: Union[Unset, UUID]
        if isinstance(_chat_session, Unset):
            chat_session = UNSET
        else:
            chat_session = UUID(_chat_session)

        flags = d.pop("flags", UNSET)

        is_archived = d.pop("is_archived", UNSET)

        message_count = d.pop("message_count", UNSET)

        is_flagged = d.pop("is_flagged", UNSET)

        _max_severity = d.pop("max_severity", UNSET)
        max_severity: Union[Unset, InjectionSeverityEnum]
        if isinstance(_max_severity, Unset):
            max_severity = UNSET
        else:
            max_severity = InjectionSeverityEnum(_max_severity)

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

        thread_session = cls(
            uuid=uuid,
            name=name,
            chat_session=chat_session,
            flags=flags,
            is_archived=is_archived,
            message_count=message_count,
            is_flagged=is_flagged,
            max_severity=max_severity,
            user_username=user_username,
            user_full_name=user_full_name,
            created=created,
            modified=modified,
        )

        thread_session.additional_properties = d
        return thread_session

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
