from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsUploadedImage")



@_attrs_define
class ManagedAgentsUploadedImage:
    """ The stored image an upload produced. Reference it from a message by putting uri on an image content block.

        Example:
            {'byte_size': 1, 'height': 1, 'media_type': 'example', 'sha256': 'example', 'uri': 'example', 'width': 1}

        Attributes:
            byte_size (int): Stored image size in bytes.
            height (int): Decoded image height in pixels.
            media_type (str): Sniffed media type of the stored bytes.
            sha256 (str): Lowercase SHA-256 of the stored bytes; also the image's model-facing id prefix.
            uri (str): Private content reference to place on an image content block in a later sendSessionEvents call.
                Readable only through this session.
            width (int): Decoded image width in pixels.
     """

    byte_size: int
    height: int
    media_type: str
    sha256: str
    uri: str
    width: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        byte_size = self.byte_size

        height = self.height

        media_type = self.media_type

        sha256 = self.sha256

        uri = self.uri

        width = self.width


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "byte_size": byte_size,
            "height": height,
            "media_type": media_type,
            "sha256": sha256,
            "uri": uri,
            "width": width,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        byte_size = d.pop("byte_size")

        height = d.pop("height")

        media_type = d.pop("media_type")

        sha256 = d.pop("sha256")

        uri = d.pop("uri")

        width = d.pop("width")

        managed_agents_uploaded_image = cls(
            byte_size=byte_size,
            height=height,
            media_type=media_type,
            sha256=sha256,
            uri=uri,
            width=width,
        )


        managed_agents_uploaded_image.additional_properties = d
        return managed_agents_uploaded_image

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
