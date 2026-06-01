# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Custom exceptions used in the Invenio-Requests module."""

from invenio_i18n import lazy_gettext as _
from invenio_records_resources.services.errors import PermissionDeniedError


class ActionError(Exception):
    """Exception indicating an error related to the action."""

    def __init__(self, action, reason):
        """Constructor.

        :param action: The name of the action in question.
        :param reason: Description of what went wrong.
        """
        self.action = action
        self.reason = reason

    def __str__(self):
        """Return str(self)."""
        return f"Error for action '{self.action}': {self.reason}"


class NoSuchActionError(ActionError):
    """There was no such action available."""

    def __init__(self, action, reason=None):
        """Constructor.

        :param action: The name of the action.
        """
        reason = reason or "No such action available"
        super().__init__(action, reason)


class CannotExecuteActionError(ActionError):
    """The selected action could not be executed."""

    def __init__(self, action, reason=None):
        """Constructor.

        :param action: The name of the action.
        """
        reason = reason or "Could not execute the action"
        super().__init__(action, reason)


class RequestLockedError(PermissionDeniedError):
    """Exception indicating that the request is locked."""

    def __init__(self, description=None):
        """Constructor.

        :param message: The message to display.
        """
        self._description = description or _("The request is locked.")

    @property
    def description(self):
        """Return the description."""
        return self._description

    def __str__(self):
        """Return str(self)."""
        return self.description


class RequestEventPermissionError(PermissionDeniedError):
    """Exception indicating that the request event permission is denied."""

    def __init__(self, description=None):
        """Constructor.

        :param message: The message to display.
        """
        self._description = description or _("Permission denied.")

    @property
    def description(self):
        """Return the description."""
        return self._description

    def __str__(self):
        """Return str(self)."""
        return self.description


class ChildrenNotSupportedError(Exception):
    """Exception raised when children are attempted on an event type that doesn't support it."""

    def __init__(self, event_type, message=None):
        """Constructor.

        :param event_type: The event type that doesn't support children.
        :param message: Optional custom error message.
        """
        self.event_type = event_type
        self.message = message or _(
            (f"Event type '{event_type}' does not support event replies.")
        )
        super().__init__(self.message)


class NestedChildrenNotAllowedError(Exception):
    """Exception raised when attempting to create nested children (reply to a reply)."""

    def __init__(self, message=None):
        """Constructor.

        :param message: Optional custom error message.
        """
        self.message = message or _(
            (
                "Nested children are not allowed. "
                "You cannot reply to a comment that is already a reply. "
                "Only one level of parent-child relationships is supported."
            )
        )
        super().__init__(self.message)
