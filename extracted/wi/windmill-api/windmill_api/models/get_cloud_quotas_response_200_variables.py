from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetCloudQuotasResponse200Variables")


@_attrs_define
class GetCloudQuotasResponse200Variables:
    """
    Attributes:
        used (int):
        limit (int):
        prunable (int):
    """

    used: int
    limit: int
    prunable: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        used = self.used
        limit = self.limit
        prunable = self.prunable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "used": used,
                "limit": limit,
                "prunable": prunable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        used = d.pop("used")

        limit = d.pop("limit")

        prunable = d.pop("prunable")

        get_cloud_quotas_response_200_variables = cls(
            used=used,
            limit=limit,
            prunable=prunable,
        )

        get_cloud_quotas_response_200_variables.additional_properties = d
        return get_cloud_quotas_response_200_variables

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
