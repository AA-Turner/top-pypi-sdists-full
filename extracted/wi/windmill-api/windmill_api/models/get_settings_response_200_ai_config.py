from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_ai_config_code_completion_model import (
        GetSettingsResponse200AiConfigCodeCompletionModel,
    )
    from ..models.get_settings_response_200_ai_config_context_window_per_model import (
        GetSettingsResponse200AiConfigContextWindowPerModel,
    )
    from ..models.get_settings_response_200_ai_config_custom_prompts import GetSettingsResponse200AiConfigCustomPrompts
    from ..models.get_settings_response_200_ai_config_default_model import GetSettingsResponse200AiConfigDefaultModel
    from ..models.get_settings_response_200_ai_config_free_tier import GetSettingsResponse200AiConfigFreeTier
    from ..models.get_settings_response_200_ai_config_max_tokens_per_model import (
        GetSettingsResponse200AiConfigMaxTokensPerModel,
    )
    from ..models.get_settings_response_200_ai_config_metadata_model import GetSettingsResponse200AiConfigMetadataModel
    from ..models.get_settings_response_200_ai_config_model_pricing import GetSettingsResponse200AiConfigModelPricing
    from ..models.get_settings_response_200_ai_config_providers import GetSettingsResponse200AiConfigProviders


T = TypeVar("T", bound="GetSettingsResponse200AiConfig")


