from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.logger_resource import LoggerResource


T = TypeVar("T", bound="LoggerResponse")


@_attrs_define
class LoggerResponse:
    """JSON:API single-resource response envelope for a logger.

    Attributes:
        data (LoggerResource): JSON:API resource envelope for a logger.

            `id` is the logger's dot-separated key (e.g. `sqlalchemy.engine`).
            On a `PUT /api/v1/loggers/{id}` create, the id is taken from the URL
            path; on update, an `id` in the body renames the logger. Example: {'attributes': {'created_at':
            '2026-04-01T10:00:00Z', 'environments': {'production': {'level': 'WARN'}, 'staging': {'level': 'DEBUG'}},
            'group': 'database-loggers', 'level': 'DEBUG', 'managed': True, 'name': 'SQL Logger', 'updated_at':
            '2026-04-01T10:00:00Z'}, 'id': 'com.example.sql', 'type': 'logger'}.
    """

    data: LoggerResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.logger_resource import LoggerResource

        d = dict(src_dict)
        data = LoggerResource.from_dict(d.pop("data"))

        logger_response = cls(
            data=data,
        )

        logger_response.additional_properties = d
        return logger_response

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
