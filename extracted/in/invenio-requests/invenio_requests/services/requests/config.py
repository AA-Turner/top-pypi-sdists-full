# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021-2026 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Requests service configuration."""

from invenio_records_resources.services import (
    RecordServiceConfig,
    SearchOptions,
    pagination_endpoint_links,
)
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfig,
    FromConfigSearchOptions,
    SearchOptionsMixin,
)

from invenio_requests.services.requests import facets

from ...customizations import RequestActions
from ...records.api import Request
from ..links import (
    ActionsEndpointLinks,
    RequestEndpointLink,
    RequestListOfCommentsEndpointLink,
    RequestTypeDependentEndpointLink,
)
from ..permissions import PermissionPolicy
from .components import (
    EntityReferencesComponent,
    RequestDataComponent,
    RequestLockComponent,
    RequestNumberComponent,
    RequestPayloadComponent,
    RequestReviewersComponent,
)
from .params import IsOpenParam, ReferenceFilterParam, SharedOrMyRequestsParam
from .results import RequestItem, RequestList


def _is_action_available(request, context):
    """Check if the given action is available on the request."""
    action = context.get("action")
    identity = context.get("identity")
    permission_policy_cls = context.get("permission_policy_cls")
    permission = permission_policy_cls(f"action_{action}", request=request)
    return RequestActions.can_execute(request, action) and permission.allows(identity)


class RequestSearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options."""

    params_interpreters_cls = SearchOptions.params_interpreters_cls + [
        ReferenceFilterParam.factory(param="created_by", field="created_by"),
        ReferenceFilterParam.factory(param="receiver", field="receiver"),
        ReferenceFilterParam.factory(param="topic", field="topic"),
        IsOpenParam.factory("is_open"),
    ]

    facets = {
        "type": facets.type,
        "status": facets.status,
    }


class UserRequestSearchOptions(RequestSearchOptions):
    """User request search options."""

    params_interpreters_cls = RequestSearchOptions.params_interpreters_cls + [
        SharedOrMyRequestsParam,
    ]


class RequestsServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Requests service configuration."""

    service_id = "requests"

    # common configuration
    permission_policy_cls = FromConfig(
        "REQUESTS_PERMISSION_POLICY", default=PermissionPolicy
    )
    result_item_cls = RequestItem
    result_list_cls = RequestList
    search = FromConfigSearchOptions(
        config_key="REQUESTS_SEARCH",
        sort_key="REQUESTS_SORT_OPTIONS",
        facet_key="REQUESTS_FACETS",
        search_option_cls=RequestSearchOptions,
    )

    # user requests search configuration
    search_user_requests = FromConfigSearchOptions(
        config_key="REQUESTS_SEARCH",
        sort_key="REQUESTS_SORT_OPTIONS",
        facet_key="REQUESTS_FACETS",
        search_option_cls=UserRequestSearchOptions,
    )

    # request-specific configuration
    record_cls = Request  # needed for model queries
    schema = None  # stored in the API classes, for customization
    indexer_queue_name = "requests"
    index_dumper = None

    # links configuration
    links_item = {
        "self": RequestEndpointLink("requests.read"),
        "self_html": RequestTypeDependentEndpointLink(
            key="self_html",
            request_retriever=lambda obj, vars: obj,
            request_type_retriever=lambda obj, vars: obj.type,
        ),
        # Note that `request_events` is the name of the blueprint for
        # the RequestCommentsResource actually.
        "comments": RequestListOfCommentsEndpointLink("request_events.create"),
        "timeline": RequestListOfCommentsEndpointLink("request_events.search"),
        "timeline_focused": RequestListOfCommentsEndpointLink(
            "request_events.focused_list"
        ),
        "lock": RequestEndpointLink("requests.lock_request"),
        "unlock": RequestEndpointLink("requests.unlock_request"),
        "actions": ActionsEndpointLinks(
            RequestEndpointLink(
                "requests.execute_action",
                # "id" would have been added by RequestEndpointLink but
                # it's more explicit this way
                params=["id", "action"],
                when=_is_action_available,
            )
        ),
    }
    links_search = pagination_endpoint_links("requests.search")
    links_user_requests_search = pagination_endpoint_links(
        "requests.search_user_requests"
    )

    payload_schema_cls = None

    # TODO: discuss conflict between this and custom request service.
    #  Does it create issues?
    components = FromConfig(
        "REQUESTS_SERVICE_COMPONENTS",
        default=[
            # Order of components is important!
            RequestPayloadComponent,
            RequestDataComponent,
            RequestReviewersComponent,
            EntityReferencesComponent,
            RequestNumberComponent,
            RequestLockComponent,
        ],
    )
