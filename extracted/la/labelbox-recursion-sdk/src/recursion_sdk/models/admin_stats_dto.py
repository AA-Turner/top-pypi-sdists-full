from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.admin_stats_dto_counts import AdminStatsDtoCounts
  from ..models.admin_stats_dto_runs_by_status_item import AdminStatsDtoRunsByStatusItem
  from ..models.admin_stats_dto_runs_over_time_item import AdminStatsDtoRunsOverTimeItem
  from ..models.admin_stats_dto_tokens_by_model_item import AdminStatsDtoTokensByModelItem





T = TypeVar("T", bound="AdminStatsDto")



@_attrs_define
class AdminStatsDto:
    """ Aggregated platform-wide statistics.

        Attributes:
            counts (AdminStatsDtoCounts): Top-line entity counts across the platform.
            runs_over_time (list[AdminStatsDtoRunsOverTimeItem]): Daily problem-run counts over the selected window.
            tokens_by_model (list[AdminStatsDtoTokensByModelItem]): Token usage broken down by LLM model.
            runs_by_status (list[AdminStatsDtoRunsByStatusItem]): Problem-run counts grouped by terminal status.
     """

    counts: AdminStatsDtoCounts
    runs_over_time: list[AdminStatsDtoRunsOverTimeItem]
    tokens_by_model: list[AdminStatsDtoTokensByModelItem]
    runs_by_status: list[AdminStatsDtoRunsByStatusItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.admin_stats_dto_counts import AdminStatsDtoCounts # noqa: PLC0415
        from ..models.admin_stats_dto_runs_by_status_item import AdminStatsDtoRunsByStatusItem # noqa: PLC0415
        from ..models.admin_stats_dto_runs_over_time_item import AdminStatsDtoRunsOverTimeItem # noqa: PLC0415
        from ..models.admin_stats_dto_tokens_by_model_item import AdminStatsDtoTokensByModelItem # noqa: PLC0415
        counts = self.counts.to_dict()

        runs_over_time = []
        for runs_over_time_item_data in self.runs_over_time:
            runs_over_time_item = runs_over_time_item_data.to_dict()
            runs_over_time.append(runs_over_time_item)



        tokens_by_model = []
        for tokens_by_model_item_data in self.tokens_by_model:
            tokens_by_model_item = tokens_by_model_item_data.to_dict()
            tokens_by_model.append(tokens_by_model_item)



        runs_by_status = []
        for runs_by_status_item_data in self.runs_by_status:
            runs_by_status_item = runs_by_status_item_data.to_dict()
            runs_by_status.append(runs_by_status_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "counts": counts,
            "runsOverTime": runs_over_time,
            "tokensByModel": tokens_by_model,
            "runsByStatus": runs_by_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_stats_dto_counts import AdminStatsDtoCounts # noqa: PLC0415
        from ..models.admin_stats_dto_runs_by_status_item import AdminStatsDtoRunsByStatusItem # noqa: PLC0415
        from ..models.admin_stats_dto_runs_over_time_item import AdminStatsDtoRunsOverTimeItem # noqa: PLC0415
        from ..models.admin_stats_dto_tokens_by_model_item import AdminStatsDtoTokensByModelItem # noqa: PLC0415
        d = dict(src_dict)
        counts = AdminStatsDtoCounts.from_dict(d.pop("counts"))




        runs_over_time = []
        _runs_over_time = d.pop("runsOverTime")
        for runs_over_time_item_data in (_runs_over_time):
            runs_over_time_item = AdminStatsDtoRunsOverTimeItem.from_dict(runs_over_time_item_data)



            runs_over_time.append(runs_over_time_item)


        tokens_by_model = []
        _tokens_by_model = d.pop("tokensByModel")
        for tokens_by_model_item_data in (_tokens_by_model):
            tokens_by_model_item = AdminStatsDtoTokensByModelItem.from_dict(tokens_by_model_item_data)



            tokens_by_model.append(tokens_by_model_item)


        runs_by_status = []
        _runs_by_status = d.pop("runsByStatus")
        for runs_by_status_item_data in (_runs_by_status):
            runs_by_status_item = AdminStatsDtoRunsByStatusItem.from_dict(runs_by_status_item_data)



            runs_by_status.append(runs_by_status_item)


        admin_stats_dto = cls(
            counts=counts,
            runs_over_time=runs_over_time,
            tokens_by_model=tokens_by_model,
            runs_by_status=runs_by_status,
        )

        return admin_stats_dto

