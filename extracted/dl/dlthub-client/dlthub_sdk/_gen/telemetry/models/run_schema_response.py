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
    from ..models.schema_migration import SchemaMigration
    from ..models.schema_table_response import SchemaTableResponse


T = TypeVar("T", bound="RunSchemaResponse")


@_attrs_define
class RunSchemaResponse:
    """
    Attributes:
        load_id (str):
        schema_hash (str):
        schema_name (str):
        first_seen_at (datetime.datetime | None | Unset):
        first_seen_pipeline_run_id (None | Unset | UUID):
        migration (None | SchemaMigration | Unset):
        previous_hashes (list[str] | None | Unset):
        schema_version (int | None | Unset):
        table_count (int | None | Unset):
        tables (list[SchemaTableResponse] | Unset):
        total_column_count (int | None | Unset):
    """

    load_id: str
    schema_hash: str
    schema_name: str
    first_seen_at: datetime.datetime | None | Unset = UNSET
    first_seen_pipeline_run_id: None | Unset | UUID = UNSET
    migration: None | SchemaMigration | Unset = UNSET
    previous_hashes: list[str] | None | Unset = UNSET
    schema_version: int | None | Unset = UNSET
    table_count: int | None | Unset = UNSET
    tables: list[SchemaTableResponse] | Unset = UNSET
    total_column_count: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.schema_migration import SchemaMigration

        load_id = self.load_id

        schema_hash = self.schema_hash

        schema_name = self.schema_name

        first_seen_at: None | str | Unset
        if isinstance(self.first_seen_at, Unset):
            first_seen_at = UNSET
        elif isinstance(self.first_seen_at, datetime.datetime):
            first_seen_at = self.first_seen_at.isoformat()
        else:
            first_seen_at = self.first_seen_at

        first_seen_pipeline_run_id: None | str | Unset
        if isinstance(self.first_seen_pipeline_run_id, Unset):
            first_seen_pipeline_run_id = UNSET
        elif isinstance(self.first_seen_pipeline_run_id, UUID):
            first_seen_pipeline_run_id = str(self.first_seen_pipeline_run_id)
        else:
            first_seen_pipeline_run_id = self.first_seen_pipeline_run_id

        migration: dict[str, Any] | None | Unset
        if isinstance(self.migration, Unset):
            migration = UNSET
        elif isinstance(self.migration, SchemaMigration):
            migration = self.migration.to_dict()
        else:
            migration = self.migration

        previous_hashes: list[str] | None | Unset
        if isinstance(self.previous_hashes, Unset):
            previous_hashes = UNSET
        elif isinstance(self.previous_hashes, list):
            previous_hashes = self.previous_hashes

        else:
            previous_hashes = self.previous_hashes

        schema_version: int | None | Unset
        if isinstance(self.schema_version, Unset):
            schema_version = UNSET
        else:
            schema_version = self.schema_version

        table_count: int | None | Unset
        if isinstance(self.table_count, Unset):
            table_count = UNSET
        else:
            table_count = self.table_count

        tables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tables, Unset):
            tables = []
            for tables_item_data in self.tables:
                tables_item = tables_item_data.to_dict()
                tables.append(tables_item)

        total_column_count: int | None | Unset
        if isinstance(self.total_column_count, Unset):
            total_column_count = UNSET
        else:
            total_column_count = self.total_column_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "load_id": load_id,
                "schema_hash": schema_hash,
                "schema_name": schema_name,
            }
        )
        if first_seen_at is not UNSET:
            field_dict["first_seen_at"] = first_seen_at
        if first_seen_pipeline_run_id is not UNSET:
            field_dict["first_seen_pipeline_run_id"] = first_seen_pipeline_run_id
        if migration is not UNSET:
            field_dict["migration"] = migration
        if previous_hashes is not UNSET:
            field_dict["previous_hashes"] = previous_hashes
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if table_count is not UNSET:
            field_dict["table_count"] = table_count
        if tables is not UNSET:
            field_dict["tables"] = tables
        if total_column_count is not UNSET:
            field_dict["total_column_count"] = total_column_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schema_migration import SchemaMigration
        from ..models.schema_table_response import SchemaTableResponse

        d = dict(src_dict)
        load_id = d.pop("load_id")

        schema_hash = d.pop("schema_hash")

        schema_name = d.pop("schema_name")

        def _parse_first_seen_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_seen_at_type_0 = isoparse(data)

                return first_seen_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        first_seen_at = _parse_first_seen_at(d.pop("first_seen_at", UNSET))

        def _parse_first_seen_pipeline_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_seen_pipeline_run_id_type_0 = UUID(data)

                return first_seen_pipeline_run_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        first_seen_pipeline_run_id = _parse_first_seen_pipeline_run_id(
            d.pop("first_seen_pipeline_run_id", UNSET)
        )

        def _parse_migration(data: object) -> None | SchemaMigration | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                migration_type_0 = SchemaMigration.from_dict(data)

                return migration_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SchemaMigration | Unset, data)

        migration = _parse_migration(d.pop("migration", UNSET))

        def _parse_previous_hashes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                previous_hashes_type_0 = cast(list[str], data)

                return previous_hashes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        previous_hashes = _parse_previous_hashes(d.pop("previous_hashes", UNSET))

        def _parse_schema_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        schema_version = _parse_schema_version(d.pop("schema_version", UNSET))

        def _parse_table_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        table_count = _parse_table_count(d.pop("table_count", UNSET))

        _tables = d.pop("tables", UNSET)
        tables: list[SchemaTableResponse] | Unset = UNSET
        if _tables is not UNSET:
            tables = []
            for tables_item_data in _tables:
                tables_item = SchemaTableResponse.from_dict(tables_item_data)

                tables.append(tables_item)

        def _parse_total_column_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_column_count = _parse_total_column_count(
            d.pop("total_column_count", UNSET)
        )

        run_schema_response = cls(
            load_id=load_id,
            schema_hash=schema_hash,
            schema_name=schema_name,
            first_seen_at=first_seen_at,
            first_seen_pipeline_run_id=first_seen_pipeline_run_id,
            migration=migration,
            previous_hashes=previous_hashes,
            schema_version=schema_version,
            table_count=table_count,
            tables=tables,
            total_column_count=total_column_count,
        )

        run_schema_response.additional_properties = d
        return run_schema_response

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
