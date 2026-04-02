from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ImageCreateResponse")


@_attrs_define
class ImageCreateResponse:
    """
    Attributes:
        image_id (UUID):
        name (str):
        status (str):
        upload_url (str):
    """

    image_id: UUID
    name: str
    status: str
    upload_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_id = str(self.image_id)

        name = self.name

        status = self.status

        upload_url = self.upload_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image_id": image_id,
                "name": name,
                "status": status,
                "upload_url": upload_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image_id = UUID(d.pop("image_id"))

        name = d.pop("name")

        status = d.pop("status")

        upload_url = d.pop("upload_url")

        image_create_response = cls(
            image_id=image_id,
            name=name,
            status=status,
            upload_url=upload_url,
        )

        image_create_response.additional_properties = d
        return image_create_response

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
