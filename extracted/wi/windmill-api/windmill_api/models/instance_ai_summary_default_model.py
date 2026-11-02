from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.instance_ai_summary_default_model_provider import InstanceAISummaryDefaultModelProvider

T = TypeVar("T", bound="InstanceAISummaryDefaultModel")


@_attrs_define
class InstanceAISummaryDefaultModel:
    """
    Attributes:
        model (str):
        provider (InstanceAISummaryDefaultModelProvider):
    """

    model: str
    provider: InstanceAISummaryDefaultModelProvider
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        model = self.model
        provider = self.provider.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "provider": provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model = d.pop("model")

        provider = InstanceAISummaryDefaultModelProvider(d.pop("provider"))

        instance_ai_summary_default_model = cls(
            model=model,
            provider=provider,
        )

        instance_ai_summary_default_model.additional_properties = d
        return instance_ai_summary_default_model

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
