from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_config_code_completion_model import AIConfigCodeCompletionModel
    from ..models.ai_config_custom_prompts import AIConfigCustomPrompts
    from ..models.ai_config_default_model import AIConfigDefaultModel
    from ..models.ai_config_free_tier import AIConfigFreeTier
    from ..models.ai_config_max_tokens_per_model import AIConfigMaxTokensPerModel
    from ..models.ai_config_metadata_model import AIConfigMetadataModel
    from ..models.ai_config_model_pricing import AIConfigModelPricing
    from ..models.ai_config_providers import AIConfigProviders


T = TypeVar("T", bound="AIConfig")


@_attrs_define
class AIConfig:
    """
    Attributes:
        providers (Union[Unset, AIConfigProviders]):
        default_model (Union[Unset, AIConfigDefaultModel]):
        metadata_model (Union[Unset, AIConfigMetadataModel]):
        code_completion_model (Union[Unset, AIConfigCodeCompletionModel]):
        custom_prompts (Union[Unset, AIConfigCustomPrompts]):
        max_tokens_per_model (Union[Unset, AIConfigMaxTokensPerModel]):
        free_tier (Union[Unset, AIConfigFreeTier]): Read-only. Present when the workspace has no AI provider of its own
            and is running on Windmill's free tier. Ignored on write.
        model_pricing (Union[Unset, AIConfigModelPricing]):
    """

    providers: Union[Unset, "AIConfigProviders"] = UNSET
    default_model: Union[Unset, "AIConfigDefaultModel"] = UNSET
    metadata_model: Union[Unset, "AIConfigMetadataModel"] = UNSET
    code_completion_model: Union[Unset, "AIConfigCodeCompletionModel"] = UNSET
    custom_prompts: Union[Unset, "AIConfigCustomPrompts"] = UNSET
    max_tokens_per_model: Union[Unset, "AIConfigMaxTokensPerModel"] = UNSET
    free_tier: Union[Unset, "AIConfigFreeTier"] = UNSET
    model_pricing: Union[Unset, "AIConfigModelPricing"] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_config_code_completion_model import AIConfigCodeCompletionModel
        from ..models.ai_config_custom_prompts import AIConfigCustomPrompts
        from ..models.ai_config_default_model import AIConfigDefaultModel
        from ..models.ai_config_free_tier import AIConfigFreeTier
        from ..models.ai_config_max_tokens_per_model import AIConfigMaxTokensPerModel
        from ..models.ai_config_metadata_model import AIConfigMetadataModel
        from ..models.ai_config_model_pricing import AIConfigModelPricing
        from ..models.ai_config_providers import AIConfigProviders

        d = src_dict.copy()
        _providers = d.pop("providers", UNSET)
        providers: Union[Unset, AIConfigProviders]
        if isinstance(_providers, Unset):
            providers = UNSET
        else:
            providers = AIConfigProviders.from_dict(_providers)

        _default_model = d.pop("default_model", UNSET)
        default_model: Union[Unset, AIConfigDefaultModel]
        if isinstance(_default_model, Unset):
            default_model = UNSET
        else:
            default_model = AIConfigDefaultModel.from_dict(_default_model)

        _metadata_model = d.pop("metadata_model", UNSET)
        metadata_model: Union[Unset, AIConfigMetadataModel]
        if isinstance(_metadata_model, Unset):
            metadata_model = UNSET
        else:
            metadata_model = AIConfigMetadataModel.from_dict(_metadata_model)

        _code_completion_model = d.pop("code_completion_model", UNSET)
        code_completion_model: Union[Unset, AIConfigCodeCompletionModel]
        if isinstance(_code_completion_model, Unset):
            code_completion_model = UNSET
        else:
            code_completion_model = AIConfigCodeCompletionModel.from_dict(_code_completion_model)

        _custom_prompts = d.pop("custom_prompts", UNSET)
        custom_prompts: Union[Unset, AIConfigCustomPrompts]
        if isinstance(_custom_prompts, Unset):
            custom_prompts = UNSET
        else:
            custom_prompts = AIConfigCustomPrompts.from_dict(_custom_prompts)

        _max_tokens_per_model = d.pop("max_tokens_per_model", UNSET)
        max_tokens_per_model: Union[Unset, AIConfigMaxTokensPerModel]
        if isinstance(_max_tokens_per_model, Unset):
            max_tokens_per_model = UNSET
        else:
            max_tokens_per_model = AIConfigMaxTokensPerModel.from_dict(_max_tokens_per_model)

        _free_tier = d.pop("free_tier", UNSET)
        free_tier: Union[Unset, AIConfigFreeTier]
        if isinstance(_free_tier, Unset):
            free_tier = UNSET
        else:
            free_tier = AIConfigFreeTier.from_dict(_free_tier)

        _model_pricing = d.pop("model_pricing", UNSET)
        model_pricing: Union[Unset, AIConfigModelPricing]
        if isinstance(_model_pricing, Unset):
            model_pricing = UNSET
        else:
            model_pricing = AIConfigModelPricing.from_dict(_model_pricing)

        ai_config = cls(
            providers=providers,
            default_model=default_model,
            metadata_model=metadata_model,
            code_completion_model=code_completion_model,
            custom_prompts=custom_prompts,
            max_tokens_per_model=max_tokens_per_model,
            free_tier=free_tier,
            model_pricing=model_pricing,
        )

        ai_config.additional_properties = d
        return ai_config

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
