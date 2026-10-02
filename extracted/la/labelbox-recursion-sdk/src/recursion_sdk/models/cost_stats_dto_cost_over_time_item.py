from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostStatsDtoCostOverTimeItem")



@_attrs_define
class CostStatsDtoCostOverTimeItem:
    """ Single day in the cost time series.

        Attributes:
            date (str): Calendar day for the bucketed cost (ISO-8601 date, UTC).
            total_cost_usd (float): Total cost incurred on this day in USD.
            agent_cost_usd (float): Agent (LLM) inference cost on this day in USD.
            compute_cost_usd (float): Compute (sandbox) execution cost on this day in USD.
            runs (float): Number of runs that contributed to this day’s costs.
     """

    date: str
    total_cost_usd: float
    agent_cost_usd: float
    compute_cost_usd: float
    runs: float





    def to_dict(self) -> dict[str, Any]:
        date = self.date

        total_cost_usd = self.total_cost_usd

        agent_cost_usd = self.agent_cost_usd

        compute_cost_usd = self.compute_cost_usd

        runs = self.runs


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "date": date,
            "totalCostUsd": total_cost_usd,
            "agentCostUsd": agent_cost_usd,
            "computeCostUsd": compute_cost_usd,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        total_cost_usd = d.pop("totalCostUsd")

        agent_cost_usd = d.pop("agentCostUsd")

        compute_cost_usd = d.pop("computeCostUsd")

        runs = d.pop("runs")

        cost_stats_dto_cost_over_time_item = cls(
            date=date,
            total_cost_usd=total_cost_usd,
            agent_cost_usd=agent_cost_usd,
            compute_cost_usd=compute_cost_usd,
            runs=runs,
        )

        return cost_stats_dto_cost_over_time_item

