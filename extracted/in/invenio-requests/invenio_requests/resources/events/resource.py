# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 CERN.
# Copyright (C) 2021-2022 Northwestern University.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Requests resource."""

from copy import deepcopy

from flask import g
from flask_resources import (
    from_conf,
    request_body_parser,
    request_parser,
    resource_requestctx,
    response_handler,
    route,
)
from invenio_records_resources.resources import RecordResource
from invenio_records_resources.resources.records.resource import (
    request_extra_args,
    request_headers,
)
from invenio_records_resources.resources.records.utils import search_preference

from ...customizations.event_types import CommentEventType


#
# Resource
#
class RequestCommentsResource(RecordResource):
    """Resource for Request comments for now."""

    list_view_args_parser = request_parser(
        from_conf("request_list_view_args"), location="view_args"
    )
    item_view_args_parser = request_parser(
        from_conf("request_item_view_args"), location="view_args"
    )
    search_args_parser = request_parser(
        from_conf("request_search_args"), location="args"
    )
    data_parser = request_body_parser(
        parsers=from_conf("request_body_parsers"),
        default_content_type=from_conf("default_content_type"),
    )

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        # Assignment of routes should be part of the
        # Config class
        routes = self.config.routes
        return [
            route("POST", routes["list"], self.create),
            route("POST", routes["reply"], self.reply),
            route("GET", routes["item"], self.read),
            route("PUT", routes["item"], self.update),
            route("DELETE", routes["item"], self.delete),
            route("GET", routes["timeline"], self.search),
            route("GET", routes["timeline_focused"], self.focused_list),
            route("GET", routes["replies"], self.get_replies),
            route("GET", routes["replies_focused"], self.focused_replies),
        ]

    @list_view_args_parser
    @request_extra_args
    @data_parser
    @response_handler()
    def create(self):
        """Create a top-level comment (no parent)."""
        data = deepcopy(resource_requestctx.data) if resource_requestctx.data else {}
        item = self.service.create(
            identity=g.identity,
            request_id=resource_requestctx.view_args["request_id"],
            data=data,
            event_type=CommentEventType,
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 201

    @item_view_args_parser
    @request_extra_args
    @data_parser
    @response_handler()
    def reply(self):
        """Create a reply to a comment."""
        data = deepcopy(resource_requestctx.data) if resource_requestctx.data else {}
        # Extract parent_id from the route (comment_id in the URL)
        parent_id = resource_requestctx.view_args["comment_id"]
        item = self.service.create(
            identity=g.identity,
            request_id=resource_requestctx.view_args["request_id"],
            parent_id=parent_id,
            data=data,
            event_type=CommentEventType,
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 201

    @item_view_args_parser
    @request_extra_args
    @response_handler()
    def read(self):
        """Read an event.

        Because each event has a unique id, we can disregard the request_id
        for now.
        """
        item = self.service.read(
            identity=g.identity,
            id_=resource_requestctx.view_args["comment_id"],
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 200

    @item_view_args_parser
    @request_extra_args
    @request_headers
    @data_parser
    @response_handler()
    def update(self):
        """Update a comment."""
        item = self.service.update(
            identity=g.identity,
            id_=resource_requestctx.view_args["comment_id"],
            data=resource_requestctx.data,
            revision_id=resource_requestctx.headers.get("if_match"),
            expand=resource_requestctx.args.get("expand", False),
        )
        return item.to_dict(), 200

    @item_view_args_parser
    @request_headers
    def delete(self):
        """Delete a comment."""
        self.service.delete(
            identity=g.identity,
            id_=resource_requestctx.view_args["comment_id"],
            revision_id=resource_requestctx.headers.get("if_match"),
        )
        return "", 204

    @list_view_args_parser
    @request_extra_args
    @search_args_parser
    @response_handler(many=True)
    def search(self):
        """Perform a search over EVENTS.

        Its primary purpose is as a batch read of events i.e. the timeline.
        """
        hits = self.service.search(
            identity=g.identity,
            request_id=resource_requestctx.view_args["request_id"],
            params=resource_requestctx.args,
            search_preference=search_preference(),
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200

    @list_view_args_parser
    @request_extra_args
    @search_args_parser
    @response_handler(many=True)
    def focused_list(self):
        """List the page containing the event with ID focus_event_id, or the first page of results if this is not found."""
        hits = self.service.focused_list(
            identity=g.identity,
            request_id=resource_requestctx.view_args["request_id"],
            focus_event_id=resource_requestctx.args.get("focus_event_id"),
            page_size=resource_requestctx.args.get("size"),
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200

    @item_view_args_parser
    @request_extra_args
    @search_args_parser
    @response_handler(many=True)
    def get_replies(self):
        """Get paginated replies for a specific comment."""
        hits = self.service.get_comment_replies(
            identity=g.identity,
            parent_id=resource_requestctx.view_args["comment_id"],
            params=resource_requestctx.args,
            search_preference=search_preference(),
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200

    @list_view_args_parser
    @request_extra_args
    @search_args_parser
    @response_handler(many=True)
    def focused_replies(self):
        """List the reply page containing the event with ID focus_event_id, or the first page of results if this is not found."""
        hits = self.service.focused_reply_list(
            identity=g.identity,
            parent_id=resource_requestctx.view_args["comment_id"],
            focus_reply_event_id=resource_requestctx.args.get("focus_event_id"),
            page_size=resource_requestctx.args.get("size"),
            expand=resource_requestctx.args.get("expand", False),
            params=resource_requestctx.args,
        )
        return hits.to_dict(), 200
