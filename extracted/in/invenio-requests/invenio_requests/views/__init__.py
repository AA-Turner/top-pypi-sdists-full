# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-FileCopyrightText: 2023 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
