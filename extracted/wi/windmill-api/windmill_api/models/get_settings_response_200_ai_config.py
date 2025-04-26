from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_ai_config_code_completion_model import (
        GetSettingsResponse200AiConfigCodeCompletionModel,
    )
    from ..models.get_settings_response_200_ai_config_default_model import GetSettingsResponse200AiConfigDefaultModel
    from ..models.get_settings_response_200_ai_config_providers import GetSettingsResponse200AiConfigProviders


T = TypeVar("T", bound="GetSettingsResponse200AiConfig")


@_attrs_define
class GetSettingsResponse200AiConfig:
    """
    Attributes:
        providers (Union[Unset, GetSettingsResponse200AiConfigProviders]):
        default_model (Union[Unset, GetSettingsResponse200AiConfigDefaultModel]):
        code_completion_model (Union[Unset, GetSettingsResponse200AiConfigCodeCompletionModel]):
    """

    providers: Union[Unset, "GetSettingsResponse200AiConfigProviders"] = UNSET
    default_model: Union[Unset, "GetSettingsResponse200AiConfigDefaultModel"] = UNSET
    code_completion_model: Union[Unset, "GetSettingsResponse200AiConfigCodeCompletionModel"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        providers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers.to_dict()

        default_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_model, Unset):
            default_model = self.default_model.to_dict()

        code_completion_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_completion_model, Unset):
            code_completion_model = self.code_completion_model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if providers is not UNSET:
            field_dict["providers"] = providers
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if code_completion_model is not UNSET:
            field_dict["code_completion_model"] = code_completion_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_ai_config_code_completion_model import (
            GetSettingsResponse200AiConfigCodeCompletionModel,
        )
        from ..models.get_settings_response_200_ai_config_default_model import (
            GetSettingsResponse200AiConfigDefaultModel,
        )
        from ..models.get_settings_response_200_ai_config_providers import GetSettingsResponse200AiConfigProviders

        d = src_dict.copy()
        _providers = d.pop("providers", UNSET)
        providers: Union[Unset, GetSettingsResponse200AiConfigProviders]
        if isinstance(_providers, Unset):
            providers = UNSET
        else:
            providers = GetSettingsResponse200AiConfigProviders.from_dict(_providers)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, GetSettingsResponse200AiConfigDefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = GetSettingsResponse200AiConfigDefaultModel.from_dict(_default_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, GetSettingsResponse200AiConfigCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = GetSettingsResponse200AiConfigCodeCompletionModel.from_dict(_code_completion_model)

        get_settings_response_200_ai_config = cls(
            providers=providers,
            default_model=default_model,
            code_completion_model=code_completion_model,
        )

        get_settings_response_200_ai_config.additional_properties = d
        return get_settings_response_200_ai_config

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
