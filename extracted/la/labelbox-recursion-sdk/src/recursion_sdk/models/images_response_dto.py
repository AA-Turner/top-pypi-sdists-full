from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.images_response_dto_images_item import ImagesResponseDtoImagesItem





T = TypeVar("T", bound="ImagesResponseDto")



@_attrs_define
class ImagesResponseDto:
    """ Response payload listing available runtime images.

        Example:
            {'images': [{'id': 'claude-code', 'displayName': 'Claude Code'}]}

        Attributes:
            images (list[ImagesResponseDtoImagesItem]): Image summaries available to the caller.
     """

    images: list[ImagesResponseDtoImagesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.images_response_dto_images_item import ImagesResponseDtoImagesItem # noqa: PLC0415
        images = []
        for images_item_data in self.images:
            images_item = images_item_data.to_dict()
            images.append(images_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "images": images,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.images_response_dto_images_item import ImagesResponseDtoImagesItem # noqa: PLC0415
        d = dict(src_dict)
        images = []
        _images = d.pop("images")
        for images_item_data in (_images):
            images_item = ImagesResponseDtoImagesItem.from_dict(images_item_data)



            images.append(images_item)


        images_response_dto = cls(
            images=images,
        )

        return images_response_dto

