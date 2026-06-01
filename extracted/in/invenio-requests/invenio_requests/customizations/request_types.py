# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 TU Wien.
# Copyright (C) 2021-2024 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Base class for creating custom types of requests.

The `RequestType` classes are the most important part in the customization/extension
mechanism for custom types of requests.
TODO explain what can be done here, and how!
"""

import base32_lib as base32
import marshmallow as ma
from flask import current_app
from invenio_records_resources.services.references import (
    EntityReferenceBaseSchema,
    MultipleEntityReferenceBaseSchema,
)

from ..notifications.builders import (
    CommentRequestEventCreateNotificationBuilder,
    CommentRequestEventReplyNotificationBuilder,
)
from ..proxies import current_requests
from .actions import (
    AcceptAction,
    CancelAction,
    CreateAction,
    DeclineAction,
    DeleteAction,
    ExpireAction,
    SubmitAction,
)
from .states import RequestState


class RequestType:
    """Base class for custom request types."""

    type_id = "base-request"
    """The unique and constant identifier for this type of requests.

    Since this property is used to map generic chunks of data from the database
    (i.e. the request model entries) to their correct `RequestType`, this should
    be a globally unique value.
    By convention, this would be the name of the package in which the custom
    `RequestType` is defined as prefix, together with a suffix related to the
    `RequestType`.
    Further, it should be constant after the first release of the package
    (otherwise, requests created with the old value will no longer be able to be
    mapped to their `RequestType`).
    """

    name = "Base Request"
    """The human-readable name for this type of requests."""

    available_statuses = {
        "created": RequestState.UNDEFINED,
        "submitted": RequestState.OPEN,
        "cancelled": RequestState.CLOSED,
        "declined": RequestState.CLOSED,
        "accepted": RequestState.CLOSED,
        "expired": RequestState.CLOSED,
        "deleted": RequestState.UNDEFINED,
    }
    """Available statuses for the request.

    The keys in this dictionary is the set of available statuses, and their
    values are indicators whether this request is considered to be open, closed
    or undefined.
    """

    create_action = "create"
    """Defines the action that's able to create this request.

    This must be set to one of the available actions for the custom request type.
    """

    delete_action = "delete"
    """Defines the action that's able to create this request.

    This must be set to one of the available actions for the custom request type.
    """

    available_actions = {
        "create": CreateAction,
        "submit": SubmitAction,
        "delete": DeleteAction,
        "accept": AcceptAction,
        "decline": DeclineAction,
        "cancel": CancelAction,
        "expire": ExpireAction,
    }
    """Available actions for this Request.

    The keys are the internal identifiers for the actions, the values are
    the actual RequestAction classes (not objects).
    Whenever an action is looked up, a new object of the registered
    RequestAction class is instantiated with the current Request object as
    argument.
    """

    creator_can_be_none = True
    """Determines if the ``created_by`` reference accepts ``None``.
    In case of ``None`` the creator will be ``System``."""

    receiver_can_be_none = False
    """Determines if the ``receiver`` reference accepts ``None``."""

    topic_can_be_none = True
    """Determines if the ``topic`` reference accepts ``None``."""

    files_can_be_none = True
    """Determines if the ``files`` reference accepts ``None``."""

    allowed_creator_ref_types = ["user"]
    """A list of allowed TYPE keys for ``created_by`` reference dicts."""

    allowed_receiver_ref_types = ["user"]
    """A list of allowed TYPE keys for ``receiver`` reference dicts."""

    @classmethod
    def allowed_reviewers_ref_types(cls):
        """Return the allowed reviewers reference types."""
        if current_app.config.get("USERS_RESOURCES_GROUPS_ENABLED", False):
            return ["user", "group"]
        return ["user"]

    @classmethod
    def reviewers_can_be_none(cls):
        """Return whether reviewers can be None."""
        return current_app.config.get("REQUESTS_REVIEWERS_ENABLED", False)

    @classmethod
    def locking_enabled(cls):
        """Return whether locking is enabled."""
        return current_app.config.get("REQUESTS_LOCKING_ENABLED", False)

    allowed_topic_ref_types = []
    """A list of allowed TYPE keys for ``topic`` reference dicts."""

    resolve_topic_needs = False
    """Whether to resolve needs for the topic entity."""

    allowed_files_ref_types = ["enabled"]
    """A list of allowed TYPE keys for ``files`` reference dicts."""

    payload_schema = None
    payload_schema_cls = None
    """Schema for supported payload fields.

    Define it as a dictionary of fields mapping:

    .. code-block:: python

        payload_schema = {
            "content": fields.String(),
            # ...
        }
    """

    comment_notification_builder = CommentRequestEventCreateNotificationBuilder
    reply_notification_builder = CommentRequestEventReplyNotificationBuilder

    needs_context = None
    """The context for needs.

    This allows a request type to customize which and how needs are generated
    for a specific entity. For instance which needs are generated for a
    community entity or system entity.
    """

    links_item = {}
    """Dict of keys to EndpointLinks for the RequestType.

    This specifies how "self_html" (and potentially
    other keys) should render. Keys are "links" keys e.g. "self_html"
    (only use for now) and values are EndpointLinks. The defined EndpointLinks
    are guaranteed to have the following keys in their passed `vars`:
    - "request": the Request object
    - "request_type": the RequestType object
    - "request_event": the optional RequestEvent (the key "request_event" will
                       always be present, but it may have the value None)
    """

    @classmethod
    def entity_needs(cls, entity):
        """Generate entity needs for the given entity."""
        if entity is not None:
            return entity.get_needs(ctx=cls.needs_context)
        return []

    @classmethod
    def _create_payload_cls(cls):
        class PayloadBaseSchema(ma.Schema):
            class Meta:
                # Raise on invalid payload keys
                unknown = ma.RAISE

        cls.payload_schema_cls = PayloadBaseSchema

    @classmethod
    def _create_marshmallow_schema(cls):
        """Create a marshmallow schema for this request type."""
        # Avoid circular imports
        from invenio_requests.services.schemas import RequestSchema

        # The reference fields always need to be added
        RefBaseSchema = EntityReferenceBaseSchema
        additional_fields = {
            "created_by": ma.fields.Nested(
                RefBaseSchema.create_from_dict(cls.allowed_creator_ref_types),
                allow_none=cls.creator_can_be_none,
            ),
            "receiver": ma.fields.Nested(
                RefBaseSchema.create_from_dict(cls.allowed_receiver_ref_types),
                allow_none=cls.receiver_can_be_none,
            ),
            "topic": ma.fields.Nested(
                RefBaseSchema.create_from_dict(cls.allowed_topic_ref_types),
                allow_none=cls.topic_can_be_none,
            ),
            "files": ma.fields.Nested(
                RefBaseSchema.create_from_dict(
                    cls.allowed_files_ref_types,
                    special_fields={"enabled": ma.fields.Boolean()},
                ),
                allow_none=cls.files_can_be_none,
            ),
        }

        if cls.reviewers_can_be_none():
            # if the config is enabled, add the reviewers field to the schema
            additional_fields["reviewers"] = ma.fields.List(
                ma.fields.Nested(
                    MultipleEntityReferenceBaseSchema.create_from_dict(
                        cls.allowed_reviewers_ref_types()
                    ),
                    allow_none=cls.reviewers_can_be_none(),
                )
            )

        if cls.locking_enabled():
            # `is_locked` field would be automatically added as False on dump if not present and loaded as False if not present
            additional_fields["is_locked"] = ma.fields.Boolean(
                dump_default=False, load_default=False
            )

        # If a payload schema is defined, add it to the request schema
        if cls.payload_schema is not None:
            # TODO probably could be improved, probably in a wrong place
            cls._create_payload_cls()
            additional_fields["payload"] = ma.fields.Nested(
                cls.payload_schema_cls.from_dict(cls.payload_schema),
            )

        # Dynamically create a schema from the fields defined
        # by the payload schema dict.
        return RequestSchema.from_dict(additional_fields)

    @classmethod
    def marshmallow_schema(cls):
        """Create a schema for the entire request including payload."""
        type_id = cls.type_id
        if type_id not in current_requests._schema_cache:
            current_requests._schema_cache[type_id] = cls._create_marshmallow_schema()
        return current_requests._schema_cache[type_id]

    def generate_request_number(self, request, **kwargs):
        """Generate a new request number identifier.

        This method can be overridden in subclasses to create external identifiers
        according to a custom schema, using the information associated with the request
        (e.g. topic, receiver, creator).
        """
        from invenio_requests.records.models import RequestNumber

        return base32.encode(RequestNumber.next())

    def __str__(self):
        """Return str(self)."""
        # Value used by marshmallow schemas to represent the type.
        return self.type_id

    def __repr__(self):
        """Return repr(self)."""
        return f"<RequestType '{self.type_id}'>"
