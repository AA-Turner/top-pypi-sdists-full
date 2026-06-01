# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
