from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqQueueTotals")


@_attrs_define
class RmqQueueTotals:
    """
    Attributes:
        messages (int): Total messages across all queues
        messages_ready (int): Messages ready for delivery
        messages_unacknowledged (int): Messages awaiting acknowledgement
    """

    messages: int
    messages_ready: int
    messages_unacknowledged: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        messages = self.messages

        messages_ready = self.messages_ready

        messages_unacknowledged = self.messages_unacknowledged

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messages": messages,
                "messages_ready": messages_ready,
                "messages_unacknowledged": messages_unacknowledged,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        messages = d.pop("messages")

        messages_ready = d.pop("messages_ready")

        messages_unacknowledged = d.pop("messages_unacknowledged")

        rmq_queue_totals = cls(
            messages=messages,
            messages_ready=messages_ready,
            messages_unacknowledged=messages_unacknowledged,
        )

        rmq_queue_totals.additional_properties = d
        return rmq_queue_totals

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
