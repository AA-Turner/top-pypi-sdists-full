from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.logger_bulk_item import LoggerBulkItem


T = TypeVar("T", bound="LoggerBulkRequest")


@_attrs_define
class LoggerBulkRequest:
    """Payload for bulk registration of loggers discovered by an SDK.

    Example:
        {'loggers': [{'environment': 'production', 'id': 'sqlalchemy.engine', 'level': 'WARN', 'service': 'api-
            gateway'}, {'environment': 'production', 'id': 'stripe', 'level': 'INFO', 'service': 'api-gateway'}]}

    Attributes:
        loggers (list[LoggerBulkItem]): Loggers to register or refresh observations for.
    """

    loggers: list[LoggerBulkItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        loggers = []
        for loggers_item_data in self.loggers:
            loggers_item = loggers_item_data.to_dict()
            loggers.append(loggers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "loggers": loggers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.logger_bulk_item import LoggerBulkItem

        d = dict(src_dict)
        loggers = []
        _loggers = d.pop("loggers")
        for loggers_item_data in _loggers:
            loggers_item = LoggerBulkItem.from_dict(loggers_item_data)

            loggers.append(loggers_item)

        logger_bulk_request = cls(
            loggers=loggers,
        )

        logger_bulk_request.additional_properties = d
        return logger_bulk_request

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
