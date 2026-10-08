from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.pipeline_run_status import PipelineRunStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineStatsResponse")


@_attrs_define
class PipelineStatsResponse:
    """
    Attributes:
        pipeline_name (str):
        succeeded_pipeline_run_count (int):
        success_ratio (float):
        total_bytes_loaded (int):
        total_pipeline_run_count (int):
        total_rows_extracted (int):
        total_rows_loaded (int):
        average_duration_ms (int | None | Unset):
        latest_dataset_name (None | str | Unset):
        latest_destination_name (None | str | Unset):
        latest_pipeline_run_at (datetime.datetime | None | Unset):
        latest_source_names (list[str] | None | Unset):
        latest_status (None | PipelineRunStatus | str | Unset):
        total_duration_ms (int | Unset):  Default: 0.
    """

    pipeline_name: str
    succeeded_pipeline_run_count: int
    success_ratio: float
    total_bytes_loaded: int
    total_pipeline_run_count: int
    total_rows_extracted: int
    total_rows_loaded: int
    average_duration_ms: int | None | Unset = UNSET
    latest_dataset_name: None | str | Unset = UNSET
    latest_destination_name: None | str | Unset = UNSET
    latest_pipeline_run_at: datetime.datetime | None | Unset = UNSET
    latest_source_names: list[str] | None | Unset = UNSET
    latest_status: None | PipelineRunStatus | str | Unset = UNSET
    total_duration_ms: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pipeline_name = self.pipeline_name

        succeeded_pipeline_run_count = self.succeeded_pipeline_run_count

        success_ratio = self.success_ratio

        total_bytes_loaded = self.total_bytes_loaded

        total_pipeline_run_count = self.total_pipeline_run_count

        total_rows_extracted = self.total_rows_extracted

        total_rows_loaded = self.total_rows_loaded

        average_duration_ms: int | None | Unset
        if isinstance(self.average_duration_ms, Unset):
            average_duration_ms = UNSET
        else:
            average_duration_ms = self.average_duration_ms

        latest_dataset_name: None | str | Unset
        if isinstance(self.latest_dataset_name, Unset):
            latest_dataset_name = UNSET
        else:
            latest_dataset_name = self.latest_dataset_name

        latest_destination_name: None | str | Unset
        if isinstance(self.latest_destination_name, Unset):
            latest_destination_name = UNSET
        else:
            latest_destination_name = self.latest_destination_name

        latest_pipeline_run_at: None | str | Unset
        if isinstance(self.latest_pipeline_run_at, Unset):
            latest_pipeline_run_at = UNSET
        elif isinstance(self.latest_pipeline_run_at, datetime.datetime):
            latest_pipeline_run_at = self.latest_pipeline_run_at.isoformat()
        else:
            latest_pipeline_run_at = self.latest_pipeline_run_at

        latest_source_names: list[str] | None | Unset
        if isinstance(self.latest_source_names, Unset):
            latest_source_names = UNSET
        elif isinstance(self.latest_source_names, list):
            latest_source_names = self.latest_source_names

        else:
            latest_source_names = self.latest_source_names

        latest_status: None | str | Unset
        if isinstance(self.latest_status, Unset):
            latest_status = UNSET
        elif isinstance(self.latest_status, PipelineRunStatus):
            latest_status = self.latest_status.value
        else:
            latest_status = self.latest_status

        total_duration_ms = self.total_duration_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pipeline_name": pipeline_name,
                "succeeded_pipeline_run_count": succeeded_pipeline_run_count,
                "success_ratio": success_ratio,
                "total_bytes_loaded": total_bytes_loaded,
                "total_pipeline_run_count": total_pipeline_run_count,
                "total_rows_extracted": total_rows_extracted,
                "total_rows_loaded": total_rows_loaded,
            }
        )
        if average_duration_ms is not UNSET:
            field_dict["average_duration_ms"] = average_duration_ms
        if latest_dataset_name is not UNSET:
            field_dict["latest_dataset_name"] = latest_dataset_name
        if latest_destination_name is not UNSET:
            field_dict["latest_destination_name"] = latest_destination_name
        if latest_pipeline_run_at is not UNSET:
            field_dict["latest_pipeline_run_at"] = latest_pipeline_run_at
        if latest_source_names is not UNSET:
            field_dict["latest_source_names"] = latest_source_names
        if latest_status is not UNSET:
            field_dict["latest_status"] = latest_status
        if total_duration_ms is not UNSET:
            field_dict["total_duration_ms"] = total_duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pipeline_name = d.pop("pipeline_name")

        succeeded_pipeline_run_count = d.pop("succeeded_pipeline_run_count")

        success_ratio = d.pop("success_ratio")

        total_bytes_loaded = d.pop("total_bytes_loaded")

        total_pipeline_run_count = d.pop("total_pipeline_run_count")

        total_rows_extracted = d.pop("total_rows_extracted")

        total_rows_loaded = d.pop("total_rows_loaded")

        def _parse_average_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        average_duration_ms = _parse_average_duration_ms(
            d.pop("average_duration_ms", UNSET)
        )

        def _parse_latest_dataset_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latest_dataset_name = _parse_latest_dataset_name(
            d.pop("latest_dataset_name", UNSET)
        )

        def _parse_latest_destination_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latest_destination_name = _parse_latest_destination_name(
            d.pop("latest_destination_name", UNSET)
        )

        def _parse_latest_pipeline_run_at(
            data: object,
        ) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_pipeline_run_at_type_0 = isoparse(data)

                return latest_pipeline_run_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        latest_pipeline_run_at = _parse_latest_pipeline_run_at(
            d.pop("latest_pipeline_run_at", UNSET)
        )

        def _parse_latest_source_names(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                latest_source_names_type_0 = cast(list[str], data)

                return latest_source_names_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        latest_source_names = _parse_latest_source_names(
            d.pop("latest_source_names", UNSET)
        )

        def _parse_latest_status(
            data: object,
        ) -> None | PipelineRunStatus | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_status_type_0 = PipelineRunStatus(data)

                return latest_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PipelineRunStatus | str | Unset, data)

        latest_status = _parse_latest_status(d.pop("latest_status", UNSET))

        total_duration_ms = d.pop("total_duration_ms", UNSET)

        pipeline_stats_response = cls(
            pipeline_name=pipeline_name,
            succeeded_pipeline_run_count=succeeded_pipeline_run_count,
            success_ratio=success_ratio,
            total_bytes_loaded=total_bytes_loaded,
            total_pipeline_run_count=total_pipeline_run_count,
            total_rows_extracted=total_rows_extracted,
            total_rows_loaded=total_rows_loaded,
            average_duration_ms=average_duration_ms,
            latest_dataset_name=latest_dataset_name,
            latest_destination_name=latest_destination_name,
            latest_pipeline_run_at=latest_pipeline_run_at,
            latest_source_names=latest_source_names,
            latest_status=latest_status,
            total_duration_ms=total_duration_ms,
        )

        pipeline_stats_response.additional_properties = d
        return pipeline_stats_response

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
