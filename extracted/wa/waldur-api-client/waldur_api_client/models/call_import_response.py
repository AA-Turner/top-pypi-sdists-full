from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallImportResponse")


@_attrs_define
class CallImportResponse:
    """
    Attributes:
        call_uuid (UUID):
        call_name (str):
        imported_sections (list[str]):
        warnings (list[str]):
    """

    call_uuid: UUID
    call_name: str
    imported_sections: list[str]
    warnings: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        imported_sections = self.imported_sections

        warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_uuid": call_uuid,
                "call_name": call_name,
                "imported_sections": imported_sections,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        imported_sections = cast(list[str], d.pop("imported_sections"))

        warnings = cast(list[str], d.pop("warnings"))

        call_import_response = cls(
            call_uuid=call_uuid,
            call_name=call_name,
            imported_sections=imported_sections,
            warnings=warnings,
        )

        call_import_response.additional_properties = d
        return call_import_response

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
