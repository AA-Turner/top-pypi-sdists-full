from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LinkResourceResponse")


@_attrs_define
class LinkResourceResponse:
    """
    Attributes:
        resource_uuid (UUID):
        resource_name (str):
        license_reference (str):
        previous_backend_id (str):
        success (bool):
    """

    resource_uuid: UUID
    resource_name: str
    license_reference: str
    previous_backend_id: str
    success: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        license_reference = self.license_reference

        previous_backend_id = self.previous_backend_id

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "license_reference": license_reference,
                "previous_backend_id": previous_backend_id,
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

        previous_backend_id = d.pop("previous_backend_id")

        success = d.pop("success")

        link_resource_response = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            license_reference=license_reference,
            previous_backend_id=previous_backend_id,
            success=success,
        )

        link_resource_response.additional_properties = d
        return link_resource_response

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
