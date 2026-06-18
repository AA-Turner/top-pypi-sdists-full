# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-License-Identifier: MIT

"""Request Resources module."""

from .config import RequestsResourceConfig
from .resource import RequestsResource

__all__ = (
    "RequestsResource",
    "RequestsResourceConfig",
)
