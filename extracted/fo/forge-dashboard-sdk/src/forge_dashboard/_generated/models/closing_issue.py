from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.issue_relation import IssueRelation
from ..types import UNSET, Unset






T = TypeVar("T", bound="ClosingIssue")



@_attrs_define
class ClosingIssue:
    """ One issue a pull request will close when it merges.

        Attributes:
            relation (IssueRelation): How a pull request relates to an issue: `closes` (it will close the
                issue on merge), `refs` (it says Refs, Ref, Related to or See, so it
                works on an issue that stays open) or `mentions` (the issue is named
                in passing). A pull request holds an issue under one relation, closes
                first.
            repo (str): The issue's repository as `owner/name`, which is not always the pull request's own.
            number (int):
            url (str): The issue's page on its forge.
            page_url (str): The address on this dashboard that opens the Issues page with this
                issue's pop-up open: `/issues.html?issue=` and
                `forge/owner/name/number`, on the pull request's own forge. A
                relative address. When the issue is closed, hidden by the user's
                settings or in a repo the dashboard does not track, the page opens
                no pop-up and shows a plain note over the list. The note has no
                forge link, since the dashboard knows nothing else about the issue.
            title (str | Unset): The issue's title as the board holds it, so a client can show it
                on hover. Left out when the dashboard does not hold the issue
                (closed, in a repo it does not track), and a client then words
                the pill without it. Text, never markup.
     """

    relation: IssueRelation
    repo: str
    number: int
    url: str
    page_url: str
    title: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        relation = self.relation.value

        repo = self.repo

        number = self.number

        url = self.url

        page_url = self.page_url

        title = self.title


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "relation": relation,
            "repo": repo,
            "number": number,
            "url": url,
            "pageUrl": page_url,
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

        title = d.pop("title", UNSET)

        closing_issue = cls(
            relation=relation,
            repo=repo,
            number=number,
            url=url,
            page_url=page_url,
            title=title,
        )


        closing_issue.additional_properties = d
        return closing_issue

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
