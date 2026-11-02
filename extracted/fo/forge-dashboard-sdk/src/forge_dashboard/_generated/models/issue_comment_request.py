from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge






T = TypeVar("T", bound="IssueCommentRequest")



@_attrs_define
class IssueCommentRequest:
    """ Which issue to comment on, and what to say.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching an Issue.repo from GET /api/v1/dashboard.
            number (int): Matching an Issue.number from GET /api/v1/dashboard.
            body (str): The comment, as Markdown. Blank text is refused.
     """

    forge: Forge
    full_name: str
    number: int
    body: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        number = self.number

        body = self.body


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "number": number,
            "body": body,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        number = d.pop("number")

        body = d.pop("body")

        issue_comment_request = cls(
            forge=forge,
            full_name=full_name,
            number=number,
            body=body,
        )


        issue_comment_request.additional_properties = d
        return issue_comment_request

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
