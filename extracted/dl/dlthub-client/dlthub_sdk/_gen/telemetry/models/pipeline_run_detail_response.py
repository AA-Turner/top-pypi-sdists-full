from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.load_package_response import LoadPackageResponse
    from ..models.pipeline_run_resource_response import PipelineRunResourceResponse
    from ..models.pipeline_run_table_response import PipelineRunTableResponse


T = TypeVar("T", bound="PipelineRunDetailResponse")


@_attrs_define
class PipelineRunDetailResponse:
    """
    Attributes:
        id (UUID):
        pipeline_name (str):
        status (str):
        transaction_id (str):
        dataset_name (None | str | Unset):
        destination_name (None | str | Unset):
        dlt_plus_version (None | str | Unset):
        dlt_version (None | str | Unset):
        duration_ms (int | None | Unset):
        error_message (None | str | Unset):
        error_step (None | str | Unset):
        error_traceback (None | str | Unset):
        extract_duration_ms (int | None | Unset):
        finished_at (datetime.datetime | None | Unset):
        has_failed_jobs (bool | None | Unset):  Default: False.
        has_pending_packages (bool | None | Unset):  Default: False.
        has_schema_migration (bool | None | Unset):
        is_empty_run (bool | None | Unset):  Default: False.
        job_run_id (None | Unset | UUID):
        load_duration_ms (int | None | Unset):
        load_package_count (int | None | Unset):  Default: 0.
        load_packages (list[LoadPackageResponse] | Unset):
        normalize_duration_ms (int | None | Unset):
        os_name (None | str | Unset):
        os_version (None | str | Unset):
        python_version (None | str | Unset):
        resources (list[PipelineRunResourceResponse] | Unset):
        started_at (datetime.datetime | None | Unset):
        tables (list[PipelineRunTableResponse] | Unset):
        total_bytes_extracted (int | Unset):  Default: 0.
        total_bytes_loaded (int | Unset):  Default: 0.
        total_rows_extracted (int | Unset):  Default: 0.
        total_rows_loaded (int | Unset):  Default: 0.
    """

    id: UUID
    pipeline_name: str
    status: str
    transaction_id: str
    dataset_name: None | str | Unset = UNSET
    destination_name: None | str | Unset = UNSET
    dlt_plus_version: None | str | Unset = UNSET
    dlt_version: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    error_step: None | str | Unset = UNSET
    error_traceback: None | str | Unset = UNSET
    extract_duration_ms: int | None | Unset = UNSET
    finished_at: datetime.datetime | None | Unset = UNSET
    has_failed_jobs: bool | None | Unset = False
    has_pending_packages: bool | None | Unset = False
    has_schema_migration: bool | None | Unset = UNSET
    is_empty_run: bool | None | Unset = False
    job_run_id: None | Unset | UUID = UNSET
    load_duration_ms: int | None | Unset = UNSET
    load_package_count: int | None | Unset = 0
    load_packages: list[LoadPackageResponse] | Unset = UNSET
    normalize_duration_ms: int | None | Unset = UNSET
    os_name: None | str | Unset = UNSET
    os_version: None | str | Unset = UNSET
    python_version: None | str | Unset = UNSET
    resources: list[PipelineRunResourceResponse] | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    tables: list[PipelineRunTableResponse] | Unset = UNSET
    total_bytes_extracted: int | Unset = 0
    total_bytes_loaded: int | Unset = 0
    total_rows_extracted: int | Unset = 0
    total_rows_loaded: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        pipeline_name = self.pipeline_name

        status = self.status

        transaction_id = self.transaction_id

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

        dlt_plus_version: None | str | Unset
        if isinstance(self.dlt_plus_version, Unset):
            dlt_plus_version = UNSET
        else:
            dlt_plus_version = self.dlt_plus_version

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

        error_traceback: None | str | Unset
        if isinstance(self.error_traceback, Unset):
            error_traceback = UNSET
        else:
            error_traceback = self.error_traceback

        extract_duration_ms: int | None | Unset
        if isinstance(self.extract_duration_ms, Unset):
            extract_duration_ms = UNSET
        else:
            extract_duration_ms = self.extract_duration_ms

        finished_at: None | str | Unset
        if isinstance(self.finished_at, Unset):
            finished_at = UNSET
        elif isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        has_failed_jobs: bool | None | Unset
        if isinstance(self.has_failed_jobs, Unset):
            has_failed_jobs = UNSET
        else:
            has_failed_jobs = self.has_failed_jobs

        has_pending_packages: bool | None | Unset
        if isinstance(self.has_pending_packages, Unset):
            has_pending_packages = UNSET
        else:
            has_pending_packages = self.has_pending_packages

        has_schema_migration: bool | None | Unset
        if isinstance(self.has_schema_migration, Unset):
            has_schema_migration = UNSET
        else:
            has_schema_migration = self.has_schema_migration

        is_empty_run: bool | None | Unset
        if isinstance(self.is_empty_run, Unset):
            is_empty_run = UNSET
        else:
            is_empty_run = self.is_empty_run

        job_run_id: None | str | Unset
        if isinstance(self.job_run_id, Unset):
            job_run_id = UNSET
        elif isinstance(self.job_run_id, UUID):
            job_run_id = str(self.job_run_id)
        else:
            job_run_id = self.job_run_id

        load_duration_ms: int | None | Unset
        if isinstance(self.load_duration_ms, Unset):
            load_duration_ms = UNSET
        else:
            load_duration_ms = self.load_duration_ms

        load_package_count: int | None | Unset
        if isinstance(self.load_package_count, Unset):
            load_package_count = UNSET
        else:
            load_package_count = self.load_package_count

        load_packages: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.load_packages, Unset):
            load_packages = []
            for load_packages_item_data in self.load_packages:
                load_packages_item = load_packages_item_data.to_dict()
                load_packages.append(load_packages_item)

        normalize_duration_ms: int | None | Unset
        if isinstance(self.normalize_duration_ms, Unset):
            normalize_duration_ms = UNSET
        else:
            normalize_duration_ms = self.normalize_duration_ms

        os_name: None | str | Unset
        if isinstance(self.os_name, Unset):
            os_name = UNSET
        else:
            os_name = self.os_name

        os_version: None | str | Unset
        if isinstance(self.os_version, Unset):
            os_version = UNSET
        else:
            os_version = self.os_version

        python_version: None | str | Unset
        if isinstance(self.python_version, Unset):
            python_version = UNSET
        else:
            python_version = self.python_version

        resources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = []
            for resources_item_data in self.resources:
                resources_item = resources_item_data.to_dict()
                resources.append(resources_item)

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        tables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tables, Unset):
            tables = []
            for tables_item_data in self.tables:
                tables_item = tables_item_data.to_dict()
                tables.append(tables_item)

        total_bytes_extracted = self.total_bytes_extracted

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
                "transaction_id": transaction_id,
            }
        )
        if dataset_name is not UNSET:
            field_dict["dataset_name"] = dataset_name
        if destination_name is not UNSET:
            field_dict["destination_name"] = destination_name
        if dlt_plus_version is not UNSET:
            field_dict["dlt_plus_version"] = dlt_plus_version
        if dlt_version is not UNSET:
            field_dict["dlt_version"] = dlt_version
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_step is not UNSET:
            field_dict["error_step"] = error_step
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if extract_duration_ms is not UNSET:
            field_dict["extract_duration_ms"] = extract_duration_ms
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if has_failed_jobs is not UNSET:
            field_dict["has_failed_jobs"] = has_failed_jobs
        if has_pending_packages is not UNSET:
            field_dict["has_pending_packages"] = has_pending_packages
        if has_schema_migration is not UNSET:
            field_dict["has_schema_migration"] = has_schema_migration
        if is_empty_run is not UNSET:
            field_dict["is_empty_run"] = is_empty_run
        if job_run_id is not UNSET:
            field_dict["job_run_id"] = job_run_id
        if load_duration_ms is not UNSET:
            field_dict["load_duration_ms"] = load_duration_ms
        if load_package_count is not UNSET:
            field_dict["load_package_count"] = load_package_count
        if load_packages is not UNSET:
            field_dict["load_packages"] = load_packages
        if normalize_duration_ms is not UNSET:
            field_dict["normalize_duration_ms"] = normalize_duration_ms
        if os_name is not UNSET:
            field_dict["os_name"] = os_name
        if os_version is not UNSET:
            field_dict["os_version"] = os_version
        if python_version is not UNSET:
            field_dict["python_version"] = python_version
        if resources is not UNSET:
            field_dict["resources"] = resources
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if tables is not UNSET:
            field_dict["tables"] = tables
        if total_bytes_extracted is not UNSET:
            field_dict["total_bytes_extracted"] = total_bytes_extracted
        if total_bytes_loaded is not UNSET:
            field_dict["total_bytes_loaded"] = total_bytes_loaded
        if total_rows_extracted is not UNSET:
            field_dict["total_rows_extracted"] = total_rows_extracted
        if total_rows_loaded is not UNSET:
            field_dict["total_rows_loaded"] = total_rows_loaded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.load_package_response import LoadPackageResponse
        from ..models.pipeline_run_resource_response import PipelineRunResourceResponse
        from ..models.pipeline_run_table_response import PipelineRunTableResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        pipeline_name = d.pop("pipeline_name")

        status = d.pop("status")

        transaction_id = d.pop("transaction_id")

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

        def _parse_dlt_plus_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dlt_plus_version = _parse_dlt_plus_version(d.pop("dlt_plus_version", UNSET))

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

        def _parse_error_traceback(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_traceback = _parse_error_traceback(d.pop("error_traceback", UNSET))

        def _parse_extract_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        extract_duration_ms = _parse_extract_duration_ms(
            d.pop("extract_duration_ms", UNSET)
        )

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

        def _parse_has_failed_jobs(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_failed_jobs = _parse_has_failed_jobs(d.pop("has_failed_jobs", UNSET))

        def _parse_has_pending_packages(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_pending_packages = _parse_has_pending_packages(
            d.pop("has_pending_packages", UNSET)
        )

        def _parse_has_schema_migration(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_schema_migration = _parse_has_schema_migration(
            d.pop("has_schema_migration", UNSET)
        )

        def _parse_is_empty_run(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_empty_run = _parse_is_empty_run(d.pop("is_empty_run", UNSET))

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

        def _parse_load_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        load_duration_ms = _parse_load_duration_ms(d.pop("load_duration_ms", UNSET))

        def _parse_load_package_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        load_package_count = _parse_load_package_count(
            d.pop("load_package_count", UNSET)
        )

        _load_packages = d.pop("load_packages", UNSET)
        load_packages: list[LoadPackageResponse] | Unset = UNSET
        if _load_packages is not UNSET:
            load_packages = []
            for load_packages_item_data in _load_packages:
                load_packages_item = LoadPackageResponse.from_dict(
                    load_packages_item_data
                )

                load_packages.append(load_packages_item)

        def _parse_normalize_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        normalize_duration_ms = _parse_normalize_duration_ms(
            d.pop("normalize_duration_ms", UNSET)
        )

        def _parse_os_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        os_name = _parse_os_name(d.pop("os_name", UNSET))

        def _parse_os_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        os_version = _parse_os_version(d.pop("os_version", UNSET))

        def _parse_python_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        python_version = _parse_python_version(d.pop("python_version", UNSET))

        _resources = d.pop("resources", UNSET)
        resources: list[PipelineRunResourceResponse] | Unset = UNSET
        if _resources is not UNSET:
            resources = []
            for resources_item_data in _resources:
                resources_item = PipelineRunResourceResponse.from_dict(
                    resources_item_data
                )

                resources.append(resources_item)

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

        _tables = d.pop("tables", UNSET)
        tables: list[PipelineRunTableResponse] | Unset = UNSET
        if _tables is not UNSET:
            tables = []
            for tables_item_data in _tables:
                tables_item = PipelineRunTableResponse.from_dict(tables_item_data)

                tables.append(tables_item)

        total_bytes_extracted = d.pop("total_bytes_extracted", UNSET)

        total_bytes_loaded = d.pop("total_bytes_loaded", UNSET)

        total_rows_extracted = d.pop("total_rows_extracted", UNSET)

        total_rows_loaded = d.pop("total_rows_loaded", UNSET)

        pipeline_run_detail_response = cls(
            id=id,
            pipeline_name=pipeline_name,
            status=status,
            transaction_id=transaction_id,
            dataset_name=dataset_name,
            destination_name=destination_name,
            dlt_plus_version=dlt_plus_version,
            dlt_version=dlt_version,
            duration_ms=duration_ms,
            error_message=error_message,
            error_step=error_step,
            error_traceback=error_traceback,
            extract_duration_ms=extract_duration_ms,
            finished_at=finished_at,
            has_failed_jobs=has_failed_jobs,
            has_pending_packages=has_pending_packages,
            has_schema_migration=has_schema_migration,
            is_empty_run=is_empty_run,
            job_run_id=job_run_id,
            load_duration_ms=load_duration_ms,
            load_package_count=load_package_count,
            load_packages=load_packages,
            normalize_duration_ms=normalize_duration_ms,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
            resources=resources,
            started_at=started_at,
            tables=tables,
            total_bytes_extracted=total_bytes_extracted,
            total_bytes_loaded=total_bytes_loaded,
            total_rows_extracted=total_rows_extracted,
            total_rows_loaded=total_rows_loaded,
        )

        pipeline_run_detail_response.additional_properties = d
        return pipeline_run_detail_response

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
