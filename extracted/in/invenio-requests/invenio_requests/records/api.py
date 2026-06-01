# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2022 TU Wien.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""API classes for requests in Invenio."""

from enum import Enum
from functools import partial

from flask import current_app
from invenio_db import db
from invenio_files_rest.models import ObjectVersion
from invenio_records.dumpers import SearchDumper
from invenio_records.systemfields import ConstantField, DictField, ModelField
from invenio_records_resources.records.api import FileRecord, Record
from invenio_records_resources.records.systemfields import IndexField

from invenio_requests.records.systemfields.files import RequestFilesField

from ..customizations import RequestState as State
from .dumpers import (
    CalculatedFieldDumperExt,
    GrantTokensDumperExt,
    ParentChildDumperExt,
)
from .models import RequestEventModel, RequestFileMetadata, RequestMetadata
from .systemfields import (
    EntityReferenceField,
    EventTypeField,
    ExpiredStateCalculatedField,
    IdentityField,
    LastActivity,
    LastReply,
    RequestStateCalculatedField,
    RequestStatusField,
    RequestTypeField,
)
from .systemfields.entity_reference import (
    MultiEntityReferenceField,
    check_allowed_creators,
    check_allowed_receivers,
    check_allowed_references,
    check_allowed_reviewers,
    check_allowed_topics,
)


class RequestEventFormat(Enum):
    """Comment/content format enum."""

    HTML = "html"


class RequestEvent(Record):
    """A Request Event."""

    model_cls = RequestEventModel

    dumper = SearchDumper(extensions=[ParentChildDumperExt()])
    """Search dumper with parent-child relationship extension and files extension."""

    # Systemfields
    metadata = None

    schema = ConstantField("$schema", "local://requestevents/requestevent-v1.0.0.json")
    """The JSON Schema to use for validation."""

    request = ModelField(dump=False)
    """The request."""

    request_id = DictField("request_id")
    """The data-layer id of the related Request."""

    type = EventTypeField("type")
    """Request event type system field."""

    index = IndexField(
        "requestevents-requestevent-v1.0.0", search_alias="requestevents"
    )
    """The ES index used."""

    id = ModelField("id")
    """The data-layer id."""

    check_referenced = partial(
        check_allowed_references,
        lambda r: True,  # for system process for now
        lambda r: ["user", "email"],  # only users for now
    )

    created_by = EntityReferenceField("created_by", check_referenced)
    """Who created the event."""

    parent_id = DictField("parent_id")
    """The parent event ID for parent-child relationships."""

    def pre_commit(self):
        """Hook called before committing the record.

        Validates that children are allowed for this event type.
        """
        from .validators import validate_children_allowed

        validate_children_allowed(self)
        super().pre_commit()


def get_files_quota(record=None):
    """Get bucket quota configuration for request files."""
    # Returns quota_size and max_file_size from Flask config
    # with defaults (100MB total quota, 10MB max file size)
    return dict(
        quota_size=current_app.config["REQUESTS_FILES_DEFAULT_QUOTA_SIZE"],
        max_file_size=current_app.config["REQUESTS_FILES_DEFAULT_MAX_FILE_SIZE"],
    )


class RequestFile(FileRecord):
    """Request file API."""

    model_cls = RequestFileMetadata

    @classmethod
    def list_by_file_ids(cls, record_id, file_ids):
        """Get record files by record ID and file IDs."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.join(ObjectVersion).filter(
                cls.model_cls.record_id == record_id,
                ObjectVersion.file_id.in_(file_ids),
                cls.model_cls.is_deleted != True,
            )

            for obj in query:
                yield cls(obj.data, model=obj)


class Request(Record):
    """A generic request record."""

    event_cls = RequestEvent
    """The event class used for request events."""

    model_cls = RequestMetadata
    """The model class for the request."""

    dumper = SearchDumper(
        extensions=[
            CalculatedFieldDumperExt("is_closed"),
            CalculatedFieldDumperExt("is_open"),
            GrantTokensDumperExt("created_by", "receiver", "topic", "reviewers"),
        ]
    )
    """Search dumper with configured extensions."""

    number = IdentityField("number")
    """The request's number (i.e. external identifier)."""

    metadata = None
    """Disabled metadata field from the base class."""

    index = IndexField("requests-request-v1.0.0", search_alias="requests")
    """The Search index to use for the request."""

    schema = ConstantField("$schema", "local://requests/request-v1.0.0.json")
    """The JSON Schema to use for validation."""

    type = RequestTypeField("type")
    """System field for management of the request type.

    This field manages loading of the correct RequestType classes associated with
    `Requests`, based on their `request_type_id` field.
    This is important because the `RequestType` classes are the place where the
    custom request actions are registered.
    """

    topic = EntityReferenceField("topic", check_allowed_topics)
    """Topic (associated object) of the request."""

    created_by = EntityReferenceField("created_by", check_allowed_creators)
    """The entity that created the request."""

    receiver = EntityReferenceField("receiver", check_allowed_receivers)
    """The entity that will receive the request."""

    reviewers = MultiEntityReferenceField("reviewers", check_allowed_reviewers)
    """The entity that will receive the request."""

    status = RequestStatusField("status")
    """The current status of the request."""

    is_closed = RequestStateCalculatedField("status", expected_state=State.CLOSED)
    """Whether or not the current status can be seen as a 'closed' state."""

    is_open = RequestStateCalculatedField("status", expected_state=State.OPEN)
    """Whether or not the current status can be seen as an 'open' state."""

    expires_at = ModelField("expires_at")
    """Expiration date of the request."""

    is_expired = ExpiredStateCalculatedField("expires_at")
    """Whether or not the request is already expired."""

    last_reply = LastReply()
    """The complete last reply event in the request."""

    last_activity_at = LastActivity()
    """The last activity (derived from other fields)."""

    is_locked = DictField("is_locked")
    """Whether or not the request is locked."""

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)

    # Files NOT dumped or stored in JSON - internal only
    files = RequestFilesField(
        store=False,  # Don't serialize to request JSON
        dump=False,  # Don't include in dumps()
        file_cls=RequestFile,
        delete=False,  # Manual management via service
        create=False,  # Lazy initialization
        bucket_args=get_files_quota,  # Quota config
    )
