from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.grade_history_response_dto_items_item import GradeHistoryResponseDtoItemsItem





T = TypeVar("T", bound="GradeHistoryResponseDto")



@_attrs_define
class GradeHistoryResponseDto:
    """ Superseded grades for a problem run, most recent re-grade first.

        Example:
            {'items': [{'id': 'b2c3d4e5-6f70-4a1b-8c2d-3e4f5a6b7c8d', 'finalScore': 0.83, 'gradedAt':
                '2026-01-15T09:31:05.000Z', 'justification': 'All four visible scratches were correctly localized; one faint
                dent was missed.', 'gradingModelName': 'claude-opus-4-6', 'archivedAt': '2026-01-16T14:02:11.000Z'}],
                'nextCursor': None, 'total': 1}

        Attributes:
            items (list[GradeHistoryResponseDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[GradeHistoryResponseDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.grade_history_response_dto_items_item import GradeHistoryResponseDtoItemsItem # noqa: PLC0415
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
        from ..models.grade_history_response_dto_items_item import GradeHistoryResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = GradeHistoryResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        grade_history_response_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return grade_history_response_dto

