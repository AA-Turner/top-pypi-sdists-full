from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.import_response_list_dto_item_errors_item_severity import ImportResponseListDtoItemErrorsItemSeverity
from ..types import UNSET, Unset






T = TypeVar("T", bound="ImportResponseListDtoItemErrorsItem")



@_attrs_define
class ImportResponseListDtoItemErrorsItem:
    """ One per-row error or warning captured during import processing.

        Attributes:
            external_id (str): External identifier of the problem the error is associated with.
            message (str): Human-readable description of what went wrong for this row.
            severity (ImportResponseListDtoItemErrorsItemSeverity | Unset): Severity of the entry; defaults to error when
                omitted by legacy producers.
     """

    external_id: str
    message: str
    severity: ImportResponseListDtoItemErrorsItemSeverity | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        external_id = self.external_id

        message = self.message

        severity: str | Unset = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "externalId": external_id,
            "message": message,
        })
        if severity is not UNSET:
            field_dict["severity"] = severity

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_id = d.pop("externalId")

        message = d.pop("message")

        _severity = d.pop("severity", UNSET)
        severity: ImportResponseListDtoItemErrorsItemSeverity | Unset
        if isinstance(_severity,  Unset):
            severity = UNSET
        else:
            severity = ImportResponseListDtoItemErrorsItemSeverity(_severity)




        import_response_list_dto_item_errors_item = cls(
            external_id=external_id,
            message=message,
            severity=severity,
        )

        return import_response_list_dto_item_errors_item

