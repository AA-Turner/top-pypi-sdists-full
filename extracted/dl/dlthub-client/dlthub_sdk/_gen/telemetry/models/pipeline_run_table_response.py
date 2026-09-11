from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineRunTableResponse")


@_attrs_define
class PipelineRunTableResponse:
    """
    Attributes:
        table_name (str):
        bytes_extracted (int | None | Unset):
        bytes_loaded (int | None | Unset):
        file_format (None | str | Unset):
        load_duration_ms (int | None | Unset):
        load_job_state (None | str | Unset):
        rows_extracted (int | None | Unset):
        rows_loaded (int | None | Unset):
        schema_name (str | Unset):  Default: ''.
        write_disposition (None | str | Unset):
    """

    table_name: str
    bytes_extracted: int | None | Unset = UNSET
    bytes_loaded: int | None | Unset = UNSET
    file_format: None | str | Unset = UNSET
    load_duration_ms: int | None | Unset = UNSET
    load_job_state: None | str | Unset = UNSET
    rows_extracted: int | None | Unset = UNSET
    rows_loaded: int | None | Unset = UNSET
    schema_name: str | Unset = ""
    write_disposition: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        table_name = self.table_name

        bytes_extracted: int | None | Unset
        if isinstance(self.bytes_extracted, Unset):
            bytes_extracted = UNSET
        else:
            bytes_extracted = self.bytes_extracted

        bytes_loaded: int | None | Unset
        if isinstance(self.bytes_loaded, Unset):
            bytes_loaded = UNSET
        else:
            bytes_loaded = self.bytes_loaded

        file_format: None | str | Unset
        if isinstance(self.file_format, Unset):
            file_format = UNSET
        else:
            file_format = self.file_format

        load_duration_ms: int | None | Unset
        if isinstance(self.load_duration_ms, Unset):
            load_duration_ms = UNSET
        else:
            load_duration_ms = self.load_duration_ms

        load_job_state: None | str | Unset
        if isinstance(self.load_job_state, Unset):
            load_job_state = UNSET
        else:
            load_job_state = self.load_job_state

        rows_extracted: int | None | Unset
        if isinstance(self.rows_extracted, Unset):
            rows_extracted = UNSET
        else:
            rows_extracted = self.rows_extracted

        rows_loaded: int | None | Unset
        if isinstance(self.rows_loaded, Unset):
            rows_loaded = UNSET
        else:
            rows_loaded = self.rows_loaded

        schema_name = self.schema_name

        write_disposition: None | str | Unset
        if isinstance(self.write_disposition, Unset):
            write_disposition = UNSET
        else:
            write_disposition = self.write_disposition

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_name": table_name,
            }
        )
        if bytes_extracted is not UNSET:
            field_dict["bytes_extracted"] = bytes_extracted
        if bytes_loaded is not UNSET:
            field_dict["bytes_loaded"] = bytes_loaded
        if file_format is not UNSET:
            field_dict["file_format"] = file_format
        if load_duration_ms is not UNSET:
            field_dict["load_duration_ms"] = load_duration_ms
        if load_job_state is not UNSET:
            field_dict["load_job_state"] = load_job_state
        if rows_extracted is not UNSET:
            field_dict["rows_extracted"] = rows_extracted
        if rows_loaded is not UNSET:
            field_dict["rows_loaded"] = rows_loaded
        if schema_name is not UNSET:
            field_dict["schema_name"] = schema_name
        if write_disposition is not UNSET:
            field_dict["write_disposition"] = write_disposition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        table_name = d.pop("table_name")

        def _parse_bytes_extracted(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        bytes_extracted = _parse_bytes_extracted(d.pop("bytes_extracted", UNSET))

        def _parse_bytes_loaded(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        bytes_loaded = _parse_bytes_loaded(d.pop("bytes_loaded", UNSET))

        def _parse_file_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_format = _parse_file_format(d.pop("file_format", UNSET))

        def _parse_load_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        load_duration_ms = _parse_load_duration_ms(d.pop("load_duration_ms", UNSET))

        def _parse_load_job_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        load_job_state = _parse_load_job_state(d.pop("load_job_state", UNSET))

        def _parse_rows_extracted(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rows_extracted = _parse_rows_extracted(d.pop("rows_extracted", UNSET))

        def _parse_rows_loaded(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rows_loaded = _parse_rows_loaded(d.pop("rows_loaded", UNSET))

        schema_name = d.pop("schema_name", UNSET)

        def _parse_write_disposition(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        write_disposition = _parse_write_disposition(d.pop("write_disposition", UNSET))

        pipeline_run_table_response = cls(
            table_name=table_name,
            bytes_extracted=bytes_extracted,
            bytes_loaded=bytes_loaded,
            file_format=file_format,
            load_duration_ms=load_duration_ms,
            load_job_state=load_job_state,
            rows_extracted=rows_extracted,
            rows_loaded=rows_loaded,
            schema_name=schema_name,
            write_disposition=write_disposition,
        )

        pipeline_run_table_response.additional_properties = d
        return pipeline_run_table_response

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
