from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.cost_stats_dto_cost_by_run_type_item_run_type import CostStatsDtoCostByRunTypeItemRunType






T = TypeVar("T", bound="CostStatsDtoCostByRunTypeItem")



@_attrs_define
class CostStatsDtoCostByRunTypeItem:
    """ Cost roll-up for a single run type.

        Attributes:
            run_type (CostStatsDtoCostByRunTypeItemRunType): Run category. One of the RunType values — solver (the agent
                attempting the problem), the grading variants (agentic / rubric / programmatic / MCP-tool-call), qa, and the
                non–problem-run cost surfaces (synthesizer, run-config probe, probe judge, grade extraction, transcript
                synthesis, title generation, transcript reformat), plus the jobs-v2-rooted surfaces (rollout, check-fix cycle)
                and managed-agent turns. QA and the non–problem-run surfaces are attributed via their environment/problem rather
                than a problem run; managed-agent turns are attributed to their organization only.
            total_cost (float): Total cost incurred by this run type in USD.
            runs (float): Number of runs of this type.
     """

    run_type: CostStatsDtoCostByRunTypeItemRunType
    total_cost: float
    runs: float





    def to_dict(self) -> dict[str, Any]:
        run_type = self.run_type.value

        total_cost = self.total_cost

        runs = self.runs


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runType": run_type,
            "totalCost": total_cost,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_type = CostStatsDtoCostByRunTypeItemRunType(d.pop("runType"))




        total_cost = d.pop("totalCost")

        runs = d.pop("runs")

        cost_stats_dto_cost_by_run_type_item = cls(
            run_type=run_type,
            total_cost=total_cost,
            runs=runs,
        )

        return cost_stats_dto_cost_by_run_type_item

