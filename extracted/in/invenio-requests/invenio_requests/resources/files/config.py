# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""RequestFiles Resource Configuration."""

from flask_resources import HTTPJSONException, create_error_handler
from invenio_records_resources.resources import RecordResourceConfig
from marshmallow import fields

from invenio_requests.services.files.errors import (
    RequestFileNotFoundError,
    RequestFileSizeLimitError,
)


class RequestFilesResourceConfig(RecordResourceConfig):
    """Request Files resource configuration."""

    blueprint_name = "request_files"
    url_prefix = "/requests"
    routes = {
        "create": "/<id>/files/upload/<key>",
        "item": "/<id>/files/<key>",
        "item_content": "/<id>/files/<key>/content",
    }

    request_view_args = {
        "id": fields.UUID(),
        "key": fields.Str(),
    }

    response_handlers = {
        "application/vnd.inveniordm.v1+json": RecordResourceConfig.response_handlers[
            "application/json"
        ],
        **RecordResourceConfig.response_handlers,
    }

    error_handlers = {
        **RecordResourceConfig.error_handlers,
        RequestFileSizeLimitError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=str(e),
            )
        ),
        RequestFileNotFoundError: create_error_handler(
            lambda e: HTTPJSONException(
                code=404,
                description=str(e),
            )
        ),
    }
