from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_level import check_log_level
from ..models.log_level import LogLevel
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.log_group_environments_type_0 import LogGroupEnvironmentsType0


T = TypeVar("T", bound="LogGroup")


@_attrs_define
class LogGroup:
    """A named collection of loggers that share a level configuration.

    Assigning a logger to a group ties the logger's effective level to
    the group's level (and per-environment overrides). Loggers can move
    between groups or be detached from a group entirely.

        Example:
            {'created_at': '2026-04-01T10:00:00Z', 'environments': {'production': {'level': 'ERROR'}}, 'level': 'WARN',
                'name': 'Database Loggers', 'updated_at': '2026-04-01T10:00:00Z'}

        Attributes:
            name (str): Human-readable label for the group.
            level (LogLevel | None | Unset): Default level applied to every logger in the group. `null` leaves member
                loggers to inherit from elsewhere.
            parent_id (None | str | Unset): Reserved for nested groups. Must be `null` in this version; nested groups are
                not yet supported.
            environments (LogGroupEnvironmentsType0 | None | Unset): Per-environment level overrides keyed by environment
                name. Each value is an object with an optional `level` field, e.g. `{"production": {"level": "ERROR"}}`. Member
                loggers inherit the per-environment level unless they set their own override.
            created_at (datetime.datetime | None | Unset): When the group was created.
            updated_at (datetime.datetime | None | Unset): When the group was last modified.
    """

    name: str
    level: LogLevel | None | Unset = UNSET
    parent_id: None | str | Unset = UNSET
    environments: LogGroupEnvironmentsType0 | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.log_group_environments_type_0 import LogGroupEnvironmentsType0

        name = self.name

        level: None | str | Unset
        if isinstance(self.level, Unset):
            level = UNSET
        elif isinstance(self.level, str):
            level = self.level
        else:
            level = self.level

        parent_id: None | str | Unset
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        environments: dict[str, Any] | None | Unset
        if isinstance(self.environments, Unset):
            environments = UNSET
        elif isinstance(self.environments, LogGroupEnvironmentsType0):
            environments = self.environments.to_dict()
        else:
            environments = self.environments

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if level is not UNSET:
            field_dict["level"] = level
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if environments is not UNSET:
            field_dict["environments"] = environments
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_group_environments_type_0 import LogGroupEnvironmentsType0

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_level(data: object) -> LogLevel | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                level_type_0 = check_log_level(data)

                return level_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LogLevel | None | Unset, data)

        level = _parse_level(d.pop("level", UNSET))

        def _parse_parent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_id = _parse_parent_id(d.pop("parent_id", UNSET))

        def _parse_environments(data: object) -> LogGroupEnvironmentsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                environments_type_0 = LogGroupEnvironmentsType0.from_dict(data)

                return environments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LogGroupEnvironmentsType0 | None | Unset, data)

        environments = _parse_environments(d.pop("environments", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        log_group = cls(
            name=name,
            level=level,
            parent_id=parent_id,
            environments=environments,
            created_at=created_at,
            updated_at=updated_at,
        )

        log_group.additional_properties = d
        return log_group

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
