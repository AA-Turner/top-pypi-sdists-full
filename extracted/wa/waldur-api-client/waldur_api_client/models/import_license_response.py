from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ImportLicenseResponse")


@_attrs_define
class ImportLicenseResponse:
    """
    Attributes:
        resource_uuid (UUID):
        resource_name (str):
        license_reference (str):
        offering_name (str):
        project_name (str):
        success (bool):
    """

    resource_uuid: UUID
    resource_name: str
    license_reference: str
    offering_name: str
    project_name: str
    success: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        license_reference = self.license_reference

        offering_name = self.offering_name

        project_name = self.project_name

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "license_reference": license_reference,
                "offering_name": offering_name,
                "project_name": project_name,
                "success": success,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        license_reference = d.pop("license_reference")

        offering_name = d.pop("offering_name")

        project_name = d.pop("project_name")

        success = d.pop("success")

        import_license_response = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            license_reference=license_reference,
            offering_name=offering_name,
            project_name=project_name,
            success=success,
        )

        import_license_response.additional_properties = d
        return import_license_response

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
