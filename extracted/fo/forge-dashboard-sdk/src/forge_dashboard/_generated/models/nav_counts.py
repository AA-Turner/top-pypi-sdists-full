from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.nav_issue_count import NavIssueCount
  from ..models.nav_pull_request_count import NavPullRequestCount





T = TypeVar("T", bound="NavCounts")



@_attrs_define
class NavCounts:
    """ The numbers behind the navigation badges, counted from what the
    board shows by default, so they match each page when it opens. Pull
    requests leave out ignored repos, draft pull requests and hidden pull
    requests whatever `includeDrafts` and `includeHidden` ask for, so the
    badge doesn't jump when a toggle flips. Pull requests are
    split by `kind`
    (release pull requests under `releases`, Dependabot and Renovate
    under `bots`, the rest under `pullRequests`). Always present, with
    zeros when there is nothing. A client hides a page's whole nav item at
    zero total, and a state's number at zero. Every page except Issues also
    carries `running` and `passed`. The Branches badge isn't here: a
    client counts the rows of `mainBranchPage`.

        Attributes:
            pull_requests (NavPullRequestCount): A pull request page's numbers. `running`, `failed` and
                `passed` count the pull requests whose CI is pending, failing and
                succeeded. A pull request with no checks counts in `total` only, so
                the four numbers need not add up. All four are always present.
            issues (NavIssueCount):
            releases (NavPullRequestCount): A pull request page's numbers. `running`, `failed` and
                `passed` count the pull requests whose CI is pending, failing and
                succeeded. A pull request with no checks counts in `total` only, so
                the four numbers need not add up. All four are always present.
            bots (NavPullRequestCount): A pull request page's numbers. `running`, `failed` and
                `passed` count the pull requests whose CI is pending, failing and
                succeeded. A pull request with no checks counts in `total` only, so
                the four numbers need not add up. All four are always present.
     """

    pull_requests: NavPullRequestCount
    issues: NavIssueCount
    releases: NavPullRequestCount
    bots: NavPullRequestCount
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.nav_issue_count import NavIssueCount # noqa: PLC0415
        from ..models.nav_pull_request_count import NavPullRequestCount # noqa: PLC0415
        pull_requests = self.pull_requests.to_dict()

        issues = self.issues.to_dict()

        releases = self.releases.to_dict()

        bots = self.bots.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pullRequests": pull_requests,
            "issues": issues,
            "releases": releases,
            "bots": bots,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nav_issue_count import NavIssueCount # noqa: PLC0415
        from ..models.nav_pull_request_count import NavPullRequestCount # noqa: PLC0415
        d = dict(src_dict)
        pull_requests = NavPullRequestCount.from_dict(d.pop("pullRequests"))




        issues = NavIssueCount.from_dict(d.pop("issues"))




        releases = NavPullRequestCount.from_dict(d.pop("releases"))




        bots = NavPullRequestCount.from_dict(d.pop("bots"))




        nav_counts = cls(
            pull_requests=pull_requests,
            issues=issues,
            releases=releases,
            bots=bots,
        )


        nav_counts.additional_properties = d
        return nav_counts

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
