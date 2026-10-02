from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsPullRequestSummary")



@_attrs_define
class ManagedAgentsPullRequestSummary:
    """ The picker-safe identity and immutable head of one GitHub pull request reachable through an integration connection.

        Example:
            {'draft': True, 'head_sha': 'example', 'number': 1, 'title': 'example'}

        Attributes:
            draft (bool): Whether GitHub currently marks this pull request as a draft.
            head_sha (str): Immutable head commit SHA observed when this pull request was listed.
            number (int): GitHub pull request number within the repository.
            title (str): GitHub pull request title to display in a picker.
     """

    draft: bool
    head_sha: str
    number: int
    title: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        draft = self.draft

        head_sha = self.head_sha

        number = self.number

        title = self.title


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "draft": draft,
            "head_sha": head_sha,
            "number": number,
            "title": title,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        draft = d.pop("draft")

        head_sha = d.pop("head_sha")

        number = d.pop("number")

        title = d.pop("title")

        managed_agents_pull_request_summary = cls(
            draft=draft,
            head_sha=head_sha,
            number=number,
            title=title,
        )


        managed_agents_pull_request_summary.additional_properties = d
        return managed_agents_pull_request_summary

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
