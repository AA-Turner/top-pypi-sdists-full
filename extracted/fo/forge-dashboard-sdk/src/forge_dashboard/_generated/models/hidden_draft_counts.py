from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="HiddenDraftCounts")



@_attrs_define
class HiddenDraftCounts:
    """ How many draft pull requests the board left out, per page that lists
    them: release pull requests under `releases`, Dependabot and Renovate
    under `bots`, the rest under `pullRequests`, the same split as
    `navCounts`. A page shows its Show drafts button only when its own
    number is above zero, so the button never appears on a page where it
    would reveal nothing. Always present, with zeros when there is nothing
    hidden or the request set `includeDrafts=true`.

        Attributes:
            pull_requests (int):
            releases (int):
            bots (int):
     """

    pull_requests: int
    releases: int
    bots: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        pull_requests = self.pull_requests

        releases = self.releases

        bots = self.bots


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pullRequests": pull_requests,
            "releases": releases,
            "bots": bots,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pull_requests = d.pop("pullRequests")

        releases = d.pop("releases")

        bots = d.pop("bots")

        hidden_draft_counts = cls(
            pull_requests=pull_requests,
            releases=releases,
            bots=bots,
        )


        hidden_draft_counts.additional_properties = d
        return hidden_draft_counts

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
