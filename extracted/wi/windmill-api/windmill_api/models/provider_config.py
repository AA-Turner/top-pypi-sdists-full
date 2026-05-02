from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.provider_config_kind import ProviderConfigKind

T = TypeVar("T", bound="ProviderConfig")


@_attrs_define
class ProviderConfig:
    """Complete AI provider configuration with resource reference and model selection

    Attributes:
        kind (ProviderConfigKind): Supported AI provider types
        resource (str): Resource reference in format '$res:{resource_path}' pointing to provider credentials
        model (str): Model identifier (e.g., 'gpt-4', 'claude-3-opus-20240229', 'gemini-pro')
    """

    kind: ProviderConfigKind
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
        kind = ProviderConfigKind(d.pop("kind"))

        resource = d.pop("resource")

        model = d.pop("model")

        provider_config = cls(
            kind=kind,
            resource=resource,
            model=model,
        )

        provider_config.additional_properties = d
        return provider_config

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
