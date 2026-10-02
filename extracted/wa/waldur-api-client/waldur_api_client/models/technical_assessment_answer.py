from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.technical_assessment_answer_answer_data import TechnicalAssessmentAnswerAnswerData


T = TypeVar("T", bound="TechnicalAssessmentAnswer")


@_attrs_define
class TechnicalAssessmentAnswer:
    """
    Attributes:
        question_uuid (UUID):
        question_description (str):
        question_type (str):
        answer_data (TechnicalAssessmentAnswerAnswerData):
        answer_display (Union[None, str]):
    """

    question_uuid: UUID
    question_description: str
    question_type: str
    answer_data: "TechnicalAssessmentAnswerAnswerData"
    answer_display: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_uuid = str(self.question_uuid)

        question_description = self.question_description

        question_type = self.question_type

        answer_data = self.answer_data.to_dict()

        answer_display: Union[None, str]
        answer_display = self.answer_display

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
                "question_description": question_description,
                "question_type": question_type,
                "answer_data": answer_data,
                "answer_display": answer_display,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.technical_assessment_answer_answer_data import TechnicalAssessmentAnswerAnswerData

        d = dict(src_dict)
        question_uuid = UUID(d.pop("question_uuid"))

        question_description = d.pop("question_description")

        question_type = d.pop("question_type")

        answer_data = TechnicalAssessmentAnswerAnswerData.from_dict(d.pop("answer_data"))

        def _parse_answer_display(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        answer_display = _parse_answer_display(d.pop("answer_display"))

        technical_assessment_answer = cls(
            question_uuid=question_uuid,
            question_description=question_description,
            question_type=question_type,
            answer_data=answer_data,
            answer_display=answer_display,
        )

        technical_assessment_answer.additional_properties = d
        return technical_assessment_answer

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
