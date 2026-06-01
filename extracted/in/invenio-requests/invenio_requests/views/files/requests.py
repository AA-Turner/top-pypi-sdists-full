# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request Files views module."""

from flask import g

from invenio_requests.proxies import current_request_files_service


def read_file(pid_value, file_key):
    """Read a file."""
    file = current_request_files_service.read_file(
        identity=g.identity,
        id_=pid_value,
        file_key=file_key,
    )
    return file.send_file(as_attachment=True, restricted=True), 200
