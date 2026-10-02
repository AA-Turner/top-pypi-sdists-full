from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportScreenshotDataRequest")


@_attrs_define
class ExportScreenshotDataRequest:
    """
    Attributes:
        name (str):
        description (str):
        image_content (str):
        image_filename (str):
        content_type (str):
    """

    name: str
    description: str
    image_content: str
    image_filename: str
    content_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        image_content = self.image_content

        image_filename = self.image_filename

        content_type = self.content_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "image_content": image_content,
                "image_filename": image_filename,
                "content_type": content_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        image_content = d.pop("image_content")

        image_filename = d.pop("image_filename")

        content_type = d.pop("content_type")

        export_screenshot_data_request = cls(
            name=name,
            description=description,
            image_content=image_content,
            image_filename=image_filename,
            content_type=content_type,
        )

        export_screenshot_data_request.additional_properties = d
        return export_screenshot_data_request

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
