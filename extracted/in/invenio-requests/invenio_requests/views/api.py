# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""View functions for the requests."""


def create_requests_bp(app):
    """Create requests blueprint."""
    ext = app.extensions["invenio-requests"]
    return ext.requests_resource.as_blueprint()


def create_request_events_bp(app):
    """Create request events blueprint."""
    ext = app.extensions["invenio-requests"]
    # `request_events_resource` is really the RequestCommentsResource
    return ext.request_events_resource.as_blueprint()


def create_request_files_bp(app):
    """Create request files blueprint."""
    ext = app.extensions["invenio-requests"]
    return ext.request_files_resource.as_blueprint()
