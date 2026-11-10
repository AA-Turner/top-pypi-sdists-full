import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeedbackSurveyPublic")


@_attrs_define
class FeedbackSurveyPublic:
    """
    Attributes:
        uuid (UUID):
        name (str):
        ends_at (datetime.datetime):
        intro (Union[Unset, str]): Markdown text shown above the questions.
    """

    uuid: UUID
    name: str
    ends_at: datetime.datetime
    intro: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        ends_at = self.ends_at.isoformat()

        intro = self.intro

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "ends_at": ends_at,
            }
        )
        if intro is not UNSET:
            field_dict["intro"] = intro

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        ends_at = isoparse(d.pop("ends_at"))

        intro = d.pop("intro", UNSET)

        feedback_survey_public = cls(
            uuid=uuid,
            name=name,
            ends_at=ends_at,
            intro=intro,
        )

        feedback_survey_public.additional_properties = d
        return feedback_survey_public

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
