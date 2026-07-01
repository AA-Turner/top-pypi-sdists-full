from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.run_status import RunStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_run_summary_response import PipelineRunSummaryResponse


T = TypeVar("T", bound="RunResponse")


@_attrs_define
class RunResponse:
    """
    Attributes:
        configuration_id (UUID): The ID of the configuration that will be used when running the script
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        deployment_id (UUID): The ID of the deployment that will be used when running the script
        duration (float | None): The duration of the run in seconds, may be fractional (null if not yet completed)
        id (UUID): The unique ID of the entity
        logs (None | str): A link to the logs of the run
        number (int): The number of the run. Will increment for each new run of the script
        script_version_id (UUID): The ID of the script version that will be used when running the script
        status (RunStatus): The status of the run
        time_ended (datetime.datetime | None): The time the run ended
        time_started (datetime.datetime | None): The time the run started
        trigger (str): The trigger that started this run (full TTrigger string, e.g. schedule:0 8 * * *, manual:,
            job.success:jobs.ref)
        triggered_by (None | UUID): The ID of the identity who triggered the run if triggered manually
        workspace_id (UUID): The ID of the workspace the run belongs to
        interval_end (datetime.datetime | None | Unset): End of the interval being processed (for interval-based jobs)
        interval_start (datetime.datetime | None | Unset): Start of the interval being processed (for interval-based
            jobs)
        pipeline_run_summaries (list[PipelineRunSummaryResponse] | Unset): Pipeline run summaries linked to this job
            run, populated by telemetry
        prev_run_id (None | Unset | UUID): The ID of the upstream run that triggered this run (for job event triggers)
        profile (None | str | Unset): The name of the profile that was used for the run
    """

    configuration_id: UUID
    date_added: datetime.datetime
    date_updated: datetime.datetime
    deployment_id: UUID
    duration: float | None
    id: UUID
    logs: None | str
    number: int
    script_version_id: UUID
    status: RunStatus
    time_ended: datetime.datetime | None
    time_started: datetime.datetime | None
    trigger: str
    triggered_by: None | UUID
    workspace_id: UUID
    interval_end: datetime.datetime | None | Unset = UNSET
    interval_start: datetime.datetime | None | Unset = UNSET
    pipeline_run_summaries: list[PipelineRunSummaryResponse] | Unset = UNSET
    prev_run_id: None | Unset | UUID = UNSET
    profile: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configuration_id = str(self.configuration_id)

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        deployment_id = str(self.deployment_id)

        duration: float | None
        duration = self.duration

        id = str(self.id)

        logs: None | str
        logs = self.logs

        number = self.number

        script_version_id = str(self.script_version_id)

        status = self.status.value

        time_ended: None | str
        if isinstance(self.time_ended, datetime.datetime):
            time_ended = self.time_ended.isoformat()
        else:
            time_ended = self.time_ended

        time_started: None | str
        if isinstance(self.time_started, datetime.datetime):
            time_started = self.time_started.isoformat()
        else:
            time_started = self.time_started

        trigger = self.trigger

        triggered_by: None | str
        if isinstance(self.triggered_by, UUID):
            triggered_by = str(self.triggered_by)
        else:
            triggered_by = self.triggered_by

        workspace_id = str(self.workspace_id)

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

        prev_run_id: None | str | Unset
        if isinstance(self.prev_run_id, Unset):
            prev_run_id = UNSET
        elif isinstance(self.prev_run_id, UUID):
            prev_run_id = str(self.prev_run_id)
        else:
            prev_run_id = self.prev_run_id

        profile: None | str | Unset
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "configuration_id": configuration_id,
                "date_added": date_added,
                "date_updated": date_updated,
                "deployment_id": deployment_id,
                "duration": duration,
                "id": id,
                "logs": logs,
                "number": number,
                "script_version_id": script_version_id,
                "status": status,
                "time_ended": time_ended,
                "time_started": time_started,
                "trigger": trigger,
                "triggered_by": triggered_by,
                "workspace_id": workspace_id,
            }
        )
        if interval_end is not UNSET:
            field_dict["interval_end"] = interval_end
        if interval_start is not UNSET:
            field_dict["interval_start"] = interval_start
        if pipeline_run_summaries is not UNSET:
            field_dict["pipeline_run_summaries"] = pipeline_run_summaries
        if prev_run_id is not UNSET:
            field_dict["prev_run_id"] = prev_run_id
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_run_summary_response import PipelineRunSummaryResponse

        d = dict(src_dict)
        configuration_id = UUID(d.pop("configuration_id"))

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        deployment_id = UUID(d.pop("deployment_id"))

        def _parse_duration(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        duration = _parse_duration(d.pop("duration"))

        id = UUID(d.pop("id"))

        def _parse_logs(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        logs = _parse_logs(d.pop("logs"))

        number = d.pop("number")

        script_version_id = UUID(d.pop("script_version_id"))

        status = RunStatus(d.pop("status"))

        def _parse_time_ended(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_ended_type_0 = isoparse(data)

                return time_ended_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        time_ended = _parse_time_ended(d.pop("time_ended"))

        def _parse_time_started(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_started_type_0 = isoparse(data)

                return time_started_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        time_started = _parse_time_started(d.pop("time_started"))

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

        workspace_id = UUID(d.pop("workspace_id"))

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

        def _parse_prev_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                prev_run_id_type_0 = UUID(data)

                return prev_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        prev_run_id = _parse_prev_run_id(d.pop("prev_run_id", UNSET))

        def _parse_profile(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile = _parse_profile(d.pop("profile", UNSET))

        run_response = cls(
            configuration_id=configuration_id,
            date_added=date_added,
            date_updated=date_updated,
            deployment_id=deployment_id,
            duration=duration,
            id=id,
            logs=logs,
            number=number,
            script_version_id=script_version_id,
            status=status,
            time_ended=time_ended,
            time_started=time_started,
            trigger=trigger,
            triggered_by=triggered_by,
            workspace_id=workspace_id,
            interval_end=interval_end,
            interval_start=interval_start,
            pipeline_run_summaries=pipeline_run_summaries,
            prev_run_id=prev_run_id,
            profile=profile,
        )

        run_response.additional_properties = d
        return run_response

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
