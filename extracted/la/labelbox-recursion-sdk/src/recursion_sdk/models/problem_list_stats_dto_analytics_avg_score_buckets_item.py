from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ProblemListStatsDtoAnalyticsAvgScoreBucketsItem")



@_attrs_define
class ProblemListStatsDtoAnalyticsAvgScoreBucketsItem:
    """ Single histogram bucket in the problem-list analytics payload.

        Attributes:
            label (str): Human-readable bucket label (e.g. '0-25%').
            count (int): Total number of items (problems or runs) that fall into this bucket.
            sample_items (list[str]): Up to ANALYTICS_BUCKET_SAMPLE_LIMIT representative items as display-ready strings,
                used to populate the bucket tooltip.
     """

    label: str
    count: int
    sample_items: list[str]





    def to_dict(self) -> dict[str, Any]:
        label = self.label

        count = self.count

        sample_items = self.sample_items




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "count": count,
            "sampleItems": sample_items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        count = d.pop("count")

        sample_items = cast(list[str], d.pop("sampleItems"))


        problem_list_stats_dto_analytics_avg_score_buckets_item = cls(
            label=label,
            count=count,
            sample_items=sample_items,
        )

        return problem_list_stats_dto_analytics_avg_score_buckets_item

