# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Notification builders."""

from invenio_notifications.models import Notification
from invenio_notifications.registry import EntityResolverRegistry
from invenio_notifications.services.builders import NotificationBuilder
from invenio_notifications.services.filters import KeyRecipientFilter
from invenio_notifications.services.generators import EntityResolve, UserEmailBackend
from invenio_users_resources.notifications.filters import UserPreferencesRecipientFilter
from invenio_users_resources.notifications.generators import (
    EmailRecipient,
    IfEmailRecipient,
)

from invenio_requests.notifications.filters import UserRecipientFilter

from .generators import (
    CommentRepliesParticipantsRecipient,
    RequestParticipantsRecipient,
)


class CommentRequestEventCreateNotificationBuilder(NotificationBuilder):
    """Notification builder for comment request event creation."""

    type = "comment-request-event.create"

    @classmethod
    def build(cls, request, request_event):
        """Build notification with context."""
        return Notification(
            type=cls.type,
            context={
                "request": EntityResolverRegistry.reference_entity(request),
                "request_event": EntityResolverRegistry.reference_entity(request_event),
            },
        )

    context = [
        EntityResolve(key="request"),
        EntityResolve(key="request.created_by"),
        EntityResolve(key="request.receiver"),
        EntityResolve(key="request_event"),
        EntityResolve(key="request_event.created_by"),
    ]

    recipients = [
        RequestParticipantsRecipient(key="request"),
        IfEmailRecipient(
            key="request.created_by",
            then_=[EmailRecipient(key="request.created_by")],
            else_=[],
        ),
    ]

    recipient_filters = [
        # remove a possible email recipient
        KeyRecipientFilter(key="request_event.created_by"),
        # do not send notification to user creating the comment
        UserRecipientFilter(key="request_event.created_by"),
        UserPreferencesRecipientFilter(),
    ]

    recipient_backends = [
        UserEmailBackend(),
    ]


class CommentRequestEventReplyNotificationBuilder(
    CommentRequestEventCreateNotificationBuilder
):
    """Notification builder for reply creation.

    Notifies only participants in the specific comment thread
    (parent author and other reply authors), not all request participants.
    """

    type = "comment-request-event.reply"

    recipients = [
        CommentRepliesParticipantsRecipient(event_key="request_event", key="request"),
    ]
