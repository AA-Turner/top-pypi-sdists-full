# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 CERN.
# Copyright (C) 2021 - 2022 TU Wien.
# Copyright (C) 2025 KTH Royal Institute of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for generic and customizable requests."""

from invenio_i18n import lazy_gettext as _
from invenio_users_resources.entity_resolvers import GroupResolver, UserResolver

from invenio_requests.services.requests import facets
from invenio_requests.services.requests.components import (
    RequestCommentFileCleanupComponent,
    RequestCommentFileValidationComponent,
)

from .customizations import CommentEventType, LogEventType, ReviewersUpdatedType
from .services.permissions import PermissionPolicy

REQUESTS_PERMISSION_POLICY = PermissionPolicy
"""Override the default requests/comments permission policy."""

REQUESTS_REGISTERED_TYPES = []
"""Configuration for registered Request Types."""

REQUESTS_REGISTERED_EVENT_TYPES = [
    LogEventType(),
    CommentEventType(),
    ReviewersUpdatedType(),
]
"""Configuration for registered Request Event Types."""

REQUESTS_ENTITY_RESOLVERS = [UserResolver(), GroupResolver()]
"""Registered resolvers for resolving/creating references in request metadata."""

REQUESTS_ROUTES = {
    "download_file_html": "/requests/<uuid:pid_value>/files/<path:file_key>",
}
"""Invenio requests ui endpoints."""

REQUESTS_SEARCH = {
    "facets": ["type", "status"],
    "sort": ["bestmatch", "newest", "oldest", "newestactivity", "oldestactivity"],
}
"""Requests search default configuration."""

REQUESTS_SORT_OPTIONS = {
    "bestmatch": dict(
        title=_("Best match"),
        fields=["_score"],  # search defaults to desc on `_score` field
    ),
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
    "oldest": dict(
        title=_("Oldest"),
        fields=["created"],
    ),
    "newestactivity": dict(
        title=_("Newest activity"),
        fields=["-last_activity_at"],
    ),
    "oldestactivity": dict(
        title=_("Oldest activity"),
        fields=["last_activity_at"],
    ),
}
"""Definitions of available request sort options."""

REQUESTS_FACETS = {
    "type": {
        "facet": facets.type,
        "ui": {
            "field": "type",
        },
    },
    "status": {
        "facet": facets.status,
        "ui": {
            "field": "status",
        },
    },
}
"""Invenio requests facets."""

REQUESTS_TIMELINE_PAGE_SIZE = 10
"""Amount of items per page on the request details timeline"""


REQUESTS_MODERATION_ROLE = "administration-moderation"
"""ID of the Role used for moderation."""


#
# User moderation administration
#
REQUESTS_USER_MODERATION_SEARCH = {
    "facets": ["status", "is_open"],
    "sort": ["bestmatch", "newest", "oldest"],
}
"""Community requests search configuration (i.e list of community requests)"""

REQUESTS_USER_MODERATION_SORT_OPTIONS = {
    "bestmatch": dict(
        title=_("Best match"),
        fields=["_score"],  # ES defaults to desc on `_score` field
    ),
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
    "oldest": dict(
        title=_("Oldest"),
        fields=["created"],
    ),
}
"""Definitions of available record sort options."""

REQUESTS_USER_MODERATION_FACETS = {
    "status": {
        "facet": facets.status,
        "ui": {
            "field": "status",
        },
    },
    "is_open": {"facet": facets.is_open, "ui": {"field": "is_open"}},
}
"""Available facets defined for this module."""

REQUESTS_REVIEWERS_ENABLED = False
"""Enable reviewers for requests."""

REQUESTS_REVIEWERS_MAX_NUMBER = 15
"""Maximum number of reviewers allowed for a request."""

REQUESTS_LOCKING_ENABLED = False
"""Enable locking/unlocking for request conversations."""

REQUESTS_COMMENT_PREVIEW_LIMIT = 5
"""Number of most recent child comments to inline in parent's search index.

This limits the size of indexed documents when comments have many replies.
Additional replies can be loaded via pagination.
"""

REQUESTS_FILES_DEFAULT_QUOTA_SIZE = 100 * 10**6  # 100MB
REQUESTS_FILES_DEFAULT_MAX_FILE_SIZE = 10 * 10**6  # 10MB

REQUESTS_EVENTS_SERVICE_COMPONENTS = [
    RequestCommentFileValidationComponent,
    RequestCommentFileCleanupComponent,
]

REQUESTS_COMMENTS_ALLOWED_EXTRA_HTML_TAGS = ["img"]
"""Extend allowed HTML tags list for requests comments content."""

REQUESTS_COMMENTS_ALLOWED_EXTRA_HTML_ATTRS = {
    "img": ["src", "alt", "width", "height"],
}
"""Extend allowed HTML attrs list for requests comments content."""
