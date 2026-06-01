# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Services module."""

from .events import RequestEventsService, RequestEventsServiceConfig
from .files import RequestFilesService, RequestFilesServiceConfig
from .requests import RequestsService, RequestsServiceConfig
from .user_moderation import UserModerationRequestService

__all__ = (
    "RequestEventsService",
    "RequestEventsServiceConfig",
    "RequestFilesService",
    "RequestFilesServiceConfig",
    "RequestsService",
    "RequestsServiceConfig",
    "UserModerationRequestService",
)
