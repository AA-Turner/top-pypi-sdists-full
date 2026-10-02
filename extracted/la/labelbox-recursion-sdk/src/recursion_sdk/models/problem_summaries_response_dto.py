from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_summaries_response_dto_items_item import ProblemSummariesResponseDtoItemsItem





T = TypeVar("T", bound="ProblemSummariesResponseDto")



@_attrs_define
class ProblemSummariesResponseDto:
    """ Response payload for the picker-summary endpoint listing problems in an environment.

        Example:
            {'items': [{'id': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'externalId': 'detect-surface-defects', 'title':
                'Detect surface defects on machined parts', 'hasLockedVersion': True}], 'truncated': False, 'total': 1}

        Attributes:
            items (list[ProblemSummariesResponseDtoItemsItem]): Problem summaries for the current page, bounded by the
                requested limit.
            truncated (bool): True when more problems match the request than the requested limit returned (limit < total);
                the client should surface a truncation banner or paginate.
            total (int): Total problems matching the request filters, independent of the requested limit.
     """

    items: list[ProblemSummariesResponseDtoItemsItem]
    truncated: bool
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_summaries_response_dto_items_item import ProblemSummariesResponseDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        truncated = self.truncated

        total = self.total


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "truncated": truncated,
            "total": total,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_summaries_response_dto_items_item import ProblemSummariesResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ProblemSummariesResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        truncated = d.pop("truncated")

        total = d.pop("total")

        problem_summaries_response_dto = cls(
            items=items,
            truncated=truncated,
            total=total,
        )

        return problem_summaries_response_dto

