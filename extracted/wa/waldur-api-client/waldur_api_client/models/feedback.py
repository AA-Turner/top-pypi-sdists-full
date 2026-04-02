import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.core_states import CoreStates
from ..types import UNSET, Unset

T = TypeVar("T", bound="Feedback")


@_attrs_define
class Feedback:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        state (CoreStates):
        evaluation (int):
        issue_uuid (UUID):
        user_full_name (str):
        issue_key (str):
        issue_summary (str):
        comment (Union[Unset, str]):
    """

    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    state: CoreStates
    evaluation: int
    issue_uuid: UUID
    user_full_name: str
    issue_key: str
    issue_summary: str
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        state = self.state.value

        evaluation = self.evaluation

        issue_uuid = str(self.issue_uuid)

        user_full_name = self.user_full_name

        issue_key = self.issue_key

        issue_summary = self.issue_summary

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "state": state,
                "evaluation": evaluation,
                "issue_uuid": issue_uuid,
                "user_full_name": user_full_name,
                "issue_key": issue_key,
                "issue_summary": issue_summary,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        state = CoreStates(d.pop("state"))

        evaluation = d.pop("evaluation")

        issue_uuid = UUID(d.pop("issue_uuid"))

        user_full_name = d.pop("user_full_name")

        issue_key = d.pop("issue_key")

        issue_summary = d.pop("issue_summary")

        comment = d.pop("comment", UNSET)

        feedback = cls(
            uuid=uuid,
            created=created,
            modified=modified,
            state=state,
            evaluation=evaluation,
            issue_uuid=issue_uuid,
            user_full_name=user_full_name,
            issue_key=issue_key,
            issue_summary=issue_summary,
            comment=comment,
        )

        feedback.additional_properties = d
        return feedback

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
