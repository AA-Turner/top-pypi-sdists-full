# SPDX-FileCopyrightText: 2025 CERN.
# SPDX-License-Identifier: MIT

"""Requests files errors."""

from invenio_i18n import gettext as _


class RequestFileSizeLimitError(Exception):
    """The provided file size exceeds limit."""

    def __init__(self):
        """Initialise error."""
        super().__init__(_("File size exceeds limit"))


class RequestFileNotFoundError(Exception):
    """The provided file is not found."""

    def __init__(self):
        """Initialise error."""
        super().__init__(_("File not found"))


class RequestFileArgumentMissingError(Exception):
    """The provided file argument is missing."""

    def __init__(self):
        """Initialise error."""
        super().__init__(_("Missing required argument file_key or file_id"))
