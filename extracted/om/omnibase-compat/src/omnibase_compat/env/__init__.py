# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.env subpackage.

Hosts small, dependency-free helpers that read process environment
variables with canonical, well-documented semantics so every consumer
agrees.
"""

from __future__ import annotations

from omnibase_compat.env.util_is_strict_mode import is_strict_mode

__all__ = ["is_strict_mode"]
