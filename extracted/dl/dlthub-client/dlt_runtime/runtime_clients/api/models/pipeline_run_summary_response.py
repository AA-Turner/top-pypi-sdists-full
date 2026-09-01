from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineRunSummaryResponse")


@_attrs_define
class PipelineRunSummaryResponse:
    """
    Attributes:
        pipeline_name (str): Name of the dlt pipeline
        dataset_name (None | str | Unset): Name of the dataset the pipeline wrote to
        destination_name (None | str | Unset): Name of the destination the pipeline wrote to
        duration_ms (int | None | Unset): Duration of the pipeline run in milliseconds
        finished_at (datetime.datetime | None | Unset): When the pipeline run finished
        started_at (datetime.datetime | None | Unset): When the pipeline run started
        status (None | str | Unset): Status of the pipeline run
        total_rows (int | None | Unset): Total number of rows loaded by the pipeline
        transaction_id (None | str | Unset): Transaction ID of the pipeline run
    """

    pipeline_name: str
    dataset_name: None | str | Unset = UNSET
    destination_name: None | str | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    finished_at: datetime.datetime | None | Unset = UNSET
    started_at: datetime.datetime | None | Unset = UNSET
    status: None | str | Unset = UNSET
    total_rows: int | None | Unset = UNSET
    transaction_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pipeline_name = self.pipeline_name

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

        duration_ms: int | None | Unset
        if isinstance(self.duration_ms, Unset):
            duration_ms = UNSET
        else:
            duration_ms = self.duration_ms

        finished_at: None | str | Unset
        if isinstance(self.finished_at, Unset):
            finished_at = UNSET
        elif isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        elif isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        total_rows: int | None | Unset
        if isinstance(self.total_rows, Unset):
            total_rows = UNSET
        else:
            total_rows = self.total_rows

        transaction_id: None | str | Unset
        if isinstance(self.transaction_id, Unset):
            transaction_id = UNSET
        else:
            transaction_id = self.transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pipeline_name": pipeline_name,
            }
        )
        if dataset_name is not UNSET:
            field_dict["dataset_name"] = dataset_name
        if destination_name is not UNSET:
            field_dict["destination_name"] = destination_name
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if status is not UNSET:
            field_dict["status"] = status
        if total_rows is not UNSET:
            field_dict["total_rows"] = total_rows
        if transaction_id is not UNSET:
            field_dict["transaction_id"] = transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pipeline_name = d.pop("pipeline_name")

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

        def _parse_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        duration_ms = _parse_duration_ms(d.pop("duration_ms", UNSET))

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

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_total_rows(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_rows = _parse_total_rows(d.pop("total_rows", UNSET))

        def _parse_transaction_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        transaction_id = _parse_transaction_id(d.pop("transaction_id", UNSET))

        pipeline_run_summary_response = cls(
            pipeline_name=pipeline_name,
            dataset_name=dataset_name,
            destination_name=destination_name,
            duration_ms=duration_ms,
            finished_at=finished_at,
            started_at=started_at,
            status=status,
            total_rows=total_rows,
            transaction_id=transaction_id,
        )

        pipeline_run_summary_response.additional_properties = d
        return pipeline_run_summary_response

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
