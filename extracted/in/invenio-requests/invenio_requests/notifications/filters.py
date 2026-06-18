# SPDX-FileCopyrightText: 2023 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Recipient filters for notifications."""

from invenio_notifications.services.filters import RecipientFilter
from invenio_records.dictutils import dict_lookup


class UserRecipientFilter(RecipientFilter):
    """Recipient filter based on user."""

    def __init__(self, key):
        """Initialize with key for user lookup."""
        super().__init__()
        self._key = key

    def __call__(self, notification, recipients):
        """Filter recipients."""
        user = dict_lookup(notification.context, self._key)
        if not isinstance(user, dict):
            # e.g. resolved email entity
            return recipients

        # lookup (non) expanded user field
        user_id = user.get("user") or user.get("id")

        if user_id in recipients:
            del recipients[user_id]

        return recipients
