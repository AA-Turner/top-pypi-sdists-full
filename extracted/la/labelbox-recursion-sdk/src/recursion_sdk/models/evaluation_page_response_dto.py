from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.evaluation_page_response_dto_items_item import EvaluationPageResponseDtoItemsItem





T = TypeVar("T", bound="EvaluationPageResponseDto")



@_attrs_define
class EvaluationPageResponseDto:
    """ Cursor-paginated page of evaluation list entries.

        Example:
            {'items': [{'id': '40811982-da7a-42bb-9963-5ca612372c63', 'kind': 'solve_and_grade', 'name': 'claude-sonnet-
                baseline', 'description': 'Baseline run of Claude Sonnet against the surface-defect detection problem.',
                'status': 'completed', 'nAttemptsPerProblem': 3, 'tags': [], 'graderRunConfigVersionId': None, 'totalSolvers':
                1, 'totalProblems': 1, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-15T10:05:00.000Z',
                'startedAt': '2026-01-15T09:30:12.000Z', 'completedAt': '2026-01-15T10:05:00.000Z', 'createdByName': 'Jane
                Doe'}], 'nextCursor': None, 'total': 1}

        Attributes:
            items (list[EvaluationPageResponseDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[EvaluationPageResponseDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_page_response_dto_items_item import EvaluationPageResponseDtoItemsItem # noqa: PLC0415
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
        from ..models.evaluation_page_response_dto_items_item import EvaluationPageResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = EvaluationPageResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        evaluation_page_response_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return evaluation_page_response_dto

