from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="MentionedIssue")



@_attrs_define
class MentionedIssue:
    """ One issue or pull request a pull request mentions without closing it.
    The number is an issue's or a pull request's, which the forge's address
    tells apart.

        Attributes:
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
     """

    repo: str
    number: int
    url: str
    page_url: str
    tracked: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        repo = self.repo

        number = self.number

        url = self.url

        page_url = self.page_url

        tracked = self.tracked


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "repo": repo,
            "number": number,
            "url": url,
            "pageUrl": page_url,
            "tracked": tracked,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo = d.pop("repo")

        number = d.pop("number")

        url = d.pop("url")

        page_url = d.pop("pageUrl")

        tracked = d.pop("tracked")

        mentioned_issue = cls(
            repo=repo,
            number=number,
            url=url,
            page_url=page_url,
            tracked=tracked,
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
