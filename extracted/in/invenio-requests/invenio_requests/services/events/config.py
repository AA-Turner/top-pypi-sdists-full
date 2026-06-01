# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021-2025 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Request Events Service Config."""

from uuid import UUID

from invenio_indexer.api import RecordIndexer
from invenio_records_resources.services import (
    RecordServiceConfig,
    ServiceSchemaWrapper,
    pagination_endpoint_links,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig
from invenio_records_resources.services.records.results import (
    RecordItem,
    RecordList,
)

from ...proxies import (
    current_request_files_service,
)
from ...records.api import Request, RequestEvent, RequestFile
from ...services.links import (
    RequestSingleCommentEndpointLink,
    RequestTypeDependentEndpointLink,
)
from ..permissions import PermissionPolicy
from ..schemas import RequestEventSchema


def _expand_files_for_projections(projections, request, identity):
    """Expand file details for multiple projections in a single batch query.

    :param projections: List of projection dictionaries
    :param request: The request object for context
    :param identity: The identity for link generation
    """
    if not projections or not request:
        return

    request_id = request.id

    # Collect all file IDs from all projections
    all_file_ids = set()
    for projection in projections:
        payload_files = projection.get("payload", {}).get("files", [])
        for file_obj in payload_files:
            if "file_id" in file_obj:
                all_file_ids.add(UUID(file_obj["file_id"]))

    # Early return if no files to expand
    if not all_file_ids:
        return

    # Single batch query to fetch all files
    request_files = RequestFile.list_by_file_ids(request_id, list(all_file_ids))
    request_files_by_file_id = {
        request_file.file.file_id: request_file for request_file in request_files
    }

    # Create link template using the files service factory
    file_links_tpl = current_request_files_service.links_tpl_factory(
        current_request_files_service.config.links_item,
        request_type=str(request.type),
    )

    # Expand files in each projection
    for projection in projections:
        payload_files = projection.get("payload", {}).get("files", [])

        # Nothing to expand if no files
        if not payload_files:
            continue

        # Build expanded files list
        expanded_files = []
        for payload_file in payload_files:
            if "file_id" not in payload_file:
                continue

            payload_file_uuid = UUID(payload_file["file_id"])
            file_details = request_files_by_file_id.get(payload_file_uuid)

            # Only expand if the file is found in the database
            if file_details:
                expanded_files.append(
                    {
                        "file_id": str(file_details.file.file_id),
                        "key": file_details.file.key,
                        "original_filename": file_details.model.data[
                            "original_filename"
                        ],
                        "size": file_details.file.size,
                        "mimetype": file_details.file.mimetype,
                        "created": file_details.file.created,
                        # Use link template to expand links
                        "links": file_links_tpl.expand(identity, file_details),
                    }
                )

        # Add expanded files to the projection's expanded field
        if expanded_files:
            if "expanded" not in projection:
                projection["expanded"] = {}
            projection["expanded"]["files"] = expanded_files


class RequestEventItem(RecordItem):
    """RequestEvent result item."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self._request = request

    @property
    def id(self):
        """Id property."""
        return self._record.id

    @property
    def data(self):
        """Property to get the record projection with request in context."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context=dict(
                identity=self._identity,
                record=self._record,
                request=self._request,  # Need to pass the request to the schema to get the permissions to check if locked
            ),
        )
        if self._links_tpl:
            self._data["links"] = self.links

        if self._nested_links_item:
            for link in self._nested_links_item:
                link.expand(self._identity, self._record, self._data)

        if self._expand and self._fields_resolver:
            self._fields_resolver.resolve(self._identity, [self._data])
            fields = self._fields_resolver.expand(self._identity, self._data)
            self._data["expanded"] = fields

            # Expand file details if present
            _expand_files_for_projections([self._data], self._request, self._identity)

        return self._data


