# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-FileCopyrightText: 2026 KTH Royal Institute of Technology.
# SPDX-License-Identifier: MIT

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
    return file.send_file(as_attachment=True, restricted=True)
