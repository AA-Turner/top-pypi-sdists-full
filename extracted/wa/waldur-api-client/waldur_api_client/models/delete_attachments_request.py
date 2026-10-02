from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeleteAttachmentsRequest")


@_attrs_define
class DeleteAttachmentsRequest:
    """
    Attributes:
        attachment_ids (list[UUID]):
    """

    attachment_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attachment_ids = []
        for attachment_ids_item_data in self.attachment_ids:
            attachment_ids_item = str(attachment_ids_item_data)
            attachment_ids.append(attachment_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attachment_ids": attachment_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attachment_ids = []
        _attachment_ids = d.pop("attachment_ids")
        for attachment_ids_item_data in _attachment_ids:
            attachment_ids_item = UUID(attachment_ids_item_data)

            attachment_ids.append(attachment_ids_item)

        delete_attachments_request = cls(
            attachment_ids=attachment_ids,
        )

        delete_attachments_request.additional_properties = d
        return delete_attachments_request

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
