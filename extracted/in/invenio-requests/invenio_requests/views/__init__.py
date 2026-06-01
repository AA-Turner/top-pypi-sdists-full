# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request views module."""

from flask import Blueprint

from .api import create_request_events_bp, create_request_files_bp, create_requests_bp
from .ui import create_ui_blueprint

blueprint = Blueprint("invenio-requests-ext", __name__)


__all__ = (
    "blueprint",
    "create_ui_blueprint",
    "create_requests_bp",
    "create_request_events_bp",
    "create_request_files_bp",
)
