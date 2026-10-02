from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsUsage")



@_attrs_define
class ManagedAgentsUsage:
    """ Token counts and cost for a single unit of work, in the provider's usage vocabulary. Attached to an event's content
    for the model turn that produced it; see session usage for whole-session totals.

        Example:
            {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_usd': 1.5, 'input_tokens': 1, 'output_tokens': 1}

        Attributes:
            cache_read_tokens (int | Unset): Prompt tokens served from the provider's prompt cache, billed at the cached
                rate.
            cache_write_tokens (int | Unset): Prompt tokens written into the provider's prompt cache.
            cost_usd (float | Unset): Accrued cost in USD, derived from cost_micros for display.
            input_tokens (int | Unset): Prompt tokens billed for this unit of work.
            output_tokens (int | Unset): Completion tokens billed for this unit of work.
     """

    cache_read_tokens: int | Unset = UNSET
    cache_write_tokens: int | Unset = UNSET
    cost_usd: float | Unset = UNSET
    input_tokens: int | Unset = UNSET
    output_tokens: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        cost_usd = self.cost_usd

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if cost_usd is not UNSET:
            field_dict["cost_usd"] = cost_usd
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        cost_usd = d.pop("cost_usd", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        managed_agents_usage = cls(
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            cost_usd=cost_usd,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


        managed_agents_usage.additional_properties = d
        return managed_agents_usage

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
