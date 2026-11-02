from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_copilot_info_response_200_default_model_provider import GetCopilotInfoResponse200DefaultModelProvider

T = TypeVar("T", bound="GetCopilotInfoResponse200DefaultModel")


@_attrs_define
class GetCopilotInfoResponse200DefaultModel:
    """
    Attributes:
        model (str):
        provider (GetCopilotInfoResponse200DefaultModelProvider):
    """

    model: str
    provider: GetCopilotInfoResponse200DefaultModelProvider
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

        provider = GetCopilotInfoResponse200DefaultModelProvider(d.pop("provider"))

        get_copilot_info_response_200_default_model = cls(
            model=model,
            provider=provider,
        )

        get_copilot_info_response_200_default_model.additional_properties = d
        return get_copilot_info_response_200_default_model

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
