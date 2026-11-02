from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.check_status import CheckStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="Check")



@_attrs_define
class Check:
    """ One job/check run against a pull request's head commit.

        Attributes:
            name (str):
            status (CheckStatus): How far one job has got, as a fact. The page works out what to show
                from it and `conclusion`.

                "waiting" is a GitHub workflow run held until a maintainer approves
                it. It has no jobs yet, so it is not queued and has not failed; its
                `url` is the run's page, where the approve button is. A check run
                that finishes as `action_required` is the other shape of the same
                wait: it is "completed" with that conclusion. The page treats the
                two alike.
            url (str): That job's own page on the forge that ran it — never the pull request's own page.
            conclusion (str | Unset): How a finished job ended, in the forge's own word. Sent only when
                `status` is "completed". It is not folded onto a fixed set: GitHub
                sends its check run conclusion as it is (`success`, `failure`,
                `neutral`, `cancelled`, `skipped`, `timed_out`, `action_required`,
                `stale`, `startup_failure`) and Forgejo sends the terminal status of
                the job (`success`, `failure`, `cancelled`, `skipped`). A legacy
                commit status, which has no conclusion, is sent as `success` or
                `failure`. A client decides what each word means and what to do
                with one it doesn't know.

                `action_required` means the job needs someone's approval, and `url`
                is where to give it. The page shows it as waiting for approval,
                the same as a held run whose `status` is "waiting".
            job_id (int | Unset): The Actions job (or check run) id to pass to GET /api/v1/checks/log.
                Absent for a legacy commit status and for a workflow held for
                approval, which have no output to read.
            run_id (int | Unset): The Actions workflow run this job belongs to, to pass to
                `POST /api/v1/checks/cancel-run`. Present on every Actions job,
                finished or not; only a job that is queued or running has
                anything left to cancel, which a client reads from `status`. A
                third-party check and a legacy commit status have none.

                A Forgejo run whose jobs couldn't be read is listed as one check
                named for the run, with a `runId` and no `jobId`. A client treats
                a check with a `runId` and no `jobId` as the run itself, not as a
                job of it, and doesn't list its name among the run's jobs.
            run_name (str | Unset): The name of that workflow run, for a client to say which run a
                cancel stops. Present with `runId`; on GitHub it can be absent
                when the lookup of the commit's runs failed or didn't list the run.
            run_number (int | Unset): The forge's own number for that run, the one in the run's page
                address. It tells two runs of one workflow apart. Present with
                `runId` when the forge says it; on GitHub it can be absent when
                the lookup of the commit's runs failed or didn't list the run.
            required (bool | Unset): Whether the base branch's protection makes this check block the
                merge (GitHub required status checks and rulesets, Forgejo
                `status_check_contexts`). Absent when the forge can't tell — a
                token that can't read protection, or a check that can't be
                mapped to a protection entry. Absent is not the same as false.
            started_at (datetime.datetime | Unset): When the forge says the job started. Absent until it has, and when
                the forge doesn't say. A client works out how long a job ran from
                this and `completedAt`.
            completed_at (datetime.datetime | Unset): When the forge says the job finished. Absent while it runs, and
                when the forge doesn't say.
            run_attempt (int | Unset): Which attempt of its workflow run the job belongs to. Both
                forges keep a run's id when it is retried, and Forgejo keeps the
                job's id and page too, so this is what tells a retry's output
                from the first attempt's. On GitHub it is absent for a check that
                isn't an Actions job, and when neither the job's page address nor
                the lookup of the commit's runs gives one.
            failed_step (str | Unset): The name of the step of a failed job that broke. Absent when
                the check isn't a job the token can read (a third-party check,
                a forge with no step data, a token without access).
            excerpt (str | Unset): The tail of the failed job's log as plain text: the last lines,
                with per-line timestamps and colour codes removed, at most 2,000
                characters. Never markup, and a client must render it as text.
                Whatever the forge already masks stays masked. Absent when the
                log can't be read or has expired. GitHub fills it for at most
                the first five failed jobs of a list, in the list's order.
                Forgejo never fills it in a list, since that would read a log
                while the list is built: ask for it through
                GET /api/v1/checks/log with `excerpt=true`. The whole output is read
                through GET /api/v1/checks/log.
     """

    name: str
    status: CheckStatus
    url: str
    conclusion: str | Unset = UNSET
    job_id: int | Unset = UNSET
    run_id: int | Unset = UNSET
    run_name: str | Unset = UNSET
    run_number: int | Unset = UNSET
    required: bool | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    run_attempt: int | Unset = UNSET
    failed_step: str | Unset = UNSET
    excerpt: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status.value

        url = self.url

        conclusion = self.conclusion

        job_id = self.job_id

        run_id = self.run_id

        run_name = self.run_name

        run_number = self.run_number

        required = self.required

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        run_attempt = self.run_attempt

        failed_step = self.failed_step

        excerpt = self.excerpt


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "status": status,
            "url": url,
        })
        if conclusion is not UNSET:
            field_dict["conclusion"] = conclusion
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if run_id is not UNSET:
            field_dict["runId"] = run_id
        if run_name is not UNSET:
            field_dict["runName"] = run_name
        if run_number is not UNSET:
            field_dict["runNumber"] = run_number
        if required is not UNSET:
            field_dict["required"] = required
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if run_attempt is not UNSET:
            field_dict["runAttempt"] = run_attempt
        if failed_step is not UNSET:
            field_dict["failedStep"] = failed_step
        if excerpt is not UNSET:
            field_dict["excerpt"] = excerpt

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        status = CheckStatus(d.pop("status"))




        url = d.pop("url")

        conclusion = d.pop("conclusion", UNSET)

        job_id = d.pop("jobId", UNSET)

        run_id = d.pop("runId", UNSET)

        run_name = d.pop("runName", UNSET)

        run_number = d.pop("runNumber", UNSET)

        required = d.pop("required", UNSET)

        _started_at = d.pop("startedAt", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)




        _completed_at = d.pop("completedAt", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(_completed_at)




        run_attempt = d.pop("runAttempt", UNSET)

        failed_step = d.pop("failedStep", UNSET)

        excerpt = d.pop("excerpt", UNSET)

        check = cls(
            name=name,
            status=status,
            url=url,
            conclusion=conclusion,
            job_id=job_id,
            run_id=run_id,
            run_name=run_name,
            run_number=run_number,
            required=required,
            started_at=started_at,
            completed_at=completed_at,
            run_attempt=run_attempt,
            failed_step=failed_step,
            excerpt=excerpt,
        )


        check.additional_properties = d
        return check

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
