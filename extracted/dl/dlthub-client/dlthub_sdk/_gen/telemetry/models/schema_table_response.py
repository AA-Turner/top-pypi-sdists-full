from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.table_load_status import TableLoadStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_column_response import SchemaColumnResponse


T = TypeVar("T", bound="SchemaTableResponse")


@_attrs_define
class SchemaTableResponse:
    """
    Attributes:
        table_name (str):
        bytes_extracted (int | None | Unset):
        bytes_loaded (int | None | Unset):
        column_count (int | None | Unset):
        columns (list[SchemaColumnResponse] | Unset):
        last_loaded_at (datetime.datetime | None | Unset):
        load_error_message (None | str | Unset):
        load_status (None | TableLoadStatus | Unset):
        parent_table_name (None | str | Unset):
        primary_key (None | str | Unset):
        rows_extracted (int | None | Unset):
        rows_loaded (int | None | Unset):
        source_pipeline_name (None | str | Unset):
        write_disposition (None | str | Unset):
    """

    table_name: str
    bytes_extracted: int | None | Unset = UNSET
    bytes_loaded: int | None | Unset = UNSET
    column_count: int | None | Unset = UNSET
    columns: list[SchemaColumnResponse] | Unset = UNSET
    last_loaded_at: datetime.datetime | None | Unset = UNSET
    load_error_message: None | str | Unset = UNSET
    load_status: None | TableLoadStatus | Unset = UNSET
    parent_table_name: None | str | Unset = UNSET
    primary_key: None | str | Unset = UNSET
    rows_extracted: int | None | Unset = UNSET
    rows_loaded: int | None | Unset = UNSET
    source_pipeline_name: None | str | Unset = UNSET
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

        column_count: int | None | Unset
        if isinstance(self.column_count, Unset):
            column_count = UNSET
        else:
            column_count = self.column_count

        columns: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        last_loaded_at: None | str | Unset
        if isinstance(self.last_loaded_at, Unset):
            last_loaded_at = UNSET
        elif isinstance(self.last_loaded_at, datetime.datetime):
            last_loaded_at = self.last_loaded_at.isoformat()
        else:
            last_loaded_at = self.last_loaded_at

        load_error_message: None | str | Unset
        if isinstance(self.load_error_message, Unset):
            load_error_message = UNSET
        else:
            load_error_message = self.load_error_message

        load_status: None | str | Unset
        if isinstance(self.load_status, Unset):
            load_status = UNSET
        elif isinstance(self.load_status, TableLoadStatus):
            load_status = self.load_status.value
        else:
            load_status = self.load_status

        parent_table_name: None | str | Unset
        if isinstance(self.parent_table_name, Unset):
            parent_table_name = UNSET
        else:
            parent_table_name = self.parent_table_name

        primary_key: None | str | Unset
        if isinstance(self.primary_key, Unset):
            primary_key = UNSET
        else:
            primary_key = self.primary_key

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

        source_pipeline_name: None | str | Unset
        if isinstance(self.source_pipeline_name, Unset):
            source_pipeline_name = UNSET
        else:
            source_pipeline_name = self.source_pipeline_name

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
        if column_count is not UNSET:
            field_dict["column_count"] = column_count
        if columns is not UNSET:
            field_dict["columns"] = columns
        if last_loaded_at is not UNSET:
            field_dict["last_loaded_at"] = last_loaded_at
        if load_error_message is not UNSET:
            field_dict["load_error_message"] = load_error_message
        if load_status is not UNSET:
            field_dict["load_status"] = load_status
        if parent_table_name is not UNSET:
            field_dict["parent_table_name"] = parent_table_name
        if primary_key is not UNSET:
            field_dict["primary_key"] = primary_key
        if rows_extracted is not UNSET:
            field_dict["rows_extracted"] = rows_extracted
        if rows_loaded is not UNSET:
            field_dict["rows_loaded"] = rows_loaded
        if source_pipeline_name is not UNSET:
            field_dict["source_pipeline_name"] = source_pipeline_name
        if write_disposition is not UNSET:
            field_dict["write_disposition"] = write_disposition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schema_column_response import SchemaColumnResponse

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

        def _parse_column_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        column_count = _parse_column_count(d.pop("column_count", UNSET))

        _columns = d.pop("columns", UNSET)
        columns: list[SchemaColumnResponse] | Unset = UNSET
        if _columns is not UNSET:
            columns = []
            for columns_item_data in _columns:
                columns_item = SchemaColumnResponse.from_dict(columns_item_data)

                columns.append(columns_item)

        def _parse_last_loaded_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_loaded_at_type_0 = isoparse(data)

                return last_loaded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_loaded_at = _parse_last_loaded_at(d.pop("last_loaded_at", UNSET))

        def _parse_load_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        load_error_message = _parse_load_error_message(
            d.pop("load_error_message", UNSET)
        )

        def _parse_load_status(data: object) -> None | TableLoadStatus | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                load_status_type_0 = TableLoadStatus(data)

                return load_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TableLoadStatus | Unset, data)

        load_status = _parse_load_status(d.pop("load_status", UNSET))

        def _parse_parent_table_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_table_name = _parse_parent_table_name(d.pop("parent_table_name", UNSET))

        def _parse_primary_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        primary_key = _parse_primary_key(d.pop("primary_key", UNSET))

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

        def _parse_source_pipeline_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_pipeline_name = _parse_source_pipeline_name(
            d.pop("source_pipeline_name", UNSET)
        )

        def _parse_write_disposition(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        write_disposition = _parse_write_disposition(d.pop("write_disposition", UNSET))

        schema_table_response = cls(
            table_name=table_name,
            bytes_extracted=bytes_extracted,
            bytes_loaded=bytes_loaded,
            column_count=column_count,
            columns=columns,
            last_loaded_at=last_loaded_at,
            load_error_message=load_error_message,
            load_status=load_status,
            parent_table_name=parent_table_name,
            primary_key=primary_key,
            rows_extracted=rows_extracted,
            rows_loaded=rows_loaded,
            source_pipeline_name=source_pipeline_name,
            write_disposition=write_disposition,
        )

        schema_table_response.additional_properties = d
        return schema_table_response

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