@_attrs_define
class GetSettingsResponse200AiConfig:
    """
    Attributes:
        providers (Union[Unset, GetSettingsResponse200AiConfigProviders]):
        default_model (Union[Unset, GetSettingsResponse200AiConfigDefaultModel]):
        metadata_model (Union[Unset, GetSettingsResponse200AiConfigMetadataModel]):
        code_completion_model (Union[Unset, GetSettingsResponse200AiConfigCodeCompletionModel]):
        custom_prompts (Union[Unset, GetSettingsResponse200AiConfigCustomPrompts]):
        max_tokens_per_model (Union[Unset, GetSettingsResponse200AiConfigMaxTokensPerModel]):
        free_tier (Union[Unset, GetSettingsResponse200AiConfigFreeTier]): Read-only. Present when the workspace has no
            AI provider of its own and is running on Windmill's free tier. Ignored on write.
        model_pricing (Union[Unset, GetSettingsResponse200AiConfigModelPricing]):
        context_window_per_model (Union[Unset, GetSettingsResponse200AiConfigContextWindowPerModel]): Context window in
            tokens per `provider:model`, overriding the built-in table the AI chat uses to decide when to compact its
            history.
        copilot_disabled (Union[Unset, bool]): Hides the Windmill AI assistant (chat, sessions, code generation,
            completion, fixes) from the workspace UI. Read from the workspace's own settings even when the providers served
            fall back to the instance config. AI agent steps and the AI sandbox in flows are unaffected.
        sessions_storage_disabled (Union[Unset, bool]): Stops browsers from backing their AI sessions up to the
            workspace's object storage. Read from the workspace's own settings like `copilot_disabled`.
        sessions_retention_days (Union[Unset, int]): The server deletes the backup of a session no push has reached for
            this many days. Unset keeps backups until the user deletes the session. Read from the workspace's own settings
            like `copilot_disabled`.
    """

    providers: Union[Unset, "GetSettingsResponse200AiConfigProviders"] = UNSET
    default_model: Union[Unset, "GetSettingsResponse200AiConfigDefaultModel"] = UNSET
    metadata_model: Union[Unset, "GetSettingsResponse200AiConfigMetadataModel"] = UNSET
    code_completion_model: Union[Unset, "GetSettingsResponse200AiConfigCodeCompletionModel"] = UNSET
    custom_prompts: Union[Unset, "GetSettingsResponse200AiConfigCustomPrompts"] = UNSET
    max_tokens_per_model: Union[Unset, "GetSettingsResponse200AiConfigMaxTokensPerModel"] = UNSET
    free_tier: Union[Unset, "GetSettingsResponse200AiConfigFreeTier"] = UNSET
    model_pricing: Union[Unset, "GetSettingsResponse200AiConfigModelPricing"] = UNSET
    context_window_per_model: Union[Unset, "GetSettingsResponse200AiConfigContextWindowPerModel"] = UNSET
    copilot_disabled: Union[Unset, bool] = UNSET
    sessions_storage_disabled: Union[Unset, bool] = UNSET
    sessions_retention_days: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        providers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers.to_dict()

        default_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_model, Unset):
            default_model = self.default_model.to_dict()

        metadata_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata_model, Unset):
            metadata_model = self.metadata_model.to_dict()

        code_completion_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.code_completion_model, Unset):
            code_completion_model = self.code_completion_model.to_dict()

        custom_prompts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_prompts, Unset):
            custom_prompts = self.custom_prompts.to_dict()

        max_tokens_per_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.max_tokens_per_model, Unset):
            max_tokens_per_model = self.max_tokens_per_model.to_dict()

        free_tier: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.free_tier, Unset):
            free_tier = self.free_tier.to_dict()

        model_pricing: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model_pricing, Unset):
            model_pricing = self.model_pricing.to_dict()

        context_window_per_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context_window_per_model, Unset):
            context_window_per_model = self.context_window_per_model.to_dict()

        copilot_disabled = self.copilot_disabled
        sessions_storage_disabled = self.sessions_storage_disabled
        sessions_retention_days = self.sessions_retention_days

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if providers is not UNSET:
            field_dict["providers"] = providers
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if metadata_model is not UNSET:
            field_dict["metadata_model"] = metadata_model
        if code_completion_model is not UNSET:
            field_dict["code_completion_model"] = code_completion_model
        if custom_prompts is not UNSET:
            field_dict["custom_prompts"] = custom_prompts
        if max_tokens_per_model is not UNSET:
            field_dict["max_tokens_per_model"] = max_tokens_per_model
        if free_tier is not UNSET:
            field_dict["free_tier"] = free_tier
        if model_pricing is not UNSET:
            field_dict["model_pricing"] = model_pricing
        if context_window_per_model is not UNSET:
            field_dict["context_window_per_model"] = context_window_per_model
        if copilot_disabled is not UNSET:
            field_dict["copilot_disabled"] = copilot_disabled
        if sessions_storage_disabled is not UNSET:
            field_dict["sessions_storage_disabled"] = sessions_storage_disabled
        if sessions_retention_days is not UNSET:
            field_dict["sessions_retention_days"] = sessions_retention_days

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_ai_config_code_completion_model import (
            GetSettingsResponse200AiConfigCodeCompletionModel,
        )
        from ..models.get_settings_response_200_ai_config_context_window_per_model import (
            GetSettingsResponse200AiConfigContextWindowPerModel,
        )
        from ..models.get_settings_response_200_ai_config_custom_prompts import (
            GetSettingsResponse200AiConfigCustomPrompts,
        )
        from ..models.get_settings_response_200_ai_config_default_model import (
            GetSettingsResponse200AiConfigDefaultModel,
        )
        from ..models.get_settings_response_200_ai_config_free_tier import GetSettingsResponse200AiConfigFreeTier
        from ..models.get_settings_response_200_ai_config_max_tokens_per_model import (
            GetSettingsResponse200AiConfigMaxTokensPerModel,
        )
        from ..models.get_settings_response_200_ai_config_metadata_model import (
            GetSettingsResponse200AiConfigMetadataModel,
        )
        from ..models.get_settings_response_200_ai_config_model_pricing import (
            GetSettingsResponse200AiConfigModelPricing,
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

        _metadata_model = d.pop("metadata_model", UNSET)
        metadata_model: Union[Unset, GetSettingsResponse200AiConfigMetadataModel]
        if isinstance(_metadata_model, Unset):
            metadata_model = UNSET
        else:
            metadata_model = GetSettingsResponse200AiConfigMetadataModel.from_dict(_metadata_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, GetSettingsResponse200AiConfigCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = GetSettingsResponse200AiConfigCodeCompletionModel.from_dict(_code_completion_model)

        _custom_prompts = d.pop("custom_prompts", UNSET)
        custom_prompts: Union[Unset, GetSettingsResponse200AiConfigCustomPrompts]
        if isinstance(_custom_prompts, Unset):
            custom_prompts = UNSET
        else:
            custom_prompts = GetSettingsResponse200AiConfigCustomPrompts.from_dict(_custom_prompts)

        _max_tokens_per_model = d.pop("max_tokens_per_model", UNSET)
        max_tokens_per_model: Union[Unset, GetSettingsResponse200AiConfigMaxTokensPerModel]
        if isinstance(_max_tokens_per_model, Unset):
            max_tokens_per_model = UNSET
        else:
            max_tokens_per_model = GetSettingsResponse200AiConfigMaxTokensPerModel.from_dict(_max_tokens_per_model)

        _free_tier = d.pop("free_tier", UNSET)
        free_tier: Union[Unset, GetSettingsResponse200AiConfigFreeTier]
        if isinstance(_free_tier, Unset):
            free_tier = UNSET
        else:
            free_tier = GetSettingsResponse200AiConfigFreeTier.from_dict(_free_tier)

        _model_pricing = d.pop("model_pricing", UNSET)
        model_pricing: Union[Unset, GetSettingsResponse200AiConfigModelPricing]
        if isinstance(_model_pricing, Unset):
            model_pricing = UNSET
        else:
            model_pricing = GetSettingsResponse200AiConfigModelPricing.from_dict(_model_pricing)

        _context_window_per_model = d.pop("context_window_per_model", UNSET)
        context_window_per_model: Union[Unset, GetSettingsResponse200AiConfigContextWindowPerModel]
        if isinstance(_context_window_per_model, Unset):
            context_window_per_model = UNSET
        else:
            context_window_per_model = GetSettingsResponse200AiConfigContextWindowPerModel.from_dict(
                _context_window_per_model
            )

        copilot_disabled = d.pop("copilot_disabled", UNSET)

        sessions_storage_disabled = d.pop("sessions_storage_disabled", UNSET)

        sessions_retention_days = d.pop("sessions_retention_days", UNSET)

        get_settings_response_200_ai_config = cls(
            providers=providers,
            default_model=default_model,
            metadata_model=metadata_model,
            code_completion_model=code_completion_model,
            custom_prompts=custom_prompts,
            max_tokens_per_model=max_tokens_per_model,
            free_tier=free_tier,
            model_pricing=model_pricing,
            context_window_per_model=context_window_per_model,
            copilot_disabled=copilot_disabled,
            sessions_storage_disabled=sessions_storage_disabled,
            sessions_retention_days=sessions_retention_days,
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
