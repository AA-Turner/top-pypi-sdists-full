from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LoadPackageResponse")


@_attrs_define
class LoadPackageResponse:
    """
    Attributes:
        load_id (str):
        completed_at (datetime.datetime | None | Unset):
        completed_job_count (int | None | Unset):  Default: 0.
        failed_job_count (int | None | Unset):  Default: 0.
        has_failed_jobs (bool | None | Unset):  Default: False.
        has_schema_migration (bool | None | Unset):  Default: False.
        is_pending (bool | None | Unset):  Default: False.
        job_count (int | None | Unset):  Default: 0.
        load_status (None | str | Unset):
        schema_hash (None | str | Unset):
        schema_name (None | str | Unset):
        total_bytes_loaded (int | None | Unset):  Default: 0.
        total_rows_loaded (int | None | Unset):  Default: 0.
    """

    load_id: str
    completed_at: datetime.datetime | None | Unset = UNSET
    completed_job_count: int | None | Unset = 0
    failed_job_count: int | None | Unset = 0
    has_failed_jobs: bool | None | Unset = False
    has_schema_migration: bool | None | Unset = False
    is_pending: bool | None | Unset = False
    job_count: int | None | Unset = 0
    load_status: None | str | Unset = UNSET
    schema_hash: None | str | Unset = UNSET
    schema_name: None | str | Unset = UNSET
    total_bytes_loaded: int | None | Unset = 0
    total_rows_loaded: int | None | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        load_id = self.load_id

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        completed_job_count: int | None | Unset
        if isinstance(self.completed_job_count, Unset):
            completed_job_count = UNSET
        else:
            completed_job_count = self.completed_job_count

        failed_job_count: int | None | Unset
        if isinstance(self.failed_job_count, Unset):
            failed_job_count = UNSET
        else:
            failed_job_count = self.failed_job_count

        has_failed_jobs: bool | None | Unset
        if isinstance(self.has_failed_jobs, Unset):
            has_failed_jobs = UNSET
        else:
            has_failed_jobs = self.has_failed_jobs

        has_schema_migration: bool | None | Unset
        if isinstance(self.has_schema_migration, Unset):
            has_schema_migration = UNSET
        else:
            has_schema_migration = self.has_schema_migration

        is_pending: bool | None | Unset
        if isinstance(self.is_pending, Unset):
            is_pending = UNSET
        else:
            is_pending = self.is_pending

        job_count: int | None | Unset
        if isinstance(self.job_count, Unset):
            job_count = UNSET
        else:
            job_count = self.job_count

        load_status: None | str | Unset
        if isinstance(self.load_status, Unset):
            load_status = UNSET
        else:
            load_status = self.load_status

        schema_hash: None | str | Unset
        if isinstance(self.schema_hash, Unset):
            schema_hash = UNSET
        else:
            schema_hash = self.schema_hash

        schema_name: None | str | Unset
        if isinstance(self.schema_name, Unset):
            schema_name = UNSET
        else:
            schema_name = self.schema_name

        total_bytes_loaded: int | None | Unset
        if isinstance(self.total_bytes_loaded, Unset):
            total_bytes_loaded = UNSET
        else:
            total_bytes_loaded = self.total_bytes_loaded

        total_rows_loaded: int | None | Unset
        if isinstance(self.total_rows_loaded, Unset):
            total_rows_loaded = UNSET
        else:
            total_rows_loaded = self.total_rows_loaded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "load_id": load_id,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if completed_job_count is not UNSET:
            field_dict["completed_job_count"] = completed_job_count
        if failed_job_count is not UNSET:
            field_dict["failed_job_count"] = failed_job_count
        if has_failed_jobs is not UNSET:
            field_dict["has_failed_jobs"] = has_failed_jobs
        if has_schema_migration is not UNSET:
            field_dict["has_schema_migration"] = has_schema_migration
        if is_pending is not UNSET:
            field_dict["is_pending"] = is_pending
        if job_count is not UNSET:
            field_dict["job_count"] = job_count
        if load_status is not UNSET:
            field_dict["load_status"] = load_status
        if schema_hash is not UNSET:
            field_dict["schema_hash"] = schema_hash
        if schema_name is not UNSET:
            field_dict["schema_name"] = schema_name
        if total_bytes_loaded is not UNSET:
            field_dict["total_bytes_loaded"] = total_bytes_loaded
        if total_rows_loaded is not UNSET:
            field_dict["total_rows_loaded"] = total_rows_loaded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        load_id = d.pop("load_id")

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_completed_job_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        completed_job_count = _parse_completed_job_count(
            d.pop("completed_job_count", UNSET)
        )

        def _parse_failed_job_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        failed_job_count = _parse_failed_job_count(d.pop("failed_job_count", UNSET))

        def _parse_has_failed_jobs(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_failed_jobs = _parse_has_failed_jobs(d.pop("has_failed_jobs", UNSET))

        def _parse_has_schema_migration(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_schema_migration = _parse_has_schema_migration(
            d.pop("has_schema_migration", UNSET)
        )

        def _parse_is_pending(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_pending = _parse_is_pending(d.pop("is_pending", UNSET))

        def _parse_job_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        job_count = _parse_job_count(d.pop("job_count", UNSET))

        def _parse_load_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        load_status = _parse_load_status(d.pop("load_status", UNSET))

        def _parse_schema_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        schema_hash = _parse_schema_hash(d.pop("schema_hash", UNSET))

        def _parse_schema_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        schema_name = _parse_schema_name(d.pop("schema_name", UNSET))

        def _parse_total_bytes_loaded(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_bytes_loaded = _parse_total_bytes_loaded(
            d.pop("total_bytes_loaded", UNSET)
        )

        def _parse_total_rows_loaded(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_rows_loaded = _parse_total_rows_loaded(d.pop("total_rows_loaded", UNSET))

        load_package_response = cls(
            load_id=load_id,
            completed_at=completed_at,
            completed_job_count=completed_job_count,
            failed_job_count=failed_job_count,
            has_failed_jobs=has_failed_jobs,
            has_schema_migration=has_schema_migration,
            is_pending=is_pending,
            job_count=job_count,
            load_status=load_status,
            schema_hash=schema_hash,
            schema_name=schema_name,
            total_bytes_loaded=total_bytes_loaded,
            total_rows_loaded=total_rows_loaded,
        )

        load_package_response.additional_properties = d
        return load_package_response

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
