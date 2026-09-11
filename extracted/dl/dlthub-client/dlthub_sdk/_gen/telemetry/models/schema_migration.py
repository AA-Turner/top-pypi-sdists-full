from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_migration_modified_table import SchemaMigrationModifiedTable


T = TypeVar("T", bound="SchemaMigration")


@_attrs_define
class SchemaMigration:
    """
    Attributes:
        added_tables (list[str] | Unset):
        modified_tables (list[SchemaMigrationModifiedTable] | Unset):
    """

    added_tables: list[str] | Unset = UNSET
    modified_tables: list[SchemaMigrationModifiedTable] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added_tables: list[str] | Unset = UNSET
        if not isinstance(self.added_tables, Unset):
            added_tables = self.added_tables

        modified_tables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.modified_tables, Unset):
            modified_tables = []
            for modified_tables_item_data in self.modified_tables:
                modified_tables_item = modified_tables_item_data.to_dict()
                modified_tables.append(modified_tables_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if added_tables is not UNSET:
            field_dict["added_tables"] = added_tables
        if modified_tables is not UNSET:
            field_dict["modified_tables"] = modified_tables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schema_migration_modified_table import (
            SchemaMigrationModifiedTable,
        )

        d = dict(src_dict)
        added_tables = cast(list[str], d.pop("added_tables", UNSET))

        _modified_tables = d.pop("modified_tables", UNSET)
        modified_tables: list[SchemaMigrationModifiedTable] | Unset = UNSET
        if _modified_tables is not UNSET:
            modified_tables = []
            for modified_tables_item_data in _modified_tables:
                modified_tables_item = SchemaMigrationModifiedTable.from_dict(
                    modified_tables_item_data
                )

                modified_tables.append(modified_tables_item)

        schema_migration = cls(
            added_tables=added_tables,
            modified_tables=modified_tables,
        )

        schema_migration.additional_properties = d
        return schema_migration

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
