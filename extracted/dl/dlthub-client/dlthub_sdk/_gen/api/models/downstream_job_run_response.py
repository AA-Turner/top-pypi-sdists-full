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

T = TypeVar("T", bound="DownstreamJobRunResponse")


@_attrs_define
class DownstreamJobRunResponse:
    """
    Attributes:
        id (UUID): The run ID
        job_id (UUID): The ID of the job that ran
        job_ref (str): The job's canonical reference
        name (str): The job's display name
        number (int): The run number within the job
        status (RunStatus | str): The status of the run
        trigger (str): The trigger that started the downstream run
        category (JobCategory | None | Unset): The category the job declares in `expose.category`, null when it declares
            none. Callers that want one kind of downstream run, such as agents, filter on this.
        duration_seconds (float | None | Unset): The run duration in seconds, null if not finished (may be fractional)
        started_at (datetime.datetime | None | Unset): When the run started, null if not yet started
    """

    id: UUID
    job_id: UUID
    job_ref: str
    name: str
    number: int
    status: RunStatus | str
    trigger: str
    category: JobCategory | None | Unset = UNSET
    duration_seconds: float | None | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        job_id = str(self.job_id)

        job_ref = self.job_ref

        name = self.name

        number = self.number

        status: str
        if isinstance(self.status, RunStatus):
            status = self.status.value
        else:
            status = self.status

        trigger = self.trigger

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, JobCategory):
            category = self.category.value
        else:
            category = self.category

        duration_seconds: float | None | Unset
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "job_id": job_id,
                "job_ref": job_ref,
                "name": name,
                "number": number,
                "status": status,
                "trigger": trigger,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        job_id = UUID(d.pop("job_id"))

        job_ref = d.pop("job_ref")

        name = d.pop("name")

        number = d.pop("number")

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

        def _parse_duration_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds", UNSET))

        def _parse_started_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))

        downstream_job_run_response = cls(
            id=id,
            job_id=job_id,
            job_ref=job_ref,
            name=name,
            number=number,
            status=status,
            trigger=trigger,
            category=category,
            duration_seconds=duration_seconds,
            started_at=started_at,
        )

        downstream_job_run_response.additional_properties = d
        return downstream_job_run_response

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
