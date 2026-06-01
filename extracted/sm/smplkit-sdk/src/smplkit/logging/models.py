"""SmplLogger / SmplLogGroup active-record models."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from smplkit import LogLevel
    from smplkit.logging.client import AsyncLoggingClient, LoggingClient
    from smplkit.management.client import (
        AsyncLogGroupsClient,
        AsyncLoggersClient,
        LogGroupsClient,
        LoggersClient,
    )


@dataclasses.dataclass(frozen=True)
class LoggerEnvironment:
    """Per-environment configuration on a logger or log group.

    Lives at ``logger.environments[env_name]`` (a ``dict[str, LoggerEnvironment]``).
    Frozen — mutate the override via ``logger.set_level(level, environment="...")``
    or remove it via ``logger.clear_level(environment="...")``.

    Attributes:
        level: Per-environment level override (``None`` means no override).
    """

    level: LogLevel | None = None


def _convert_environments(
    value: dict[str, Any] | None,
) -> dict[str, LoggerEnvironment]:
    """Coerce a dict input into ``dict[str, LoggerEnvironment]``.

    Accepts both pre-built :class:`LoggerEnvironment` instances and the wire-shaped
    ``{env_id: {"level": "ERROR"}}`` dicts produced by ``_extract_environments``.
    """
    if not value:
        return {}
    from smplkit import LogLevel as _LogLevel  # lazy to avoid circular import

    result: dict[str, LoggerEnvironment] = {}
    for env_id, env_data in value.items():
        if isinstance(env_data, LoggerEnvironment):
            result[env_id] = env_data
        elif isinstance(env_data, dict):
            level_str = env_data.get("level")
            if level_str is not None:
                try:
                    result[env_id] = LoggerEnvironment(level=_LogLevel(level_str))
                except ValueError:
                    result[env_id] = LoggerEnvironment()
            else:
                result[env_id] = LoggerEnvironment()
        else:
            result[env_id] = LoggerEnvironment()
    return result


def _environments_to_wire(
    environments: dict[str, LoggerEnvironment],
) -> dict[str, Any]:
    """Convert a typed environments dict to the wire-shaped dict for sending.

    Entries with ``level=None`` are skipped (no override to send).
    """
    return {env_id: {"level": env.level.value} for env_id, env in environments.items() if env.level is not None}


class SmplLogger:
    """SDK model for a logger resource.

    Modify properties locally, then call :meth:`save` to persist.
    """

    id: str | None
    name: str
    level: LogLevel | None
    group: str | None
    managed: bool | None
    sources: list[dict[str, Any]]
    created_at: Any
    updated_at: Any

    def __init__(
        self,
        client: LoggersClient | LoggingClient | None = None,
        *,
        id: str | None = None,
        name: str,
        level: LogLevel | None = None,
        group: str | None = None,
        managed: bool | None = None,
        sources: list[dict[str, Any]] | None = None,
        environments: dict[str, Any] | None = None,
        created_at: Any = None,
        updated_at: Any = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.level = level
        self.group = group
        self.managed = managed
        self.sources = sources or []
        self._environments: dict[str, LoggerEnvironment] = _convert_environments(environments)
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def environments(self) -> dict[str, LoggerEnvironment]:
        """Read-only view of per-environment level overrides.

        Mutate via :meth:`set_level` / :meth:`clear_level` /
        :meth:`clear_all_environment_levels` (with ``environment="..."``).
        """
        return dict(self._environments)

    def save(self) -> None:
        """Persist this logger to the server (create or update)."""
        if self._client is None:
            raise RuntimeError("SmplLogger was constructed without a client; cannot save")
        updated = self._client._save_logger(self)
        self._apply(updated)

    def delete(self) -> None:
        """Delete this logger from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("SmplLogger was constructed without a client or id; cannot delete")
        self._client.delete(self.id)

    def set_level(self, level: LogLevel, *, environment: str | None = None) -> None:
        """Set the log level.

        With ``environment=None`` (the default), sets the base log level used
        when no environment-specific override applies.  With ``environment="..."``,
        sets the per-environment override.
        """
        if environment is None:
            self.level = level
        else:
            self._environments[environment] = LoggerEnvironment(level=level)

    def clear_level(self, *, environment: str | None = None) -> None:
        """Remove a log level.

        With ``environment=None`` (the default), removes the base log level
        (the logger then inherits from its group / dot-notation ancestor /
        system default).  With ``environment="..."``, removes the per-environment
        override only.
        """
        if environment is None:
            self.level = None
        else:
            self._environments.pop(environment, None)

    def clear_all_environment_levels(self) -> None:
        """Remove all per-environment level overrides."""
        self._environments = {}

    def _apply(self, other: SmplLogger) -> None:
        """Copy all properties from other into self."""
        self.id = other.id
        self.name = other.name
        self.level = other.level
        self.group = other.group
        self.managed = other.managed
        self.sources = other.sources
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def __repr__(self) -> str:
        return f"SmplLogger(id={self.id!r}, name={self.name!r})"


