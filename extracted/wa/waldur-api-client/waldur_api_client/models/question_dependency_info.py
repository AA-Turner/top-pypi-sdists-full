from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.question_condition import QuestionCondition


T = TypeVar("T", bound="QuestionDependencyInfo")


@_attrs_define
class QuestionDependencyInfo:
    """
    Attributes:
        logic (str):
        conditions (list['QuestionCondition']):
    """

    logic: str
    conditions: list["QuestionCondition"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logic = self.logic

        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()
            conditions.append(conditions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logic": logic,
                "conditions": conditions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.question_condition import QuestionCondition

        d = dict(src_dict)
        logic = d.pop("logic")

        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = QuestionCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        question_dependency_info = cls(
            logic=logic,
            conditions=conditions,
        )

        question_dependency_info.additional_properties = d
        return question_dependency_info

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
