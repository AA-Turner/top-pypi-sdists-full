import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SupportUserAttachmentBrief")


@_attrs_define
class SupportUserAttachmentBrief:
    """
    Attributes:
        uuid (UUID):
        file_name (str):
        created (datetime.datetime):
        issue_key (str):
        issue_uuid (UUID):
    """

    uuid: UUID
    file_name: str
    created: datetime.datetime
    issue_key: str
    issue_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        file_name = self.file_name

        created = self.created.isoformat()

        issue_key = self.issue_key

        issue_uuid = str(self.issue_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "file_name": file_name,
                "created": created,
                "issue_key": issue_key,
                "issue_uuid": issue_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        file_name = d.pop("file_name")

        created = isoparse(d.pop("created"))

        issue_key = d.pop("issue_key")

        issue_uuid = UUID(d.pop("issue_uuid"))

        support_user_attachment_brief = cls(
            uuid=uuid,
            file_name=file_name,
            created=created,
            issue_key=issue_key,
            issue_uuid=issue_uuid,
        )

        support_user_attachment_brief.additional_properties = d
        return support_user_attachment_brief

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
