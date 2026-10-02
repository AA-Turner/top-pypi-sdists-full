from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CostDrillDownItemsResponseDtoItemsItem")



@_attrs_define
class CostDrillDownItemsResponseDtoItemsItem:
    """ Single row of a cost drill-down aggregation (one bucket at the requested drill level).

        Attributes:
            id (str): Stable identifier of the aggregation row (entity id for the drill level).
            label (str): Human-readable label rendered for the row.
            total_runs (float): Number of runs aggregated into this row.
            total_tokens (float): Total tokens across all runs in this row.
            input_tokens (float): Total input tokens across all runs in this row.
            output_tokens (float): Total output tokens across all runs in this row.
            cache_read_tokens (float): Total tokens read from prompt cache.
            cache_creation_tokens (float): Total tokens written to prompt cache.
            agent_cost_usd (float): Agent (LLM) inference cost for this row in USD.
            compute_cost_usd (float): Compute (sandbox) execution cost for this row in USD.
            total_cost_usd (float): Sum of agent and compute costs for this row in USD.
            scored_runs (float | Unset): Number of runs that produced a grading score (subset of totalRuns).
            avg_score (float | Unset): Mean grading score across scored runs in this row.
            total_problems (float | Unset): Number of distinct problems represented in this row.
     """

    id: str
    label: str
    total_runs: float
    total_tokens: float
    input_tokens: float
    output_tokens: float
    cache_read_tokens: float
    cache_creation_tokens: float
    agent_cost_usd: float
    compute_cost_usd: float
    total_cost_usd: float
    scored_runs: float | Unset = UNSET
    avg_score: float | Unset = UNSET
    total_problems: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        label = self.label

        total_runs = self.total_runs

        total_tokens = self.total_tokens

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        cache_read_tokens = self.cache_read_tokens

        cache_creation_tokens = self.cache_creation_tokens

        agent_cost_usd = self.agent_cost_usd

        compute_cost_usd = self.compute_cost_usd

        total_cost_usd = self.total_cost_usd

        scored_runs = self.scored_runs

        avg_score = self.avg_score

        total_problems = self.total_problems


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "label": label,
            "totalRuns": total_runs,
            "totalTokens": total_tokens,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "cacheReadTokens": cache_read_tokens,
            "cacheCreationTokens": cache_creation_tokens,
            "agentCostUsd": agent_cost_usd,
            "computeCostUsd": compute_cost_usd,
            "totalCostUsd": total_cost_usd,
        })
        if scored_runs is not UNSET:
            field_dict["scoredRuns"] = scored_runs
        if avg_score is not UNSET:
            field_dict["avgScore"] = avg_score
        if total_problems is not UNSET:
            field_dict["totalProblems"] = total_problems

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        label = d.pop("label")

        total_runs = d.pop("totalRuns")

        total_tokens = d.pop("totalTokens")

        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        cache_read_tokens = d.pop("cacheReadTokens")

        cache_creation_tokens = d.pop("cacheCreationTokens")

        agent_cost_usd = d.pop("agentCostUsd")

        compute_cost_usd = d.pop("computeCostUsd")

        total_cost_usd = d.pop("totalCostUsd")

        scored_runs = d.pop("scoredRuns", UNSET)

        avg_score = d.pop("avgScore", UNSET)

        total_problems = d.pop("totalProblems", UNSET)

        cost_drill_down_items_response_dto_items_item = cls(
            id=id,
            label=label,
            total_runs=total_runs,
            total_tokens=total_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_creation_tokens=cache_creation_tokens,
            agent_cost_usd=agent_cost_usd,
            compute_cost_usd=compute_cost_usd,
            total_cost_usd=total_cost_usd,
            scored_runs=scored_runs,
            avg_score=avg_score,
            total_problems=total_problems,
        )

        return cost_drill_down_items_response_dto_items_item

