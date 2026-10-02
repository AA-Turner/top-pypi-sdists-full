from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LinkResourceRequestRequest")


@_attrs_define
class LinkResourceRequestRequest:
    """
    Attributes:
        resource_uuid (UUID): UUID of the Waldur resource to link.
        license_reference (str): Arrow license reference to set as backend_id (e.g., XSP12345).
    """

    resource_uuid: UUID
    license_reference: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        license_reference = self.license_reference

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "license_reference": license_reference,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        license_reference = d.pop("license_reference")

        link_resource_request_request = cls(
            resource_uuid=resource_uuid,
            license_reference=license_reference,
        )

        link_resource_request_request.additional_properties = d
        return link_resource_request_request

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
