from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_copilot_config_json_body_code_completion_model import (
        EditCopilotConfigJsonBodyCodeCompletionModel,
    )
    from ..models.edit_copilot_config_json_body_custom_prompts import EditCopilotConfigJsonBodyCustomPrompts
    from ..models.edit_copilot_config_json_body_default_model import EditCopilotConfigJsonBodyDefaultModel
    from ..models.edit_copilot_config_json_body_free_tier import EditCopilotConfigJsonBodyFreeTier
    from ..models.edit_copilot_config_json_body_max_tokens_per_model import EditCopilotConfigJsonBodyMaxTokensPerModel
    from ..models.edit_copilot_config_json_body_metadata_model import EditCopilotConfigJsonBodyMetadataModel
    from ..models.edit_copilot_config_json_body_model_pricing import EditCopilotConfigJsonBodyModelPricing
    from ..models.edit_copilot_config_json_body_providers import EditCopilotConfigJsonBodyProviders


T = TypeVar("T", bound="EditCopilotConfigJsonBody")


@_attrs_define
class EditCopilotConfigJsonBody:
    """
    Attributes:
        providers (Union[Unset, EditCopilotConfigJsonBodyProviders]):
        default_model (Union[Unset, EditCopilotConfigJsonBodyDefaultModel]):
        metadata_model (Union[Unset, EditCopilotConfigJsonBodyMetadataModel]):
        code_completion_model (Union[Unset, EditCopilotConfigJsonBodyCodeCompletionModel]):
        custom_prompts (Union[Unset, EditCopilotConfigJsonBodyCustomPrompts]):
        max_tokens_per_model (Union[Unset, EditCopilotConfigJsonBodyMaxTokensPerModel]):
        free_tier (Union[Unset, EditCopilotConfigJsonBodyFreeTier]): Read-only. Present when the workspace has no AI
            provider of its own and is running on Windmill's free tier. Ignored on write.
        model_pricing (Union[Unset, EditCopilotConfigJsonBodyModelPricing]):
        copilot_disabled (Union[Unset, bool]): Hides the Windmill AI assistant (chat, sessions, code generation,
            completion, fixes) from the workspace UI. Read from the workspace's own settings even when the providers served
            fall back to the instance config. AI agent steps and the AI sandbox in flows are unaffected.
    """

    providers: Union[Unset, "EditCopilotConfigJsonBodyProviders"] = UNSET
    default_model: Union[Unset, "EditCopilotConfigJsonBodyDefaultModel"] = UNSET
    metadata_model: Union[Unset, "EditCopilotConfigJsonBodyMetadataModel"] = UNSET
    code_completion_model: Union[Unset, "EditCopilotConfigJsonBodyCodeCompletionModel"] = UNSET
    custom_prompts: Union[Unset, "EditCopilotConfigJsonBodyCustomPrompts"] = UNSET
    max_tokens_per_model: Union[Unset, "EditCopilotConfigJsonBodyMaxTokensPerModel"] = UNSET
    free_tier: Union[Unset, "EditCopilotConfigJsonBodyFreeTier"] = UNSET
    model_pricing: Union[Unset, "EditCopilotConfigJsonBodyModelPricing"] = UNSET
    copilot_disabled: Union[Unset, bool] = UNSET
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

        copilot_disabled = self.copilot_disabled

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
        if copilot_disabled is not UNSET:
            field_dict["copilot_disabled"] = copilot_disabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_copilot_config_json_body_code_completion_model import (
            EditCopilotConfigJsonBodyCodeCompletionModel,
        )
        from ..models.edit_copilot_config_json_body_custom_prompts import EditCopilotConfigJsonBodyCustomPrompts
        from ..models.edit_copilot_config_json_body_default_model import EditCopilotConfigJsonBodyDefaultModel
        from ..models.edit_copilot_config_json_body_free_tier import EditCopilotConfigJsonBodyFreeTier
        from ..models.edit_copilot_config_json_body_max_tokens_per_model import (
            EditCopilotConfigJsonBodyMaxTokensPerModel,
        )
        from ..models.edit_copilot_config_json_body_metadata_model import EditCopilotConfigJsonBodyMetadataModel
        from ..models.edit_copilot_config_json_body_model_pricing import EditCopilotConfigJsonBodyModelPricing
        from ..models.edit_copilot_config_json_body_providers import EditCopilotConfigJsonBodyProviders

        d = src_dict.copy()
        _providers = d.pop("providers", UNSET)
        providers: Union[Unset, EditCopilotConfigJsonBodyProviders]
        if isinstance(_providers, Unset):
            providers = UNSET
        else:
            providers = EditCopilotConfigJsonBodyProviders.from_dict(_providers)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, EditCopilotConfigJsonBodyDefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = EditCopilotConfigJsonBodyDefaultModel.from_dict(_default_model)

        _metadata_model = d.pop("metadata_model", UNSET)
        metadata_model: Union[Unset, EditCopilotConfigJsonBodyMetadataModel]
        if isinstance(_metadata_model, Unset):
            metadata_model = UNSET
        else:
            metadata_model = EditCopilotConfigJsonBodyMetadataModel.from_dict(_metadata_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, EditCopilotConfigJsonBodyCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = EditCopilotConfigJsonBodyCodeCompletionModel.from_dict(_code_completion_model)

        _custom_prompts = d.pop("custom_prompts", UNSET)
        custom_prompts: Union[Unset, EditCopilotConfigJsonBodyCustomPrompts]
        if isinstance(_custom_prompts, Unset):
            custom_prompts = UNSET
        else:
            custom_prompts = EditCopilotConfigJsonBodyCustomPrompts.from_dict(_custom_prompts)

        _max_tokens_per_model = d.pop("max_tokens_per_model", UNSET)
        max_tokens_per_model: Union[Unset, EditCopilotConfigJsonBodyMaxTokensPerModel]
        if isinstance(_max_tokens_per_model, Unset):
            max_tokens_per_model = UNSET
        else:
            max_tokens_per_model = EditCopilotConfigJsonBodyMaxTokensPerModel.from_dict(_max_tokens_per_model)

        _free_tier = d.pop("free_tier", UNSET)
        free_tier: Union[Unset, EditCopilotConfigJsonBodyFreeTier]
        if isinstance(_free_tier, Unset):
            free_tier = UNSET
        else:
            free_tier = EditCopilotConfigJsonBodyFreeTier.from_dict(_free_tier)

        _model_pricing = d.pop("model_pricing", UNSET)
        model_pricing: Union[Unset, EditCopilotConfigJsonBodyModelPricing]
        if isinstance(_model_pricing, Unset):
            model_pricing = UNSET
        else:
            model_pricing = EditCopilotConfigJsonBodyModelPricing.from_dict(_model_pricing)

        copilot_disabled = d.pop("copilot_disabled", UNSET)

        edit_copilot_config_json_body = cls(
            providers=providers,
            default_model=default_model,
            metadata_model=metadata_model,
            code_completion_model=code_completion_model,
            custom_prompts=custom_prompts,
            max_tokens_per_model=max_tokens_per_model,
            free_tier=free_tier,
            model_pricing=model_pricing,
            copilot_disabled=copilot_disabled,
        )

        edit_copilot_config_json_body.additional_properties = d
        return edit_copilot_config_json_body

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
