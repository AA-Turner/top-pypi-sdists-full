from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ImagesResponseDtoImagesItem")



@_attrs_define
class ImagesResponseDtoImagesItem:
    """ Lightweight image record suitable for listing in pickers.

        Attributes:
            id (str): Stable identifier for a runtime container image.
            display_name (str): Human-readable name of the image shown in selection UIs.
     """

    id: str
    display_name: str





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        display_name = self.display_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "displayName": display_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        display_name = d.pop("displayName")

        images_response_dto_images_item = cls(
            id=id,
            display_name=display_name,
        )

        return images_response_dto_images_item

