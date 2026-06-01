"""Stateless helpers shared between the runtime and management logging clients."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from smplkit._generated.logging.models.log_group import LogGroup as GenLogGroup
from smplkit._generated.logging.models.log_group_environments_type_0 import LogGroupEnvironmentsType0
from smplkit._generated.logging.models.log_group_resource import LogGroupResource
from smplkit._generated.logging.models.log_group_response import LogGroupResponse
from smplkit._generated.logging.models.logger import Logger as GenLogger
from smplkit._generated.logging.models.logger_environments_type_0 import LoggerEnvironmentsType0
from smplkit._generated.logging.models.logger_resource import LoggerResource
from smplkit._generated.logging.models.logger_response import LoggerResponse
from smplkit.logging.models import AsyncSmplLogGroup, AsyncSmplLogger, SmplLogGroup, SmplLogger

if TYPE_CHECKING:  # pragma: no cover
    from smplkit import LogLevel
    from smplkit.logging.client import AsyncLoggingClient, LoggingClient
    from smplkit.management.client import (
        AsyncLogGroupsClient,
        AsyncLoggersClient,
        LogGroupsClient,
        LoggersClient,
    )


def _str_to_log_level(s: str | None) -> LogLevel | None:
    """Convert a raw wire-format level string to a LogLevel enum, or None."""
    if s is None:
        return None
    from smplkit import LogLevel as _LogLevel  # lazy to avoid circular import

    try:
        return _LogLevel(s)
    except ValueError:
        return None


def _loglevel_value(level: Any, *, where: str) -> str | None:
    """Return the wire-format string for a ``LogLevel | str | None`` argument."""
    if level is None:
        return None
    from smplkit import LogLevel as _LogLevel  # lazy to avoid circular import

    if isinstance(level, _LogLevel):
        return level.value
    if isinstance(level, str):
        try:
            return _LogLevel(level).value
        except ValueError as exc:
            raise TypeError(
                f"{where}: level string must match a LogLevel (got {level!r})",
            ) from exc
    raise TypeError(f"{where}: level must be a LogLevel (got {type(level).__name__}: {level!r})")


def _unset_to_none(value: Any) -> Any:
    """Convert Unset sentinels to None."""
    type_name = type(value).__name__
    if type_name == "Unset":
        return None
    return value


def _extract_datetime(value: Any) -> Any:
    """Pass through datetime objects, return None for Unset/None."""
    if value is None:
        return None
    type_name = type(value).__name__
    if type_name == "Unset":
        return None
    return value


def _extract_environments(environments: Any) -> dict[str, Any]:
    """Extract a plain dict from a generated environments object."""
    if environments is None:
        return {}
    type_name = type(environments).__name__
    if type_name == "Unset":
        return {}
    if isinstance(environments, (LoggerEnvironmentsType0, LogGroupEnvironmentsType0)):
        return dict(environments.additional_properties)
    if isinstance(environments, dict):
        return dict(environments)
    return {}


def _make_environments(environments: dict[str, Any] | None) -> LoggerEnvironmentsType0 | None:
    """Convert a plain dict to the generated LoggerEnvironmentsType0."""
    if environments is None:
        return None
    obj = LoggerEnvironmentsType0()
    obj.additional_properties = dict(environments)
    return obj


def _make_group_environments(environments: dict[str, Any] | None) -> LogGroupEnvironmentsType0 | None:
    """Convert a plain dict to the generated LogGroupEnvironmentsType0."""
    if environments is None:
        return None
    obj = LogGroupEnvironmentsType0()
    obj.additional_properties = dict(environments)
    return obj


def _extract_sources(sources: Any) -> list[dict[str, Any]]:
    """Extract sources list from generated model."""
    if sources is None:
        return []
    type_name = type(sources).__name__
    if type_name == "Unset":
        return []
    if isinstance(sources, list):
        result = []
        for item in sources:
            if hasattr(item, "additional_properties"):
                result.append(dict(item.additional_properties))
            elif isinstance(item, dict):
                result.append(item)
        return result
    return []


def _build_logger_body(
    *,
    logger_id: str | None = None,
    name: str,
    level: str | None = None,
    group: str | None = None,
    managed: bool | None = None,
    environments: dict[str, Any] | None = None,
) -> LoggerResponse:
    """Build a JSON:API request body for logger create/update."""
    attrs = GenLogger(
        name=name,
        level=level,
        group=group,
        managed=managed,
        environments=_make_environments(environments),
    )
    resource = LoggerResource(attributes=attrs, id=logger_id, type_="logger")
    return LoggerResponse(data=resource)


def _build_log_group_body(
    *,
    group_id: str | None = None,
    name: str,
    level: str | None = None,
    group: str | None = None,
    environments: dict[str, Any] | None = None,
) -> LogGroupResponse:
    """Build a JSON:API request body for log group create/update."""
    attrs = GenLogGroup(
        name=name,
        level=level,
        parent_id=group,
        environments=_make_group_environments(environments),
    )
    resource = LogGroupResource(attributes=attrs, id=group_id, type_="log_group")
    return LogGroupResponse(data=resource)


def _logger_resource_to_model(client: LoggingClient | LoggersClient | None, resource: Any) -> SmplLogger:
    attrs = resource.attributes
    return SmplLogger(
        client,
        id=_unset_to_none(resource.id) or "",
        name=attrs.name,
        level=_str_to_log_level(_unset_to_none(attrs.level)),
        group=_unset_to_none(attrs.group),
        managed=_unset_to_none(attrs.managed),
        sources=_extract_sources(getattr(attrs, "sources", None)),
        environments=_extract_environments(attrs.environments),
        created_at=_extract_datetime(attrs.created_at),
        updated_at=_extract_datetime(attrs.updated_at),
    )


def _logger_resource_to_async_model(
    client: AsyncLoggingClient | AsyncLoggersClient | None, resource: Any
) -> AsyncSmplLogger:
    attrs = resource.attributes
    return AsyncSmplLogger(
        client,
        id=_unset_to_none(resource.id) or "",
        name=attrs.name,
        level=_str_to_log_level(_unset_to_none(attrs.level)),
        group=_unset_to_none(attrs.group),
        managed=_unset_to_none(attrs.managed),
        sources=_extract_sources(getattr(attrs, "sources", None)),
        environments=_extract_environments(attrs.environments),
        created_at=_extract_datetime(attrs.created_at),
        updated_at=_extract_datetime(attrs.updated_at),
    )


def _log_group_resource_to_model(client: LoggingClient | LogGroupsClient | None, resource: Any) -> SmplLogGroup:
    attrs = resource.attributes
    return SmplLogGroup(
        client,
        id=_unset_to_none(resource.id) or "",
        name=attrs.name,
        level=_str_to_log_level(_unset_to_none(attrs.level)),
        group=_unset_to_none(attrs.parent_id),
        environments=_extract_environments(attrs.environments),
        created_at=_extract_datetime(attrs.created_at),
        updated_at=_extract_datetime(attrs.updated_at),
    )


def _log_group_resource_to_async_model(
    client: AsyncLoggingClient | AsyncLogGroupsClient | None, resource: Any
) -> AsyncSmplLogGroup:
    attrs = resource.attributes
    return AsyncSmplLogGroup(
        client,
        id=_unset_to_none(resource.id) or "",
        name=attrs.name,
        level=_str_to_log_level(_unset_to_none(attrs.level)),
        group=_unset_to_none(attrs.parent_id),
        environments=_extract_environments(attrs.environments),
        created_at=_extract_datetime(attrs.created_at),
        updated_at=_extract_datetime(attrs.updated_at),
    )
