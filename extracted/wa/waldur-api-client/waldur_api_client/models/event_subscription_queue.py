import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="EventSubscriptionQueue")


@_attrs_define
class EventSubscriptionQueue:
    """
    Attributes:
        uuid (UUID):
        url (str):
        event_subscription (str):
        event_subscription_uuid (str):
        offering_uuid (str):
        object_type (str): Observable object type (e.g., 'resource', 'order')
        queue_name (str):
        vhost (str):
        created (datetime.datetime):
    """

    uuid: UUID
    url: str
    event_subscription: str
    event_subscription_uuid: str
    offering_uuid: str
    object_type: str
    queue_name: str
    vhost: str
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        event_subscription = self.event_subscription

        event_subscription_uuid = self.event_subscription_uuid

        offering_uuid = self.offering_uuid

        object_type = self.object_type

        queue_name = self.queue_name

        vhost = self.vhost

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "event_subscription": event_subscription,
                "event_subscription_uuid": event_subscription_uuid,
                "offering_uuid": offering_uuid,
                "object_type": object_type,
                "queue_name": queue_name,
                "vhost": vhost,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        event_subscription = d.pop("event_subscription")

        event_subscription_uuid = d.pop("event_subscription_uuid")

        offering_uuid = d.pop("offering_uuid")

        object_type = d.pop("object_type")

        queue_name = d.pop("queue_name")

        vhost = d.pop("vhost")

        created = isoparse(d.pop("created"))

        event_subscription_queue = cls(
            uuid=uuid,
            url=url,
            event_subscription=event_subscription,
            event_subscription_uuid=event_subscription_uuid,
            offering_uuid=offering_uuid,
            object_type=object_type,
            queue_name=queue_name,
            vhost=vhost,
            created=created,
        )

        event_subscription_queue.additional_properties = d
        return event_subscription_queue

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
