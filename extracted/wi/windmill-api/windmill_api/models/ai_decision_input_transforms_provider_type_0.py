from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_decision_input_transforms_provider_type_0_type import AiDecisionInputTransformsProviderType0Type

if TYPE_CHECKING:
    from ..models.ai_decision_input_transforms_provider_type_0_value import AiDecisionInputTransformsProviderType0Value


T = TypeVar("T", bound="AiDecisionInputTransformsProviderType0")


@_attrs_define
class AiDecisionInputTransformsProviderType0:
    """Static provider configuration passed directly to the AI agent

    Attributes:
        value (AiDecisionInputTransformsProviderType0Value): Complete AI provider configuration with resource reference
            and model selection
        type (AiDecisionInputTransformsProviderType0Type):
    """

    value: "AiDecisionInputTransformsProviderType0Value"
    type: AiDecisionInputTransformsProviderType0Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value.to_dict()

        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_decision_input_transforms_provider_type_0_value import (
            AiDecisionInputTransformsProviderType0Value,
        )

        d = src_dict.copy()
        value = AiDecisionInputTransformsProviderType0Value.from_dict(d.pop("value"))

        type = AiDecisionInputTransformsProviderType0Type(d.pop("type"))

        ai_decision_input_transforms_provider_type_0 = cls(
            value=value,
            type=type,
        )

        ai_decision_input_transforms_provider_type_0.additional_properties = d
        return ai_decision_input_transforms_provider_type_0

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
