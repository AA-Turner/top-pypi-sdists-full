# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.config — contract/overlay config resolution (OMN-13564).

Zero-upstream-dep stand-in for the canonical overlay system. Resolves endpoint
URLs and config tunables from a packaged overlay document instead of hardcoded
Python literals or bare ``os.environ`` reads.
"""

from __future__ import annotations

from omnibase_compat.config.overlay_resolver import (
    ModelAutowireOverlay,
    ModelCompatRuntimeOverlay,
    ModelEndpointOverlay,
    OverlayResolutionError,
    load_overlay,
    resolve_autowire_strict_raw,
    resolve_endpoint_url,
)

__all__: list[str] = [
    "ModelAutowireOverlay",
    "ModelCompatRuntimeOverlay",
    "ModelEndpointOverlay",
    "OverlayResolutionError",
    "load_overlay",
    "resolve_autowire_strict_raw",
    "resolve_endpoint_url",
]
