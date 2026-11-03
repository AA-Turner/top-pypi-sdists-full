from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_ai_session_tool_response_200_effects_item import CallAiSessionToolResponse200EffectsItem


T = TypeVar("T", bound="CallAiSessionToolResponse200")


@_attrs_define
class CallAiSessionToolResponse200:
    """
    Attributes:
        text (str):
        is_error (bool):
        effects (List['CallAiSessionToolResponse200EffectsItem']):
    """

    text: str
    is_error: bool
    effects: List["CallAiSessionToolResponse200EffectsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        is_error = self.is_error
        effects = []
        for effects_item_data in self.effects:
            effects_item = effects_item_data.to_dict()

            effects.append(effects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "is_error": is_error,
                "effects": effects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.call_ai_session_tool_response_200_effects_item import CallAiSessionToolResponse200EffectsItem

        d = src_dict.copy()
        text = d.pop("text")

        is_error = d.pop("is_error")

        effects = []
        _effects = d.pop("effects")
        for effects_item_data in _effects:
            effects_item = CallAiSessionToolResponse200EffectsItem.from_dict(effects_item_data)

            effects.append(effects_item)

        call_ai_session_tool_response_200 = cls(
            text=text,
            is_error=is_error,
            effects=effects,
        )

        call_ai_session_tool_response_200.additional_properties = d
        return call_ai_session_tool_response_200

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
