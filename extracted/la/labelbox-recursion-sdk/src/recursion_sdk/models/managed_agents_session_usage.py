from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsSessionUsage")



@_attrs_define
class ManagedAgentsSessionUsage:
    """ Token and cost totals for one session, summed over that session's own events. Scoped to the session's own timeline
    and not its subtree, so a delegating session's totals exclude its children.

        Example:
            {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_micros': 1, 'event_count': 1, 'input_tokens': 1,
                'output_tokens': 1, 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            cache_read_tokens (int): Prompt tokens served from the provider's prompt cache, billed at the cached rate.
            cache_write_tokens (int): Prompt tokens written into the provider's prompt cache.
            cost_micros (int): Accrued cost in micro-USD (1,000,000 = 1 USD). Integer to avoid float rounding across many
                small charges.
            event_count (int): How many of the session's own events were summed to produce these totals.
            input_tokens (int): Prompt tokens billed for this unit of work.
            output_tokens (int): Completion tokens billed for this unit of work.
            session_id (str): Session these totals cover (UUID).
     """

    cache_read_tokens: int
    cache_write_tokens: int
    cost_micros: int
    event_count: int
    input_tokens: int
    output_tokens: int
    session_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        cost_micros = self.cost_micros

        event_count = self.event_count

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        session_id = self.session_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cache_read_tokens": cache_read_tokens,
            "cache_write_tokens": cache_write_tokens,
            "cost_micros": cost_micros,
            "event_count": event_count,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "session_id": session_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_read_tokens = d.pop("cache_read_tokens")

        cache_write_tokens = d.pop("cache_write_tokens")

        cost_micros = d.pop("cost_micros")

        event_count = d.pop("event_count")

        input_tokens = d.pop("input_tokens")

        output_tokens = d.pop("output_tokens")

        session_id = d.pop("session_id")

        managed_agents_session_usage = cls(
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            cost_micros=cost_micros,
            event_count=event_count,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            session_id=session_id,
        )


        managed_agents_session_usage.additional_properties = d
        return managed_agents_session_usage

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
