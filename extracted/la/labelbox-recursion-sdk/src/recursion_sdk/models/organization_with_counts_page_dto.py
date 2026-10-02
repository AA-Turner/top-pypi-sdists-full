from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.organization_with_counts_page_dto_items_item import OrganizationWithCountsPageDtoItemsItem





T = TypeVar("T", bound="OrganizationWithCountsPageDto")



@_attrs_define
class OrganizationWithCountsPageDto:
    """ Cursor-paginated page of organizations with their problem and environment counts.

        Attributes:
            items (list[OrganizationWithCountsPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[OrganizationWithCountsPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.organization_with_counts_page_dto_items_item import OrganizationWithCountsPageDtoItemsItem # noqa: PLC0415
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
        from ..models.organization_with_counts_page_dto_items_item import OrganizationWithCountsPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = OrganizationWithCountsPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        organization_with_counts_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return organization_with_counts_page_dto

