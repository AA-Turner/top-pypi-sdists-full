from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetOverviewResponse")


@_attrs_define
class DatasetOverviewResponse:
    """
    Attributes:
        dataset_name (str):
        distinct_pipeline_count (int):
        schema_migration_count (int):
        succeeded_runs (int):
        success_rate (float):
        total_bytes_loaded (int):
        total_rows_loaded (int):
        total_runs (int):
        avg_duration_ms (int | None | Unset):
        latest_destination_name (None | str | Unset):
        latest_pipeline_name (None | str | Unset):
        latest_run_at (datetime.datetime | None | Unset):
        latest_status (None | str | Unset):
    """

    dataset_name: str
    distinct_pipeline_count: int
    schema_migration_count: int
    succeeded_runs: int
    success_rate: float
    total_bytes_loaded: int
    total_rows_loaded: int
    total_runs: int
    avg_duration_ms: int | None | Unset = UNSET
    latest_destination_name: None | str | Unset = UNSET
    latest_pipeline_name: None | str | Unset = UNSET
    latest_run_at: datetime.datetime | None | Unset = UNSET
    latest_status: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_name = self.dataset_name

        distinct_pipeline_count = self.distinct_pipeline_count

        schema_migration_count = self.schema_migration_count

        succeeded_runs = self.succeeded_runs

        success_rate = self.success_rate

        total_bytes_loaded = self.total_bytes_loaded

        total_rows_loaded = self.total_rows_loaded

        total_runs = self.total_runs

        avg_duration_ms: int | None | Unset
        if isinstance(self.avg_duration_ms, Unset):
            avg_duration_ms = UNSET
        else:
            avg_duration_ms = self.avg_duration_ms

        latest_destination_name: None | str | Unset
        if isinstance(self.latest_destination_name, Unset):
            latest_destination_name = UNSET
        else:
            latest_destination_name = self.latest_destination_name

        latest_pipeline_name: None | str | Unset
        if isinstance(self.latest_pipeline_name, Unset):
            latest_pipeline_name = UNSET
        else:
            latest_pipeline_name = self.latest_pipeline_name

        latest_run_at: None | str | Unset
        if isinstance(self.latest_run_at, Unset):
            latest_run_at = UNSET
        elif isinstance(self.latest_run_at, datetime.datetime):
            latest_run_at = self.latest_run_at.isoformat()
        else:
            latest_run_at = self.latest_run_at

        latest_status: None | str | Unset
        if isinstance(self.latest_status, Unset):
            latest_status = UNSET
        else:
            latest_status = self.latest_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_name": dataset_name,
                "distinct_pipeline_count": distinct_pipeline_count,
                "schema_migration_count": schema_migration_count,
                "succeeded_runs": succeeded_runs,
                "success_rate": success_rate,
                "total_bytes_loaded": total_bytes_loaded,
                "total_rows_loaded": total_rows_loaded,
                "total_runs": total_runs,
            }
        )
        if avg_duration_ms is not UNSET:
            field_dict["avg_duration_ms"] = avg_duration_ms
        if latest_destination_name is not UNSET:
            field_dict["latest_destination_name"] = latest_destination_name
        if latest_pipeline_name is not UNSET:
            field_dict["latest_pipeline_name"] = latest_pipeline_name
        if latest_run_at is not UNSET:
            field_dict["latest_run_at"] = latest_run_at
        if latest_status is not UNSET:
            field_dict["latest_status"] = latest_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_name = d.pop("dataset_name")

        distinct_pipeline_count = d.pop("distinct_pipeline_count")

        schema_migration_count = d.pop("schema_migration_count")

        succeeded_runs = d.pop("succeeded_runs")

        success_rate = d.pop("success_rate")

        total_bytes_loaded = d.pop("total_bytes_loaded")

        total_rows_loaded = d.pop("total_rows_loaded")

        total_runs = d.pop("total_runs")

        def _parse_avg_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        avg_duration_ms = _parse_avg_duration_ms(d.pop("avg_duration_ms", UNSET))

        def _parse_latest_destination_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latest_destination_name = _parse_latest_destination_name(
            d.pop("latest_destination_name", UNSET)
        )

        def _parse_latest_pipeline_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latest_pipeline_name = _parse_latest_pipeline_name(
            d.pop("latest_pipeline_name", UNSET)
        )

        def _parse_latest_run_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_run_at_type_0 = isoparse(data)

                return latest_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        latest_run_at = _parse_latest_run_at(d.pop("latest_run_at", UNSET))

        def _parse_latest_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latest_status = _parse_latest_status(d.pop("latest_status", UNSET))

        dataset_overview_response = cls(
            dataset_name=dataset_name,
            distinct_pipeline_count=distinct_pipeline_count,
            schema_migration_count=schema_migration_count,
            succeeded_runs=succeeded_runs,
            success_rate=success_rate,
            total_bytes_loaded=total_bytes_loaded,
            total_rows_loaded=total_rows_loaded,
            total_runs=total_runs,
            avg_duration_ms=avg_duration_ms,
            latest_destination_name=latest_destination_name,
            latest_pipeline_name=latest_pipeline_name,
            latest_run_at=latest_run_at,
            latest_status=latest_status,
        )

        dataset_overview_response.additional_properties = d
        return dataset_overview_response

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
