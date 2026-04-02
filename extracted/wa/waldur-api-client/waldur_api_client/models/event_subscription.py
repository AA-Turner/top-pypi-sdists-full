import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventSubscription")


@_attrs_define
class EventSubscription:
    """
    Attributes:
        uuid (UUID):
        url (str):
        user (str):
        user_uuid (UUID):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_full_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        source_ip (Union[None, str]): An IPv4 or IPv6 address.
        description (Union[Unset, str]):
        observable_objects (Union[Unset, Any]): List of objects to observe. Each item must have 'object_type' (one of:
            order, user_role, resource, offering_user, importable_resources, service_account, course_account,
            resource_periodic_limits) and optionally 'object_id' (integer). Example: [{"object_type": "resource"},
            {"object_type": "order", "object_id": 123}]
    """

    uuid: UUID
    url: str
    user: str
    user_uuid: UUID
    user_username: str
    user_full_name: str
    created: datetime.datetime
    modified: datetime.datetime
    source_ip: Union[None, str]
    description: Union[Unset, str] = UNSET
    observable_objects: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        user = self.user

        user_uuid = str(self.user_uuid)

        user_username = self.user_username

        user_full_name = self.user_full_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        source_ip: Union[None, str]
        source_ip = self.source_ip

        description = self.description

        observable_objects = self.observable_objects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "user": user,
                "user_uuid": user_uuid,
                "user_username": user_username,
                "user_full_name": user_full_name,
                "created": created,
                "modified": modified,
                "source_ip": source_ip,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if observable_objects is not UNSET:
            field_dict["observable_objects"] = observable_objects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        user = d.pop("user")

        user_uuid = UUID(d.pop("user_uuid"))

        user_username = d.pop("user_username")

        user_full_name = d.pop("user_full_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_source_ip(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_ip = _parse_source_ip(d.pop("source_ip"))

        description = d.pop("description", UNSET)

        observable_objects = d.pop("observable_objects", UNSET)

        event_subscription = cls(
            uuid=uuid,
            url=url,
            user=user,
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            created=created,
            modified=modified,
            source_ip=source_ip,
            description=description,
            observable_objects=observable_objects,
        )

        event_subscription.additional_properties = d
        return event_subscription

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
