from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineRunResponse")


@_attrs_define
class PipelineRunResponse:
    """
    Attributes:
        id (UUID):
        pipeline_name (str):
        status (str):
        dataset_name (None | str | Unset):
        destination_name (None | str | Unset):
        dlt_version (None | str | Unset):
        duration_ms (int | None | Unset):
        error_message (None | str | Unset):
        error_step (None | str | Unset):
        finished_at (datetime.datetime | None | Unset):
        has_schema_migration (bool | None | Unset):
        started_at (datetime.datetime | None | Unset):
        total_bytes_loaded (int | Unset):  Default: 0.
        total_rows_extracted (int | Unset):  Default: 0.
        total_rows_loaded (int | Unset):  Default: 0.
    """

    id: UUID
    pipeline_name: str
    status: str
    dataset_name: None | str | Unset = UNSET
    destination_name: None | str | Unset = UNSET
    dlt_version: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    error_step: None | str | Unset = UNSET
    finished_at: datetime.datetime | None | Unset = UNSET
    has_schema_migration: bool | None | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    total_bytes_loaded: int | Unset = 0
    total_rows_extracted: int | Unset = 0
    total_rows_loaded: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        pipeline_name = self.pipeline_name

        status = self.status

        dataset_name: None | str | Unset
        if isinstance(self.dataset_name, Unset):
            dataset_name = UNSET
        else:
            dataset_name = self.dataset_name

        destination_name: None | str | Unset
        if isinstance(self.destination_name, Unset):
            destination_name = UNSET
        else:
            destination_name = self.destination_name

        dlt_version: None | str | Unset
        if isinstance(self.dlt_version, Unset):
            dlt_version = UNSET
        else:
            dlt_version = self.dlt_version

        duration_ms: int | None | Unset
        if isinstance(self.duration_ms, Unset):
            duration_ms = UNSET
        else:
            duration_ms = self.duration_ms

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        error_step: None | str | Unset
        if isinstance(self.error_step, Unset):
            error_step = UNSET
        else:
            error_step = self.error_step

        finished_at: None | str | Unset
        if isinstance(self.finished_at, Unset):
            finished_at = UNSET
        elif isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        has_schema_migration: bool | None | Unset
        if isinstance(self.has_schema_migration, Unset):
            has_schema_migration = UNSET
        else:
            has_schema_migration = self.has_schema_migration

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        total_bytes_loaded = self.total_bytes_loaded

        total_rows_extracted = self.total_rows_extracted

        total_rows_loaded = self.total_rows_loaded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "pipeline_name": pipeline_name,
                "status": status,
            }
        )
        if dataset_name is not UNSET:
            field_dict["dataset_name"] = dataset_name
        if destination_name is not UNSET:
            field_dict["destination_name"] = destination_name
        if dlt_version is not UNSET:
            field_dict["dlt_version"] = dlt_version
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_step is not UNSET:
            field_dict["error_step"] = error_step
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if has_schema_migration is not UNSET:
            field_dict["has_schema_migration"] = has_schema_migration
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if total_bytes_loaded is not UNSET:
            field_dict["total_bytes_loaded"] = total_bytes_loaded
        if total_rows_extracted is not UNSET:
            field_dict["total_rows_extracted"] = total_rows_extracted
        if total_rows_loaded is not UNSET:
            field_dict["total_rows_loaded"] = total_rows_loaded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        pipeline_name = d.pop("pipeline_name")

        status = d.pop("status")

        def _parse_dataset_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_name = _parse_dataset_name(d.pop("dataset_name", UNSET))

        def _parse_destination_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        destination_name = _parse_destination_name(d.pop("destination_name", UNSET))

        def _parse_dlt_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dlt_version = _parse_dlt_version(d.pop("dlt_version", UNSET))

        def _parse_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        duration_ms = _parse_duration_ms(d.pop("duration_ms", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_error_step(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_step = _parse_error_step(d.pop("error_step", UNSET))

        def _parse_finished_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        finished_at = _parse_finished_at(d.pop("finished_at", UNSET))

        def _parse_has_schema_migration(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_schema_migration = _parse_has_schema_migration(
            d.pop("has_schema_migration", UNSET)
        )

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

        total_bytes_loaded = d.pop("total_bytes_loaded", UNSET)

        total_rows_extracted = d.pop("total_rows_extracted", UNSET)

        total_rows_loaded = d.pop("total_rows_loaded", UNSET)

        pipeline_run_response = cls(
            id=id,
            pipeline_name=pipeline_name,
            status=status,
            dataset_name=dataset_name,
            destination_name=destination_name,
            dlt_version=dlt_version,
            duration_ms=duration_ms,
            error_message=error_message,
            error_step=error_step,
            finished_at=finished_at,
            has_schema_migration=has_schema_migration,
            started_at=started_at,
            total_bytes_loaded=total_bytes_loaded,
            total_rows_extracted=total_rows_extracted,
            total_rows_loaded=total_rows_loaded,
        )

        pipeline_run_response.additional_properties = d
        return pipeline_run_response

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
