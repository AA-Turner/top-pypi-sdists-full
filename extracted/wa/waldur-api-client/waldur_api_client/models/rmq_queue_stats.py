from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqQueueStats")


@_attrs_define
class RmqQueueStats:
    """
    Attributes:
        name (str): Queue name (e.g., 'subscription_{uuid}_offering_{uuid}_{type}')
        messages (int): Total number of messages in the queue
        messages_ready (int): Number of messages ready for delivery
        messages_unacknowledged (int): Number of messages awaiting acknowledgement
        consumers (int): Number of active consumers for this queue
        subscription_uuid (Union[None, str]): Parsed subscription UUID from queue name
        offering_uuid (Union[None, str]): Parsed offering UUID from queue name
        object_type (Union[None, str]): Parsed object type from queue name (e.g., 'resource', 'order')
        message_ttl (Union[None, int]): Message TTL in milliseconds
        max_length (Union[None, int]): Maximum number of messages in queue
        max_length_bytes (Union[None, int]): Maximum total size of messages in bytes
        expires (Union[None, int]): Queue TTL - auto-delete after idle in milliseconds
        overflow (Union[None, str]): Behavior when full: 'drop-head', 'reject-publish', or 'reject-publish-dlx'
        dead_letter_exchange (Union[None, str]): Dead letter exchange name
        dead_letter_routing_key (Union[None, str]): Dead letter routing key
        max_priority (Union[None, int]): Maximum priority level (1-255)
        queue_mode (Union[None, str]): Queue mode: 'default' or 'lazy'
        queue_type (Union[None, str]): Queue type: 'classic', 'quorum', or 'stream'
    """

    name: str
    messages: int
    messages_ready: int
    messages_unacknowledged: int
    consumers: int
    subscription_uuid: Union[None, str]
    offering_uuid: Union[None, str]
    object_type: Union[None, str]
    message_ttl: Union[None, int]
    max_length: Union[None, int]
    max_length_bytes: Union[None, int]
    expires: Union[None, int]
    overflow: Union[None, str]
    dead_letter_exchange: Union[None, str]
    dead_letter_routing_key: Union[None, str]
    max_priority: Union[None, int]
    queue_mode: Union[None, str]
    queue_type: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        messages = self.messages

        messages_ready = self.messages_ready

        messages_unacknowledged = self.messages_unacknowledged

        consumers = self.consumers

        subscription_uuid: Union[None, str]
        subscription_uuid = self.subscription_uuid

        offering_uuid: Union[None, str]
        offering_uuid = self.offering_uuid

        object_type: Union[None, str]
        object_type = self.object_type

        message_ttl: Union[None, int]
        message_ttl = self.message_ttl

        max_length: Union[None, int]
        max_length = self.max_length

        max_length_bytes: Union[None, int]
        max_length_bytes = self.max_length_bytes

        expires: Union[None, int]
        expires = self.expires

        overflow: Union[None, str]
        overflow = self.overflow

        dead_letter_exchange: Union[None, str]
        dead_letter_exchange = self.dead_letter_exchange

        dead_letter_routing_key: Union[None, str]
        dead_letter_routing_key = self.dead_letter_routing_key

        max_priority: Union[None, int]
        max_priority = self.max_priority

        queue_mode: Union[None, str]
        queue_mode = self.queue_mode

        queue_type: Union[None, str]
        queue_type = self.queue_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "messages": messages,
                "messages_ready": messages_ready,
                "messages_unacknowledged": messages_unacknowledged,
                "consumers": consumers,
                "subscription_uuid": subscription_uuid,
                "offering_uuid": offering_uuid,
                "object_type": object_type,
                "message_ttl": message_ttl,
                "max_length": max_length,
                "max_length_bytes": max_length_bytes,
                "expires": expires,
                "overflow": overflow,
                "dead_letter_exchange": dead_letter_exchange,
                "dead_letter_routing_key": dead_letter_routing_key,
                "max_priority": max_priority,
                "queue_mode": queue_mode,
                "queue_type": queue_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        messages = d.pop("messages")

        messages_ready = d.pop("messages_ready")

        messages_unacknowledged = d.pop("messages_unacknowledged")

        consumers = d.pop("consumers")

        def _parse_subscription_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        subscription_uuid = _parse_subscription_uuid(d.pop("subscription_uuid"))

        def _parse_offering_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_uuid = _parse_offering_uuid(d.pop("offering_uuid"))

        def _parse_object_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        object_type = _parse_object_type(d.pop("object_type"))

        def _parse_message_ttl(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        message_ttl = _parse_message_ttl(d.pop("message_ttl"))

        def _parse_max_length(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_length = _parse_max_length(d.pop("max_length"))

        def _parse_max_length_bytes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_length_bytes = _parse_max_length_bytes(d.pop("max_length_bytes"))

        def _parse_expires(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        expires = _parse_expires(d.pop("expires"))

        def _parse_overflow(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        overflow = _parse_overflow(d.pop("overflow"))

        def _parse_dead_letter_exchange(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        dead_letter_exchange = _parse_dead_letter_exchange(d.pop("dead_letter_exchange"))

        def _parse_dead_letter_routing_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        dead_letter_routing_key = _parse_dead_letter_routing_key(d.pop("dead_letter_routing_key"))

        def _parse_max_priority(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_priority = _parse_max_priority(d.pop("max_priority"))

        def _parse_queue_mode(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        queue_mode = _parse_queue_mode(d.pop("queue_mode"))

        def _parse_queue_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        queue_type = _parse_queue_type(d.pop("queue_type"))

        rmq_queue_stats = cls(
            name=name,
            messages=messages,
            messages_ready=messages_ready,
            messages_unacknowledged=messages_unacknowledged,
            consumers=consumers,
            subscription_uuid=subscription_uuid,
            offering_uuid=offering_uuid,
            object_type=object_type,
            message_ttl=message_ttl,
            max_length=max_length,
            max_length_bytes=max_length_bytes,
            expires=expires,
            overflow=overflow,
            dead_letter_exchange=dead_letter_exchange,
            dead_letter_routing_key=dead_letter_routing_key,
            max_priority=max_priority,
            queue_mode=queue_mode,
            queue_type=queue_type,
        )

        rmq_queue_stats.additional_properties = d
        return rmq_queue_stats

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
