# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Package constants.

``VERSION`` is the single source of truth for the package version; pyproject.toml
reads it via setuptools' dynamic ``attr`` (mirroring aiohomematic's
``const.VERSION``). Bump it on every published change to the shared surface.
"""

from typing import Final

VERSION: Final = "2026.6.1"