class RequestEventList(RecordList):
    """RequestEvent result item."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self._request = request

    def to_dict(self):
        """Return result as a dictionary with expanded fields for parents and children."""
        # Call parent to handle standard expansion
        res = super().to_dict()

        # Additionally expand children fields if present
        if self._expand and self._fields_resolver:
            self._expand_children_fields(res["hits"]["hits"])

            # Batch expand file details for all hits
            self._batch_expand_file_details(res["hits"]["hits"])

        return res

    def _expand_children_fields(self, hits):
        """Apply field expansion to children arrays in hits.

        :param hits: List of hit dictionaries that may contain children arrays
        """
        # Collect all children from all hits
        all_children = []
        for hit in hits:
            if "children" in hit and hit["children"]:
                all_children.extend(hit["children"])

        if all_children:
            # Batch resolve all children at once for efficiency
            self._fields_resolver.resolve(self._identity, all_children)

            # Expand each child individually
            for child in all_children:
                fields = self._fields_resolver.expand(self._identity, child)
                child["expanded"] = fields

    def _batch_expand_file_details(self, hits):
        """Batch expand file details for all hits in a single database query.

        :param hits: List of hit dictionaries that may contain payload.files
        """
        # Collect all projections (parents and children)
        all_projections = []
        for hit in hits:
            all_projections.append(hit)
            # Also include children
            all_projections.extend(hit.get("children", []))

        # Use common expansion function
        _expand_files_for_projections(all_projections, self._request, self._identity)

    @property
    def hits(self):
        """Iterator over the hits."""
        for hit in self._results:
            # Load dump
            record = self._service.record_cls.loads(hit.to_dict())

            # Project the record
            schema = ServiceSchemaWrapper(
                self._service, record.type.marshmallow_schema()
            )
            projection = schema.dump(
                record,
                context=dict(
                    identity=self._identity,
                    record=record,
                    request=self._request,  # Need to pass the request to the schema to get the permissions to check if locked
                    meta=hit.meta,
                ),
            )

            # Handle inner_hits from has_child queries (join relationship approach)
            # Initialize defaults for parents without children
            projection["children"] = []
            projection["children_count"] = 0

            if (
                hasattr(hit.meta, "inner_hits")
                and "replies_preview" in hit.meta.inner_hits
            ):
                # Extract children from inner_hits
                inner_hits_data = hit.meta.inner_hits.replies_preview.hits
                inner_children = inner_hits_data.hits
                total_children = inner_hits_data.total.value

                projection["children_count"] = total_children

                for inner_hit in inner_children:
                    # Load child record
                    child_record = self._service.record_cls.loads(
                        inner_hit["_source"].to_dict()
                    )

                    # Project child record
                    child_schema = ServiceSchemaWrapper(
                        self._service, child_record.type.marshmallow_schema()
                    )
                    child_projection = child_schema.dump(
                        child_record,
                        context=dict(
                            identity=self._identity,
                            record=child_record,
                            request=self._request,  # Need to pass the request to the schema to get the permissions to check if locked
                            meta=hit.meta,
                        ),
                    )

                    if self._links_item_tpl:
                        child_projection["links"] = self._links_item_tpl.expand(
                            self._identity, child_record
                        )

                    projection["children"].append(child_projection)

            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(
                    self._identity, record
                )

            yield projection


class ParentChildRecordIndexer(RecordIndexer):
    """Parent-Child Record Indexer placeholder."""

    def _prepare_record(self, record, index, arguments=None, **kwargs):
        """Prepare request-event data for indexing.

        Pass routing information for parent-child relationships.
        """
        data = super()._prepare_record(record, index, arguments, **kwargs)
        if hasattr(record, "parent_id") and record.parent_id:
            arguments["routing"] = str(record.parent_id)
        return data


def request_event_anchor(_, vars):
    """Generate the anchor for request events.

    This is also called for requests, so we need to return None if it isn't being called for a request event.
    """
    request_event = vars["request_event"]
    if request_event is None:
        return None

    if request_event.parent_id is not None:
        return f"commentevent-{request_event.parent_id}_{request_event.id}"
    else:
        return f"commentevent-{request_event.id}"


class RequestEventsServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Config."""

    service_id = "request_events"

    request_cls = Request
    permission_policy_cls = FromConfig(
        "REQUESTS_PERMISSION_POLICY", default=PermissionPolicy
    )
    schema = RequestEventSchema
    record_cls = RequestEvent
    result_item_cls = RequestEventItem
    result_list_cls = RequestEventList
    indexer_queue_name = "events"
    indexer_cls = ParentChildRecordIndexer

    # ResultItem configurations
    links_item = {
        # Note that `request_events` is the name of the blueprint for
        # the RequestCommentsResource actually.
        "self": RequestSingleCommentEndpointLink("request_events.read"),
        # Keeps assumption that there is no dedicated UI endpoint for
        # a RequestEvent i.e., RequestType is what determines the UI endpoint
        "self_html": RequestTypeDependentEndpointLink(
            key="self_html",
            request_retriever=lambda obj, vars: vars.get("request"),
            request_type_retriever=lambda obj, vars: vars.get("request_type"),
            # The presence of request_event_retriever
            # provides for further differentiation
            request_event_retriever=lambda obj, vars: obj,
            anchor=request_event_anchor,
        ),
        "reply": RequestSingleCommentEndpointLink(
            "request_events.reply",
            # The reply link is only shown if the request_event is top-level:
            # to send stronger signal to client that only top-level comments
            # can be replied to + no need to parse link to figure if parent or
            # current comment is targeted
            when=lambda obj, vars: obj.parent_id is None,
        ),
        "replies": RequestSingleCommentEndpointLink(
            "request_events.get_replies",
            # The replies link is only shown if the request_event is top-level
            # only case where there *can* be replies
            when=lambda obj, vars: obj.parent_id is None,
        ),
        "replies_focused": RequestSingleCommentEndpointLink(
            "request_events.focused_replies",
            when=lambda obj, vars: obj.parent_id is None,
        ),
    }

    links_search = pagination_endpoint_links(
        "request_events.search",
        params=["request_id"],
    )

    links_replies = pagination_endpoint_links(
        "request_events.get_replies",
        params=["request_id", "comment_id"],
    )

    components = FromConfig(
        "REQUESTS_EVENTS_SERVICE_COMPONENTS",
        default=[],
    )
