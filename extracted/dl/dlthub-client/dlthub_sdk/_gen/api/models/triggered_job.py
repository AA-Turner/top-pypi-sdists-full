from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.triggered_job_status_type_0 import TriggeredJobStatusType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_run_response import JobRunResponse


T = TypeVar("T", bound="TriggeredJob")


@_attrs_define
class TriggeredJob:
    """
    Attributes:
        job_id (UUID): The ID of the matched job.
        job_ref (str): The job reference of the matched job.
        matched_triggers (list[str]): Every trigger that selected this job: its default trigger when named in `job_ids`,
            plus any selector matches.
        trigger (str): The trigger the job fires with.
        job_run (JobRunResponse | None | Unset): The created run; `null` in dry-run mode or when skipped.
        job_run_id (None | Unset | UUID): The ID of the created run; `null` in dry-run mode or when skipped.
        reasons (list[str] | None | Unset): Human-readable reasons for a skip, e.g. which upstream jobs are not fresh;
            `null` when the job was triggered or no reasons were recorded.
        status (str | TriggeredJobStatusType0 | Unset): Whether the job started a run: `triggered` if it did; otherwise
            why not. `skipped_fresh`: an upstream job is not fresh (see `reasons`). `skipped_upstream_pending`: an upstream
            job is triggered in the same request. `skipped_out_of_interval`: the run would fall outside the job's
            `interval_start` / `interval_end`. `skipped_concurrency_limit`: the job is already running as many runs as it
            allows. `skipped_org_concurrency_limit`: the organization has reached its limit of concurrent runs.
            `skipped_trial_expired`: the organization's trial has ended. `skipped_minutes_limit`: the organization has used
            up its compute minutes. `skipped_workspace_archived`: the workspace is archived. Default:
            TriggeredJobStatusType0.TRIGGERED.
    """

    job_id: UUID
    job_ref: str
    matched_triggers: list[str]
    trigger: str
    job_run: JobRunResponse | None | Unset = UNSET
    job_run_id: None | Unset | UUID = UNSET
    reasons: list[str] | None | Unset = UNSET
    status: str | TriggeredJobStatusType0 | Unset = TriggeredJobStatusType0.TRIGGERED
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_run_response import JobRunResponse

        job_id = str(self.job_id)

        job_ref = self.job_ref

        matched_triggers = self.matched_triggers

        trigger = self.trigger

        job_run: dict[str, Any] | None | Unset
        if isinstance(self.job_run, Unset):
            job_run = UNSET
        elif isinstance(self.job_run, JobRunResponse):
            job_run = self.job_run.to_dict()
        else:
            job_run = self.job_run

        job_run_id: None | str | Unset
        if isinstance(self.job_run_id, Unset):
            job_run_id = UNSET
        elif isinstance(self.job_run_id, UUID):
            job_run_id = str(self.job_run_id)
        else:
            job_run_id = self.job_run_id

        reasons: list[str] | None | Unset
        if isinstance(self.reasons, Unset):
            reasons = UNSET
        elif isinstance(self.reasons, list):
            reasons = self.reasons

        else:
            reasons = self.reasons

        status: str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, TriggeredJobStatusType0):
            status = self.status.value
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "job_ref": job_ref,
                "matched_triggers": matched_triggers,
                "trigger": trigger,
            }
        )
        if job_run is not UNSET:
            field_dict["job_run"] = job_run
        if job_run_id is not UNSET:
            field_dict["job_run_id"] = job_run_id
        if reasons is not UNSET:
            field_dict["reasons"] = reasons
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_run_response import JobRunResponse

        d = dict(src_dict)
        job_id = UUID(d.pop("job_id"))

        job_ref = d.pop("job_ref")

        matched_triggers = cast(list[str], d.pop("matched_triggers"))

        trigger = d.pop("trigger")

        def _parse_job_run(data: object) -> JobRunResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                job_run_type_0 = JobRunResponse.from_dict(data)

                return job_run_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobRunResponse | None | Unset, data)

        job_run = _parse_job_run(d.pop("job_run", UNSET))

        def _parse_job_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_run_id_type_0 = UUID(data)

                return job_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        job_run_id = _parse_job_run_id(d.pop("job_run_id", UNSET))

        def _parse_reasons(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                reasons_type_0 = cast(list[str], data)

                return reasons_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        reasons = _parse_reasons(d.pop("reasons", UNSET))

        def _parse_status(data: object) -> str | TriggeredJobStatusType0 | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = TriggeredJobStatusType0(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | TriggeredJobStatusType0 | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        triggered_job = cls(
            job_id=job_id,
            job_ref=job_ref,
            matched_triggers=matched_triggers,
            trigger=trigger,
            job_run=job_run,
            job_run_id=job_run_id,
            reasons=reasons,
            status=status,
        )

        triggered_job.additional_properties = d
        return triggered_job

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
