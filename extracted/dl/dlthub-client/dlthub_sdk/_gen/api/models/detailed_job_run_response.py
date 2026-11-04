from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.attention_reason import AttentionReason
from ..models.run_status import RunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.downstream_job_run_response import DownstreamJobRunResponse
    from ..models.job_response import JobResponse
    from ..models.job_version_response import JobVersionResponse
    from ..models.pipeline_run_summary_response import PipelineRunSummaryResponse


T = TypeVar("T", bound="DetailedJobRunResponse")


@_attrs_define
class DetailedJobRunResponse:
    """
    Attributes:
        attention_reasons (list[AttentionReason | str]): Why the run needs an operator's look, every reason that applies
            in a fixed order: it failed, it completed but loaded no rows, it completed after more than 5 hours. A run still
            in progress is never flagged. Empty when nothing applies.
        configuration_id (UUID): The ID of the configuration the run uses.
        created_at (datetime.datetime): When it was created.
        deployment_id (UUID): The ID of the deployment the run uses.
        duration_seconds (float | None): Duration of the run in seconds, possibly fractional; `null` until it has
            finished.
        finished_at (datetime.datetime | None): When the run finished; `null` until it has.
        id (UUID): Unique ID (a UUID).
        job (JobResponse):
        job_version (JobVersionResponse):
        job_version_id (UUID): The ID of the job version the run uses.
        logs_url (None | str): A link to the logs of the run
        number (int): Number of the run within its job, counting up from 1; numbers repeat across jobs.
        profile (str): The name of the profile that was used for the run
        started_at (datetime.datetime | None): When the run started; `null` until it has.
        status (RunStatus | str): The status of the run
        trigger (str): The trigger the run fired with, e.g. `schedule:0 8 * * *`, `manual:jobs.my_job`,
            `job.success:jobs.upstream`.
        triggered_by (None | UUID): The `organization_membership_id` of the member who started the run; set for any run
            started through the API, `null` for runs the scheduler, another job or a public URL started.
        updated_at (datetime.datetime): When it was last changed.
        workspace_id (UUID): The ID of the workspace the run belongs to
        downstream_job_runs (list[DownstreamJobRunResponse] | None | Unset): Runs this run triggered, newest first.
            Included only when `downstream_job_runs_limit` is requested; null otherwise. Only runs started by this run's
            outcome are linked, so a manually started one is absent.
        interval_end (datetime.datetime | None | Unset): End of the interval the run processes; `null` for a job without
            intervals.
        interval_start (datetime.datetime | None | Unset): Start of the interval the run processes; `null` for a job
            without intervals.
        pipeline_run_summaries (list[PipelineRunSummaryResponse] | Unset): One entry per dlt pipeline name the run
            reported; a pipeline that ran more than once shows its latest report. In no particular order, and empty until
            telemetry has received the reports.
        previous_job_run_id (None | Unset | UUID): The upstream run whose completion started this one, through a
            `job.success:` / `job.fail:` trigger or a freshness dependency; `null` for a run started manually, by its own
            schedule, or by a trigger request.
    """

    attention_reasons: list[AttentionReason | str]
    configuration_id: UUID
    created_at: datetime.datetime
    deployment_id: UUID
    duration_seconds: float | None
    finished_at: datetime.datetime | None
    id: UUID
    job: JobResponse
    job_version: JobVersionResponse
    job_version_id: UUID
    logs_url: None | str
    number: int
    profile: str
    started_at: datetime.datetime | None
    status: RunStatus | str
    trigger: str
    triggered_by: None | UUID
    updated_at: datetime.datetime
    workspace_id: UUID
    downstream_job_runs: list[DownstreamJobRunResponse] | None | Unset = UNSET
    interval_end: datetime.datetime | None | Unset = UNSET
    interval_start: datetime.datetime | None | Unset = UNSET
    pipeline_run_summaries: list[PipelineRunSummaryResponse] | Unset = UNSET
    previous_job_run_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attention_reasons = []
        for attention_reasons_item_data in self.attention_reasons:
            attention_reasons_item: str
            if isinstance(attention_reasons_item_data, AttentionReason):
                attention_reasons_item = attention_reasons_item_data.value
            else:
                attention_reasons_item = attention_reasons_item_data
            attention_reasons.append(attention_reasons_item)

        configuration_id = str(self.configuration_id)

        created_at = self.created_at.isoformat()

        deployment_id = str(self.deployment_id)

        duration_seconds: float | None
        duration_seconds = self.duration_seconds

        finished_at: None | str
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        id = str(self.id)

        job = self.job.to_dict()

        job_version = self.job_version.to_dict()

        job_version_id = str(self.job_version_id)

        logs_url: None | str
        logs_url = self.logs_url

        number = self.number

        profile = self.profile

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        status: str
        if isinstance(self.status, RunStatus):
            status = self.status.value
        else:
            status = self.status

        trigger = self.trigger

        triggered_by: None | str
        if isinstance(self.triggered_by, UUID):
            triggered_by = str(self.triggered_by)
        else:
            triggered_by = self.triggered_by

        updated_at = self.updated_at.isoformat()

        workspace_id = str(self.workspace_id)

        downstream_job_runs: list[dict[str, Any]] | None | Unset
        if isinstance(self.downstream_job_runs, Unset):
            downstream_job_runs = UNSET
        elif isinstance(self.downstream_job_runs, list):
            downstream_job_runs = []
            for downstream_job_runs_type_0_item_data in self.downstream_job_runs:
                downstream_job_runs_type_0_item = (
                    downstream_job_runs_type_0_item_data.to_dict()
                )
                downstream_job_runs.append(downstream_job_runs_type_0_item)

        else:
            downstream_job_runs = self.downstream_job_runs

        interval_end: None | str | Unset
        if isinstance(self.interval_end, Unset):
            interval_end = UNSET
        elif isinstance(self.interval_end, datetime.datetime):
            interval_end = self.interval_end.isoformat()
        else:
            interval_end = self.interval_end

        interval_start: None | str | Unset
        if isinstance(self.interval_start, Unset):
            interval_start = UNSET
        elif isinstance(self.interval_start, datetime.datetime):
            interval_start = self.interval_start.isoformat()
        else:
            interval_start = self.interval_start

        pipeline_run_summaries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.pipeline_run_summaries, Unset):
            pipeline_run_summaries = []
            for pipeline_run_summaries_item_data in self.pipeline_run_summaries:
                pipeline_run_summaries_item = pipeline_run_summaries_item_data.to_dict()
                pipeline_run_summaries.append(pipeline_run_summaries_item)

        previous_job_run_id: None | str | Unset
        if isinstance(self.previous_job_run_id, Unset):
            previous_job_run_id = UNSET
        elif isinstance(self.previous_job_run_id, UUID):
            previous_job_run_id = str(self.previous_job_run_id)
        else:
            previous_job_run_id = self.previous_job_run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attention_reasons": attention_reasons,
                "configuration_id": configuration_id,
                "created_at": created_at,
                "deployment_id": deployment_id,
                "duration_seconds": duration_seconds,
                "finished_at": finished_at,
                "id": id,
                "job": job,
                "job_version": job_version,
                "job_version_id": job_version_id,
                "logs_url": logs_url,
                "number": number,
                "profile": profile,
                "started_at": started_at,
                "status": status,
                "trigger": trigger,
                "triggered_by": triggered_by,
                "updated_at": updated_at,
                "workspace_id": workspace_id,
            }
        )
        if downstream_job_runs is not UNSET:
            field_dict["downstream_job_runs"] = downstream_job_runs
        if interval_end is not UNSET:
            field_dict["interval_end"] = interval_end
        if interval_start is not UNSET:
            field_dict["interval_start"] = interval_start
        if pipeline_run_summaries is not UNSET:
            field_dict["pipeline_run_summaries"] = pipeline_run_summaries
        if previous_job_run_id is not UNSET:
            field_dict["previous_job_run_id"] = previous_job_run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.downstream_job_run_response import DownstreamJobRunResponse
        from ..models.job_response import JobResponse
        from ..models.job_version_response import JobVersionResponse
        from ..models.pipeline_run_summary_response import PipelineRunSummaryResponse

        d = dict(src_dict)
        attention_reasons = []
        _attention_reasons = d.pop("attention_reasons")
        for attention_reasons_item_data in _attention_reasons:

            def _parse_attention_reasons_item(data: object) -> AttentionReason | str:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    attention_reasons_item_type_0 = AttentionReason(data)

                    return attention_reasons_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(AttentionReason | str, data)

            attention_reasons_item = _parse_attention_reasons_item(
                attention_reasons_item_data
            )

            attention_reasons.append(attention_reasons_item)

        configuration_id = UUID(d.pop("configuration_id"))

        created_at = isoparse(d.pop("created_at"))

        deployment_id = UUID(d.pop("deployment_id"))

        def _parse_duration_seconds(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds"))

        def _parse_finished_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        finished_at = _parse_finished_at(d.pop("finished_at"))

        id = UUID(d.pop("id"))

        job = JobResponse.from_dict(d.pop("job"))

        job_version = JobVersionResponse.from_dict(d.pop("job_version"))

        job_version_id = UUID(d.pop("job_version_id"))

        def _parse_logs_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        logs_url = _parse_logs_url(d.pop("logs_url"))

        number = d.pop("number")

        profile = d.pop("profile")

        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("started_at"))

        def _parse_status(data: object) -> RunStatus | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = RunStatus(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(RunStatus | str, data)

        status = _parse_status(d.pop("status"))

        trigger = d.pop("trigger")

        def _parse_triggered_by(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                triggered_by_type_0 = UUID(data)

                return triggered_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        triggered_by = _parse_triggered_by(d.pop("triggered_by"))

        updated_at = isoparse(d.pop("updated_at"))

        workspace_id = UUID(d.pop("workspace_id"))

        def _parse_downstream_job_runs(
            data: object,
        ) -> list[DownstreamJobRunResponse] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                downstream_job_runs_type_0 = []
                _downstream_job_runs_type_0 = data
                for downstream_job_runs_type_0_item_data in _downstream_job_runs_type_0:
                    downstream_job_runs_type_0_item = (
                        DownstreamJobRunResponse.from_dict(
                            downstream_job_runs_type_0_item_data
                        )
                    )

                    downstream_job_runs_type_0.append(downstream_job_runs_type_0_item)

                return downstream_job_runs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DownstreamJobRunResponse] | None | Unset, data)

        downstream_job_runs = _parse_downstream_job_runs(
            d.pop("downstream_job_runs", UNSET)
        )

        def _parse_interval_end(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interval_end_type_0 = isoparse(data)

                return interval_end_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        interval_end = _parse_interval_end(d.pop("interval_end", UNSET))

        def _parse_interval_start(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interval_start_type_0 = isoparse(data)

                return interval_start_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        interval_start = _parse_interval_start(d.pop("interval_start", UNSET))

        _pipeline_run_summaries = d.pop("pipeline_run_summaries", UNSET)
        pipeline_run_summaries: list[PipelineRunSummaryResponse] | Unset = UNSET
        if _pipeline_run_summaries is not UNSET:
            pipeline_run_summaries = []
            for pipeline_run_summaries_item_data in _pipeline_run_summaries:
                pipeline_run_summaries_item = PipelineRunSummaryResponse.from_dict(
                    pipeline_run_summaries_item_data
                )

                pipeline_run_summaries.append(pipeline_run_summaries_item)

        def _parse_previous_job_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                previous_job_run_id_type_0 = UUID(data)

                return previous_job_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        previous_job_run_id = _parse_previous_job_run_id(
            d.pop("previous_job_run_id", UNSET)
        )

        detailed_job_run_response = cls(
            attention_reasons=attention_reasons,
            configuration_id=configuration_id,
            created_at=created_at,
            deployment_id=deployment_id,
            duration_seconds=duration_seconds,
            finished_at=finished_at,
            id=id,
            job=job,
            job_version=job_version,
            job_version_id=job_version_id,
            logs_url=logs_url,
            number=number,
            profile=profile,
            started_at=started_at,
            status=status,
            trigger=trigger,
            triggered_by=triggered_by,
            updated_at=updated_at,
            workspace_id=workspace_id,
            downstream_job_runs=downstream_job_runs,
            interval_end=interval_end,
            interval_start=interval_start,
            pipeline_run_summaries=pipeline_run_summaries,
            previous_job_run_id=previous_job_run_id,
        )

        detailed_job_run_response.additional_properties = d
        return detailed_job_run_response

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
