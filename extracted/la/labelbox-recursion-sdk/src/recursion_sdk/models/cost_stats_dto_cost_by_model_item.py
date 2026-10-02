from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostStatsDtoCostByModelItem")



@_attrs_define
class CostStatsDtoCostByModelItem:
    """ Cost and token roll-up for a single model.

        Attributes:
            model (str): LLM model identifier.
            total_cost (float): Total cost spent on this model in USD.
            runs (float): Number of runs that used this model.
            input_tokens (float): Total input tokens sent to the model.
            output_tokens (float): Total output tokens produced by the model.
            cache_read_tokens (float): Total tokens served from prompt cache.
            cache_creation_tokens (float): Total tokens written to prompt cache.
     """

    model: str
    total_cost: float
    runs: float
    input_tokens: float
    output_tokens: float
    cache_read_tokens: float
    cache_creation_tokens: float





    def to_dict(self) -> dict[str, Any]:
        model = self.model

        total_cost = self.total_cost

        runs = self.runs

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        cache_read_tokens = self.cache_read_tokens

        cache_creation_tokens = self.cache_creation_tokens


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "model": model,
            "totalCost": total_cost,
            "runs": runs,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "cacheReadTokens": cache_read_tokens,
            "cacheCreationTokens": cache_creation_tokens,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model")

        total_cost = d.pop("totalCost")

        runs = d.pop("runs")

        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        cache_read_tokens = d.pop("cacheReadTokens")

        cache_creation_tokens = d.pop("cacheCreationTokens")

        cost_stats_dto_cost_by_model_item = cls(
            model=model,
            total_cost=total_cost,
            runs=runs,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_creation_tokens=cache_creation_tokens,
        )

        return cost_stats_dto_cost_by_model_item

