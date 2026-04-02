import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.agent_event_subscription_with_connection import AgentEventSubscriptionWithConnection
    from ..models.agent_queue_info import AgentQueueInfo
    from ..models.agent_service_status import AgentServiceStatus


T = TypeVar("T", bound="AgentConnectionInfo")


@_attrs_define
class AgentConnectionInfo:
    """
    Attributes:
        uuid (UUID): Agent identity UUID
        name (str): Agent name
        offering_uuid (UUID): Associated offering UUID
        offering_name (str): Associated offering name
        version (Union[None, str]): Agent version
        last_restarted (datetime.datetime): When the agent was last restarted
        services (list['AgentServiceStatus']): Services running within this agent
        event_subscriptions (list['AgentEventSubscriptionWithConnection']): Event subscriptions with connection status
        queues (list['AgentQueueInfo']): RabbitMQ queues for this agent's offering
    """

    uuid: UUID
    name: str
    offering_uuid: UUID
    offering_name: str
    version: Union[None, str]
    last_restarted: datetime.datetime
    services: list["AgentServiceStatus"]
    event_subscriptions: list["AgentEventSubscriptionWithConnection"]
    queues: list["AgentQueueInfo"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        version: Union[None, str]
        version = self.version

        last_restarted = self.last_restarted.isoformat()

        services = []
        for services_item_data in self.services:
            services_item = services_item_data.to_dict()
            services.append(services_item)

        event_subscriptions = []
        for event_subscriptions_item_data in self.event_subscriptions:
            event_subscriptions_item = event_subscriptions_item_data.to_dict()
            event_subscriptions.append(event_subscriptions_item)

        queues = []
        for queues_item_data in self.queues:
            queues_item = queues_item_data.to_dict()
            queues.append(queues_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "version": version,
                "last_restarted": last_restarted,
                "services": services,
                "event_subscriptions": event_subscriptions,
                "queues": queues,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_event_subscription_with_connection import AgentEventSubscriptionWithConnection
        from ..models.agent_queue_info import AgentQueueInfo
        from ..models.agent_service_status import AgentServiceStatus

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        def _parse_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        version = _parse_version(d.pop("version"))

        last_restarted = isoparse(d.pop("last_restarted"))

        services = []
        _services = d.pop("services")
        for services_item_data in _services:
            services_item = AgentServiceStatus.from_dict(services_item_data)

            services.append(services_item)

        event_subscriptions = []
        _event_subscriptions = d.pop("event_subscriptions")
        for event_subscriptions_item_data in _event_subscriptions:
            event_subscriptions_item = AgentEventSubscriptionWithConnection.from_dict(event_subscriptions_item_data)

            event_subscriptions.append(event_subscriptions_item)

        queues = []
        _queues = d.pop("queues")
        for queues_item_data in _queues:
            queues_item = AgentQueueInfo.from_dict(queues_item_data)

            queues.append(queues_item)

        agent_connection_info = cls(
            uuid=uuid,
            name=name,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            version=version,
            last_restarted=last_restarted,
            services=services,
            event_subscriptions=event_subscriptions,
            queues=queues,
        )

        agent_connection_info.additional_properties = d
        return agent_connection_info

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
