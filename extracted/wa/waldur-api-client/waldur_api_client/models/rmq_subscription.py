import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RmqSubscription")


@_attrs_define
class RmqSubscription:
    """
    Attributes:
        created (datetime.datetime):
        uuid (UUID):
        source_ip (str): An IPv4 or IPv6 address.
    """

    created: datetime.datetime
    uuid: UUID
    source_ip: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created.isoformat()

        uuid = str(self.uuid)

        source_ip: str
        source_ip = self.source_ip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "uuid": uuid,
                "source_ip": source_ip,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = isoparse(d.pop("created"))

        uuid = UUID(d.pop("uuid"))

        def _parse_source_ip(data: object) -> str:
            return cast(str, data)

        source_ip = _parse_source_ip(d.pop("source_ip"))

        rmq_subscription = cls(
            created=created,
            uuid=uuid,
            source_ip=source_ip,
        )

        rmq_subscription.additional_properties = d
        return rmq_subscription

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
