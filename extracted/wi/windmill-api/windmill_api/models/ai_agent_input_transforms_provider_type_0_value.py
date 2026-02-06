from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_agent_input_transforms_provider_type_0_value_kind import AiAgentInputTransformsProviderType0ValueKind

T = TypeVar("T", bound="AiAgentInputTransformsProviderType0Value")


@_attrs_define
class AiAgentInputTransformsProviderType0Value:
    """Complete AI provider configuration with resource reference and model selection

    Attributes:
        kind (AiAgentInputTransformsProviderType0ValueKind): Supported AI provider types
        resource (str): Resource reference in format '$res:{resource_path}' pointing to provider credentials
        model (str): Model identifier (e.g., 'gpt-4', 'claude-3-opus-20240229', 'gemini-pro')
    """

    kind: AiAgentInputTransformsProviderType0ValueKind
    resource: str
    model: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        resource = self.resource
        model = self.model

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "resource": resource,
                "model": model,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = AiAgentInputTransformsProviderType0ValueKind(d.pop("kind"))

        resource = d.pop("resource")

        model = d.pop("model")

        ai_agent_input_transforms_provider_type_0_value = cls(
            kind=kind,
            resource=resource,
            model=model,
        )

        ai_agent_input_transforms_provider_type_0_value.additional_properties = d
        return ai_agent_input_transforms_provider_type_0_value

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
