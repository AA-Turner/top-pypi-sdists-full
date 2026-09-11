from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.schema_column_response_hints_type_0 import (
        SchemaColumnResponseHintsType0,
    )


T = TypeVar("T", bound="SchemaColumnResponse")


@_attrs_define
class SchemaColumnResponse:
    """
    Attributes:
        column_name (str):
        data_type (None | str | Unset):
        fk_parent_column (None | str | Unset):
        fk_parent_table (None | str | Unset):
        hints (None | SchemaColumnResponseHintsType0 | Unset):
        is_foreign_key (bool | None | Unset):
        is_nullable (bool | None | Unset):
        is_primary_key (bool | None | Unset):
    """

    column_name: str
    data_type: None | str | Unset = UNSET
    fk_parent_column: None | str | Unset = UNSET
    fk_parent_table: None | str | Unset = UNSET
    hints: None | SchemaColumnResponseHintsType0 | Unset = UNSET
    is_foreign_key: bool | None | Unset = UNSET
    is_nullable: bool | None | Unset = UNSET
    is_primary_key: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.schema_column_response_hints_type_0 import (
            SchemaColumnResponseHintsType0,
        )

        column_name = self.column_name

        data_type: None | str | Unset
        if isinstance(self.data_type, Unset):
            data_type = UNSET
        else:
            data_type = self.data_type

        fk_parent_column: None | str | Unset
        if isinstance(self.fk_parent_column, Unset):
            fk_parent_column = UNSET
        else:
            fk_parent_column = self.fk_parent_column

        fk_parent_table: None | str | Unset
        if isinstance(self.fk_parent_table, Unset):
            fk_parent_table = UNSET
        else:
            fk_parent_table = self.fk_parent_table

        hints: dict[str, Any] | None | Unset
        if isinstance(self.hints, Unset):
            hints = UNSET
        elif isinstance(self.hints, SchemaColumnResponseHintsType0):
            hints = self.hints.to_dict()
        else:
            hints = self.hints

        is_foreign_key: bool | None | Unset
        if isinstance(self.is_foreign_key, Unset):
            is_foreign_key = UNSET
        else:
            is_foreign_key = self.is_foreign_key

        is_nullable: bool | None | Unset
        if isinstance(self.is_nullable, Unset):
            is_nullable = UNSET
        else:
            is_nullable = self.is_nullable

        is_primary_key: bool | None | Unset
        if isinstance(self.is_primary_key, Unset):
            is_primary_key = UNSET
        else:
            is_primary_key = self.is_primary_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "column_name": column_name,
            }
        )
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if fk_parent_column is not UNSET:
            field_dict["fk_parent_column"] = fk_parent_column
        if fk_parent_table is not UNSET:
            field_dict["fk_parent_table"] = fk_parent_table
        if hints is not UNSET:
            field_dict["hints"] = hints
        if is_foreign_key is not UNSET:
            field_dict["is_foreign_key"] = is_foreign_key
        if is_nullable is not UNSET:
            field_dict["is_nullable"] = is_nullable
        if is_primary_key is not UNSET:
            field_dict["is_primary_key"] = is_primary_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.schema_column_response_hints_type_0 import (
            SchemaColumnResponseHintsType0,
        )

        d = dict(src_dict)
        column_name = d.pop("column_name")

        def _parse_data_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        data_type = _parse_data_type(d.pop("data_type", UNSET))

        def _parse_fk_parent_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fk_parent_column = _parse_fk_parent_column(d.pop("fk_parent_column", UNSET))

        def _parse_fk_parent_table(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fk_parent_table = _parse_fk_parent_table(d.pop("fk_parent_table", UNSET))

        def _parse_hints(data: object) -> None | SchemaColumnResponseHintsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                hints_type_0 = SchemaColumnResponseHintsType0.from_dict(data)

                return hints_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SchemaColumnResponseHintsType0 | Unset, data)

        hints = _parse_hints(d.pop("hints", UNSET))

        def _parse_is_foreign_key(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_foreign_key = _parse_is_foreign_key(d.pop("is_foreign_key", UNSET))

        def _parse_is_nullable(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_nullable = _parse_is_nullable(d.pop("is_nullable", UNSET))

        def _parse_is_primary_key(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_primary_key = _parse_is_primary_key(d.pop("is_primary_key", UNSET))

        schema_column_response = cls(
            column_name=column_name,
            data_type=data_type,
            fk_parent_column=fk_parent_column,
            fk_parent_table=fk_parent_table,
            hints=hints,
            is_foreign_key=is_foreign_key,
            is_nullable=is_nullable,
            is_primary_key=is_primary_key,
        )

        schema_column_response.additional_properties = d
        return schema_column_response

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
