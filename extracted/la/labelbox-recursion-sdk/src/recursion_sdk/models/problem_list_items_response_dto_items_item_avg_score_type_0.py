from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ProblemListItemsResponseDtoItemsItemAvgScoreType0")



@_attrs_define
class ProblemListItemsResponseDtoItemsItemAvgScoreType0:
    """ Aggregate score statistics for a problem scoped to its latest run group.

        Attributes:
            avg (float): Mean grader score across completed graded runs in the latest run group for this problem. May be
                negative. Example: 0.72.
            min_ (float): Minimum grader score across completed graded runs in the latest run group for this problem. May be
                negative. Example: 0.31.
            max_ (float): Maximum grader score across completed graded runs in the latest run group for this problem. May be
                negative. Example: 0.95.
     """

    avg: float
    min_: float
    max_: float





    def to_dict(self) -> dict[str, Any]:
        avg = self.avg

        min_ = self.min_

        max_ = self.max_


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "avg": avg,
            "min": min_,
            "max": max_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        avg = d.pop("avg")

        min_ = d.pop("min")

        max_ = d.pop("max")

        problem_list_items_response_dto_items_item_avg_score_type_0 = cls(
            avg=avg,
            min_=min_,
            max_=max_,
        )

        return problem_list_items_response_dto_items_item_avg_score_type_0

