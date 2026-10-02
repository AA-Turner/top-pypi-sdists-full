from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_qa_trigger_body_dto_event import CreateQaTriggerBodyDtoEvent
from uuid import UUID






T = TypeVar("T", bound="CreateQaTriggerBodyDto")



@_attrs_define
class CreateQaTriggerBodyDto:
    """ Request body for creating a QA trigger that fires a QA job when a platform event occurs.

        Example:
            {'qaConfigId': 'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'event': 'solver_completed'}

        Attributes:
            qa_config_id (UUID): Stable QA-config identifier (UUID).
            event (CreateQaTriggerBodyDtoEvent): Platform event that fires this trigger.
     """

    qa_config_id: UUID
    event: CreateQaTriggerBodyDtoEvent
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        qa_config_id = str(self.qa_config_id)

        event = self.event.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "qaConfigId": qa_config_id,
            "event": event,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        qa_config_id = UUID(d.pop("qaConfigId"))




        event = CreateQaTriggerBodyDtoEvent(d.pop("event"))




        create_qa_trigger_body_dto = cls(
            qa_config_id=qa_config_id,
            event=event,
        )


        create_qa_trigger_body_dto.additional_properties = d
        return create_qa_trigger_body_dto

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
