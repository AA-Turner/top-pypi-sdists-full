import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.level_enum import LevelEnum

T = TypeVar("T", bound="SiteAgentLog")


@_attrs_define
class SiteAgentLog:
    """
    Attributes:
        uuid (UUID):
        offering (str):
        offering_uuid (UUID):
        agent_identity_uuid (UUID):
        timestamp (float): Unix timestamp of the log entry
        level (LevelEnum):
        message (str):
        module (str):
        created (datetime.datetime):
    """

    uuid: UUID
    offering: str
    offering_uuid: UUID
    agent_identity_uuid: UUID
    timestamp: float
    level: LevelEnum
    message: str
    module: str
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        offering = self.offering

        offering_uuid = str(self.offering_uuid)

        agent_identity_uuid = str(self.agent_identity_uuid)

        timestamp = self.timestamp

        level = self.level.value

        message = self.message

        module = self.module

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "offering": offering,
                "offering_uuid": offering_uuid,
                "agent_identity_uuid": agent_identity_uuid,
                "timestamp": timestamp,
                "level": level,
                "message": message,
                "module": module,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        offering = d.pop("offering")

        offering_uuid = UUID(d.pop("offering_uuid"))

        agent_identity_uuid = UUID(d.pop("agent_identity_uuid"))

        timestamp = d.pop("timestamp")

        level = LevelEnum(d.pop("level"))

        message = d.pop("message")

        module = d.pop("module")

        created = isoparse(d.pop("created"))

        site_agent_log = cls(
            uuid=uuid,
            offering=offering,
            offering_uuid=offering_uuid,
            agent_identity_uuid=agent_identity_uuid,
            timestamp=timestamp,
            level=level,
            message=message,
            module=module,
            created=created,
        )

        site_agent_log.additional_properties = d
        return site_agent_log

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
