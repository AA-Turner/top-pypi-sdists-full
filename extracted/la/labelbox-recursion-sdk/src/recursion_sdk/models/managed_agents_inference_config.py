from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_inference_config_provider_params import ManagedAgentsInferenceConfigProviderParams





T = TypeVar("T", bound="ManagedAgentsInferenceConfig")



@_attrs_define
class ManagedAgentsInferenceConfig:
    """ Sampling and generation settings for a model call, mirroring the provider's own request parameters. Set it on an
    agent or a session to govern every turn, and read it back on a model event to see what the call actually used.

        Example:
            {'max_tokens': 1, 'provider_params': {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5,
                'top_p': 1.5}

        Attributes:
            max_tokens (int | Unset): Upper bound on tokens the model may generate for one assistant turn (the provider's
                max_tokens). Omit or 0 to use the model reference's default.
            provider_params (ManagedAgentsInferenceConfigProviderParams | Unset): Extra provider request parameters merged
                into the inference call for options this schema does not model. Keys are provider-specific and are passed
                through unvalidated.
            reasoning_effort (str | Unset): Provider-native reasoning depth value. For gateway models, use one of
                supported_reasoning_efforts from the models catalog; omit it to follow the provider's current default.
            temperature (float | Unset): Sampling temperature passed through to the provider, typically 0.0-2.0. Lower
                values are more deterministic. Omit to use the provider default.
            top_p (float | Unset): Nucleus-sampling probability mass (0.0-1.0) passed through to the provider. Prefer
                setting either this or temperature, not both. Omit to use the provider default.
     """

    max_tokens: int | Unset = UNSET
    provider_params: ManagedAgentsInferenceConfigProviderParams | Unset = UNSET
    reasoning_effort: str | Unset = UNSET
    temperature: float | Unset = UNSET
    top_p: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_inference_config_provider_params import ManagedAgentsInferenceConfigProviderParams # noqa: PLC0415
        max_tokens = self.max_tokens

        provider_params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provider_params, Unset):
            provider_params = self.provider_params.to_dict()

        reasoning_effort = self.reasoning_effort

        temperature = self.temperature

        top_p = self.top_p


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if provider_params is not UNSET:
            field_dict["provider_params"] = provider_params
        if reasoning_effort is not UNSET:
            field_dict["reasoning_effort"] = reasoning_effort
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_inference_config_provider_params import ManagedAgentsInferenceConfigProviderParams # noqa: PLC0415
        d = dict(src_dict)
        max_tokens = d.pop("max_tokens", UNSET)

        _provider_params = d.pop("provider_params", UNSET)
        provider_params: ManagedAgentsInferenceConfigProviderParams | Unset
        if isinstance(_provider_params,  Unset):
            provider_params = UNSET
        else:
            provider_params = ManagedAgentsInferenceConfigProviderParams.from_dict(_provider_params)




        reasoning_effort = d.pop("reasoning_effort", UNSET)

        temperature = d.pop("temperature", UNSET)

        top_p = d.pop("top_p", UNSET)

        managed_agents_inference_config = cls(
            max_tokens=max_tokens,
            provider_params=provider_params,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            top_p=top_p,
        )


        managed_agents_inference_config.additional_properties = d
        return managed_agents_inference_config

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
