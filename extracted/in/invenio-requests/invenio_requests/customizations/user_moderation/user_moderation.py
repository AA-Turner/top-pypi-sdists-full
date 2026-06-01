# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation requests."""

from invenio_i18n import lazy_gettext as _
from invenio_users_resources.proxies import current_users_service
from marshmallow import ValidationError

from invenio_requests.customizations import RequestType, actions


class DeclineUserAction(actions.DeclineAction):
    """Represents a decline action used to block a user."""

    def execute(self, identity, uow):
        """Executes block action."""
        user = self.request.topic.resolve()
        try:
            current_users_service.block(identity, user.id, uow=uow)
        except ValidationError:
            # User already blocked so just ignore
            pass
        super().execute(identity, uow)


class AcceptUserAction(actions.AcceptAction):
    """Represents an accept action used to approve a user."""

    def execute(self, identity, uow):
        """Executes approve action."""
        user = self.request.topic.resolve()
        try:
            current_users_service.approve(identity, user.id, uow=uow)
        except ValidationError:
            # User already approved so just ignore
            pass
        super().execute(identity, uow)


class UserModerationRequest(RequestType):
    """Request to moderate a user."""

    type_id = "user-moderation"
    name = _("User moderation")

    creator_can_be_none = False
    topic_can_be_none = False
    allowed_creator_ref_types = ["group"]
    allowed_receiver_ref_types = ["group"]
    allowed_topic_ref_types = ["user"]

    available_actions = {
        "delete": actions.DeleteAction,
        "submit": actions.SubmitAction,
        "create": actions.CreateAction,
        "cancel": actions.CancelAction,
        # Custom implemented actions
        "accept": AcceptUserAction,
        "decline": DeclineUserAction,
    }
