from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rmq_listener import RmqListener
    from ..models.rmq_message_stats import RmqMessageStats
    from ..models.rmq_object_totals import RmqObjectTotals
    from ..models.rmq_queue_totals import RmqQueueTotals


T = TypeVar("T", bound="RmqOverview")


@_attrs_define
class RmqOverview:
    """
    Attributes:
        cluster_name (str): Name of the RabbitMQ cluster
        rabbitmq_version (str): RabbitMQ server version
        erlang_version (str): Erlang/OTP runtime version
        message_stats (RmqMessageStats):
        queue_totals (RmqQueueTotals):
        object_totals (RmqObjectTotals):
        node (str): Current RabbitMQ node name
        listeners (list['RmqListener']): Active protocol listeners
    """

    cluster_name: str
    rabbitmq_version: str
    erlang_version: str
    message_stats: "RmqMessageStats"
    queue_totals: "RmqQueueTotals"
    object_totals: "RmqObjectTotals"
    node: str
    listeners: list["RmqListener"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster_name = self.cluster_name

        rabbitmq_version = self.rabbitmq_version

        erlang_version = self.erlang_version

        message_stats = self.message_stats.to_dict()

        queue_totals = self.queue_totals.to_dict()

        object_totals = self.object_totals.to_dict()

        node = self.node

        listeners = []
        for listeners_item_data in self.listeners:
            listeners_item = listeners_item_data.to_dict()
            listeners.append(listeners_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster_name": cluster_name,
                "rabbitmq_version": rabbitmq_version,
                "erlang_version": erlang_version,
                "message_stats": message_stats,
                "queue_totals": queue_totals,
                "object_totals": object_totals,
                "node": node,
                "listeners": listeners,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rmq_listener import RmqListener
        from ..models.rmq_message_stats import RmqMessageStats
        from ..models.rmq_object_totals import RmqObjectTotals
        from ..models.rmq_queue_totals import RmqQueueTotals

        d = dict(src_dict)
        cluster_name = d.pop("cluster_name")

        rabbitmq_version = d.pop("rabbitmq_version")

        erlang_version = d.pop("erlang_version")

        message_stats = RmqMessageStats.from_dict(d.pop("message_stats"))

        queue_totals = RmqQueueTotals.from_dict(d.pop("queue_totals"))

        object_totals = RmqObjectTotals.from_dict(d.pop("object_totals"))

        node = d.pop("node")

        listeners = []
        _listeners = d.pop("listeners")
        for listeners_item_data in _listeners:
            listeners_item = RmqListener.from_dict(listeners_item_data)

            listeners.append(listeners_item)

        rmq_overview = cls(
            cluster_name=cluster_name,
            rabbitmq_version=rabbitmq_version,
            erlang_version=erlang_version,
            message_stats=message_stats,
            queue_totals=queue_totals,
            object_totals=object_totals,
            node=node,
            listeners=listeners,
        )

        rmq_overview.additional_properties = d
        return rmq_overview

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
