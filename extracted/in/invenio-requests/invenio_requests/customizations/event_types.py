# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Base class for creating custom event types of requests."""

import inspect
from uuid import UUID

import marshmallow as ma
from flask import current_app
from invenio_i18n import lazy_gettext as _
from marshmallow import RAISE, Schema, ValidationError, fields, validate
from marshmallow.validate import OneOf
from marshmallow_utils import fields as utils_fields

from ..proxies import current_requests


def is_uuid(value):
    """Make sure value is a UUID."""
    try:
        UUID(value)
    except (ValueError, TypeError):
        raise ValidationError(
            _("The ID must be an Universally Unique IDentifier (UUID).")
        )


# FIXME: Ideally this should go to records-resources, with an extra argument specifying which config prefix to use.
class RequestsCommentsSanitizedHTML(utils_fields.SanitizedHTML):
    """A subclass of SanitizedHTML that dynamically configures allowed HTML tags and attributes based on application settings."""

    def __init__(self, *args, **kwargs):
        """Initializes RequestsCommentsSanitizedHTML with dynamic tag and attribute settings."""
        super().__init__(tags=None, attrs=None, *args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        """Deserialize value with dynamic HTML tags and attributes based on Flask app context or defaults."""
        self.tags = (
            current_app.config.get("ALLOWED_HTML_TAGS", [])
            + current_app.config["REQUESTS_COMMENTS_ALLOWED_EXTRA_HTML_TAGS"]
        )
        self.attrs = self.attrs = dict(
            **current_app.config.get("ALLOWED_HTML_ATTRS", {}),
            **current_app.config["REQUESTS_COMMENTS_ALLOWED_EXTRA_HTML_ATTRS"],
        )

        return super()._deserialize(value, attr, data, **kwargs)


class EventType:
    """Base class for event types."""

    type_id = None
    """The unique and constant identifier for this type of event."""

    payload_schema = None
    """Schema for supported payload fields.

    Define it as a dictionary of fields mapping or callable that returns a dictionary:

    .. code-block:: python

        payload_schema = {
            "content": fields.String(),
            # ...
        }

        # or a callable
        def payload_schema():
            return {
                "content": fields.String(),
                # ...
            }
    """

    payload_required = False
    """Require the event payload."""

    allow_children = False
    """Allow this event type to have children (parent-child relationships).

    If True, events of this type can have a parent_id and children.
    If False, attempting to set a parent_id will raise an error.
    """

    def __init__(self, payload=None):
        """Constructor."""
        self.payload = payload or {}

    def __eq__(self, other):
        """Implement comparison test."""
        if inspect.isclass(other):
            # if a class was passed rather than an instance, try to instantiate it
            other = other()
        if isinstance(other, EventType):
            return self.type_id == other.type_id
        elif isinstance(other, str):
            return self.type_id == other
        raise Exception("unknown value")

    def __str__(self):
        """Return str(self)."""
        # Value used by marshmallow schemas to represent the type.
        return self.type_id

    def __repr__(self):
        """Return repr(self)."""
        return f"<RequestEventType '{self.type_id}'>"

    @classmethod
    def _create_marshmallow_schema(cls):
        """Create a marshmallow schema for this request type."""
        # Avoid circular imports
        from invenio_requests.services.schemas import RequestEventSchema

        additional_fields = {}

        # Raise on invalid payload keys
        class PayloadBaseSchema(ma.Schema):
            class Meta:
                unknown = RAISE

        # If a payload schema is defined, add it to the request schema
        if cls.payload_schema is not None:
            payload_schema = cls.payload_schema
            if callable(cls.payload_schema):
                payload_schema = payload_schema()

            payload_required = False
            if cls.payload_required is not None:
                payload_required = cls.payload_required
            additional_fields["payload"] = ma.fields.Nested(
                PayloadBaseSchema.from_dict(payload_schema), required=payload_required
            )

        # Dynamically create a schema from the fields defined
        # by the payload schema dict.
        return RequestEventSchema.from_dict(additional_fields)

    @classmethod
    def marshmallow_schema(cls):
        """Create a schema for the entire request including payload."""
        type_id = cls.type_id
        if type_id not in current_requests._events_schema_cache:
            current_requests._events_schema_cache[type_id] = (
                cls._create_marshmallow_schema()
            )
        return current_requests._events_schema_cache[type_id]


class LogEventType(EventType):
    """Log event type."""

    type_id = "L"

    def payload_schema():
        """Return payload schema as a dictionary."""
        # we need to import here because of circular imports
        from invenio_requests.records.api import RequestEventFormat

        return dict(
            event=fields.String(validate=validate.Length(min=1)),
            content=utils_fields.SanitizedHTML(validate=validate.Length(min=1)),
            format=fields.Str(
                validate=validate.OneOf(choices=[e.value for e in RequestEventFormat]),
                load_default=RequestEventFormat.HTML.value,
            ),
        )


class ReviewersUpdatedType(EventType):
    """Reviewers updated event type."""

    type_id = "R"

    def payload_schema():
        """Return payload schema as a dictionary."""
        # we need to import here because of circular imports
        from invenio_requests.records.api import RequestEventFormat

        return dict(
            event=fields.String(validate=validate.Length(min=1)),
            content=utils_fields.SanitizedHTML(validate=validate.Length(min=1)),
            format=fields.Str(
                validate=validate.OneOf(choices=[e.value for e in RequestEventFormat]),
                load_default=RequestEventFormat.HTML.value,
            ),
            reviewers=fields.List(
                fields.Dict(
                    keys=fields.String(validate=OneOf(("user", "group"))),
                    values=fields.String(required=True),
                )
            ),
        )


class FileDetailsSchema(Schema):
    """File details schema using entity reference format.

    Files are referenced as {"file": "uuid"} to be compatible with
    the entity resolver pattern.
    """

    file_id = fields.String(validate=is_uuid, required=True)


class CommentEventType(EventType):
    """Comment event type."""

    type_id = "C"

    allow_children = True
    """Comments support parent-child relationships (replies to comments)."""

    def payload_schema():
        """Return payload schema as a dictionary."""
        # we need to import here because of circular imports
        from invenio_requests.records.api import RequestEventFormat

        return dict(
            content=RequestsCommentsSanitizedHTML(
                required=True, validate=validate.Length(min=1)
            ),
            format=fields.Str(
                validate=validate.OneOf(choices=[e.value for e in RequestEventFormat]),
                load_default=RequestEventFormat.HTML.value,
            ),
            files=fields.List(fields.Nested(FileDetailsSchema)),
        )

    payload_required = True
