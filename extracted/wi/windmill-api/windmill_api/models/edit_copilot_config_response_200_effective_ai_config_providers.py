from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.edit_copilot_config_response_200_effective_ai_config_providers_additional_property import (
        EditCopilotConfigResponse200EffectiveAiConfigProvidersAdditionalProperty,
    )


T = TypeVar("T", bound="EditCopilotConfigResponse200EffectiveAiConfigProviders")


@_attrs_define
class EditCopilotConfigResponse200EffectiveAiConfigProviders:
    """ """

    additional_properties: Dict[
        str, "EditCopilotConfigResponse200EffectiveAiConfigProvidersAdditionalProperty"
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_copilot_config_response_200_effective_ai_config_providers_additional_property import (
            EditCopilotConfigResponse200EffectiveAiConfigProvidersAdditionalProperty,
        )

        d = src_dict.copy()
        edit_copilot_config_response_200_effective_ai_config_providers = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = EditCopilotConfigResponse200EffectiveAiConfigProvidersAdditionalProperty.from_dict(
                prop_dict
            )

            additional_properties[prop_name] = additional_property

        edit_copilot_config_response_200_effective_ai_config_providers.additional_properties = additional_properties
        return edit_copilot_config_response_200_effective_ai_config_providers

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "EditCopilotConfigResponse200EffectiveAiConfigProvidersAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: "EditCopilotConfigResponse200EffectiveAiConfigProvidersAdditionalProperty"
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
