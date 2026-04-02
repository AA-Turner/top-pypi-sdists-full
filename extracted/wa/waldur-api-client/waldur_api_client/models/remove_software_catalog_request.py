from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RemoveSoftwareCatalogRequest")


@_attrs_define
class RemoveSoftwareCatalogRequest:
    """
    Attributes:
        offering_catalog_uuid (UUID): UUID of the offering catalog to remove
    """

    offering_catalog_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_catalog_uuid = str(self.offering_catalog_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_catalog_uuid": offering_catalog_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_catalog_uuid = UUID(d.pop("offering_catalog_uuid"))

        remove_software_catalog_request = cls(
            offering_catalog_uuid=offering_catalog_uuid,
        )

        remove_software_catalog_request.additional_properties = d
        return remove_software_catalog_request

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
