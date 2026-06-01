# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2026 KTH Royal Institute of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation service."""

from flask import current_app
from invenio_accounts.models import Role
from invenio_i18n import gettext as _
from invenio_records_resources.services.uow import unit_of_work
from invenio_search.engine import dsl

from invenio_requests.customizations.user_moderation.user_moderation import (
    UserModerationRequest,
)
from invenio_requests.proxies import current_request_type_registry
from invenio_requests.services.user_moderation.errors import OpenRequestAlreadyExists

from ..results import EntityResolverExpandableField


class UserModerationRequestService:
    """Service for User Moderation requests."""

    def __init__(self, requests_service):
        """Service initialisation as a sub-service of requests."""
        self.requests_service = requests_service

    @property
    def request_type_cls(self):
        """User moderation request type."""
        return current_request_type_registry.lookup(UserModerationRequest.type_id)

    def _exists(self, identity, user_id):
        """Return the request id if an open request already exists, else None."""
        results = self.requests_service.search(
            identity,
            extra_filter=dsl.query.Bool(
                "must",
                must=[
                    dsl.Q("term", **{"type": self.request_type_cls.type_id}),
                    dsl.Q("term", **{"topic.user": user_id}),
                    dsl.Q("term", **{"is_open": True}),
                ],
            ),
        )
        return next(results.hits)["id"] if results.total > 0 else None

    def _create_request(self, identity, user_id, creator, receiver, data, uow):
        """Creates and submits the request."""
        if self._exists(identity, user_id):
            raise OpenRequestAlreadyExists

        # For user moderation, topic is the user to be moderated
        topic = {"user": str(user_id)}

        # Group references are role IDs.
        receiver = {"group": receiver}
        creator = {"group": creator}

        request_item = self.requests_service.create(
            identity,
            data,
            self.request_type_cls,
            receiver,
            creator,
            topic=topic,
            uow=uow,
        )

        # Permission for identity might be denied on 'submit'
        return self.requests_service.execute_action(
            identity=identity, id_=request_item.id, action="submit", data=data, uow=uow
        )

    @unit_of_work()
    def request_moderation(self, identity, user_id, data=None, uow=None, **kwargs):
        """Creates a UserModeration request and submits it."""
        REQUESTS_MODERATION_ROLE = current_app.config.get("REQUESTS_MODERATION_ROLE")
        role = Role.query.filter(Role.name == REQUESTS_MODERATION_ROLE).one_or_none()
        assert role, _("Moderation role must exist to enable user moderation requests.")

        data = data or {}

        return self._create_request(
            identity,
            user_id,
            creator=role.id,
            receiver=role.id,
            data=data,
            uow=uow,
        )

    @property
    def expandable_fields(self):
        """Get expandable fields."""
        return [
            EntityResolverExpandableField("created_by"),
            EntityResolverExpandableField("receiver"),
            EntityResolverExpandableField("topic"),
        ]
