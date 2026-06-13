"""smplkit — Official Python SDK for the smplkit platform."""

import enum

from smplkit.account.clients import AccountClient, AsyncAccountClient
from smplkit.audit.clients import AsyncAuditClient, AuditClient
from smplkit.clients import AsyncSmplClient, SmplClient
from smplkit.context import ContextScope
from smplkit.errors import (
    ApiErrorDetail,
    Error,
    ConnectionError,
    ConflictError,
    NotFoundError,
    NotInstalledError,
    PaymentRequiredError,
    TimeoutError,
    ValidationError,
)
from smplkit.config.clients import AsyncConfigClient, ConfigChangeEvent, ConfigClient
from smplkit.config.models import ConfigEnvironment, ConfigItem, ItemType
from smplkit.flags.clients import AsyncFlagsClient, FlagChangeEvent, FlagsClient
from smplkit.flags.models import FlagEnvironment, FlagRule, FlagValue
from smplkit.flags.types import AsyncContext, Context, FlagDeclaration, Op, Rule
from smplkit.jobs.clients import AsyncJobsClient, JobsClient
from smplkit.logging.clients import AsyncLoggingClient, LoggerChangeEvent, LoggingClient
from smplkit.logging.sources import LoggerSource
from smplkit.platform.clients import AsyncPlatformClient, PlatformClient
from smplkit.platform.types import Color, EnvironmentClassification


class LogLevel(str, enum.Enum):
    """Log severity levels used by the Smpl Logging service.

    Members are declared in ascending order of severity, the canonical
    convention in Python's ``logging`` module and the wider ecosystem:
    ``TRACE < DEBUG < INFO < WARN < ERROR < FATAL < SILENT``. ``SILENT``
    sits at the top because it suppresses every lower level.
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"
    SILENT = "SILENT"


__all__ = [
    "AccountClient",
    "ApiErrorDetail",
    "AsyncAccountClient",
    "AsyncAuditClient",
    "AsyncConfigClient",
    "AsyncContext",
    "AsyncFlagsClient",
    "AsyncJobsClient",
    "AsyncLoggingClient",
    "AsyncPlatformClient",
    "AsyncSmplClient",
    "AuditClient",
    "Color",
    "ConfigChangeEvent",
    "ConfigClient",
    "ConfigEnvironment",
    "ConfigItem",
    "ConflictError",
    "ConnectionError",
    "Context",
    "ContextScope",
    "EnvironmentClassification",
    "Error",
    "FlagChangeEvent",
    "FlagDeclaration",
    "FlagEnvironment",
    "FlagRule",
    "FlagValue",
    "FlagsClient",
    "ItemType",
    "JobsClient",
    "LogLevel",
    "LoggerChangeEvent",
    "LoggerSource",
    "LoggingClient",
    "NotFoundError",
    "NotInstalledError",
    "Op",
    "PaymentRequiredError",
    "PlatformClient",
    "Rule",
    "SmplClient",
    "TimeoutError",
    "ValidationError",
]

try:
    from smplkit._version import __version__
except ImportError:
    __version__ = "0.0.0"  # Fallback for editable installs without VCS
