from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NotificationTemplateDetailSerializers")


@_attrs_define
class NotificationTemplateDetailSerializers:
    """
    Attributes:
        uuid (UUID):
        url (str):
        path (str): Example: 'flatpages/default.html'
        name (str):
        content (Union[None, str]):
        original_content (Union[None, str]):
        is_content_overridden (bool):
    """

    uuid: UUID
    url: str
    path: str
    name: str
    content: Union[None, str]
    original_content: Union[None, str]
    is_content_overridden: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        path = self.path

        name = self.name

        content: Union[None, str]
        content = self.content

        original_content: Union[None, str]
        original_content = self.original_content

        is_content_overridden = self.is_content_overridden

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "path": path,
                "name": name,
                "content": content,
                "original_content": original_content,
                "is_content_overridden": is_content_overridden,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        path = d.pop("path")

        name = d.pop("name")

        def _parse_content(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        content = _parse_content(d.pop("content"))

        def _parse_original_content(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        original_content = _parse_original_content(d.pop("original_content"))

        is_content_overridden = d.pop("is_content_overridden")

        notification_template_detail_serializers = cls(
            uuid=uuid,
            url=url,
            path=path,
            name=name,
            content=content,
            original_content=original_content,
            is_content_overridden=is_content_overridden,
        )

        notification_template_detail_serializers.additional_properties = d
        return notification_template_detail_serializers

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
