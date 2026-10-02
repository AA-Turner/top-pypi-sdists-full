import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="TemplateAttachment")


@_attrs_define
class TemplateAttachment:
    """
    Attributes:
        uuid (UUID):
        name (str):
        file (str):
        mime_type (str):
        file_size (int):
        created (datetime.datetime):
    """

    uuid: UUID
    name: str
    file: str
    mime_type: str
    file_size: int
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        file = self.file

        mime_type = self.mime_type

        file_size = self.file_size

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "file": file,
                "mime_type": mime_type,
                "file_size": file_size,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        file = d.pop("file")

        mime_type = d.pop("mime_type")

        file_size = d.pop("file_size")

        created = isoparse(d.pop("created"))

        template_attachment = cls(
            uuid=uuid,
            name=name,
            file=file,
            mime_type=mime_type,
            file_size=file_size,
            created=created,
        )

        template_attachment.additional_properties = d
        return template_attachment

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
