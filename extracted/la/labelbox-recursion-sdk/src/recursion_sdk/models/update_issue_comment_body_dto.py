from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UpdateIssueCommentBodyDto")



@_attrs_define
class UpdateIssueCommentBodyDto:
    """ Request body for editing an existing issue comment.

        Example:
            {'content': 'The detect-surface-defects grader is flagging clean parts as defective — looks like the brightness
                threshold is too aggressive. Can we lower it before the next eval run? (Edit: confirmed with the dataset owner —
                proceeding with the threshold change.)'}

        Attributes:
            content (str): Replacement comment body.
     """

    content: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        content = self.content


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "content": content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        update_issue_comment_body_dto = cls(
            content=content,
        )


        update_issue_comment_body_dto.additional_properties = d
        return update_issue_comment_body_dto

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
