from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ArrowLicense")


@_attrs_define
class ArrowLicense:
    """
    Attributes:
        license_reference (str): Arrow license reference (e.g., XSP12345). Use this as resource backend_id.
        vendor_name (str):
        offer_name (str):
        offer_sku (str):
        friendly_name (str):
    """

    license_reference: str
    vendor_name: str
    offer_name: str
    offer_sku: str
    friendly_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        license_reference = self.license_reference

        vendor_name = self.vendor_name

        offer_name = self.offer_name

        offer_sku = self.offer_sku

        friendly_name = self.friendly_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "license_reference": license_reference,
                "vendor_name": vendor_name,
                "offer_name": offer_name,
                "offer_sku": offer_sku,
                "friendly_name": friendly_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        license_reference = d.pop("license_reference")

        vendor_name = d.pop("vendor_name")

        offer_name = d.pop("offer_name")

        offer_sku = d.pop("offer_sku")

        friendly_name = d.pop("friendly_name")

        arrow_license = cls(
            license_reference=license_reference,
            vendor_name=vendor_name,
            offer_name=offer_name,
            offer_sku=offer_sku,
            friendly_name=friendly_name,
        )

        arrow_license.additional_properties = d
        return arrow_license

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
