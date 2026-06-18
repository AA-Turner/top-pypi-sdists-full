# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-License-Identifier: MIT

"""Proxies for accessing the currently instantiated requests extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_requests = LocalProxy(lambda: current_app.extensions["invenio-requests"])
"""Proxy for the instantiated requests extension."""

current_request_type_registry = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].request_type_registry
)
"""Proxy for the instantiated request type registry."""

current_event_type_registry = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].event_type_registry
)
"""Proxy for the instantiated request type registry."""

current_requests_service = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].requests_service
)
"""Proxy to the instantiated requests service."""

current_request_files_service = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].request_files_service
)
"""Proxy to the instantiated request files service."""

current_events_service = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].request_events_service
)
"""Proxy to the instantiated requests service."""

current_requests_resource = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].requests_resource
)
"""Proxy to the instantiated requests resource."""

current_user_moderation_service = LocalProxy(
    lambda: current_app.extensions["invenio-requests"].user_moderation_requests_service
)
"""Proxy to the instantiated user moderation requests service."""
