# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2022 KTH Royal Institute of Technology
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""RequestEvent Resource Configuration."""

from flask_resources import HTTPJSONException, create_error_handler
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)
from marshmallow import fields

from ...errors import (
    ChildrenNotSupportedError,
    NestedChildrenNotAllowedError,
    RequestEventPermissionError,
    RequestLockedError,
)


class RequestCommentsSearchRequestArgsSchema(SearchRequestArgsSchema):
    """Add parameter to parse tags."""

    focus_event_id = fields.UUID()


class RequestCommentsResourceConfig(RecordResourceConfig):
    """Request Events resource configuration."""

    blueprint_name = "request_events"
    url_prefix = "/requests"
    routes = {
        "list": "/<request_id>/comments",
        "item": "/<request_id>/comments/<comment_id>",
        "reply": "/<request_id>/comments/<comment_id>/reply",
        "replies": "/<request_id>/comments/<comment_id>/replies",
        "replies_focused": "/<request_id>/comments/<comment_id>/replies_focused",
        "timeline": "/<request_id>/timeline",
        "timeline_focused": "/<request_id>/timeline_focused",
    }

    # Input
    # WARNING: These "request_*" values have nothing to do with the
    #          "Request" of "RequestEvent". They are related to the Flask
    #          request.
    request_list_view_args = {
        "request_id": fields.UUID(),
        "comment_id": fields.Str(),
    }
    request_item_view_args = {
        "request_id": fields.Str(),
        "comment_id": fields.Str(),
    }

    request_search_args = RequestCommentsSearchRequestArgsSchema

    response_handlers = {
        "application/vnd.inveniordm.v1+json": RecordResourceConfig.response_handlers[
            "application/json"
        ],
        **RecordResourceConfig.response_handlers,
    }

    error_handlers = {
        **RecordResourceConfig.error_handlers,
        RequestLockedError: create_error_handler(
            lambda e: HTTPJSONException(
                code=403,
                description=e.description,
            )
        ),
        RequestEventPermissionError: create_error_handler(
            lambda e: HTTPJSONException(
                code=403,
                description=e.description,
            )
        ),
        NestedChildrenNotAllowedError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=str(e),
            )
        ),
        ChildrenNotSupportedError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=str(e),
            )
        ),
    }
