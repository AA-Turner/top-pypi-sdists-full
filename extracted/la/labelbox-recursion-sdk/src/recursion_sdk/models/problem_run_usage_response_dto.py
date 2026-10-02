from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_run_usage_response_dto_items_item import ProblemRunUsageResponseDtoItemsItem





T = TypeVar("T", bound="ProblemRunUsageResponseDto")



@_attrs_define
class ProblemRunUsageResponseDto:
    """ Cost and consumed-vs-requested resources for every agent-service run behind a problem run.

        Example:
            {'items': [{'runType': 'solver', 'modelName': 'claude-sonnet-5', 'agentCostUsd': 0.3121, 'computeCostUsd':
                0.0184, 'totalCostUsd': 0.3305, 'inputTokens': 18432, 'outputTokens': 7910, 'cacheReadInputTokens': 102400,
                'cacheCreationInputTokens': 4096, 'resourceUsage': {'scope': 'cgroup', 'sampleCount': 47, 'sampledSeconds':
                231.4, 'cpu': {'avgMillicores': 410, 'peakMillicores': 1220, 'capacityMillicores': 2000, 'coreSeconds': 94.9},
                'memory': {'avgWorkingSetBytes': 1181116006, 'peakWorkingSetBytes': 1717986918, 'capacityBytes': 4294967296},
                'gpu': None, 'disk': {'peakUsedBytes': 3435973836, 'capacityBytes': 52512901529}}}, {'runType':
                'agentic_grading', 'modelName': 'claude-sonnet-5', 'agentCostUsd': 0.0212, 'computeCostUsd': None,
                'totalCostUsd': 0.0212, 'inputTokens': 6210, 'outputTokens': 880, 'cacheReadInputTokens': 0,
                'cacheCreationInputTokens': 0, 'resourceUsage': None}], 'totalCostUsd': 0.3517}

        Attributes:
            items (list[ProblemRunUsageResponseDtoItemsItem]): One row per agent-service run attributed to this problem run:
                the solver first, then graders.
            total_cost_usd (float | None): Sum of every row that reported a cost. Null when no row has cost data yet.
     """

    items: list[ProblemRunUsageResponseDtoItemsItem]
    total_cost_usd: float | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_run_usage_response_dto_items_item import ProblemRunUsageResponseDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "totalCostUsd": total_cost_usd,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_run_usage_response_dto_items_item import ProblemRunUsageResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ProblemRunUsageResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        problem_run_usage_response_dto = cls(
            items=items,
            total_cost_usd=total_cost_usd,
        )

        return problem_run_usage_response_dto

