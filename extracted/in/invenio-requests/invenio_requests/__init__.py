# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2026 CERN.
# Copyright (C) 2021-2023 TU Wien.
# Copyright (C) 2024-2026 Graz University of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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

__version__ = "13.0.0"

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
