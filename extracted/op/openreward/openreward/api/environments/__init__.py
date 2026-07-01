"""Environment-focused client APIs for OpenReward."""

from openreward.api.errors import (
    HeartbeatTimeoutError,
    HTTPStatusError,
    MaxRetriesError,
    OpenRewardError,
    SessionTerminatedError,
    ToolCallError,
    ToolFailed,
    TransportError,
)

from .client import EnvironmentsAPI, AsyncEnvironmentsAPI, Session, AsyncSession
from .types import AuthenticationError

__all__ = [
    "AsyncEnvironmentsAPI",
    "AsyncSession",
    "AuthenticationError",
    "EnvironmentsAPI",
    "HTTPStatusError",
    "HeartbeatTimeoutError",
    "MaxRetriesError",
    "OpenRewardError",
    "Session",
    "SessionTerminatedError",
    "ToolCallError",
    "ToolFailed",
    "TransportError",
]
