from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_source_last_delivery_response_type_0_disposition import ManagedAgentsEventSourceLastDeliveryResponseType0Disposition
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsEventSourceLastDeliveryResponseType0")



@_attrs_define
class ManagedAgentsEventSourceLastDeliveryResponseType0:
    """ Most recent verified delivery observed for the source.

        Example:
            {'disposition': 'admitted', 'receivedAt': '2026-02-18T09:30:00Z'}

        Attributes:
            disposition (ManagedAgentsEventSourceLastDeliveryResponseType0Disposition): Whether the most recent verified
                delivery was admitted for processing.
            received_at (datetime.datetime): Time the most recent verified delivery reached the source.
     """

    disposition: ManagedAgentsEventSourceLastDeliveryResponseType0Disposition
    received_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        disposition = self.disposition.value

        received_at = self.received_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "disposition": disposition,
            "receivedAt": received_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disposition = ManagedAgentsEventSourceLastDeliveryResponseType0Disposition(d.pop("disposition"))




        received_at = datetime.datetime.fromisoformat(d.pop("receivedAt"))




        managed_agents_event_source_last_delivery_response_type_0 = cls(
            disposition=disposition,
            received_at=received_at,
        )

        return managed_agents_event_source_last_delivery_response_type_0

