from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFeedback")


@_attrs_define
class CreateFeedback:
    """
    Attributes:
        uuid (UUID):
        issue (str):
        evaluation (int):
        comment (Union[Unset, str]):
    """

    uuid: UUID
    issue: str
    evaluation: int
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        issue = self.issue

        evaluation = self.evaluation

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "issue": issue,
                "evaluation": evaluation,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        issue = d.pop("issue")

        evaluation = d.pop("evaluation")

        comment = d.pop("comment", UNSET)

        create_feedback = cls(
            uuid=uuid,
            issue=issue,
            evaluation=evaluation,
            comment=comment,
        )

        create_feedback.additional_properties = d
        return create_feedback

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
