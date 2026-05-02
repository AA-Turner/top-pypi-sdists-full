from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_copilot_settings_state_response_200_instance_ai_summary_code_completion_model import (
        GetCopilotSettingsStateResponse200InstanceAiSummaryCodeCompletionModel,
    )
    from ..models.get_copilot_settings_state_response_200_instance_ai_summary_default_model import (
        GetCopilotSettingsStateResponse200InstanceAiSummaryDefaultModel,
    )
    from ..models.get_copilot_settings_state_response_200_instance_ai_summary_providers_item import (
        GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem,
    )


T = TypeVar("T", bound="GetCopilotSettingsStateResponse200InstanceAiSummary")


@_attrs_define
class GetCopilotSettingsStateResponse200InstanceAiSummary:
    """
    Attributes:
        providers (List['GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem']):
        default_model (Union[Unset, GetCopilotSettingsStateResponse200InstanceAiSummaryDefaultModel]):
        code_completion_model (Union[Unset, GetCopilotSettingsStateResponse200InstanceAiSummaryCodeCompletionModel]):
    """

    providers: List["GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem"]
    default_model: Union[Unset, "GetCopilotSettingsStateResponse200InstanceAiSummaryDefaultModel"] = UNSET
    code_completion_model: Union[
        Unset, "GetCopilotSettingsStateResponse200InstanceAiSummaryCodeCompletionModel"
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()

            providers.append(providers_item)

        default_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_model, Unset):
            default_model = self.default_model.to_dict()

        code_completion_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_completion_model, Unset):
            code_completion_model = self.code_completion_model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "providers": providers,
            }
        )
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if code_completion_model is not UNSET:
            field_dict["code_completion_model"] = code_completion_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_copilot_settings_state_response_200_instance_ai_summary_code_completion_model import (
            GetCopilotSettingsStateResponse200InstanceAiSummaryCodeCompletionModel,
        )
        from ..models.get_copilot_settings_state_response_200_instance_ai_summary_default_model import (
            GetCopilotSettingsStateResponse200InstanceAiSummaryDefaultModel,
        )
        from ..models.get_copilot_settings_state_response_200_instance_ai_summary_providers_item import (
            GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem,
        )

        d = src_dict.copy()
        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = GetCopilotSettingsStateResponse200InstanceAiSummaryProvidersItem.from_dict(
                providers_item_data
            )

            providers.append(providers_item)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, GetCopilotSettingsStateResponse200InstanceAiSummaryDefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = GetCopilotSettingsStateResponse200InstanceAiSummaryDefaultModel.from_dict(_default_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, GetCopilotSettingsStateResponse200InstanceAiSummaryCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = GetCopilotSettingsStateResponse200InstanceAiSummaryCodeCompletionModel.from_dict(
                _code_completion_model
            )

        get_copilot_settings_state_response_200_instance_ai_summary = cls(
            providers=providers,
            default_model=default_model,
            code_completion_model=code_completion_model,
        )

        get_copilot_settings_state_response_200_instance_ai_summary.additional_properties = d
        return get_copilot_settings_state_response_200_instance_ai_summary

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
