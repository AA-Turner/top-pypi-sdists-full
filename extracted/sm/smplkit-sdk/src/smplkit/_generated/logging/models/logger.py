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
    from ..models.logger_effective_levels_type_0 import LoggerEffectiveLevelsType0
    from ..models.logger_environments_type_0 import LoggerEnvironmentsType0
    from ..models.logger_sources_type_0_item import LoggerSourcesType0Item


T = TypeVar("T", bound="Logger")


@_attrs_define
class Logger:
    """A logger configured for the account.

    Loggers are organized by dot-separated key (for example, `sqlalchemy.engine`),
    matching the hierarchical naming convention used by most logging
    frameworks. A managed logger applies the configured level to every
    runtime where the logger appears; unmanaged loggers are tracked only
    as observations from SDKs.

        Example:
            {'created_at': '2026-04-01T10:00:00Z', 'environments': {'production': {'level': 'WARN'}, 'staging': {'level':
                'DEBUG'}}, 'group': 'database-loggers', 'level': 'DEBUG', 'managed': True, 'name': 'SQL Logger', 'updated_at':
                '2026-04-01T10:00:00Z'}

        Attributes:
            name (str): Human-readable label for the logger.
            level (LogLevel | None | Unset): Account-wide log level applied to this logger. `null` means no override at the
                logger level — the level is inherited from the logger's group or the framework default.
            group (None | str | Unset): Key of the log group this logger belongs to, or `null` if the logger is not grouped.
                Assigning a logger to a group promotes it to managed; assigning a group cascades to unmanaged descendants by
                clearing their group reference.
            managed (bool | None | Unset): When `true`, the logger is part of the account's managed configuration and counts
                toward the managed-loggers usage counter. Setting `level`, `group`, or `environments` on an unmanaged logger
                promotes it to managed automatically.
            sources (list[LoggerSourcesType0Item] | None | Unset): Service / environment observations reported by SDKs for
                this logger. Each entry carries the service name, environment, the level the SDK saw, the resolved level after
                framework inheritance, and timestamps for the first and most recent sighting.
            environments (LoggerEnvironmentsType0 | None | Unset): Per-environment level overrides keyed by environment
                name. Each value is an object with an optional `level` field, e.g. `{"production": {"level": "WARN"}}`. An
                environment may be present with no `level` to record that the logger applies there without changing the resolved
                level.
            effective_levels (LoggerEffectiveLevelsType0 | None | Unset): Per-environment summary of what runtimes are
                reporting for this logger. Keyed by environment name; each value is the list of distinct resolved levels
                observed across all source rows in that environment, ordered from most-verbose (`TRACE`) to least-verbose
                (`SILENT`). A single-element list means every source agrees; a multi-element list means sources disagree.
                Environments with no observed sources are omitted — cross-reference `environments` to find environments that are
                configured but have not yet been reported in.
            created_at (datetime.datetime | None | Unset): When the logger was first created or discovered.
            updated_at (datetime.datetime | None | Unset): When the logger was last modified.
    """

    name: str
    level: LogLevel | None | Unset = UNSET
    group: None | str | Unset = UNSET
    managed: bool | None | Unset = UNSET
    sources: list[LoggerSourcesType0Item] | None | Unset = UNSET
    environments: LoggerEnvironmentsType0 | None | Unset = UNSET
    effective_levels: LoggerEffectiveLevelsType0 | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.logger_effective_levels_type_0 import LoggerEffectiveLevelsType0
        from ..models.logger_environments_type_0 import LoggerEnvironmentsType0

        name = self.name

        level: None | str | Unset
        if isinstance(self.level, Unset):
            level = UNSET
        elif isinstance(self.level, str):
            level = self.level
        else:
            level = self.level

        group: None | str | Unset
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        managed: bool | None | Unset
        if isinstance(self.managed, Unset):
            managed = UNSET
        else:
            managed = self.managed

        sources: list[dict[str, Any]] | None | Unset
        if isinstance(self.sources, Unset):
            sources = UNSET
        elif isinstance(self.sources, list):
            sources = []
            for sources_type_0_item_data in self.sources:
                sources_type_0_item = sources_type_0_item_data.to_dict()
                sources.append(sources_type_0_item)

        else:
            sources = self.sources

        environments: dict[str, Any] | None | Unset
        if isinstance(self.environments, Unset):
            environments = UNSET
        elif isinstance(self.environments, LoggerEnvironmentsType0):
            environments = self.environments.to_dict()
        else:
            environments = self.environments

        effective_levels: dict[str, Any] | None | Unset
        if isinstance(self.effective_levels, Unset):
            effective_levels = UNSET
        elif isinstance(self.effective_levels, LoggerEffectiveLevelsType0):
            effective_levels = self.effective_levels.to_dict()
        else:
            effective_levels = self.effective_levels

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
        if group is not UNSET:
            field_dict["group"] = group
        if managed is not UNSET:
            field_dict["managed"] = managed
        if sources is not UNSET:
            field_dict["sources"] = sources
        if environments is not UNSET:
            field_dict["environments"] = environments
        if effective_levels is not UNSET:
            field_dict["effective_levels"] = effective_levels
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.logger_effective_levels_type_0 import LoggerEffectiveLevelsType0
        from ..models.logger_environments_type_0 import LoggerEnvironmentsType0
        from ..models.logger_sources_type_0_item import LoggerSourcesType0Item

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

        def _parse_group(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group = _parse_group(d.pop("group", UNSET))

        def _parse_managed(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        managed = _parse_managed(d.pop("managed", UNSET))

        def _parse_sources(data: object) -> list[LoggerSourcesType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sources_type_0 = []
                _sources_type_0 = data
                for sources_type_0_item_data in _sources_type_0:
                    sources_type_0_item = LoggerSourcesType0Item.from_dict(sources_type_0_item_data)

                    sources_type_0.append(sources_type_0_item)

                return sources_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[LoggerSourcesType0Item] | None | Unset, data)

        sources = _parse_sources(d.pop("sources", UNSET))

        def _parse_environments(data: object) -> LoggerEnvironmentsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                environments_type_0 = LoggerEnvironmentsType0.from_dict(data)

                return environments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LoggerEnvironmentsType0 | None | Unset, data)

        environments = _parse_environments(d.pop("environments", UNSET))

        def _parse_effective_levels(data: object) -> LoggerEffectiveLevelsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                effective_levels_type_0 = LoggerEffectiveLevelsType0.from_dict(data)

                return effective_levels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LoggerEffectiveLevelsType0 | None | Unset, data)

        effective_levels = _parse_effective_levels(d.pop("effective_levels", UNSET))

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

        logger = cls(
            name=name,
            level=level,
            group=group,
            managed=managed,
            sources=sources,
            environments=environments,
            effective_levels=effective_levels,
            created_at=created_at,
            updated_at=updated_at,
        )

        logger.additional_properties = d
        return logger

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
