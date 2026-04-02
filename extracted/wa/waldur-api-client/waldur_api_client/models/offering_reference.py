from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingReference")


@_attrs_define
class OfferingReference:
    """
    Attributes:
        offering_name (str): Name of the offering
        offering_uuid (UUID): UUID of the offering
    """

    offering_name: str
    offering_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_reference = cls(
            offering_name=offering_name,
            offering_uuid=offering_uuid,
        )

        offering_reference.additional_properties = d
        return offering_reference

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
