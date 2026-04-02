import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.system_log_source_enum import SystemLogSourceEnum

T = TypeVar("T", bound="SystemLog")


@_attrs_define
class SystemLog:
    """
    Attributes:
        id (int):
        created (datetime.datetime):
        source (SystemLogSourceEnum):
        instance (str): Pod name (K8s) or container name (Docker)
        level (str):
        level_number (int):
        logger_name (str):
        message (str):
        context (Any):
    """

    id: int
    created: datetime.datetime
    source: SystemLogSourceEnum
    instance: str
    level: str
    level_number: int
    logger_name: str
    message: str
    context: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created = self.created.isoformat()

        source = self.source.value

        instance = self.instance

        level = self.level

        level_number = self.level_number

        logger_name = self.logger_name

        message = self.message

        context = self.context

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created": created,
                "source": source,
                "instance": instance,
                "level": level,
                "level_number": level_number,
                "logger_name": logger_name,
                "message": message,
                "context": context,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        created = isoparse(d.pop("created"))

        source = SystemLogSourceEnum(d.pop("source"))

        instance = d.pop("instance")

        level = d.pop("level")

        level_number = d.pop("level_number")

        logger_name = d.pop("logger_name")

        message = d.pop("message")

        context = d.pop("context")

        system_log = cls(
            id=id,
            created=created,
            source=source,
            instance=instance,
            level=level,
            level_number=level_number,
            logger_name=logger_name,
            message=message,
            context=context,
        )

        system_log.additional_properties = d
        return system_log

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
