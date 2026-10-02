from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File

T = TypeVar("T", bound="CreateAttachmentsRequest")


@_attrs_define
class CreateAttachmentsRequest:
    """
    Attributes:
        attachments (list[File]): List of files to attach
    """

    attachments: list[File]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attachments = []
        for attachments_item_data in self.attachments:
            attachments_item = attachments_item_data.to_tuple()

            attachments.append(attachments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attachments": attachments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attachments = []
        _attachments = d.pop("attachments")
        for attachments_item_data in _attachments:
            attachments_item = File(payload=BytesIO(attachments_item_data))

            attachments.append(attachments_item)

        create_attachments_request = cls(
            attachments=attachments,
        )

        create_attachments_request.additional_properties = d
        return create_attachments_request

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
