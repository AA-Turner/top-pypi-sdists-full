# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2026 Northwestern University.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utility for rendering URI template links."""

import copy

from invenio_records_resources.services import EndpointLink


class RequestEndpointLink(EndpointLink):
    """Shortcut for writing request links."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        # make sure `params` argument contains "id"
        params = kwargs.get("params", [])
        kwargs["params"] = list(set(params) | {"id"})
        super().__init__(*args, **kwargs)

    @staticmethod
    def vars(record, vars):
        """Update vars used to expand the link."""
        vars.update({"id": record.id})


class RequestTypeDependentEndpointLink(EndpointLink):
    """Class that dynamically delegates to EndpointLink on RequestType's.

    The Requests API (/requests/...) needs to return links that sometimes
    depend on the type of Request. RequestTypeDependentEndpointLink allows that
    by delegating the link to be rendered to one defined in the RequestType
    (where such responsibility should reside) under
    `links_item = {<key>: ...}`.

    RequestTypeDependentEndpointLink guarantees that the EndpointLink
    defined in the RequestType will have "request", "request_type", and
    "request_event" keys in the `vars` dict. "request_event" may be None
    but the key is guaranteed to exist. This provides all the information
    that a RequestType can legitimately require to build EndpointLinks.
    """

    def __init__(
        self,
        key,
        request_retriever=lambda obj, vars: None,
        request_type_retriever=lambda obj, vars: None,
        request_event_retriever=lambda obj, vars: None,
        anchor=lambda obj, vars: None,
    ):
        """Constructor."""
        self._key = key
        self._request_retriever = request_retriever
        self._request_type_retriever = request_type_retriever
        self._request_event_retriever = request_event_retriever
        self._anchor_func = anchor

    def _get_uniform_context(self, obj, context):
        """Fill `context` with retrieved values.

        This is what makes it possible to use
        RequestTypeDependentEndpointLink from a Request— or RequestEvent—
        Service as it sets values in keys "request", "request_type",
        "request_event" that an EndpointLink defined on a RequestType can
        and should rely on.
        """
        ctx = copy.deepcopy(context)
        ctx["request"] = self._request_retriever(obj, ctx)
        ctx["request_type"] = self._request_type_retriever(obj, ctx)
        ctx["request_event"] = self._request_event_retriever(obj, ctx)
        return ctx

    def _retrieve_endpoint_link(self, obj, context):
        """Generate EndpointLink used under the hood.

        Requires _get_uniform_context to have been called to generate
        context.
        """
        # For when an EndpointLink can't be found
        no_op_link = EndpointLink("", when=lambda obj, vars: False)

        # Retrieval
        request_type = context["request_type"]
        if not request_type:
            return no_op_link
        links_item_of_type = getattr(request_type, "links_item", {})
        endpoint_link = links_item_of_type.get(self._key, no_op_link)
        return endpoint_link

    def should_render(self, obj, context):
        """Determine if the link should be rendered."""
        ctx = self._get_uniform_context(obj, context)
        endpoint_link = self._retrieve_endpoint_link(obj, ctx)
        return endpoint_link.should_render(obj, ctx)

    def expand(self, obj, context):
        """Expand/render the endpoint defined on the RequestType."""
        ctx = self._get_uniform_context(obj, context)
        endpoint_link = self._retrieve_endpoint_link(obj, ctx)
        if hasattr(endpoint_link, "set_anchor"):
            endpoint_link.set_anchor(self._anchor_func)
        return endpoint_link.expand(obj, ctx)


class RequestListOfCommentsEndpointLink(EndpointLink):
    """Render links for a Request's Comments (Events).

    Note that the RequestCommentsResource uses RequestEventsService.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        params = kwargs.get("params", [])
        kwargs["params"] = list(set(params) | {"request_id"})
        super().__init__(*args, **kwargs)

    @staticmethod
    def vars(record, vars):
        """Update vars used to expand the link."""
        vars.update({"request_id": record.id})


class RequestSingleCommentEndpointLink(EndpointLink):
    """Render links for a Request's Comment (Event)."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        params = kwargs.get("params", [])
        kwargs["params"] = list(set(params) | {"request_id", "comment_id"})
        super().__init__(*args, **kwargs)

    @staticmethod
    def vars(obj, vars):
        """Update vars used to expand the link."""
        vars.update({"request_id": obj.request_id, "comment_id": obj.id})


class ActionsEndpointLinks:
    """Renders action links.

    This is EndpointLink-input-interface compliant, but renders a dict of
    links. That's why we don't inherit from it directly.
    """

    def __init__(self, endpoint_link):
        """Constructor."""
        self._endpoint_link = endpoint_link

    def should_render(self, obj, context):
        """Always renders to keep with previous/existing interface.

        Previous interface will render `"actions": {}` so we always want to
        at least render {}.
        """
        return True

    def expand(self, obj, context):
        """Expand the endpoints.

        :param obj: Request
        :param context: dict of context data
        """
        links = {}
        request = obj

        for action in request.type.available_actions:
            if action in [request.type.create_action, request.type.delete_action]:
                continue
            ctx = context.copy()
            ctx["action"] = action
            if self._endpoint_link.should_render(request, ctx):
                links[action] = self._endpoint_link.expand(request, ctx)

        return links
