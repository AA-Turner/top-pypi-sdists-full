from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.check_status import CheckStatus
from ..models.check_subject_kind import CheckSubjectKind
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.check import Check





T = TypeVar("T", bound="RunEvent")



@_attrs_define
class RunEvent:
    """ The `data` of a `run` event on the dashboard stream: the jobs of
    one workflow run attempt of one subject, or one check that belongs
    to no run. A later event with the same `key` replaces the earlier
    one. An event with no `key` and no `checks` says the subject has
    none. An event with `error` set stands in for the whole listing.

        Attributes:
            kind (CheckSubjectKind):
            forge (str):
            full_name (str): The repository, as `owner/repo`.
            number (int | Unset): The pull request number. Required for `pull_request`.
            key (str | Unset): Names the unit this event replaces: `run/<runId>/<attempt>`
                for a run attempt, `job/<url>|<name>` for a check with no
                run. Absent when the subject has no checks or on an error.
            run_id (int | Unset): Absent for a check with no run.
            run_attempt (int | Unset): Absent when the check has no run or the forge doesn't
                number attempts.
            status (CheckStatus | Unset): How far one job has got, as a fact. The page works out what to show
                from it and `conclusion`.

                "waiting" is a GitHub workflow run held until a maintainer approves
                it. It has no jobs yet, so it is not queued and has not failed; its
                `url` is the run's page, where the approve button is. A check run
                that finishes as `action_required` is the other shape of the same
                wait: it is "completed" with that conclusion. The page treats the
                two alike.
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
            started_at (datetime.datetime | Unset): When the forge says the run attempt started. Absent until it
                has, and when the forge doesn't say.
            completed_at (datetime.datetime | Unset): When the forge says the run attempt finished. Absent until it
                has. GitHub gives no finish time for a run, so it is always
                absent there; the page can take the latest job's
                `completedAt`.
            checks (list[Check] | Unset): Absent when `gone` or `error` is set.
            gone (bool | Unset): The unit named by `key` is no longer listed; drop it.
            final (bool | Unset): Set on the last event of a listing, so a client can draw
                once the whole listing has arrived.
            error (str | Unset):
     """

    kind: CheckSubjectKind
    forge: str
    full_name: str
    number: int | Unset = UNSET
    key: str | Unset = UNSET
    run_id: int | Unset = UNSET
    run_attempt: int | Unset = UNSET
    status: CheckStatus | Unset = UNSET
    conclusion: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    checks: list[Check] | Unset = UNSET
    gone: bool | Unset = UNSET
    final: bool | Unset = UNSET
    error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.check import Check # noqa: PLC0415
        kind = self.kind.value

        forge = self.forge

        full_name = self.full_name

        number = self.number

        key = self.key

        run_id = self.run_id

        run_attempt = self.run_attempt

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        conclusion = self.conclusion

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        checks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.checks, Unset):
            checks = []
            for checks_item_data in self.checks:
                checks_item = checks_item_data.to_dict()
                checks.append(checks_item)



        gone = self.gone

        final = self.final

        error = self.error


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "forge": forge,
            "fullName": full_name,
        })
        if number is not UNSET:
            field_dict["number"] = number
        if key is not UNSET:
            field_dict["key"] = key
        if run_id is not UNSET:
            field_dict["runId"] = run_id
        if run_attempt is not UNSET:
            field_dict["runAttempt"] = run_attempt
        if status is not UNSET:
            field_dict["status"] = status
        if conclusion is not UNSET:
            field_dict["conclusion"] = conclusion
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if checks is not UNSET:
            field_dict["checks"] = checks
        if gone is not UNSET:
            field_dict["gone"] = gone
        if final is not UNSET:
            field_dict["final"] = final
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check import Check # noqa: PLC0415
        d = dict(src_dict)
        kind = CheckSubjectKind(d.pop("kind"))




        forge = d.pop("forge")

        full_name = d.pop("fullName")

        number = d.pop("number", UNSET)

        key = d.pop("key", UNSET)

        run_id = d.pop("runId", UNSET)

        run_attempt = d.pop("runAttempt", UNSET)

        _status = d.pop("status", UNSET)
        status: CheckStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = CheckStatus(_status)




        conclusion = d.pop("conclusion", UNSET)

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




        _checks = d.pop("checks", UNSET)
        checks: list[Check] | Unset = UNSET
        if _checks is not UNSET:
            checks = []
            for checks_item_data in _checks:
                checks_item = Check.from_dict(checks_item_data)



                checks.append(checks_item)


        gone = d.pop("gone", UNSET)

        final = d.pop("final", UNSET)

        error = d.pop("error", UNSET)

        run_event = cls(
            kind=kind,
            forge=forge,
            full_name=full_name,
            number=number,
            key=key,
            run_id=run_id,
            run_attempt=run_attempt,
            status=status,
            conclusion=conclusion,
            started_at=started_at,
            completed_at=completed_at,
            checks=checks,
            gone=gone,
            final=final,
            error=error,
        )


        run_event.additional_properties = d
        return run_event

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
