import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ChecklistCompletion")


@_attrs_define
class ChecklistCompletion:
    """
    Attributes:
        uuid (UUID):
        is_completed (bool): Whether all required questions have been answered
        completion_percentage (float):
        unanswered_required_questions (list[Any]):
        checklist_name (str):
        checklist_description (str):
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    is_completed: bool
    completion_percentage: float
    unanswered_required_questions: list[Any]
    checklist_name: str
    checklist_description: str
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        is_completed = self.is_completed

        completion_percentage = self.completion_percentage

        unanswered_required_questions = self.unanswered_required_questions

        checklist_name = self.checklist_name

        checklist_description = self.checklist_description

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "is_completed": is_completed,
                "completion_percentage": completion_percentage,
                "unanswered_required_questions": unanswered_required_questions,
                "checklist_name": checklist_name,
                "checklist_description": checklist_description,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        is_completed = d.pop("is_completed")

        completion_percentage = d.pop("completion_percentage")

        unanswered_required_questions = cast(list[Any], d.pop("unanswered_required_questions"))

        checklist_name = d.pop("checklist_name")

        checklist_description = d.pop("checklist_description")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        checklist_completion = cls(
            uuid=uuid,
            is_completed=is_completed,
            completion_percentage=completion_percentage,
            unanswered_required_questions=unanswered_required_questions,
            checklist_name=checklist_name,
            checklist_description=checklist_description,
            created=created,
            modified=modified,
        )

        checklist_completion.additional_properties = d
        return checklist_completion

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
