from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dlq_queue import DLQQueue


T = TypeVar("T", bound="DeadLetterQueue")


@_attrs_define
class DeadLetterQueue:
    """
    Attributes:
        total_dlq_messages (int): Total messages across all DLQs
        dlq_count (int): Number of DLQ queues found
        dlq_queues (list['DLQQueue']): List of DLQ queues with their statistics
        note (str): Informational note about DLQs
    """

    total_dlq_messages: int
    dlq_count: int
    dlq_queues: list["DLQQueue"]
    note: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_dlq_messages = self.total_dlq_messages

        dlq_count = self.dlq_count

        dlq_queues = []
        for dlq_queues_item_data in self.dlq_queues:
            dlq_queues_item = dlq_queues_item_data.to_dict()
            dlq_queues.append(dlq_queues_item)

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_dlq_messages": total_dlq_messages,
                "dlq_count": dlq_count,
                "dlq_queues": dlq_queues,
                "note": note,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dlq_queue import DLQQueue

        d = dict(src_dict)
        total_dlq_messages = d.pop("total_dlq_messages")

        dlq_count = d.pop("dlq_count")

        dlq_queues = []
        _dlq_queues = d.pop("dlq_queues")
        for dlq_queues_item_data in _dlq_queues:
            dlq_queues_item = DLQQueue.from_dict(dlq_queues_item_data)

            dlq_queues.append(dlq_queues_item)

        note = d.pop("note")

        dead_letter_queue = cls(
            total_dlq_messages=total_dlq_messages,
            dlq_count=dlq_count,
            dlq_queues=dlq_queues,
            note=note,
        )

        dead_letter_queue.additional_properties = d
        return dead_letter_queue

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
