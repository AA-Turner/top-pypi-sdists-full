from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetNpmProxyConfigResponse200")


@_attrs_define
class GetNpmProxyConfigResponse200:
    """
    Attributes:
        registry_configured (bool):
    """

    registry_configured: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        registry_configured = self.registry_configured

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "registry_configured": registry_configured,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        registry_configured = d.pop("registry_configured")

        get_npm_proxy_config_response_200 = cls(
            registry_configured=registry_configured,
        )

        get_npm_proxy_config_response_200.additional_properties = d
        return get_npm_proxy_config_response_200

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
