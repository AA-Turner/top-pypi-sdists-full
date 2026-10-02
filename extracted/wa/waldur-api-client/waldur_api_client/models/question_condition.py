from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.question_condition_required_value import QuestionConditionRequiredValue


T = TypeVar("T", bound="QuestionCondition")


@_attrs_define
class QuestionCondition:
    """
    Attributes:
        question_description (str):
        operator (str):
        required_value (QuestionConditionRequiredValue):
    """

    question_description: str
    operator: str
    required_value: "QuestionConditionRequiredValue"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_description = self.question_description

        operator = self.operator

        required_value = self.required_value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_description": question_description,
                "operator": operator,
                "required_value": required_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.question_condition_required_value import QuestionConditionRequiredValue

        d = dict(src_dict)
        question_description = d.pop("question_description")

        operator = d.pop("operator")

        required_value = QuestionConditionRequiredValue.from_dict(d.pop("required_value"))

        question_condition = cls(
            question_description=question_description,
            operator=operator,
            required_value=required_value,
        )

        question_condition.additional_properties = d
        return question_condition

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
