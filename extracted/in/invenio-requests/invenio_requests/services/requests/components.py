# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Component for creating request numbers."""

from uuid import UUID

from flask import current_app
from invenio_i18n import _
from invenio_records_resources.services.errors import ValidationErrorGroup
from invenio_records_resources.services.records.components import (
    DataComponent,
    ServiceComponent,
)
from marshmallow import ValidationError

from invenio_requests.customizations.event_types import (
    LogEventType,
    ReviewersUpdatedType,
)
from invenio_requests.proxies import (
    current_events_service,
    current_request_files_service,
)
from invenio_requests.records.api import RequestFile


class RequestNumberComponent(ServiceComponent):
    """Component for assigning request numbers to new requests."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create identifier when record is created."""
        type(record).number.assign(record)


class EntityReferencesComponent(ServiceComponent):
    """Component for initializing a request's entity references."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Initialize the entity reference fields of a request."""
        for field in ("created_by", "receiver", "topic"):
            if field in kwargs:
                setattr(record, field, kwargs[field])


class RequestDataComponent(DataComponent):
    """Request variant of DataComponent using dynamic schema."""

    def update(self, identity, data=None, record=None, **kwargs):
        """Update an existing record (request)."""
        if record.status == "created":
            keys = ("title", "description", "payload", "receiver", "topic")
        else:
            keys = ("title", "description")
        if current_app.config["REQUESTS_LOCKING_ENABLED"]:
            keys = keys + ("is_locked",)

        for k in keys:
            if k in data:
                record[k] = data[k]


class RequestReviewersComponent(ServiceComponent):
    """Component for handling request reviewers."""

    def _reviewers_updated(self, previous_reviewers, new_reviewers):
        """Determine reviewers change type: added, removed, updated, unchanged."""

        def _normalize(reviewers):
            """Convert reviewers into a set of string identifiers."""
            normalized = set()
            for r in reviewers:
                if "user" in r:
                    normalized.add(f"user:{r['user']}")
                elif "group" in r:
                    normalized.add(f"group:{r['group']}")
            return normalized

        prev_set = _normalize(previous_reviewers)
        new_set = _normalize(new_reviewers)

        added = new_set - prev_set
        removed = prev_set - new_set

        if added and not removed:
            return "added", [
                r
                for r in new_reviewers
                if (
                    ("user" in r and f"user:{r['user']}" in added)
                    or ("group" in r and f"group:{r['group']}" in added)
                )
            ]
        elif removed and not added:
            return "removed", [
                r
                for r in previous_reviewers
                if (
                    ("user" in r and f"user:{r['user']}" in removed)
                    or ("group" in r and f"group:{r['group']}" in removed)
                )
            ]
        elif added and removed:
            return "updated", list(new_reviewers)
        else:
            return "unchanged", list(new_reviewers)

    def _validate_reviewers(self, reviewers):
        """Validate the reviewers data."""
        reviewers_enabled = current_app.config["REQUESTS_REVIEWERS_ENABLED"]
        reviewers_groups_enabled = current_app.config["USERS_RESOURCES_GROUPS_ENABLED"]
        max_reviewers = current_app.config["REQUESTS_REVIEWERS_MAX_NUMBER"]

        if not reviewers_enabled:
            raise ValidationError(_("Reviewers are not enabled for this request type."))
        if not reviewers_groups_enabled:
            for reviewer in reviewers:
                if "group" in reviewer:
                    raise ValidationError(_("Group reviewers are not enabled."))

        if len(reviewers) > max_reviewers:
            raise ValidationError(
                _(f"You can only add up to {max_reviewers} reviewers.")
            )

    def _ensure_no_duplicates(self, reviewers):
        """Ensure there are no duplicate reviewers.

        The code is preserving the original order of reviewers.
        """
        seen = set()
        unique_objs = []
        for d in reviewers:
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                unique_objs.append(d)
        return unique_objs

    def update(self, identity, data=None, record=None, uow=None, **kwargs):
        """Update the reviewers of a request."""
        if "reviewers" in data:
            # ensure there are not duplicates
            new_reviewers = self._ensure_no_duplicates(data["reviewers"])
            self._validate_reviewers(new_reviewers)
            self.service.require_permission(identity, f"action_accept", request=record)

            event_type, updated_reviewers = self._reviewers_updated(
                record.get("reviewers", []), new_reviewers
            )
            if not event_type == "unchanged":
                event = ReviewersUpdatedType(
                    payload=dict(
                        event="reviewers_updated",
                        content=_(f"{event_type} a reviewer"),
                        reviewers=updated_reviewers,
                    )
                )
                _data = dict(payload=event.payload)
                current_events_service.create(
                    identity, record.id, _data, event, uow=uow
                )
            record["reviewers"] = new_reviewers


