import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.broadcast_message_query_request import BroadcastMessageQueryRequest


T = TypeVar("T", bound="FeedbackSurveyRequest")


@_attrs_define
class FeedbackSurveyRequest:
    """
    Attributes:
        name (str):
        checklist (UUID):
        starts_at (datetime.datetime):
        ends_at (datetime.datetime):
        audience_query (BroadcastMessageQueryRequest):
        intro (Union[Unset, str]): Markdown text shown above the questions.
        is_active (Union[Unset, bool]):
        max_prompts (Union[Unset, int]): How many times a user is prompted at most.
        snooze_days (Union[Unset, int]): Days the prompt stays hidden after it is shown or postponed.
    """

    name: str
    checklist: UUID
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    audience_query: "BroadcastMessageQueryRequest"
    intro: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    max_prompts: Union[Unset, int] = UNSET
    snooze_days: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        checklist = str(self.checklist)

        starts_at = self.starts_at.isoformat()

        ends_at = self.ends_at.isoformat()

        audience_query = self.audience_query.to_dict()

        intro = self.intro

        is_active = self.is_active

        max_prompts = self.max_prompts

        snooze_days = self.snooze_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "checklist": checklist,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "audience_query": audience_query,
            }
        )
        if intro is not UNSET:
            field_dict["intro"] = intro
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if max_prompts is not UNSET:
            field_dict["max_prompts"] = max_prompts
        if snooze_days is not UNSET:
            field_dict["snooze_days"] = snooze_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.broadcast_message_query_request import BroadcastMessageQueryRequest

        d = dict(src_dict)
        name = d.pop("name")

        checklist = UUID(d.pop("checklist"))

        starts_at = isoparse(d.pop("starts_at"))

        ends_at = isoparse(d.pop("ends_at"))

        audience_query = BroadcastMessageQueryRequest.from_dict(d.pop("audience_query"))

        intro = d.pop("intro", UNSET)

        is_active = d.pop("is_active", UNSET)

        max_prompts = d.pop("max_prompts", UNSET)

        snooze_days = d.pop("snooze_days", UNSET)

        feedback_survey_request = cls(
            name=name,
            checklist=checklist,
            starts_at=starts_at,
            ends_at=ends_at,
            audience_query=audience_query,
            intro=intro,
            is_active=is_active,
            max_prompts=max_prompts,
            snooze_days=snooze_days,
        )

        feedback_survey_request.additional_properties = d
        return feedback_survey_request

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
