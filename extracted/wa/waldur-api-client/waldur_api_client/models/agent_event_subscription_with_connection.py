import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.agent_rmq_connection import AgentRmqConnection


T = TypeVar("T", bound="AgentEventSubscriptionWithConnection")


@_attrs_define
class AgentEventSubscriptionWithConnection:
    """
    Attributes:
        uuid (UUID): Event subscription UUID
        created (datetime.datetime): When the subscription was created
        observable_objects (Any): List of observable object configurations
        rmq_connection (Union['AgentRmqConnection', None]): RabbitMQ connection status for this subscription
    """

    uuid: UUID
    created: datetime.datetime
    observable_objects: Any
    rmq_connection: Union["AgentRmqConnection", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_rmq_connection import AgentRmqConnection

        uuid = str(self.uuid)

        created = self.created.isoformat()

        observable_objects = self.observable_objects

        rmq_connection: Union[None, dict[str, Any]]
        if isinstance(self.rmq_connection, AgentRmqConnection):
            rmq_connection = self.rmq_connection.to_dict()
        else:
            rmq_connection = self.rmq_connection

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "observable_objects": observable_objects,
                "rmq_connection": rmq_connection,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_rmq_connection import AgentRmqConnection

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        observable_objects = d.pop("observable_objects")

        def _parse_rmq_connection(data: object) -> Union["AgentRmqConnection", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rmq_connection_type_1 = AgentRmqConnection.from_dict(data)

                return rmq_connection_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AgentRmqConnection", None], data)

        rmq_connection = _parse_rmq_connection(d.pop("rmq_connection"))

        agent_event_subscription_with_connection = cls(
            uuid=uuid,
            created=created,
            observable_objects=observable_objects,
            rmq_connection=rmq_connection,
        )

        agent_event_subscription_with_connection.additional_properties = d
        return agent_event_subscription_with_connection

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
