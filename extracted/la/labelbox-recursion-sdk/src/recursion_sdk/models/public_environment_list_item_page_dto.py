from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.public_environment_list_item_page_dto_items_item import PublicEnvironmentListItemPageDtoItemsItem





T = TypeVar("T", bound="PublicEnvironmentListItemPageDto")



@_attrs_define
class PublicEnvironmentListItemPageDto:
    """ Cursor-paginated page of public environment marketplace cards.

        Attributes:
            items (list[PublicEnvironmentListItemPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[PublicEnvironmentListItemPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.public_environment_list_item_page_dto_items_item import PublicEnvironmentListItemPageDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_cursor: None | str
        next_cursor = self.next_cursor

        total = self.total


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "nextCursor": next_cursor,
            "total": total,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.public_environment_list_item_page_dto_items_item import PublicEnvironmentListItemPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = PublicEnvironmentListItemPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        public_environment_list_item_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return public_environment_list_item_page_dto

