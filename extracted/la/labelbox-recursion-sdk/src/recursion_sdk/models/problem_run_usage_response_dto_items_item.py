from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0





T = TypeVar("T", bound="ProblemRunUsageResponseDtoItemsItem")



@_attrs_define
class ProblemRunUsageResponseDtoItemsItem:
    """ Cost and resource usage of one agent-service run attributed to a problem run.

        Attributes:
            run_type (str): Which agent-service run this row bills: 'solver' for the attempt itself, or a grading type such
                as 'agentic_grading'. Example: solver.
            model_name (None | str): Model the run used, when known.
            agent_cost_usd (float | None): USD spent on model calls. Null when not reported.
            compute_cost_usd (float | None): USD spent on compute. Null when not reported.
            total_cost_usd (float | None): Agent plus compute cost in USD. Null when neither leg was reported.
            input_tokens (int | None): Uncached input tokens. Null when not reported.
            output_tokens (int | None): Output tokens. Null when not reported.
            cache_read_input_tokens (int | None): Input tokens served from prompt cache. Null when not reported.
            cache_creation_input_tokens (int | None): Input tokens written to prompt cache. Null when not reported.
            resource_usage (None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0): Resources the run consumed. Null
                for runs whose runner predates resource sampling or whose container could not be read.
     """

    run_type: str
    model_name: None | str
    agent_cost_usd: float | None
    compute_cost_usd: float | None
    total_cost_usd: float | None
    input_tokens: int | None
    output_tokens: int | None
    cache_read_input_tokens: int | None
    cache_creation_input_tokens: int | None
    resource_usage: None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0 # noqa: PLC0415
        run_type = self.run_type

        model_name: None | str
        model_name = self.model_name

        agent_cost_usd: float | None
        agent_cost_usd = self.agent_cost_usd

        compute_cost_usd: float | None
        compute_cost_usd = self.compute_cost_usd

        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd

        input_tokens: int | None
        input_tokens = self.input_tokens

        output_tokens: int | None
        output_tokens = self.output_tokens

        cache_read_input_tokens: int | None
        cache_read_input_tokens = self.cache_read_input_tokens

        cache_creation_input_tokens: int | None
        cache_creation_input_tokens = self.cache_creation_input_tokens

        resource_usage: dict[str, Any] | None
        if isinstance(self.resource_usage, ProblemRunUsageResponseDtoItemsItemResourceUsageType0):
            resource_usage = self.resource_usage.to_dict()
        else:
            resource_usage = self.resource_usage


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runType": run_type,
            "modelName": model_name,
            "agentCostUsd": agent_cost_usd,
            "computeCostUsd": compute_cost_usd,
            "totalCostUsd": total_cost_usd,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "cacheReadInputTokens": cache_read_input_tokens,
            "cacheCreationInputTokens": cache_creation_input_tokens,
            "resourceUsage": resource_usage,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_run_usage_response_dto_items_item_resource_usage_type_0 import ProblemRunUsageResponseDtoItemsItemResourceUsageType0 # noqa: PLC0415
        d = dict(src_dict)
        run_type = d.pop("runType")

        def _parse_model_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        model_name = _parse_model_name(d.pop("modelName"))


        def _parse_agent_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        agent_cost_usd = _parse_agent_cost_usd(d.pop("agentCostUsd"))


        def _parse_compute_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        compute_cost_usd = _parse_compute_cost_usd(d.pop("computeCostUsd"))


        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        def _parse_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        input_tokens = _parse_input_tokens(d.pop("inputTokens"))


        def _parse_output_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        output_tokens = _parse_output_tokens(d.pop("outputTokens"))


        def _parse_cache_read_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        cache_read_input_tokens = _parse_cache_read_input_tokens(d.pop("cacheReadInputTokens"))


        def _parse_cache_creation_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        cache_creation_input_tokens = _parse_cache_creation_input_tokens(d.pop("cacheCreationInputTokens"))


        def _parse_resource_usage(data: object) -> None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resource_usage_type_0 = ProblemRunUsageResponseDtoItemsItemResourceUsageType0.from_dict(data)



                return resource_usage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemRunUsageResponseDtoItemsItemResourceUsageType0, data)

        resource_usage = _parse_resource_usage(d.pop("resourceUsage"))


        problem_run_usage_response_dto_items_item = cls(
            run_type=run_type,
            model_name=model_name,
            agent_cost_usd=agent_cost_usd,
            compute_cost_usd=compute_cost_usd,
            total_cost_usd=total_cost_usd,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
            cache_creation_input_tokens=cache_creation_input_tokens,
            resource_usage=resource_usage,
        )

        return problem_run_usage_response_dto_items_item

