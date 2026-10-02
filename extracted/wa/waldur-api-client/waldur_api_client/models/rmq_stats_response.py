from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rmq_vhost_stats import RmqVhostStats


T = TypeVar("T", bound="RmqStatsResponse")


@_attrs_define
class RmqStatsResponse:
    """
    Attributes:
        vhosts (list['RmqVhostStats']): List of vhosts with their subscription queues
        total_messages (int): Total messages across all subscription queues
        total_queues (int): Total number of subscription queues
    """

    vhosts: list["RmqVhostStats"]
    total_messages: int
    total_queues: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vhosts = []
        for vhosts_item_data in self.vhosts:
            vhosts_item = vhosts_item_data.to_dict()
            vhosts.append(vhosts_item)

        total_messages = self.total_messages

        total_queues = self.total_queues

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vhosts": vhosts,
                "total_messages": total_messages,
                "total_queues": total_queues,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rmq_vhost_stats import RmqVhostStats

        d = dict(src_dict)
        vhosts = []
        _vhosts = d.pop("vhosts")
        for vhosts_item_data in _vhosts:
            vhosts_item = RmqVhostStats.from_dict(vhosts_item_data)

            vhosts.append(vhosts_item)

        total_messages = d.pop("total_messages")

        total_queues = d.pop("total_queues")

        rmq_stats_response = cls(
            vhosts=vhosts,
            total_messages=total_messages,
            total_queues=total_queues,
        )

        rmq_stats_response.additional_properties = d
        return rmq_stats_response

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
