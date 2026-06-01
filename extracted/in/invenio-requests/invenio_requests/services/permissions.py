# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2026 CESNET, z.s.p.o.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request permissions."""

from invenio_administration.generators import Administration
from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    IfConfig,
    SameAs,
    SystemProcess,
    SystemProcessWithoutSuperUser,
)

from .generators import Commenter, Creator, IfLocked, Receiver, Reviewers, Status, Topic


class PermissionPolicy(RecordPermissionPolicy):
    """Permission policy."""

    # Ability in general to create requests (not which request you can create)
    can_create = [AuthenticatedUser(), SystemProcess()]
    # Just about ability to perform a search (not what requests you can access)
    can_search = [AuthenticatedUser(), SystemProcess()]

    can_search_user_requests = SameAs("can_search")

    # Read/update/delete action deals with requests in **multiple states**, and
    # thus must take the request status into account.
    can_read = [
        Status(["created"], [Creator()]),
        Status(
            [
                "submitted",
                "deleted",
                "cancelled",
                "expired",
                "accepted",
                "declined",
            ],
            [Creator(), Receiver(), Reviewers(), Topic()],
        ),
        Administration(),
        SystemProcess(),
    ]

    can_update = [
        Administration(),
        SystemProcess(),
        Status(["created"], [Creator()]),
        Status(["submitted"], [Creator(), Receiver()]),
    ]

    can_manage_access_options = [Disable()]

    can_action_delete = [
        Status(["created"], [Creator()]),
        Status(
            ["submitted", "deleted", "cancelled", "expired", "accepted", "declined"],
            [Disable()],
        ),
        Administration(),
        SystemProcess(),
    ]

    # Submit, cancel, expire, accept and decline actions only deals
    # with requests in a **single state** and thus doesn't need to take the
    # request status into account.
    can_action_submit = [Creator(), SystemProcess()]
    can_action_cancel = SameAs("can_action_submit")
    # `SystemProcessWithoutSuperUser`: expire is an automatic action done only by
    # the system, therefore the `superuser-action` must be explicitly excluded
    # as it's added by default to any permission.
    can_action_expire = [SystemProcessWithoutSuperUser()]
    can_action_accept = [Receiver(), SystemProcess()]
    can_action_decline = SameAs("can_action_accept")

    can_lock_request = [
        IfConfig(
            "REQUESTS_LOCKING_ENABLED",
            then_=[Receiver(), SystemProcess(), Administration()],
            else_=[Disable()],
        ),
    ]

    # Request events/comments
    # Events are in most cases protected by the associated request.
    can_update_comment = [
        IfConfig(
            "REQUESTS_LOCKING_ENABLED",
            then_=[
                IfLocked(then_=[Administration()], else_=[Commenter()]),
                SystemProcess(),
            ],
            else_=[Commenter(), Administration(), SystemProcess()],
        ),
    ]
    can_delete_comment = [
        Commenter(),
        SystemProcess(),
    ]
    # If you can read the request you can create events for the request.
    can_create_comment = [
        IfConfig(
            "REQUESTS_LOCKING_ENABLED",
            then_=[
                IfLocked(
                    then_=[Administration()],
                    else_=SameAs("can_read"),
                ),
                SystemProcess(),
            ],
            else_=SameAs("can_read"),
        ),
    ]

    # If you can create a comment, you can reply to a comment.
    can_reply_comment = SameAs("can_create_comment")

    # Needed by the search events permission because a permission_action must
    # be provided to create_search(), but the event search is already protected
    # by request's can_read, thus we use a dummy permission for the search.
    can_unused = [AnyUser()]

    # Manage (Upload/Delete) files: Same as creating comments on the request.
    can_manage_files = can_create_comment

    # Read (View/Download) files: Same permission as viewing the request and its timeline.
    can_read_files = can_read
