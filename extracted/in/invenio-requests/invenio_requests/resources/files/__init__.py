# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-License-Identifier: MIT

"""Request Files Resource module."""

from .config import RequestFilesResourceConfig
from .resource import RequestFilesResource

__all__ = (
    "RequestFilesResource",
    "RequestFilesResourceConfig",
)
