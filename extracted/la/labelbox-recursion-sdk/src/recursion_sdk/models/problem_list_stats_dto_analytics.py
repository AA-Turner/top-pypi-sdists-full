from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_list_stats_dto_analytics_all_scores_buckets_item import ProblemListStatsDtoAnalyticsAllScoresBucketsItem
  from ..models.problem_list_stats_dto_analytics_avg_score_buckets_item import ProblemListStatsDtoAnalyticsAvgScoreBucketsItem





T = TypeVar("T", bound="ProblemListStatsDtoAnalytics")



@_attrs_define
class ProblemListStatsDtoAnalytics:
    """ Pre-aggregated chart buckets covering the full filtered set.

        Attributes:
            avg_score_buckets (list[ProblemListStatsDtoAnalyticsAvgScoreBucketsItem]): One bucket per quartile of average
                score, aggregated per problem.
            all_scores_buckets (list[ProblemListStatsDtoAnalyticsAllScoresBucketsItem]): One bucket per quartile of score,
                aggregated over every individual run.
     """

    avg_score_buckets: list[ProblemListStatsDtoAnalyticsAvgScoreBucketsItem]
    all_scores_buckets: list[ProblemListStatsDtoAnalyticsAllScoresBucketsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_list_stats_dto_analytics_all_scores_buckets_item import ProblemListStatsDtoAnalyticsAllScoresBucketsItem # noqa: PLC0415
        from ..models.problem_list_stats_dto_analytics_avg_score_buckets_item import ProblemListStatsDtoAnalyticsAvgScoreBucketsItem # noqa: PLC0415
        avg_score_buckets = []
        for avg_score_buckets_item_data in self.avg_score_buckets:
            avg_score_buckets_item = avg_score_buckets_item_data.to_dict()
            avg_score_buckets.append(avg_score_buckets_item)



        all_scores_buckets = []
        for all_scores_buckets_item_data in self.all_scores_buckets:
            all_scores_buckets_item = all_scores_buckets_item_data.to_dict()
            all_scores_buckets.append(all_scores_buckets_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "avgScoreBuckets": avg_score_buckets,
            "allScoresBuckets": all_scores_buckets,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_list_stats_dto_analytics_all_scores_buckets_item import ProblemListStatsDtoAnalyticsAllScoresBucketsItem # noqa: PLC0415
        from ..models.problem_list_stats_dto_analytics_avg_score_buckets_item import ProblemListStatsDtoAnalyticsAvgScoreBucketsItem # noqa: PLC0415
        d = dict(src_dict)
        avg_score_buckets = []
        _avg_score_buckets = d.pop("avgScoreBuckets")
        for avg_score_buckets_item_data in (_avg_score_buckets):
            avg_score_buckets_item = ProblemListStatsDtoAnalyticsAvgScoreBucketsItem.from_dict(avg_score_buckets_item_data)



            avg_score_buckets.append(avg_score_buckets_item)


        all_scores_buckets = []
        _all_scores_buckets = d.pop("allScoresBuckets")
        for all_scores_buckets_item_data in (_all_scores_buckets):
            all_scores_buckets_item = ProblemListStatsDtoAnalyticsAllScoresBucketsItem.from_dict(all_scores_buckets_item_data)



            all_scores_buckets.append(all_scores_buckets_item)


        problem_list_stats_dto_analytics = cls(
            avg_score_buckets=avg_score_buckets,
            all_scores_buckets=all_scores_buckets,
        )

        return problem_list_stats_dto_analytics

