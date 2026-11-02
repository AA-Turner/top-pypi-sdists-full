from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditWebsocketTriggerHeartbeat")


@_attrs_define
class EditWebsocketTriggerHeartbeat:
    """Optional periodic heartbeat message configuration

    Attributes:
        interval_secs (int): Interval in seconds between heartbeat messages
        message (str): Message to send as heartbeat. Use {{state}} as a placeholder for a value extracted from incoming
            messages (see state_field).
        state_field (Union[Unset, str]): Optional. Top-level JSON field to extract from incoming messages. The extracted
            value replaces {{state}} in the heartbeat message.
    """

    interval_secs: int
    message: str
    state_field: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        interval_secs = self.interval_secs
        message = self.message
        state_field = self.state_field

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interval_secs": interval_secs,
                "message": message,
            }
        )
        if state_field is not UNSET:
            field_dict["state_field"] = state_field

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        interval_secs = d.pop("interval_secs")

        message = d.pop("message")

        state_field = d.pop("state_field", UNSET)

        edit_websocket_trigger_heartbeat = cls(
            interval_secs=interval_secs,
            message=message,
            state_field=state_field,
        )

        edit_websocket_trigger_heartbeat.additional_properties = d
        return edit_websocket_trigger_heartbeat

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
