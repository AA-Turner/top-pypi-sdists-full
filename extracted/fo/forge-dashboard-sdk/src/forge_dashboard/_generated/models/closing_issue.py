from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ClosingIssue")



@_attrs_define
class ClosingIssue:
    """ One issue a pull request will close when it merges.

        Attributes:
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
     """

    repo: str
    number: int
    url: str
    page_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        repo = self.repo

        number = self.number

        url = self.url

        page_url = self.page_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "repo": repo,
            "number": number,
            "url": url,
            "pageUrl": page_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo = d.pop("repo")

        number = d.pop("number")

        url = d.pop("url")

        page_url = d.pop("pageUrl")

        closing_issue = cls(
            repo=repo,
            number=number,
            url=url,
            page_url=page_url,
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
