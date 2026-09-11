from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineRunBucket")


@_attrs_define
class PipelineRunBucket:
    """
    Attributes:
        bucket_start (datetime.datetime): datetime with the constraint that the value must have timezone info
        avg_duration_ms (int | None | Unset):
        failed_runs (int | Unset):  Default: 0.
        failure_rate (float | Unset):  Default: 0.0.
        succeeded_runs (int | Unset):  Default: 0.
        total_bytes_extracted (int | Unset):  Default: 0.
        total_bytes_loaded (int | Unset):  Default: 0.
        total_duration_ms (int | Unset):  Default: 0.
        total_rows_extracted (int | Unset):  Default: 0.
        total_rows_loaded (int | Unset):  Default: 0.
        total_runs (int | Unset):  Default: 0.
    """

    bucket_start: datetime.datetime
    avg_duration_ms: int | None | Unset = UNSET
    failed_runs: int | Unset = 0
    failure_rate: float | Unset = 0.0
    succeeded_runs: int | Unset = 0
    total_bytes_extracted: int | Unset = 0
    total_bytes_loaded: int | Unset = 0
    total_duration_ms: int | Unset = 0
    total_rows_extracted: int | Unset = 0
    total_rows_loaded: int | Unset = 0
    total_runs: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket_start = self.bucket_start.isoformat()

        avg_duration_ms: int | None | Unset
        if isinstance(self.avg_duration_ms, Unset):
            avg_duration_ms = UNSET
        else:
            avg_duration_ms = self.avg_duration_ms

        failed_runs = self.failed_runs

        failure_rate = self.failure_rate

        succeeded_runs = self.succeeded_runs

        total_bytes_extracted = self.total_bytes_extracted

        total_bytes_loaded = self.total_bytes_loaded

        total_duration_ms = self.total_duration_ms

        total_rows_extracted = self.total_rows_extracted

        total_rows_loaded = self.total_rows_loaded

        total_runs = self.total_runs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket_start": bucket_start,
            }
        )
        if avg_duration_ms is not UNSET:
            field_dict["avg_duration_ms"] = avg_duration_ms
        if failed_runs is not UNSET:
            field_dict["failed_runs"] = failed_runs
        if failure_rate is not UNSET:
            field_dict["failure_rate"] = failure_rate
        if succeeded_runs is not UNSET:
            field_dict["succeeded_runs"] = succeeded_runs
        if total_bytes_extracted is not UNSET:
            field_dict["total_bytes_extracted"] = total_bytes_extracted
        if total_bytes_loaded is not UNSET:
            field_dict["total_bytes_loaded"] = total_bytes_loaded
        if total_duration_ms is not UNSET:
            field_dict["total_duration_ms"] = total_duration_ms
        if total_rows_extracted is not UNSET:
            field_dict["total_rows_extracted"] = total_rows_extracted
        if total_rows_loaded is not UNSET:
            field_dict["total_rows_loaded"] = total_rows_loaded
        if total_runs is not UNSET:
            field_dict["total_runs"] = total_runs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket_start = isoparse(d.pop("bucket_start"))

        def _parse_avg_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        avg_duration_ms = _parse_avg_duration_ms(d.pop("avg_duration_ms", UNSET))

        failed_runs = d.pop("failed_runs", UNSET)

        failure_rate = d.pop("failure_rate", UNSET)

        succeeded_runs = d.pop("succeeded_runs", UNSET)

        total_bytes_extracted = d.pop("total_bytes_extracted", UNSET)

        total_bytes_loaded = d.pop("total_bytes_loaded", UNSET)

        total_duration_ms = d.pop("total_duration_ms", UNSET)

        total_rows_extracted = d.pop("total_rows_extracted", UNSET)

        total_rows_loaded = d.pop("total_rows_loaded", UNSET)

        total_runs = d.pop("total_runs", UNSET)

        pipeline_run_bucket = cls(
            bucket_start=bucket_start,
            avg_duration_ms=avg_duration_ms,
            failed_runs=failed_runs,
            failure_rate=failure_rate,
            succeeded_runs=succeeded_runs,
            total_bytes_extracted=total_bytes_extracted,
            total_bytes_loaded=total_bytes_loaded,
            total_duration_ms=total_duration_ms,
            total_rows_extracted=total_rows_extracted,
            total_rows_loaded=total_rows_loaded,
            total_runs=total_runs,
        )

        pipeline_run_bucket.additional_properties = d
        return pipeline_run_bucket

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
