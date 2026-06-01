from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="LoggerBulkItem")


@_attrs_define
class LoggerBulkItem:
    """One logger discovered by an SDK during a bulk registration call.

    Example:
        {'environment': 'production', 'id': 'sqlalchemy.engine', 'level': 'WARN', 'resolved_level': 'WARN', 'service':
            'api-gateway'}

    Attributes:
        id (str): Dot-separated logger key as the SDK saw it.
        level (None | str | Unset): Level explicitly set on the logger by application code. `null` when the level is
            inherited.
        resolved_level (None | str | Unset): Effective level after framework inheritance. SDKs should always report
            this; the server falls back to `level` when `resolved_level` is missing.
        service (None | str | Unset): Service name that observed the logger.
        environment (None | str | Unset): Environment where the logger was observed.
    """

    id: str
    level: None | str | Unset = UNSET
    resolved_level: None | str | Unset = UNSET
    service: None | str | Unset = UNSET
    environment: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        level: None | str | Unset
        if isinstance(self.level, Unset):
            level = UNSET
        else:
            level = self.level

        resolved_level: None | str | Unset
        if isinstance(self.resolved_level, Unset):
            resolved_level = UNSET
        else:
            resolved_level = self.resolved_level

        service: None | str | Unset
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if level is not UNSET:
            field_dict["level"] = level
        if resolved_level is not UNSET:
            field_dict["resolved_level"] = resolved_level
        if service is not UNSET:
            field_dict["service"] = service
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        level = _parse_level(d.pop("level", UNSET))

        def _parse_resolved_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resolved_level = _parse_resolved_level(d.pop("resolved_level", UNSET))

        def _parse_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_environment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        logger_bulk_item = cls(
            id=id,
            level=level,
            resolved_level=resolved_level,
            service=service,
            environment=environment,
        )

        logger_bulk_item.additional_properties = d
        return logger_bulk_item

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
