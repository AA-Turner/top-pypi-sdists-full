from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedFeedback")


@_attrs_define
class NestedFeedback:
    """
    Attributes:
        evaluation (int): Customer satisfaction rating (1-5 stars)
        evaluation_number (int): Numeric value of the rating
        state (str): Current state of the feedback
        comment (Union[Unset, str]):
    """

    evaluation: int
    evaluation_number: int
    state: str
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        evaluation = self.evaluation

        evaluation_number = self.evaluation_number

        state = self.state

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "evaluation": evaluation,
                "evaluation_number": evaluation_number,
                "state": state,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        evaluation = d.pop("evaluation")

        evaluation_number = d.pop("evaluation_number")

        state = d.pop("state")

        comment = d.pop("comment", UNSET)

        nested_feedback = cls(
            evaluation=evaluation,
            evaluation_number=evaluation_number,
            state=state,
            comment=comment,
        )

        nested_feedback.additional_properties = d
        return nested_feedback

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
