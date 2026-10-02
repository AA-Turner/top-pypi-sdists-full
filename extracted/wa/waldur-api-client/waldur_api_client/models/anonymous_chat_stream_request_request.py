from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AnonymousChatStreamRequestRequest")


@_attrs_define
class AnonymousChatStreamRequestRequest:
    """
    Attributes:
        input_ (str): User input text for the anonymous marketplace assistant.
        session_id (str): Client-generated session identifier. Bound to the originating IP on first use; subsequent
            requests from a different IP get 403.
    """

    input_: str
    session_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        session_id = self.session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
                "session_id": session_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_ = d.pop("input")

        session_id = d.pop("session_id")

        anonymous_chat_stream_request_request = cls(
            input_=input_,
            session_id=session_id,
        )

        anonymous_chat_stream_request_request.additional_properties = d
        return anonymous_chat_stream_request_request

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
