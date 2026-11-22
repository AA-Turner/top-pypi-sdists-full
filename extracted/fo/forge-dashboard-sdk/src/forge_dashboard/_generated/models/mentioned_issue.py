from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_relation import IssueRelation
from ..types import UNSET, Unset






T = TypeVar("T", bound="MentionedIssue")



@_attrs_define
class MentionedIssue:
    """ One issue or pull request a pull request mentions or references
    without closing it. The number is an issue's or a pull request's,
    which the forge's address tells apart.

        Attributes:
            relation (IssueRelation): How a pull request relates to an issue: `closes` (it will close the
                issue on merge), `refs` (it says Refs, Ref, Related to or See, so it
                works on an issue that stays open) or `mentions` (the issue is named
                in passing). A pull request holds an issue under one relation, closes
                first.
            repo (str): The repository as `owner/name`, which is not always the pull request's own.
            number (int):
            url (str): Its page on the forge, which a client links to when `tracked` is false.
            page_url (str): The address on this dashboard that opens the Issues page with this
                issue's pop-up open, built the same way as the closing issue's. A
                relative address.
            tracked (bool): True when the dashboard holds it as an open issue it shows, so
                `pageUrl` opens its pop-up. False for a pull request, a closed
                issue, an issue the user's settings hide and anything in a repo
                the dashboard does not track; a client then links to `url`.
            title (str | Unset): The title of the issue or pull request as the board holds it, so
                a client can show it on hover. Left out when the dashboard does
                not hold it, and a client then words the pill without it. Text,
                never markup.
     """

    relation: IssueRelation
    repo: str
    number: int
    url: str
    page_url: str
    tracked: bool
    title: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        relation = self.relation.value

        repo = self.repo

        number = self.number

        url = self.url

        page_url = self.page_url

        tracked = self.tracked

        title = self.title


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "relation": relation,
            "repo": repo,
            "number": number,
            "url": url,
            "pageUrl": page_url,
            "tracked": tracked,
        })
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        relation = IssueRelation(d.pop("relation"))




        repo = d.pop("repo")

        number = d.pop("number")

        url = d.pop("url")

        page_url = d.pop("pageUrl")

        tracked = d.pop("tracked")

        title = d.pop("title", UNSET)

        mentioned_issue = cls(
            relation=relation,
            repo=repo,
            number=number,
            url=url,
            page_url=page_url,
            tracked=tracked,
            title=title,
        )


        mentioned_issue.additional_properties = d
        return mentioned_issue

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
