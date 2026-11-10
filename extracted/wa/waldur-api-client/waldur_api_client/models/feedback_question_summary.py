from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feedback_distribution_item import FeedbackDistributionItem


T = TypeVar("T", bound="FeedbackQuestionSummary")


@_attrs_define
class FeedbackQuestionSummary:
    """
    Attributes:
        question_uuid (str):
        question (str):
        question_type (str):
        answer_count (int):
        mean (Union[None, float]):
        distribution (list['FeedbackDistributionItem']):
    """

    question_uuid: str
    question: str
    question_type: str
    answer_count: int
    mean: Union[None, float]
    distribution: list["FeedbackDistributionItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_uuid = self.question_uuid

        question = self.question

        question_type = self.question_type

        answer_count = self.answer_count

        mean: Union[None, float]
        mean = self.mean

        distribution = []
        for distribution_item_data in self.distribution:
            distribution_item = distribution_item_data.to_dict()
            distribution.append(distribution_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_uuid": question_uuid,
                "question": question,
                "question_type": question_type,
                "answer_count": answer_count,
                "mean": mean,
                "distribution": distribution,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feedback_distribution_item import FeedbackDistributionItem

        d = dict(src_dict)
        question_uuid = d.pop("question_uuid")

        question = d.pop("question")

        question_type = d.pop("question_type")

        answer_count = d.pop("answer_count")

        def _parse_mean(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        mean = _parse_mean(d.pop("mean"))

        distribution = []
        _distribution = d.pop("distribution")
        for distribution_item_data in _distribution:
            distribution_item = FeedbackDistributionItem.from_dict(distribution_item_data)

            distribution.append(distribution_item)

        feedback_question_summary = cls(
            question_uuid=question_uuid,
            question=question,
            question_type=question_type,
            answer_count=answer_count,
            mean=mean,
            distribution=distribution,
        )

        feedback_question_summary.additional_properties = d
        return feedback_question_summary

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