class RequestPayloadComponent(DataComponent):
    """Request variant of DataComponent using dynamic schema."""

    def update(self, identity, data=None, record=None, **kwargs):
        """Update an existing request payload based on permissions."""
        payload = {}
        # take permissions if exist
        permissions = getattr(
            record.type.payload_schema_cls, "field_load_permissions", {}
        )
        if permissions:
            for key in data["payload"]:
                if key in permissions:
                    # permissions should have been checked by now already
                    # so we can assign the new data
                    payload[key] = data["payload"][key]
                else:
                    # keep the old data - no permission to change it
                    # workaround for the lack of patch method
                    payload[key] = record["payload"][key]
            record["payload"] = payload


class RequestLockComponent(ServiceComponent):
    """Component for locking a request."""

    def lock_request(self, identity, record=None, uow=None, **kwargs):
        """Lock a request."""
        event = LogEventType(payload=dict(event="locked"))
        _data = dict(payload=event.payload)
        current_events_service.create(identity, record.id, _data, event, uow=uow)

    def unlock_request(self, identity, record=None, uow=None, **kwargs):
        """Unlock a request."""
        event = LogEventType(payload=dict(event="unlocked"))
        _data = dict(payload=event.payload)
        current_events_service.create(identity, record.id, _data, event, uow=uow)


class RequestCommentFileValidationComponent(ServiceComponent):
    """Component validating files referenced in a request comment."""

    def _check_file_references(
        self, identity, data=None, event=None, uow=None, **kwargs
    ):
        # The new list of files received from the current service call.
        comment_file_ids_next = [
            UUID(file_next["file_id"])
            for file_next in data.get("payload", {}).get("files", [])
        ]

        # Retrieve the existing (persisted) list of files with the given file IDs which are associated to the request.
        request_files_existing = RequestFile.list_by_file_ids(
            event["request_id"], comment_file_ids_next
        )
        request_file_ids_existing = {
            request_file_existing.file.file_id
            for request_file_existing in request_files_existing
        }

        # Check if all the file IDs exist in the database.
        error_messages = []
        for idx, comment_file_id_next in enumerate(comment_file_ids_next):
            if comment_file_id_next not in request_file_ids_existing:
                error_messages.append(
                    {
                        "messages": [_(f"File {str(comment_file_id_next)} not found.")],
                        "field": f"payload.files[{idx}]",
                    }
                )
        if error_messages:
            raise ValidationErrorGroup(error_messages)

    def create(self, identity, data=None, event=None, errors=None, uow=None, **kwargs):
        """Ensures all referenced files exist."""
        self._check_file_references(identity, data=data, event=event, uow=uow, **kwargs)

    def update_comment(
        self, identity, data=None, event=None, request=None, uow=None, **kwargs
    ):
        """Ensures all referenced files exist."""
        self._check_file_references(identity, data=data, event=event, uow=uow, **kwargs)


class RequestCommentFileCleanupComponent(ServiceComponent):
    """Component deleting files which references were removed form a request comment."""

    def update_comment(
        self, identity, data=None, event=None, request=None, uow=None, **kwargs
    ):
        """Delete files not referenced anymore in a comment."""
        # The existing (persisted) list of files associated to the comment.
        file_ids_previous = [
            file_previous["file_id"]
            for file_previous in event["payload"].get("files", [])
        ]

        # The new list of files received from the current service call.
        file_ids_next = [
            file_next["file_id"] for file_next in data["payload"].get("files", [])
        ]

        # Delete files from the persisted list which are not in the new list anymore.
        for file_id_previous in file_ids_previous:
            if file_id_previous not in file_ids_next:
                current_request_files_service.delete_file(
                    identity, event["request_id"], file_id=file_id_previous, uow=uow
                )

    def delete_comment(
        self, identity, data=None, event=None, request=None, uow=None, **kwargs
    ):
        """Delete files not associated to a deleted comment."""
        # The existing (persisted) list of files associated to the comment.
        file_ids_previous = [
            file_previous["file_id"]
            for file_previous in event["payload"].get("files", [])
        ]

        # Delete all the files.
        for file_id_previous in file_ids_previous:
            current_request_files_service.delete_file(
                identity, event["request_id"], file_id=file_id_previous, uow=uow
            )
