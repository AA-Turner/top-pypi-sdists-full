from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.public_problem_detail_dto_runs_items_item import PublicProblemDetailDtoRunsItemsItem





T = TypeVar("T", bound="PublicProblemDetailDtoRuns")



@_attrs_define
class PublicProblemDetailDtoRuns:
    """ Execution summaries for the returned locked versions.

        Attributes:
            items (list[PublicProblemDetailDtoRunsItemsItem]): Newest-first runs associated with the locked versions
                returned in this problem detail.
            truncated (bool): True when older runs were omitted because the problem exceeded the history cap.
     """

    items: list[PublicProblemDetailDtoRunsItemsItem]
    truncated: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.public_problem_detail_dto_runs_items_item import PublicProblemDetailDtoRunsItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        truncated = self.truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "truncated": truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.public_problem_detail_dto_runs_items_item import PublicProblemDetailDtoRunsItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = PublicProblemDetailDtoRunsItemsItem.from_dict(items_item_data)



            items.append(items_item)


        truncated = d.pop("truncated")

        public_problem_detail_dto_runs = cls(
            items=items,
            truncated=truncated,
        )

        return public_problem_detail_dto_runs

