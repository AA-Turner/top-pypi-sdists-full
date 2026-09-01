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

T = TypeVar("T", bound="RecentRunResponse")


@_attrs_define
class RecentRunResponse:
    """
    Attributes:
        id (UUID): The run ID
        status (RunStatus): The status of the run
        duration (float | None | Unset): The run duration in seconds, null if not finished (may be fractional)
        rows_loaded (int | None | Unset): Total rows loaded across the run's pipeline runs; null when not reported.
        time_started (datetime.datetime | None | Unset): When the run started, null if not yet started
    """

    id: UUID
    status: RunStatus
    duration: float | None | Unset = UNSET
    rows_loaded: int | None | Unset = UNSET
    time_started: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        status = self.status.value

        duration: float | None | Unset
        if isinstance(self.duration, Unset):
            duration = UNSET
        else:
            duration = self.duration

        rows_loaded: int | None | Unset
        if isinstance(self.rows_loaded, Unset):
            rows_loaded = UNSET
        else:
            rows_loaded = self.rows_loaded

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
                "status": status,
            }
        )
        if duration is not UNSET:
            field_dict["duration"] = duration
        if rows_loaded is not UNSET:
            field_dict["rows_loaded"] = rows_loaded
        if time_started is not UNSET:
            field_dict["time_started"] = time_started

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        status = RunStatus(d.pop("status"))

        def _parse_duration(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        duration = _parse_duration(d.pop("duration", UNSET))

        def _parse_rows_loaded(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rows_loaded = _parse_rows_loaded(d.pop("rows_loaded", UNSET))

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

        recent_run_response = cls(
            id=id,
            status=status,
            duration=duration,
            rows_loaded=rows_loaded,
            time_started=time_started,
        )

        recent_run_response.additional_properties = d
        return recent_run_response

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