class AsyncSmplLogger:
    """Async SDK model for a logger resource."""

    id: str | None
    name: str
    level: LogLevel | None
    group: str | None
    managed: bool | None
    sources: list[dict[str, Any]]
    created_at: Any
    updated_at: Any

    def __init__(
        self,
        client: AsyncLoggersClient | AsyncLoggingClient | None = None,
        *,
        id: str | None = None,
        name: str,
        level: LogLevel | None = None,
        group: str | None = None,
        managed: bool | None = None,
        sources: list[dict[str, Any]] | None = None,
        environments: dict[str, Any] | None = None,
        created_at: Any = None,
        updated_at: Any = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.level = level
        self.group = group
        self.managed = managed
        self.sources = sources or []
        self._environments: dict[str, LoggerEnvironment] = _convert_environments(environments)
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def environments(self) -> dict[str, LoggerEnvironment]:
        """Read-only view of per-environment level overrides.

        Mutate via :meth:`set_level` / :meth:`clear_level` /
        :meth:`clear_all_environment_levels` (with ``environment="..."``).
        """
        return dict(self._environments)

    async def save(self) -> None:
        """Persist this logger to the server (create or update)."""
        if self._client is None:
            raise RuntimeError("AsyncSmplLogger was constructed without a client; cannot save")
        updated = await self._client._save_logger(self)
        self._apply(updated)

    async def delete(self) -> None:
        """Delete this logger from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("AsyncSmplLogger was constructed without a client or id; cannot delete")
        await self._client.delete(self.id)

    def set_level(self, level: LogLevel, *, environment: str | None = None) -> None:
        """Set the log level.

        With ``environment=None`` (the default), sets the base log level used
        when no environment-specific override applies.  With ``environment="..."``,
        sets the per-environment override.
        """
        if environment is None:
            self.level = level
        else:
            self._environments[environment] = LoggerEnvironment(level=level)

    def clear_level(self, *, environment: str | None = None) -> None:
        """Remove a log level.

        With ``environment=None`` (the default), removes the base log level
        (the logger then inherits from its group / dot-notation ancestor /
        system default).  With ``environment="..."``, removes the per-environment
        override only.
        """
        if environment is None:
            self.level = None
        else:
            self._environments.pop(environment, None)

    def clear_all_environment_levels(self) -> None:
        """Remove all per-environment level overrides."""
        self._environments = {}

    def _apply(self, other: AsyncSmplLogger) -> None:
        """Copy all properties from other into self."""
        self.id = other.id
        self.name = other.name
        self.level = other.level
        self.group = other.group
        self.managed = other.managed
        self.sources = other.sources
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def __repr__(self) -> str:
        return f"AsyncSmplLogger(id={self.id!r}, name={self.name!r})"


class SmplLogGroup:
    """SDK model for a log group resource."""

    id: str | None
    name: str
    level: LogLevel | None
    group: str | None
    created_at: Any
    updated_at: Any

    def __init__(
        self,
        client: LogGroupsClient | LoggingClient | None = None,
        *,
        id: str | None = None,
        name: str,
        level: LogLevel | None = None,
        group: str | None = None,
        environments: dict[str, Any] | None = None,
        created_at: Any = None,
        updated_at: Any = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.level = level
        self.group = group
        self._environments: dict[str, LoggerEnvironment] = _convert_environments(environments)
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def environments(self) -> dict[str, LoggerEnvironment]:
        """Read-only view of per-environment level overrides.

        Mutate via :meth:`set_level` / :meth:`clear_level` /
        :meth:`clear_all_environment_levels` (with ``environment="..."``).
        """
        return dict(self._environments)

    def save(self) -> None:
        """Persist this group to the server (create or update)."""
        if self._client is None:
            raise RuntimeError("SmplLogGroup was constructed without a client; cannot save")
        updated = self._client._save_group(self)
        self._apply(updated)

    def delete(self) -> None:
        """Delete this group from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("SmplLogGroup was constructed without a client or id; cannot delete")
        self._client.delete(self.id)

    def set_level(self, level: LogLevel, *, environment: str | None = None) -> None:
        """Set the log level.

        With ``environment=None`` (the default), sets the base log level used
        when no environment-specific override applies.  With ``environment="..."``,
        sets the per-environment override.
        """
        if environment is None:
            self.level = level
        else:
            self._environments[environment] = LoggerEnvironment(level=level)

    def clear_level(self, *, environment: str | None = None) -> None:
        """Remove a log level.

        With ``environment=None`` (the default), removes the base log level
        (the logger then inherits from its group / dot-notation ancestor /
        system default).  With ``environment="..."``, removes the per-environment
        override only.
        """
        if environment is None:
            self.level = None
        else:
            self._environments.pop(environment, None)

    def clear_all_environment_levels(self) -> None:
        """Remove all per-environment level overrides."""
        self._environments = {}

    def _apply(self, other: SmplLogGroup) -> None:
        """Copy all properties from other into self."""
        self.id = other.id
        self.name = other.name
        self.level = other.level
        self.group = other.group
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def __repr__(self) -> str:
        return f"SmplLogGroup(id={self.id!r}, name={self.name!r})"


class AsyncSmplLogGroup:
    """Async SDK model for a log group resource."""

    id: str | None
    name: str
    level: LogLevel | None
    group: str | None
    created_at: Any
    updated_at: Any

    def __init__(
        self,
        client: AsyncLogGroupsClient | AsyncLoggingClient | None = None,
        *,
        id: str | None = None,
        name: str,
        level: LogLevel | None = None,
        group: str | None = None,
        environments: dict[str, Any] | None = None,
        created_at: Any = None,
        updated_at: Any = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.level = level
        self.group = group
        self._environments: dict[str, LoggerEnvironment] = _convert_environments(environments)
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def environments(self) -> dict[str, LoggerEnvironment]:
        """Read-only view of per-environment level overrides.

        Mutate via :meth:`set_level` / :meth:`clear_level` /
        :meth:`clear_all_environment_levels` (with ``environment="..."``).
        """
        return dict(self._environments)

    async def save(self) -> None:
        """Persist this group to the server (create or update)."""
        if self._client is None:
            raise RuntimeError("AsyncSmplLogGroup was constructed without a client; cannot save")
        updated = await self._client._save_group(self)
        self._apply(updated)

    async def delete(self) -> None:
        """Delete this group from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("AsyncSmplLogGroup was constructed without a client or id; cannot delete")
        await self._client.delete(self.id)

    def set_level(self, level: LogLevel, *, environment: str | None = None) -> None:
        """Set the log level.

        With ``environment=None`` (the default), sets the base log level used
        when no environment-specific override applies.  With ``environment="..."``,
        sets the per-environment override.
        """
        if environment is None:
            self.level = level
        else:
            self._environments[environment] = LoggerEnvironment(level=level)

    def clear_level(self, *, environment: str | None = None) -> None:
        """Remove a log level.

        With ``environment=None`` (the default), removes the base log level
        (the logger then inherits from its group / dot-notation ancestor /
        system default).  With ``environment="..."``, removes the per-environment
        override only.
        """
        if environment is None:
            self.level = None
        else:
            self._environments.pop(environment, None)

    def clear_all_environment_levels(self) -> None:
        """Remove all per-environment level overrides."""
        self._environments = {}

    def _apply(self, other: AsyncSmplLogGroup) -> None:
        """Copy all properties from other into self."""
        self.id = other.id
        self.name = other.name
        self.level = other.level
        self.group = other.group
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def __repr__(self) -> str:
        return f"AsyncSmplLogGroup(id={self.id!r}, name={self.name!r})"
