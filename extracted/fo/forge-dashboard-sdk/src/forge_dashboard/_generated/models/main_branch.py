from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..models.main_branch_status import MainBranchStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.advisories import Advisories
  from ..models.check_counts import CheckCounts
  from ..models.main_branch_commit import MainBranchCommit
  from ..models.main_branch_release import MainBranchRelease
  from ..models.main_branch_run import MainBranchRun





T = TypeVar("T", bound="MainBranch")



@_attrs_define
class MainBranch:
    """ One tracked repository and the CI status of its default branch.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching a Repo.fullName from GET /api/v1/dashboard.
            url (str): The repository's own page on its forge.
            branch (str): The repository's default branch. Empty for a repository the forge reports no default branch for.
            status (MainBranchStatus): The result of the latest pipeline on a default branch's newest
                commit, across all its workflows. "failed" when any job failed,
                "running" when none failed and some are still queued or running,
                "cancelled" when nothing failed and nothing is running but some run
                was cancelled (a newer push or a person stopped it, so nothing broke),
                "awaiting_approval" when GitHub holds the commit's workflow runs until
                a maintainer approves them (they create no check runs, so nothing
                runs), "passed" when all finished green, "none" when the commit has
                no pipeline at all (or the repository has no commit yet).

                This is the server's answer, and the CI poll and the MCP tools read
                it. The page folds the branch's `runs` into the pill, the counts and
                the failing jobs itself, and draws this field only for a row with no
                `runs` or whose job list was cut short (`jobsTruncated`). A branch
                whose only trouble is a cancelled run reads as cancelled in both.
            commit (MainBranchCommit | None): The newest commit, or null when the forge reported none (an empty repository,
                or no run on Forgejo to name one from).
            failing_jobs (list[str]): The names of the failed jobs (GitHub checks, Forgejo Actions
                jobs), or of the failed workflow when its jobs couldn't be read.
                Always present and empty unless `status` is "failed".
            finished_at (datetime.datetime | None): When the pipeline's last job finished. Null while it runs, or when the
                forge didn't say.
            duration_seconds (int | None): How long the pipeline ran, from its first job starting to its last
                finishing. On GitHub it is the run that finished last, alone, since
                a commit's workflows run on their own schedules and days can pass
                between two of them. Null while it runs, or when the forge didn't
                say.
            run_url (str): Where to see the run on the forge: the failed job's page for a
                failed pipeline, else the run's, else the commit's. Falls back to
                the repository's `url`.
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
                as a failure while others still run. When a held run (and, on a
                branch, cancelled ones) is the only reason a pipeline reads as failed,
                the held run counts as `failed` with the cancelled ones, so a failed
                pipeline always has a failed count on GitHub. A pull request whose `ci`
                is `cancelled`, and a branch whose status is `cancelled`, have `failed`
                at 0; the pull request counts its cancelled runs in `cancelled`. A timed-out or stale check counts as `failed`,
                a skipped,
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
            latest_release (MainBranchRelease | None): The repository's latest published release, for a link to its
                notes. Null when the repository has none, when its only releases
                are drafts or pre-releases, and for every Forgejo repository,
                whose latest release is a separate read per repository that the
                refresh does not make.
            stale_since (datetime.datetime | None): Set when this row is the last known one because its forge couldn't
                be read or its rate limit is spent: the time it was last fetched.
                Null otherwise. A client offers no write on a stale row.
            runs (list[MainBranchRun] | Unset): What each workflow run attempt on the newest commit did, the
                facts `status`, `failingJobs` and `checks` were worked out from,
                in the order the forge listed them. A client can fold them into
                its own pill. They are the jobs `GET /api/v1/main-branches/checks`
                lists, grouped as the stream's `run` events group them. Present
                for a repository with at least one check. They hold the newest
                run of each workflow on the newest commit: an older run that a
                newer run of the same workflow replaces is left out, as it is
                from `status` and `checks`. On GitHub the checks are grouped by
                the workflow run each belongs to, and only the first 100 of the
                commit's rollup are read besides the newest runs, so a run says
                `jobsTruncated` when the commit has more checks than that.
                Absent for a repository with no check.
            advisories (Advisories | Unset): The open dependency advisories on a repository's default branch, read
                from GitHub's Dependabot alerts, or for a Forgejo repository from the
                packages in its lockfiles matched against OSV, when the operator has
                switched that on. Absent from the row when no source reads them for its
                forge. A source that can't
                answer, such as alerts switched off or a token without the
                `security_events` scope, gives `state` "unknown", never a count of
                zero.
     """

    forge: Forge
    full_name: str
    url: str
    branch: str
    status: MainBranchStatus
    commit: MainBranchCommit | None
    failing_jobs: list[str]
    finished_at: datetime.datetime | None
    duration_seconds: int | None
    run_url: str
    checks: CheckCounts
    latest_release: MainBranchRelease | None
    stale_since: datetime.datetime | None
    runs: list[MainBranchRun] | Unset = UNSET
    advisories: Advisories | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.advisories import Advisories # noqa: PLC0415
        from ..models.check_counts import CheckCounts # noqa: PLC0415
        from ..models.main_branch_commit import MainBranchCommit # noqa: PLC0415
        from ..models.main_branch_release import MainBranchRelease # noqa: PLC0415
        from ..models.main_branch_run import MainBranchRun # noqa: PLC0415
        forge = self.forge.value

        full_name = self.full_name

        url = self.url

        branch = self.branch

        status = self.status.value

        commit: dict[str, Any] | None
        if isinstance(self.commit, MainBranchCommit):
            commit = self.commit.to_dict()
        else:
            commit = self.commit

        failing_jobs = self.failing_jobs



        finished_at: None | str
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        duration_seconds: int | None
        duration_seconds = self.duration_seconds

        run_url = self.run_url

        checks = self.checks.to_dict()

        latest_release: dict[str, Any] | None
        if isinstance(self.latest_release, MainBranchRelease):
            latest_release = self.latest_release.to_dict()
        else:
            latest_release = self.latest_release

        stale_since: None | str
        if isinstance(self.stale_since, datetime.datetime):
            stale_since = self.stale_since.isoformat()
        else:
            stale_since = self.stale_since

        runs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.runs, Unset):
            runs = []
            for runs_item_data in self.runs:
                runs_item = runs_item_data.to_dict()
                runs.append(runs_item)



        advisories: dict[str, Any] | Unset = UNSET
        if not isinstance(self.advisories, Unset):
            advisories = self.advisories.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "url": url,
            "branch": branch,
            "status": status,
            "commit": commit,
            "failingJobs": failing_jobs,
            "finishedAt": finished_at,
            "durationSeconds": duration_seconds,
            "runUrl": run_url,
            "checks": checks,
            "latestRelease": latest_release,
            "staleSince": stale_since,
        })
        if runs is not UNSET:
            field_dict["runs"] = runs
        if advisories is not UNSET:
            field_dict["advisories"] = advisories

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advisories import Advisories # noqa: PLC0415
        from ..models.check_counts import CheckCounts # noqa: PLC0415
        from ..models.main_branch_commit import MainBranchCommit # noqa: PLC0415
        from ..models.main_branch_release import MainBranchRelease # noqa: PLC0415
        from ..models.main_branch_run import MainBranchRun # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        url = d.pop("url")

        branch = d.pop("branch")

        status = MainBranchStatus(d.pop("status"))




        def _parse_commit(data: object) -> MainBranchCommit | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                commit_type_0 = MainBranchCommit.from_dict(data)



                return commit_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MainBranchCommit | None, data)

        commit = _parse_commit(d.pop("commit"))


        failing_jobs = cast(list[str], d.pop("failingJobs"))


        def _parse_finished_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = datetime.datetime.fromisoformat(data)



                return finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        finished_at = _parse_finished_at(d.pop("finishedAt"))


        def _parse_duration_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_seconds = _parse_duration_seconds(d.pop("durationSeconds"))


        run_url = d.pop("runUrl")

        checks = CheckCounts.from_dict(d.pop("checks"))




        def _parse_latest_release(data: object) -> MainBranchRelease | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_release_type_0 = MainBranchRelease.from_dict(data)



                return latest_release_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MainBranchRelease | None, data)

        latest_release = _parse_latest_release(d.pop("latestRelease"))


        def _parse_stale_since(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stale_since_type_0 = datetime.datetime.fromisoformat(data)



                return stale_since_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        stale_since = _parse_stale_since(d.pop("staleSince"))


        _runs = d.pop("runs", UNSET)
        runs: list[MainBranchRun] | Unset = UNSET
        if _runs is not UNSET:
            runs = []
            for runs_item_data in _runs:
                runs_item = MainBranchRun.from_dict(runs_item_data)



                runs.append(runs_item)


        _advisories = d.pop("advisories", UNSET)
        advisories: Advisories | Unset
        if isinstance(_advisories,  Unset):
            advisories = UNSET
        else:
            advisories = Advisories.from_dict(_advisories)




        main_branch = cls(
            forge=forge,
            full_name=full_name,
            url=url,
            branch=branch,
            status=status,
            commit=commit,
            failing_jobs=failing_jobs,
            finished_at=finished_at,
            duration_seconds=duration_seconds,
            run_url=run_url,
            checks=checks,
            latest_release=latest_release,
            stale_since=stale_since,
            runs=runs,
            advisories=advisories,
        )


        main_branch.additional_properties = d
        return main_branch

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
