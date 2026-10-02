from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostStatsDtoKpis")



@_attrs_define
class CostStatsDtoKpis:
    """ Headline key performance indicators for the cost explorer.

        Attributes:
            total_cost (float): Total cost in USD across all runs in the window.
            avg_cost_per_run (float): Average cost per run in USD.
            total_tokens (float): Total tokens consumed across all runs in the window.
            total_runs (float): Total number of runs included in the cost stats.
            agent_cost (float): Portion of total cost spent on agent (LLM) inference in USD.
            compute_cost (float): Portion of total cost spent on compute (sandbox) execution in USD.
     """

    total_cost: float
    avg_cost_per_run: float
    total_tokens: float
    total_runs: float
    agent_cost: float
    compute_cost: float





    def to_dict(self) -> dict[str, Any]:
        total_cost = self.total_cost

        avg_cost_per_run = self.avg_cost_per_run

        total_tokens = self.total_tokens

        total_runs = self.total_runs

        agent_cost = self.agent_cost

        compute_cost = self.compute_cost


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "totalCost": total_cost,
            "avgCostPerRun": avg_cost_per_run,
            "totalTokens": total_tokens,
            "totalRuns": total_runs,
            "agentCost": agent_cost,
            "computeCost": compute_cost,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_cost = d.pop("totalCost")

        avg_cost_per_run = d.pop("avgCostPerRun")

        total_tokens = d.pop("totalTokens")

        total_runs = d.pop("totalRuns")

        agent_cost = d.pop("agentCost")

        compute_cost = d.pop("computeCost")

        cost_stats_dto_kpis = cls(
            total_cost=total_cost,
            avg_cost_per_run=avg_cost_per_run,
            total_tokens=total_tokens,
            total_runs=total_runs,
            agent_cost=agent_cost,
            compute_cost=compute_cost,
        )

        return cost_stats_dto_kpis

