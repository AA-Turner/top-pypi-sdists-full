from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.rollout_trace_response_dto_events_item import RolloutTraceResponseDtoEventsItem





T = TypeVar("T", bound="RolloutTraceResponseDto")



@_attrs_define
class RolloutTraceResponseDto:
    """ A single rollout's trace events, proxied from agent-service after verifying the rollout belongs to the requested
    job.

        Example:
            {'events': [], 'truncated': False, 'generation': None}

        Attributes:
            events (list[RolloutTraceResponseDtoEventsItem]): The rollout run's agent-service event stream, oldest first.
            truncated (bool): True when the event stream was trimmed to the most recent window.
            generation (None | str | Unset): Opaque token identifying the run the events came from. It changes when the run
                is resubmitted and sequences restart, so a client holding an after cursor should discard what it holds and re-
                read; null while the job has no run yet.
     """

    events: list[RolloutTraceResponseDtoEventsItem]
    truncated: bool
    generation: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.rollout_trace_response_dto_events_item import RolloutTraceResponseDtoEventsItem # noqa: PLC0415
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)



        truncated = self.truncated

        generation: None | str | Unset
        if isinstance(self.generation, Unset):
            generation = UNSET
        else:
            generation = self.generation


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "events": events,
            "truncated": truncated,
        })
        if generation is not UNSET:
            field_dict["generation"] = generation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rollout_trace_response_dto_events_item import RolloutTraceResponseDtoEventsItem # noqa: PLC0415
        d = dict(src_dict)
        events = []
        _events = d.pop("events")
        for events_item_data in (_events):
            events_item = RolloutTraceResponseDtoEventsItem.from_dict(events_item_data)



            events.append(events_item)


        truncated = d.pop("truncated")

        def _parse_generation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generation = _parse_generation(d.pop("generation", UNSET))


        rollout_trace_response_dto = cls(
            events=events,
            truncated=truncated,
            generation=generation,
        )

        return rollout_trace_response_dto

