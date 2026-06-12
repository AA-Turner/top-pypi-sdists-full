"""Smpl Platform — cross-cutting CRUD resources on ``client.platform``.

``client.platform`` groups the account-wide configuration resources that
aren't owned by a single product:

- ``client.platform.environments.*``
- ``client.platform.services.*``
- ``client.platform.contexts.*``
- ``client.platform.context_types.*``

The :class:`PlatformClient` / :class:`AsyncPlatformClient` classes are
re-exported from the top-level :mod:`smplkit` package (the established
convention that clients re-export from ``smplkit`` only). This package
exports the customer-facing models and enums for the platform resources.
"""

from __future__ import annotations

from smplkit.platform.models import (
    AsyncContextType,
    AsyncEnvironment,
    AsyncService,
    ContextType,
    Environment,
    Service,
)
from smplkit.platform.types import Color, EnvironmentClassification

__all__ = [
    "AsyncContextType",
    "AsyncEnvironment",
    "AsyncService",
    "Color",
    "ContextType",
    "Environment",
    "EnvironmentClassification",
    "Service",
]
