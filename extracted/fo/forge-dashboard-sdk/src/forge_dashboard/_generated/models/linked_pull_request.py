from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.ci_status import CIStatus
from ..models.forge import Forge
from typing import cast

if TYPE_CHECKING:
  from ..models.check_counts import CheckCounts





T = TypeVar("T", bound="LinkedPullRequest")



@_attrs_define
class LinkedPullRequest:
    """ One open pull request that will close an issue when it merges.

        Attributes:
            forge (Forge):
            repo (str): The pull request's repository as `owner/name`, which is not always the issue's own.
            number (int):
            draft (bool): True while the pull request is a draft. Otherwise it is open.
            page_url (str): The address on this dashboard that opens the page listing the pull
                request, with its pop-up open: `/pull-requests.html`, `/releases.html`
                or `/bots.html`, whichever page lists that kind of pull request, then
                `?pr=` and `forge/owner/name/number`. A relative address.
            ci (CIStatus): The combined result across every check reported against the pull
                request's head commit. "none" means neither forge reported any
                check at all, not that one failed.

                This is the server's answer, and the server's rules read it: what a
                pull request may do, auto-merge, the quick filters, the navigation
                counts and the CI poll. The page draws it for a row it has no job
                facts for. For a row it has them for (the rows in view on the live
                stream), the page folds the jobs itself, so the pill it draws can
                differ from this field until the next refresh. A run that was only
                cancelled reads as cancelled in that fold; GitHub's rollup says
                `failure` and Forgejo's says `none` or `success` here.
            checks (CheckCounts): How many checks are in each state, so a client can say how far a
                pipeline is without opening it. It is on every pull request and on
                every default branch, for a passed, a failed and a running pipeline
                alike. The server tallies them from what it already reads to work out
                the overall state, so they cost no request. Always present, all zero
                when there are no checks.

                `waiting` is a check that has not started: queued, or pending where the
                forge doesn't tell queued from running. A failed pipeline can still have
                checks running or waiting, and says so. A pull request's counts agree
                with its `ci`: one whose `ci` is `pending` has `failed` at 0, and one
                whose `ci` is `success` has nothing running, waiting or failed. Two
                kinds of run are therefore in none of the four, as long as something
                else explains the state. A run held for approval: on a pull request
                `awaitingWorkflowApproval` says that. A cancelled run: a push or a
                concurrency group superseded it, and the overall state does not read it
                as a failure while others still run. When cancelled runs (and, on a
                branch, held ones) are the only reason a pipeline reads as failed, they
                count as `failed` (a held run first, where both are there), so a failed
                pipeline always has a failed count on GitHub. A branch whose status is
                `cancelled` has `failed` at 0. A timed-out or stale check counts as `failed`, a skipped,
                neutral or bare completed one as `passed`, on Forgejo too.

                `skipped` is a newer field and says how many of the `passed` checks
                were skipped. It never exceeds `passed`: it is inside `passed`, not
                beside it, so `passed` still counts every check that needs nothing more
                and the four states still add up to the checks the pipeline lists, bar
                the blocked jobs of a failed Forgejo run described below. The
                server always sends it, which is why it is required; a client that may
                talk to an older server may read a missing one as zero. A neutral or bare
                completed check is passed without being skipped. A client that draws the
                two side by side must subtract `skipped` from `passed` for the passed figure, or a skipped check is
                counted twice, and a pipeline where every passed check was skipped can
                read as skipped.

                On GitHub the counts come from the same rollup as the overall state,
                for a pull request and a branch alike; on Forgejo a pull request counts
                the statuses of the combined commit status, which only say pending, and
                takes the running ones out of the pending count by reading the jobs of
                the commit's runs that are still going. When a run has failed, a
                pending status of a job in a run that has failed is no wait: its
                needs failed, so Forgejo leaves it blocked and nothing will start it,
                and it is in none of the four. A default branch holds to the same: it
                counts the jobs of the workflow runs of the newest commit that has one,
                where a running job is `running`, a queued one `waiting`, and a blocked
                one `waiting` unless its run has failed, when it is in none of the four. A run
                whose jobs can't be read counts as one check by its own status. Forgejo
                answers one page of those statuses, and when its total says there are
                more than the page holds a pull request's counts are all zero rather
                than an undercount. When GitHub's rollup of a pull request is of an
                earlier commit than the head (a push still being processed), the counts
                are zero too. GitHub's unauthenticated fallback has no such counts, so
                there they are all zero.
            awaiting_workflow_approval (bool): The same flag as on the pull request itself: true when GitHub is
                holding a workflow run on the head commit until someone approves
                it. A client says "waiting for approval" rather than "check
                failed" while it is true. Always present; false on Forgejo.
     """

    forge: Forge
    repo: str
    number: int
    draft: bool
    page_url: str
    ci: CIStatus
    checks: CheckCounts
    awaiting_workflow_approval: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.check_counts import CheckCounts # noqa: PLC0415
        forge = self.forge.value

        repo = self.repo

        number = self.number

        draft = self.draft

        page_url = self.page_url

        ci = self.ci.value

        checks = self.checks.to_dict()

        awaiting_workflow_approval = self.awaiting_workflow_approval


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "repo": repo,
            "number": number,
            "draft": draft,
            "pageUrl": page_url,
            "ci": ci,
            "checks": checks,
            "awaitingWorkflowApproval": awaiting_workflow_approval,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_counts import CheckCounts # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        repo = d.pop("repo")

        number = d.pop("number")

        draft = d.pop("draft")

        page_url = d.pop("pageUrl")

        ci = CIStatus(d.pop("ci"))




        checks = CheckCounts.from_dict(d.pop("checks"))




        awaiting_workflow_approval = d.pop("awaitingWorkflowApproval")

        linked_pull_request = cls(
            forge=forge,
            repo=repo,
            number=number,
            draft=draft,
            page_url=page_url,
            ci=ci,
            checks=checks,
            awaiting_workflow_approval=awaiting_workflow_approval,
        )


        linked_pull_request.additional_properties = d
        return linked_pull_request

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
