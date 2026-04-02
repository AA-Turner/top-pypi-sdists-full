import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Attachment")


@_attrs_define
class Attachment:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        file (Union[Unset, str]):
        mime_type (Union[Unset, str]):
        file_size (Union[Unset, int]):
        file_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        destroy_is_available (Union[Unset, bool]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    issue: Union[Unset, str] = UNSET
    issue_key: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    file: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    file_size: Union[Unset, int] = UNSET
    file_name: Union[Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    destroy_is_available: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        issue = self.issue

        issue_key = self.issue_key

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        file = self.file

        mime_type = self.mime_type

        file_size = self.file_size

        file_name = self.file_name

        backend_id = self.backend_id

        destroy_is_available = self.destroy_is_available

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if issue is not UNSET:
            field_dict["issue"] = issue
        if issue_key is not UNSET:
            field_dict["issue_key"] = issue_key
        if created is not UNSET:
            field_dict["created"] = created
        if file is not UNSET:
            field_dict["file"] = file
        if mime_type is not UNSET:
            field_dict["mime_type"] = mime_type
        if file_size is not UNSET:
            field_dict["file_size"] = file_size
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if destroy_is_available is not UNSET:
            field_dict["destroy_is_available"] = destroy_is_available

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        issue = d.pop("issue", UNSET)

        issue_key = d.pop("issue_key", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        file = d.pop("file", UNSET)

        mime_type = d.pop("mime_type", UNSET)

        file_size = d.pop("file_size", UNSET)

        file_name = d.pop("file_name", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        destroy_is_available = d.pop("destroy_is_available", UNSET)

        attachment = cls(
            url=url,
            uuid=uuid,
            issue=issue,
            issue_key=issue_key,
            created=created,
            file=file,
            mime_type=mime_type,
            file_size=file_size,
            file_name=file_name,
            backend_id=backend_id,
            destroy_is_available=destroy_is_available,
        )

        attachment.additional_properties = d
        return attachment

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
