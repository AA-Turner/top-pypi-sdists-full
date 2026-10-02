import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.offering_export_data import OfferingExportData


T = TypeVar("T", bound="OfferingExportResponse")


@_attrs_define
class OfferingExportResponse:
    """
    Attributes:
        offering_uuid (UUID): UUID of the exported offering
        offering_name (str): Name of the exported offering
        export_data (OfferingExportData):
        exported_components (list[str]): List of exported component types
        export_timestamp (datetime.datetime): Timestamp when the export was completed
    """

    offering_uuid: UUID
    offering_name: str
    export_data: "OfferingExportData"
    exported_components: list[str]
    export_timestamp: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        export_data = self.export_data.to_dict()

        exported_components = self.exported_components

        export_timestamp = self.export_timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "export_data": export_data,
                "exported_components": exported_components,
                "export_timestamp": export_timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_export_data import OfferingExportData

        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        export_data = OfferingExportData.from_dict(d.pop("export_data"))

        exported_components = cast(list[str], d.pop("exported_components"))

        export_timestamp = isoparse(d.pop("export_timestamp"))

        offering_export_response = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            export_data=export_data,
            exported_components=exported_components,
            export_timestamp=export_timestamp,
        )

        offering_export_response.additional_properties = d
        return offering_export_response

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
