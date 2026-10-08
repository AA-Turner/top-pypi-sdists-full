from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.run_status import RunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecentJobRunResponse")


@_attrs_define
class RecentJobRunResponse:
    """
    Attributes:
        id (UUID): The run ID
        status (RunStatus | str): The status of the run
        duration_seconds (float | None | Unset): The run duration in seconds, null if not finished (may be fractional)
        rows_loaded (int | None | Unset): Total rows loaded across the run's pipeline runs; null when not reported.
        started_at (datetime.datetime | None | Unset): When the run started, null if not yet started
    """

    id: UUID
    status: RunStatus | str
    duration_seconds: float | None | Unset = UNSET
    rows_loaded: int | None | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        status: str
        if isinstance(self.status, RunStatus):
            status = self.status.value
        else:
            status = self.status

        duration_seconds: float | None | Unset
        if isinstance(self.duration_seconds, Unset):
            duration_seconds = UNSET
        else:
            duration_seconds = self.duration_seconds

        rows_loaded: int | None | Unset
        if isinstance(self.rows_loaded, Unset):
            rows_loaded = UNSET
        else:
            rows_loaded = self.rows_loaded

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
                "status": status,
            }
        )
        if duration_seconds is not UNSET:
            field_dict["duration_seconds"] = duration_seconds
        if rows_loaded is not UNSET:
            field_dict["rows_loaded"] = rows_loaded
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

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

        def _parse_duration_seconds(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds", UNSET))

        def _parse_rows_loaded(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rows_loaded = _parse_rows_loaded(d.pop("rows_loaded", UNSET))

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

        recent_job_run_response = cls(
            id=id,
            status=status,
            duration_seconds=duration_seconds,
            rows_loaded=rows_loaded,
            started_at=started_at,
        )

        recent_job_run_response.additional_properties = d
        return recent_job_run_response

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
