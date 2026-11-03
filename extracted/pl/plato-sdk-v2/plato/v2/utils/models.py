"""Pydantic models for database cleanup operations."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

from pydantic import BaseModel, ConfigDict

from plato._generated.models import SessionStateResult


class ApiCleanupResult(BaseModel):
    """Result of calling the cleanup API."""

    success: bool = False
    skipped: bool = False
    reason: str | None = None
    result: dict[str, Any] | None = None


class DatabaseCleanupResult(BaseModel):
    """Result of cleaning a single database."""

    success: bool
    tables_truncated: list[str] = []
    error: str | None = None


class EnvironmentCleanupResult(BaseModel):
    """Result of cleaning all databases for an environment."""

    api_cleanup: ApiCleanupResult
    databases: dict[str, DatabaseCleanupResult] = {}
    cache_cleared: bool = False
    cache_clear_error: str | None = None


class SessionCleanupResult(BaseModel):
    """Result of cleaning all environments in a session."""

    environments: dict[str, EnvironmentCleanupResult] = {}


class EnvironmentInfo(BaseModel):
    """Environment info for cleanup operations."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    job_id: str
    alias: str
    artifact_id: str | None = None
    cleanup_fn: Callable[[], Coroutine[Any, Any, dict[str, Any]]] | None = None
    get_state_fn: Callable[[], Coroutine[Any, Any, SessionStateResult]]
