from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_copilot_info_response_200_code_completion_model import (
        GetCopilotInfoResponse200CodeCompletionModel,
    )
    from ..models.get_copilot_info_response_200_custom_prompts import GetCopilotInfoResponse200CustomPrompts
    from ..models.get_copilot_info_response_200_default_model import GetCopilotInfoResponse200DefaultModel
    from ..models.get_copilot_info_response_200_max_tokens_per_model import GetCopilotInfoResponse200MaxTokensPerModel
    from ..models.get_copilot_info_response_200_providers import GetCopilotInfoResponse200Providers


T = TypeVar("T", bound="GetCopilotInfoResponse200")


@_attrs_define
class GetCopilotInfoResponse200:
    """
    Attributes:
        providers (Union[Unset, GetCopilotInfoResponse200Providers]):
        default_model (Union[Unset, GetCopilotInfoResponse200DefaultModel]):
        code_completion_model (Union[Unset, GetCopilotInfoResponse200CodeCompletionModel]):
        custom_prompts (Union[Unset, GetCopilotInfoResponse200CustomPrompts]):
        max_tokens_per_model (Union[Unset, GetCopilotInfoResponse200MaxTokensPerModel]):
    """

    providers: Union[Unset, "GetCopilotInfoResponse200Providers"] = UNSET
    default_model: Union[Unset, "GetCopilotInfoResponse200DefaultModel"] = UNSET
    code_completion_model: Union[Unset, "GetCopilotInfoResponse200CodeCompletionModel"] = UNSET
    custom_prompts: Union[Unset, "GetCopilotInfoResponse200CustomPrompts"] = UNSET
    max_tokens_per_model: Union[Unset, "GetCopilotInfoResponse200MaxTokensPerModel"] = UNSET
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

        custom_prompts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_prompts, Unset):
            custom_prompts = self.custom_prompts.to_dict()

        max_tokens_per_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.max_tokens_per_model, Unset):
            max_tokens_per_model = self.max_tokens_per_model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if providers is not UNSET:
            field_dict["providers"] = providers
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if code_completion_model is not UNSET:
            field_dict["code_completion_model"] = code_completion_model
        if custom_prompts is not UNSET:
            field_dict["custom_prompts"] = custom_prompts
        if max_tokens_per_model is not UNSET:
            field_dict["max_tokens_per_model"] = max_tokens_per_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_copilot_info_response_200_code_completion_model import (
            GetCopilotInfoResponse200CodeCompletionModel,
        )
        from ..models.get_copilot_info_response_200_custom_prompts import GetCopilotInfoResponse200CustomPrompts
        from ..models.get_copilot_info_response_200_default_model import GetCopilotInfoResponse200DefaultModel
        from ..models.get_copilot_info_response_200_max_tokens_per_model import (
            GetCopilotInfoResponse200MaxTokensPerModel,
        )
        from ..models.get_copilot_info_response_200_providers import GetCopilotInfoResponse200Providers

        d = src_dict.copy()
        _providers = d.pop("providers", UNSET)
        providers: Union[Unset, GetCopilotInfoResponse200Providers]
        if isinstance(_providers, Unset):
            providers = UNSET
        else:
            providers = GetCopilotInfoResponse200Providers.from_dict(_providers)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, GetCopilotInfoResponse200DefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = GetCopilotInfoResponse200DefaultModel.from_dict(_default_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, GetCopilotInfoResponse200CodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = GetCopilotInfoResponse200CodeCompletionModel.from_dict(_code_completion_model)

        _custom_prompts = d.pop("custom_prompts", UNSET)
        custom_prompts: Union[Unset, GetCopilotInfoResponse200CustomPrompts]
        if isinstance(_custom_prompts, Unset):
            custom_prompts = UNSET
        else:
            custom_prompts = GetCopilotInfoResponse200CustomPrompts.from_dict(_custom_prompts)

        _max_tokens_per_model = d.pop("max_tokens_per_model", UNSET)
        max_tokens_per_model: Union[Unset, GetCopilotInfoResponse200MaxTokensPerModel]
        if isinstance(_max_tokens_per_model, Unset):
            max_tokens_per_model = UNSET
        else:
            max_tokens_per_model = GetCopilotInfoResponse200MaxTokensPerModel.from_dict(_max_tokens_per_model)

        get_copilot_info_response_200 = cls(
            providers=providers,
            default_model=default_model,
            code_completion_model=code_completion_model,
            custom_prompts=custom_prompts,
            max_tokens_per_model=max_tokens_per_model,
        )

        get_copilot_info_response_200.additional_properties = d
        return get_copilot_info_response_200

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
