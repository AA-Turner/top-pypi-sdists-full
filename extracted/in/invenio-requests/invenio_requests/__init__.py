# SPDX-FileCopyrightText: 2021-2026 CERN.
# SPDX-FileCopyrightText: 2021-2023 TU Wien.
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module for generic and customizable requests."""

from .customizations import RequestAction
from .ext import InvenioRequests
from .proxies import (
    current_event_type_registry,
    current_events_service,
    current_request_files_service,
    current_request_type_registry,
    current_requests,
    current_requests_resource,
    current_requests_service,
)

__version__ = "15.0.0"

__all__ = (
    "__version__",
    "current_event_type_registry",
    "current_events_service",
    "current_request_files_service",
    "current_request_type_registry",
    "current_requests_resource",
    "current_requests_service",
    "current_requests",
    "InvenioRequests",
    "RequestAction",
)
