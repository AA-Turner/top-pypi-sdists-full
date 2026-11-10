from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feedback_survey_public import FeedbackSurveyPublic


T = TypeVar("T", bound="FeedbackPrompt")


@_attrs_define
class FeedbackPrompt:
    """
    Attributes:
        request_uuid (UUID):
        survey (FeedbackSurveyPublic):
    """

    request_uuid: UUID
    survey: "FeedbackSurveyPublic"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_uuid = str(self.request_uuid)

        survey = self.survey.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request_uuid": request_uuid,
                "survey": survey,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feedback_survey_public import FeedbackSurveyPublic

        d = dict(src_dict)
        request_uuid = UUID(d.pop("request_uuid"))

        survey = FeedbackSurveyPublic.from_dict(d.pop("survey"))

        feedback_prompt = cls(
            request_uuid=request_uuid,
            survey=survey,
        )

        feedback_prompt.additional_properties = d
        return feedback_prompt

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
