from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqMessageStats")


@_attrs_define
class RmqMessageStats:
    """
    Attributes:
        publish (int): Total messages published
        publish_rate (float): Messages published per second
        deliver (int): Total messages delivered to consumers
        deliver_rate (float): Messages delivered per second
        confirm (int): Total messages confirmed by broker
        confirm_rate (float): Messages confirmed per second
        ack (int): Total messages acknowledged by consumers
        ack_rate (float): Messages acknowledged per second
    """

    publish: int
    publish_rate: float
    deliver: int
    deliver_rate: float
    confirm: int
    confirm_rate: float
    ack: int
    ack_rate: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        publish = self.publish

        publish_rate = self.publish_rate

        deliver = self.deliver

        deliver_rate = self.deliver_rate

        confirm = self.confirm

        confirm_rate = self.confirm_rate

        ack = self.ack

        ack_rate = self.ack_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "publish": publish,
                "publish_rate": publish_rate,
                "deliver": deliver,
                "deliver_rate": deliver_rate,
                "confirm": confirm,
                "confirm_rate": confirm_rate,
                "ack": ack,
                "ack_rate": ack_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        publish = d.pop("publish")

        publish_rate = d.pop("publish_rate")

        deliver = d.pop("deliver")

        deliver_rate = d.pop("deliver_rate")

        confirm = d.pop("confirm")

        confirm_rate = d.pop("confirm_rate")

        ack = d.pop("ack")

        ack_rate = d.pop("ack_rate")

        rmq_message_stats = cls(
            publish=publish,
            publish_rate=publish_rate,
            deliver=deliver,
            deliver_rate=deliver_rate,
            confirm=confirm,
            confirm_rate=confirm_rate,
            ack=ack,
            ack_rate=ack_rate,
        )

        rmq_message_stats.additional_properties = d
        return rmq_message_stats

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
