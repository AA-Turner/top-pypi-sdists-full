"""Smpl Flags SDK module — wraps generated flags client.

The fused ``FlagsClient`` / ``AsyncFlagsClient`` live in
``smplkit.flags._client`` and are re-exported only from the top-level
``smplkit`` package (mirroring config), not from here.
"""

from smplkit.flags._client import (
    FlagChangeEvent,
    FlagStats,
)
from smplkit.flags.models import (
    AsyncBooleanFlag,
    AsyncFlag,
    AsyncJsonFlag,
    AsyncNumberFlag,
    AsyncStringFlag,
    BooleanFlag,
    Flag,
    FlagEnvironment,
    FlagRule,
    FlagValue,
    JsonFlag,
    NumberFlag,
    StringFlag,
)
from smplkit.flags.types import AsyncContext, Context, FlagDeclaration, Op, Rule

__all__ = [
    "AsyncBooleanFlag",
    "AsyncContext",
    "AsyncFlag",
    "AsyncJsonFlag",
    "AsyncNumberFlag",
    "AsyncStringFlag",
    "BooleanFlag",
    "Context",
    "Flag",
    "FlagChangeEvent",
    "FlagDeclaration",
    "FlagEnvironment",
    "FlagRule",
    "FlagValue",
    "FlagStats",
    "JsonFlag",
    "NumberFlag",
    "Op",
    "Rule",
    "StringFlag",
]
