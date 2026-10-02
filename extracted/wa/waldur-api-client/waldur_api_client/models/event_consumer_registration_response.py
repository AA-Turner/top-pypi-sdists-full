from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EventConsumerRegistrationResponse")


@_attrs_define
class EventConsumerRegistrationResponse:
    """
    Attributes:
        rmq_username (str): RabbitMQ username (UUID hex) for STOMP authentication
        queue_name (str): RabbitMQ queue name (consumer_{consumer_uuid})
        vhost (str): RabbitMQ virtual host (user UUID)
        observable_object_types (list[str]): Object types routed to this queue
    """

    rmq_username: str
    queue_name: str
    vhost: str
    observable_object_types: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rmq_username = self.rmq_username

        queue_name = self.queue_name

        vhost = self.vhost

        observable_object_types = self.observable_object_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rmq_username": rmq_username,
                "queue_name": queue_name,
                "vhost": vhost,
                "observable_object_types": observable_object_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rmq_username = d.pop("rmq_username")

        queue_name = d.pop("queue_name")

        vhost = d.pop("vhost")

        observable_object_types = cast(list[str], d.pop("observable_object_types"))

        event_consumer_registration_response = cls(
            rmq_username=rmq_username,
            queue_name=queue_name,
            vhost=vhost,
            observable_object_types=observable_object_types,
        )

        event_consumer_registration_response.additional_properties = d
        return event_consumer_registration_response

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
