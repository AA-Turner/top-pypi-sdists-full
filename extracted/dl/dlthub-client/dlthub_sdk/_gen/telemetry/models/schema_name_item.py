from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaNameItem")


@_attrs_define
class SchemaNameItem:
    """
    Attributes:
        latest_schema_hash (str):
        schema_name (str):
        version_count (int):
        first_seen_at (datetime.datetime | None | Unset):
        latest_schema_version (int | None | Unset):
        latest_table_count (int | None | Unset):
        latest_total_column_count (int | None | Unset):
        latest_version_at (datetime.datetime | None | Unset):
    """

    latest_schema_hash: str
    schema_name: str
    version_count: int
    first_seen_at: datetime.datetime | None | Unset = UNSET
    latest_schema_version: int | None | Unset = UNSET
    latest_table_count: int | None | Unset = UNSET
    latest_total_column_count: int | None | Unset = UNSET
    latest_version_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        latest_schema_hash = self.latest_schema_hash

        schema_name = self.schema_name

        version_count = self.version_count

        first_seen_at: None | str | Unset
        if isinstance(self.first_seen_at, Unset):
            first_seen_at = UNSET
        elif isinstance(self.first_seen_at, datetime.datetime):
            first_seen_at = self.first_seen_at.isoformat()
        else:
            first_seen_at = self.first_seen_at

        latest_schema_version: int | None | Unset
        if isinstance(self.latest_schema_version, Unset):
            latest_schema_version = UNSET
        else:
            latest_schema_version = self.latest_schema_version

        latest_table_count: int | None | Unset
        if isinstance(self.latest_table_count, Unset):
            latest_table_count = UNSET
        else:
            latest_table_count = self.latest_table_count

        latest_total_column_count: int | None | Unset
        if isinstance(self.latest_total_column_count, Unset):
            latest_total_column_count = UNSET
        else:
            latest_total_column_count = self.latest_total_column_count

        latest_version_at: None | str | Unset
        if isinstance(self.latest_version_at, Unset):
            latest_version_at = UNSET
        elif isinstance(self.latest_version_at, datetime.datetime):
            latest_version_at = self.latest_version_at.isoformat()
        else:
            latest_version_at = self.latest_version_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "latest_schema_hash": latest_schema_hash,
                "schema_name": schema_name,
                "version_count": version_count,
            }
        )
        if first_seen_at is not UNSET:
            field_dict["first_seen_at"] = first_seen_at
        if latest_schema_version is not UNSET:
            field_dict["latest_schema_version"] = latest_schema_version
        if latest_table_count is not UNSET:
            field_dict["latest_table_count"] = latest_table_count
        if latest_total_column_count is not UNSET:
            field_dict["latest_total_column_count"] = latest_total_column_count
        if latest_version_at is not UNSET:
            field_dict["latest_version_at"] = latest_version_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        latest_schema_hash = d.pop("latest_schema_hash")

        schema_name = d.pop("schema_name")

        version_count = d.pop("version_count")

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

        def _parse_latest_schema_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latest_schema_version = _parse_latest_schema_version(
            d.pop("latest_schema_version", UNSET)
        )

        def _parse_latest_table_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latest_table_count = _parse_latest_table_count(
            d.pop("latest_table_count", UNSET)
        )

        def _parse_latest_total_column_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        latest_total_column_count = _parse_latest_total_column_count(
            d.pop("latest_total_column_count", UNSET)
        )

        def _parse_latest_version_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_version_at_type_0 = isoparse(data)

                return latest_version_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        latest_version_at = _parse_latest_version_at(d.pop("latest_version_at", UNSET))

        schema_name_item = cls(
            latest_schema_hash=latest_schema_hash,
            schema_name=schema_name,
            version_count=version_count,
            first_seen_at=first_seen_at,
            latest_schema_version=latest_schema_version,
            latest_table_count=latest_table_count,
            latest_total_column_count=latest_total_column_count,
            latest_version_at=latest_version_at,
        )

        schema_name_item.additional_properties = d
        return schema_name_item

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
