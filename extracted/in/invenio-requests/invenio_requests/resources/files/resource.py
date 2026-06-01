# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""RequestFiles Resource."""

from flask import g
from flask_resources import resource_requestctx, response_handler, route
from invenio_records_resources.resources import RecordResource
from invenio_records_resources.resources.files.resource import request_stream
from invenio_records_resources.resources.records.resource import (
    request_extra_args,
    request_headers,
    request_view_args,
)


#
# Resource
#
class RequestFilesResource(RecordResource):
    """Resource for Request files."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("PUT", routes["create"], self.create),
            route("DELETE", routes["item"], self.delete),
            route("GET", routes["item_content"], self.read),
        ]

    @request_extra_args
    @request_headers
    @request_view_args
    @request_stream
    @response_handler()
    def create(self):
        """Create a file."""
        item = self.service.create_file(
            identity=g.identity,
            id_=resource_requestctx.view_args["id"],
            key=resource_requestctx.view_args["key"],
            stream=resource_requestctx.data["request_stream"],
            content_length=resource_requestctx.data["request_content_length"],
        )
        return item.to_dict(), 200

    @request_view_args
    def delete(self):
        """Delete a file."""
        self.service.delete_file(
            identity=g.identity,
            id_=resource_requestctx.view_args["id"],
            file_key=resource_requestctx.view_args["key"],
        )
        return "", 204

    @request_view_args
    def read(self):
        """Read a file."""
        file = self.service.read_file(
            identity=g.identity,
            id_=resource_requestctx.view_args["id"],
            file_key=resource_requestctx.view_args["key"],
        )
        return file.send_file(as_attachment=True, restricted=True), 200
