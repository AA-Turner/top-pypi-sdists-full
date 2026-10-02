from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_trigger_response_array_dto_item_event import QaTriggerResponseArrayDtoItemEvent
from uuid import UUID






T = TypeVar("T", bound="QaTriggerResponseArrayDtoItem")



@_attrs_define
class QaTriggerResponseArrayDtoItem:
    """ A QA trigger that fires a QA job on an environment when a platform event occurs.

        Attributes:
            id (UUID): Stable QA-trigger identifier (UUID). A trigger fires a QA job when a platform event occurs.
            environment_id (UUID): Stable environment identifier (UUID).
            qa_config_id (UUID): Stable QA-config identifier (UUID).
            qa_config_name (str): Display name of the QA config bound to the trigger.
            event (QaTriggerResponseArrayDtoItemEvent): Platform event that fires this trigger.
            created_at (str): Timestamp when the trigger was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the trigger was last updated (ISO-8601, UTC).
     """

    id: UUID
    environment_id: UUID
    qa_config_id: UUID
    qa_config_name: str
    event: QaTriggerResponseArrayDtoItemEvent
    created_at: str
    updated_at: str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        qa_config_id = str(self.qa_config_id)

        qa_config_name = self.qa_config_name

        event = self.event.value

        created_at = self.created_at

        updated_at = self.updated_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "qaConfigId": qa_config_id,
            "qaConfigName": qa_config_name,
            "event": event,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        qa_config_id = UUID(d.pop("qaConfigId"))




        qa_config_name = d.pop("qaConfigName")

        event = QaTriggerResponseArrayDtoItemEvent(d.pop("event"))




        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        qa_trigger_response_array_dto_item = cls(
            id=id,
            environment_id=environment_id,
            qa_config_id=qa_config_id,
            qa_config_name=qa_config_name,
            event=event,
            created_at=created_at,
            updated_at=updated_at,
        )

        return qa_trigger_response_array_dto_item

