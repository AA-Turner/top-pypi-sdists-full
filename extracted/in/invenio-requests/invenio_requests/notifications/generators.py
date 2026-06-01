# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Notification generators."""

from invenio_access.permissions import system_identity
from invenio_notifications.models import Recipient
from invenio_notifications.services.generators import RecipientGenerator
from invenio_records.dictutils import dict_lookup
from invenio_search.engine import dsl
from invenio_users_resources.proxies import current_users_service

from ..proxies import current_events_service


def _get_user_id_from_entity(entity_field):
    """Extract user ID from an entity field (expanded or non-expanded).

    :param entity_field: Entity dictionary that may contain user ID
    :returns: User ID string or None

    Examples:
        Non-expanded: {"user": "1"} -> "1"
        Expanded: {"id": "1", "profile": {...}} -> "1"
        Email entity: "user@example.com" -> None
    """
    if not isinstance(entity_field, dict):
        # e.g. resolved email entity
        return None

    # non expanded looks like {"user": "1"}
    non_expanded_id = entity_field.get("user")
    # expanded looks like {"id": "1", "profile": {"full_name": "A user"}, ... }
    # checking for None as the profile might be an empty dict (user never set a profile)
    expanded_id = (
        entity_field["id"] if entity_field.get("profile") is not None else None
    )
    return non_expanded_id or expanded_id


class RequestParticipantsRecipient(RecipientGenerator):
    """Recipient generator based on request and it's events."""

    def __init__(self, key):
        """Ctor."""
        self.key = key

    def __call__(self, notification, recipients: dict):
        """Fetch users involved in request and add as recipients."""
        request = dict_lookup(notification.context, self.key)

        # checking if entities are users. If not, we will not add them.
        # TODO: add support for other entities? (e.g. groups)
        created_by_user_id = _get_user_id_from_entity(request["created_by"])
        receiver_user_id = _get_user_id_from_entity(request["receiver"])

        user_ids = set()
        if created_by_user_id:
            user_ids.add(created_by_user_id)

        if receiver_user_id:
            user_ids.add(receiver_user_id)

        # fetching all request events to get involved users
        request_events = current_events_service.scan(
            request_id=request["id"],
            identity=system_identity,
            extra_filter=dsl.Q("term", request_id=request["id"]),
        )

        user_ids.update(
            {
                re["created_by"]["user"]
                for re in request_events
                if re["created_by"].get("user")
            }
        )

        # remove system_user_id if present
        user_ids.discard(system_identity.id)

        filter_ = dsl.Q("terms", **{"id": list(user_ids)})
        users = current_users_service.scan(system_identity, extra_filter=filter_)
        for u in users:
            recipients[u["id"]] = Recipient(data=u)
        return recipients


class CommentRepliesParticipantsRecipient(RecipientGenerator):
    """Recipient generator for comment replies thread participants.

    Collects users who are participants in a specific comment thread:
    - Parent comment author
    - All reply (child comment) authors

    This is used for reply notifications to notify only those involved
    in the specific conversation thread, not all request participants.
    """

    def __init__(self, key, event_key):
        """Ctor."""
        self.key = key
        self.event_key = event_key

    def __call__(self, notification, recipients: dict):
        """Fetch users involved in the comment thread and add as recipients."""
        request_event = dict_lookup(notification.context, self.event_key)
        request = dict_lookup(notification.context, self.key)

        # Determine the parent comment ID
        # If this event has a parent_id, use it. Otherwise, this IS the parent.
        parent_id = request_event.get("parent_id") or request_event["id"]

        user_ids = set()

        # Get parent event and its creator
        try:
            parent_event = current_events_service.read(
                identity=system_identity, id_=parent_id
            ).to_dict()

            parent_user_id = _get_user_id_from_entity(
                parent_event.get("created_by", {})
            )
            if parent_user_id:
                user_ids.add(parent_user_id)
        except Exception:
            # Parent not found or error reading, skip
            pass

        # Get all replies to the parent event for the given request
        replies_filter = dsl.Q(
            "bool",
            must=[
                dsl.Q("term", request_id=request["id"]),
                dsl.Q("term", parent_id=parent_id),
            ],
        )
        # Get all children (replies) and their creators
        # NOTE: To be improved in https://github.com/inveniosoftware/invenio-requests/issues/508
        children_events = current_events_service.scan(
            identity=system_identity,
            request_id=request["id"],
            extra_filter=replies_filter,
        )

        user_ids.update(
            {
                child["created_by"]["user"]
                for child in children_events
                if child.get("created_by", {}).get("user")
            }
        )

        # Remove system user if present
        user_ids.discard(system_identity.id)

        # Fetch users and add as recipients
        if user_ids:
            filter_ = dsl.Q("terms", **{"id": list(user_ids)})
            users = current_users_service.scan(system_identity, extra_filter=filter_)
            for u in users:
                recipients[u["id"]] = Recipient(data=u)

        return recipients
