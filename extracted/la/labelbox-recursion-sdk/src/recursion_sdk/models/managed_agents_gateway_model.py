from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsGatewayModel")



@_attrs_define
class ManagedAgentsGatewayModel:
    """ A caller-facing model-catalog entry. It exposes selection and capability metadata without leaking the gateway
    transport configuration used to invoke the model.

        Example:
            {'contextWindow': 1, 'displayName': 'example', 'family': 'example', 'maxOutputTokens': 1, 'modelId': 'example',
                'supportedReasoningEfforts': ['example'], 'supportsImageInput': True}

        Attributes:
            display_name (str): Human-readable model name.
            family (str): Provider or model family reported by the gateway.
            model_id (str): Provider-qualified model id to use when configuring an agent.
            supports_image_input (bool): Whether this routed model accepts image content.
            context_window (int | Unset): Maximum prompt size in tokens, when the gateway reports it.
            max_output_tokens (int | Unset): Maximum generated output in tokens, when the gateway reports it.
            supported_reasoning_efforts (list[str] | Unset): Exact provider-native reasoning effort values. Omitted means
                unknown; an empty array means no explicit effort is valid.
     """

    display_name: str
    family: str
    model_id: str
    supports_image_input: bool
    context_window: int | Unset = UNSET
    max_output_tokens: int | Unset = UNSET
    supported_reasoning_efforts: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        family = self.family

        model_id = self.model_id

        supports_image_input = self.supports_image_input

        context_window = self.context_window

        max_output_tokens = self.max_output_tokens

        supported_reasoning_efforts: list[str] | Unset = UNSET
        if not isinstance(self.supported_reasoning_efforts, Unset):
            supported_reasoning_efforts = self.supported_reasoning_efforts




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "displayName": display_name,
            "family": family,
            "modelId": model_id,
            "supportsImageInput": supports_image_input,
        })
        if context_window is not UNSET:
            field_dict["contextWindow"] = context_window
        if max_output_tokens is not UNSET:
            field_dict["maxOutputTokens"] = max_output_tokens
        if supported_reasoning_efforts is not UNSET:
            field_dict["supportedReasoningEfforts"] = supported_reasoning_efforts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("displayName")

        family = d.pop("family")

        model_id = d.pop("modelId")

        supports_image_input = d.pop("supportsImageInput")

        context_window = d.pop("contextWindow", UNSET)

        max_output_tokens = d.pop("maxOutputTokens", UNSET)

        supported_reasoning_efforts = cast(list[str], d.pop("supportedReasoningEfforts", UNSET))


        managed_agents_gateway_model = cls(
            display_name=display_name,
            family=family,
            model_id=model_id,
            supports_image_input=supports_image_input,
            context_window=context_window,
            max_output_tokens=max_output_tokens,
            supported_reasoning_efforts=supported_reasoning_efforts,
        )


        managed_agents_gateway_model.additional_properties = d
        return managed_agents_gateway_model

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
