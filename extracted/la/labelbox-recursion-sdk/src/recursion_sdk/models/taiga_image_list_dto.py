from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.taiga_image_list_dto_items_item import TaigaImageListDtoItemsItem





T = TypeVar("T", bound="TaigaImageListDto")



@_attrs_define
class TaigaImageListDto:
    """ Response for GET /v1/organizations/:organizationId/taiga-images. Returned unpaginated because the catalog is bounded
    by manual admin actions and is expected to remain small per organization.

        Attributes:
            items (list[TaigaImageListDtoItemsItem]): Active (non-soft-deleted) catalog entries for the organization,
                ordered by creation time.
     """

    items: list[TaigaImageListDtoItemsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.taiga_image_list_dto_items_item import TaigaImageListDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.taiga_image_list_dto_items_item import TaigaImageListDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = TaigaImageListDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        taiga_image_list_dto = cls(
            items=items,
        )

        return taiga_image_list_dto

