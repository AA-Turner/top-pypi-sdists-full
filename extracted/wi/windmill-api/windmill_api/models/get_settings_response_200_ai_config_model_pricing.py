from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_settings_response_200_ai_config_model_pricing_additional_property import (
        GetSettingsResponse200AiConfigModelPricingAdditionalProperty,
    )


T = TypeVar("T", bound="GetSettingsResponse200AiConfigModelPricing")


@_attrs_define
class GetSettingsResponse200AiConfigModelPricing:
    """ """

    additional_properties: Dict[str, "GetSettingsResponse200AiConfigModelPricingAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_ai_config_model_pricing_additional_property import (
            GetSettingsResponse200AiConfigModelPricingAdditionalProperty,
        )

        d = src_dict.copy()
        get_settings_response_200_ai_config_model_pricing = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetSettingsResponse200AiConfigModelPricingAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_settings_response_200_ai_config_model_pricing.additional_properties = additional_properties
        return get_settings_response_200_ai_config_model_pricing

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetSettingsResponse200AiConfigModelPricingAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetSettingsResponse200AiConfigModelPricingAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
