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
    from ..models.event_consumer_scope_output import EventConsumerScopeOutput


T = TypeVar("T", bound="EventConsumer")


@_attrs_define
class EventConsumer:
    """
    Attributes:
        uuid (UUID):
        object_types (list[str]):
        scopes (list['EventConsumerScopeOutput']):
        is_global (bool):
        rmq_username (str): RabbitMQ username (UUID hex) for the consumer queue.
        queue_created (bool):
        user_uuid (UUID):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_full_name (str):
        user_is_staff (bool): Designates whether the user can log into this admin site.
        auth_kind (Union[AuthKindEnum, BlankEnum]):
        auth_token_prefix (str): Prefix of the Personal Access Token used, when auth_kind is pat.
        auth_token_name (str): Name of the Personal Access Token used, when auth_kind is pat.
        authorized_via (Union[AuthorizedViaEnum, BlankEnum]):
        delivery_blocked_reason (Union[None, str]):
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    uuid: UUID
    object_types: list[str]
    scopes: list["EventConsumerScopeOutput"]
    is_global: bool
    rmq_username: str
    queue_created: bool
    user_uuid: UUID
    user_username: str
    user_full_name: str
    user_is_staff: bool
    auth_kind: Union[AuthKindEnum, BlankEnum]
    auth_token_prefix: str
    auth_token_name: str
    authorized_via: Union[AuthorizedViaEnum, BlankEnum]
    delivery_blocked_reason: Union[None, str]
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        object_types = self.object_types

        scopes = []
        for scopes_item_data in self.scopes:
            scopes_item = scopes_item_data.to_dict()
            scopes.append(scopes_item)

        is_global = self.is_global

        rmq_username = self.rmq_username

        queue_created = self.queue_created

        user_uuid = str(self.user_uuid)

        user_username = self.user_username

        user_full_name = self.user_full_name

        user_is_staff = self.user_is_staff

        auth_kind: str
        if isinstance(self.auth_kind, AuthKindEnum):
            auth_kind = self.auth_kind.value
        else:
            auth_kind = self.auth_kind.value

        auth_token_prefix = self.auth_token_prefix

        auth_token_name = self.auth_token_name

        authorized_via: str
        if isinstance(self.authorized_via, AuthorizedViaEnum):
            authorized_via = self.authorized_via.value
        else:
            authorized_via = self.authorized_via.value

        delivery_blocked_reason: Union[None, str]
        delivery_blocked_reason = self.delivery_blocked_reason

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "object_types": object_types,
                "scopes": scopes,
                "is_global": is_global,
                "rmq_username": rmq_username,
                "queue_created": queue_created,
                "user_uuid": user_uuid,
                "user_username": user_username,
                "user_full_name": user_full_name,
                "user_is_staff": user_is_staff,
                "auth_kind": auth_kind,
                "auth_token_prefix": auth_token_prefix,
                "auth_token_name": auth_token_name,
                "authorized_via": authorized_via,
                "delivery_blocked_reason": delivery_blocked_reason,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_consumer_scope_output import EventConsumerScopeOutput

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        object_types = cast(list[str], d.pop("object_types"))

        scopes = []
        _scopes = d.pop("scopes")
        for scopes_item_data in _scopes:
            scopes_item = EventConsumerScopeOutput.from_dict(scopes_item_data)

            scopes.append(scopes_item)

        is_global = d.pop("is_global")

        rmq_username = d.pop("rmq_username")

        queue_created = d.pop("queue_created")

        user_uuid = UUID(d.pop("user_uuid"))

        user_username = d.pop("user_username")

        user_full_name = d.pop("user_full_name")

        user_is_staff = d.pop("user_is_staff")

        def _parse_auth_kind(data: object) -> Union[AuthKindEnum, BlankEnum]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                auth_kind_type_0 = AuthKindEnum(data)

                return auth_kind_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            auth_kind_type_1 = BlankEnum(data)

            return auth_kind_type_1

        auth_kind = _parse_auth_kind(d.pop("auth_kind"))

        auth_token_prefix = d.pop("auth_token_prefix")

        auth_token_name = d.pop("auth_token_name")

        def _parse_authorized_via(data: object) -> Union[AuthorizedViaEnum, BlankEnum]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                authorized_via_type_0 = AuthorizedViaEnum(data)

                return authorized_via_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            authorized_via_type_1 = BlankEnum(data)

            return authorized_via_type_1

        authorized_via = _parse_authorized_via(d.pop("authorized_via"))

        def _parse_delivery_blocked_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        delivery_blocked_reason = _parse_delivery_blocked_reason(d.pop("delivery_blocked_reason"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        event_consumer = cls(
            uuid=uuid,
            object_types=object_types,
            scopes=scopes,
            is_global=is_global,
            rmq_username=rmq_username,
            queue_created=queue_created,
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            user_is_staff=user_is_staff,
            auth_kind=auth_kind,
            auth_token_prefix=auth_token_prefix,
            auth_token_name=auth_token_name,
            authorized_via=authorized_via,
            delivery_blocked_reason=delivery_blocked_reason,
            created=created,
            modified=modified,
        )

        event_consumer.additional_properties = d
        return event_consumer

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
