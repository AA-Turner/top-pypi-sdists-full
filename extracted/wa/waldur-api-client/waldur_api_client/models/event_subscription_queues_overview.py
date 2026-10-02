from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.top_queue import TopQueue


T = TypeVar("T", bound="EventSubscriptionQueuesOverview")


@_attrs_define
class EventSubscriptionQueuesOverview:
    """
    Attributes:
        total_vhosts (int): Total number of vhosts with subscription queues
        total_queues (int): Total number of subscription queues
        total_messages (int): Total messages across all subscription queues
        top_queues_by_messages (list['TopQueue']): Top 10 queues by message count
    """

    total_vhosts: int
    total_queues: int
    total_messages: int
    top_queues_by_messages: list["TopQueue"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_vhosts = self.total_vhosts

        total_queues = self.total_queues

        total_messages = self.total_messages

        top_queues_by_messages = []
        for top_queues_by_messages_item_data in self.top_queues_by_messages:
            top_queues_by_messages_item = top_queues_by_messages_item_data.to_dict()
            top_queues_by_messages.append(top_queues_by_messages_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_vhosts": total_vhosts,
                "total_queues": total_queues,
                "total_messages": total_messages,
                "top_queues_by_messages": top_queues_by_messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.top_queue import TopQueue

        d = dict(src_dict)
        total_vhosts = d.pop("total_vhosts")

        total_queues = d.pop("total_queues")

        total_messages = d.pop("total_messages")

        top_queues_by_messages = []
        _top_queues_by_messages = d.pop("top_queues_by_messages")
        for top_queues_by_messages_item_data in _top_queues_by_messages:
            top_queues_by_messages_item = TopQueue.from_dict(top_queues_by_messages_item_data)

            top_queues_by_messages.append(top_queues_by_messages_item)

        event_subscription_queues_overview = cls(
            total_vhosts=total_vhosts,
            total_queues=total_queues,
            total_messages=total_messages,
            top_queues_by_messages=top_queues_by_messages,
        )

        event_subscription_queues_overview.additional_properties = d
        return event_subscription_queues_overview

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
