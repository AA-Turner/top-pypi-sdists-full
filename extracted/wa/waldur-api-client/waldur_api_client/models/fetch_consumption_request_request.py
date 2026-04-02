from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FetchConsumptionRequestRequest")


@_attrs_define
class FetchConsumptionRequestRequest:
    """
    Attributes:
        license_reference (str):
        period (str): YYYY-MM format
    """

    license_reference: str
    period: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        license_reference = self.license_reference

        period = self.period

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "license_reference": license_reference,
                "period": period,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        license_reference = d.pop("license_reference")

        period = d.pop("period")

        fetch_consumption_request_request = cls(
            license_reference=license_reference,
            period=period,
        )

        fetch_consumption_request_request.additional_properties = d
        return fetch_consumption_request_request

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
