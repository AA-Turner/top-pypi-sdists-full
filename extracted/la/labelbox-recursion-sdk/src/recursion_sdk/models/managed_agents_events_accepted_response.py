from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_events_accepted_response_delivery_state import ManagedAgentsEventsAcceptedResponseDeliveryState






T = TypeVar("T", bound="ManagedAgentsEventsAcceptedResponse")



@_attrs_define
class ManagedAgentsEventsAcceptedResponse:
    """ Shared response body of POST /v1/sessions/{session_id}/events and POST /v1/sessions/{session_id}/interrupt-and-send.
    It acknowledges durable acceptance of the turn, never the agent's reply: read the reply by listing events or
    streaming. Compare events_accepted against what was sent to detect silently dropped entries, and read delivery_state
    to learn whether an agent is actually going to act on them. events_accepted counts canonical events rather than
    requests, so interrupt-and-send reports 2 for its single instruction: the stop and the message that follows it.

        Example:
            {'delivery_state': 'stored', 'events_accepted': 1, 'ok': True, 'temporal_signaled': True}

        Attributes:
            delivery_state (ManagedAgentsEventsAcceptedResponseDeliveryState): How the accepted events reached a reader.
                queued: the agent was mid-turn, so the input is waiting outside the transcript and the next turn boundary will
                read it; interrupt to bring that forward. signaled: a running workflow was woken and will act on them. resumed:
                the session's workflow had already finished, so a new one was started to consume them. stored: appended to the
                timeline with nothing running to consume them yet.
            events_accepted (int): How many canonical events were written or queued. This counts the inputs actually derived
                from the body, not its length: a plain message body yields 1, and a typed event with an unrecognised type or no
                content is dropped, so this can be lower than the events array sent.
            ok (bool): Always true. Every event in the request was durably accepted; any partial or total failure is an HTTP
                error instead, so this field never reports false.
            temporal_signaled (bool): Compatibility bit, superseded by delivery_state: true when an existing workflow was
                signaled or a new one was started for this session. Read delivery_state instead, which tells those two cases
                apart.
     """

    delivery_state: ManagedAgentsEventsAcceptedResponseDeliveryState
    events_accepted: int
    ok: bool
    temporal_signaled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        delivery_state = self.delivery_state.value

        events_accepted = self.events_accepted

        ok = self.ok

        temporal_signaled = self.temporal_signaled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "delivery_state": delivery_state,
            "events_accepted": events_accepted,
            "ok": ok,
            "temporal_signaled": temporal_signaled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        delivery_state = ManagedAgentsEventsAcceptedResponseDeliveryState(d.pop("delivery_state"))




        events_accepted = d.pop("events_accepted")

        ok = d.pop("ok")

        temporal_signaled = d.pop("temporal_signaled")

        managed_agents_events_accepted_response = cls(
            delivery_state=delivery_state,
            events_accepted=events_accepted,
            ok=ok,
            temporal_signaled=temporal_signaled,
        )


        managed_agents_events_accepted_response.additional_properties = d
        return managed_agents_events_accepted_response

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
