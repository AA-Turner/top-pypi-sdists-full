from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_api_key_usage_totals_usages import ResourceApiKeyUsageTotalsUsages


T = TypeVar("T", bound="ResourceApiKeyUsageTotals")


@_attrs_define
class ResourceApiKeyUsageTotals:
    """
    Attributes:
        usages (ResourceApiKeyUsageTotalsUsages): Usage per component type in the current month, summed over the
            resource's keys, deleted ones included.
    """

    usages: "ResourceApiKeyUsageTotalsUsages"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usages = self.usages.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usages": usages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_api_key_usage_totals_usages import ResourceApiKeyUsageTotalsUsages

        d = dict(src_dict)
        usages = ResourceApiKeyUsageTotalsUsages.from_dict(d.pop("usages"))

        resource_api_key_usage_totals = cls(
            usages=usages,
        )

        resource_api_key_usage_totals.additional_properties = d
        return resource_api_key_usage_totals

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
