import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.action_taken_enum import ActionTakenEnum
from ..models.injection_severity_enum import InjectionSeverityEnum
from ..models.message_role_enum import MessageRoleEnum

T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """
    Attributes:
        uuid (UUID):
        thread (UUID):
        role (MessageRoleEnum):
        content (str):
        sequence_index (int):
        replaces (UUID):
        created (datetime.datetime):
        is_flagged (bool):
        severity (InjectionSeverityEnum):
        injection_categories (Any):
        pii_categories (Any):
        action_taken (ActionTakenEnum):
    """

    uuid: UUID
    thread: UUID
    role: MessageRoleEnum
    content: str
    sequence_index: int
    replaces: UUID
    created: datetime.datetime
    is_flagged: bool
    severity: InjectionSeverityEnum
    injection_categories: Any
    pii_categories: Any
    action_taken: ActionTakenEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        thread = str(self.thread)

        role = self.role.value

        content = self.content

        sequence_index = self.sequence_index

        replaces = str(self.replaces)

        created = self.created.isoformat()

        is_flagged = self.is_flagged

        severity = self.severity.value

        injection_categories = self.injection_categories

        pii_categories = self.pii_categories

        action_taken = self.action_taken.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "thread": thread,
                "role": role,
                "content": content,
                "sequence_index": sequence_index,
                "replaces": replaces,
                "created": created,
                "is_flagged": is_flagged,
                "severity": severity,
                "injection_categories": injection_categories,
                "pii_categories": pii_categories,
                "action_taken": action_taken,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        thread = UUID(d.pop("thread"))

        role = MessageRoleEnum(d.pop("role"))

        content = d.pop("content")

        sequence_index = d.pop("sequence_index")

        replaces = UUID(d.pop("replaces"))

        created = isoparse(d.pop("created"))

        is_flagged = d.pop("is_flagged")

        severity = InjectionSeverityEnum(d.pop("severity"))

        injection_categories = d.pop("injection_categories")

        pii_categories = d.pop("pii_categories")

        action_taken = ActionTakenEnum(d.pop("action_taken"))

        message = cls(
            uuid=uuid,
            thread=thread,
            role=role,
            content=content,
            sequence_index=sequence_index,
            replaces=replaces,
            created=created,
            is_flagged=is_flagged,
            severity=severity,
            injection_categories=injection_categories,
            pii_categories=pii_categories,
            action_taken=action_taken,
        )

        message.additional_properties = d
        return message

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
