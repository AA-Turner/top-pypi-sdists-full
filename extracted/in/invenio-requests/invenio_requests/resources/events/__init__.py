# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-FileCopyrightText: 2021 Northwestern University.
# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-License-Identifier: MIT

"""Request Events Resource module."""

from .config import RequestCommentsResourceConfig
from .resource import RequestCommentsResource

__all__ = (
    "RequestCommentsResource",
    "RequestCommentsResourceConfig",
)
