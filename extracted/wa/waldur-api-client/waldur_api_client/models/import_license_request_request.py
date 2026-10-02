from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportLicenseRequestRequest")


@_attrs_define
class ImportLicenseRequestRequest:
    """
    Attributes:
        license_reference (str): Arrow license reference (e.g., XSP12345). Will be set as backend_id.
        offering_uuid (UUID): UUID of the Waldur offering to create the resource under.
        project_uuid (UUID): UUID of the project to create the resource in.
        license_name (Union[Unset, str]): Name for the new resource. Defaults to license_reference if not provided.
    """

    license_reference: str
    offering_uuid: UUID
    project_uuid: UUID
    license_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        license_reference = self.license_reference

        offering_uuid = str(self.offering_uuid)

        project_uuid = str(self.project_uuid)

        license_name = self.license_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "license_reference": license_reference,
                "offering_uuid": offering_uuid,
                "project_uuid": project_uuid,
            }
        )
        if license_name is not UNSET:
            field_dict["license_name"] = license_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        license_reference = d.pop("license_reference")

        offering_uuid = UUID(d.pop("offering_uuid"))

        project_uuid = UUID(d.pop("project_uuid"))

        license_name = d.pop("license_name", UNSET)

        import_license_request_request = cls(
            license_reference=license_reference,
            offering_uuid=offering_uuid,
            project_uuid=project_uuid,
            license_name=license_name,
        )

        import_license_request_request.additional_properties = d
        return import_license_request_request

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
