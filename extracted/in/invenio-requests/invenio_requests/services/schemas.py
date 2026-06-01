# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 - 2022 TU Wien.
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Request Event Schemas."""

from datetime import timezone

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import (
    RAISE,
    Schema,
    fields,
)
from marshmallow_utils import fields as utils_fields
from marshmallow_utils.context import context_schema
from marshmallow_utils.fields import Links

from invenio_requests.proxies import current_requests

from ..customizations.event_types import CommentEventType, EventType


class EventTypeMarshmallowField(fields.Str):
    """Serializes event type from `EventType` to string."""

    def _serialize(self, value, attr, data, **kwargs):
        if isinstance(value, EventType):
            value = value.type_id
        return value


class RequestEventSchema(BaseRecordSchema):
    """Base Event schema that other schemas should inherit from."""

    type = EventTypeMarshmallowField(dump_only=True)
    created_by = fields.Dict(dump_only=True)
    permissions = fields.Method("get_permissions", dump_only=True)
    parent_id = fields.String(allow_none=True, dump_only=True)
    children = fields.List(fields.Dict(), dump_only=True)

    def get_permissions(self, obj):
        """Return permissions to act on comments or empty dict."""
        service = current_requests.request_events_service

        current_identity = context_schema.get()["identity"]
        current_request = context_schema.get().get("request", None)
        permissions = {}

        if current_request is None:
            return {}

        if obj.type == CommentEventType:
            permissions["can_update_comment"] = service.check_permission(
                current_identity,
                "update_comment",
                event=obj,
                request=current_request,
            )
            permissions["can_delete_comment"] = service.check_permission(
                current_identity,
                "delete_comment",
                event=obj,
                request=current_request,
            )
        else:
            # Other event types (e.g. log events) might be deleted comments, for which these permissions are inherently False.
            permissions["can_update_comment"] = False
            permissions["can_delete_comment"] = False

        permissions["can_reply_comment"] = service.check_permission(
            current_identity,
            "reply_comment",
            event=obj,
            request=current_request,
        )

        return permissions


class RequestFileSchema(Schema):
    """Schema for file requests."""

    id = fields.UUID(attribute="file.file_id", dump_only=True)
    key = fields.String(dump_only=True)
    checksum = fields.String(attribute="file.checksum", dump_only=True)
    mimetype = fields.String(attribute="file.mimetype", dump_only=True)
    size = fields.Integer(attribute="file.size", dump_only=True)
    metadata = fields.Dict(attribute="model.data", dump_only=True)
    links = Links()


class RequestSchema(BaseRecordSchema):
    """Schema for requests.

    Note that the payload schema and the entity reference schemas (i.e. creator,
    receiver, and topic) are dynamically constructed and injected into this schema.
    """

    # load and dump
    type = fields.String()
    title = utils_fields.SanitizedUnicode(dump_default="")
    description = utils_fields.SanitizedUnicode()

    # Dump-only
    number = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    is_closed = fields.Boolean(dump_only=True)
    is_open = fields.Boolean(dump_only=True)
    expires_at = utils_fields.TZDateTime(
        timezone=timezone.utc, format="iso", dump_only=True
    )
    is_expired = fields.Boolean(dump_only=True)

    last_reply = fields.Nested(RequestEventSchema, dump_only=True)

    last_activity_at = utils_fields.TZDateTime(
        timezone=timezone.utc, format="iso", dump_only=True
    )

    class Meta:
        """Schema meta."""

        unknown = RAISE


class GenericRequestSchema(RequestSchema):
    """Generic request schema.

    CAUTION: This schema should not be used for the final validation of input
    data. Use the request type's own defined schema instead.

    This schema can be used in situations where you need to do basic validation
    or dumping of a request without the payload.

    This is used e.g. in Invenio-RDM-Records for dumping a request without
    having to know the specific request type.
    """

    created_by = fields.Dict()
    receiver = fields.Dict()
    topic = fields.Dict()
