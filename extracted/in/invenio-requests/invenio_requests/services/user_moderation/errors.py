# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation requests service errors."""

from invenio_i18n import lazy_gettext as _


class InvalidCreator(Exception):
    """Request creator is invalid."""

    description = _("Invalid creator for user moderation request.")


class OpenRequestAlreadyExists(Exception):
    """An open request already exists for the user."""

    description = _("There is already an open moderation request for this user.")
