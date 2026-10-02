from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.live_transcript_envelope_dto_events_item import LiveTranscriptEnvelopeDtoEventsItem





T = TypeVar("T", bound="LiveTranscriptEnvelopeDto")



@_attrs_define
class LiveTranscriptEnvelopeDto:
    """ Live transcript events together with the generation token of the run they came from.

        Attributes:
            events (list[LiveTranscriptEnvelopeDtoEventsItem]): Live transcript events, ordered by sequence ascending.
            generation (None | str): Opaque token identifying the run the events came from. It changes when the run is
                resubmitted and sequences restart, so a client holding an after cursor should discard what it holds and re-read;
                null while the job has no run yet.
     """

    events: list[LiveTranscriptEnvelopeDtoEventsItem]
    generation: None | str





    def to_dict(self) -> dict[str, Any]:
        from ..models.live_transcript_envelope_dto_events_item import LiveTranscriptEnvelopeDtoEventsItem # noqa: PLC0415
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)



        generation: None | str
        generation = self.generation


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "events": events,
            "generation": generation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.live_transcript_envelope_dto_events_item import LiveTranscriptEnvelopeDtoEventsItem # noqa: PLC0415
        d = dict(src_dict)
        events = []
        _events = d.pop("events")
        for events_item_data in (_events):
            events_item = LiveTranscriptEnvelopeDtoEventsItem.from_dict(events_item_data)



            events.append(events_item)


        def _parse_generation(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        generation = _parse_generation(d.pop("generation"))


        live_transcript_envelope_dto = cls(
            events=events,
            generation=generation,
        )

        return live_transcript_envelope_dto

