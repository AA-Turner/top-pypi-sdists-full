from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.cost_stats_dto_cost_by_model_item import CostStatsDtoCostByModelItem
  from ..models.cost_stats_dto_cost_by_organization_item import CostStatsDtoCostByOrganizationItem
  from ..models.cost_stats_dto_cost_by_run_type_item import CostStatsDtoCostByRunTypeItem
  from ..models.cost_stats_dto_cost_over_time_item import CostStatsDtoCostOverTimeItem
  from ..models.cost_stats_dto_kpis import CostStatsDtoKpis





T = TypeVar("T", bound="CostStatsDto")



@_attrs_define
class CostStatsDto:
    """ Aggregated cost statistics powering the admin cost explorer.

        Attributes:
            kpis (CostStatsDtoKpis): Headline key performance indicators for the cost explorer.
            cost_over_time (list[CostStatsDtoCostOverTimeItem]): Daily cost breakdown across the selected window.
            cost_by_run_type (list[CostStatsDtoCostByRunTypeItem]): Cost broken down by run type, across every RunType value
                (solver, the grading variants, QA, and the non–problem-run surfaces: synthesizer, run-config probe, probe judge,
                grade extraction, transcript synthesis, title generation, transcript reformat).
            cost_by_model (list[CostStatsDtoCostByModelItem]): Cost broken down by LLM model with detailed token accounting.
            cost_by_organization (list[CostStatsDtoCostByOrganizationItem]): Cost broken down by organization.
     """

    kpis: CostStatsDtoKpis
    cost_over_time: list[CostStatsDtoCostOverTimeItem]
    cost_by_run_type: list[CostStatsDtoCostByRunTypeItem]
    cost_by_model: list[CostStatsDtoCostByModelItem]
    cost_by_organization: list[CostStatsDtoCostByOrganizationItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.cost_stats_dto_cost_by_model_item import CostStatsDtoCostByModelItem # noqa: PLC0415
        from ..models.cost_stats_dto_cost_by_organization_item import CostStatsDtoCostByOrganizationItem # noqa: PLC0415
        from ..models.cost_stats_dto_cost_by_run_type_item import CostStatsDtoCostByRunTypeItem # noqa: PLC0415
        from ..models.cost_stats_dto_cost_over_time_item import CostStatsDtoCostOverTimeItem # noqa: PLC0415
        from ..models.cost_stats_dto_kpis import CostStatsDtoKpis # noqa: PLC0415
        kpis = self.kpis.to_dict()

        cost_over_time = []
        for cost_over_time_item_data in self.cost_over_time:
            cost_over_time_item = cost_over_time_item_data.to_dict()
            cost_over_time.append(cost_over_time_item)



        cost_by_run_type = []
        for cost_by_run_type_item_data in self.cost_by_run_type:
            cost_by_run_type_item = cost_by_run_type_item_data.to_dict()
            cost_by_run_type.append(cost_by_run_type_item)



        cost_by_model = []
        for cost_by_model_item_data in self.cost_by_model:
            cost_by_model_item = cost_by_model_item_data.to_dict()
            cost_by_model.append(cost_by_model_item)



        cost_by_organization = []
        for cost_by_organization_item_data in self.cost_by_organization:
            cost_by_organization_item = cost_by_organization_item_data.to_dict()
            cost_by_organization.append(cost_by_organization_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kpis": kpis,
            "costOverTime": cost_over_time,
            "costByRunType": cost_by_run_type,
            "costByModel": cost_by_model,
            "costByOrganization": cost_by_organization,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cost_stats_dto_cost_by_model_item import CostStatsDtoCostByModelItem # noqa: PLC0415
        from ..models.cost_stats_dto_cost_by_organization_item import CostStatsDtoCostByOrganizationItem # noqa: PLC0415
        from ..models.cost_stats_dto_cost_by_run_type_item import CostStatsDtoCostByRunTypeItem # noqa: PLC0415
        from ..models.cost_stats_dto_cost_over_time_item import CostStatsDtoCostOverTimeItem # noqa: PLC0415
        from ..models.cost_stats_dto_kpis import CostStatsDtoKpis # noqa: PLC0415
        d = dict(src_dict)
        kpis = CostStatsDtoKpis.from_dict(d.pop("kpis"))




        cost_over_time = []
        _cost_over_time = d.pop("costOverTime")
        for cost_over_time_item_data in (_cost_over_time):
            cost_over_time_item = CostStatsDtoCostOverTimeItem.from_dict(cost_over_time_item_data)



            cost_over_time.append(cost_over_time_item)


        cost_by_run_type = []
        _cost_by_run_type = d.pop("costByRunType")
        for cost_by_run_type_item_data in (_cost_by_run_type):
            cost_by_run_type_item = CostStatsDtoCostByRunTypeItem.from_dict(cost_by_run_type_item_data)



            cost_by_run_type.append(cost_by_run_type_item)


        cost_by_model = []
        _cost_by_model = d.pop("costByModel")
        for cost_by_model_item_data in (_cost_by_model):
            cost_by_model_item = CostStatsDtoCostByModelItem.from_dict(cost_by_model_item_data)



            cost_by_model.append(cost_by_model_item)


        cost_by_organization = []
        _cost_by_organization = d.pop("costByOrganization")
        for cost_by_organization_item_data in (_cost_by_organization):
            cost_by_organization_item = CostStatsDtoCostByOrganizationItem.from_dict(cost_by_organization_item_data)



            cost_by_organization.append(cost_by_organization_item)


        cost_stats_dto = cls(
            kpis=kpis,
            cost_over_time=cost_over_time,
            cost_by_run_type=cost_by_run_type,
            cost_by_model=cost_by_model,
            cost_by_organization=cost_by_organization,
        )

        return cost_stats_dto

