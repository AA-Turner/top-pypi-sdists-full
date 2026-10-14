import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.auth_kind_enum import AuthKindEnum
from ..models.authorized_via_enum import AuthorizedViaEnum
from ..models.blank_enum import BlankEnum

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
        event_consumer_uuid (Union[None, UUID]): UUID of the unified event consumer the agent drains, null while it
            still runs on legacy subscriptions
        user_uuid (Union[None, UUID]): Consumer owner UUID
        user_username (Union[None, str]): Consumer owner username
        user_full_name (Union[None, str]): Consumer owner full name
        user_is_staff (Union[None, bool]): Whether the consumer owner is a staff user, whose delivery scope is platform-
            wide
        auth_kind (Union[AuthKindEnum, BlankEnum, None]): How the agent authenticated when it registered the queue
        auth_token_prefix (Union[None, str]): Prefix of the Personal Access Token backing the queue
        auth_token_name (Union[None, str]): Name of the Personal Access Token backing the queue
        authorized_via (Union[AuthorizedViaEnum, BlankEnum, None]): Permission branch that authorised the registration
        delivery_blocked_reason (Union[None, str]): Why no event can reach this consumer, null when delivery works
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
    event_consumer_uuid: Union[None, UUID]
    user_uuid: Union[None, UUID]
    user_username: Union[None, str]
    user_full_name: Union[None, str]
    user_is_staff: Union[None, bool]
    auth_kind: Union[AuthKindEnum, BlankEnum, None]
    auth_token_prefix: Union[None, str]
    auth_token_name: Union[None, str]
    authorized_via: Union[AuthorizedViaEnum, BlankEnum, None]
    delivery_blocked_reason: Union[None, str]
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

        event_consumer_uuid: Union[None, str]
        if isinstance(self.event_consumer_uuid, UUID):
            event_consumer_uuid = str(self.event_consumer_uuid)
        else:
            event_consumer_uuid = self.event_consumer_uuid

        user_uuid: Union[None, str]
        if isinstance(self.user_uuid, UUID):
            user_uuid = str(self.user_uuid)
        else:
            user_uuid = self.user_uuid

        user_username: Union[None, str]
        user_username = self.user_username

        user_full_name: Union[None, str]
        user_full_name = self.user_full_name

        user_is_staff: Union[None, bool]
        user_is_staff = self.user_is_staff

        auth_kind: Union[None, str]
        if isinstance(self.auth_kind, AuthKindEnum):
            auth_kind = self.auth_kind.value
        elif isinstance(self.auth_kind, BlankEnum):
            auth_kind = self.auth_kind.value
        else:
            auth_kind = self.auth_kind

        auth_token_prefix: Union[None, str]
        auth_token_prefix = self.auth_token_prefix

        auth_token_name: Union[None, str]
        auth_token_name = self.auth_token_name

        authorized_via: Union[None, str]
        if isinstance(self.authorized_via, AuthorizedViaEnum):
            authorized_via = self.authorized_via.value
        elif isinstance(self.authorized_via, BlankEnum):
            authorized_via = self.authorized_via.value
        else:
            authorized_via = self.authorized_via

        delivery_blocked_reason: Union[None, str]
        delivery_blocked_reason = self.delivery_blocked_reason

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
                "event_consumer_uuid": event_consumer_uuid,
                "user_uuid": user_uuid,
                "user_username": user_username,
                "user_full_name": user_full_name,
                "user_is_staff": user_is_staff,
                "auth_kind": auth_kind,
                "auth_token_prefix": auth_token_prefix,
                "auth_token_name": auth_token_name,
                "authorized_via": authorized_via,
                "delivery_blocked_reason": delivery_blocked_reason,
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

        def _parse_event_consumer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                event_consumer_uuid_type_0 = UUID(data)

                return event_consumer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        event_consumer_uuid = _parse_event_consumer_uuid(d.pop("event_consumer_uuid"))

        def _parse_user_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_uuid_type_0 = UUID(data)

                return user_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        user_uuid = _parse_user_uuid(d.pop("user_uuid"))

        def _parse_user_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        user_username = _parse_user_username(d.pop("user_username"))

        def _parse_user_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        user_full_name = _parse_user_full_name(d.pop("user_full_name"))

        def _parse_user_is_staff(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        user_is_staff = _parse_user_is_staff(d.pop("user_is_staff"))

        def _parse_auth_kind(data: object) -> Union[AuthKindEnum, BlankEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                auth_kind_type_0 = AuthKindEnum(data)

                return auth_kind_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                auth_kind_type_1 = BlankEnum(data)

                return auth_kind_type_1
            except:  # noqa: E722
                pass
            return cast(Union[AuthKindEnum, BlankEnum, None], data)

        auth_kind = _parse_auth_kind(d.pop("auth_kind"))

        def _parse_auth_token_prefix(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        auth_token_prefix = _parse_auth_token_prefix(d.pop("auth_token_prefix"))

        def _parse_auth_token_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        auth_token_name = _parse_auth_token_name(d.pop("auth_token_name"))

        def _parse_authorized_via(data: object) -> Union[AuthorizedViaEnum, BlankEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                authorized_via_type_0 = AuthorizedViaEnum(data)

                return authorized_via_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                authorized_via_type_1 = BlankEnum(data)

                return authorized_via_type_1
            except:  # noqa: E722
                pass
            return cast(Union[AuthorizedViaEnum, BlankEnum, None], data)

        authorized_via = _parse_authorized_via(d.pop("authorized_via"))

        def _parse_delivery_blocked_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        delivery_blocked_reason = _parse_delivery_blocked_reason(d.pop("delivery_blocked_reason"))

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
            event_consumer_uuid=event_consumer_uuid,
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            user_is_staff=user_is_staff,
            auth_kind=auth_kind,
            auth_token_prefix=auth_token_prefix,
            auth_token_name=auth_token_name,
            authorized_via=authorized_via,
            delivery_blocked_reason=delivery_blocked_reason,
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
