# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-License-Identifier: MIT

"""Request comment services module."""

from .config import RequestEventsServiceConfig
from .service import RequestEventsService

__all__ = (
    "RequestEventsService",
    "RequestEventsServiceConfig",
)
