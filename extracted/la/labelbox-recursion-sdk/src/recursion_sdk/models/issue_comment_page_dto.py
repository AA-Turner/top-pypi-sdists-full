from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.issue_comment_page_dto_items_item import IssueCommentPageDtoItemsItem





T = TypeVar("T", bound="IssueCommentPageDto")



@_attrs_define
class IssueCommentPageDto:
    """ Cursor-paginated page of issue comments.

        Example:
            {'items': [{'id': '6fd7956e-cd53-4f46-a493-20e1356dd800', 'issueId': 'e12cb018-b24c-4b35-9d8d-e7b486eb4e95',
                'authorId': '49dea803-7390-49c4-abb1-5629718fc9cd', 'content': 'The detect-surface-defects grader is flagging
                clean parts as defective — looks like the brightness threshold is too aggressive. Can we lower it before the
                next eval run?', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-15T09:30:00.000Z'}],
                'nextCursor': None, 'total': 1}

        Attributes:
            items (list[IssueCommentPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[IssueCommentPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.issue_comment_page_dto_items_item import IssueCommentPageDtoItemsItem # noqa: PLC0415
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
        from ..models.issue_comment_page_dto_items_item import IssueCommentPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = IssueCommentPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        issue_comment_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return issue_comment_page_dto

