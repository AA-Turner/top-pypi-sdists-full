"""Shared provider runtime wiring for product surfaces.

This module keeps surface-level provider profile parsing, encrypted local
credential lookup, endpoint model discovery, and runtime capability selection
in one place so CLI, API, and gateway do not each keep private copies of the
same rules.
"""

from __future__ import annotations

from .provider_runtime_support import *  # noqa: F401,F403
from .provider_runtime_capability import SurfaceModelProviderCapability
