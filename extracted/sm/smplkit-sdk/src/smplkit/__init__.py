"""smplkit — Official Python SDK for the smplkit platform."""

import enum

from smplkit.client import AsyncSmplClient, SmplClient
from smplkit._errors import (
    ApiErrorDetail,
    Error,
    ConnectionError,
    ConflictError,
    NotFoundError,
    PaymentRequiredError,
    TimeoutError,
    ValidationError,
)
from smplkit.config.models import ConfigEnvironment, ConfigItem, ItemType
from smplkit.flags.models import FlagEnvironment, FlagRule, FlagValue
from smplkit.flags.types import AsyncContext, Context, FlagDeclaration, Op, Rule
from smplkit.logging._sources import LoggerSource
from smplkit.management.client import AsyncSmplManagementClient, SmplManagementClient
from smplkit.management.types import Color, EnvironmentClassification


class LogLevel(str, enum.Enum):
    """Log severity levels used by the Smpl Logging service.

    Members are declared in ascending order of severity, the canonical
    convention in Python's ``logging`` module and the wider ecosystem:
    ``TRACE < DEBUG < INFO < WARN < ERROR < FATAL < SILENT``. ``SILENT``
    sits at the top because it suppresses every lower level. See
    :mod:`smplkit.logging._levels` for the integer mapping.
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"
    SILENT = "SILENT"


__all__ = [
    "ApiErrorDetail",
    "AsyncContext",
    "AsyncSmplClient",
    "AsyncSmplManagementClient",
    "Color",
    "ConfigEnvironment",
    "ConfigItem",
    "Context",
    "EnvironmentClassification",
    "FlagDeclaration",
    "FlagEnvironment",
    "FlagRule",
    "FlagValue",
    "ItemType",
    "LoggerSource",
    "LogLevel",
    "Op",
    "Rule",
    "SmplClient",
    "Error",
    "ConnectionError",
    "ConflictError",
    "SmplManagementClient",
    "NotFoundError",
    "PaymentRequiredError",
    "TimeoutError",
    "ValidationError",
]

try:
    from smplkit._version import __version__
except ImportError:
    __version__ = "0.0.0"  # Fallback for editable installs without VCS
