from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunAgentJsonBody")


@_attrs_define
class RunAgentJsonBody:
    """
    Attributes:
        user_message (Union[Unset, str]):
        user_attachments (Union[Unset, List[Any]]):
        previous_messages (Union[Unset, List[Any]]): The history to answer from, as chat messages, when the agent's
            memory is off.
            An agent with managed memory reads its conversation instead and ignores this.
    """

    user_message: Union[Unset, str] = UNSET
    user_attachments: Union[Unset, List[Any]] = UNSET
    previous_messages: Union[Unset, List[Any]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_message = self.user_message
        user_attachments: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.user_attachments, Unset):
            user_attachments = self.user_attachments

        previous_messages: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.previous_messages, Unset):
            previous_messages = self.previous_messages

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_message is not UNSET:
            field_dict["user_message"] = user_message
        if user_attachments is not UNSET:
            field_dict["user_attachments"] = user_attachments
        if previous_messages is not UNSET:
            field_dict["previous_messages"] = previous_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_message = d.pop("user_message", UNSET)

        user_attachments = cast(List[Any], d.pop("user_attachments", UNSET))

        previous_messages = cast(List[Any], d.pop("previous_messages", UNSET))

        run_agent_json_body = cls(
            user_message=user_message,
            user_attachments=user_attachments,
            previous_messages=previous_messages,
        )

        run_agent_json_body.additional_properties = d
        return run_agent_json_body

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
