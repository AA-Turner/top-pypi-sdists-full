import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingImportResponse")


@_attrs_define
class OfferingImportResponse:
    """
    Attributes:
        imported_offering_uuid (UUID): UUID of the imported offering
        imported_offering_name (str): Name of the imported offering
        imported_components (list[str]): List of imported component types
        import_timestamp (datetime.datetime): Timestamp when the import was completed
        warnings (Union[Unset, list[str]]): List of warnings encountered during import
    """

    imported_offering_uuid: UUID
    imported_offering_name: str
    imported_components: list[str]
    import_timestamp: datetime.datetime
    warnings: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        imported_offering_uuid = str(self.imported_offering_uuid)

        imported_offering_name = self.imported_offering_name

        imported_components = self.imported_components

        import_timestamp = self.import_timestamp.isoformat()

        warnings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imported_offering_uuid": imported_offering_uuid,
                "imported_offering_name": imported_offering_name,
                "imported_components": imported_components,
                "import_timestamp": import_timestamp,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        imported_offering_uuid = UUID(d.pop("imported_offering_uuid"))

        imported_offering_name = d.pop("imported_offering_name")

        imported_components = cast(list[str], d.pop("imported_components"))

        import_timestamp = isoparse(d.pop("import_timestamp"))

        warnings = cast(list[str], d.pop("warnings", UNSET))

        offering_import_response = cls(
            imported_offering_uuid=imported_offering_uuid,
            imported_offering_name=imported_offering_name,
            imported_components=imported_components,
            import_timestamp=import_timestamp,
            warnings=warnings,
        )

        offering_import_response.additional_properties = d
        return offering_import_response

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
