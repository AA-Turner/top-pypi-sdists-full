# SPDX-FileCopyrightText: 2023 CERN.
# SPDX-License-Identifier: MIT
"""User moderation requests service errors."""

from invenio_i18n import lazy_gettext as _


class InvalidCreator(Exception):
    """Request creator is invalid."""

    description = _("Invalid creator for user moderation request.")


class OpenRequestAlreadyExists(Exception):
    """An open request already exists for the user."""

    description = _("There is already an open moderation request for this user.")
