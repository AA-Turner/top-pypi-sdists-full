from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_copilot_settings_state_response_200_instance_ai_summary_providers_item_provider import (
    GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItemProvider,
)

T = TypeVar("T", bound="GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem")


@_attrs_define
class GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem:
    """
    Attributes:
        provider (GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItemProvider):
        models (List[str]):
    """

    provider: GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItemProvider
    models: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        provider = self.provider.value

        models = self.models

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "models": models,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        provider = GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItemProvider(d.pop("provider"))

        models = cast(List[str], d.pop("models"))

        get_copilot_settings_state_response_200_instance_ai_summary_providers_item = cls(
            provider=provider,
            models=models,
        )

        get_copilot_settings_state_response_200_instance_ai_summary_providers_item.additional_properties = d
        return get_copilot_settings_state_response_200_instance_ai_summary_providers_item

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
