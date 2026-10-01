from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_category import JobCategory
from ..models.run_status import RunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DownstreamRunResponse")


@_attrs_define
class DownstreamRunResponse:
    """
    Attributes:
        id (UUID): The run ID
        job_ref (str): The job's canonical reference
        name (str): The job's display name
        number (int): The run number within the job
        script_id (UUID): The ID of the job that ran
        status (RunStatus): The status of the run
        trigger (str): The trigger that started the downstream run
        category (JobCategory | None | Unset): The category the job declares in `expose.category`, null when it declares
            none. Callers that want one kind of downstream run, such as agents, filter on this.
        duration (float | None | Unset): The run duration in seconds, null if not finished (may be fractional)
        time_started (datetime.datetime | None | Unset): When the run started, null if not yet started
    """

    id: UUID
    job_ref: str
    name: str
    number: int
    script_id: UUID
    status: RunStatus
    trigger: str
    category: JobCategory | None | Unset = UNSET
    duration: float | None | Unset = UNSET
    time_started: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        job_ref = self.job_ref

        name = self.name

        number = self.number

        script_id = str(self.script_id)

        status = self.status.value

        trigger = self.trigger

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, JobCategory):
            category = self.category.value
        else:
            category = self.category

        duration: float | None | Unset
        if isinstance(self.duration, Unset):
            duration = UNSET
        else:
            duration = self.duration

        time_started: None | str | Unset
        if isinstance(self.time_started, Unset):
            time_started = UNSET
        elif isinstance(self.time_started, datetime.datetime):
            time_started = self.time_started.isoformat()
        else:
            time_started = self.time_started

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "job_ref": job_ref,
                "name": name,
                "number": number,
                "script_id": script_id,
                "status": status,
                "trigger": trigger,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category
        if duration is not UNSET:
            field_dict["duration"] = duration
        if time_started is not UNSET:
            field_dict["time_started"] = time_started

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        job_ref = d.pop("job_ref")

        name = d.pop("name")

        number = d.pop("number")

        script_id = UUID(d.pop("script_id"))

        status = RunStatus(d.pop("status"))

        trigger = d.pop("trigger")

        def _parse_category(data: object) -> JobCategory | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_0 = JobCategory(data)

                return category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobCategory | None | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_duration(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration = _parse_duration(d.pop("duration", UNSET))

        def _parse_time_started(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_started_type_0 = isoparse(data)

                return time_started_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        time_started = _parse_time_started(d.pop("time_started", UNSET))

        downstream_run_response = cls(
            id=id,
            job_ref=job_ref,
            name=name,
            number=number,
            script_id=script_id,
            status=status,
            trigger=trigger,
            category=category,
            duration=duration,
            time_started=time_started,
        )

        downstream_run_response.additional_properties = d
        return downstream_run_response

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
