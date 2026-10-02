from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.agent_run_event_list_dto_item_event_type import AgentRunEventListDtoItemEventType
from typing import cast

if TYPE_CHECKING:
  from ..models.agent_run_event_list_dto_item_data import AgentRunEventListDtoItemData





T = TypeVar("T", bound="AgentRunEventListDtoItem")



@_attrs_define
class AgentRunEventListDtoItem:
    """ Single event emitted by the agent-service while running a solver or grader.

        Attributes:
            sequence (float): Monotonically increasing sequence number assigned by the agent-service.
            event_type (AgentRunEventListDtoItemEventType): Category of the event: lifecycle markers (started, launched,
                done, error), stdio (stdout, stderr), structured event payloads (event), agent observations (observation), and
                setup/snapshot phases.
            data (AgentRunEventListDtoItemData): Payload of the event; shape varies by event_type.
            created_at (str): Timestamp when the agent-service emitted the event (ISO-8601, UTC).
     """

    sequence: float
    event_type: AgentRunEventListDtoItemEventType
    data: AgentRunEventListDtoItemData
    created_at: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_run_event_list_dto_item_data import AgentRunEventListDtoItemData # noqa: PLC0415
        sequence = self.sequence

        event_type = self.event_type.value

        data = self.data.to_dict()

        created_at = self.created_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sequence": sequence,
            "event_type": event_type,
            "data": data,
            "created_at": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_run_event_list_dto_item_data import AgentRunEventListDtoItemData # noqa: PLC0415
        d = dict(src_dict)
        sequence = d.pop("sequence")

        event_type = AgentRunEventListDtoItemEventType(d.pop("event_type"))




        data = AgentRunEventListDtoItemData.from_dict(d.pop("data"))




        created_at = d.pop("created_at")

        agent_run_event_list_dto_item = cls(
            sequence=sequence,
            event_type=event_type,
            data=data,
            created_at=created_at,
        )

        return agent_run_event_list_dto_item

