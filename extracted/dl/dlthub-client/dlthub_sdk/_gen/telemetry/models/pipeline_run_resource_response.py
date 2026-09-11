from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineRunResourceResponse")


@_attrs_define
class PipelineRunResourceResponse:
    """
    Attributes:
        resource_name (str):
        bytes_extracted (int | None | Unset):
        parent_resource_name (None | str | Unset):
        rows_extracted (int | None | Unset):
        schema_name (str | Unset):  Default: ''.
        write_disposition (None | str | Unset):
    """

    resource_name: str
    bytes_extracted: int | None | Unset = UNSET
    parent_resource_name: None | str | Unset = UNSET
    rows_extracted: int | None | Unset = UNSET
    schema_name: str | Unset = ""
    write_disposition: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_name = self.resource_name

        bytes_extracted: int | None | Unset
        if isinstance(self.bytes_extracted, Unset):
            bytes_extracted = UNSET
        else:
            bytes_extracted = self.bytes_extracted

        parent_resource_name: None | str | Unset
        if isinstance(self.parent_resource_name, Unset):
            parent_resource_name = UNSET
        else:
            parent_resource_name = self.parent_resource_name

        rows_extracted: int | None | Unset
        if isinstance(self.rows_extracted, Unset):
            rows_extracted = UNSET
        else:
            rows_extracted = self.rows_extracted

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
                "resource_name": resource_name,
            }
        )
        if bytes_extracted is not UNSET:
            field_dict["bytes_extracted"] = bytes_extracted
        if parent_resource_name is not UNSET:
            field_dict["parent_resource_name"] = parent_resource_name
        if rows_extracted is not UNSET:
            field_dict["rows_extracted"] = rows_extracted
        if schema_name is not UNSET:
            field_dict["schema_name"] = schema_name
        if write_disposition is not UNSET:
            field_dict["write_disposition"] = write_disposition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_name = d.pop("resource_name")

        def _parse_bytes_extracted(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        bytes_extracted = _parse_bytes_extracted(d.pop("bytes_extracted", UNSET))

        def _parse_parent_resource_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_resource_name = _parse_parent_resource_name(
            d.pop("parent_resource_name", UNSET)
        )

        def _parse_rows_extracted(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rows_extracted = _parse_rows_extracted(d.pop("rows_extracted", UNSET))

        schema_name = d.pop("schema_name", UNSET)

        def _parse_write_disposition(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        write_disposition = _parse_write_disposition(d.pop("write_disposition", UNSET))

        pipeline_run_resource_response = cls(
            resource_name=resource_name,
            bytes_extracted=bytes_extracted,
            parent_resource_name=parent_resource_name,
            rows_extracted=rows_extracted,
            schema_name=schema_name,
            write_disposition=write_disposition,
        )

        pipeline_run_resource_response.additional_properties = d
        return pipeline_run_resource_response

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
