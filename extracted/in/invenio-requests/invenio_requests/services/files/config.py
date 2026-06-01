# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Requests service configuration."""

from invenio_records_resources.services import (
    EndpointLink,
    FileServiceConfig,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig
from invenio_records_resources.services.files.links import FileEndpointLink
from invenio_records_resources.services.records.results import RecordItem

from ...records.api import Request, RequestFile
from ..permissions import PermissionPolicy
from ..schemas import RequestFileSchema


class RequestFileItem(RecordItem):
    """RequestFile result item."""

    @property
    def id(self):
        """Id property."""
        return self._record.id


class RequestFileEndpointLink(EndpointLink):
    """Rendering of a file link with specific vars expansion."""

    @staticmethod
    def vars(obj, vars):
        """Variables for the endpoint expansion.

        WARNING: This is the *direct* translation of the previous deprecated
                 RequestFileLink to use EndpointLink. As such, it keeps the
                 behavior and shortcomings of the *original* implementation
                 with respect to vars generation, chiefly: touching the DB to
                 get the request id (!). Refactoring to pass the request id
                 to the context (vars) should alleviate that, but it is outside
                 of scope of this PR.

        :param obj: api.RequestFile
        :param vars: dict
        """
        vars.update({"id": obj.model.record_id, "key": obj.key})


class RequestFilesServiceConfig(FileServiceConfig, ConfiguratorMixin):
    """Requests Files service configuration."""

    service_id = "request_files"

    # common configuration
    permission_action_prefix = ""
    permission_policy_cls = FromConfig(
        "REQUESTS_PERMISSION_POLICY", default=PermissionPolicy
    )
    result_item_cls = RequestFileItem

    # request files-specific configuration
    record_cls = RequestFile  # needed for model queries
    schema = RequestFileSchema  # stored in the API classes, for customization
    request_cls = Request
    indexer_queue_name = "files"

    # links configuration / ResultItem configurations
    links_item = {
        "self": RequestFileEndpointLink("request_files.delete", params=["id", "key"]),
        "content": RequestFileEndpointLink("request_files.read", params=["id", "key"]),
        "download_html": EndpointLink(
            "invenio_requests_files.read_file",
            params=["pid_value", "file_key"],
            vars=lambda obj, vars: (
                vars.update(
                    # Same WARNING as in RequestFileEndpointLink applies
                    {"pid_value": obj.model.record_id, "file_key": obj.key}
                )
            ),
        ),
    }

    file_links_item = {
        "self": FileEndpointLink("request_files.read", params=["pid_value", "key"]),
    }

    components = FromConfig(
        "REQUESTS_FILES_SERVICE_COMPONENTS",
        default=[],
    )
