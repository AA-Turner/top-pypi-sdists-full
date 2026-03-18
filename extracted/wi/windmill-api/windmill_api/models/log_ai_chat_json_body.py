from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LogAiChatJsonBody")


@_attrs_define
class LogAiChatJsonBody:
    """
    Attributes:
        session_id (str):
        provider (str):
        model (str):
        mode (str):
    """

    session_id: str
    provider: str
    model: str
    mode: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        session_id = self.session_id
        provider = self.provider
        model = self.model
        mode = self.mode

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "provider": provider,
                "model": model,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        session_id = d.pop("session_id")

        provider = d.pop("provider")

        model = d.pop("model")

        mode = d.pop("mode")

        log_ai_chat_json_body = cls(
            session_id=session_id,
            provider=provider,
            model=model,
            mode=mode,
        )

        log_ai_chat_json_body.additional_properties = d
        return log_ai_chat_json_body

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
