# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 CERN.
# Copyright (C) 2021-2022 Northwestern University.
# Copyright (C) 2021-2022 TU Wien.
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2026 CESNET z.s.p.o.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""RequestEvents Service."""

import sqlalchemy.exc
from flask import current_app
from flask_principal import AnonymousIdentity
from invenio_i18n import lazy_gettext as _
from invenio_notifications.services.uow import NotificationOp
from invenio_records_resources.services import RecordService, ServiceSchemaWrapper
from invenio_records_resources.services.base.links import LinksTemplate
from invenio_records_resources.services.errors import PermissionDeniedError
from invenio_records_resources.services.records.params import PaginationParam
from invenio_records_resources.services.uow import (
    RecordCommitOp,
    RecordIndexOp,
    unit_of_work,
)
from invenio_search.engine import dsl

from invenio_requests.customizations import CommentEventType
from invenio_requests.customizations.event_types import LogEventType
from invenio_requests.proxies import current_requests_service as requests_service
from invenio_requests.services.results import EntityResolverExpandableField

from ...errors import (
    NestedChildrenNotAllowedError,
    RequestEventPermissionError,
    RequestLockedError,
)
from ...records.api import RequestEventFormat
from ...resolvers.registry import ResolverRegistry


class RequestEventsService(RecordService):
    """Request Events service."""

    def _wrap_schema(self, schema):
        """Wrap schema."""
        return ServiceSchemaWrapper(self, schema)

    @property
    def expandable_fields(self):
        """Get expandable fields for request events.

        Includes:
        - created_by: User or email who created the event

        Note: payload.files: File attachments in comment events are resolved in the result class.
        """
        return [EntityResolverExpandableField("created_by")]

    def links_tpl_factory(self, links, **context):
        """Include context information in the link template.

        This way, the link URLs can be contextualised depending e.g. on the type of the event's
        parent request.
        """
        return LinksTemplate(links, context=context)

    @unit_of_work()
    def create(
        self,
        identity,
        request_id,
        data,
        event_type,
        uow=None,
        expand=False,
        notify=True,
        parent_id=None,
        **kwargs,
    ):
        """Create a request event (top-level or reply).

        :param request_id: Identifier of the request (data-layer id).
        :param identity: Identity of user creating the event.
        :param dict data: Input data according to the data schema.
        :param event_type: The type of event to create.
        :param parent_id: Optional parent event ID for replies.
        """
        request = self._get_request(request_id)
        self.require_permission(
            identity,
            "read",
            request=request,
            data=data,
            event_type=event_type,
            notify=notify,
            **kwargs,
        )
        try:
            # If the event is a log, we don't check for permissions to not block logs creation
            if event_type.type_id != LogEventType.type_id:
                # Check permission based on whether this is a reply or top-level comment
                permission = "reply_comment" if parent_id else "create_comment"
                self.require_permission(
                    identity,
                    permission,
                    request=request,
                    data=data,
                    event_type=event_type,
                    notify=notify,
                    **kwargs,
                )
        except PermissionDeniedError:
            if current_app.config.get(
                "REQUESTS_LOCKING_ENABLED", False
            ) and request.get("is_locked", False):
                raise RequestLockedError(
                    description=_("Commenting is now locked for this conversation.")
                )
            else:
                raise RequestEventPermissionError(
                    description=_(
                        "You do not have permission to comment on this conversation."
                    )
                )

        # Validate that nested children (reply to reply) are not allowed
        if parent_id is not None:
            parent_event = self._get_event(parent_id)
            if parent_event.parent_id is not None:
                raise NestedChildrenNotAllowedError()

        # Validate data (if there are errors, .load() raises)
        schema = self._wrap_schema(event_type.marshmallow_schema())

        data, errors = schema.load(
            data,
            context={"identity": identity},
        )

        event = self.record_cls.create(
            {},
            request=request.model,
            request_id=str(request.id),
            type=event_type,
        )
        event.update(data)
        event.created_by = self._get_creator(identity, request=request)

        # Set parent_id for replies
        if parent_id is not None:
            event.parent_id = parent_id

        # Run components
        self.run_components(
            "create",
            identity,
            data=data,
            event=event,
            errors=errors,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(event, indexer=self.indexer))

        # Reindex the request to update events-related computed fields
        # NOTE: We're not reindexing if the event is a deletion log event, since the
        # associated request will anyways be deleted from the index. Ideally, instead of
        # checking this here, the Unit of Work, should be able to optimize away the
        # unecessary reindexing operations (i.e. if there's a RecordDeleteOp registered,
        # all previous RecordIndexOps for the same record should be ignored).
        is_delete_event = (
            isinstance(event_type, LogEventType) or event_type is LogEventType
        ) and (data.get("payload", {}).get("event") == "deleted")
        if not is_delete_event:
            uow.register(RecordIndexOp(request, indexer=requests_service.indexer))

        if notify and event_type is CommentEventType:
            # Use different notification builder for replies vs top-level comments
            if parent_id:
                builder = request.type.reply_notification_builder
            else:
                builder = request.type.comment_notification_builder

            uow.register(NotificationOp(builder.build(request, event)))

        return self.result_item(
            self,
            identity,
            event,
            schema=schema,
            links_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    def read(self, identity, id_, expand=False, **kwargs):
        """Retrieve a record."""
        event = self._get_event(id_)
        request = self._get_request(event.request_id)

        self.require_permission(identity, "read", request=request, **kwargs)

        return self.result_item(
            self,
            identity,
            event,
            schema=self._wrap_schema(event.type.marshmallow_schema()),
            links_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    @unit_of_work()
    def update(
        self, identity, id_, data, revision_id=None, uow=None, expand=False, **kwargs
    ):
        """Update a comment (only comments can be updated)."""
        event = self._get_event(id_)
        request = self._get_request(event.request.id)
        try:
            self.require_permission(
                identity,
                "update_comment",
                request=request,
                event=event,
                data=data,
                **kwargs,
            )
        except PermissionDeniedError:
            if current_app.config.get(
                "REQUESTS_LOCKING_ENABLED", False
            ) and request.get("is_locked", False):
                raise RequestLockedError(
                    description=_("Updating is now locked for this comment.")
                )
            else:
                raise RequestEventPermissionError(
                    description=_("You do not have permission to update this comment.")
                )
        self.check_revision_id(event, revision_id)

        if event.type != CommentEventType:
            raise RequestEventPermissionError(
                description=_("You cannot update this event.")
            )

        schema = self._wrap_schema(event.type.marshmallow_schema())
        data, errors = schema.load(
            data,
            context=dict(
                identity=identity, record=event, request=request, event_type=event.type
            ),
        )

        event["payload"]["content"] = data["payload"]["content"]
        event["payload"]["format"] = data["payload"]["format"]

        # Run components
        self.run_components(
            "update_comment",
            identity,
            data=data,
            event=event,
            request=request,
            uow=uow,
        )

        # Updating the list of files after running components,
        # so that RequestCommentFileCleanupComponent can compare the list of files.
        if "files" in data["payload"]:
            event["payload"]["files"] = data["payload"]["files"]

        # Persist record (DB and index)
        uow.register(RecordCommitOp(event, indexer=self.indexer))

        # Reindex the request to update events-related computed fields
        uow.register(RecordIndexOp(request, indexer=requests_service.indexer))

        return self.result_item(
            self,
            identity,
            event,
            schema=schema,
            links_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    @unit_of_work()
    def delete(self, identity, id_, revision_id=None, uow=None, **kwargs):
        """Delete a comment (only comments can be deleted)."""
        event = self._get_event(id_)
        request_id = event.request_id
        request = self._get_request(request_id)

        # Permissions
        self.require_permission(
            identity, "delete_comment", request=request, event=event, **kwargs
        )
        self.check_revision_id(event, revision_id)

        if event.type != CommentEventType:
            raise RequestEventPermissionError(
                description=_("You cannot delete this event.")
            )

        # update the event for the deleted comment with a LogEvent
        event.type = LogEventType
        schema = self._wrap_schema(event.type.marshmallow_schema())
        data = dict(
            payload=dict(
                event="comment_deleted",
                content="comment was deleted",
                format=RequestEventFormat.HTML.value,
            )
        )
        data, _errors = schema.load(
            data,
            context=dict(identity=identity, record=event, event_type=event.type),
        )

        for data_key, data_value in data["payload"].items():
            if data_key != "files":
                event["payload"][data_key] = data_value

        # Run components
        self.run_components(
            "delete_comment",
            identity,
            data=data,
            event=event,
            request=request,
            uow=uow,
        )

        # Updating the list of files after running components,
        # so that RequestCommentFileCleanupComponent can get the list of files.
        if "files" in data["payload"]:
            event["payload"]["files"] = data["payload"]["files"]

        # Commit the updated comment
        uow.register(RecordCommitOp(event, indexer=self.indexer))

        # Reindex the request to update events-related computed fields
        uow.register(RecordIndexOp(request, indexer=requests_service.indexer))

        return True

    def search(
        self,
        identity,
        request_id,
        params=None,
        search_preference=None,
        preview_size=None,
        **kwargs,
    ):
        """Search for events (timeline) for a given request.

        Returns all top-level events (parent comments without parent_id) for the request.
        For parents that have children, includes a preview via inner_hits using
        OpenSearch join relationships.

        """
        params = params or {}
        params.setdefault("sort", "oldest")
        expand = kwargs.pop("expand", False)

        # Permissions - guarded by the request's can_read.
        request = self._get_request(request_id)
        self.require_permission(
            identity, "read", request=request, params=params, **kwargs
        )

        # Build query for top-level events (parents) with optional children preview
        # Uses join relationships to include children via inner_hits when they exist
        search = self._search(
            "search",
            identity,
            params,
            search_preference,
            permission_action="unused",
            **kwargs,
        )

        # Query structure:
        # - must: filter to this request
        # - must_not: exclude children (events with parent_id)
        # - should: optionally add children preview via has_child + inner_hits
        search = search.query(
            "bool",
            must=[
                dsl.Q("term", request_id=str(request.id)),
            ],
            must_not=[
                dsl.Q("exists", field="parent_id"),  # Exclude replies
            ],
            should=[self._timeline_query_child_preview(preview_size)],
            minimum_should_match=0,  # Make should clause optional to return parents without children
        )

        # Execute search
        search_result = search.execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=self.links_tpl_factory(
                self.config.links_search, request_id=str(request.id), args=params
            ),
            links_item_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    def focused_list(
        self,
        identity,
        request_id,
        focus_event_id,
        page_size,
        expand=False,
        search_preference=None,
        preview_size=None,
    ):
        """Return a page of results focused on a given event, or the first page if the event is not found.

        Only searches parent comments (excludes child comments/replies).
        If the focused event is a reply (child comment), the page containing its parent will be returned.
        """
        # Permissions - guarded by the request's can_read.
        request = self._get_request(request_id)
        self.require_permission(identity, "read", request=request)

        # If a specific event ID is requested, we need to work out the corresponding page number.
        focus_event = None
        try:
            focus_event = self._get_event(focus_event_id)
            # Make sure the event belongs to the request, otherwise the `require_permission` call above
            # might not be valid for this particular event.
            if str(focus_event.request_id) != str(request_id):
                raise PermissionDeniedError()

            if focus_event.parent_id is not None:
                focus_event = self._get_event(focus_event.parent_id)
        except sqlalchemy.exc.NoResultFound:
            # Silently ignore
            pass

        params = {"sort": "oldest", "size": page_size}

        # Build filter to only include parent comments (exclude child comments)
        parent_filter = dsl.Q(
            "bool",
            must=[dsl.Q("term", request_id=str(request.id))],
            must_not=[dsl.Q("exists", field="parent_id")],  # Exclude replies
            should=[self._timeline_query_child_preview(preview_size)],
            minimum_should_match=0,
        )
        search = self._search(
            "search",
            identity,
            params,
            search_preference,
            permission_action="unused",
            extra_filter=parent_filter,
            versioning=False,
        )

        page = 1
        if focus_event is not None:
            num_older_than_event = search.filter(
                "range", created={"lt": focus_event.created}
            ).count()
            page = num_older_than_event // page_size + 1

        # Re run the pagination param interpreter to update the search with the new page number
        params.update(page=page)
        search = PaginationParam(self.config.search).apply(identity, search, params)

        # We deactivated versioning before (it doesn't apply for count queries) so we need to re-enable it.
        search_result = search.params(version=True).execute()
        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=self.links_tpl_factory(
                self.config.links_search, request_id=str(request.id), args=params
            ),
            links_item_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    def scan(
        self,
        identity,
        request_id,
        params=None,
        search_preference=None,
        expand=False,
        extra_filter=None,
        **kwargs,
    ):
        """Scan for events matching the querystring."""
        request = self._get_request(request_id)
        self.require_permission(identity, "read", request=request)

        # Prepare and execute the search as scan()
        params = params or {}
        search_result = self._search(
            "scan",
            identity,
            params,
            search_preference,
            extra_filter=extra_filter,
            **kwargs,
        ).scan()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=self.links_tpl_factory(
                self.config.links_search, request_id=str(request.id), args=params
            ),
            links_item_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    def get_comment_replies(
        self, identity, parent_id, params=None, search_preference=None, **kwargs
    ):
        """Get paginated replies for a specific comment.

        :param identity: Identity of user.
        :param parent_id: ID of the parent comment.
        :param params: Query parameters (page, size, sort, etc.).
        :param search_preference: Search preference.
        :returns: Paginated list of reply events.
        """
        params = params or {}
        params.setdefault("sort", "oldest")

        expand = kwargs.pop("expand", False)

        # Get the parent event to verify permissions and get request_id
        parent_event = self._get_event(parent_id)
        request = self._get_request(parent_event.request_id)

        # Permissions - guarded by the request's can_read
        self.require_permission(identity, "read", request=request)

        # Prepare and execute the search for children
        replies_filter = dsl.Q(
            "bool",
            must=[
                dsl.Q("term", request_id=str(request.id)),
                dsl.Q("term", parent_id=parent_id),
            ],
        )
        search = self._search(
            "search",
            identity,
            params,
            search_preference,
            permission_action="unused",
            extra_filter=replies_filter,
            **kwargs,
        )

        search_result = search.execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=self.links_tpl_factory(
                self.config.links_replies,
                request_id=str(request.id),
                comment_id=parent_id,
                args=params,
            ),
            links_item_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    def focused_reply_list(
        self,
        identity,
        parent_id,
        focus_reply_event_id,
        page_size,
        expand=False,
        search_preference=None,
        params=None,
    ):
        """Return a page of results focused on a given reply event, or the first page if the event is not found.

        Only searches reply comments (excludes parents comments/replies).
        """
        parent_event = self._get_event(parent_id)
        request = self._get_request(parent_event.request_id)
        # Permissions - guarded by the request's can_read.
        self.require_permission(identity, "read", request=request)

        # If a specific event ID is requested, we need to work out the corresponding page number.
        focus_event = None
        try:
            focus_event = self._get_event(focus_reply_event_id)
            # Make sure the event belongs to the request, otherwise the `require_permission` call above
            # might not be valid for this particular event.
            if str(focus_event.request_id) != str(parent_event.request_id):
                raise PermissionDeniedError()

            if str(focus_event.parent_id) != str(parent_id):
                raise Exception("Focus event must be a reply to the parent.")

            if focus_event.parent_id is None:
                raise Exception("Cannot focus on non-reply event.")
        except sqlalchemy.exc.NoResultFound:
            # Silently ignore
            pass

        params = params or {}
        params.setdefault("sort", "newest")
        params.setdefault("size", page_size)

        replies_filter = dsl.Q(
            "bool",
            must=[
                dsl.Q("term", request_id=str(request.id)),
                dsl.Q("term", parent_id=parent_id),
            ],
        )
        search = self._search(
            "search",
            identity,
            params,
            search_preference,
            permission_action="unused",
            extra_filter=replies_filter,
            versioning=False,
        )

        page = 1
        if focus_event is not None:
            num_newer_than_event = search.filter(
                "range", created={"gt": focus_event.created}
            ).count()
            page = num_newer_than_event // page_size + 1

        # Re run the pagination param interpreter to update the search with the new page number
        params.update(page=page)
        search = PaginationParam(self.config.search).apply(identity, search, params)

        # We deactivated versioning before (it doesn't apply for count queries) so we need to re-enable it.
        search_result = search.params(version=True).execute()
        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=self.links_tpl_factory(
                self.config.links_replies,
                request_id=str(request.id),
                comment_id=parent_id,
                args=params,
            ),
            links_item_tpl=self.links_tpl_factory(
                self.config.links_item, request=request, request_type=request.type
            ),
            expandable_fields=self.expandable_fields,
            expand=expand,
            request=request,
        )

    # Utilities
    @property
    def request_cls(self):
        """Get associated request class."""
        return self.config.request_cls

    def _get_request(self, request_id):
        """Get associated request."""
        # If it's already a request, return it
        if isinstance(request_id, self.request_cls):
            return request_id
        return self.request_cls.get_record(request_id)

    def _get_event(self, event_id, with_deleted=True):
        """Get associated event_id."""
        return self.record_cls.get_record(event_id, with_deleted=with_deleted)

    def _get_creator(self, identity, request=None):
        """Get the creator dict from the identity."""
        creator = None
        if isinstance(identity, AnonymousIdentity):
            # not ideal - assumes that comment is created by same person
            # who created a request - solution for guest users
            creator = request["created_by"]

        referenced_creator = (
            ResolverRegistry.reference_entity(creator, raise_=True)
            if creator is not None
            else ResolverRegistry.reference_identity(identity)
        )
        return referenced_creator

    def _timeline_query_child_preview(self, preview_size):
        """Return an OpenSearch query to include a size-limited preview of replies to a parent comment."""
        if preview_size is None:
            preview_size = current_app.config["REQUESTS_COMMENT_PREVIEW_LIMIT"]
        return dsl.Q(
            "has_child",
            type="child",
            query=dsl.Q("match_all"),
            score_mode="none",
            inner_hits={
                "name": "replies_preview",
                "size": preview_size,
                "sort": [{"created": "desc"}],
            },
        )
