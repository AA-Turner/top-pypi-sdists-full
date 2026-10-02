from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ImportPlatformLimitsDto")



@_attrs_define
class ImportPlatformLimitsDto:
    """ Effective platform import limits for the current environment, surfaced to the upload UI.

        Example:
            {'maxImportFileSizeBytes': 104857600}

        Attributes:
            max_import_file_size_bytes (int | None): Platform import-file ceiling in bytes derived from the import worker
                memory limit; null means no platform ceiling is available. Example: 5726623061.
     """

    max_import_file_size_bytes: int | None





    def to_dict(self) -> dict[str, Any]:
        max_import_file_size_bytes: int | None
        max_import_file_size_bytes = self.max_import_file_size_bytes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "maxImportFileSizeBytes": max_import_file_size_bytes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_max_import_file_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_import_file_size_bytes = _parse_max_import_file_size_bytes(d.pop("maxImportFileSizeBytes"))


        import_platform_limits_dto = cls(
            max_import_file_size_bytes=max_import_file_size_bytes,
        )

        return import_platform_limits_dto

