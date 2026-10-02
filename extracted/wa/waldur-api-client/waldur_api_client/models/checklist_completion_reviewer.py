import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChecklistCompletionReviewer")


@_attrs_define
class ChecklistCompletionReviewer:
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
        requires_review (bool): Whether any answers triggered review requirements
        reviewed_by_name (str):
        review_trigger_summary (list[Any]):
        reviewed_by (Union[None, Unset, int]): User who reviewed the checklist completion
        reviewed_at (Union[None, Unset, datetime.datetime]):
        review_notes (Union[Unset, str]): Notes from the reviewer
    """

    uuid: UUID
    is_completed: bool
    completion_percentage: float
    unanswered_required_questions: list[Any]
    checklist_name: str
    checklist_description: str
    created: datetime.datetime
    modified: datetime.datetime
    requires_review: bool
    reviewed_by_name: str
    review_trigger_summary: list[Any]
    reviewed_by: Union[None, Unset, int] = UNSET
    reviewed_at: Union[None, Unset, datetime.datetime] = UNSET
    review_notes: Union[Unset, str] = UNSET
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

        requires_review = self.requires_review

        reviewed_by_name = self.reviewed_by_name

        review_trigger_summary = self.review_trigger_summary

        reviewed_by: Union[None, Unset, int]
        if isinstance(self.reviewed_by, Unset):
            reviewed_by = UNSET
        else:
            reviewed_by = self.reviewed_by

        reviewed_at: Union[None, Unset, str]
        if isinstance(self.reviewed_at, Unset):
            reviewed_at = UNSET
        elif isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        review_notes = self.review_notes

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
                "requires_review": requires_review,
                "reviewed_by_name": reviewed_by_name,
                "review_trigger_summary": review_trigger_summary,
            }
        )
        if reviewed_by is not UNSET:
            field_dict["reviewed_by"] = reviewed_by
        if reviewed_at is not UNSET:
            field_dict["reviewed_at"] = reviewed_at
        if review_notes is not UNSET:
            field_dict["review_notes"] = review_notes

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

        requires_review = d.pop("requires_review")

        reviewed_by_name = d.pop("reviewed_by_name")

        review_trigger_summary = cast(list[Any], d.pop("review_trigger_summary"))

        def _parse_reviewed_by(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by", UNSET))

        def _parse_reviewed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at", UNSET))

        review_notes = d.pop("review_notes", UNSET)

        checklist_completion_reviewer = cls(
            uuid=uuid,
            is_completed=is_completed,
            completion_percentage=completion_percentage,
            unanswered_required_questions=unanswered_required_questions,
            checklist_name=checklist_name,
            checklist_description=checklist_description,
            created=created,
            modified=modified,
            requires_review=requires_review,
            reviewed_by_name=reviewed_by_name,
            review_trigger_summary=review_trigger_summary,
            reviewed_by=reviewed_by,
            reviewed_at=reviewed_at,
            review_notes=review_notes,
        )

        checklist_completion_reviewer.additional_properties = d
        return checklist_completion_reviewer

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
