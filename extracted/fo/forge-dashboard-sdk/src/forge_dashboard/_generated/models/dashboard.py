from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.auto_merged_pull_request import AutoMergedPullRequest
  from ..models.forge_health import ForgeHealth
  from ..models.issue import Issue
  from ..models.main_branches import MainBranches
  from ..models.nav_counts import NavCounts
  from ..models.pull_request import PullRequest
  from ..models.queued_action import QueuedAction
  from ..models.repo_status import RepoStatus





T = TypeVar("T", bound="Dashboard")



@_attrs_define
class Dashboard:
    """ 
        Attributes:
            queued_actions (list[QueuedAction]): The signed-in user's queued actions, waiting and finished in the
                last 24 hours (GET /api/v1/queued-actions), so a client lists them in
                its Activity panel and learns an outcome from the stream it
                already reads. Always present, empty when there are none.
            auto_merged (list[AutoMergedPullRequest]): Pull requests this app auto-merged in the last ten minutes, newest
                first. They have already left `pullRequests`, so this is how a
                client shows "Auto-merged owner/repo#N after checks passed". Always
                present, empty when there are none. A client shows each one once,
                matched on `forge`, `fullName`, `number` and `mergedAt`.
            open_issue_count (int): How many of `issues` are real work: all of them except the
                `housekeeping` ones. What the Issues badge shows.
            first_refresh_done (bool): False from process start until this viewer's first refresh has
                finished, whether it succeeded or failed; true from then on,
                including after later refreshes. Per viewer: another user's
                refresh does not flip it. A client shows a loading state instead
                of empty lists while it is false; a failed first refresh is
                reported through forge health, not by keeping this false. It is
                also true when the server started from the snapshot saved by its
                last run: those rows are on the page, and their forge reports
                `reachable: false` with `staleSince` until the first refresh
                succeeds. The same
                on `GET /api/v1/dashboard`, the stream and the MCP `get_dashboard`
                output. Always present. A client of an older server that
                lacks it should treat a missing flag as true (loaded).
            nav_counts (NavCounts): The numbers behind the navigation badges, counted from what the
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
            main_branch_page (MainBranches): Every default branch the page lists, in no particular order. There is
                no tally: a client counts the rows it holds, so the filter pills and
                the navigation badge always agree with the list.
            generated_at (datetime.datetime): When this snapshot was refreshed, not when it was requested.
            read_interval_seconds (int): How often, in seconds, a client should re-read GET
                /api/v1/dashboard. The server's advice, so a client needs no
                interval of its own. The read is cheap and never calls a
                forge; this is not the backend's refresh schedule. It is
                shorter (2) until the viewer's first refresh has finished, so a
                page that is still loading picks the data up soon after it is
                ready, and the normal 30 from then on.
            hidden_drafts (int): How many draft pull requests `pullRequests` leaves out. Always
                present, and `0` when the request set `includeDrafts=true`, so
                a client can render "N hidden" without a special case. Drafts
                in a repo the account ignores aren't counted, since none of
                that repo's pull requests show.
            forges (list[ForgeHealth]):
            pull_requests (list[PullRequest]):
            issues (list[Issue]):
            repos (list[RepoStatus]):
            settings_hidden_issue_count (int | Unset): How many open issues the user's own settings
                (`hideDependencyDashboard`
                and `ignoredTitles`) left out of `issues`, so a client can say
                "N hidden by your settings" and link to Settings; it cannot work
                that out, the issues are not sent. Always present once the
                server applies the settings; 0 when none are hidden.
            hidden_pull_requests (int | Unset): How many pull requests the user hid that are still open and not
                expired. Always present, so a client can render "Hidden (N)"
                without a special case. With `includeHidden=true` they are in
                `pullRequests`, marked `hidden`, and this still counts them.
     """

    queued_actions: list[QueuedAction]
    auto_merged: list[AutoMergedPullRequest]
    open_issue_count: int
    first_refresh_done: bool
    nav_counts: NavCounts
    main_branch_page: MainBranches
    generated_at: datetime.datetime
    read_interval_seconds: int
    hidden_drafts: int
    forges: list[ForgeHealth]
    pull_requests: list[PullRequest]
    issues: list[Issue]
    repos: list[RepoStatus]
    settings_hidden_issue_count: int | Unset = UNSET
    hidden_pull_requests: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_merged_pull_request import AutoMergedPullRequest # noqa: PLC0415
        from ..models.forge_health import ForgeHealth # noqa: PLC0415
        from ..models.issue import Issue # noqa: PLC0415
        from ..models.main_branches import MainBranches # noqa: PLC0415
        from ..models.nav_counts import NavCounts # noqa: PLC0415
        from ..models.pull_request import PullRequest # noqa: PLC0415
        from ..models.queued_action import QueuedAction # noqa: PLC0415
        from ..models.repo_status import RepoStatus # noqa: PLC0415
        queued_actions = []
        for queued_actions_item_data in self.queued_actions:
            queued_actions_item = queued_actions_item_data.to_dict()
            queued_actions.append(queued_actions_item)



        auto_merged = []
        for auto_merged_item_data in self.auto_merged:
            auto_merged_item = auto_merged_item_data.to_dict()
            auto_merged.append(auto_merged_item)



        open_issue_count = self.open_issue_count

        first_refresh_done = self.first_refresh_done

        nav_counts = self.nav_counts.to_dict()

        main_branch_page = self.main_branch_page.to_dict()

        generated_at = self.generated_at.isoformat()

        read_interval_seconds = self.read_interval_seconds

        hidden_drafts = self.hidden_drafts

        forges = []
        for forges_item_data in self.forges:
            forges_item = forges_item_data.to_dict()
            forges.append(forges_item)



        pull_requests = []
        for pull_requests_item_data in self.pull_requests:
            pull_requests_item = pull_requests_item_data.to_dict()
            pull_requests.append(pull_requests_item)



        issues = []
        for issues_item_data in self.issues:
            issues_item = issues_item_data.to_dict()
            issues.append(issues_item)



        repos = []
        for repos_item_data in self.repos:
            repos_item = repos_item_data.to_dict()
            repos.append(repos_item)



        settings_hidden_issue_count = self.settings_hidden_issue_count

        hidden_pull_requests = self.hidden_pull_requests


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "queuedActions": queued_actions,
            "autoMerged": auto_merged,
            "openIssueCount": open_issue_count,
            "firstRefreshDone": first_refresh_done,
            "navCounts": nav_counts,
            "mainBranchPage": main_branch_page,
            "generatedAt": generated_at,
            "readIntervalSeconds": read_interval_seconds,
            "hiddenDrafts": hidden_drafts,
            "forges": forges,
            "pullRequests": pull_requests,
            "issues": issues,
            "repos": repos,
        })
        if settings_hidden_issue_count is not UNSET:
            field_dict["settingsHiddenIssueCount"] = settings_hidden_issue_count
        if hidden_pull_requests is not UNSET:
            field_dict["hiddenPullRequests"] = hidden_pull_requests

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auto_merged_pull_request import AutoMergedPullRequest # noqa: PLC0415
        from ..models.forge_health import ForgeHealth # noqa: PLC0415
        from ..models.issue import Issue # noqa: PLC0415
        from ..models.main_branches import MainBranches # noqa: PLC0415
        from ..models.nav_counts import NavCounts # noqa: PLC0415
        from ..models.pull_request import PullRequest # noqa: PLC0415
        from ..models.queued_action import QueuedAction # noqa: PLC0415
        from ..models.repo_status import RepoStatus # noqa: PLC0415
        d = dict(src_dict)
        queued_actions = []
        _queued_actions = d.pop("queuedActions")
        for queued_actions_item_data in (_queued_actions):
            queued_actions_item = QueuedAction.from_dict(queued_actions_item_data)



            queued_actions.append(queued_actions_item)


        auto_merged = []
        _auto_merged = d.pop("autoMerged")
        for auto_merged_item_data in (_auto_merged):
            auto_merged_item = AutoMergedPullRequest.from_dict(auto_merged_item_data)



            auto_merged.append(auto_merged_item)


        open_issue_count = d.pop("openIssueCount")

        first_refresh_done = d.pop("firstRefreshDone")

        nav_counts = NavCounts.from_dict(d.pop("navCounts"))




        main_branch_page = MainBranches.from_dict(d.pop("mainBranchPage"))




        generated_at = datetime.datetime.fromisoformat(d.pop("generatedAt"))




        read_interval_seconds = d.pop("readIntervalSeconds")

        hidden_drafts = d.pop("hiddenDrafts")

        forges = []
        _forges = d.pop("forges")
        for forges_item_data in (_forges):
            forges_item = ForgeHealth.from_dict(forges_item_data)



            forges.append(forges_item)


        pull_requests = []
        _pull_requests = d.pop("pullRequests")
        for pull_requests_item_data in (_pull_requests):
            pull_requests_item = PullRequest.from_dict(pull_requests_item_data)



            pull_requests.append(pull_requests_item)


        issues = []
        _issues = d.pop("issues")
        for issues_item_data in (_issues):
            issues_item = Issue.from_dict(issues_item_data)



            issues.append(issues_item)


        repos = []
        _repos = d.pop("repos")
        for repos_item_data in (_repos):
            repos_item = RepoStatus.from_dict(repos_item_data)



            repos.append(repos_item)


        settings_hidden_issue_count = d.pop("settingsHiddenIssueCount", UNSET)

        hidden_pull_requests = d.pop("hiddenPullRequests", UNSET)

        dashboard = cls(
            queued_actions=queued_actions,
            auto_merged=auto_merged,
            open_issue_count=open_issue_count,
            first_refresh_done=first_refresh_done,
            nav_counts=nav_counts,
            main_branch_page=main_branch_page,
            generated_at=generated_at,
            read_interval_seconds=read_interval_seconds,
            hidden_drafts=hidden_drafts,
            forges=forges,
            pull_requests=pull_requests,
            issues=issues,
            repos=repos,
            settings_hidden_issue_count=settings_hidden_issue_count,
            hidden_pull_requests=hidden_pull_requests,
        )


        dashboard.additional_properties = d
        return dashboard

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
