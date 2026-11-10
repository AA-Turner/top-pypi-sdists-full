from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_settings_response_200_ai_config_web_search_provider import (
    GetSettingsResponse200AiConfigWebSearchProvider,
)

T = TypeVar("T", bound="GetSettingsResponse200AiConfigWebSearch")


@_attrs_define
class GetSettingsResponse200AiConfigWebSearch:
    """The search API the AI chat searches the web and reads pages through when the model's provider has no built-in web
    search. Read from the workspace's own settings like `copilot_disabled`.

        Attributes:
            provider (GetSettingsResponse200AiConfigWebSearchProvider):
            resource_path (str):
    """

    provider: GetSettingsResponse200AiConfigWebSearchProvider
    resource_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        provider = self.provider.value

        resource_path = self.resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "resource_path": resource_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        provider = GetSettingsResponse200AiConfigWebSearchProvider(d.pop("provider"))

        resource_path = d.pop("resource_path")

        get_settings_response_200_ai_config_web_search = cls(
            provider=provider,
            resource_path=resource_path,
        )

        get_settings_response_200_ai_config_web_search.additional_properties = d
        return get_settings_response_200_ai_config_web_search

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
