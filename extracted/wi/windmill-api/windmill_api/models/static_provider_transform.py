from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.static_provider_transform_type import StaticProviderTransformType

if TYPE_CHECKING:
    from ..models.static_provider_transform_value import StaticProviderTransformValue


T = TypeVar("T", bound="StaticProviderTransform")


@_attrs_define
class StaticProviderTransform:
    """Static provider configuration passed directly to the AI agent

    Attributes:
        value (StaticProviderTransformValue): Complete AI provider configuration with resource reference and model
            selection
        type (StaticProviderTransformType):
    """

    value: "StaticProviderTransformValue"
    type: StaticProviderTransformType
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
        from ..models.static_provider_transform_value import StaticProviderTransformValue

        d = src_dict.copy()
        value = StaticProviderTransformValue.from_dict(d.pop("value"))

        type = StaticProviderTransformType(d.pop("type"))

        static_provider_transform = cls(
            value=value,
            type=type,
        )

        static_provider_transform.additional_properties = d
        return static_provider_transform

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
