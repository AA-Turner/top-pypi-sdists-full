import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.call_export_response_export_data import CallExportResponseExportData


T = TypeVar("T", bound="CallExportResponse")


@_attrs_define
class CallExportResponse:
    """
    Attributes:
        call_uuid (UUID):
        call_name (str):
        export_data (CallExportResponseExportData):
        exported_sections (list[str]):
        export_timestamp (datetime.datetime):
        warnings (list[str]): Parts that could not be exported, such as unreadable documents.
    """

    call_uuid: UUID
    call_name: str
    export_data: "CallExportResponseExportData"
    exported_sections: list[str]
    export_timestamp: datetime.datetime
    warnings: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        export_data = self.export_data.to_dict()

        exported_sections = self.exported_sections

        export_timestamp = self.export_timestamp.isoformat()

        warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_uuid": call_uuid,
                "call_name": call_name,
                "export_data": export_data,
                "exported_sections": exported_sections,
                "export_timestamp": export_timestamp,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_export_response_export_data import CallExportResponseExportData

        d = dict(src_dict)
        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        export_data = CallExportResponseExportData.from_dict(d.pop("export_data"))

        exported_sections = cast(list[str], d.pop("exported_sections"))

        export_timestamp = isoparse(d.pop("export_timestamp"))

        warnings = cast(list[str], d.pop("warnings"))

        call_export_response = cls(
            call_uuid=call_uuid,
            call_name=call_name,
            export_data=export_data,
            exported_sections=exported_sections,
            export_timestamp=export_timestamp,
            warnings=warnings,
        )

        call_export_response.additional_properties = d
        return call_export_response

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
